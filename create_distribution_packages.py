#!/usr/bin/env python3
"""
Universal Document Converter - Multi-Platform Distribution Package Creator
Creates platform-specific ZIP packages for Windows, macOS, and Linux
"""

import os
import zipfile
import shutil
import stat
import platform
from pathlib import Path
from datetime import datetime

class DistributionPackageCreator:
    """Creates platform-specific distribution packages"""
    
    def __init__(self):
        self.app_name = "UniversalDocumentConverter"
        self.version = "2.0.0"
        self.dist_dir = Path("dist")
        self.dist_dir.mkdir(exist_ok=True)
        
        # Common files for all platforms
        self.common_files = [
            "universal_document_converter_ultimate.py",
            "universal_document_converter.py",
            "requirements.txt",
            "README.md",
            "LICENSE",
            "QUICK_START.md",
            "INSTALLATION_GUIDE.md",
            "TROUBLESHOOTING.md",
            "config_ultimate.json",
            "icon.ico",
            # Include all Python modules
            "ocr_engine/__init__.py",
            "ocr_engine/ocr_engine.py",
            "ocr_engine/ocr_integration.py",
            "ocr_engine/format_detector.py",
            "ocr_engine/image_processor.py",
            # Documentation
            "docs/CROSS_PLATFORM_GUIDE.md",
        ]
        
        # Platform-specific files
        self.windows_files = [
            "Launch_Ultimate.bat",
            "run_converter.bat",
            "run_converter.ps1",
            "setup_shortcuts.py",
            "create_desktop_shortcut.py",
            "install_converter.py",
            "setup_windows_installer.bat",
            "requirements_installer.txt",
        ]
        
        self.macos_files = [
            "run_converter.sh",
            "setup_shortcuts.py",
            "cross_platform/macos_integration.py",
        ]
        
        self.linux_files = [
            "run_converter.sh",
            "setup_shortcuts.py",
            "cross_platform/linux_integration.py",
        ]
    
    def create_windows_zip(self):
        """Create Windows-specific ZIP package"""
        print("\n📦 Creating Windows ZIP package...")
        
        package_name = f"{self.app_name}_Windows_{self.version}"
        package_dir = self.dist_dir / package_name
        
        # Clean and create directory
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # Create subdirectories
        (package_dir / "ocr_engine").mkdir()
        (package_dir / "docs").mkdir()
        (package_dir / "cross_platform").mkdir()
        
        # Copy files
        self._copy_files(self.common_files + self.windows_files, package_dir)
        
        # Create Windows-specific launcher
        launcher_content = f"""@echo off
echo ===============================================
echo {self.app_name} v{self.version} - Windows Edition
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check for virtual environment
if exist "venv\\Scripts\\activate.bat" (
    echo Activating virtual environment...
    call venv\\Scripts\\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\\Scripts\\activate.bat
    
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Launch the application
echo Starting {self.app_name}...
python universal_document_converter_ultimate.py

pause
"""
        
        launcher_path = package_dir / "START_HERE.bat"
        launcher_path.write_text(launcher_content)
        
        # Create README for Windows
        readme_content = f"""# {self.app_name} - Windows Edition

## Quick Start

1. **First Time Setup:**
   - Double-click `START_HERE.bat`
   - Wait for dependencies to install (first time only)
   - The application will start automatically

2. **Regular Use:**
   - Double-click `START_HERE.bat`
   - Or use `Launch_Ultimate.bat` after first setup

## Features Included:
✅ Full Document Conversion (DOCX, PDF, HTML, RTF, EPUB, TXT)
✅ OCR Support (requires Tesseract - will prompt to install)
✅ Drag & Drop Support
✅ API Server
✅ Multi-threading (1-32 threads)
✅ Statistics & Export

## Optional: Install Tesseract OCR
For OCR functionality, download and install from:
https://github.com/UB-Mannheim/tesseract/wiki

## Support
See TROUBLESHOOTING.md for common issues.
"""
        
        (package_dir / "README_WINDOWS.txt").write_text(readme_content)
        
        # Create ZIP
        zip_path = self.dist_dir / f"{package_name}.zip"
        self._create_zip(package_dir, zip_path)
        
        print(f"✅ Windows package created: {zip_path}")
        return zip_path
    
    def create_macos_zip(self):
        """Create macOS-specific ZIP package"""
        print("\n📦 Creating macOS ZIP package...")
        
        package_name = f"{self.app_name}_macOS_{self.version}"
        package_dir = self.dist_dir / package_name
        
        # Clean and create directory
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # Create subdirectories
        (package_dir / "ocr_engine").mkdir()
        (package_dir / "docs").mkdir()
        (package_dir / "cross_platform").mkdir()
        
        # Copy files
        self._copy_files(self.common_files + self.macos_files, package_dir)
        
        # Create macOS launcher script
        launcher_content = f"""#!/bin/bash
echo "==============================================="
echo "{self.app_name} v{self.version} - macOS Edition"
echo "==============================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8+ using:"
    echo "  brew install python@3.11"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check for virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check for Tesseract
if ! command -v tesseract &> /dev/null; then
    echo ""
    echo "WARNING: Tesseract OCR not found!"
    echo "For OCR support, install with: brew install tesseract"
    echo ""
fi

# Launch the application
echo "Starting {self.app_name}..."
python universal_document_converter_ultimate.py
"""
        
        launcher_path = package_dir / "START_HERE.command"
        launcher_path.write_text(launcher_content)
        # Make executable
        launcher_path.chmod(launcher_path.stat().st_mode | stat.S_IEXEC)
        
        # Create README for macOS
        readme_content = f"""# {self.app_name} - macOS Edition

## Quick Start

1. **First Time Setup:**
   - Double-click `START_HERE.command`
   - If prompted, allow Terminal to run
   - Wait for dependencies to install (first time only)
   - The application will start automatically

2. **Regular Use:**
   - Double-click `START_HERE.command`

## Prerequisites:
- Python 3.8+ (install with: brew install python@3.11)
- Tesseract OCR (install with: brew install tesseract)

## Features Included:
✅ Full Document Conversion (DOCX, PDF, HTML, RTF, EPUB, TXT)
✅ OCR Support (with Tesseract)
✅ Drag & Drop Support
✅ API Server
✅ Multi-threading (1-32 threads)
✅ Statistics & Export

## Terminal Permission
If macOS blocks the script:
1. Go to System Preferences → Security & Privacy
2. Click "Open Anyway" for START_HERE.command
3. Or run in Terminal: chmod +x START_HERE.command

## Support
See TROUBLESHOOTING.md for common issues.
"""
        
        (package_dir / "README_MACOS.txt").write_text(readme_content)
        
        # Create ZIP
        zip_path = self.dist_dir / f"{package_name}.zip"
        self._create_zip(package_dir, zip_path)
        
        print(f"✅ macOS package created: {zip_path}")
        return zip_path
    
    def create_linux_zip(self):
        """Create Linux-specific ZIP package"""
        print("\n📦 Creating Linux ZIP package...")
        
        package_name = f"{self.app_name}_Linux_{self.version}"
        package_dir = self.dist_dir / package_name
        
        # Clean and create directory
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # Create subdirectories
        (package_dir / "ocr_engine").mkdir()
        (package_dir / "docs").mkdir()
        (package_dir / "cross_platform").mkdir()
        
        # Copy files
        self._copy_files(self.common_files + self.linux_files, package_dir)
        
        # Create Linux launcher script
        launcher_content = f"""#!/bin/bash
echo "==============================================="
echo "{self.app_name} v{self.version} - Linux Edition"
echo "==============================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8+ using:"
    echo "  sudo apt install python3 python3-pip python3-venv"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check for virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check for Tesseract
if ! command -v tesseract &> /dev/null; then
    echo ""
    echo "WARNING: Tesseract OCR not found!"
    echo "For OCR support, install with: sudo apt install tesseract-ocr"
    echo ""
fi

# Check for tkinter
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: tkinter not found!"
    echo "Please install with: sudo apt install python3-tk"
    echo ""
fi

# Launch the application
echo "Starting {self.app_name}..."
python3 universal_document_converter_ultimate.py
"""
        
        launcher_path = package_dir / "START_HERE.sh"
        launcher_path.write_text(launcher_content)
        # Make executable
        launcher_path.chmod(launcher_path.stat().st_mode | stat.S_IEXEC)
        
        # Create README for Linux
        readme_content = f"""# {self.app_name} - Linux Edition

## Quick Start

1. **First Time Setup:**
   - Open Terminal in this directory
   - Run: ./START_HERE.sh
   - Or double-click START_HERE.sh (if file manager supports it)
   - Wait for dependencies to install (first time only)

2. **Regular Use:**
   - Run: ./START_HERE.sh
   - Or double-click if your file manager supports it

## Prerequisites:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk tesseract-ocr
```

## Features Included:
✅ Full Document Conversion (DOCX, PDF, HTML, RTF, EPUB, TXT)
✅ OCR Support (with Tesseract)
✅ Drag & Drop Support
✅ API Server
✅ Multi-threading (1-32 threads)
✅ Statistics & Export

## Desktop Integration:
Run setup_shortcuts.py to create desktop shortcuts and menu entries.

## Support
See TROUBLESHOOTING.md for common issues.
"""
        
        (package_dir / "README_LINUX.txt").write_text(readme_content)
        
        # Create .desktop file for Linux desktop integration
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={self.app_name}
Comment=Convert documents between multiple formats
Exec=bash -c 'cd "$(dirname "%k")" && ./START_HERE.sh'
Icon=document-converter
Terminal=true
Categories=Office;Utility;
"""
        (package_dir / f"{self.app_name}.desktop").write_text(desktop_content)
        
        # Create ZIP
        zip_path = self.dist_dir / f"{package_name}.zip"
        self._create_zip(package_dir, zip_path)
        
        print(f"✅ Linux package created: {zip_path}")
        return zip_path
    
    def create_all_packages(self):
        """Create packages for all platforms"""
        print(f"🚀 Creating distribution packages for {self.app_name} v{self.version}")
        print("=" * 60)
        
        packages = []
        
        # Create platform packages
        packages.append(self.create_windows_zip())
        packages.append(self.create_macos_zip())
        packages.append(self.create_linux_zip())
        
        # Create a universal source package
        print("\n📦 Creating Universal Source package...")
        universal_name = f"{self.app_name}_Source_{self.version}"
        universal_dir = self.dist_dir / universal_name
        
        if universal_dir.exists():
            shutil.rmtree(universal_dir)
        universal_dir.mkdir()
        
        # Copy everything for source package
        all_files = self.common_files + self.windows_files + self.macos_files + self.linux_files
        
        # Create necessary subdirectories
        (universal_dir / "ocr_engine").mkdir(exist_ok=True)
        (universal_dir / "docs").mkdir(exist_ok=True)
        (universal_dir / "cross_platform").mkdir(exist_ok=True)
        
        self._copy_files(list(set(all_files)), universal_dir)
        
        # Create universal README
        readme_content = f"""# {self.app_name} - Universal Source Package

