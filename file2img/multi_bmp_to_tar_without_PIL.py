import os
from multiprocessing import Pool
from PIL import Image
import re

def rename_files(folder_path):
    # 确保目标文件夹存在
    target_folder = os.path.join(folder_path)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 匹配文件名的正则表达式
    pattern = re.compile(r'^example(?:_(\d+))?\.bmp$')

    # 存储匹配的文件及其编号
    files = []

    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            # 特殊处理原始的example.bmp文件
            if match.group(1) is None:
                index = 0
            else:
                index = int(match.group(1)) + 1  # 由于example_0对应002，所以+1
            files.append((filename, index))

    # 按编号排序文件
    files.sort(key=lambda x: x[1])

    # 重命名文件
    for i, (filename, _) in enumerate(files, start=1):
        new_filename = f"example.{i:03}.bmp"
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(target_folder, new_filename)
        os.rename(old_file_path, new_file_path)
        print(f"Renamed {filename} to {new_filename}")


def find_closest_color(pixel):
    color_map = {
        (255, 0, 0): '0', 
        (0, 255, 0): '1', 
        (0, 0, 255): '2', 
        (255, 255, 255): '3', 
        (0, 0, 0): '4'
    }
    # 初始化最小距离和最接近的颜色
    min_distance = float('inf')
    closest_color = None
    
    for color, value in color_map.items():
        # 计算当前颜色与目标像素之间的距离
        distance = sum((c - p) ** 2 for c, p in zip(color, pixel))
        
        # 更新最小距离和最接近的颜色
        if distance < min_distance:
            min_distance = distance
            closest_color = value
    
    return closest_color

def find_closest_color_by_rule(pixel):
    color_map = {
        (255, 0, 0): '0', 
        (0, 255, 0): '1', 
        (0, 0, 255): '2', 
        (255, 255, 255): '3', 
        (0, 0, 0): '4'
    }
    # 根据规则判断最接近的颜色
    rules = [all(c > 180 for c in pixel), all(c < 100 for c in pixel)]
    if rules[0]:
        closest_color = '3'  # 白色
    elif rules[1]:
        closest_color = '4'  # 黑色
    else:
        # 如果不符合以上两个规则，使用原始方法找到最接近的颜色
        closest_color = find_closest_color(pixel)
    # print(f"The closest color value by rule is: {closest_color}")
    return closest_color
    
def pixel_to_quaternary(pixel):
    """将像素颜色转换为四进制数字。"""
    # 定义颜色与四进制的映射
    # color_map = {(255, 0, 0): '0', (0, 255, 0): '1', (0, 0, 255): '2', (255, 255, 255): '3', (0, 0, 0): '4'}
    # 计算与四种颜色的距离
    # distances = {color: np.linalg.norm(np.array(pixel) - np.array(color)) for color in color_map.keys()}
    # 选择最近的颜色
    # closest_color = min(distances, key=distances.get)
    # return color_map[closest_color]
    return find_closest_color_by_rule(pixel)

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
    rename_files(folder_path)
    convert_files_in_folder(folder_path)