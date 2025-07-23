#!/usr/bin/env python3
"""
Build OCR Document Converter Packages
Creates the two distribution packages as specified in README:
1. UniversalConverter32.dll.zip - DLL package for VFP9/VB6
2. Universal-Document-Converter-v3.1.0-Windows-Complete.zip - Complete application
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
import json

class OCRPackageBuilder:
    def __init__(self):
        self.version = "3.1.0"
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / "dist"
        self.dist_dir.mkdir(exist_ok=True)
        
    def log(self, message):
        print(f"[BUILD] {message}")
        
    def create_dll_package(self):
        """Create the DLL package for VFP9/VB6 integration"""
        self.log("Creating DLL package...")
        
        dll_files = [
            "UniversalConverter32.dll.bat",  # DLL simulator
            "vb6_integration_simple.vb",     # VB6 integration for simple CLI
            "vfp9_integration_simple.prg",   # VFP9 integration for simple CLI
            "cli.py",                        # Simple CLI without OCR
            "requirements.txt",              # Dependencies for CLI
            "README_DLL.md"                  # DLL package documentation
        ]
        
        dll_zip_path = self.dist_dir / "UniversalConverter32.dll.zip"
        
        with zipfile.ZipFile(dll_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in dll_files:
                file_path = self.root_dir / file
                if file_path.exists():
                    zf.write(file_path, file)
                    self.log(f"  Added: {file}")
                else:
                    self.log(f"  Warning: {file} not found")
                    
        self.log(f"DLL package created: {dll_zip_path}")
        return dll_zip_path
        
    def create_complete_package(self):
        """Create the complete application package"""
        self.log("Creating complete package...")
        
        # Files to include in complete package
        app_files = [
            # Main complete GUI application (OCR + Document Conversion + VB6/VFP9)
            "universal_document_converter.py",
            
            # OCR engine
            "ocr_engine/__init__.py",
            "ocr_engine/ocr_engine.py",
            "ocr_engine/ocr_integration.py",
            "ocr_engine/format_detector.py",
            "ocr_engine/image_processor.py",
            "ocr_engine/error_handler.py",
            "ocr_engine/memory_processor.py",
            "ocr_engine/security.py",
            "ocr_engine/config_manager.py",
            
            # Cross-platform Tesseract configuration
            "tesseract_config.py",
            
            # Launchers
            "run_ocr_converter.bat",
            "launch_ocr.py",
            "⚡ Quick Launch OCR.bat",
            
            # Simple CLI for VB6/VFP9 DLL system (without OCR)
            "cli.py",
            
            # VB6/VFP9 integration files
            "vb6_integration_simple.vb",
            "vfp9_integration_simple.prg",
            
            # Installation
            "install.bat",
            "setup_ocr_environment.py",
            "requirements.txt",
            
            # Documentation
            "README.md",
            "OCR_README.md",
            "QUICK_START.md",
            "TROUBLESHOOTING.md",
            "LICENSE",
            
            # Configuration
            "config.json"
        ]
        
        # Create temporary directory for package contents
        temp_dir = self.root_dir / "temp_package"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()
        
        # Copy files maintaining structure
        for file in app_files:
            src = self.root_dir / file
            if src.exists():
                # Maintain directory structure
                if "/" in file:
                    dst_dir = temp_dir / Path(file).parent
                    dst_dir.mkdir(parents=True, exist_ok=True)
                dst = temp_dir / file
                shutil.copy2(src, dst)
                self.log(f"  Added: {file}")
            else:
                self.log(f"  Warning: {file} not found")
                
        # Copy DLL package into complete package
        dll_zip = self.dist_dir / "UniversalConverter32.dll.zip"
        if dll_zip.exists():
            shutil.copy2(dll_zip, temp_dir / "UniversalConverter32.dll.zip")
            self.log("  Added: UniversalConverter32.dll.zip")
            
        # Create install.bat if it doesn't exist
        install_bat = temp_dir / "install.bat"
        if not install_bat.exists():
            with open(install_bat, 'w') as f:
                f.write('''@echo off
title OCR Document Converter Installer
echo Installing OCR Document Converter v3.1.0...
echo.

:: Run Python setup
python setup_ocr_environment.py

:: Create desktop shortcut
echo Creating desktop shortcut...
python -c "import os; os.system('powershell -Command \\"$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut(\\''$Home\\\\Desktop\\\\OCR Document Converter.lnk\\''); $Shortcut.TargetPath = \\''%CD%\\\\run_ocr_converter.bat\\''; $Shortcut.Save()\\"')"

echo.
echo Installation complete!
pause
''')
            
        # Create the complete package zip
        complete_zip_path = self.dist_dir / f"Universal-Document-Converter-v{self.version}-Windows-Complete.zip"
        
        with zipfile.ZipFile(complete_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in temp_dir.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(temp_dir)
                    zf.write(file, arcname)
                    
        # Cleanup
        shutil.rmtree(temp_dir)
        
        self.log(f"Complete package created: {complete_zip_path}")
        return complete_zip_path
        
    def build_all(self):
        """Build all packages"""
        self.log("=== OCR Document Converter Package Builder ===")
        self.log(f"Version: {self.version}")
        self.log(f"Output directory: {self.dist_dir}")
        self.log("")
        
        # Build DLL package first
        dll_package = self.create_dll_package()
        
        # Build complete package (includes DLL package)
        complete_package = self.create_complete_package()
        
        # Summary
        self.log("")
        self.log("=== Build Summary ===")
        if dll_package.exists():
            size_kb = dll_package.stat().st_size / 1024
            self.log(f"DLL Package: {dll_package.name} ({size_kb:.1f} KB)")
        if complete_package.exists():
            size_kb = complete_package.stat().st_size / 1024
            self.log(f"Complete Package: {complete_package.name} ({size_kb:.1f} KB)")
            
        self.log("")
        self.log("Packages ready for release!")
        self.log("Upload these files to GitHub releases:")
        self.log(f"  - {dll_package.name}")
        self.log(f"  - {complete_package.name}")

def main():
    builder = OCRPackageBuilder()
    builder.build_all()

if __name__ == "__main__":
    main()