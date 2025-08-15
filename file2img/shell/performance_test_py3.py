#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3 性能测试脚本 - 比较原始版本和优化版本的性能
"""

import time
import os
import tempfile
import shutil
from multiprocessing import cpu_count
import argparse

# 导入原始版本和优化版本
import multi_tars_to_bmps_4K as original
import multi_tars_to_bmps_4K_optimized_py3 as optimized

def create_test_files(num_files=5, file_size=1024*1024):  # 1MB each
    """创建测试文件"""
    test_dir = "temp_test"
    os.makedirs(test_dir, exist_ok=True)
    
    print(f"Creating {num_files} test files...")
    for i in range(num_files):
        filename = f"example.tar.{i:03d}"
        filepath = os.path.join(test_dir, filename)
        
        # 创建随机二进制数据
        with open(filepath, 'wb') as f:
            f.write(os.urandom(file_size))
    
    return test_dir

def cleanup_test_files(test_dir):
    """清理测试文件"""
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    # 清理输出文件
    if os.path.exists("output"):
        shutil.rmtree("output")

def test_original_version(test_dir):
    """测试原始版本"""
    print("Testing original version...")
    start_time = time.time()
    
    try:
        original.convert_folder(test_dir)
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Original version error: {e}")
        return None

def test_optimized_version(test_dir, use_multiprocessing=True, max_workers=None):
    """测试优化版本"""
    print(f"Testing optimized version (multiprocessing: {use_multiprocessing})...")
    start_time = time.time()
    
    try:
        optimized.convert_folder_optimized(
            test_dir, 
            use_multiprocessing=use_multiprocessing,
            max_workers=max_workers
        )
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Optimized version error: {e}")
        return None

def test_legacy_version(test_dir):
    """测试兼容版本"""
    print("Testing legacy compatible version...")
    start_time = time.time()
    
    try:
        optimized.convert_folder_legacy(test_dir)
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Legacy version error: {e}")
        return None

def run_performance_test(num_files=5, file_size=1024*1024, test_legacy=False):
    """运行完整的性能测试"""
    print("=" * 60)
    print("性能测试开始")
    print("=" * 60)
    
    # 创建测试文件
    test_dir = create_test_files(num_files, file_size)
    
    try:
        # 测试原始版本
        original_time = test_original_version(test_dir)
        
        # 清理输出
        if os.path.exists("output"):
            shutil.rmtree("output")
        
        # 测试优化版本（单进程）
        optimized_single_time = test_optimized_version(test_dir, use_multiprocessing=False)
        
        # 清理输出
        if os.path.exists("output"):
            shutil.rmtree("output")
        
        # 测试优化版本（多进程）
        optimized_multi_time = test_optimized_version(test_dir, use_multiprocessing=True)
        
        # 测试兼容版本（如果请求）
        legacy_time = None
        if test_legacy:
            # 清理输出
            if os.path.exists("output"):
                shutil.rmtree("output")
            legacy_time = test_legacy_version(test_dir)
        
        # 输出结果
        print("\n" + "=" * 60)
        print("性能测试结果")
        print("=" * 60)
        
        if original_time is not None:
            print(f"原始版本执行时间: {original_time:.2f} 秒")
        
        if optimized_single_time is not None:
            print(f"优化版本(单进程)执行时间: {optimized_single_time:.2f} 秒")
            if original_time is not None:
                speedup = original_time / optimized_single_time
                print(f"单进程性能提升: {speedup:.2f}x")
        
        if optimized_multi_time is not None:
            print(f"优化版本(多进程)执行时间: {optimized_multi_time:.2f} 秒")
            if original_time is not None:
                speedup = original_time / optimized_multi_time
                print(f"多进程性能提升: {speedup:.2f}x")
        
        if legacy_time is not None:
            print(f"兼容版本执行时间: {legacy_time:.2f} 秒")
            if original_time is not None:
                speedup = original_time / legacy_time
                print(f"兼容版本性能提升: {speedup:.2f}x")
        
        # 系统信息
        print(f"\n系统信息:")
        print(f"CPU核心数: {cpu_count()}")
        print(f"测试文件数: {num_files}")
        print(f"每个文件大小: {file_size / (1024*1024):.1f} MB")
        
        # 性能对比表格
        print(f"\n性能对比表格:")
        print(f"{'版本':<20} {'时间(秒)':<12} {'性能提升':<12}")
        print("-" * 50)
        
        if original_time is not None:
            print(f"{'原始版本':<20} {original_time:<12.2f} {'1.00x':<12}")
        
        if optimized_single_time is not None:
            speedup = original_time / optimized_single_time if original_time else 1.0
            print(f"{'优化版本(单进程)':<20} {optimized_single_time:<12.2f} {speedup:<12.2f}x")
        
        if optimized_multi_time is not None:
            speedup = original_time / optimized_multi_time if original_time else 1.0
            print(f"{'优化版本(多进程)':<20} {optimized_multi_time:<12.2f} {speedup:<12.2f}x")
        
        if legacy_time is not None:
            speedup = original_time / legacy_time if original_time else 1.0
            print(f"{'兼容版本':<20} {legacy_time:<12.2f} {speedup:<12.2f}x")
        
    finally:
        # 清理测试文件
        cleanup_test_files(test_dir)

def run_quick_test():
    """快速测试"""
    print("运行快速测试...")
    run_performance_test(num_files=3, file_size=512*1024)  # 512KB each

def run_full_test():
    """完整测试"""
    print("运行完整测试...")
    run_performance_test(num_files=10, file_size=1024*1024)  # 1MB each

def run_comprehensive_test():
    """综合测试，包含所有版本"""
    print("运行综合测试...")
    run_performance_test(num_files=5, file_size=1024*1024, test_legacy=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Performance test for TAR to BMP converter')
    parser.add_argument('--mode', choices=['quick', 'full', 'comprehensive'], 
                       default='quick', help='Test mode')
    parser.add_argument('--files', type=int, default=5, help='Number of test files')
    parser.add_argument('--size', type=int, default=1024*1024, help='Size of each test file in bytes')
    
    args = parser.parse_args()
    
    if args.mode == 'full':
        run_full_test()
    elif args.mode == 'comprehensive':
        run_comprehensive_test()
    else:
        run_quick_test() 