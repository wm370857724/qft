from PIL import Image
import os
import re

def binary_to_quaternary(binary_data):
    """将二进制数据转换为四进制字符串。"""
    quaternary_str = ''
    for byte in binary_data:
        quaternary_str += format(byte, '08b')  # 转换为8位二进制
    # 将二进制转换为四进制
    quaternary_str = ''.join(str(int(quaternary_str[i:i+2], 2)) for i in range(0, len(quaternary_str), 2))
    return quaternary_str

def quaternary_to_pixels(quaternary_str, width, height):
    """将四进制字符串转换为像素数据。"""
    # 定义颜色映射
    color_map = {'0': (255, 0, 0), '1': (0, 255, 0), '2': (0, 0, 255), '3': (255, 255, 255)}
    pixels = [color_map[digit] for digit in quaternary_str]
    # 补全黑色像素
    pixels += [(0, 0, 0)] * (width * height - len(pixels))
    return pixels

def tar_to_bmp(tar_path, bmp_path, width=1900, height=950):
    """将tar文件转换为BMP图像。"""
    with open(tar_path, 'rb') as tar_file:
        binary_data = tar_file.read()
    
    quaternary_str = binary_to_quaternary(binary_data)
    pixels = quaternary_to_pixels(quaternary_str, width, height)
    
    img = Image.new('RGB', (width, height))
    img.putdata(pixels)
    img.save(bmp_path)

def convert_folder(folder_path):
    # 正则表达式匹配 example.tar.001 到 example.tar.nnn 的文件名
    pattern = re.compile(r'^example\.tar\.(\d{3})$')

    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            # 构建原始tar文件的完整路径
            tar_file_path = os.path.join(folder_path, filename)
            # 构建目标bmp文件的文件名和完整路径
            bmp_filename = f"example.{match.group(1)}.bmp"
            bmp_file_path = os.path.join(folder_path, bmp_filename)
            # 调用tar_to_bmp函数进行转换
            tar_to_bmp(tar_file_path, bmp_file_path)
            print(f"Converted {tar_file_path} to {bmp_file_path}")


# 使用示例
if __name__ == '__main__':
    folder_path = 'tar'  # 替换为你的文件夹路径
    convert_folder(folder_path)