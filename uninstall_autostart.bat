@echo off
chcp 65001 >nul
title Go bo Google Calendar Hotkey

echo =======================================================
echo         GO BO TU KHOI DONG GOOGLE CALENDAR HOTKEY
echo =======================================================
echo.

cd /d "%~dp0"

REM 1. Tat tien trinh dang chay
echo [*] Dang dung ung dung...
taskkill /f /im pythonw.exe >nul 2>nul

REM 2. Huy khoi dong
python setup_autostart.py uninstall

echo.
echo =======================================================
echo   DA TAT UNG DUNG VA HUY KHOI DONG CUNG WINDOWS!
echo =======================================================
echo.
pause
