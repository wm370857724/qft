#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将BMP图片转换回文本文件
"""

from PIL import Image
import numpy as np
import argparse

# 预定义颜色映射
COLOR_MAP = {
    (255, 0, 0): '0', 
    (0, 255, 0): '1', 
    (0, 0, 255): '2', 
    (255, 255, 255): '3'
}

def pixels_to_quaternary(image_array: np.ndarray) -> str:
    """将像素数组转换为四进制字符串"""
    pixels_flat = image_array.reshape(-1, 3)
    
    # 向量化处理所有像素
    white_mask = np.all(pixels_flat > 180, axis=1)
    black_mask = np.all(pixels_flat < 100, axis=1)
    
    # 初始化结果数组
    result = np.full(len(pixels_flat), '4', dtype='U1')
    
    # 应用规则
    result[white_mask] = '3'
    result[black_mask] = '4'
    
    # 对于不符合规则的像素，使用向量化颜色匹配
    other_mask = ~(white_mask | black_mask)
    if np.any(other_mask):
        other_pixels = pixels_flat[other_mask]
        
        # 计算与所有颜色的距离
        color_arrays = np.array(list(COLOR_MAP.keys()))
        distances = np.sum((color_arrays[:, np.newaxis, :] - other_pixels[np.newaxis, :, :]) ** 2, axis=2)
        min_indices = np.argmin(distances, axis=0)
        
        # 映射到对应的四进制数字
        color_values = list(COLOR_MAP.values())
        result[other_mask] = [color_values[i] for i in min_indices]
    
    # 找到第一个'4'的位置
    try:
        end_idx = np.where(result == '4')[0][0]
        quaternary_str = ''.join(result[:end_idx])
    except IndexError:
        quaternary_str = ''.join(result)
    
    return quaternary_str

def quaternary_to_text(quaternary_str: str) -> str:
    """将四进制字符串转换为文本"""
    # 确保字符串长度是4的倍数
    padding = (4 - len(quaternary_str) % 4) % 4
    quaternary_str += '0' * padding
    
    # 转换为二进制字符串
    binary_str = ''
    for i in range(0, len(quaternary_str), 4):
        # 每4个四进制数字转换为8个二进制位
        quat_group = quaternary_str[i:i+4]
        binary_group = ''
        for digit in quat_group:
            binary_group += format(int(digit), '02b')
        binary_str += binary_group
    
    # 转换为字节
    bytes_data = bytearray()
    for i in range(0, len(binary_str), 8):
        if i + 8 <= len(binary_str):
            byte_val = int(binary_str[i:i+8], 2)
            bytes_data.append(byte_val)
    
    # 转换为文本
    try:
        text = bytes_data.decode('utf-8')
        return text
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，尝试其他编码
        return bytes_data.decode('utf-8', errors='ignore')

def bmp_to_txt(bmp_path: str, txt_path: str) -> None:
    """将BMP图片转换为文本文件"""
    # 打开并裁剪图像（与bmp_to_tar.py保持一致）
    original_image = Image.open(bmp_path)
    left, top, width, height = 10, 65, 1900, 950
    # left, top, width, height = 0, 0, 1920, 1080
    cropped_image = original_image.crop((left, top, left + width, top + height))
    
    # 转换为numpy数组
    image_array = np.array(cropped_image)
    
    # 转换为四进制字符串
    quaternary_str = pixels_to_quaternary(image_array)
    
    # 转换为文本
    text_content = quaternary_to_text(quaternary_str)
    
    # 写入文件
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text_content)
    
    print(f"Converted {bmp_path} to {txt_path}")
    print(f"Quaternary length: {len(quaternary_str)} digits")
    print(f"Text length: {len(text_content)} characters")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert BMP image to text file')
    parser.add_argument('--input', '-i', required=True, help='Input BMP file path')
    parser.add_argument('--output', '-o', required=True, help='Output text file path')
    
    args = parser.parse_args()
    
    bmp_to_txt(args.input, args.output) 