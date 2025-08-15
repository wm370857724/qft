#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3 优化版本 - TAR到BMP转换脚本
包含更多高级优化技术
"""

from PIL import Image
import numpy as np
import os
import re
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
from typing import Tuple, List, Optional
import array
from functools import lru_cache

# 预定义颜色映射，避免重复创建
COLOR_MAP = {'0': (255, 0, 0), '1': (0, 255, 0), '2': (0, 0, 255), '3': (255, 255, 255)}
COLOR_ARRAYS = np.array(list(COLOR_MAP.values()), dtype=np.uint8)

# 缓存颜色映射索引，避免重复计算
@lru_cache(maxsize=1024)
def get_color_index(color_tuple):
    """获取颜色在预定义数组中的索引"""
    return list(COLOR_MAP.values()).index(color_tuple)

def binary_to_quaternary_optimized(binary_data: bytes) -> str:
    """优化的二进制到四进制转换，使用numpy向量化操作"""
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
    
    # 使用更高效的字符串转换
    return ''.join(map(str, quaternary_digits))

def quaternary_to_pixels_optimized(quaternary_str: str, width: int, height: int) -> np.ndarray:
    """优化的四进制到像素转换，使用numpy向量化操作"""
    # 将四进制字符串转换为数字数组
    quaternary_array = np.array([int(digit) for digit in quaternary_str], dtype=np.uint8)
    
    # 使用索引直接获取颜色
    pixels = COLOR_ARRAYS[quaternary_array]
    
    # 如果像素数量不足，用黑色填充
    if len(pixels) < width * height:
        padding = np.zeros((width * height - len(pixels), 3), dtype=np.uint8)
        pixels = np.vstack([pixels, padding])
    
    # 重塑为图像尺寸
    return pixels.reshape(height, width, 3)

def tar_to_bmp_optimized(tar_path: str, bmp_path: str, width: int = 2540, height: int = 1470) -> None:
    """优化的TAR到BMP转换函数"""
    # 读取二进制数据
    with open(tar_path, 'rb') as tar_file:
        binary_data = tar_file.read()
    
    # 转换为四进制
    quaternary_str = binary_to_quaternary_optimized(binary_data)
    
    # 转换为像素数组
    pixels = quaternary_to_pixels_optimized(quaternary_str, width, height)
    
    # 创建图像并保存，使用优化的保存参数
    img = Image.fromarray(pixels, 'RGB')
    img.save(bmp_path, optimize=True, quality=95)

def process_single_file(args: Tuple[str, str, int, int]) -> str:
    """单个文件处理函数，用于多进程"""
    tar_file_path, bmp_file_path, width, height = args
    try:
        start_time = time.time()
        tar_to_bmp_optimized(tar_file_path, bmp_file_path, width, height)
        end_time = time.time()
        return f"Converted {tar_file_path} to {bmp_file_path} in {end_time - start_time:.2f}s"
    except Exception as e:
        return f"Error converting {tar_file_path}: {str(e)}"

def convert_folder_optimized(folder_path: str, width: int = 2540, height: int = 1470, 
                           use_multiprocessing: bool = True, max_workers: Optional[int] = None) -> None:
    """优化的文件夹转换函数，支持多进程和进度显示"""
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
    
    print(f"Found {len(files_to_process)} files to process...")
    
    if use_multiprocessing and len(files_to_process) > 1:
        # 使用ProcessPoolExecutor进行多进程处理
        if max_workers is None:
            max_workers = min(cpu_count(), len(files_to_process))
        
        print(f"Using {max_workers} processes to convert {len(files_to_process)} files...")
        start_time = time.time()
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_file = {executor.submit(process_single_file, args): args for args in files_to_process}
            
            # 处理完成的任务
            completed = 0
            for future in as_completed(future_to_file):
                result = future.result()
                print(result)
                completed += 1
                print(f"Progress: {completed}/{len(files_to_process)} ({completed/len(files_to_process)*100:.1f}%)")
        
        end_time = time.time()
        print(f"Total processing time: {end_time - start_time:.2f}s")
        print(f"Average time per file: {(end_time - start_time)/len(files_to_process):.2f}s")
        
    else:
        # 单进程处理
        print("Using single process mode...")
        start_time = time.time()
        
        for i, args in enumerate(files_to_process, 1):
            result = process_single_file(args)
            print(result)
            print(f"Progress: {i}/{len(files_to_process)} ({i/len(files_to_process)*100:.1f}%)")
        
        end_time = time.time()
        print(f"Total processing time: {end_time - start_time:.2f}s")
        print(f"Average time per file: {(end_time - start_time)/len(files_to_process):.2f}s")

def convert_folder_legacy(folder_path: str, width: int = 2540, height: int = 1470) -> None:
    """兼容原始版本的转换函数"""
    pattern = re.compile(r'^example\.tar\.(\d{3})$')
    
    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            tar_file_path = os.path.join(folder_path, filename)
            bmp_filename = f"output.{match.group(1)}.bmp"
            bmp_file_path = os.path.join("output", bmp_filename)
            tar_to_bmp_optimized(tar_file_path, bmp_file_path, width, height)
            print(f"Converted {tar_file_path} to {bmp_file_path}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Optimized TAR to BMP converter')
    parser.add_argument('--folder', default='temp', help='Input folder path')
    parser.add_argument('--input', '-i', help='Input single TAR file path')
    parser.add_argument('--output', '-o', help='Output BMP file path')
    parser.add_argument('--width', type=int, default=2540, help='Output image width')
    parser.add_argument('--height', type=int, default=1470, help='Output image height')
    parser.add_argument('--single', action='store_true', help='Use single process mode')
    parser.add_argument('--workers', type=int, help='Number of worker processes')
    parser.add_argument('--legacy', action='store_true', help='Use legacy mode (compatible with original)')
    
    args = parser.parse_args()
    
    # 如果指定了单个文件，直接处理单个文件
    if args.input and args.output:
        print(f"Processing single file: {args.input} -> {args.output}")
        tar_to_bmp_optimized(args.input, args.output, args.width, args.height)
    elif args.legacy:
        convert_folder_legacy(args.folder, args.width, args.height)
    else:
        convert_folder_optimized(
            args.folder, 
            args.width, 
            args.height, 
            use_multiprocessing=not args.single,
            max_workers=args.workers
        ) 