# -*- coding: utf-8 -*-
import time
import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append('.')

# 导入原始版本和优化版本
from single_bmp_to_tar_without_PIL import bmp_to_tar as original_bmp_to_tar
from single_bmp_to_tar_without_PIL_optimized import bmp_to_tar_optimized, bmp_to_tar_vectorized

def test_performance():
    """测试不同版本的性能"""
    test_file = 'example/example.bmp'
    
    if not os.path.exists(test_file):
        print(f"测试文件 {test_file} 不存在，请确保有可用的BMP文件")
        return
    
    print("性能测试开始...")
    print("=" * 50)
    
    # 测试原始版本
    print("测试原始版本...")
    start_time = time.time()
    try:
        original_bmp_to_tar(test_file, 'test_original.tar')
        original_time = time.time() - start_time
        print(f"原始版本执行时间: {original_time:.4f} 秒")
    except Exception as e:
        print(f"原始版本执行失败: {e}")
        original_time = None
    
    # 测试优化版本
    print("\n测试优化版本...")
    start_time = time.time()
    try:
        bmp_to_tar_optimized(test_file, 'test_optimized.tar')
        optimized_time = time.time() - start_time
        print(f"优化版本执行时间: {optimized_time:.4f} 秒")
    except Exception as e:
        print(f"优化版本执行失败: {e}")
        optimized_time = None
    
    # 测试向量化版本
    print("\n测试向量化版本...")
    start_time = time.time()
    try:
        bmp_to_tar_vectorized(test_file, 'test_vectorized.tar')
        vectorized_time = time.time() - start_time
        print(f"向量化版本执行时间: {vectorized_time:.4f} 秒")
    except Exception as e:
        print(f"向量化版本执行失败: {e}")
        vectorized_time = None
    
    # 比较结果
    print("\n" + "=" * 50)
    print("性能比较结果:")
    
    if original_time and optimized_time:
        speedup = original_time / optimized_time
        print(f"优化版本比原始版本快 {speedup:.2f} 倍")
    
    if original_time and vectorized_time:
        speedup = original_time / vectorized_time
        print(f"向量化版本比原始版本快 {speedup:.2f} 倍")
    
    if optimized_time and vectorized_time:
        speedup = optimized_time / vectorized_time
        print(f"向量化版本比优化版本快 {speedup:.2f} 倍")
    
    # 清理测试文件
    for file in ['test_original.tar', 'test_optimized.tar', 'test_vectorized.tar']:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n测试完成！")

def benchmark_small_functions():
    """对关键函数进行基准测试"""
    print("\n关键函数基准测试...")
    print("=" * 30)
    
    # 测试像素处理函数
    test_pixels = [(255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
    
    # 导入函数
    from single_bmp_to_tar_without_PIL import find_closest_color_by_rule
    from single_bmp_to_tar_without_PIL_optimized import find_closest_color_by_rule_optimized
    
    # 测试原始函数
    start_time = time.time()
    for _ in range(10000):
        for pixel in test_pixels:
            find_closest_color_by_rule(pixel)
    original_func_time = time.time() - start_time
    
    # 测试优化函数
    start_time = time.time()
    for _ in range(10000):
        for pixel in test_pixels:
            find_closest_color_by_rule_optimized(pixel)
    optimized_func_time = time.time() - start_time
    
    print(f"原始像素处理函数: {original_func_time:.4f} 秒")
    print(f"优化像素处理函数: {optimized_func_time:.4f} 秒")
    print(f"函数级优化提升: {original_func_time / optimized_func_time:.2f} 倍")

if __name__ == '__main__':
    test_performance()
    benchmark_small_functions() 