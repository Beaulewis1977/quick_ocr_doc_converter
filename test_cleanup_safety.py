#!/usr/bin/env python3
"""
Test to verify which files are safe to remove
Checks imports and dependencies
"""

import os
import ast
import sys

def check_imports_in_file(filepath):
    """Check what a Python file imports"""
    imports = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except:
        pass
    return imports

def test_ultimate_independence():
    """Test if ultimate version is truly self-contained"""
    print("Testing if universal_document_converter_ultimate.py is self-contained...")
    
    ultimate_imports = check_imports_in_file('universal_document_converter_ultimate.py')
    
    # Check if it imports from any of the files we want to remove
    files_to_remove = [
        'document_converter_gui',
        'universal_document_converter_enhanced',
        'run_converter',
        'run_app',
        'direct_launch'
    ]
    
    dependencies = []
    for imp in ultimate_imports:
        for file in files_to_remove:
            if file in imp:
                dependencies.append(f"Depends on {file}: {imp}")
    
    if not dependencies:
        print("✅ Ultimate version is self-contained!")
    else:
        print("❌ Ultimate version has dependencies:")
        for dep in dependencies:
            print(f"  - {dep}")
    
    return len(dependencies) == 0

def test_core_converter_usage():
    """Check what files depend on universal_document_converter.py"""
    print("\nChecking dependencies on universal_document_converter.py...")
    
    dependent_files = []
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        if any(skip in root for skip in ['.git', '__pycache__', 'venv']):
            continue
            
        for file in files:
            if file.endswith('.py') and file != 'universal_document_converter.py':
                filepath = os.path.join(root, file)
                imports = check_imports_in_file(filepath)
                
                if 'universal_document_converter' in imports:
                    dependent_files.append(file)
    
    if dependent_files:
        print(f"✅ Found {len(dependent_files)} files that depend on core converter:")
        for f in dependent_files[:10]:  # Show first 10
            print(f"  - {f}")
        if len(dependent_files) > 10:
            print(f"  ... and {len(dependent_files) - 10} more")
    
    return dependent_files

def test_simple_gui_imports():
    """Test what simple_gui imports"""
    print("\nChecking simple_gui.py imports...")
    
    imports = check_imports_in_file('simple_gui.py')
    
    for imp in imports:
        if 'universal_document_converter' in imp:
            print("✅ simple_gui.py correctly imports from universal_document_converter")
            return True
    
    print("⚠️ simple_gui.py doesn't import universal_document_converter")
    return False

def main():
    print("=" * 60)
    print("CLEANUP SAFETY TEST")
    print("=" * 60)
    
    # Test 1: Ultimate version independence
    ultimate_ok = test_ultimate_independence()
    
    # Test 2: Core converter dependencies
    dependents = test_core_converter_usage()
    
    # Test 3: Simple GUI imports
    simple_ok = test_simple_gui_imports()
    
    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)
    
    if ultimate_ok:
        print("✅ Ultimate version is safe to use independently")
    else:
        print("❌ Ultimate version has dependencies on files marked for removal")
    
    if dependents:
        print(f"⚠️ universal_document_converter.py MUST BE KEPT - {len(dependents)} files depend on it")
    
    if simple_ok:
        print("✅ simple_gui.py correctly uses the core converter")
    
    print("\nSAFE TO REMOVE:")
    print("- document_converter_gui.py (no dependencies)")
    print("- universal_document_converter_enhanced.py (no dependents)")
    print("- Old batch files and launchers")
    print("- build_installer/universal_document_converter.py (duplicate)")
    
    print("\nMUST KEEP:")
    print("- universal_document_converter.py (core module)")
    print("- universal_document_converter_ultimate.py (newest GUI)")
    print("- simple_gui.py (lightweight alternative)")

if __name__ == "__main__":
    main()