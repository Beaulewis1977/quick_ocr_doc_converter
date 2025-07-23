@echo off
title OCR Document Converter Installer
color 0A

echo.
echo ============================================================
echo     OCR Document Converter v3.1.0 - Installation
echo ============================================================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This installer requires Administrator privileges.
    echo Please right-click and select "Run as Administrator"
    pause
    exit /b 1
)

:: Check Python installation
echo Checking Python installation...
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

:: Run the setup script
echo.
echo Running OCR environment setup...
python3 setup_ocr_environment.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Setup failed. Please check the error messages above.
    pause
    exit /b 1
)

:: Create Start Menu shortcut
echo.
echo Creating Start Menu shortcut...
set "startMenuPath=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
mkdir "%startMenuPath%" >nul 2>&1

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%startMenuPath%\OCR Document Converter.lnk'); $Shortcut.TargetPath = '%CD%\run_ocr_converter.bat'; $Shortcut.IconLocation = '%CD%\icon.ico'; $Shortcut.Save()"

:: Create Desktop shortcut
echo Creating Desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\OCR Document Converter.lnk'); $Shortcut.TargetPath = '%CD%\run_ocr_converter.bat'; $Shortcut.IconLocation = '%CD%\icon.ico'; $Shortcut.Save()"

:: Success message
echo.
echo ============================================================
echo     Installation Complete!
echo ============================================================
echo.
echo OCR Document Converter has been installed successfully.
echo.
echo You can now:
echo   - Use the Desktop shortcut
echo   - Find it in the Start Menu
echo   - Run run_ocr_converter.bat directly
echo.
pause