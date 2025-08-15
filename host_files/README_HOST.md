# 宿主机端文件传输系统

## 概述

这是宿主机端的文件传输组件，负责截图、转换文件、验证完整性，实现与虚拟机的自动化文件传输。

## 文件说明

### 核心脚本
- `host_screenshot.py` - 宿主机端自动截图脚本
- `bmp_to_tar.py` - BMP到TAR转换工具
- `bmp_to_txt.py` - BMP到TXT转换工具

### 启动脚本
- `start_host_transfer.bat` - 宿主机端启动脚本

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
   mkdir "D:\transferPath"
   mkdir "D:\sijinnzhi\example"
   ```

## 使用方法

### 1. 启动自动传输
运行启动脚本：
```bash
start_host_transfer.bat
```

或者直接运行：
```bash
python host_screenshot.py
```

### 2. 等待虚拟机端准备
脚本启动后会等待5秒，然后开始自动截图和转换过程。

## 配置选项

### host_screenshot.py 参数
```bash
python host_screenshot.py --transfer-path "D:\transferPath" --output-folder "D:\sijinnzhi\example" --monitor-id 2 --screenshot-interval 5 --max-retries 3
```

参数说明：
- `--transfer-path`: 传输路径（默认：D:\transferPath）
- `--output-folder`: 输出文件夹（默认：D:\sijinnzhi\example）
- `--monitor-id`: 显示器ID（默认：2，即第二屏幕）
- `--screenshot-interval`: 截图间隔秒数（默认：5秒）
- `--max-retries`: MD5验证最大重试次数（默认：3次）

## 工作流程

1. **初始化阶段**：
   - 等待5秒让虚拟机准备
   - 截图 `index.bmp` 并转换为 `index.txt`
   - 读取文件列表

2. **传输阶段**：
   - 每5秒截图一次
   - 将截图转换为TAR文件
   - 验证MD5值（带重试机制）
   - 保存到传输路径

3. **完成阶段**：
   - 所有文件处理完成后自动结束

## 改进功能

### 1. MD5验证重试机制
- 当TAR文件MD5值不匹配时，会自动重试最多3次
- 每次重试间隔3秒
- 只有在所有重试都失败后才会跳过该文件

### 2. 更好的错误处理
- 完善的异常处理机制
- 详细的错误信息输出
- 程序崩溃时自动清理资源

### 3. 信号处理
- 支持Ctrl+C中断程序
- 程序退出时自动清理资源
- 确保临时文件被正确删除

### 4. 可配置参数
- 支持自定义重试次数
- 支持自定义截图间隔
- 支持自定义显示器ID

## 故障排除

### 常见问题

1. **Python路径错误**：
   - 检查 `start_host_transfer.bat` 中的Python路径
   - 确保Python已正确安装并添加到PATH

2. **找不到显示器**：
   - 确保虚拟机窗口在第二屏幕上可见
   - 检查显示器ID设置
   ```bash
   # 查看可用显示器
   python -c "import mss; print(mss.mss().monitors)"
   ```

3. **依赖包安装失败**：
   ```bash
   # 如果mss安装失败
   pip install mss
   
   # 如果Pillow安装失败
   pip install Pillow
   
   # 如果numpy安装失败
   pip install numpy
   ```

4. **权限错误**：
   - 确保对输出文件夹有写入权限
   - 以管理员身份运行脚本

5. **文件路径错误**：
   - 确保所有路径都存在
   - 检查文件夹权限

6. **MD5验证失败**：
   - 检查截图质量
   - 确保虚拟机窗口清晰可见
   - 程序会自动重试，如果仍然失败请检查虚拟机端

### 调试模式

可以通过修改脚本参数来调试：
```bash
python host_screenshot.py --screenshot-interval 10 --monitor-id 1 --max-retries 5
```

### 手动测试截图
```bash
python -c "
import mss
with mss.mss() as sct:
    print('Available monitors:', sct.monitors)
    screenshot = sct.grab(sct.monitors[2])
    screenshot.save('test_screenshot.png')
    print('Screenshot saved as test_screenshot.png')
"
```

### 手动测试转换
```bash
# 测试BMP到TAR转换
python bmp_to_tar.py --input "test.bmp" --output "test.tar"

# 测试BMP到TXT转换
python bmp_to_txt.py --input "test.bmp" --output "test.txt"
```

## 注意事项

1. 确保虚拟机窗口始终可见
2. 不要在传输过程中移动或调整窗口
3. 保持网络连接稳定
4. 确保共享文件夹权限正确
5. 大文件传输可能需要较长时间
6. 确保有足够的磁盘空间
7. 程序支持Ctrl+C中断，会自动清理资源

## 系统要求

- Windows 7/10/11
- Python 3.6+
- 至少2个显示器
- 共享文件夹访问权限
- 足够的磁盘空间

## 性能优化

### 调整传输速度
如果传输速度较慢，可以增加截图间隔：
```bash
python host_screenshot.py --screenshot-interval 10
```

### 调整显示器ID
如果虚拟机不在第二屏幕，可以调整显示器ID：
```bash
python host_screenshot.py --monitor-id 1
```

### 自定义输出路径
可以自定义输出路径：
```bash
python host_screenshot.py --output-folder "C:\my_output" --transfer-path "C:\my_transfer"
```

### 调整重试次数
如果网络不稳定，可以增加重试次数：
```bash
python host_screenshot.py --max-retries 5
```

## 更新日志

### v1.1 (最新)
- ✅ 添加MD5验证重试机制
- ✅ 改进错误处理和资源清理
- ✅ 添加信号处理器
- ✅ 支持可配置参数
- ✅ 完善异常处理

### v1.0
- ✅ 基本自动截图功能
- ✅ 支持文件转换和验证
- ✅ 增加MD5校验
- ✅ 优化性能和稳定性 