#!/usr/bin/env python3
"""
Build Release Packages - Creates ready-to-download ZIP files for GitHub releases
Includes pre-built executables for Windows users
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
import platform
import json
from datetime import datetime

class ReleaseBuilder:
    """Builds release packages with executables for direct download"""
    
    def __init__(self):
        self.app_name = "UniversalDocumentConverter"
        self.version = "2.1.0"
        self.release_dir = Path("releases")
        self.release_dir.mkdir(exist_ok=True)
        
    def build_windows_exe(self):
        """Build Windows executable with all features"""
        print("🔨 Building Windows executable with all features...")
        
        # Check if PyInstaller is available
        try:
            import PyInstaller
        except ImportError:
            print("❌ PyInstaller not found. Installing...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        
        # Create build directory
        build_dir = Path("build_exe")
        build_dir.mkdir(exist_ok=True)
        
        # Create PyInstaller spec file with all features
        spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# All required data files
added_files = [
    ('icon.ico', '.'),
    ('requirements.txt', '.'),
    ('config_ultimate.json', '.'),
    ('README.md', '.'),
    ('LICENSE', '.'),
    ('ocr_engine/*.py', 'ocr_engine'),
]

# All hidden imports for complete functionality
hidden_imports = [
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.ttk',
    'tkinterdnd2',
    'flask',
    'flask_cors',
    'waitress',
    'pytesseract',
    'PIL',
    'PIL.Image',
    'cv2',
    'numpy',
    'docx',
    'PyPDF2',
    'bs4',
    'striprtf',
    'striprtf.striprtf',
    'ebooklib',
    'psutil',
    'concurrent.futures',
    'threading',
    'json',
    'pathlib',
    'logging',
    'datetime',
    'webbrowser',
]

a = Analysis(
    ['universal_document_converter_ultimate.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
"""
        
        spec_path = build_dir / f"{self.app_name}.spec"
        spec_path.write_text(spec_content)
        
        # Build the executable
        print("📦 Running PyInstaller...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'PyInstaller',
                '--clean',
                '--onefile',
                '--windowed',
                '--name', self.app_name,
                str(spec_path)
            ])
            
            # Find the built executable
            exe_path = Path('dist') / f"{self.app_name}.exe"
            if exe_path.exists():
                print(f"✅ Executable built successfully: {exe_path}")
                return exe_path
            else:
                print("❌ Executable not found after build")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            return None
    
    def create_windows_release_zip(self):
        """Create Windows release ZIP with executable"""
        print("\n📦 Creating Windows Release ZIP...")
        
        # Build the executable first
        exe_path = self.build_windows_exe()
        if not exe_path:
            print("❌ Failed to build executable")
            return None
        
        # Create release package directory
        package_name = f"{self.app_name}_Windows_{self.version}_Installer"
        package_dir = self.release_dir / package_name
        
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # Copy executable
        shutil.copy2(exe_path, package_dir / f"{self.app_name}.exe")
        
        # Create README for the release
        readme_content = f"""# {self.app_name} v{self.version} - Windows Edition

## 🚀 Quick Start

1. **Run the Application:**
   - Double-click `{self.app_name}.exe`
   - Windows may show a security warning - click "More info" → "Run anyway"
   - The application will start immediately

## ✨ Features Included

This executable includes ALL features:

✅ **Document Conversion**
   - Convert between DOCX, PDF, TXT, HTML, RTF, EPUB
   - Batch processing support
   - Preserve formatting

✅ **OCR Capabilities**
   - Extract text from images (JPG, PNG, TIFF, BMP, GIF, WebP)
   - PDF OCR support
   - Multi-language recognition

✅ **Advanced Features**
   - Drag & Drop files directly onto the window
   - REST API server for remote processing
   - Multi-threading (1-32 threads)
   - Statistics tracking and export
   - Configuration persistence

✅ **Professional GUI**
   - Modern tabbed interface
   - Real-time progress tracking
   - Advanced settings panel
   - API server control
   - Theme support

## 📋 System Requirements

- **OS**: Windows 10 or Windows 11 (64-bit)
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 200 MB free space
- **Tesseract OCR**: Will prompt to install if not found (for OCR features)

## 🔧 First Time Setup

1. **Run the executable**
2. **If OCR is needed**, the app will guide you to install Tesseract
3. **All other features** work immediately

## 💡 Tips

- **Drag & Drop**: Drag files directly onto the main window
- **API Server**: Enable in the API tab for REST endpoints
- **Batch Processing**: Add multiple files or entire folders
- **Thread Selection**: Adjust threads based on your CPU cores

## 🆘 Troubleshooting

**Windows Security Warning:**
- This is normal for unsigned executables
- Click "More info" → "Run anyway"

**OCR Not Working:**
- Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Restart the application

**Application Won't Start:**
- Right-click → Properties → Unblock
- Run as Administrator if needed

## 📝 Version Information

- Version: {self.version}
- Build Date: {datetime.now().strftime('%Y-%m-%d')}
- All Features Included: Yes
- Portable: Yes (no installation required)

---
Designed and built by Beau Lewis
"""
        
        (package_dir / "README.txt").write_text(readme_content)
        
        # Create a quick start guide
        quickstart_content = f"""QUICK START - {self.app_name}
==================================

1. Double-click {self.app_name}.exe

2. If Windows shows a security warning:
   - Click "More info"
   - Click "Run anyway"

3. The application starts immediately!

That's it! All features are included.
"""
        
        (package_dir / "QUICK_START.txt").write_text(quickstart_content)
        
        # Create the ZIP file
        zip_filename = f"{package_name}.zip"
        zip_path = self.release_dir / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in package_dir.iterdir():
                zipf.write(file, file.name)
        
        # Clean up
        shutil.rmtree(package_dir)
        
        # Get file size
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        
        print(f"✅ Windows release ZIP created: {zip_path}")
        print(f"📦 Size: {size_mb:.1f} MB")
        
        return zip_path
    
    def create_source_release_zip(self):
        """Create source code ZIP for other platforms"""
        print("\n📦 Creating Source Code Release ZIP...")
        
        package_name = f"{self.app_name}_Source_{self.version}"
        package_dir = self.release_dir / package_name
        
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # Files to include in source release
        source_files = [
            "universal_document_converter_ultimate.py",
            "universal_document_converter.py",
            "requirements.txt",
            "README.md",
            "LICENSE",
            "INSTALLATION_GUIDE.md",
            "run_converter.sh",
            "run_converter.bat",
            "setup_shortcuts.py",
        ]
        
        # Create subdirectories
        (package_dir / "ocr_engine").mkdir()
        
        # Copy source files
        for file in source_files:
            if Path(file).exists():
                shutil.copy2(file, package_dir)
        
        # Copy OCR engine files
        ocr_files = Path("ocr_engine").glob("*.py")
        for file in ocr_files:
            shutil.copy2(file, package_dir / "ocr_engine")
        
        # Create platform-specific launchers
        self._create_platform_launchers(package_dir)
        
        # Create README
        readme_content = f"""# {self.app_name} v{self.version} - Source Code Package

## Installation by Platform

### Windows:
1. Install Python 3.8+ from python.org
2. Double-click `INSTALL_AND_RUN_WINDOWS.bat`

### macOS:
1. Install Python 3.8+ (usually pre-installed)
2. Run: `chmod +x INSTALL_AND_RUN_MACOS.sh && ./INSTALL_AND_RUN_MACOS.sh`

### Linux:
1. Install Python 3.8+ (usually pre-installed)
2. Run: `chmod +x INSTALL_AND_RUN_LINUX.sh && ./INSTALL_AND_RUN_LINUX.sh`

## Manual Installation (All Platforms):
```bash
pip install -r requirements.txt
python universal_document_converter_ultimate.py
```

## Features:
- All features included (API, OCR, Drag & Drop)
- Auto-installs dependencies
- Cross-platform compatible
"""
        
        (package_dir / "README_SOURCE.txt").write_text(readme_content)
        
        # Create ZIP
        zip_filename = f"{package_name}.zip"
        zip_path = self.release_dir / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(package_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(package_dir.parent)
                    zipf.write(file_path, arc_path)
        
        # Clean up
        shutil.rmtree(package_dir)
        
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"✅ Source release ZIP created: {zip_path}")
        print(f"📦 Size: {size_mb:.1f} MB")
        
        return zip_path
    
    def _create_platform_launchers(self, package_dir):
        """Create platform-specific launcher scripts"""
        
        # Windows launcher
        windows_launcher = """@echo off
echo Installing Universal Document Converter...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please make sure Python and pip are installed
    pause
    exit /b 1
)

echo.
echo Starting Universal Document Converter...
python universal_document_converter_ultimate.py
pause
"""
        (package_dir / "INSTALL_AND_RUN_WINDOWS.bat").write_text(windows_launcher)
        
        # macOS/Linux launcher
        unix_launcher = """#!/bin/bash
echo "Installing Universal Document Converter..."
echo ""

pip3 install -r requirements.txt || pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies"
    echo "Please make sure Python and pip are installed"
    exit 1
fi

echo ""
echo "Starting Universal Document Converter..."
python3 universal_document_converter_ultimate.py || python universal_document_converter_ultimate.py
"""
        
        macos_launcher = package_dir / "INSTALL_AND_RUN_MACOS.sh"
        macos_launcher.write_text(unix_launcher)
        macos_launcher.chmod(0o755)
        
        linux_launcher = package_dir / "INSTALL_AND_RUN_LINUX.sh"
        linux_launcher.write_text(unix_launcher)
        linux_launcher.chmod(0o755)
    
    def create_release_info(self, packages):
        """Create release information file"""
        release_info = {
            "version": self.version,
            "date": datetime.now().isoformat(),
            "packages": []
        }
        
        for package in packages:
            if package and package.exists():
                release_info["packages"].append({
                    "name": package.name,
                    "size_mb": round(package.stat().st_size / (1024 * 1024), 1),
                    "path": str(package)
                })
        
        info_path = self.release_dir / "release_info.json"
        with open(info_path, 'w') as f:
            json.dump(release_info, f, indent=2)
        
        return release_info


