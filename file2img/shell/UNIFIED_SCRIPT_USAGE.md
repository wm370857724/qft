# 统一转换脚本使用说明

## 概述

`multi_tars_to_bmps_4K_optimized_py3.py` 现在是一个统一的转换脚本，支持单文件和多文件处理，无需单独的 `single_tar_to_bmp_optimized_py3.py`。

## 使用方法

### 1. 单文件处理

```bash
# 处理单个TAR文件
python3 multi_tars_to_bmps_4K_optimized_py3.py --input example.tar --output output.bmp

# 指定分辨率
python3 multi_tars_to_bmps_4K_optimized_py3.py --input example.tar --output output.bmp --width 1920 --height 1080
```

### 2. 多文件处理（文件夹模式）

```bash
# 处理temp文件夹中的所有文件
python3 multi_tars_to_bmps_4K_optimized_py3.py --folder temp

# 指定文件夹和分辨率
python3 multi_tars_to_bmps_4K_optimized_py3.py --folder temp --width 2540 --height 1470

# 使用单进程模式
python3 multi_tars_to_bmps_4K_optimized_py3.py --folder temp --single

# 指定工作进程数
python3 multi_tars_to_bmps_4K_optimized_py3.py --folder temp --workers 4
```

### 3. 兼容模式

```bash
# 使用兼容模式（与原始版本行为一致）
python3 multi_tars_to_bmps_4K_optimized_py3.py --folder temp --legacy
```

## 命令行参数

```bash
usage: multi_tars_to_bmps_4K_optimized_py3.py [-h] [--folder FOLDER] [--input INPUT] [--output OUTPUT]
                                              [--width WIDTH] [--height HEIGHT] [--single]
                                              [--workers WORKERS] [--legacy]

Optimized TAR to BMP converter

optional arguments:
  -h, --help            show this help message and exit
  --folder FOLDER       Input folder path (for multiple files)
  --input INPUT, -i INPUT
                        Input single TAR file path
  --output OUTPUT, -o OUTPUT
                        Output BMP file path
  --width WIDTH         Output image width (default: 2540)
  --height HEIGHT       Output image height (default: 1470)
  --single              Use single process mode
  --workers WORKERS     Number of worker processes
  --legacy              Use legacy mode (compatible with original)
```

## 使用场景

### 场景1: 单文件转换
```bash
# 将单个TAR文件转换为BMP
python3 multi_tars_to_bmps_4K_optimized_py3.py --input data.tar --output result.bmp
```

### 场景2: 批量文件转换
```bash
# 将temp文件夹中的所有TAR文件转换为BMP
python3 multi_tars_to_bmps_4K_optimized_py3.py --folder temp
```

### 场景3: 自定义分辨率
```bash
# 使用自定义分辨率
python3 multi_tars_to_bmps_4K_optimized_py3.py --input data.tar --output result.bmp --width 1920 --height 1080
```

### 场景4: 性能优化
```bash
# 使用4个工作进程
python3 multi_tars_to_bmps_4K_optimized_py3.py --folder temp --workers 4

# 使用单进程模式（适合小文件）
python3 multi_tars_to_bmps_4K_optimized_py3.py --folder temp --single
```

## 批处理脚本集成

在批处理脚本中，统一使用这个脚本：

```batch
# 单文件处理
"%PYTHONEXE%" "%SHELL_FOLDER%\multi_tars_to_bmps_4K_optimized_py3.py" --input "%TAR_FILE%" --output "%OUTPUT_FOLDER%\output.bmp" --width !WIDTH! --height !HEIGHT!

# 多文件处理
"%PYTHONEXE%" "%SHELL_FOLDER%\multi_tars_to_bmps_4K_optimized_py3.py" --folder temp --width !WIDTH! --height !HEIGHT!
```

## 优势

### 1. 简化维护
- 只需要维护一个脚本
- 减少代码重复
- 统一的错误处理和日志

### 2. 功能完整
- 支持单文件和多文件处理
- 支持自定义分辨率
- 支持多进程和单进程模式
- 支持兼容模式

### 3. 性能优化
- 统一的优化算法
- 向量化操作
- 内存优化
- 多进程支持

## 迁移说明

如果你之前使用了 `single_tar_to_bmp_optimized_py3.py`，现在可以这样迁移：

```bash
# 旧方式
python3 single_tar_to_bmp_optimized_py3.py --input file.tar --output result.bmp

# 新方式
python3 multi_tars_to_bmps_4K_optimized_py3.py --input file.tar --output result.bmp
```

功能完全相同，但性能更好，维护更简单。 