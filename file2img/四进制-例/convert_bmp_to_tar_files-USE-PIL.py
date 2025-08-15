import os
from multiprocessing import Pool
from PIL import Image
import numpy as np

def pixel_to_quaternary(pixel):
    """将像素颜色转换为四进制数字。"""
    # 定义颜色与四进制的映射
    color_map = {(255, 0, 0): '0', (0, 255, 0): '1', (0, 0, 255): '2', (255, 255, 255): '3', (0, 0, 0): '4'}
    # 计算与四种颜色的距离
    distances = {color: np.linalg.norm(np.array(pixel) - np.array(color)) for color in color_map.keys()}
    # 选择最近的颜色
    closest_color = min(distances, key=distances.get)
    return color_map[closest_color]

def quaternary_to_binary(quaternary_str):
    """将四进制字符串转换为二进制数据。"""
    binary_data = bytearray()
    for i in range(0, len(quaternary_str), 4):
        # 每四个四进制数字转换为一个字节
        byte_str = ''.join(format(int(digit), '02b') for digit in quaternary_str[i:i+4])
        binary_data.append(int(byte_str, 2))
    return binary_data

def bmp_to_tar(bmp_path, tar_path):
    """将BMP图像转换回tar文件。"""
    original_image = Image.open(bmp_path)
    left = 10
    top = 62
    width = 1900
    height = 950
    cropped_image = original_image.crop((left,top,left+width,top+height))
    pixels = list(cropped_image.getdata())

    quaternary_str = ''
    for pixel in pixels:
        if pixel_to_quaternary(pixel) != '4':
            quaternary_str = quaternary_str+pixel_to_quaternary(pixel)
        else:
            break

    binary_data = quaternary_to_binary(quaternary_str)
    
    with open(tar_path, 'wb') as tar_file:
        tar_file.write(binary_data)

  
def convert_file(file_info):
    bmp_file, tar_file = file_info
    bmp_to_tar(bmp_file, tar_file)
    print(f"Converted {bmp_file} to {tar_file}")

def convert_files_in_folder(folder_path):
    # 获取所有符合条件的文件
    bmp_files = [f for f in os.listdir(folder_path) if f.startswith('example.') and f.endswith('.bmp')]
    # 构建输入参数列表
    tasks = []
    for bmp_file in bmp_files:
        # 提取编号
        number = bmp_file.split('.')[1]
        tar_file = f"example.tar.{number}"
        tasks.append((os.path.join(folder_path, bmp_file), os.path.join(folder_path, tar_file)))
    
    # 使用多进程并行处理文件转换
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(convert_file, tasks)

if __name__ == '__main__':
    folder_path = 'example'  # 替换为你的example文件夹路径
    convert_files_in_folder(folder_path)