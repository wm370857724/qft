#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将index.txt文件转换为BMP图片
"""

from PIL import Image
import numpy as np
import argparse

# 预定义颜色映射
COLOR_MAP = {'0': (255, 0, 0), '1': (0, 255, 0), '2': (0, 0, 255), '3': (255, 255, 255)}

def text_to_quaternary(text: str) -> str:
    """将文本转换为四进制字符串"""
    # 将文本转换为字节
    text_bytes = text.encode('utf-8')
    
    # 转换为二进制字符串
    binary_str = ''.join(format(byte, '08b') for byte in text_bytes)
    
    # 转换为四进制
    quaternary_str = ''
    for i in range(0, len(binary_str), 2):
        if i + 1 < len(binary_str):
            quaternary_str += str(int(binary_str[i:i+2], 2))
        else:
            quaternary_str += str(int(binary_str[i] + '0', 2))
    
    return quaternary_str

def quaternary_to_pixels(quaternary_str: str, width: int, height: int) -> np.ndarray:
    """将四进制字符串转换为像素数组"""
    # 将四进制字符串转换为数字数组
    quaternary_array = np.array([int(digit) for digit in quaternary_str], dtype=np.uint8)
    
    # 使用预定义颜色映射
    color_arrays = np.array(list(COLOR_MAP.values()), dtype=np.uint8)
    pixels = color_arrays[quaternary_array]
    
    # 如果像素数量不足，用黑色填充
    if len(pixels) < width * height:
        padding = np.zeros((width * height - len(pixels), 3), dtype=np.uint8)
        pixels = np.vstack([pixels, padding])
    
    # 重塑为图像尺寸
    return pixels.reshape(height, width, 3)

def txt_to_bmp(txt_path: str, bmp_path: str, width: int = 2540, height: int = 1470) -> None:
    """将txt文件转换为BMP图片"""
    # 读取文本内容
    with open(txt_path, 'r', encoding='utf-8') as f:
        text_content = f.read()
    
    # 转换为四进制
    quaternary_str = text_to_quaternary(text_content)
    
    # 转换为像素数组
    pixels = quaternary_to_pixels(quaternary_str, width, height)
    
    # 创建图像并保存
    img = Image.fromarray(pixels, 'RGB')
    img.save(bmp_path, optimize=True, quality=95)
    
    print(f"Converted {txt_path} to {bmp_path}")
    print(f"Text length: {len(text_content)} characters")
    print(f"Quaternary length: {len(quaternary_str)} digits")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert text file to BMP image')
    parser.add_argument('--input', '-i', required=True, help='Input text file path')
    parser.add_argument('--output', '-o', required=True, help='Output BMP file path')
    parser.add_argument('--width', type=int, default=2540, help='Output image width')
    parser.add_argument('--height', type=int, default=1470, help='Output image height')
    
    args = parser.parse_args()
    
    txt_to_bmp(args.input, args.output, args.width, args.height) 