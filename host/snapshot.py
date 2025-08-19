import cv2
import numpy as np
import mss
import time
import os
from PIL import Image
import hashlib


def calculate_md5(file_path: str) -> str:
    """计算文件的MD5值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

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

def monitor_screen2(region, callback, interval=0.1, threshold=10):
    """
    监听屏幕2的指定区域，用红框标记并检测变化
    :param region: 监控区域 (x, y, width, height)，基于屏幕2的坐标系
    :param callback: 变化时触发的回调函数
    :param interval: 检测间隔（秒）
    :param threshold: 像素变化阈值
    """
    with mss.mss() as sct:
        # 获取所有屏幕信息
        monitors = sct.monitors
        if len(monitors) < 3:  # 索引0是虚拟屏，物理屏从1开始
            raise ValueError("屏幕2不存在！当前检测到{}块屏幕".format(len(monitors)-1))
        
        # 定位屏幕2的物理坐标
        screen2 = monitors[2]  # 索引1=主屏，索引2=第二屏幕
        print(f"屏幕2坐标范围: top={screen2['top']}, left={screen2['left']}, width={screen2['width']}, height={screen2['height']}")

        # 调整区域到屏幕2的绝对坐标
        abs_region = {
            "top": screen2["top"] + region[1],
            "left": screen2["left"] + region[0],
            "width": region[2],
            "height": region[3]
        }

        prev_frame = None
        while True:
            # 截取屏幕2的指定区域
            sct_img = sct.grab(abs_region)
            current_frame = np.array(sct_img)[:, :, :3]  # 移除Alpha通道

            # 用红框标记监控区域（在原图上绘制）
            marked_frame = current_frame.copy()
            cv2.rectangle(marked_frame, (0, 0), (region[2]-1, region[3]-1), (0, 0, 255), 2)
            
            # 显示带红框的监控画面
            # cv2.imshow("Screen2 Monitoring", marked_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q退出
                break

            # 检测变化
            if prev_frame is not None:
                gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                gray_curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
                diff = cv2.absdiff(gray_prev, gray_curr)
                _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
                non_zero = cv2.countNonZero(thresh)
                
                if non_zero > threshold:
                    callback(non_zero, marked_frame)

            prev_frame = current_frame
            time.sleep(interval)

        cv2.destroyAllWindows()

# 示例回调函数
fileNumb=1
def on_change(diff_pixels, frame):
    print("检测到变化后让图片加载一会儿再截图")
    time.sleep(0.2)

    # print(f"检测到变化！差异像素数: {diff_pixels}")
    # 可保存变化瞬间的图像
    # cv2.imwrite(f"img\\hange_{time.time()}.png", frame)
    global fileNumb
    cur1 = time.time()
    screenshot_path = os.path.join("example", f"example.{fileNumb:03}.bmp")
    print(f"截取图片: {screenshot_path}")
    capture_screen(2, screenshot_path)
    fileNumb+=1
    

    # cur2 = time.time()
    # original_md5 = calculate_md5(screenshot_path)
    # print(original_md5)
    # print("计算图片MD5耗时",time.time() - cur2)
    # print("截图保存并计算图片MD5耗时",time.time() - cur1)

 # 等待5秒后开始执行
print("等待打开云桌面并打开图片播放窗口后，大概2秒钟再开始执行...")
time.sleep(2)

# 启动监听（区域基于屏幕2的局部坐标系）
monitor_screen2(
    region=(100, 100, 10, 10),  # 在屏幕2的(100,100)处监听10x10区域
    callback=on_change,
    threshold=5  # 低阈值适应小区域
)