This package contains the source code for all platforms.

## Platform-Specific Instructions:

### Windows:
- Run: START_HERE.bat or Launch_Ultimate.bat

### macOS:
- Run: ./START_HERE.command

### Linux:
- Run: ./START_HERE.sh

## Manual Installation:
1. Install Python 3.8+
2. Install dependencies: pip install -r requirements.txt
3. Run: python universal_document_converter_ultimate.py

See platform-specific README files for detailed instructions.
"""
        (universal_dir / "README_UNIVERSAL.txt").write_text(readme_content)
        
        universal_zip = self.dist_dir / f"{universal_name}.zip"
        self._create_zip(universal_dir, universal_zip)
        packages.append(universal_zip)
        
        print(f"✅ Universal source package created: {universal_zip}")
        
        return packages
    
    def _copy_files(self, files, destination):
        """Copy files to destination, creating directories as needed"""
        for file_path in files:
            src = Path(file_path)
            if src.exists():
                dst = destination / file_path
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.is_file():
                    shutil.copy2(src, dst)
                    print(f"  ✓ {file_path}")
            else:
                print(f"  ⚠ Missing: {file_path}")
    
    def _create_zip(self, source_dir, zip_path):
        """Create a ZIP file from a directory"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(source_dir.parent)
                    zipf.write(file_path, arc_path)
        
        # Get size in MB
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"  📦 Size: {size_mb:.1f} MB")


def main():
    """Create all distribution packages"""
    creator = DistributionPackageCreator()
    
    print("🎯 Universal Document Converter - Distribution Package Creator")
    print("=" * 60)
    print("This will create platform-specific ZIP packages for:")
    print("  • Windows (with .bat launchers)")
    print("  • macOS (with .command launchers)")
    print("  • Linux (with .sh launchers)")
    print("  • Universal Source (all platforms)")
    print("=" * 60)
    
    packages = creator.create_all_packages()
    
    print("\n" + "=" * 60)
    print("✅ ALL PACKAGES CREATED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📦 Distribution packages ready:")
    for package in packages:
        print(f"  • {package.name}")
    
    print("\n📋 Each package includes:")
    print("  ✅ All source code")
    print("  ✅ Platform-specific launchers")
    print("  ✅ Automatic dependency installation")
    print("  ✅ All features (API, OCR, Drag & Drop)")
    print("  ✅ Documentation")
    
    print("\n🚀 Ready for distribution!")


if __name__ == "__main__":
    main()