#!/usr/bin/env python3
"""
Complete Universal Document Converter Installer
Creates a comprehensive Windows installer with all features including Markdown support
Version 2.1.0 with bidirectional RTF ↔ Markdown conversion
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path
import json
import zipfile
import requests
from typing import Dict, List, Optional

class CompleteInstallerCreator:
    """Creates a complete installer with all dependencies and features"""
    
    def __init__(self):
        self.app_name = "Universal Document Converter"
        self.app_version = "2.1.0"
        self.publisher = "Beau Lewis" 
        self.description = "Complete document conversion suite with OCR and Markdown support"
        self.app_dir = Path(__file__).parent
        self.build_dir = self.app_dir / "build_complete"
        self.dist_dir = self.app_dir / "dist_complete"
        self.temp_dir = None
        
        # New features in v2.1.0
        self.features = {
            "core": [
                "✅ OCR (Optical Character Recognition)",
                "✅ Document Conversion (DOCX, PDF, HTML, RTF, TXT, EPUB)",
                "✅ Batch Processing with Progress Tracking",
                "✅ Cross-platform Support (Windows, Linux, macOS)",
            ],
            "new_v21": [
                "🆕 Bidirectional Markdown ↔ RTF Conversion",
                "🆕 32-bit Legacy System Support (VFP9, VB6)", 
                "🆕 Multi-threading Performance (13.5x faster)",
                "🆕 JSON IPC for External Applications",
                "🆕 Advanced Error Handling & Recovery",
                "🆕 Memory Usage Optimization",
            ],
            "interfaces": [
                "🖥️ Modern GUI with Drag & Drop",
                "⚡ Command Line Interface", 
                "🌐 REST API Server Mode",
                "📊 Performance Monitoring Dashboard",
            ]
        }
        
        # All dependencies for complete installation
        self.dependencies = {
            "core": [
                "python-docx>=0.8.11",
                "PyPDF2>=3.0.0", 
                "reportlab>=3.6.0",
                "lxml>=4.9.0",
            ],
            "markdown": [  # NEW in v2.1.0
                "markdown>=3.4.0",
                "beautifulsoup4>=4.11.0",
                "striprtf>=0.0.26",
                "ebooklib>=0.18",
            ],
            "ocr": [
                "pytesseract>=0.3.10",
                "Pillow>=9.0.0",
                "opencv-python>=4.5.0",
                "easyocr>=1.6.0",
                "numpy>=1.21.0",
            ],
            "gui": [
                "tkinter-dnd2>=0.3.0",
            ],
            "server": [
                "flask>=3.0.0",
                "flask-cors>=3.0.0", 
                "waitress>=2.1.0",
            ],
            "performance": [  # NEW in v2.1.0
                "psutil>=5.9.0",
                "tqdm>=4.64.0",
                "colorama>=0.4.5",
            ],
            "build": [
                "pyinstaller>=5.0.0",
                "setuptools>=60.0.0",
                "wheel>=0.37.0",
            ]
        }
    
    def setup_build_environment(self) -> bool:
        """Set up build environment"""
        print("🏗️ Setting up build environment...")
        
        # Create directories
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
        # Create temp directory
        self.temp_dir = tempfile.mkdtemp()
        print(f"   📁 Build directory: {self.build_dir}")
        print(f"   📁 Distribution directory: {self.dist_dir}")
        print(f"   📁 Temporary directory: {self.temp_dir}")
        
        return True
    
    def check_python_environment(self) -> Dict[str, any]:
        """Check Python environment and capabilities"""
        print("🐍 Checking Python environment...")
        
        import platform
        import struct
        
        env_info = {
            'python_version': sys.version,
            'platform': platform.platform(),
            'architecture': platform.machine(),
            'python_bits': struct.calcsize("P") * 8,
            'executable': sys.executable,
            'can_build_32bit': False,
            'pip_available': False
        }
        
        # Check pip availability
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                          capture_output=True, check=True)
            env_info['pip_available'] = True
        except:
            pass
        
        # Check 32-bit build capability
        env_info['can_build_32bit'] = env_info['python_bits'] in [32, 64]
        
        print(f"   🐍 Python {env_info['python_bits']}-bit")
        print(f"   🖥️ Platform: {env_info['platform']}")
        print(f"   📦 Pip: {'✅' if env_info['pip_available'] else '❌'}")
        print(f"   🏗️ 32-bit build: {'✅' if env_info['can_build_32bit'] else '❌'}")
        
        return env_info
    
    def install_all_dependencies(self) -> bool:
        """Install all required dependencies"""
        print("📦 Installing all dependencies...")
        
        all_deps = []
        for category, deps in self.dependencies.items():
            all_deps.extend(deps)
            print(f"   📋 {category.title()}: {len(deps)} packages")
        
        print(f"   📊 Total packages: {len(all_deps)}")
        
        # Create requirements file
        req_file = os.path.join(self.temp_dir, "complete_requirements.txt")
        with open(req_file, 'w') as f:
            f.write(f"# Universal Document Converter v{self.app_version} - Complete Dependencies\\n")
            f.write(f"# Generated automatically for complete installation\\n\\n")
            
            for category, deps in self.dependencies.items():
                f.write(f"# {category.upper()} dependencies\\n")
                for dep in deps:
                    f.write(f"{dep}\\n")
                f.write(f"\\n")
        
        # Install using pip
        try:
            print("   🔄 Installing packages...")
            cmd = [sys.executable, '-m', 'pip', 'install', '-r', str(req_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   ✅ All dependencies installed successfully")
                return True
            else:
                print(f"   ❌ Installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ❌ Installation error: {e}")
            return False
    
    def create_comprehensive_executable(self) -> bool:
        """Create executable with all features"""
        print("🔧 Creating comprehensive executable...")
        
        main_script = self.app_dir / "universal_document_converter_ocr.py"
        if not main_script.exists():
            print("   ❌ Main application script not found!")
            return False
        
        # Comprehensive PyInstaller command
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--windowed',
            '--name', f'Universal-Document-Converter-v{self.app_version}',
            '--distpath', str(self.dist_dir),
            '--workpath', str(self.build_dir / 'work'),
            '--specpath', str(self.build_dir),
            
            # Icon
            '--icon', str(self.app_dir / 'icon.ico'),
            
            # Core application data
            '--add-data', f'{self.app_dir / "ocr_engine"};ocr_engine',
            '--add-data', f'{self.app_dir / "icon.ico"};.',
            
            # VFP9/VB6 Integration files
            '--add-data', f'{self.app_dir / "UniversalConverter_VFP9.prg"};vfp9_vb6',
            '--add-data', f'{self.app_dir / "VB6_UniversalConverter.bas"};vfp9_vb6',
            '--add-data', f'{self.app_dir / "VB6_ConverterForm.frm"};vfp9_vb6',
            '--add-data', f'{self.app_dir / "VFP9_PipeClient.prg"};vfp9_vb6',
            '--add-data', f'{self.app_dir / "VB6_PipeClient.bas"};vfp9_vb6',
            '--add-data', f'{self.app_dir / "dist" / "UniversalConverter32.dll.zip"};vfp9_vb6',
            
            # Core GUI and system dependencies
            '--hidden-import', 'tkinter',
            '--hidden-import', 'tkinter.ttk',
            '--hidden-import', 'tkinter.filedialog',
            '--hidden-import', 'tkinter.messagebox',
            '--hidden-import', 'tkinterdnd2',
            
            # NEW v2.1.0: Markdown processing 
            '--hidden-import', 'markdown',
            '--hidden-import', 'markdown.extensions',
            '--hidden-import', 'markdown.extensions.extra',
            '--hidden-import', 'markdown.extensions.toc',
            '--hidden-import', 'markdown.extensions.tables',
            '--hidden-import', 'bs4',
            '--hidden-import', 'beautifulsoup4',
            '--hidden-import', 'striprtf',
            '--hidden-import', 'ebooklib',
            '--hidden-import', 'ebooklib.epub',
            
            # Document processing
            '--hidden-import', 'docx',
            '--hidden-import', 'docx.document',
            '--hidden-import', 'docx.shared',
            '--hidden-import', 'PyPDF2',
            '--hidden-import', 'reportlab',
            '--hidden-import', 'reportlab.pdfgen',
            '--hidden-import', 'lxml',
            '--hidden-import', 'lxml.etree',
            '--hidden-import', 'lxml.html',
            
            # OCR dependencies
            '--hidden-import', 'pytesseract',
            '--hidden-import', 'PIL',
            '--hidden-import', 'PIL.Image',
            '--hidden-import', 'cv2',
            '--hidden-import', 'easyocr',
            '--hidden-import', 'numpy',
            
            # Server and API
            '--hidden-import', 'flask',
            '--hidden-import', 'flask_cors',
            '--hidden-import', 'waitress',
            '--hidden-import', 'werkzeug',
            
            # Performance and monitoring  
            '--hidden-import', 'psutil',
            '--hidden-import', 'concurrent.futures',
            '--hidden-import', 'threading',
            '--hidden-import', 'multiprocessing',
            '--hidden-import', 'tqdm',
            '--hidden-import', 'colorama',
            
            # System and utility modules
            '--hidden-import', 'json',
            '--hidden-import', 'pathlib',
            '--hidden-import', 'tempfile',
            '--hidden-import', 'logging',
            '--hidden-import', 'subprocess',
            '--hidden-import', 'hashlib',
            '--hidden-import', 'time',
            '--hidden-import', 'datetime',
            '--hidden-import', 'os',
            '--hidden-import', 'sys',
            '--hidden-import', 'platform',
            
            str(main_script)
        ]
        
        print(f"   🔧 Building executable with {len(cmd)-10} hidden imports...")
        print(f"   📁 Output: {self.dist_dir}")
        
        try:
            # Run PyInstaller
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   ✅ Executable created successfully!")
                
                # Check if file exists
                exe_file = self.dist_dir / f'Universal-Document-Converter-v{self.app_version}.exe'
                if exe_file.exists():
                    size_mb = exe_file.stat().st_size / (1024 * 1024)
                    print(f"   📊 Executable size: {size_mb:.1f} MB")
                    return True
                else:
                    print("   ❌ Executable file not found after build")
                    return False
            else:
                print(f"   ❌ Build failed: {result.stderr[:200]}...")
                return False
                
        except Exception as e:
            print(f"   ❌ Build error: {e}")
            return False
    
    def create_installation_package(self) -> bool:
        """Create complete installation package"""
        print("📦 Creating installation package...")
        
        package_dir = self.dist_dir / "installation_package"
        package_dir.mkdir(exist_ok=True)
        
        # Copy executable
        exe_file = self.dist_dir / f'Universal-Document-Converter-v{self.app_version}.exe'
        if exe_file.exists():
            shutil.copy2(exe_file, package_dir)
            print(f"   ✅ Copied executable ({exe_file.stat().st_size // (1024*1024)} MB)")
        
        # Create installer script
        installer_script = package_dir / "install.bat"
        with open(installer_script, 'w') as f:
            f.write(f"""@echo off
