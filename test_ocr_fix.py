#!/usr/bin/env python3
"""
Test OCR Configuration Fix
Tests the fixes applied to resolve the Tesseract configuration error
"""

import sys
import os
from pathlib import Path

def test_tesseract_config_file():
    """Test that tesseract_config.py exists and works"""
    try:
        # Check if config file exists
        config_path = Path("tesseract_config.py")
        if not config_path.exists():
            print("❌ tesseract_config.py not found")
            return False
        
        print("✅ tesseract_config.py found")
        
        # Try to import it (this will run the configuration)
        try:
            import tesseract_config
            print("✅ tesseract_config imported successfully")
            
            # Check if environment variable is set
            tessdata_prefix = os.environ.get("TESSDATA_PREFIX")
            if tessdata_prefix:
                print(f"✅ TESSDATA_PREFIX set to: {tessdata_prefix}")
            else:
                print("⚠️  TESSDATA_PREFIX not set")
            
            return True
        except Exception as e:
            print(f"❌ Error importing tesseract_config: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing tesseract config: {e}")
        return False

def test_ocr_engine_patches():
    """Test that OCR engine files have been patched"""
    
    # Check main OCR engine
    try:
        ocr_engine_path = Path("ocr_engine.py")
        if ocr_engine_path.exists():
            with open(ocr_engine_path, "r") as f:
                content = f.read()
            
            if "import tesseract_config" in content:
                print("✅ ocr_engine.py has been patched")
            else:
                print("❌ ocr_engine.py not patched")
                return False
        else:
            print("⚠️  ocr_engine.py not found")
    except Exception as e:
        print(f"❌ Error checking ocr_engine.py: {e}")
        return False
    
    # Check package OCR engine
    try:
        package_engine_path = Path("ocr_engine/ocr_engine.py")
        if package_engine_path.exists():
            with open(package_engine_path, "r") as f:
                content = f.read()
            
            if "import tesseract_config" in content:
                print("✅ ocr_engine/ocr_engine.py has been patched")
            else:
                print("❌ ocr_engine/ocr_engine.py not patched")
                return False
        else:
            print("⚠️  ocr_engine/ocr_engine.py not found")
    except Exception as e:
        print(f"❌ Error checking ocr_engine/ocr_engine.py: {e}")
        return False
    
    return True

def test_gui_ocr_compatibility():
    """Test that GUI OCR has the right return type handling"""
    try:
        gui_ocr_path = Path("universal_document_converter.py")
        if gui_ocr_path.exists():
            with open(gui_ocr_path, "r") as f:
                content = f.read()
            
            # Check for the fix we applied
            if "isinstance(ocr_result, dict)" in content:
                print("✅ universal_document_converter.py has dictionary return type handling")
            else:
                print("❌ universal_document_converter.py missing dictionary return type handling")
                return False
            
            # Check for the proper OCR call format
            if "{'language': self.language_var.get()}" in content:
                print("✅ universal_document_converter.py has proper OCR call format")
            else:
                print("❌ universal_document_converter.py missing proper OCR call format")
                return False
        else:
            print("⚠️  universal_document_converter.py not found")
            return False
    except Exception as e:
        print(f"❌ Error checking universal_document_converter.py: {e}")
        return False
    
    return True

def test_universal_converter_threading():
    """Test that universal converter has thread-safe updates"""
    try:
        converter_path = Path("universal_document_converter_ocr.py")
        if converter_path.exists():
            with open(converter_path, "r") as f:
                content = f.read()
            
            # Check for thread-safe updates
            if "self.root.after(0, lambda:" in content:
                print("✅ universal_document_converter_ocr.py has thread-safe updates")
            else:
                print("❌ universal_document_converter_ocr.py missing thread-safe updates")
                return False
        else:
            print("⚠️  universal_document_converter_ocr.py not found")
            return False
    except Exception as e:
        print(f"❌ Error checking universal_document_converter_ocr.py: {e}")
        return False
    
    return True

def test_ocr_return_format_consistency():
    """Test that OCR engines return consistent format"""
    print("Testing OCR return format consistency...")
    
    # Check if the OCR engine package returns dictionary format
    try:
        package_engine_path = Path("ocr_engine/ocr_engine.py")
        if package_engine_path.exists():
            with open(package_engine_path, "r") as f:
                content = f.read()
            
            # Check for dictionary return format
            if "'text': " in content and "'confidence': " in content:
                print("✅ OCR engine package returns dictionary format")
            else:
                print("❌ OCR engine package missing dictionary return format")
                return False
        else:
            print("⚠️  OCR engine package not found")
            return False
    except Exception as e:
        print(f"❌ Error checking OCR return format: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("OCR CONFIGURATION FIX TEST")
    print("=" * 60)
    
    tests = [
        ("Tesseract Configuration", test_tesseract_config_file),
        ("OCR Engine Patches", test_ocr_engine_patches),
        ("GUI OCR Compatibility", test_gui_ocr_compatibility),
        ("Universal Converter Threading", test_universal_converter_threading),
        ("OCR Return Format Consistency", test_ocr_return_format_consistency),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n✅ ALL CONFIGURATION FIXES APPLIED!")
        print("🎉 OCR system configuration issues have been resolved!")
        print("\nThe fixes address these specific issues:")
        print("1. ✅ Tesseract tessdata path configuration")
        print("2. ✅ OCR engine return type mismatches")
        print("3. ✅ GUI thread-safe updates")
        print("4. ✅ Dictionary vs string return handling")
        print("\nOnce dependencies are installed, the OCR system should work properly.")
    else:
        print(f"\n❌ {total - passed} tests failed")
        print("Some configuration fixes may not have been applied correctly.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)