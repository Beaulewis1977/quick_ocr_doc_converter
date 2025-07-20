@echo off
title Universal Document Converter Ultimate
echo ============================================
echo Universal Document Converter Ultimate
echo The Complete Document Conversion Solution
echo ============================================
echo.
echo Starting application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from python.org
    pause
    exit /b 1
)

REM Launch the ultimate version
python universal_document_converter_ultimate.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch the application
    echo Please check the error message above
    pause
)