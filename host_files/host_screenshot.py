"""
宿主机端自动截图脚本（带重试机制）
"""

import mss
import time
import os
import hashlib
import subprocess
import sys
import signal
import atexit
import re
from PIL import Image
import argparse
from typing import List, Tuple

def capture_screen(monitor_id=2, output_path="screenshot.bmp"):
    """截取指定屏幕的截图"""
    with mss.mss() as sct:
        # 获取所有显示器信息
        monitors = sct.monitors
        
        # 检查输入的显示器编号是否有效（编号从1开始）
        if monitor_id < 1 or monitor_id >= len(monitors):
            raise ValueError(f"无效的屏幕编号。可用屏幕范围: 1 ~ {len(monitors)-1}")
        
        # 选择指定编号的显示器（monitors[0]是合并所有屏幕的区域）
        target_monitor = monitors[monitor_id]
      
        # 截取屏幕
        screenshot = sct.grab(target_monitor)
        
        # 转换为PIL图像并保存为BMP
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img.save(output_path, "BMP")
        print(f"截图已保存至: {output_path}")

def calculate_md5(file_path: str) -> str:
    """计算文件的MD5值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def read_index_file(index_path: str) -> List[Tuple[str, str]]:
    """读取index.txt文件，返回文件编号和MD5值的列表（宽松模式）"""
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

def read_index_file_strict(index_path: str) -> List[Tuple[str, str]]:
    """严格读取并校验index.txt，全部行需满足: 三位编号,32位MD5。返回有效列表，若任何行不合法或为空则返回空列表。"""
    if not os.path.exists(index_path):
        return []
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    except Exception:
        return []
    if not lines:
        return []
    pattern = re.compile(r'^(\d{3}),([a-fA-F0-9]{32})$')
    results: List[Tuple[str, str]] = []
    for ln in lines:
        m = pattern.match(ln)
        if not m:
            # 任意一行不合法，视为无效
            return []
        results.append((m.group(1), m.group(2).lower()))
    # 合法且至少一条
    return results

def convert_bmp_to_tar(bmp_path: str, tar_path: str) -> bool:
    """将BMP图片转换为TAR文件"""
    try:
        subprocess.run([
            sys.executable, 'bmp_to_tar.py',
            '--input', bmp_path,
            '--output', tar_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e}")
        return False

def convert_bmp_to_txt(bmp_path: str, txt_path: str) -> bool:
    """将BMP图片转换为TXT文件"""
    try:
        subprocess.run([
            sys.executable, 'bmp_to_txt.py',
            '--input', bmp_path,
            '--output', txt_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e}")
        return False

def verify_and_save_tar_file(temp_tar_path: str, final_tar_path: str, expected_md5: str) -> bool:
    """
    验证TAR文件MD5值并保存（单次校验）
    返回: True-验证成功, False-验证失败
    """
    if not os.path.exists(temp_tar_path):
        print(f"错误: 临时TAR文件不存在: {temp_tar_path}")
        return False
    
    # 验证MD5值
    actual_md5 = calculate_md5(temp_tar_path)
    print(f"期望MD5: {expected_md5}")
    print(f"实际MD5: {actual_md5}")
    
    if actual_md5 == expected_md5:
        # MD5匹配，移动到传输路径并重命名
        try:
            os.rename(temp_tar_path, final_tar_path)
            print(f"文件验证成功，已保存到: {final_tar_path}")
            return True
        except Exception as e:
            print(f"移动文件失败: {e}")
            return False
    else:
        print("MD5值不匹配")
        # 删除临时文件
        try:
            os.remove(temp_tar_path)
            print(f"已删除临时文件: {temp_tar_path}")
        except Exception as e:
            print(f"删除临时文件失败: {e}")
        return False

def signal_handler(signum, frame):
    """信号处理器，确保程序退出时清理资源"""
    print("\n接收到退出信号，正在清理...")
    sys.exit(0)

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    parser = argparse.ArgumentParser(description='Host Screenshot and Convert Script')
    parser.add_argument('--transfer-path', default='D:\\auto_transfer\\host_files\\transferPath', help='Transfer path for communication')
    parser.add_argument('--output-folder', default='D:\\auto_transfer\\host_files\\transferPath', help='Output folder for screenshots')
    parser.add_argument('--monitor-id', type=int, default=2, help='Monitor ID to capture')
    parser.add_argument('--screenshot-interval', type=int, default=5, help='Screenshot interval in seconds')
    parser.add_argument('--index-file', default='index.txt', help='Index file name')
    parser.add_argument('--index-bmp', default='index.bmp', help='Index BMP file name')
    parser.add_argument('--max-retries', type=int, default=3, help='(unused)Maximum retry attempts for MD5 verification')
    
    args = parser.parse_args()
    
    try:
        # 确保输出文件夹存在
        os.makedirs(args.output_folder, exist_ok=True)
        os.makedirs(args.transfer_path, exist_ok=True)
        
        print("=== 宿主机端自动截图脚本 ===")
        print(f"传输路径: {args.transfer_path}")
        print(f"输出文件夹: {args.output_folder}")
        print(f"显示器ID: {args.monitor_id}")
        print(f"截图间隔: {args.screenshot_interval}秒")
        print(f"最大重试次数(未使用): {args.max_retries}")
        print()
        
        # 等待5秒后开始执行
        print("等待5秒后开始执行...")
        time.sleep(5)
        
        # 步骤1: 循环截图index.bmp并转换为index.txt，直到得到有效列表
        index_bmp_screenshot = os.path.join(args.output_folder, args.index_bmp)
        index_txt_output = os.path.join(args.transfer_path, args.index_file)
        files_to_process: List[Tuple[str, str]] = []
        attempt = 0
        while True:
            attempt += 1
            print(f"\n[索引捕获] 第 {attempt} 次尝试：截图 index.bmp 并转换为 index.txt")
            capture_screen(args.monitor_id, index_bmp_screenshot)
            if not convert_bmp_to_txt(index_bmp_screenshot, index_txt_output):
                print("转换index.txt失败，准备重试...")
                time.sleep(max(1, args.screenshot_interval))
                continue
            # 严格校验读取
            files_to_process = read_index_file_strict(index_txt_output)
            if len(files_to_process) == 0:
                print("index.txt 无效（为空/零条/格式错误），继续重试截图...")
                time.sleep(max(1, args.screenshot_interval))
                continue
            else:
                print(f"index.txt 有效，包含 {len(files_to_process)} 条记录")
                break
        
        # 步骤2: 循环截图并转换文件 - 修改为持续重试直到成功
        print("\n步骤2: 开始循环截图并转换文件（失败将持续重试）...")
        
        for i, (file_number, expected_md5) in enumerate(files_to_process, 1):
            success = False
            attempt = 0
            
            while not success:
                attempt += 1
                print(f"\n处理文件 {i}/{len(files_to_process)}: {file_number} (尝试 #{attempt})")
                
                # 等待指定间隔
                print(f"等待 {args.screenshot_interval} 秒...")
                time.sleep(args.screenshot_interval)
                
                try:
                    # 截图
                    screenshot_path = os.path.join(args.output_folder, f"example.{file_number}.bmp")
                    print(f"截取图片: {screenshot_path}")
                    capture_screen(args.monitor_id, screenshot_path)
                    
                    # 转换为tar文件
                    temp_tar_path = os.path.join(args.output_folder, f"temp_example.tar.{file_number}")
                    print(f"转换为tar文件: {temp_tar_path}")
                    
                    if convert_bmp_to_tar(screenshot_path, temp_tar_path):
                        # 验证MD5值并保存文件
                        final_tar_path = os.path.join(args.transfer_path, f"example.tar.{file_number}")
                        if verify_and_save_tar_file(temp_tar_path, final_tar_path, expected_md5):
                            success = True
                            print(f"✓ 文件 {file_number} 处理成功")
                        else:
                            print(f"× 文件 {file_number} 验证失败，准备重试...")
                    else:
                        print(f"× 文件 {file_number} 转换失败，准备重试...")
                except Exception as e:
                    print(f"! 处理过程中发生异常: {e}")
                    traceback.print_exc()
        
        print("\n=== 所有文件处理完成 ===")
        
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"\n程序发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
