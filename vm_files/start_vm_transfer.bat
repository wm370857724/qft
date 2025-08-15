@echo off
echo ========================================
echo    虚拟机端自动传输启动脚本
echo ========================================
echo.

:: 设置Python路径
set "PYTHONEXE=C:\Program Files\Python36\python.exe"

:: 检查Python是否可用
"%PYTHONEXE%" --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python or update the PYTHONEXE path.
    echo Current path: %PYTHONEXE%
    pause
    goto End
)

echo 正在启动虚拟机端自动播放脚本...
echo.
echo 请确保：
echo 1. 已经运行了convert.bat生成了所有文件
echo 2. 宿主机端已经启动了host_screenshot.py
echo 3. 虚拟机窗口在第二屏幕上可见
echo.

:: 启动虚拟机端脚本
"%PYTHONEXE%" vm_player.py

:End
echo.
echo 按任意键退出...
pause >nul 