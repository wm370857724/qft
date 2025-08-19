#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成index.txt文件，记录文件名和MD5值
"""

import os
import hashlib
import argparse
import re
from typing import List, Tuple

def calculate_md5(file_path: str) -> str:
    """计算文件的MD5值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def generate_index_from_folder(folder_path: str, output_path: str) -> None:
    """从文件夹中的TAR文件生成index.txt"""
    pattern = re.compile(r'^example\.tar\.(\d{3})$')
    
    # 收集所有TAR文件
    tar_files = []
    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            file_path = os.path.join(folder_path, filename)
            file_number = match.group(1)
            md5_value = calculate_md5(file_path)
            tar_files.append((file_number, file_path, md5_value))
    
    # 按文件编号排序
    tar_files.sort(key=lambda x: x[0])
    
    # 写入index.txt文件
    with open(output_path, 'w', encoding='utf-8') as f:
        for file_number, file_path, md5_value in tar_files:
            f.write(f"{file_number},{md5_value}\n")
    
    print(f"Generated index.txt with {len(tar_files)} files")
    for file_number, _, md5_value in tar_files:
        print(f"  File {file_number}: {md5_value}")

def generate_index_from_single_file(file_path: str, output_path: str) -> None:
    """从单个TAR文件生成index.txt"""
    md5_value = calculate_md5(file_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"001,{md5_value}\n")
    
    print(f"Generated index.txt for single file")
    print(f"  File 001: {md5_value}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate index.txt file with file names and MD5 values')
    parser.add_argument('--folder', help='Input folder path containing TAR files')
    parser.add_argument('--input', '-i', help='Input single TAR file path')
    parser.add_argument('--output', '-o', required=True, help='Output index.txt file path')
    
    args = parser.parse_args()
    
    if args.folder:
        generate_index_from_folder(args.folder, args.output)
    elif args.input:
        generate_index_from_single_file(args.input, args.output)
    else:
        print("Error: Please specify either --folder or --input")
        exit(1) 