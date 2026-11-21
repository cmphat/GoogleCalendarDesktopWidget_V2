@echo off
chcp 65001 >nul
title Cai dat Google Calendar Hotkey

echo =======================================================
echo    CAI DAT GOOGLE CALENDAR HOTKEY VA TU KHOI DONG
echo =======================================================
echo.

cd /d "%~dp0"

REM 1. Kiem tra Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [LOI] May tinh chua cai dat Python hoac chua them Python vao PATH!
    echo Vui long tai va cai dat Python tu https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM 2. Tao icon neu chua co
if not exist "calendar.ico" (
    echo [*] Dang tao icon cho ung dung...
    python generate_icon.py
)

REM 3. Thiet lap khoi dong cung Windows
echo [*] Dang thiet lap tu dong khoi dong cung Windows...
python setup_autostart.py install

REM 4. Khoi chay ung dung chay ngam
echo.
echo [*] Dang khoi chay ung dung...
start "" pythonw "%~dp0google_calendar_toggle.pyw"

echo.
echo =======================================================
echo   DA CAI DAT VA KHOI CHAY THANH CONG!
echo.
echo   - Phim tat: Ctrl + Alt + C
echo   - An lan 1: Hien Google Calendar
echo   - An lan 2: An Google Calendar
echo   - Tu dong mo khi bat may: DA BAT
echo.
echo   Icon lich mau xanh da xuat hien o goc duoi ben phai
echo   (khay he thong / System Tray canh dong ho).
echo =======================================================
echo.
pause
