#!/usr/bin/env python3
"""Test actual document conversion functionality"""

import os
import tempfile
from pathlib import Path

def test_text_conversion():
    """Test basic text file conversion"""
    try:
        from universal_document_converter_ultimate import DocumentConverterUltimate
        
        # Create a test text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content for conversion")
            test_file = f.name
        
        # Test save_text_as_format method
        converter = DocumentConverterUltimate.__new__(DocumentConverterUltimate)
        
        # Test saving as different formats
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test TXT format
            txt_output = os.path.join(tmpdir, "output.txt")
            converter.save_text_as_format("Test content", txt_output, "txt")
            
            if not os.path.exists(txt_output):
                print("❌ TXT conversion failed")
                return False
            
            # Read and verify
            with open(txt_output, 'r') as f:
                content = f.read()
                if content != "Test content":
                    print("❌ TXT content mismatch")
                    return False
        
        # Clean up
        os.unlink(test_file)
        
        print("✓ Text conversion functional")
        return True
        
    except Exception as e:
        print(f"❌ Conversion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ocr_format_detection():
    """Test OCR format detection with real file checks"""
    try:
        from ocr_engine.format_detector import OCRFormatDetector
        
        # Test with extensions only (since we can't create real image files easily)
        detector = OCRFormatDetector()
        
        # Create temporary files to test
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            test_files = {
                "image.jpg": True,
                "document.pdf": False,  # PDF is not in SUPPORTED_IMAGE_FORMATS
                "text.txt": False,
                "photo.png": True,
                "scan.tiff": True
            }
            
            for filename, should_be_ocr in test_files.items():
                filepath = os.path.join(tmpdir, filename)
                # Create empty file
                Path(filepath).touch()
                
                # Test detection
                is_ocr = detector.is_ocr_format(filepath)
                
                if is_ocr != should_be_ocr:
                    print(f"❌ OCR detection wrong for {filename}: got {is_ocr}, expected {should_be_ocr}")
                    # Check what formats are actually supported
                    print(f"   Supported formats: {OCRFormatDetector.SUPPORTED_IMAGE_FORMATS}")
                    return False
        
        print("✓ OCR format detection functional")
        return True
        
    except Exception as e:
        print(f"❌ OCR detection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_persistence():
    """Test configuration save/load"""
    try:
        from universal_document_converter_ultimate import ConfigManager
        
        # Create temporary config
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change config path
            config = ConfigManager()
            config.config_path = Path(tmpdir) / "test_config.json"
            
            # Set test values
            config.set("test_key", "test_value")
            config.set("test_number", 42)
            
            # Create new instance to test loading
            config2 = ConfigManager()
            config2.config_path = config.config_path
            config2.config = config2.load_config()
            
            # Verify values
            if config2.get("test_key") != "test_value":
                print("❌ Config string persistence failed")
                return False
            
            if config2.get("test_number") != 42:
                print("❌ Config number persistence failed") 
                return False
        
        print("✓ Configuration persistence functional")
        return True
        
    except Exception as e:
        print(f"❌ Config persistence test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all conversion tests"""
    print("=== Testing Actual Conversion Functionality ===\n")
    
    tests = [
        test_text_conversion,
        test_ocr_format_detection,
        test_config_persistence
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Summary: {passed}/{len(tests)} tests passed ===")
    
    if passed == len(tests):
        print("\n✅ All conversion tests passed!")
    else:
        print("\n❌ Some tests failed - fix before release!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())