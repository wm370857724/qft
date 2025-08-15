@echo off
setlocal
cls

set "PYTHONEXE=C:\Program Files\Python36\python.exe"
set "SEVENZIP=C:\Program Files\7-Zip\7z.exe"
::Set default type value
set "choice=1"

echo Please select an option according to the external screen resolution.
echo 1. 1080P(Default)
echo 2. 4K
echo 3. Quit

set /p choice="Please type your choice(1-3):"
if "%choice%"=="1" (
	set /a THRESHOLD=1900*950/4
	set "SURFFIX="
)
if "%choice%"=="2" (
	set /a THRESHOLD=2540*1470/4 
	set "SURFFIX=_4K"
)
if "%choice%"=="3" goto Exit

set "SOURCE_FOLDER=%cd%\input"
set "SHELL_FOLDER=%cd%\shell"
set "OUTPUT_FOLDER=%cd%\output"
set "TEMP_FOLDER=%cd%\temp"
set "SEVENZ_FILE=%TEMP_FOLDER%\files_compressed.7z"
set "TAR_FILE=%TEMP_FOLDER%\example.tar"
rd /s /q "%TEMP_FOLDER%"
rd /s /q "%OUTPUT_FOLDER%"
if not exist "%TEMP_FOLDER%" mkdir "%TEMP_FOLDER%"
if not exist "%OUTPUT_FOLDER%" mkdir "%OUTPUT_FOLDER%"
::compress file to 7z
"%SEVENZIP%" a -r -t7z -mx9 -m0=LZMA2:d=27:mt=4:fb=64 "%SEVENZ_FILE%" "%SOURCE_FOLDER%"

for %%F in ("%SEVENZ_FILE%") do set "FILE_SIZE=%%~zF"
::compare file size
if %FILE_SIZE% GTR %THRESHOLD% (
	echo FILE_SIZE OVER THRESHOLD
	"%SEVENZIP%" a -ttar -v%THRESHOLD% "%TAR_FILE%" "%SEVENZ_FILE%"
	"%PYTHONEXE%" "%SHELL_FOLDER%\multi_tars_to_bmps%SURFFIX%.py"
) else (
	"%SEVENZIP%" a -ttar "%TAR_FILE%" "%SEVENZ_FILE%"
	"%PYTHONEXE%" "%SHELL_FOLDER%\single_tar_to_bmp%SURFFIX%.py"
)

rd /s /q "%TEMP_FOLDER%"
rd /s /q "%SOURCE_FOLDER%"
mkdir "%SOURCE_FOLDER%"
rem rd /s /q "%OUTPUT_FOLDER%"
echo completed.
goto End

:Exit
echo quit
goto End

:End
pause
setlocal