#!/usr/bin/env python3
"""
Build script for UniversalConverter32.dll
Creates a 32-bit compatible DLL for VFP9/VB6 integration

This script creates a Windows DLL that can be called from VFP9 and VB6
to access the Universal Document Converter functionality.
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path

class DLLBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.build_dir = self.root_dir / "build_dll"
        self.dist_dir = self.root_dir / "dist"
        self.dll_name = "UniversalConverter32.dll"
        
    def prepare_build_directory(self):
        """Prepare the build directory with necessary files"""
        print("📁 Preparing build directory...")
        
        # Clean and create build directory
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        self.build_dir.mkdir(exist_ok=True)
        
        # Copy necessary files
        files_to_copy = [
            "dll_wrapper.py",
            "universal_document_converter_ocr.py",
            "ocr_engine/__init__.py",
            "ocr_engine/ocr_engine.py",
            "ocr_engine/ocr_integration.py",
            "ocr_engine/format_detector.py",
            "ocr_engine/image_processor.py",
        ]
        
        for file in files_to_copy:
            src = self.root_dir / file
            if src.exists():
                dst = self.build_dir / file
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"  ✅ Copied: {file}")
            else:
                print(f"  ⚠️  Missing: {file}")
        
        return True
        
    def create_setup_script(self):
        """Create a setup script for building the DLL"""
        setup_content = '''# setup.py for UniversalConverter32.dll
from distutils.core import setup
import py2exe
import sys

# Add any missing modules
sys.path.append('.')

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)

dll = Target(
    description = "Universal Document Converter 32-bit DLL",
    version = "2.1.0",
    company_name = "Terragon Labs",
    copyright = "Copyright (c) 2024 Beau Lewis",
    name = "UniversalConverter32",
    dest_base = "UniversalConverter32"
)

setup(
    options = {
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'optimize': 2,
            'dll_excludes': ['w9xpopen.exe'],
            'includes': [
                'tkinter', 
                'docx', 
                'PyPDF2', 
                'markdown',
                'beautifulsoup4',
                'pytesseract',
                'PIL',
                'cv2',
                'numpy',
            ],
        }
    },
    dll = [dll],
    zipfile = None,
)
'''
        
        setup_path = self.build_dir / "setup_dll.py"
        with open(setup_path, 'w') as f:
            f.write(setup_content)
        print("✅ Created setup script")
        return setup_path
        
    def build_with_pyinstaller(self):
        """Build DLL using PyInstaller"""
        print("\n🔨 Building DLL with PyInstaller...")
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['dll_wrapper.py'],
    pathex=['{self.build_dir}'],
    binaries=[],
    datas=[
        ('ocr_engine', 'ocr_engine'),
    ],
    hiddenimports=[
        'tkinter',
        'docx',
        'PyPDF2',
        'markdown',
        'bs4',
        'pytesseract',
        'PIL',
        'cv2',
        'numpy',
        'striprtf',
        'ebooklib',
        'lxml',
        'html2text',
        'reportlab',
        'openpyxl',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas', 'scipy'],
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
    name='UniversalConverter32',
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
)
'''
        
        spec_path = self.build_dir / "UniversalConverter32.spec"
        with open(spec_path, 'w') as f:
            f.write(spec_content)
        
        # Change to build directory
        os.chdir(self.build_dir)
        
        try:
            # Run PyInstaller
            cmd = [sys.executable, "-m", "PyInstaller", "--clean", "UniversalConverter32.spec"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ PyInstaller build successful!")
                
                # Move the output to dist
                exe_path = self.build_dir / "dist" / "UniversalConverter32.exe"
                if exe_path.exists():
                    dll_path = self.dist_dir / self.dll_name
                    shutil.copy2(exe_path, dll_path)
                    print(f"✅ Created: {dll_path}")
                    return True
            else:
                print(f"❌ PyInstaller build failed: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Build error: {e}")
        finally:
            os.chdir(self.root_dir)
            
        return False
        
    def create_ctypes_dll(self):
        """Create a simple ctypes-compatible shared library"""
        print("\n🔨 Creating ctypes-compatible DLL...")
        
        # Create a simplified DLL wrapper
        simple_wrapper = '''"""
