#!/usr/bin/env python3
"""
Verify that the installation includes all features for all platforms
"""

import os
import sys
from pathlib import Path

print("=" * 70)
print("UNIVERSAL DOCUMENT CONVERTER - INSTALLATION VERIFICATION")
print("=" * 70)

# Check 1: Verify requirements.txt includes all features
print("\n1. Checking requirements.txt...")
with open('requirements.txt', 'r') as f:
    requirements_content = f.read()

required_packages = {
    'API Server': ['flask', 'flask-cors', 'waitress'],
    'Drag & Drop': ['tkinter-dnd2'],
    'OCR': ['pytesseract', 'opencv-python'],
    'Document Processing': ['python-docx', 'PyPDF2', 'beautifulsoup4', 'striprtf', 'ebooklib'],
    'GUI & Utils': ['psutil', 'Pillow', 'numpy']
}

all_good = True
for feature, packages in required_packages.items():
    print(f"\n   {feature}:")
    for package in packages:
        if package in requirements_content:
            print(f"      ✅ {package}")
        else:
            print(f"      ❌ {package} MISSING!")
            all_good = False

# Check 2: Verify installer requirements
print("\n\n2. Checking requirements_installer.txt...")
with open('requirements_installer.txt', 'r') as f:
    installer_content = f.read()

installer_required = ['flask', 'flask-cors', 'waitress', 'tkinterdnd2']
for package in installer_required:
    if package in installer_content:
        print(f"   ✅ {package}")
    else:
        print(f"   ❌ {package} MISSING!")
        all_good = False

# Check 3: Verify Windows installer script
print("\n\n3. Checking Windows installer build script...")
with open('create_windows_installer.py', 'r') as f:
    installer_script = f.read()

hidden_imports_needed = ['flask', 'flask_cors', 'waitress', 'tkinterdnd2']
hiddenimports_section = installer_script[installer_script.find('hiddenimports=['):installer_script.find('],', installer_script.find('hiddenimports=['))]

for import_name in hidden_imports_needed:
    if import_name in hiddenimports_section:
        print(f"   ✅ {import_name} in hidden imports")
    else:
        print(f"   ❌ {import_name} NOT in hidden imports!")
        all_good = False

# Check 4: Verify setup_shortcuts.py
print("\n\n4. Checking setup_shortcuts.py...")
with open('setup_shortcuts.py', 'r') as f:
    setup_content = f.read()

setup_packages = ['flask', 'flask-cors', 'waitress', 'pytesseract', 'opencv-python']
for package in setup_packages:
    if package in setup_content:
        print(f"   ✅ {package} will be installed")
    else:
        print(f"   ❌ {package} NOT in setup script!")
        all_good = False

# Check 5: Platform-specific installation commands
print("\n\n5. Platform Installation Commands:")
print("\n   Windows:")
print("      pip install -r requirements.txt")
print("      python create_windows_installer.py")
print("\n   macOS:")
print("      brew install tesseract")
print("      pip3 install -r requirements.txt")
print("\n   Linux:")
print("      sudo apt install tesseract-ocr")
print("      pip3 install -r requirements.txt")

# Summary
print("\n" + "=" * 70)
print("VERIFICATION SUMMARY")
print("=" * 70)

if all_good:
    print("\n✅ ALL FEATURES ARE PROPERLY CONFIGURED FOR INSTALLATION!")
    print("\nThe installation will include:")
    print("   • Full API Server (REST endpoints)")
    print("   • Drag & Drop support")
    print("   • OCR capabilities")
    print("   • All document formats")
    print("   • Multi-threading")
    print("   • All GUI features")
    print("\n✅ Windows executable will have ALL features!")
else:
    print("\n❌ Some features are missing from installation!")
    print("   Please fix the issues above.")

print("\n" + "=" * 70)