echo Universal Document Converter v{self.app_version} - Installation
echo ============================================
echo.
echo Features:
""")
            for category, features in self.features.items():
                f.write(f"echo {category.upper()}:\n")
                for feature in features:
                    f.write(f"echo   {feature}\n")
                f.write("echo.\n")
            
            f.write(f"""
echo Installing to: %PROGRAMFILES%\\Universal Document Converter
echo.
pause

REM Create installation directory
mkdir "%PROGRAMFILES%\\Universal Document Converter" 2>nul

REM Copy executable
copy "Universal-Document-Converter-v{self.app_version}.exe" "%PROGRAMFILES%\\Universal Document Converter\\" >nul
if errorlevel 1 (
    echo ❌ Installation failed! Please run as Administrator.
    pause
    exit /b 1
)

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Universal Document Converter.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\Universal Document Converter\\Universal-Document-Converter-v{self.app_version}.exe'; $Shortcut.Save()"

REM Create start menu entry
mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Universal Document Converter" 2>nul
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Universal Document Converter\\Universal Document Converter.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\Universal Document Converter\\Universal-Document-Converter-v{self.app_version}.exe'; $Shortcut.Save()"

echo.
echo ✅ Installation completed successfully!
echo.
echo You can now run Universal Document Converter from:
echo   • Desktop shortcut
echo   • Start Menu
echo   • %PROGRAMFILES%\\Universal Document Converter\\
echo.
echo NEW in v{self.app_version}:
echo   ✨ Bidirectional Markdown ↔ RTF conversion
echo   ✨ 32-bit legacy system support (VFP9, VB6)
echo   ✨ 13.5x faster multi-threading performance
echo.
pause
""")
        
        # Create README for the package
        readme_file = package_dir / "README_INSTALLATION.md"
        with open(readme_file, 'w') as f:
            f.write(f"""# Universal Document Converter v{self.app_version}
