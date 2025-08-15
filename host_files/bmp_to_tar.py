# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import array
import argparse
import concurrent.futures
import threading

# 预定义颜色映射
COLOR_MAP = {
    (255, 0, 0): '0', 
    (0, 255, 0): '1', 
    (0, 0, 255): '2', 
    (255, 255, 255): '3', 
    (0, 0, 0): '4'
}

# 预定义颜色数组
COLOR_ARRAYS = np.array(list(COLOR_MAP.keys()))

def quaternary_to_binary_optimized(quaternary_str: str) -> bytes:
    """优化的四进制到二进制转换"""
    if not quaternary_str:
        return b''
    
    # 确保字符串长度是4的倍数
    padding = (4 - len(quaternary_str) % 4) % 4
    quaternary_str += '0' * padding
    
    # 使用更高效的转换方法
    binary_data = bytearray()
    for i in range(0, len(quaternary_str), 4):
        # 直接计算字节值，避免字符串操作
        byte_val = 0
        for j in range(4):
            if i + j < len(quaternary_str):
                byte_val |= int(quaternary_str[i + j]) << (6 - j * 2)
        binary_data.append(byte_val)
    
    return bytes(binary_data)

def process_image_chunk(chunk_pixels, lock, results, chunk_id):
    """处理图像分块的核心逻辑"""
    pixels_flat = chunk_pixels.reshape(-1, 3)
    
    # 创建规则掩码
    white_mask = np.all(pixels_flat > 180, axis=1)
    black_mask = np.all(pixels_flat < 100, axis=1)
    
    # 初始化结果数组
    result = np.full(len(pixels_flat), '4', dtype='U1')
    
    # 应用规则
    result[white_mask] = '3'
    result[black_mask] = '4'
    
    # 处理其他像素
    other_mask = ~(white_mask | black_mask)
    if np.any(other_mask):
        other_pixels = pixels_flat[other_mask]
        
        # 计算与所有颜色的距离
        distances = np.sum((COLOR_ARRAYS[:, np.newaxis, :] - other_pixels[np.newaxis, :, :]) ** 2, axis=2)
        min_indices = np.argmin(distances, axis=0)
        
        # 映射到对应的四进制数字
        color_values = list(COLOR_MAP.values())
        result[other_mask] = [color_values[i] for i in min_indices]
    
    # 将结果存储到共享列表
    with lock:
        results[chunk_id] = ''.join(result.tolist())

def bmp_to_tar_vectorized(bmp_path: str, tar_path: str, bmp_width: int, bmp_height: int):
    """多线程版本的图像转换"""
    # 打开并裁剪图像
    original_image = Image.open(bmp_path)
    cropped_image = original_image.crop((5, 5, 5 + bmp_width, 5 + bmp_height))
    
    # 转换为numpy数组
    image_array = np.array(cropped_image)
    height = image_array.shape[0]
    
    # 将图像分成4个水平条带
    chunk_height = height // 4
    chunks = [
        image_array[i*chunk_height: (i+1)*chunk_height] 
        for i in range(4)
    ]
    
    # 处理最后可能不完整的部分
    if height % 4 != 0:
        chunks[-1] = image_array[3*chunk_height:]
    
    # 多线程处理
    lock = threading.Lock()
    results = [None] * 4  # 预分配结果存储
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for i, chunk in enumerate(chunks):
            futures.append(executor.submit(
                process_image_chunk, chunk, lock, results, i
            ))
        
        # 等待所有任务完成
        concurrent.futures.wait(futures)
    
    # 合并结果
    quaternary_str = ''.join(results)
    
    # 找到第一个'4'的位置
    try:
        end_idx = quaternary_str.index('4')
        quaternary_str = quaternary_str[:end_idx]
    except ValueError:
        pass  # 如果没有找到'4'，则使用整个字符串
    
    # 转换为二进制数据
    binary_data = quaternary_to_binary_optimized(quaternary_str)
    
    # 写入文件
    with open(tar_path, 'wb') as tar_file:
        tar_file.write(binary_data)

def main():
    parser = argparse.ArgumentParser(description='Convert BMP image to TAR file')
    parser.add_argument('--input', '-i', required=True, help='Input BMP file path')
    parser.add_argument('--output', '-o', required=True, help='Output TAR file path')
    parser.add_argument('--width', type=int, help='BMP file width')
    parser.add_argument('--height', type=int, help='BMP file height')
    
    args = parser.parse_args()
    
    bmp_to_tar_vectorized(args.input, args.output, args.width, args.height)
    print(f"Converted {args.input} to {args.output}")

if __name__ == '__main__':
    main()
