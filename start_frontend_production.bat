@echo off
setlocal enabledelayedexpansion

echo ========================================
echo K1 Watermark Frontend Server - Production
echo ========================================
echo.

REM Get LAN IP address (more reliable method)
set "ip="
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "temp=%%a"
    set "temp=!temp:~1!"
    REM Skip 127.0.0.1 (localhost)
    echo !temp! | findstr /r "^192\. ^10\. ^172\." >nul
    if !errorlevel! equ 0 (
        set "ip=!temp!"
        goto :found_ip
    )
)

REM If no LAN IP found, try alternative method
if "!ip!"=="" (
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
        set "temp=%%a"
        set "temp=!temp:~1!"
        if not "!temp!"=="127.0.0.1" (
            set "ip=!temp!"
            goto :found_ip
        )
    )
)

:found_ip
if "!ip!"=="" set "ip=127.0.0.1"

echo Detected IP address: !ip!
echo.

REM Start the production server
echo Starting production server...
echo.
start "K1 Watermark Production Server" py server_production.py

REM Wait a moment for server to start
timeout /t 3 /nobreak >nul

REM Open browser with LAN URL
echo Opening browser at http://!ip!:5000
start http://!ip!:5000

echo.
echo ========================================
echo Server is running in production mode
echo ========================================
echo Local URL:   http://localhost:5000
echo Network URL: http://!ip!:5000
echo.
echo The server window is running separately.
echo Close the "K1 Watermark Production Server" window to stop the server.
echo ========================================
echo.
pause

