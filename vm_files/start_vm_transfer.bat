@echo off
echo ========================================
echo    ��������Զ����������ű�
echo ========================================
echo.

:: ����Python·��
set "PYTHONEXE=C:\Program Files\Python36\python.exe"

:: ���Python�Ƿ����
"%PYTHONEXE%" --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python or update the PYTHONEXE path.
    echo Current path: %PYTHONEXE%
    pause
    goto End
)

echo ����������������Զ����Žű�...
echo.
echo ��ȷ����
echo 1. �Ѿ�������convert.bat�����������ļ�
echo 2. ���������Ѿ�������host_screenshot.py
echo 3. ����������ڵڶ���Ļ�Ͽɼ�
echo.

:: ����������˽ű�
"%PYTHONEXE%" vm_player.py

:End
echo.
echo ��������˳�...
pause >nul 