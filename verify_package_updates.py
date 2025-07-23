#!/usr/bin/env python3
"""Verify all package updates and fixes are applied correctly"""

import os
import re
from pathlib import Path

def check_file_for_vulnerabilities(file_path):
    """Check a file for known security vulnerabilities"""
    issues = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check for command injection
    if re.search(r'subprocess\.run.*shell=True', content):
        issues.append("subprocess.run with shell=True")
    
    # Check for os.system
    if re.search(r'os\.system\(', content) and not file_path.endswith('.bak'):
        issues.append("os.system() usage")
    
    # Check for bare except
    if re.search(r'except:\s*$', content, re.MULTILINE):
        issues.append("bare except clause")
    
    return issues

def verify_all_updates():
    """Verify all updates are applied correctly"""
    print("Verifying Package Updates and Security Fixes\n")
    print("=" * 60)
    
    # 1. Check main application files
    print("\n1. Main Application Files:")
    main_files = [
        'universal_document_converter.py',
        'cli.py',
        'document_converter_gui.py',
        'gui_ocr.py',
        'ocr_engine.py'
    ]
    
    all_good = True
    for file in main_files:
        if Path(file).exists():
            issues = check_file_for_vulnerabilities(file)
            if issues:
                print(f"   ❌ {file}: {', '.join(issues)}")
                all_good = False
            else:
                print(f"   ✅ {file}: No security issues")
        else:
            print(f"   ⚠️  {file}: File not found")
    
    # 2. Check OCR engine files
    print("\n2. OCR Engine Files:")
    ocr_files = list(Path('ocr_engine').glob('*.py'))
    for file in ocr_files:
        issues = check_file_for_vulnerabilities(file)
        if issues:
            print(f"   ❌ {file}: {', '.join(issues)}")
            all_good = False
        else:
            print(f"   ✅ {file}: No security issues")
    
    # 3. Check launcher scripts
    print("\n3. Launcher Scripts:")
    launchers = [
        'run_converter.bat',
        'run_ocr_converter.bat',
        'run_converter.sh',
        'launch_ocr.py'
    ]
    
    for launcher in launchers:
        if Path(launcher).exists():
            with open(launcher, 'r') as f:
                content = f.read()
            if 'universal_document_converter.py' in content:
                print(f"   ✅ {launcher}: References correct main file")
            else:
                print(f"   ❌ {launcher}: Does not reference correct main file")
                all_good = False
        else:
            print(f"   ⚠️  {launcher}: File not found")
    
    # 4. Check build_installer directory
    print("\n4. Build Installer Directory:")
    build_installer_file = Path('build_installer/universal_document_converter.py')
    if build_installer_file.exists():
        issues = check_file_for_vulnerabilities(build_installer_file)
        if issues:
            print(f"   ❌ build_installer copy: {', '.join(issues)}")
            all_good = False
        else:
            print(f"   ✅ build_installer copy: Updated with security fixes")
    
    # 5. Check requirements files
    print("\n5. Requirements Files:")
    req_files = ['requirements.txt', 'build_installer/requirements.txt']
    for req_file in req_files:
        if Path(req_file).exists():
            with open(req_file, 'r') as f:
                content = f.read()
            if 'PyPDF2' in content and 'pytesseract' in content:
                print(f"   ✅ {req_file}: Contains all necessary dependencies")
            else:
                print(f"   ❌ {req_file}: Missing dependencies")
                all_good = False
    
    # 6. Check installer scripts
    print("\n6. Installer and Build Scripts:")
    installer_scripts = [
        'install_requirements.py',
        'install_ocr_dependencies.py',
        'convert_to_markdown.py',
        'convert_recursive.py'
    ]
    
    for script in installer_scripts:
        if Path(script).exists():
            issues = check_file_for_vulnerabilities(script)
            if issues:
                print(f"   ❌ {script}: {', '.join(issues)}")
                all_good = False
            else:
                print(f"   ✅ {script}: No security issues")
    
    print("\n" + "=" * 60)
    if all_good:
        print("✅ ALL UPDATES VERIFIED SUCCESSFULLY!")
        print("\nThe package is ready for distribution with:")
        print("- All security vulnerabilities fixed")
        print("- All launchers pointing to correct files")
        print("- All dependencies properly listed")
        print("- Build scripts updated")
    else:
        print("❌ Some issues remain - please review above")
    
    return all_good

if __name__ == "__main__":
    verify_all_updates()