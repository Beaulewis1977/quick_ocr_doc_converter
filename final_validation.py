#!/usr/bin/env python3
"""
Final validation before release
Checks for common bugs and issues
"""

import os
import subprocess
import sys
import ast
import re

def check_syntax_all_files():
    """Check Python syntax for all .py files"""
    print("Checking Python syntax...")
    errors = []
    
    py_files = []
    for root, dirs, files in os.walk("."):
        # Skip venv and cache directories
        if "venv" in root or "__pycache__" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    
    for file in py_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            compile(content, file, 'exec')
            ast.parse(content)
        except SyntaxError as e:
            errors.append(f"Syntax error in {file}: {e}")
        except Exception as e:
            errors.append(f"Parse error in {file}: {e}")
    
    if errors:
        print(f"❌ Found {len(errors)} syntax errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"✓ Syntax check passed for {len(py_files)} files")
    
    return len(errors) == 0

def check_common_bugs():
    """Check for common Python bugs"""
    print("\nChecking for common bugs...")
    issues = []
    
    patterns = [
        # Check for bare except
        (r'except\s*:', "Bare except clause (catches all exceptions)"),
        # Check for mutable default arguments
        (r'def\s+\w+\s*\([^)]*=\s*(\[\]|\{\})', "Mutable default argument"),
        # Check for == None instead of is None
        (r'==\s*None', "Use 'is None' instead of '== None'"),
        # Check for != None instead of is not None  
        (r'!=\s*None', "Use 'is not None' instead of '!= None'"),
        # Check for print statements (should use logging)
        (r'^\s*print\s*\(', "Consider using logging instead of print"),
    ]
    
    gui_files = [
        'universal_document_converter_ultimate.py',
        'universal_document_converter_ocr.py',
        'universal_document_converter.py',
        'simple_gui.py'
    ]
    
    for file in gui_files:
        if not os.path.exists(file):
            continue
            
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        for i, line in enumerate(lines):
            for pattern, message in patterns:
                if re.search(pattern, line):
                    # Skip if it's in a comment or string
                    if line.strip().startswith('#') or '"""' in line or "'''" in line:
                        continue
                    issues.append(f"{file}:{i+1} - {message}: {line.strip()}")
    
    if issues:
        print(f"⚠ Found {len(issues)} potential issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    else:
        print("✓ No common bugs found")
    
    return len(issues)

def check_error_handling():
    """Check for proper error handling"""
    print("\nChecking error handling...")
    issues = []
    
    # Check main GUI files
    gui_files = [
        'universal_document_converter_ultimate.py',
        'universal_document_converter_ocr.py'
    ]
    
    for file in gui_files:
        if not os.path.exists(file):
            continue
            
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for try blocks without specific exception handling
        try_blocks = re.findall(r'try:.*?except.*?:', content, re.DOTALL)
        bare_excepts = [block for block in try_blocks if 'except:' in block or 'except Exception:' in block]
        
        if bare_excepts:
            issues.append(f"{file}: {len(bare_excepts)} broad exception handlers found")
        
        # Check for file operations without proper error handling
        file_ops = ['open(', 'Path(', '.read(', '.write(']
        for op in file_ops:
            count = content.count(op)
            if count > 0:
                # Rough check - count try blocks around file operations
                protected = len(re.findall(rf'try:.*?{re.escape(op)}.*?except', content, re.DOTALL))
                if protected < count:
                    issues.append(f"{file}: {count - protected} unprotected '{op}' operations")
    
    if issues:
        print(f"⚠ Error handling issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ Error handling looks good")
    
    return len(issues) == 0

def check_imports():
    """Check for import issues"""
    print("\nChecking imports...")
    issues = []
    
    # Test importing main modules
    modules = [
        'universal_document_converter_ultimate',
        'universal_document_converter_ocr',
        'universal_document_converter',
        'simple_gui'
    ]
    
    for module in modules:
        if not os.path.exists(f"{module}.py"):
            continue
            
        try:
            # Import in subprocess to avoid polluting namespace
            result = subprocess.run(
                [sys.executable, '-c', f'import {module}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                issues.append(f"Failed to import {module}: {result.stderr}")
        except subprocess.TimeoutExpired:
            issues.append(f"Import timeout for {module}")
        except Exception as e:
            issues.append(f"Import error for {module}: {e}")
    
    if issues:
        print(f"❌ Import issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ All imports successful")
    
    return len(issues) == 0

def check_dependencies():
    """Check if all required dependencies are documented"""
    print("\nChecking dependencies...")
    
    # Check requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    # Check for core dependencies
    core_deps = [
        'tkinter',  # This is system package
        'python-docx',
        'PyPDF2',
        'beautifulsoup4',
        'striprtf',
        'ebooklib',
        'pytesseract',
        'opencv-python',
        'numpy',
        'Pillow'
    ]
    
    missing = []
    for dep in core_deps:
        if dep != 'tkinter' and dep.lower() not in requirements.lower():
            missing.append(dep)
    
    if missing:
        print(f"⚠ Missing from requirements.txt: {', '.join(missing)}")
    else:
        print("✓ Core dependencies documented")
    
    return len(missing) == 0

def check_file_structure():
    """Check project file structure"""
    print("\nChecking file structure...")
    
    required_files = [
        'README.md',
        'requirements.txt',
        'universal_document_converter_ultimate.py',
        'ocr_engine/__init__.py',
        'ocr_engine/ocr_engine.py',
        'ocr_engine/ocr_integration.py',
        'ocr_engine/format_detector.py'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing required files:")
        for file in missing:
            print(f"  - {file}")
    else:
        print("✓ All required files present")
    
    return len(missing) == 0

def main():
    """Run all validation checks"""
    print("="*60)
    print("FINAL VALIDATION BEFORE RELEASE")
    print("="*60)
    
    checks = [
        ("Syntax Check", check_syntax_all_files),
        ("Import Check", check_imports),
        ("Error Handling", check_error_handling),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure)
    ]
    
    passed = 0
    warnings = 0
    
    for name, check in checks:
        try:
            result = check()
            if result:
                passed += 1
            else:
                warnings += 1
        except Exception as e:
            print(f"❌ {name} failed with error: {e}")
            warnings += 1
    
    # Check for common bugs (informational)
    bug_count = check_common_bugs()
    
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"✓ Passed: {passed}/{len(checks)} checks")
    print(f"⚠ Warnings: {warnings}")
    print(f"⚠ Potential issues: {bug_count}")
    
    if passed == len(checks):
        print("\n✅ READY FOR RELEASE!")
        print("\nRecommended next steps:")
        print("1. Run the application with: python3 universal_document_converter_ultimate.py")
        print("2. Test basic conversion functionality")
        print("3. Review any warnings above")
        print("4. Commit and push to GitHub")
        return 0
    else:
        print("\n❌ NOT READY FOR RELEASE - Fix the issues above!")
        return 1

if __name__ == "__main__":
    exit(main())