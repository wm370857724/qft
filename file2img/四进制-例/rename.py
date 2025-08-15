import os
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

# 使用示例
if __name__ == '__main__':
    folder_path = 'example'  # 替换为你的文件夹路径
    rename_files(folder_path)