@echo off
title Quick Document Convertor - Force GUI
echo.
echo 🖥️ FORCING GUI TO APPEAR
echo ========================
echo.
echo If the window doesn't appear, check your taskbar!
echo.

cd /d "%~dp0"

python direct_launch.py

echo.
echo Press any key to exit...
pause >nul 