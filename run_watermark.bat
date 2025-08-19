@echo off
echo Bulk Image Watermark Script
echo ===========================
echo.

if "%1"=="" (
    echo Usage: run_watermark.bat "input_folder" "output_folder" "watermark.png"
    echo.
    echo Example: run_watermark.bat "C:\Photos" "C:\Watermarked" "C:\logo.png"
    echo.
    echo This will run the watermark script with numbering enabled.
    echo.
    pause
    exit /b 1
)

if "%2"=="" (
    echo Error: Missing output folder parameter
    echo Usage: run_watermark.bat "input_folder" "output_folder" "watermark.png"
    pause
    exit /b 1
)

if "%3"=="" (
    echo Error: Missing watermark file parameter
    echo Usage: run_watermark.bat "input_folder" "output_folder" "watermark.png"
    pause
    exit /b 1
)

echo Input folder: %1
echo Output folder: %2
echo Watermark file: %3
echo.
echo Starting watermark process...
echo.

py watermark_script.py --input-folder "%1" --output-folder "%2" --png-watermark "%3" --enable-numbering

echo.
echo Process completed!
pause
