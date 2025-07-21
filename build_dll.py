#!/usr/bin/env python3
"""
Build script for UniversalConverter32.dll

Requirements:
- Python 3.x (32-bit for 32-bit DLL)  
- Nuitka: pip install nuitka
- OR cx_Freeze: pip install cx_freeze
- OR PyInstaller: pip install pyinstaller

Usage:
    python build_dll.py
"""

import os
import sys
import subprocess
import shutil

def build_with_nuitka():
    """Build DLL using Nuitka (recommended)"""
    print("🔨 Building DLL with Nuitka...")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--plugin-enable=no-qt",
        "--plugin-disable=tk-inter",
        "--output-dir=dist",
        "--output-filename=UniversalConverter32.dll",
        "--windows-company-name=TerragonLabs",
        "--windows-product-name=UniversalConverter",
        "--windows-file-version=2.1.0.0",
        "--windows-product-version=2.1.0",
        "--windows-file-description=Universal Document Converter DLL",
        "dll_wrapper.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Nuitka build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Nuitka build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Nuitka not found. Install with: pip install nuitka")
        return False

def build_with_cython():
    """Build DLL using Cython"""
    print("🔨 Building DLL with Cython...")
    
    # Create setup.py for Cython
    setup_py = \"""
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

ext = Extension(
    "UniversalConverter32", 
    ["dll_wrapper.py"],
    define_macros=[("WIN32", "1")],
)

setup(
    ext_modules=cythonize([ext], language_level=3),
    zip_safe=False,
)
\"""
    
    with open("setup_dll.py", "w") as f:
        f.write(setup_py)
    
    try:
        cmd = [sys.executable, "setup_dll.py", "build_ext", "--inplace"]
        result = subprocess.run(cmd, check=True)
        print("✅ Cython build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Cython build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Cython not found. Install with: pip install cython")
        return False

def build_with_pyinstaller():
    """Build EXE that can act like DLL"""
    print("🔨 Building executable with PyInstaller...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name=UniversalConverter32",
        "dll_wrapper.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ PyInstaller build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False

if __name__ == "__main__":
    print("🏗️ Building UniversalConverter32.dll")
    print("=" * 50)
    
    # Try build methods in order of preference
    success = False
    
    if not success:
        success = build_with_nuitka()
    
    if not success:
        success = build_with_cython()
    
    if not success:
        success = build_with_pyinstaller()
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("📁 Check the dist/ folder for output files")
    else:
        print("\n❌ All build methods failed")
        print("💡 Install build tools:")
        print("   pip install nuitka")
        print("   pip install cython")  
        print("   pip install pyinstaller")
