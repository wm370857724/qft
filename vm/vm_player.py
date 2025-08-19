#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟机端自动播放脚本 (优化版 - 单窗口更新)
"""

import os
import time
import hashlib
import subprocess
import sys
import signal
import atexit
import threading
from typing import List, Tuple, Optional
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap

# 全局变量存储当前打开的进程
current_process: Optional[subprocess.Popen] = None

# 用于线程间通信的信号
class ImageUpdater(QObject):
    update_signal = pyqtSignal(str)

class FullScreenBMPViewer(QMainWindow):
    def __init__(self, screen_index=1, initial_image="image.bmp"):
        super().__init__()

        # 获取多显示器配置
        screens = QApplication.screens()
        if len(screens) <= screen_index:
            print(f"错误：系统只有{len(screens)}个显示器，无法使用2号屏幕")
            sys.exit(1)

        # 设置目标屏幕的几何参数
        target_screen = screens[screen_index]
        screen_geometry = target_screen.geometry()

        # 配置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(screen_geometry)

        # 创建图片显示标签
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())

        # 加载并显示初始图片
        self.load_image(initial_image)

        # 窗口关闭快捷键
        self.label.setFocus()
        self.label.keyPressEvent = self.keyPressEvent

    def load_image(self, image_path):
        """加载并居中显示BMP图片（不缩放）"""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"错误：无法加载图片 {image_path}")
            return False

        # 获取图片和窗口的尺寸
        image_width = pixmap.width()
        image_height = pixmap.height()
        window_width = self.width()
        window_height = self.height()

        # 计算居中位置
        x = (window_width - image_width) // 2
        y = (window_height - image_height) // 2

        # 设置标签位置和大小（使用图片原始尺寸）
        self.label.setPixmap(pixmap)
        self.label.setGeometry(x, y, image_width, image_height)

        print(f"图片已更新: {image_path}")
        print(f"图片尺寸: {image_width}x{image_height}")
        print(f"窗口尺寸: {window_width}x{window_height}")
        print(f"居中位置: ({x}, {y})")
        return True

    def update_image(self, image_path):
        """更新当前窗口显示的图片"""
        self.load_image(image_path)

    def keyPressEvent(self, event):
        """ESC键退出程序"""
        if event.key() == Qt.Key_Escape:
            QApplication.quit()

def cleanup_process():
    """清理当前打开的进程"""
    global current_process
    if current_process:
        try:
            current_process.terminate()
            current_process.wait(timeout=5)
        except:
            try:
                current_process.kill()
            except:
                pass
        current_process = None

def signal_handler(signum, frame):
    """信号处理器，确保程序退出时关闭窗口"""
    print("\n接收到退出信号，正在清理...")
    cleanup_process()
    sys.exit(0)

# 注册信号处理器和退出清理函数
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
atexit.register(cleanup_process)

def calculate_md5(file_path: str) -> str:
    """计算文件的MD5值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def read_index_file(index_path: str) -> List[Tuple[str, str]]:
    """读取index.txt文件，返回文件编号和MD5值的列表"""
    files = []
    with open(index_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(',')
                if len(parts) == 2:
                    file_number, md5_value = parts
                    files.append((file_number, md5_value))
    return files

def open_image_with_window(image_path: str, viewer, updater) -> bool:
    """在现有窗口中更新图片"""
    try:
        # 通过信号安全更新图片（跨线程）
        updater.update_signal.emit(image_path)
        return True
    except Exception as e:
        print(f"Error updating image {image_path}: {e}")
        return False

def check_bmp_file_exists(transfer_path: str, file_number: str) -> bool:
    """检查对应的bmp文件是否存在且可访问（带稳定性检查）"""
    tar_file_path = os.path.join(transfer_path, f"example.{file_number}.bmp")
    
    # 文件不存在直接返回False
    if not os.path.exists(tar_file_path):
        return False
    
    try:
        # 尝试打开文件确认文件状态稳定
        with open(tar_file_path, 'rb') as test_file:
            # 尝试读取1字节确认文件可访问
            if test_file.read(1):
                # 文件有内容且可读
                print(f"验证成功: example.{file_number}.bmp 稳定存在")
                return True
            else:
                # 文件存在但为空（可能正在传输中）
                print(f"文件为空，可能正在传输: example.{file_number}.bmp")
                return False
    except (IOError, PermissionError) as e:
        # 文件访问错误
        print(f"文件访问错误，可能正在生成: {e}")
        return False
    except Exception as e:
        # 其他异常情况
        print(f"检查文件时发生意外错误: {e}")
        return False

def run_playback_logic(args, viewer, updater):
    """执行播放逻辑的工作线程函数"""
    try:
        curt = time.time()
        # 步骤4: 读取文件列表并依次播放（支持断点续传）
        received_index_path = os.path.join("output", "index.txt")
        files_to_play = read_index_file(received_index_path)
        total_files = len(files_to_play)
        print(f"需要播放 {total_files} 个文件")
            
        for i, (file_number, md5_value) in enumerate(files_to_play, 1):            
            # 构建图片文件路径
            image_filename = f"output.{file_number}.bmp"
            image_path = os.path.join(args.output_folder, image_filename)

            if not os.path.exists(image_path):
                print(f"\n错误: 找不到图片文件: {image_path}")
                continue

            # 更新图片
            print(f"\n更新图片: {image_filename} ({i}/{total_files})")
            if not open_image_with_window(image_path, viewer, updater):
                print(f"错误: 无法更新图片: {image_filename}")
                continue

            # 等待截图
            print(f"等待bmp文件生成: example.tar.{file_number}")
            while not check_bmp_file_exists(args.transfer_path, file_number):
                # time.sleep(args.check_interval)
                time.sleep(0.1)

            print(f"检测到bmp文件，准备下一张图片...")

        # 进度条完成后换行
        print("\n\n=== 所有文件播放完成 ===")
        print("总耗时：", time.time()-curt)

    except KeyboardInterrupt:
        print("\n\n用户中断程序，进度已保留")
    except Exception as e:
        print(f"\n\n程序发生错误: {e}")
    finally:
        # 确保清理所有资源
        cleanup_process()
        # 退出应用
        QApplication.quit()


def main():
    parser = argparse.ArgumentParser(description='VM Image Player')
    parser.add_argument('--progress-file', default='progress.txt', help='Progress tracking file')
    parser.add_argument('--output-folder', default='output', help='Output folder path')
    parser.add_argument('--transfer-path', default='Z:\\Users\\37085\\Desktop\\snapshot\\example', help='Transfer path for communication')
    parser.add_argument('--index-file', default='index.txt', help='Index file name')
    parser.add_argument('--index-bmp', default='index.bmp', help='Index BMP file name')
    parser.add_argument('--check-interval', type=int, default=1, help='Check interval in seconds')
    parser.add_argument('--max-retries', type=int, default=999, help='Maximum retry attempts for MD5 verification')
    parser.add_argument('--wait-timeout', type=int, default=120, help='Timeout for waiting index.txt file')

    args = parser.parse_args()
        
    # 创建Qt应用
    app = QApplication(sys.argv)

    # 创建图像更新器
    updater = ImageUpdater()

    # 创建全屏查看器
    index_bmp_path = os.path.join(args.output_folder, args.index_bmp)
    viewer = FullScreenBMPViewer(1, index_bmp_path)
    viewer.showFullScreen()

    # 连接更新信号
    updater.update_signal.connect(viewer.update_image)

    # 创建并启动工作线程
    worker_thread = threading.Thread(target=run_playback_logic, args=(args, viewer, updater))
    worker_thread.daemon = True
    worker_thread.start()

    # 启动Qt主循环
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
