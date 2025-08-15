@echo off
setlocal

set "SEVENZIP=C:\Program Files\7-Zip\7z.exe"
echo 1
set "SOURCE_FOLDER=H:\sijinzhi\tar\example"
echo 2
set "OUTPUT_FILE=H:\sijinzhi\tar\example.7z"
set "TAR_FILE=H:\sijinzhi\tar\example.tar"
echo 3
rem "%SEVENZIP%" a -r -t7z -solid -mx9 -ms=on -m0=LZMA2:d=27:fb=64:s=16g:mt=4 "%OUTPUT_FILE%" "%SOURCE_FOLDER%"
"%SEVENZIP%" a -r -t7z -mx9 -m0=LZMA2:d=27:mt=4:fb=64 "%OUTPUT_FILE%" "%SOURCE_FOLDER%"
"%SEVENZIP%" a -ttar -v911K "%TAR_FILE%" "%OUTPUT_FILE%"
echo Compression completed.
pause