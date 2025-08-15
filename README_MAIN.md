# 虚拟机到宿主机自动文件传输系统

## 项目结构

```
requirement/
├── vm_files/                    # 虚拟机端文件
│   ├── convert.bat              # 文件转换主脚本
│   ├── generate_index.py        # 生成文件索引和MD5值
│   ├── txt_to_bmp.py           # 将index.txt转换为index.bmp
│   ├── vm_player.py            # 虚拟机端自动播放脚本
│   ├── window.py               # 图片显示工具
│   ├── tar_to_bmp.py           # TAR到BMP转换工具
│   ├── start_vm_transfer.bat   # 虚拟机端启动脚本
│   ├── requirements.txt        # Python依赖包列表
│   ├── README.md              # 完整系统说明文档
│   └── README_VM.md           # 虚拟机端专用说明
│
├── host_files/                  # 宿主机端文件
│   ├── host_screenshot.py      # 宿主机端自动截图脚本
│   ├── bmp_to_tar.py          # BMP到TAR转换工具
│   ├── bmp_to_txt.py          # BMP到TXT转换工具
│   ├── start_host_transfer.bat # 宿主机端启动脚本
│   ├── requirements.txt        # Python依赖包列表
│   ├── README.md              # 完整系统说明文档
│   └── README_HOST.md         # 宿主机端专用说明
│
├── deploy.bat                  # 一键部署工具
├── README_MAIN.md             # 主说明文档
├── README.md                  # 完整系统说明
├── requirements.txt           # 通用依赖包列表
├── requirement.txt            # 原始需求文档
└── snapshot.py               # 原始截图脚本
```

## 🚀 快速部署

### 方法一：使用一键部署工具（推荐）

1. **运行部署工具**
   ```bash
   deploy.bat
   ```

2. **选择部署目标**
   - 选择 `1` 部署到虚拟机端
   - 选择 `2` 部署到宿主机端
   - 选择 `3` 查看部署说明

3. **按提示完成部署**

### 方法二：手动部署

#### 虚拟机端部署

1. **复制文件**
   ```bash
   # 将 vm_files/ 文件夹复制到虚拟机
   xcopy vm_files\* H:\convert\ /E /Y
   ```

2. **安装依赖**
   ```bash
   cd H:\convert\
   pip install -r requirements.txt
   ```

3. **创建文件夹**
   ```bash
   mkdir input
   mkdir output
   mkdir temp
   mkdir Y:\transferPath
   ```

#### 宿主机端部署

1. **复制文件**
   ```bash
   # 将 host_files/ 文件夹复制到宿主机
   xcopy host_files\* D:\transfer\ /E /Y
   ```

2. **安装依赖**
   ```bash
   cd D:\transfer\
   pip install -r requirements.txt
   ```

3. **创建文件夹**
   ```bash
   mkdir "D:\transferPath"
   mkdir "D:\sijinnzhi\example"
   ```

## 📋 使用步骤

### 1. 虚拟机端操作

1. **准备文件**
   ```bash
   # 将需要传输的文件放入 input 文件夹
   ```

2. **生成传输文件**
   ```bash
   convert.bat
   # 选择合适的分辨率选项
   ```

3. **启动传输**
   ```bash
   start_vm_transfer.bat
   ```

### 2. 宿主机端操作

1. **启动传输**
   ```bash
   start_host_transfer.bat
   ```

2. **等待完成**
   - 系统会自动截图、转换、验证文件
   - 传输完成后会自动结束

## 🔧 系统要求

### 虚拟机端
- ✅ Windows 7/10/11
- ✅ Python 3.6+
- ✅ PyQt5
- ✅ 至少2个显示器（或虚拟机支持多显示器）
- ✅ 共享文件夹访问权限

### 宿主机端
- ✅ Windows 7/10/11
- ✅ Python 3.6+
- ✅ 至少2个显示器
- ✅ 共享文件夹访问权限
- ✅ 足够的磁盘空间

## 📖 详细文档

| 文档 | 说明 |
|------|------|
| `README_MAIN.md` | 完整系统说明和项目结构 |
| `vm_files/README_VM.md` | 虚拟机端详细使用说明 |
| `host_files/README_HOST.md` | 宿主机端详细使用说明 |
| `README.md` | 原始完整系统说明 |

