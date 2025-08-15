# 虚拟机端文件传输系统

## 概述

这是虚拟机端的文件传输组件，负责生成文件列表、播放图片文件，实现与宿主机的自动化文件传输。

## 文件说明

### 核心脚本
- `convert.bat` - 文件转换主脚本，生成TAR分片和BMP图片
- `generate_index.py` - 生成文件索引和MD5值
- `txt_to_bmp.py` - 将index.txt转换为index.bmp
- `vm_player.py` - 虚拟机端自动播放脚本
- `window.py` - 图片显示工具
- `tar_to_bmp.py` - TAR到BMP转换工具

### 启动脚本
- `start_vm_transfer.bat` - 虚拟机端启动脚本

### 配置文件
- `requirements.txt` - Python依赖包列表
- `README.md` - 完整系统说明文档

## 安装步骤

1. **安装Python 3.6+**
   ```bash
   # 下载并安装Python 3.6或更高版本
   # 确保添加到系统PATH
   ```

2. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

3. **创建必要的文件夹**
   ```bash
   mkdir input
   mkdir output
   mkdir temp
   ```

## 使用方法

### 1. 准备文件
将需要传输的文件放入 `input` 文件夹中。

### 2. 生成传输文件
运行转换脚本：
```bash
convert.bat
```

选择合适的分辨率选项：
- 1. 1080P (1920x1080) - 适合大多数情况
- 2. 4K (3840x2160) - 高分辨率，支持更大文件
- 3. 自定义分辨率 - 根据实际需求调整

系统会自动：
- 压缩文件并生成TAR分片
- 将TAR文件转换为BMP图片
- 生成 `index.txt` 文件（包含文件编号和MD5值）
- 将 `index.txt` 转换为 `index.bmp` 图片

### 3. 启动自动传输
确保宿主机端已经启动后，运行：
```bash
start_vm_transfer.bat
```

或者直接运行：
```bash
python vm_player.py
```

## 配置选项

### vm_player.py 参数
```bash
python vm_player.py --output-folder "H:\convert\output" --transfer-path "Y:\transferPath" --check-interval 3 --max-retries 3 --wait-timeout 30
```

参数说明：
- `--output-folder`: 输出文件夹路径（默认：H:\convert\output）
- `--transfer-path`: 传输路径（默认：Y:\transferPath）
- `--check-interval`: 检查间隔秒数（默认：3秒）
- `--max-retries`: MD5验证最大重试次数（默认：3次）
- `--wait-timeout`: 等待index.txt文件超时时间（默认：30秒）

### window.py 参数
```bash
python window.py --image "image.bmp" --screen 1
```

参数说明：
- `--image`: 图片文件路径
- `--screen`: 目标屏幕索引（0开始）

## 工作流程

1. **初始化阶段**：
   - 播放 `index.bmp` 文件
   - 等待宿主机截图并生成 `index.txt`
   - 验证MD5值匹配（带重试机制）

2. **传输阶段**：
   - 依次播放每个BMP文件
   - 检测对应的TAR文件是否生成
   - 播放下一个文件

3. **完成阶段**：
   - 所有文件传输完成后自动结束

## 改进功能

### 1. MD5验证重试机制
- 当MD5值不匹配时，会自动重试最多3次
- 每次重试间隔5秒
- 只有在所有重试都失败后才会退出程序

### 2. 自动窗口管理
- 程序退出时自动关闭所有打开的图片窗口
- 支持Ctrl+C中断程序
- 确保资源正确清理

### 3. 更好的错误处理
- 完善的异常处理机制
- 详细的错误信息输出
- 程序崩溃时自动清理资源

### 4. 可配置参数
- 支持自定义重试次数
- 支持自定义等待超时时间
- 支持自定义检查间隔

## 故障排除

### 常见问题

1. **Python路径错误**：
   - 检查 `start_vm_transfer.bat` 中的Python路径
   - 确保Python已正确安装并添加到PATH

2. **找不到显示器**：
   - 确保虚拟机窗口在第二屏幕上可见
   - 检查显示器设置

3. **文件路径错误**：
   - 确保所有路径都存在
   - 检查文件夹权限

4. **PyQt5安装失败**：
   ```bash
   pip install PyQt5
   # 如果失败，尝试：
   pip install PyQt5-tools
   ```

5. **MD5验证失败**：
   - 检查图片显示是否正常
   - 确保截图区域正确
   - 程序会自动重试，如果仍然失败请检查宿主机端

### 调试模式

可以通过修改脚本参数来调试：
```bash
python vm_player.py --check-interval 1 --output-folder "C:\test\output" --max-retries 5
```

### 手动测试
```bash
# 测试MD5计算
python -c "import hashlib; print(hashlib.md5(open('index.txt', 'rb').read()).hexdigest())"

# 测试图片显示
python window.py --image "output\index.bmp" --screen 1
```

## 注意事项

1. 确保虚拟机窗口始终可见
2. 不要在传输过程中移动或调整窗口
3. 保持网络连接稳定
4. 确保共享文件夹权限正确
5. 大文件传输可能需要较长时间
6. 程序支持Ctrl+C中断，会自动清理资源

## 系统要求

- Windows 7/10/11
- Python 3.6+
- PyQt5
- 至少2个显示器（或虚拟机支持多显示器）
- 共享文件夹访问权限

## 更新日志

### v1.1 (最新)
- ✅ 添加MD5验证重试机制
- ✅ 自动窗口管理和资源清理
- ✅ 改进错误处理
- ✅ 支持可配置参数
- ✅ 添加信号处理器

### v1.0
- ✅ 基本自动传输功能
- ✅ 支持多文件传输
- ✅ 增加MD5校验
- ✅ 优化性能和稳定性 