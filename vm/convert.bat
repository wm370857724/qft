@echo off
setlocal enabledelayedexpansion
cls

:: 设置Python 3路径（可以根据实际情况调整）
set "PYTHONEXE=C:\Program Files\Python36\python.exe"
set "SEVENZIP=C:\Program Files\7-Zip\7z.exe"

:: 检查Python 3是否可用
"%PYTHONEXE%" --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 not found. Please install Python 3 or update the PYTHONEXE path.
    echo Current path: %PYTHONEXE%
    pause
    goto End
)

:: 检查7-Zip是否可用
if not exist "%SEVENZIP%" (
    echo Error: 7-Zip not found at %SEVENZIP%
    echo Please install 7-Zip or update the SEVENZIP path.
    pause
    goto End
)

::Set default type value
set "choice=2"

echo ========================================
echo    TAR to BMP Converter (Optimized)
echo ========================================
echo.
echo Please select an option according to the external screen resolution.
echo 1. 1080P (1920x1080)
echo 2. 4K (3840x2160) real pixels: 2560*1600 - Default
echo 3. Custom resolution
echo 4. Quit
echo.

set /p choice="Please type your choice(1-4): "

if "%choice%"=="1" (
    set /a WIDTH=1910
    set /a HEIGHT=1070
    set "RESOLUTION=1080P"
    set "SURFFIX="
    set /a THRESHOLD=!WIDTH!*!HEIGHT!/4
)
if "%choice%"=="2" (
    set /a WIDTH=2550
    set /a HEIGHT=1590
    set "RESOLUTION=4K"
    set "SURFFIX=_4K"
    set /a THRESHOLD=!WIDTH!*!HEIGHT!/4
)
if "%choice%"=="3" (
    echo.
    set /p WIDTH="Enter custom width (default 2540): "
    if "!WIDTH!"=="" set "WIDTH=2540"
    set /p HEIGHT="Enter custom height (default 1470): "
    if "!HEIGHT!"=="" set "HEIGHT=1470"
    set "RESOLUTION=Custom"
    set "SURFFIX=_custom"
    set /a THRESHOLD=!WIDTH!*!HEIGHT!/4
)
if "%choice%"=="4" goto Exit

echo.
echo Selected resolution: %RESOLUTION% (!WIDTH!x!HEIGHT!)
echo Threshold size: %THRESHOLD% bytes
echo.

:: 设置文件夹路径
set "SOURCE_FOLDER=%cd%\input"
set "SHELL_FOLDER=%cd%\shell"
set "OUTPUT_FOLDER=%cd%\output"
set "TEMP_FOLDER=%cd%\temp"
set "SEVENZ_FILE=%TEMP_FOLDER%\files_compressed.7z"
set "TAR_FILE=%TEMP_FOLDER%\example.tar"

:: 清理并创建临时文件夹
echo Cleaning up previous files...
rd /s /q "%TEMP_FOLDER%" 2>nul
rd /s /q "%OUTPUT_FOLDER%" 2>nul
if not exist "%TEMP_FOLDER%" mkdir "%TEMP_FOLDER%"
if not exist "%OUTPUT_FOLDER%" mkdir "%OUTPUT_FOLDER%"

:: 检查输入文件夹是否存在
if not exist "%SOURCE_FOLDER%" (
    echo Error: Input folder not found at %SOURCE_FOLDER%
    echo Please place your files in the input folder.
    pause
    goto End
)

:: 检查输入文件夹是否为空
dir /b "%SOURCE_FOLDER%\*" >nul 2>&1
if errorlevel 1 (
    echo Error: Input folder is empty.
    echo Please add files to the input folder.
    pause
    goto End
)

echo.
echo Step 1: Compressing files with 7-Zip...
"%SEVENZIP%" a -r -t7z -mx9 -m0=LZMA2:d=27:mt=4:fb=64 "%SEVENZ_FILE%" "%SOURCE_FOLDER%"
if errorlevel 1 (
    echo Error: Failed to compress files with 7-Zip.
    pause
    goto End
)

:: 获取文件大小
for %%F in ("%SEVENZ_FILE%") do set "FILE_SIZE=%%~zF"
echo File size: %FILE_SIZE% bytes
echo Threshold: %THRESHOLD% bytes

echo.
echo Step 2: Creating TAR file...
if %FILE_SIZE% GTR %THRESHOLD% (
    echo File size exceeds threshold, creating split TAR files...
    "%SEVENZIP%" a -ttar -v%THRESHOLD% "%TAR_FILE%" "%SEVENZ_FILE%"
    if errorlevel 1 (
        echo Error: Failed to create split TAR files.
        pause
        goto End
    )
    
    echo.
    echo Step 3: Converting to BMP using optimized multi-file script...
    "%PYTHONEXE%" "%SHELL_FOLDER%\tar_to_bmp.py" --folder temp --width !WIDTH! --height !HEIGHT!
    
    :: 生成index.txt文件
    echo.
    echo Step 4: Generating index.txt file...
    "%PYTHONEXE%" "%SHELL_FOLDER%\generate_index.py" --folder temp --output "%OUTPUT_FOLDER%\index.txt"
   
) else (
    echo File size within threshold, creating single TAR file...
    "%SEVENZIP%" a -ttar "%TAR_FILE%" "%SEVENZ_FILE%"
    if errorlevel 1 (
        echo Error: Failed to create TAR file.
        pause
        goto End
    )
    
    echo.
    echo Step 3: Converting to BMP using optimized script...
    "%PYTHONEXE%" "%SHELL_FOLDER%\tar_to_bmp.py" --input "%TAR_FILE%" --output "%OUTPUT_FOLDER%\output.001.bmp" --width !WIDTH! --height !HEIGHT!
    
    :: 生成index.txt文件
    echo.
    echo Step 4: Generating index.txt file...
    "%PYTHONEXE%" "%SHELL_FOLDER%\generate_index.py" --input "%TAR_FILE%" --output "%OUTPUT_FOLDER%\index.txt"
)

if errorlevel 1 (
    echo Error: Failed to convert TAR to BMP.
    pause
    goto End
)

echo.
echo Step 6: Cleaning up temporary files...
rd /s /q "%TEMP_FOLDER%"
rd /s /q "%SOURCE_FOLDER%"
mkdir "%SOURCE_FOLDER%"

echo.
echo ========================================
echo           Conversion completed!
echo ========================================
echo Resolution: %RESOLUTION% (!WIDTH!x!HEIGHT!)
echo Output folder: %OUTPUT_FOLDER%
echo.
echo Files have been converted successfully.
echo Check the output folder for your BMP files.
echo.

goto End

:Exit
echo.
echo Quitting...
goto End

:End
echo.
echo Press any key to exit...
pause >nul
endlocal 