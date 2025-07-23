#!/usr/bin/env python3
"""Check all Python files for syntax errors using py_compile."""

import py_compile
import sys
from pathlib import Path

def check_python_files():
    """Check all Python files for syntax errors."""
    # Get all Python files
    python_files = list(Path('.').glob('**/*.py'))
    
    errors_found = []
    files_checked = 0
    
    print(f"Checking {len(python_files)} Python files for syntax errors...\n")
    
    for py_file in sorted(python_files):
        files_checked += 1
        try:
            # Compile the file to check for syntax errors
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            error_info = {
                'file': str(py_file),
                'error': str(e)
            }
            errors_found.append(error_info)
            print(f"❌ Syntax error in {py_file}")
            print(f"   Error: {e}")
            print()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Summary: Checked {files_checked} files")
    
    if errors_found:
        print(f"\n⚠️  Found {len(errors_found)} files with syntax errors:")
        for error in errors_found:
            print(f"\n📄 {error['file']}")
            print(f"   {error['error']}")
    else:
        print(f"\n✅ All {files_checked} Python files have valid syntax!")
    
    return errors_found

if __name__ == "__main__":
    errors = check_python_files()
    # Exit with error code if syntax errors were found
    sys.exit(1 if errors else 0)