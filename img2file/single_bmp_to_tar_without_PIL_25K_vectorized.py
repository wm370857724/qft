# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import array

# 预定义颜色映射，避免重复创建
COLOR_MAP = {
    (255, 0, 0): '0', 
    (0, 255, 0): '1', 
    (0, 0, 255): '2', 
    (255, 255, 255): '3', 
    (0, 0, 0): '4'
}

# 预定义颜色数组，用于快速计算
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

def bmp_to_tar_vectorized(bmp_path: str, tar_path: str):
    """完全向量化的版本，最高性能"""
    # 打开并裁剪图像
    original_image = Image.open(bmp_path)
    left, top, width, height = 10, 62, 2540, 1470
    cropped_image = original_image.crop((left, top, left + width, top + height))
    
    # 转换为numpy数组
    image_array = np.array(cropped_image)
    pixels_flat = image_array.reshape(-1, 3)
    
    # 向量化处理所有像素
    # 创建规则掩码
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
        distances = np.sum((COLOR_ARRAYS[:, np.newaxis, :] - other_pixels[np.newaxis, :, :]) ** 2, axis=2)
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
    
    # 转换为二进制数据
    binary_data = quaternary_to_binary_optimized(quaternary_str)
    
    # 写入文件
    with open(tar_path, 'wb') as tar_file:
        tar_file.write(binary_data)

if __name__ == '__main__':
    # 或者使用完全向量化版本（最高性能）
    bmp_to_tar_vectorized('example/example.bmp', 'recovered_example_vectorized.tar') 
