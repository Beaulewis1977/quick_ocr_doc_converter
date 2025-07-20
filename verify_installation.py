#!/usr/bin/env python3
"""
Installation Verification Script
Checks that all dependencies are correctly installed
"""

import sys
import os
import subprocess
from packaging import version

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 8:
        print(f"✅ Python {py_version.major}.{py_version.minor}.{py_version.micro} - OK")
        return True
    else:
        print(f"❌ Python {py_version.major}.{py_version.minor} - Requires 3.8+")
        return False

def check_module(module_name, package_name=None, required_version=None, max_version=None):
    """Check if a module is installed with correct version"""
    if package_name is None:
        package_name = module_name
    
    try:
        module = __import__(module_name.replace('-', '_'))
        
        # Get version
        module_version = None
        if hasattr(module, '__version__'):
            module_version = module.__version__
        elif hasattr(module, 'VERSION'):
            module_version = module.VERSION
        elif module_name == 'cv2':
            module_version = module.__version__
        
        # Check version constraints
        if module_version and required_version:
            if version.parse(module_version) < version.parse(required_version):
                print(f"⚠️  {package_name}: {module_version} (requires >= {required_version})")
                return False
        
        if module_version and max_version:
            if version.parse(module_version) >= version.parse(max_version):
                print(f"⚠️  {package_name}: {module_version} (requires < {max_version})")
                return False
        
        print(f"✅ {package_name}: {module_version or 'installed'}")
        return True
        
    except ImportError:
        print(f"❌ {package_name}: NOT INSTALLED")
        return False
    except Exception as e:
        print(f"⚠️  {package_name}: Error checking - {e}")
        return False

def check_tesseract():
    """Check if Tesseract is installed"""
    print("\n🔍 Checking Tesseract OCR...")
    
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ Tesseract: {version_line}")
            
            # Check for language data
            tessdata_paths = [
                '/usr/share/tesseract-ocr/5/tessdata',
                '/usr/share/tesseract-ocr/4/tessdata', 
                'C:\\Program Files\\Tesseract-OCR\\tessdata',
                'C:\\Program Files (x86)\\Tesseract-OCR\\tessdata',
            ]
            
            for path in tessdata_paths:
                if os.path.exists(path):
                    files = os.listdir(path)
                    if 'eng.traineddata' in files or 'en.traineddata' in files:
                        print(f"✅ Tessdata found at: {path}")
                        return True
                    
            print("⚠️  Tesseract installed but language data not found")
            return True
        else:
            print("❌ Tesseract: NOT INSTALLED or not in PATH")
            return False
            
    except FileNotFoundError:
        print("❌ Tesseract: NOT INSTALLED or not in PATH")
        if sys.platform == 'win32':
            print("   Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        else:
            print("   Install with: sudo apt install tesseract-ocr")
        return False

def check_display():
    """Check display availability"""
    print("\n🖥️  Checking display...")
    
    if sys.platform == 'win32':
        print("✅ Windows - Display should be available")
        return True
    
    display = os.environ.get('DISPLAY')
    if display:
        print(f"✅ Display available: {display}")
        return True
    else:
        print("⚠️  No display detected (DISPLAY not set)")
        print("   For headless systems, use: export DISPLAY=:99 && Xvfb :99 &")
        return True  # Not a critical error

def main():
    """Run all checks"""
    print("=" * 60)
    print("Enhanced OCR Document Converter - Installation Verification")
    print("=" * 60)
    
    all_good = True
    
    # Check Python
    if not check_python_version():
        all_good = False
    
    # Check core dependencies
    print("\n📦 Checking core dependencies...")
    dependencies = [
        ('numpy', None, '1.21.0', '2.0'),  # Must be < 2.0
        ('cv2', 'opencv-python-headless', '4.5.0', None),
        ('pytesseract', None, '0.3.10', None),
        ('packaging', None, '21.3', None),
        ('PIL', 'Pillow', '9.0.0', None),
    ]
    
    for dep in dependencies:
        if not check_module(*dep):
            all_good = False
    
    # Check additional modules
    print("\n📦 Checking additional modules...")
    additional = [
        ('cryptography', None, '41.0.0', None),
        ('docx', 'python-docx', '0.8.11', None),
        ('bs4', 'beautifulsoup4', '4.11.0', None),
        ('reportlab', None, '3.6.0', None),
        ('markdown', None, '3.4.0', None),
        ('psutil', None, '5.9.0', None),
    ]
    
    for mod in additional:
        check_module(*mod)  # Not critical if missing
    
    # Check our custom modules
    print("\n📦 Checking application modules...")
    app_modules = [
        'backends.manager',
        'security.credentials', 
        'monitoring.cost_tracker',
        'ocr_engine.ocr_engine',
    ]
    
    for mod in app_modules:
        if not check_module(mod):
            all_good = False
    
    # Check Tesseract
    if not check_tesseract():
        all_good = False
    
    # Check display
    check_display()
    
    # Final verdict
    print("\n" + "=" * 60)
    if all_good:
        print("✅ All critical dependencies are correctly installed!")
        print("🚀 You can now run: python enhanced_ocr_gui.py")
    else:
        print("❌ Some dependencies are missing or incorrect.")
        print("📋 Please install missing dependencies using:")
        if sys.platform == 'win32':
            print("   install_dependencies_windows.bat")
        else:
            print("   pip install -r requirements.txt")
    
    print("=" * 60)
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())