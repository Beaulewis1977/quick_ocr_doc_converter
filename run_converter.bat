@echo off
setlocal enabledelayedexpansion

:: Universal Document Converter - Windows Batch Runner
:: Version 2.1.0 - Complete Edition with OCR and Markdown Support

echo.
echo ===============================================
echo Universal Document Converter v2.1.0
echo Complete Edition with OCR and Markdown Support
echo ===============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    echo.
    pause
    exit /b 1
)

:: Check if the converter script exists
if not exist "universal_document_converter_ocr.py" (
    echo ERROR: universal_document_converter_ocr.py not found!
    echo Please ensure you're running this from the correct directory.
    echo.
    pause
    exit /b 1
)

:: Install dependencies if needed
echo Checking dependencies...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    python -m pip install -r requirements.txt
)

:: Run the Universal Document Converter with OCR support
echo Starting Universal Document Converter...
echo.
python universal_document_converter_ocr.py %*

if errorlevel 1 (
    echo.
    echo ERROR: The converter encountered an error.
    echo Please check the error message above.
    pause
)

endlocal