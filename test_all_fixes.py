#!/usr/bin/env python3
"""
Test script to verify all OCR fixes are working
"""

import sys
import os
from pathlib import Path
import traceback

def test_import_ocr_engine():
    """Test importing OCREngine from the package"""
    try:
        from ocr_engine import OCREngine
        ocr = OCREngine()
        
        # Test if methods exist
        methods_to_test = ['is_available', 'extract_text_from_pdf', 'extract_text']
        for method in methods_to_test:
            if hasattr(ocr, method):
                print(f"✅ {method} method exists")
            else:
                print(f"❌ {method} method missing")
                return False
        
        print("✅ OCREngine package import successful")
        return True
        
    except Exception as e:
        print(f"❌ OCREngine package import failed: {e}")
        traceback.print_exc()
        return False

def test_gui_ocr_import():
    """Test importing GUI OCR"""
    try:
        from gui_ocr import OCRGUI
        print("✅ GUI OCR import successful")
        return True
        
    except Exception as e:
        print(f"❌ GUI OCR import failed: {e}")
        traceback.print_exc()
        return False

def test_universal_converter_import():
    """Test importing Universal Document Converter"""
    try:
        from universal_document_converter_ocr import DocumentConverterApp
        print("✅ Universal Document Converter import successful")
        return True
        
    except Exception as e:
        print(f"❌ Universal Document Converter import failed: {e}")
        traceback.print_exc()
        return False

def test_tkinterdnd2_import():
    """Test importing tkinterdnd2"""
    try:
        from tkinterdnd2 import DND_FILES, TkinterDnD
        print("✅ tkinterdnd2 import successful")
        return True
        
    except Exception as e:
        print(f"❌ tkinterdnd2 import failed: {e}")
        print("   Please install with: pip install tkinterdnd2")
        return False

def test_packaging_resolved():
    """Test that packaging conflicts are resolved"""
    try:
        # Test core OCR dependencies
        import pytesseract
        print("✅ pytesseract import successful")
        
        import easyocr
        print("✅ easyocr import successful")
        
        # Test packaging module
        from packaging.version import Version
        print("✅ packaging.version import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Packaging test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("OCR SYSTEM COMPREHENSIVE TEST")
    print("="*60)
    
    tests = [
        ("Packaging Conflicts", test_packaging_resolved),
        ("OCREngine Package", test_import_ocr_engine),
        ("GUI OCR Import", test_gui_ocr_import),
        ("Universal Converter Import", test_universal_converter_import),
        ("tkinterdnd2 Import", test_tkinterdnd2_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        print("🎉 OCR system is ready to use!")
        print("\nYou can now run:")
        print("  - python gui_ocr.py")
        print("  - python universal_document_converter_ocr.py")
        print("  - Drag and drop functionality should work")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        print("Please check the error messages above and install missing dependencies.")
        print("\nTo install missing dependencies:")
        print("  python install_requirements.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())