@echo off
REM Enhanced OCR Document Converter - Windows Dependency Installer
REM This script installs all required Python packages with correct versions

echo ============================================================
echo Enhanced OCR Document Converter - Dependency Installer
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python is installed. Proceeding with package installation...
echo.

REM Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install critical dependencies with specific versions
echo.
echo Installing core dependencies with compatibility fixes...
echo.

REM CRITICAL: Install numpy FIRST with version constraint
echo Installing numpy (must be less than 2.0 for OpenCV compatibility)...
python -m pip install "numpy==1.26.4"

REM Install OpenCV with specific version
echo Installing OpenCV...
python -m pip install "opencv-python==4.8.1.78"

REM Install other core packages
echo Installing other core packages...
python -m pip install "pytesseract==0.3.13"
python -m pip install "packaging==25.0"
python -m pip install "Pillow==10.4.0"

REM Install document processing packages
echo Installing document processing packages...
python -m pip install "python-docx==1.2.0"
python -m pip install "beautifulsoup4==4.13.4"
python -m pip install "reportlab==4.4.2"
python -m pip install "markdown==3.8.2"
python -m pip install "lxml==6.0.0"

REM Install security and utility packages
echo Installing security and utility packages...
python -m pip install "cryptography==43.0.3"
python -m pip install "requests==2.32.4"
python -m pip install "psutil==6.2.0"

REM Install Windows-specific packages
echo Installing Windows-specific packages...
python -m pip install "pywin32==306"

REM Optional: Install development tools
echo.
echo Do you want to install development tools (PyInstaller, pytest)? (y/n)
set /p install_dev=
if /i "%install_dev%"=="y" (
    echo Installing development tools...
    python -m pip install "pyinstaller==6.12.0"
    python -m pip install "pytest==8.4.1"
    python -m pip install "pytest-cov==6.0.0"
)

echo.
echo ============================================================
echo Installation complete!
echo ============================================================
echo.
echo IMPORTANT NOTES:
echo 1. You still need to install Tesseract OCR separately
echo    Download from: https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 2. If you encounter any DLL errors, install Visual C++ Redistributables:
echo    https://aka.ms/vs/17/release/vc_redist.x64.exe
echo.
echo 3. To configure API keys, run the application and go to Settings tab
echo.
echo Press any key to exit...
pause >nul