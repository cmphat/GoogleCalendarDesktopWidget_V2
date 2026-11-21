@echo off
chcp 65001 >nul
title Dang nhap Google Calendar

echo =======================================================
echo         DANG NHAP TAI KHOAN GOOGLE CALENDAR
echo =======================================================
echo.
echo Ly do bi chuyen huong:
echo Khi chua dang nhap, Google se khong cho mo o che do App doc lap.
echo.
echo Chon trinh duyet ban muon dung de dang nhap:
echo   [1] Google Chrome (Khuyen dung)
echo   [2] Microsoft Edge
echo.
set /p choice="Nhap lua chon (1 hoac 2, mac dinh 1): "

if "%choice%"=="2" (
    echo [*] Dang mo Microsoft Edge de ban dang nhap...
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "https://accounts.google.com/ServiceLogin?service=cl&continue=https://calendar.google.com"
) else (
    echo [*] Dang mo Google Chrome de ban dang nhap...
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" "https://accounts.google.com/ServiceLogin?service=cl&continue=https://calendar.google.com"
)

echo.
echo =======================================================
echo   HUONG DAN TIEP THEO:
echo   1. Dang nhap tai khoan Google cua ban tren cua so vua mo.
echo   2. Khi nao vao duoc Lịch (Calendar) roi thi dong cua so do lai.
echo   3. An to hop phim Ctrl + Alt + C la ung dung se chay mươt ma!
echo =======================================================
echo.
pause
