#!/usr/bin/env python3
"""
Quick test to verify the main GUI file imports correctly
"""

def test_main_import():
    """Test that the main GUI file can be imported"""
    try:
        print("Testing import of universal_document_converter.py...")
        
        # Try to import the main class
        from universal_document_converter import UniversalDocumentConverter
        print("✅ UniversalDocumentConverter class imported successfully")
        
        # Check if it has the expected methods
        expected_methods = ['setup_ui', 'start_conversion', 'process_ocr']
        for method in expected_methods:
            if hasattr(UniversalDocumentConverter, method):
                print(f"  ✅ Found method: {method}")
            else:
                print(f"  ⚠ Missing method: {method}")
        
        print("\n✅ Import test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_main_import()