@echo off
echo ========================================
echo Quick Document Convertor - Windows Installer Setup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking version...
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"

REM Install required dependencies
echo.
echo Installing required dependencies...
echo This may take a few minutes...
python -m pip install --upgrade pip
python -m pip install -r requirements_installer.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!

REM Create the installer
echo.
echo Creating Windows installer...
python create_windows_installer.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create installer
    pause
    exit /b 1
)

echo.
echo ========================================
echo Windows installer created successfully!
echo ========================================
echo.
echo You can now find the installer files in the dist_installer folder.
echo.
echo To install the application:
echo 1. Run the installer as Administrator
echo 2. Follow the installation wizard
echo 3. The app will be added to Start Menu and Desktop
echo 4. System tray will auto-start with Windows
echo 5. Right-click taskbar shortcuts to pin to taskbar
echo.
pause 