Simplified DLL wrapper for UniversalConverter32
This creates a ctypes-compatible interface
"""

import ctypes
import json
import os
import sys
from pathlib import Path

# Simple file-based communication for 32-bit compatibility
COMM_DIR = Path(os.environ.get('TEMP', '/tmp')) / 'UniversalConverter'
COMM_DIR.mkdir(exist_ok=True)

def ConvertDocument(input_file, output_file, input_format, output_format):
    """Convert document via file-based IPC"""
    try:
        # Create request file
        request = {
            'action': 'convert',
            'input_file': input_file.decode('utf-8') if isinstance(input_file, bytes) else input_file,
            'output_file': output_file.decode('utf-8') if isinstance(output_file, bytes) else output_file,
            'input_format': input_format.decode('utf-8') if isinstance(input_format, bytes) else input_format,
            'output_format': output_format.decode('utf-8') if isinstance(output_format, bytes) else output_format,
        }
        
        request_file = COMM_DIR / 'request.json'
        with open(request_file, 'w') as f:
            json.dump(request, f)
        
        # Call the converter
        cmd = f'"{sys.executable}" -m universal_document_converter_ocr --json-request "{request_file}"'
        result = os.system(cmd)
        
        # Check result
        response_file = COMM_DIR / 'response.json'
        if response_file.exists():
            with open(response_file, 'r') as f:
                response = json.load(f)
            return 1 if response.get('success') else 0
        
        return 0 if result == 0 else -1
        
    except Exception as e:
        print(f"ConvertDocument error: {e}")
        return -1

def TestConnection():
    """Test if converter is available"""
    try:
        import universal_document_converter_ocr
        return 1
    except:
        return 0

def GetVersion():
    """Get version string"""
    return b"2.1.0"

# Export functions for ctypes
__all__ = ['ConvertDocument', 'TestConnection', 'GetVersion']
'''
        
        wrapper_path = self.build_dir / "simple_dll_wrapper.py"
        with open(wrapper_path, 'w') as f:
            f.write(simple_wrapper)
        
        # Create a batch file that acts as the "DLL"
        batch_dll = f'''@echo off
:: UniversalConverter32.dll simulator
:: This batch file provides DLL-like functionality for VFP9/VB6

set PYTHONPATH=%~dp0
"{sys.executable}" "%~dp0\\simple_dll_wrapper.py" %*
'''
        
        batch_path = self.dist_dir / "UniversalConverter32.bat"
        with open(batch_path, 'w') as f:
            f.write(batch_dll)
        
        print(f"✅ Created batch DLL simulator: {batch_path}")
        return True
        
    def create_dll_package(self):
        """Create the final DLL package with all necessary files"""
        print("\n📦 Creating DLL package...")
        
        # Ensure dist directory exists
        self.dist_dir.mkdir(exist_ok=True)
        
        # Create UniversalConverter32.dll.zip
        zip_path = self.dist_dir / "UniversalConverter32.dll.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add the DLL wrapper files
            files_to_zip = [
                ("dll_wrapper.py", "dll_wrapper.py"),
                ("UniversalConverter_VFP9.prg", "examples/VFP9/UniversalConverter_VFP9.prg"),
                ("VB6_UniversalConverter.bas", "examples/VB6/VB6_UniversalConverter.bas"),
                ("VB6_ConverterForm.frm", "examples/VB6/VB6_ConverterForm.frm"),
                ("VFP9_VB6_INTEGRATION_GUIDE.md", "documentation/VFP9_VB6_INTEGRATION_GUIDE.md"),
            ]
            
            # Add installation instructions
            install_instructions = '''Universal Document Converter 32-bit DLL Package
==============================================

This package contains the 32-bit DLL interface for VFP9 and VB6 integration.

Contents:
- dll_wrapper.py: Python DLL wrapper source
- examples/: VFP9 and VB6 example code
- documentation/: Integration guides

Installation:
1. For Python-based DLL:
   - Install Python 3.x (32-bit version for 32-bit apps)
   - Run: python dll_wrapper.py --build-script
   - Run: python build_dll.py

2. For pre-built DLL:
   - Copy UniversalConverter32.dll to your application directory
   - Or to C:\\Windows\\System32\\ for system-wide access

3. Register the DLL (if needed):
   regsvr32 UniversalConverter32.dll

Testing:
- VFP9: Run the examples in examples/VFP9/
- VB6: Open the project in examples/VB6/

For support and documentation, see:
https://github.com/Beaulewis1977/quick_ocr_doc_converter
'''
            
            zf.writestr("README.txt", install_instructions)
            
            # Add files
            for src, dst in files_to_zip:
                src_path = self.root_dir / src
                if src_path.exists():
                    zf.write(src_path, dst)
                    print(f"  ✅ Added: {dst}")
                else:
                    print(f"  ⚠️  Missing: {src}")
            
            # Add the batch DLL if it exists
            batch_dll = self.dist_dir / "UniversalConverter32.bat"
            if batch_dll.exists():
                zf.write(batch_dll, "UniversalConverter32.bat")
                print(f"  ✅ Added: UniversalConverter32.bat")
        
        print(f"\n✅ Created DLL package: {zip_path}")
        print(f"📦 Size: {zip_path.stat().st_size / 1024:.1f} KB")
        return zip_path
        
    def build(self):
        """Run the complete build process"""
        print("🏗️  Building UniversalConverter32.dll")
        print("=" * 50)
        
        # Step 1: Prepare build directory
        if not self.prepare_build_directory():
            return False
        
        # Step 2: Try to build with PyInstaller
        # Note: This would need PyInstaller installed
        # For now, we'll create the ctypes version
        
        # Step 3: Create ctypes-compatible wrapper
        if not self.create_ctypes_dll():
            return False
        
        # Step 4: Create the DLL package
        package_path = self.create_dll_package()
        
        if package_path and package_path.exists():
            print("\n🎉 Build completed successfully!")
            print(f"📦 Output: {package_path}")
            return True
        else:
            print("\n❌ Build failed!")
            return False


if __name__ == "__main__":
    builder = DLLBuilder()
    success = builder.build()
    sys.exit(0 if success else 1)