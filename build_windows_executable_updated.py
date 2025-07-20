#!/usr/bin/env python3
"""
Windows Executable Builder for Enhanced OCR Document Converter
Creates a standalone Windows executable with all dependencies
Updated with fixes for all compatibility issues
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

class WindowsBuilder:
    def __init__(self):
        self.app_name = "Enhanced OCR Document Converter"
        self.exe_name = "QuickDocumentConvertor"
        self.version = "3.0.0"
        self.root_dir = Path(__file__).parent
        self.build_dir = self.root_dir / "build"
        self.dist_dir = self.root_dir / "dist"
        
    def check_dependencies(self):
        """Check and install required dependencies"""
        print("🔍 Checking dependencies...")
        
        required_packages = [
            ('pyinstaller', '6.12.0'),
            ('pillow', '10.4.0'),
            ('numpy', '1.26.4'),  # Must be <2.0
            ('opencv-python', '4.8.1.78'),
            ('pytesseract', '0.3.13'),
            ('packaging', '25.0'),
            ('cryptography', '43.0.3'),
            ('pywin32', '306'),
        ]
        
        for package, version in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"✅ {package} is installed")
            except ImportError:
                print(f"📦 Installing {package}=={version}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    f"{package}=={version}"
                ])
                
    def create_version_info(self):
        """Create version info file for Windows"""
        version_info = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({self.version.replace('.', ', ')}, 0),
    prodvers=({self.version.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Terragon Labs'),
        StringStruct(u'FileDescription', u'{self.app_name}'),
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'{self.exe_name}'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2025 Beau Lewis'),
        StringStruct(u'OriginalFilename', u'{self.exe_name}.exe'),
        StringStruct(u'ProductName', u'{self.app_name}'),
        StringStruct(u'ProductVersion', u'{self.version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
        with open(self.root_dir / 'version_info.txt', 'w') as f:
            f.write(version_info)
            
    def create_runtime_hook(self):
        """Create runtime hook to set environment variables"""
        hook_content = '''
import os
import sys

# Set Tesseract path for Windows
if sys.platform == 'win32':
    tesseract_path = os.path.join(sys._MEIPASS, 'Tesseract-OCR', 'tesseract.exe')
    if os.path.exists(tesseract_path):
        os.environ['TESSERACT_CMD'] = tesseract_path
    else:
        # Try standard installation paths
        standard_paths = [
            r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
            r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe',
        ]
        for path in standard_paths:
            if os.path.exists(path):
                os.environ['TESSERACT_CMD'] = path
                break
                
    # Set tessdata path
    tessdata_path = os.path.join(os.path.dirname(os.environ.get('TESSERACT_CMD', '')), 'tessdata')
    if os.path.exists(tessdata_path):
        os.environ['TESSDATA_PREFIX'] = tessdata_path
'''
        
        hooks_dir = self.root_dir / 'hooks'
        hooks_dir.mkdir(exist_ok=True)
        
        with open(hooks_dir / 'runtime_hook.py', 'w') as f:
            f.write(hook_content)
            
    def build_executable(self):
        """Build the Windows executable"""
        print("🔨 Building executable...")
        
        # Clean previous builds
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
            
        # Create version info and runtime hook
        self.create_version_info()
        self.create_runtime_hook()
        
        # PyInstaller command with all options
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name", self.exe_name,
            "--onefile",
            "--windowed",
            "--icon", str(self.root_dir / "icon.ico"),
            "--version-file", str(self.root_dir / "version_info.txt"),
            "--runtime-hook", str(self.root_dir / "hooks" / "runtime_hook.py"),
            
            # Add all data files
            "--add-data", f"{self.root_dir / 'backends'};backends",
            "--add-data", f"{self.root_dir / 'security'};security",
            "--add-data", f"{self.root_dir / 'monitoring'};monitoring",
            "--add-data", f"{self.root_dir / 'ocr_engine'};ocr_engine",
            "--add-data", f"{self.root_dir / 'cross_platform'};cross_platform",
            "--add-data", f"{self.root_dir / 'icon.ico'};.",
            
            # Hidden imports
            "--hidden-import", "tkinter",
            "--hidden-import", "PIL",
            "--hidden-import", "cv2",
            "--hidden-import", "numpy",
            "--hidden-import", "pytesseract",
            "--hidden-import", "packaging.version",
            "--hidden-import", "cryptography.fernet",
            "--hidden-import", "win32com.client",
            "--hidden-import", "backends.manager",
            "--hidden-import", "security.validator",
            "--hidden-import", "security.credentials",
            "--hidden-import", "monitoring.cost_tracker",
            "--hidden-import", "ocr_engine.ocr_engine",
            
            # Exclude unnecessary modules
            "--exclude-module", "matplotlib",
            "--exclude-module", "scipy",
            "--exclude-module", "pandas",
            
            # Main script
            str(self.root_dir / "enhanced_ocr_gui.py")
        ]
        
        subprocess.check_call(cmd)
        
        print("✅ Executable built successfully!")
        
    def create_installer_package(self):
        """Create installer package with all necessary files"""
        print("📦 Creating installer package...")
        
        installer_dir = self.root_dir / "installer_package"
        installer_dir.mkdir(exist_ok=True)
        
        # Copy executable
        exe_path = self.dist_dir / f"{self.exe_name}.exe"
        if exe_path.exists():
            shutil.copy2(exe_path, installer_dir)
            
        # Create README for installer
        readme_content = f"""# {self.app_name} - Windows Installation