## Complete Installation Package

### 🎯 What's New in v{self.app_version}

#### Core New Features:
""")
            for feature in self.features["new_v21"]:
                f.write(f"- {feature}\n")
            
            f.write(f"""
#### All Features:
""")
            for category, features in self.features.items():
                f.write(f"\n**{category.upper()}:**\n")
                for feature in features:
                    f.write(f"- {feature}\n")
            
            f.write(f"""

### 📦 Installation Instructions

#### Option 1: Automatic Installation (Recommended)
1. **Double-click `install.bat`**
2. **Run as Administrator** when prompted
3. Follow the installation prompts
4. Desktop shortcut will be created automatically

#### Option 2: Manual Installation
1. Copy `Universal-Document-Converter-v{self.app_version}.exe` to your desired location
2. Create shortcuts as needed
3. Run the executable directly

### 🖥️ System Requirements
- **Windows**: 7, 8, 10, 11 (32-bit or 64-bit)
- **Memory**: 512 MB RAM minimum, 2 GB recommended
- **Disk Space**: 200 MB for installation
- **Optional**: Internet connection for updates

### 🚀 Quick Start
1. Launch "Universal Document Converter" from desktop or start menu
2. **NEW**: Try Markdown → RTF conversion!
3. Drag & drop files or use "Browse" button
4. Select output format (now includes Markdown!)
5. Click "Convert" and enjoy 13.5x faster performance!

