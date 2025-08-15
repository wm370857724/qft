@echo off
setlocal enabledelayedexpansion
cls

echo ========================================
echo    虚拟机到宿主机文件传输系统部署工具
echo ========================================
echo.
echo 请选择部署目标：
echo 1. 部署到虚拟机端
echo 2. 部署到宿主机端
echo 3. 查看部署说明
echo 4. 退出
echo.

set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" goto DeployVM
if "%choice%"=="2" goto DeployHost
if "%choice%"=="3" goto ShowHelp
if "%choice%"=="4" goto Exit

echo 无效选择，请重新输入。
goto End

:DeployVM
echo.
echo ========================================
echo           部署到虚拟机端
echo ========================================
echo.
echo 请确保：
echo 1. 已安装Python 3.6+
echo 2. 已配置共享文件夹（D盘映射到Y盘）
echo 3. 有足够的磁盘空间
echo.

set /p vm_path="请输入虚拟机部署路径 (默认: H:\convert\): "
if "!vm_path!"=="" set "vm_path=H:\convert\"

echo.
echo 正在部署到: !vm_path!
echo.

:: 创建目标目录
if not exist "!vm_path!" (
    echo 创建目录: !vm_path!
    mkdir "!vm_path!"
)

:: 复制文件
echo 复制虚拟机端文件...
xcopy "vm_files\*" "!vm_path!" /E /Y /Q

:: 创建必要文件夹
echo 创建必要文件夹...
if not exist "!vm_path!input" mkdir "!vm_path!input"
if not exist "!vm_path!output" mkdir "!vm_path!output"
if not exist "!vm_path!temp" mkdir "!vm_path!temp"

:: 创建共享文件夹
if not exist "Y:\transferPath" (
    echo 创建共享文件夹: Y:\transferPath
    mkdir "Y:\transferPath"
)

echo.
echo 虚拟机端部署完成！
echo.
echo 下一步操作：
echo 1. 将需要传输的文件放入 !vm_path!input 文件夹
echo 2. 运行 convert.bat 生成传输文件
echo 3. 运行 start_vm_transfer.bat 启动传输
echo.
echo 详细说明请查看: !vm_path!README_VM.md
echo.
goto End

:DeployHost
echo.
echo ========================================
echo           部署到宿主机端
echo ========================================
echo.
echo 请确保：
echo 1. 已安装Python 3.6+
echo 2. 有足够的磁盘空间
echo 3. 虚拟机窗口在第二屏幕上可见
echo.

set /p host_path="请输入宿主机部署路径 (默认: D:\transfer\): "
if "!host_path!"=="" set "host_path=D:\transfer\"

echo.
echo 正在部署到: !host_path!
echo.

:: 创建目标目录
if not exist "!host_path!" (
    echo 创建目录: !host_path!
    mkdir "!host_path!"
)

:: 复制文件
echo 复制宿主机端文件...
xcopy "host_files\*" "!host_path!" /E /Y /Q

:: 创建必要文件夹
echo 创建必要文件夹...
if not exist "D:\transferPath" mkdir "D:\transferPath"
if not exist "D:\sijinnzhi\example" mkdir "D:\sijinnzhi\example"

echo.
echo 宿主机端部署完成！
echo.
echo 下一步操作：
echo 1. 确保虚拟机端已准备就绪
echo 2. 运行 start_host_transfer.bat 启动传输
echo.
echo 详细说明请查看: !host_path!README_HOST.md
echo.
goto End

:ShowHelp
echo.
echo ========================================
echo           部署说明
echo ========================================
echo.
echo 系统架构：
echo - 虚拟机端：负责生成文件列表、播放图片文件
echo - 宿主机端：负责截图、转换文件、验证完整性
echo - 通信方式：通过共享文件夹进行消息传递
echo.
echo 部署步骤：
echo.
echo 1. 虚拟机端部署：
echo    - 运行此脚本选择选项1
echo    - 安装Python依赖：pip install -r requirements.txt
echo    - 将文件放入input文件夹
echo    - 运行convert.bat生成传输文件
echo.
echo 2. 宿主机端部署：
echo    - 运行此脚本选择选项2
echo    - 安装Python依赖：pip install -r requirements.txt
echo    - 确保虚拟机窗口可见
echo.
echo 3. 启动传输：
echo    - 先启动宿主机端：start_host_transfer.bat
echo    - 再启动虚拟机端：start_vm_transfer.bat
echo.
echo 系统要求：
echo - Windows 7/10/11
echo - Python 3.6+
echo - 至少2个显示器
echo - 共享文件夹访问权限
echo.
echo 详细文档：
echo - README_MAIN.md - 完整系统说明
echo - vm_files/README_VM.md - 虚拟机端说明
echo - host_files/README_HOST.md - 宿主机端说明
echo.
goto End

:Exit
echo.
echo 退出部署工具。
goto End

:End
echo.
echo 按任意键退出...
pause >nul
endlocal 