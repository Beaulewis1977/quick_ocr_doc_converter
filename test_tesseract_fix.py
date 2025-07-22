#!/usr/bin/env python3
"""
Test Tesseract Configuration Fix
"""

import sys
import os

def test_tesseract_config():
    """Test if Tesseract configuration is working"""
    try:
        # Import the configuration
        import tesseract_config
        
        # Test pytesseract
        import pytesseract
        
        # Test if we can get the version
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract version: {version}")
        
        # Test if we can get languages
        languages = pytesseract.get_languages()
        print(f"✅ Available languages: {languages}")
        
        # Check environment variables
        tessdata_prefix = os.environ.get("TESSDATA_PREFIX")
        print(f"✅ TESSDATA_PREFIX: {tessdata_prefix}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tesseract configuration test failed: {e}")
        return False

def test_ocr_engine_import():
    """Test if OCR engine imports correctly"""
    try:
        from ocr_engine import OCREngine
        ocr = OCREngine()
        
        if ocr.is_available():
            print("✅ OCR Engine available")
            return True
        else:
            print("❌ OCR Engine not available")
            return False
            
    except Exception as e:
        print(f"❌ OCR Engine import failed: {e}")
        return False

def main():
    print("=" * 60)
    print("TESSERACT CONFIGURATION TEST")
    print("=" * 60)
    
    tests = [
        ("Tesseract Configuration", test_tesseract_config),
        ("OCR Engine Import", test_ocr_engine_import),
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED")
    
    print(f"\n={'='*60}")
    print(f"RESULTS: {passed}/{len(tests)} tests passed")
    print("=" * 60)
    
    if passed == len(tests):
        print("\n✅ Tesseract configuration is working!")
        print("You can now run the OCR applications.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
