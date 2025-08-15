# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import os
import re
from multiprocessing import Pool, cpu_count
from typing import Tuple, List
import array

# 预定义颜色映射，避免重复创建
COLOR_MAP = {'0': (255, 0, 0), '1': (0, 255, 0), '2': (0, 0, 255), '3': (255, 255, 255)}
COLOR_ARRAYS = np.array(list(COLOR_MAP.values()))

def binary_to_quaternary_optimized(binary_data: bytes) -> str:
    """优化的二进制到四进制转换"""
    if not binary_data:
        return ''
    
    # 使用numpy进行批量位操作
    binary_array = np.unpackbits(np.frombuffer(binary_data, dtype=np.uint8))
    
    # 将二进制位两两分组并转换为四进制
    # 确保长度为偶数
    if len(binary_array) % 2 != 0:
        binary_array = np.append(binary_array, 0)
    
    # 重塑为2列，然后计算四进制值
    binary_pairs = binary_array.reshape(-1, 2)
    quaternary_digits = binary_pairs[:, 0] * 2 + binary_pairs[:, 1]
    
    # 转换为字符串
    return ''.join(quaternary_digits.astype(str))

def quaternary_to_pixels_optimized(quaternary_str: str, width: int, height: int) -> np.ndarray:
    """优化的四进制到像素转换，使用numpy向量化操作"""
    # 预定义颜色数组
    color_arrays = np.array(list(COLOR_MAP.values()), dtype=np.uint8)
    
    # 将四进制字符串转换为数字数组
    quaternary_array = np.array([int(digit) for digit in quaternary_str], dtype=np.uint8)
    
    # 使用索引直接获取颜色
    pixels = color_arrays[quaternary_array]
    
    # 如果像素数量不足，用黑色填充
    if len(pixels) < width * height:
        padding = np.zeros((width * height - len(pixels), 3), dtype=np.uint8)
        pixels = np.vstack([pixels, padding])
    
    # 重塑为图像尺寸
    return pixels.reshape(height, width, 3)

def tar_to_bmp_optimized(tar_path: str, bmp_path: str, width: int = 2540, height: int = 1470):
    """优化的TAR到BMP转换函数"""
    # 读取二进制数据
    with open(tar_path, 'rb') as tar_file:
        binary_data = tar_file.read()
    
    # 转换为四进制
    quaternary_str = binary_to_quaternary_optimized(binary_data)
    
    # 转换为像素数组
    pixels = quaternary_to_pixels_optimized(quaternary_str, width, height)
    
    # 创建图像并保存
    img = Image.fromarray(pixels, 'RGB')
    img.save(bmp_path, optimize=True)

def process_single_file(args):
    """单个文件处理函数，用于多进程"""
    tar_file_path, bmp_file_path, width, height = args
    try:
        tar_to_bmp_optimized(tar_file_path, bmp_file_path, width, height)
        return f"Converted {tar_file_path} to {bmp_file_path}"
    except Exception as e:
        return f"Error converting {tar_file_path}: {str(e)}"

def convert_folder_optimized(folder_path: str, width: int = 2540, height: int = 1470, use_multiprocessing: bool = True):
    """优化的文件夹转换函数，支持多进程"""
    pattern = re.compile(r'^example\.tar\.(\d{3})$')
    
    # 收集需要处理的文件
    files_to_process = []
    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            tar_file_path = os.path.join(folder_path, filename)
            bmp_filename = f"output.{match.group(1)}.bmp"
            bmp_file_path = os.path.join("output", bmp_filename)
            files_to_process.append((tar_file_path, bmp_file_path, width, height))
    
    if not files_to_process:
        print("No matching files found.")
        return
    
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    if use_multiprocessing and len(files_to_process) > 1:
        # 使用多进程处理
        num_processes = min(cpu_count(), len(files_to_process))
        print(f"Using {num_processes} processes to convert {len(files_to_process)} files...")
        
        with Pool(processes=num_processes) as pool:
            results = pool.map(process_single_file, files_to_process)
        
        for result in results:
            print(result)
    else:
        # 单进程处理
        for tar_file_path, bmp_file_path, width, height in files_to_process:
            result = process_single_file((tar_file_path, bmp_file_path, width, height))
            print(result)

if __name__ == '__main__':
    folder_path = 'temp'
    # 可以通过参数控制是否使用多进程
    convert_folder_optimized(folder_path, use_multiprocessing=True) 