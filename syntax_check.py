#!/usr/bin/env python3
"""Check syntax of all Python files"""

import ast
import sys
from pathlib import Path

def check_syntax(file_path):
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content, filename=str(file_path))
        return True, None
    except SyntaxError as e:
        return False, f"{e.msg} at line {e.lineno}"
    except Exception as e:
        return False, str(e)

def main():
    repo_path = Path('.')
    python_files = list(repo_path.glob('**/*.py'))
    
    print(f"Checking {len(python_files)} Python files for syntax errors...")
    
    errors = []
    for file_path in python_files:
        if '.venv' in str(file_path) or '__pycache__' in str(file_path):
            continue
            
        valid, error = check_syntax(file_path)
        if not valid:
            errors.append((file_path, error))
    
    if errors:
        print(f"\n❌ Found {len(errors)} files with syntax errors:")
        for file_path, error in errors:
            print(f"  - {file_path}: {error}")
        sys.exit(1)
    else:
        print(f"\n✅ All {len(python_files)} Python files have valid syntax!")
        sys.exit(0)

if __name__ == "__main__":
    main()