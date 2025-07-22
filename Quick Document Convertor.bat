@echo off
REM Quick Document Convertor Launcher
REM This batch file launches the Quick Document Convertor application

title Quick Document Convertor

REM Get the directory where this batch file is located
set "APP_DIR=%~dp0"

REM Change to the application directory
cd /d "%APP_DIR%"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if the main application file exists
if not exist "universal_document_converter_ocr.py" (
    echo ERROR: Application file not found
    echo Make sure you're running this from the correct directory
    pause
    exit /b 1
)

REM Launch the application
echo Starting OCR Document Converter...
python universal_document_converter_ocr.py

REM If we get here, the application has closed
if errorlevel 1 (
    echo.
    echo Application encountered an error
    pause
)
