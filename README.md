# 虚拟机到宿主机自动文件传输系统

## 概述

这是一个自动化文件传输系统，通过屏幕截图的方式实现从虚拟机到宿主机的文件传输。系统使用BMP图片作为传输媒介，通过MD5校验确保文件完整性。

## 系统架构

- **虚拟机端**: 负责生成文件列表、播放图片文件
- **宿主机端**: 负责截图、转换文件、验证完整性
- **通信方式**: 通过共享文件夹 `D:\transferPath` (虚拟机映射为 `Y:\transferPath`) 进行消息传递

## 文件说明

### 核心脚本
- `convert.bat` - 文件转换主脚本（已修改，增加index.txt生成）
- `generate_index.py` - 生成文件索引和MD5值
- `txt_to_bmp.py` - 将index.txt转换为index.bmp
- `bmp_to_txt.py` - 将index.bmp转换回index.txt
- `vm_player.py` - 虚拟机端自动播放脚本
- `host_screenshot.py` - 宿主机端自动截图脚本

### 辅助脚本
- `tar_to_bmp.py` - TAR到BMP转换（原有）
- `bmp_to_tar.py` - BMP到TAR转换（已修改，支持命令行参数）

### 启动脚本
- `start_vm_transfer.bat` - 虚拟机端启动脚本
- `start_host_transfer.bat` - 宿主机端启动脚本

## 使用步骤

### 1. 准备工作

1. **虚拟机端**:
   - 将需要传输的文件放入 `input` 文件夹
   - 确保Python 3.6+已安装
   - 确保PyQt5已安装（用于图片显示）

2. **宿主机端**:
   - 确保Python 3.6+已安装
   - 安装必要的依赖：`pip install mss pillow numpy`
   - 确保 `D:\transferPath` 文件夹存在

### 2. 生成文件

在虚拟机端运行：
```bash
convert.bat
```

选择合适的分辨率选项，系统会：
1. 压缩文件并生成TAR分片
2. 将TAR文件转换为BMP图片
3. 生成 `index.txt` 文件（包含文件编号和MD5值）
4. 将 `index.txt` 转换为 `index.bmp` 图片

### 3. 启动自动传输

#### 步骤1: 启动宿主机端脚本
在宿主机端运行：
```bash
start_host_transfer.bat
```
或者直接运行：
```bash
python host_screenshot.py
```

#### 步骤2: 启动虚拟机端脚本
在虚拟机端运行：
```bash
start_vm_transfer.bat
```
或者直接运行：
```bash
python vm_player.py
```

### 4. 传输流程

1. **初始化阶段**:
   - 虚拟机播放 `index.bmp` 文件
   - 宿主机截图并转换为 `index.txt`
   - 虚拟机验证MD5值匹配

2. **文件传输阶段**:
   - 虚拟机依次播放每个BMP文件
   - 宿主机每5秒截图一次
   - 宿主机将截图转换为TAR文件
   - 宿主机验证MD5值并保存到传输路径
   - 虚拟机检测到对应TAR文件后播放下一个文件

3. **完成阶段**:
   - 所有文件传输完成后自动结束

## 配置选项

### 虚拟机端配置 (vm_player.py)
```bash
python vm_player.py --output-folder "H:\convert\output" --transfer-path "Y:\transferPath" --check-interval 3
```

### 宿主机端配置 (host_screenshot.py)
```bash
python host_screenshot.py --transfer-path "D:\transferPath" --output-folder "D:\sijinnzhi\example" --monitor-id 2 --screenshot-interval 5
```

## 故障排除

### 常见问题

1. **找不到Python**:
   - 检查Python是否正确安装
   - 更新脚本中的Python路径

2. **找不到显示器**:
   - 确保虚拟机窗口在第二屏幕上可见
   - 检查显示器ID设置

3. **MD5值不匹配**:
   - 检查图片显示是否正常
   - 确保截图区域正确
   - 重新运行转换过程

4. **文件传输中断**:
   - 检查网络连接
   - 确保共享文件夹权限正确
   - 重新启动传输脚本

### 调试模式

可以通过修改脚本中的参数来调整行为：
- 增加等待时间
- 调整截图间隔
- 修改文件路径

## 技术细节

### 文件格式
- **index.txt**: 每行格式为 `文件编号,MD5值`
- **BMP图片**: 使用四进制编码，4种颜色表示2位数据
- **TAR文件**: 标准TAR格式，支持分片

### 颜色映射
- 红色 (255,0,0) = '0'
- 绿色 (0,255,0) = '1'  
- 蓝色 (0,0,255) = '2'
- 白色 (255,255,255) = '3'

### 性能优化
- 使用numpy向量化操作
- 多进程并行处理
- 内存优化的文件读写

## 注意事项

1. 确保虚拟机窗口始终可见
2. 不要在传输过程中移动或调整窗口
3. 保持网络连接稳定
4. 定期清理临时文件
5. 大文件传输可能需要较长时间

## 更新日志

- v1.0: 初始版本，实现基本自动传输功能
- 支持多文件传输
- 增加MD5校验
- 优化性能和稳定性 