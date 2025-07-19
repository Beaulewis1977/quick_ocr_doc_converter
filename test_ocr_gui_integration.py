#!/usr/bin/env python3
"""
Test script for OCR GUI Integration
Tests the document converter GUI with OCR functionality
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ocr_availability():
    """Test if OCR components are available"""
    print("Testing OCR availability...")
    
    try:
        from ocr_engine.ocr_integration import OCRIntegration
        from ocr_engine.format_detector import OCRFormatDetector
        print("✅ OCR modules imported successfully")
        
        # Test OCR initialization
        ocr = OCRIntegration()
        detector = OCRFormatDetector()
        
        # Check availability
        availability = ocr.check_availability()
        print(f"✅ OCR availability: {availability}")
        
        # Check supported formats
        formats = detector.get_supported_extensions()
        print(f"✅ Supported image formats: {formats}")
        
        return True
        
    except Exception as e:
        print(f"❌ OCR test failed: {str(e)}")
        return False

def test_gui_with_ocr():
    """Test the GUI with OCR integration"""
    print("\nTesting GUI with OCR integration...")
    
    try:
        # Import the GUI module
        from document_converter_gui import DocumentConverterGUI, OCR_AVAILABLE
        
        print(f"✅ GUI module imported successfully")
        print(f"✅ OCR_AVAILABLE flag: {OCR_AVAILABLE}")
        
        # Check if main components are available
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window for testing
        
        # Create GUI instance
        app = DocumentConverterGUI(root)
        
        # Check OCR components
        if OCR_AVAILABLE:
            assert hasattr(app, 'ocr_integration'), "OCR integration not found"
            assert hasattr(app, 'format_detector'), "Format detector not found"
            assert hasattr(app, 'ocr_mode_var'), "OCR mode variable not found"
            print("✅ All OCR components initialized in GUI")
            
            # Check OCR methods
            assert hasattr(app, 'toggle_ocr_mode'), "toggle_ocr_mode method not found"
            assert hasattr(app, 'check_ocr_status'), "check_ocr_status method not found"
            assert hasattr(app, 'convert_image_to_markdown'), "convert_image_to_markdown method not found"
            assert hasattr(app, 'is_pdf_image_based'), "is_pdf_image_based method not found"
            print("✅ All OCR methods available in GUI")
        else:
            print("⚠️  OCR not available - OCR dependencies may need to be installed")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Testing OCR GUI Integration\n")
    
    tests_passed = 0
    tests_total = 2
    
    # Test 1: OCR availability
    if test_ocr_availability():
        tests_passed += 1
    
    # Test 2: GUI with OCR
    if test_gui_with_ocr():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 Test Results: {tests_passed}/{tests_total} passed")
    
    if tests_passed == tests_total:
        print("✅ All tests passed! OCR is successfully integrated into the GUI.")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    
    return tests_passed == tests_total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)