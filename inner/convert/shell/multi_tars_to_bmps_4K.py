from PIL import Image
import os
import re

def binary_to_quaternary(binary_data):
    quaternary_str = ''
    for byte in binary_data:
        quaternary_str += format(byte, '08b') 
    quaternary_str = ''.join(str(int(quaternary_str[i:i+2], 2)) for i in range(0, len(quaternary_str), 2))
    return quaternary_str

def quaternary_to_pixels(quaternary_str, width, height):
    color_map = {'0': (255, 0, 0), '1': (0, 255, 0), '2': (0, 0, 255), '3': (255, 255, 255)}
    pixels = [color_map[digit] for digit in quaternary_str]
    pixels += [(0, 0, 0)] * (width * height - len(pixels))
    return pixels

def tar_to_bmp(tar_path, bmp_path, width=2540, height=1470):
    with open(tar_path, 'rb') as tar_file:
        binary_data = tar_file.read()
    
    quaternary_str = binary_to_quaternary(binary_data)
    pixels = quaternary_to_pixels(quaternary_str, width, height)
    
    img = Image.new('RGB', (width, height))
    img.putdata(pixels)
    img.save(bmp_path)

def convert_folder(folder_path):
    pattern = re.compile(r'^example\.tar\.(\d{3})$')

    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            tar_file_path = os.path.join(folder_path, filename)
            bmp_filename = f"output.{match.group(1)}.bmp"
            bmp_file_path = os.path.join("output", bmp_filename)
            tar_to_bmp(tar_file_path, bmp_file_path)
            print(f"Converted {tar_file_path} to {bmp_file_path}")

if __name__ == '__main__':
    folder_path = 'temp' 
    convert_folder(folder_path)