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

def compare_bmp_files(file1, file2):
    # 打开两个图像文件
    img1 = Image.open(file1)
    img2 = Image.open(file2)

    # 确保两个图像的大小相同
    if img1.size != img2.size:
        print("Error: The two images are not the same size.")
        return
    # 逐像素对比
    for y in range(img1.height):
        if y % 50 == 0:
            print(y)
        for x in range(img1.width):
            #  获取两个图像的像素值
            pixel1 = img1.getpixel((x, y))
            pixel2 = img2.getpixel((x, y))

            # 忽略黑色像素
            # if pixel != (0, 0, 0):
            quaternary_str1 = pixel_to_quaternary(pixel1)
            quaternary_str2 = pixel_to_quaternary(pixel2)

            #  对比像素值是否相同
            if quaternary_str1 != quaternary_str2:
                print(f"Pixel at ({x}, {y}) is different.{pixel1}{pixel2}")


#  使用示例
compare_bmp_files("example-origin.bmp", "example1.bmp")
