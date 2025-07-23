#!/usr/bin/env python3
"""Test basic imports and structure without dependencies"""

import sys
import ast
from pathlib import Path

def test_file_structure(file_path):
    """Test if a Python file can be parsed and has expected structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content, filename=str(file_path))
        
        # Check for class definitions
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        return True, {"classes": classes, "functions": functions}
    except Exception as e:
        return False, str(e)

def main():
    print("Testing key file structures...")
    
    key_files = [
        "universal_document_converter.py",
        "ocr_engine/ocr_engine.py", 
        "ocr_engine/security.py",
        "document_converter_gui.py",
        "dll_builder_cli.py"
    ]
    
    all_good = True
    
    for file_path in key_files:
        success, result = test_file_structure(file_path)
        if success:
            print(f"\n✅ {file_path}:")
            print(f"   Classes: {len(result['classes'])}")
            print(f"   Functions: {len(result['functions'])}")
            if result['classes']:
                print(f"   Main classes: {', '.join(result['classes'][:3])}")
        else:
            print(f"\n❌ {file_path}: {result}")
            all_good = False
    
    # Check our security fixes
    print("\n\nChecking security fixes...")
    
    # Check subprocess.run with shell=True
    dangerous_patterns = [
        ("subprocess.run.*shell=True", "Command injection vulnerability"),
        ("os.system\\(", "OS command injection vulnerability"),
        ("except:\\s*$", "Bare except clause")
    ]
    
    for pattern, description in dangerous_patterns:
        print(f"\nChecking for {description}...")
        import re
        found = False
        for py_file in Path('.').rglob('*.py'):
            if '.venv' in str(py_file) or '__pycache__' in str(py_file) or '.bak' in str(py_file):
                continue
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(pattern, content, re.MULTILINE):
                    print(f"   ⚠️  Found in {py_file}")
                    found = True
        if not found:
            print(f"   ✅ No {description} found!")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())