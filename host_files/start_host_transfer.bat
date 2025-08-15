@echo off
echo ===============================================
echo    Host machine auto-transfer startup script
echo ===============================================
echo.

:: Clean and create a Transfer folder.
echo Cleaning up previous files...
rd /s /q "transferPath" 2>nul
if not exist "transferPath" mkdir "transferPath"

:: Set Python path
set "PYTHONEXE=python"

:: Check if Python is available
"%PYTHONEXE%" --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python or update the PYTHONEXE path.
    echo Current path: %PYTHONEXE%
    pause
    goto End
)

echo Launching host machine automatic screenshot script...
echo.
echo Please ensure:
echo 1. All files are ready on the virtual machine side
echo 2. The virtual machine window is visible on the second screen
echo 3. The transfer path D:\transferPath exists
echo.

:: Start the host machine script
"%PYTHONEXE%" host_screenshot.py

:End
echo.
echo Press any key to exit...
pause >nul 