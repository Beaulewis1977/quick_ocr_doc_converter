@echo off
title OCR Document Converter v3.1.0
cd /d "%~dp0"
echo.
echo ====================================================
echo    OCR Document Converter v3.1.0
echo    Enhanced by Terragon Labs
echo ====================================================
echo.
echo Starting application...
python launch_ocr.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to start application.
    echo Make sure Python is installed and requirements are met.
    pause
)
echo.
echo Application closed.
pause