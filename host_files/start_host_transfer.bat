@echo off
setlocal enabledelayedexpansion
cls
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


::Set default type value
set "choice=1"

echo.
echo Please select an option according to the BMP files size.
echo 1. 1080P (1920x1080) - Default
echo 2. 4K (3840x2160) real pixels: 2560*1600
echo 3. Custom resolution
echo 4. Quit
echo.

set /p choice="Please type your choice(1-4): "

if "%choice%"=="1" (
    set /a WIDTH=1910
    set /a HEIGHT=1070
)
if "%choice%"=="2" (
    set /a WIDTH=2550
    set /a HEIGHT=1590
)
if "%choice%"=="3" (
    echo.
    set /p WIDTH="Enter custom width (default 2540): "
    if "!WIDTH!"=="" set "WIDTH=2540"
    set /p HEIGHT="Enter custom height (default 1470): "
    if "!HEIGHT!"=="" set "HEIGHT=1470"
)
if "%choice%"=="4" goto End

echo.
echo Selected resolution: (!WIDTH!x!HEIGHT!)
echo.

:: Start the host machine script
"%PYTHONEXE%" host_screenshot.py --bmp-width=!WIDTH! --bmp-height !HEIGHT!

:End
echo.
echo Press any key to exit...
pause >nul 