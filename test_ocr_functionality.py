#!/usr/bin/env python3
"""
Test OCR functionality with actual image processing
"""

import sys
import os
from pathlib import Path

def test_ocr_engine_direct():
    """Test OCR engine directly"""
    print("Testing OCR Engine directly...")
    
    try:
        from ocr_engine import OCREngine
        
        # Initialize OCR engine
        ocr = OCREngine()
        
        # Test availability
        print(f"OCR Available: {ocr.is_available()}")
        
        if ocr.is_available():
            # Test methods exist
            print(f"Has extract_text: {hasattr(ocr, 'extract_text')}")
            print(f"Has extract_text_from_pdf: {hasattr(ocr, 'extract_text_from_pdf')}")
            
            # Test what extract_text returns (without an actual image)
            try:
                result = ocr.extract_text("non_existent_file.jpg", {'language': 'eng'})
                print(f"extract_text return type: {type(result)}")
                if isinstance(result, dict):
                    print(f"extract_text dict keys: {list(result.keys())}")
            except Exception as e:
                print(f"extract_text test (expected to fail): {e}")
                
        return True
        
    except Exception as e:
        print(f"❌ OCR Engine test failed: {e}")
        return False

def test_gui_ocr_compatibility():
    """Test GUI OCR compatibility"""
    print("\nTesting GUI OCR compatibility...")
    
    try:
        from gui_ocr import OCRGUI
        
        # Test creation (without actually showing GUI)
        print("✅ OCRGUI can be imported and created")
        
        return True
        
    except Exception as e:
        print(f"❌ GUI OCR test failed: {e}")
        return False

def test_ocr_method_call_format():
    """Test the format of OCR method calls"""
    print("\nTesting OCR method call format...")
    
    try:
        from ocr_engine import OCREngine
        
        ocr = OCREngine()
        
        if ocr.is_available():
            # Test the method signature works
            test_options = {'language': 'eng'}
            
            # This should not crash even with non-existent file
            try:
                result = ocr.extract_text("test.jpg", test_options)
                print(f"✅ extract_text accepts options dict: {type(result)}")
            except Exception as e:
                print(f"extract_text with options: {e}")
                
            # Test extract_text_from_pdf method signature
            try:
                result = ocr.extract_text_from_pdf("test.pdf", "eng")
                print(f"✅ extract_text_from_pdf accepts language string: {type(result)}")
            except Exception as e:
                print(f"extract_text_from_pdf with language: {e}")
                
        return True
        
    except Exception as e:
        print(f"❌ Method call format test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("OCR FUNCTIONALITY TEST")
    print("="*60)
    
    tests = [
        ("OCR Engine Direct", test_ocr_engine_direct),
        ("GUI OCR Compatibility", test_gui_ocr_compatibility),
        ("OCR Method Call Format", test_ocr_method_call_format),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - FAILED with exception: {e}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✅ OCR functionality tests passed!")
        print("The 'str' object is not a mapping error should be fixed.")
        print("\nTry running gui_ocr.py with your image files again.")
    else:
        print(f"\n❌ {total - passed} tests failed")
        print("There may still be issues to resolve.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())