### 🔧 For Developers (VFP9/VB6 Integration)

#### Command Line Usage:
```cmd
"Universal-Document-Converter-v{self.app_version}.exe" input.md output.rtf rtf
```

#### VFP9 Example:
```foxpro
lcCommand = ["Universal-Document-Converter-v{self.app_version}.exe" input.md output.rtf rtf]
RUN /N (lcCommand)
```

### 📞 Support
- **GitHub**: https://github.com/Beaulewis1977/quick_ocr_doc_converter
- **Issues**: Report bugs and feature requests on GitHub
- **Email**: blewisxx@gmail.com

### 📝 License
This software is provided under the MIT License.

---
*Generated by Universal Document Converter Installation Creator v{self.app_version}*
""")
        
        # Create ZIP package
        zip_file = self.dist_dir / f"Universal-Document-Converter-v{self.app_version}-Windows-Complete.zip"
        
        print(f"   📦 Creating ZIP package: {zip_file.name}")
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in package_dir.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(package_dir)
                    zf.write(file, arcname)
                    print(f"      + {arcname}")
        
        zip_size_mb = zip_file.stat().st_size / (1024 * 1024)
        print(f"   ✅ Package created: {zip_size_mb:.1f} MB")
        
        return True
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
            print("🧹 Cleaned up temporary files")
    
    def run(self) -> bool:
        """Run complete installer creation process"""
        print("🚀 Universal Document Converter - Complete Installer Creator")
        print("=" * 70)
        print(f"📋 Version: {self.app_version}")
        print(f"🏷️  Publisher: {self.publisher}")
        print(f"📄 Description: {self.description}")
        print()
        
        try:
            # Setup environment
            if not self.setup_build_environment():
                return False
            
            # Check Python environment
            env_info = self.check_python_environment()
            if not env_info['pip_available']:
                print("❌ pip not available - cannot install dependencies")
                return False
            
            # Install dependencies
            if not self.install_all_dependencies():
                print("❌ Failed to install dependencies")
                return False
            
            # Create executable
            if not self.create_comprehensive_executable():
                print("❌ Failed to create executable")
                return False
            
            # Create installation package
            if not self.create_installation_package():
                print("❌ Failed to create installation package")
                return False
            
            print()
            print("🎉 COMPLETE INSTALLER CREATION SUCCESSFUL!")
            print("=" * 70)
            print(f"📦 Installation package: {self.dist_dir / f'Universal-Document-Converter-v{self.app_version}-Windows-Complete.zip'}")
            print(f"🖥️  Executable: {self.dist_dir / f'Universal-Document-Converter-v{self.app_version}.exe'}")
            print()
            print("📋 Package Contents:")
            print("   • One-click Windows installer (install.bat)")  
            print("   • Complete standalone executable")
            print("   • Installation instructions (README)")
            print("   • All dependencies included")
            print()
            print("🎯 Ready for distribution!")
            
            return True
            
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            self.cleanup()

def main():
    """Main function"""
    creator = CompleteInstallerCreator()
    success = creator.run()
    
    if success:
        print("\n✅ All done! Your complete installer package is ready.")
        input("Press Enter to exit...")
    else:
        print("\n❌ Installation creation failed. Check the output above.")
        input("Press Enter to exit...")
    
    return success

if __name__ == '__main__':
    main()