## Version {self.version}

### Prerequisites

1. **Tesseract OCR** (Required for local OCR)
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - During installation, note the installation path
   - Default: C:\\Program Files\\Tesseract-OCR

2. **Visual C++ Redistributables** (May be required)
   - Download from Microsoft if you encounter DLL errors

### Installation Steps

1. Install Tesseract OCR if not already installed
2. Run {self.exe_name}.exe
3. On first run, the app will automatically detect Tesseract

### API Key Configuration

The application supports multiple OCR backends:

1. **Free Local OCR** (Tesseract) - No API keys required
2. **Google Vision API** - Requires Google Cloud credentials
3. **AWS Textract** - Requires AWS access keys
4. **Azure Computer Vision** - Requires Azure subscription key

To configure API keys:
1. Launch the application
2. Go to Settings tab
3. Enter your API credentials
4. Click "Save Configuration"
5. Click "Test Backends" to verify

### Troubleshooting

If OCR is not working:
1. Ensure Tesseract is installed
2. Check that tessdata folder contains language files
3. Try running as Administrator
4. Check Windows Defender/Antivirus exceptions

### Support

For issues or questions, contact support@terragonlabs.com
"""
        
        with open(installer_dir / "README.txt", 'w') as f:
            f.write(readme_content)
            
        # Create batch file for easy launch
        batch_content = f"""@echo off
title {self.app_name}
echo Starting {self.app_name}...
start "" "%~dp0\\{self.exe_name}.exe"
exit
"""
        
        with open(installer_dir / f"Launch_{self.exe_name}.bat", 'w') as f:
            f.write(batch_content)
            
        # Create requirements file for reference
        shutil.copy2(self.root_dir / "requirements_windows.txt", installer_dir)
        
        print("✅ Installer package created!")
        
    def run(self):
        """Run the complete build process"""
        print(f"🚀 Building {self.app_name} v{self.version} for Windows")
        print("=" * 60)
        
        try:
            self.check_dependencies()
            self.build_executable()
            self.create_installer_package()
            
            print("\n" + "=" * 60)
            print("✅ BUILD SUCCESSFUL!")
            print(f"📁 Executable location: {self.dist_dir / f'{self.exe_name}.exe'}")
            print(f"📦 Installer package: {self.root_dir / 'installer_package'}")
            print("\n🎉 The Windows executable is ready for distribution!")
            
        except Exception as e:
            print(f"\n❌ Build failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    builder = WindowsBuilder()
    builder.run()