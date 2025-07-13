@echo off
title Quick Document Convertor
echo.
echo 🚀 Quick Document Convertor
echo ==============================
echo.
echo Starting application...
echo.

cd /d "%~dp0"

python run_app.py

if errorlevel 1 (
    echo.
    echo ❌ Error occurred. Press any key to exit...
    pause >nul
) else (
    echo.
    echo ✅ Application closed successfully.
) 