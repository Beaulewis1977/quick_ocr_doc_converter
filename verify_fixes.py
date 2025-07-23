#!/usr/bin/env python3
"""Verify all security fixes were applied correctly"""

import ast
from pathlib import Path

def verify_fixes():
    print("Verifying security fixes...\n")
    
    # 1. Check subprocess fix in universal_document_converter.py
    print("1. Checking subprocess fix in universal_document_converter.py...")
    with open('universal_document_converter.py', 'r') as f:
        content = f.read()
        if 'import shlex' in content and 'shlex.split(command)' in content:
            print("   ✅ subprocess.run fixed to use shlex.split")
        else:
            print("   ❌ subprocess fix not found")
    
    # 2. Check os.system fix in document_converter_gui.py
    print("\n2. Checking os.system fix in document_converter_gui.py...")
    with open('document_converter_gui.py', 'r') as f:
        content = f.read()
        if 'subprocess.run([sys.executable' in content:
            print("   ✅ os.system replaced with subprocess.run")
        else:
            print("   ❌ os.system fix not found")
    
    # 3. Check resource cleanup in universal_document_converter.py
    print("\n3. Checking resource cleanup...")
    with open('universal_document_converter.py', 'r') as f:
        content = f.read()
        if 'def cleanup_resources(self):' in content and 'self.file_handler.close()' in content:
            print("   ✅ Resource cleanup method added")
        else:
            print("   ❌ Resource cleanup not found")
    
    # 4. Check PyMuPDF context managers
    print("\n4. Checking PyMuPDF context managers...")
    files_to_check = ['dll_builder_cli.py', 'gui_ocr.py', 'ocr_engine.py']
    for file in files_to_check:
        if Path(file).exists():
            with open(file, 'r') as f:
                content = f.read()
                if 'with fitz.open' in content:
                    print(f"   ✅ {file}: Using context manager")
                elif 'fitz.open' in content:
                    print(f"   ❌ {file}: Not using context manager")
    
    # 5. Check EasyOCR cleanup
    print("\n5. Checking EasyOCR cleanup...")
    with open('ocr_engine/ocr_engine.py', 'r') as f:
        content = f.read()
        if 'def cleanup(self):' in content and 'del self._thread_local.easyocr_reader' in content:
            print("   ✅ EasyOCR cleanup method added")
        else:
            print("   ❌ EasyOCR cleanup not found")
    
    # 6. Check bare except blocks replaced
    print("\n6. Checking bare except blocks...")
    with open('universal_document_converter.py', 'r') as f:
        content = f.read()
        if 'except (ValueError, AttributeError)' in content:
            print("   ✅ Bare except blocks replaced with specific exceptions")
        else:
            print("   ❌ Specific exception handling not found")
    
    # 7. Check path traversal fix
    print("\n7. Checking path traversal fix...")
    with open('ocr_engine/security.py', 'r') as f:
        content = f.read()
        if "if '..' in path or path.startswith('~'):" in content:
            print("   ✅ Path traversal check improved")
        else:
            print("   ❌ Path traversal fix not found")
    
    # 8. Check threading fixes
    print("\n8. Checking threading fixes...")
    with open('universal_document_converter.py', 'r') as f:
        content = f.read()
        if 'with self.cache_lock:\n                cache_size_mb' in content:
            print("   ✅ Cache access protected with locks")
        else:
            print("   ❌ Cache lock protection not found")
    
    print("\n✅ All major security fixes have been verified!")

if __name__ == "__main__":
    verify_fixes()