## 🛠️ 故障排除

### 常见问题

1. **Python路径错误**
   ```bash
   # 检查Python是否正确安装
   python --version
   
   # 更新启动脚本中的Python路径
   ```

2. **依赖包安装失败**
   ```bash
   # 单独安装依赖包
   pip install mss pillow numpy PyQt5
   ```

3. **找不到显示器**
   ```bash
   # 查看可用显示器
   python -c "import mss; print(mss.mss().monitors)"
   ```

4. **权限错误**
   - 以管理员身份运行脚本
   - 检查文件夹权限

5. **MD5验证失败**
   - 检查图片显示是否正常
   - 确保截图区域正确
   - 程序会自动重试，如果仍然失败请重新运行转换过程

### 调试方法

1. **虚拟机端调试**
   ```bash
   python vm_player.py --check-interval 1 --output-folder "C:\test\output" --max-retries 5
   ```

2. **宿主机端调试**
   ```bash
   python host_screenshot.py --screenshot-interval 10 --monitor-id 1 --max-retries 5
   ```

## ⚡ 性能优化

### 调整传输速度
- 虚拟机端：调整 `--check-interval` 参数
- 宿主机端：调整 `--screenshot-interval` 参数

### 调整分辨率
- 在convert.bat中选择合适的分辨率
- 高分辨率支持更大文件，但传输时间更长

### 自定义路径
- 可以自定义所有输入输出路径
- 确保路径存在且有正确权限

## 📝 注意事项

1. ✅ 确保虚拟机窗口始终可见
2. ✅ 不要在传输过程中移动或调整窗口
3. ✅ 保持网络连接稳定
4. ✅ 确保共享文件夹权限正确
5. ✅ 大文件传输可能需要较长时间
6. ✅ 定期清理临时文件
7. ✅ 程序支持Ctrl+C中断，会自动清理资源

## 🎯 工作流程

```
1. 文件准备阶段
   ├── 虚拟机：将文件放入input文件夹
   └── 虚拟机：运行convert.bat生成传输文件

2. 传输初始化
   ├── 宿主机：启动host_screenshot.py
   ├── 虚拟机：启动vm_player.py
   ├── 虚拟机：播放index.bmp
   ├── 宿主机：截图并转换为index.txt
   └── 虚拟机：验证MD5值匹配（带重试机制）

3. 自动传输阶段
   ├── 虚拟机：依次播放每个BMP文件
   ├── 宿主机：每5秒截图一次
   ├── 宿主机：将截图转换为TAR文件并验证MD5（带重试机制）
   └── 虚拟机：检测到对应TAR文件后播放下一个文件

4. 完成阶段
   └── 所有文件传输完成后自动结束
```

## 🆘 技术支持

如果遇到问题，请按以下顺序查看文档：

1. 查看对应的专用说明文档
2. 查看完整系统说明文档
3. 使用调试模式进行问题排查
4. 检查系统要求和依赖包安装

## 🆕 最新改进 (v1.1)

### 虚拟机端改进
- ✅ **MD5验证重试机制**：当MD5值不匹配时，自动重试最多3次
- ✅ **自动窗口管理**：程序退出时自动关闭所有打开的图片窗口
- ✅ **信号处理**：支持Ctrl+C中断程序，确保资源正确清理
- ✅ **可配置参数**：支持自定义重试次数、等待超时时间等

### 宿主机端改进
- ✅ **MD5验证重试机制**：TAR文件MD5验证失败时自动重试
- ✅ **改进错误处理**：完善的异常处理机制和资源清理
- ✅ **信号处理**：支持Ctrl+C中断，自动清理临时文件
- ✅ **可配置参数**：支持自定义重试次数、截图间隔等

### 通用改进
- ✅ **更好的错误处理**：详细的错误信息输出和异常处理
- ✅ **资源管理**：确保程序退出时正确清理所有资源
- ✅ **调试支持**：提供多种调试模式和测试方法
- ✅ **文档完善**：更新所有相关文档，包含新功能说明

---

**祝您使用愉快！** 🎉 