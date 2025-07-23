@echo off
title OCR Document Converter
color 0A

:: Check for Python installation
where python3 >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ###########################################################
    echo # PYTHON NOT FOUND IN SYSTEM PATH                         #
    echo ###########################################################
    echo.
    echo Please install Python 3.8+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Verify main script exists
if not exist "universal_document_converter.py" (
    echo.
    echo ###########################################################
    echo # APPLICATION FILES MISSING                               #
    echo ###########################################################
    echo.
    echo Required files not found! Please:
    echo 1. Download the full application package
    echo 2. Extract all files to a folder
    echo 3. Run this batch file from that folder
    echo.
    pause
    exit /b 1
)

:: Run the application
echo.
echo ###########################################################
echo # STARTING UNIVERSAL DOCUMENT CONVERTER v3.1.0            #
echo ###########################################################
echo.
python3 -X utf8 universal_document_converter.py %*

:: Pause if launched by double-click
if "%1" == "" pause