def main():
    """Build all release packages"""
    print("🚀 Universal Document Converter - Release Builder")
    print("=" * 60)
    
    builder = ReleaseBuilder()
    packages = []
    
    # Build Windows executable ZIP
    if platform.system() == "Windows" or True:  # Allow building on any platform for testing
        windows_zip = builder.create_windows_release_zip()
        if windows_zip:
            packages.append(windows_zip)
    
    # Build source code ZIP
    source_zip = builder.create_source_release_zip()
    if source_zip:
        packages.append(source_zip)
    
    # Create release info
    release_info = builder.create_release_info(packages)
    
    print("\n" + "=" * 60)
    print("✅ RELEASE PACKAGES CREATED!")
    print("=" * 60)
    
    print("\n📦 Ready for GitHub Release:")
    for pkg_info in release_info["packages"]:
        print(f"  • {pkg_info['name']} ({pkg_info['size_mb']} MB)")
    
    print("\n📋 Upload these files to GitHub Releases:")
    print("1. Go to your repository on GitHub")
    print("2. Click 'Releases' → 'Create a new release'")
    print("3. Upload the ZIP files from the 'releases' folder")
    print("4. Users can download directly without cloning!")
    
    print("\n✨ Windows users just:")
    print("1. Download the Windows ZIP")
    print("2. Extract it")
    print("3. Double-click the .exe")
    print("4. Everything works immediately!")


if __name__ == "__main__":
    main()