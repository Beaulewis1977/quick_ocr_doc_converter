#!/usr/bin/env python3
"""
Test script for OCR fallback system
Tests all fallback scenarios to ensure they work correctly
"""

import os
import sys
import tempfile
import logging
from pathlib import Path
from PIL import Image, ImageDraw

# Add the repo root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from ocr_engine.ocr_engine import OCREngine
from ocr_engine.google_vision_backend import GoogleVisionBackend

def create_test_image(text="TEST FALLBACK", filename="test_image.png"):
    """Create a simple test image with text"""
    img = Image.new('RGB', (400, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a better font
        from PIL import ImageFont
        font = ImageFont.load_default()
        draw.text((20, 30), text, fill='black', font=font)
    except:
        # Fallback to basic text
        draw.text((20, 30), text, fill='black')
    
    temp_path = Path(tempfile.gettempdir()) / filename
    img.save(str(temp_path), 'PNG')
    return str(temp_path)

def test_google_vision_fallback():
    """Test Google Vision to Tesseract fallback"""
    print("🧪 Testing Google Vision API fallback...")
    
    # Create test image
    test_image = create_test_image("FALLBACK TEST")
    
    try:
        # Test with invalid Google Vision config (should fallback)
        config = {
            'backend': 'google_vision',
            'google_vision_key_json': '{"invalid": "json"}',  # Invalid JSON
            'languages': ['en']
        }
        
        ocr_engine = OCREngine(config)
        
        print(f"   Available backends: {ocr_engine.get_available_backends()}")
        print(f"   Google Vision available: {ocr_engine.is_google_vision_available()}")
        print(f"   Tesseract available: {ocr_engine.is_tesseract_available()}")
        
        if not ocr_engine.is_tesseract_available():
            print("   ⚠️ Tesseract not available - cannot test fallback")
            return False
        
        # Try to extract text (should fallback to Tesseract)
        result = ocr_engine.extract_text(test_image)
        
        print(f"   Result: {result}")
        
        # Check if fallback occurred
        if result.get('fallback', False):
            print("   ✅ Fallback activated successfully!")
            print(f"   ✅ Fallback reason: {result.get('fallback_reason', 'Unknown')}")
            print(f"   ✅ Backend used: {result.get('backend', 'Unknown')}")
            return True
        else:
            print("   ❌ Fallback did not activate as expected")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed with error: {e}")
        return False
    finally:
        # Clean up
        Path(test_image).unlink(missing_ok=True)

def test_backend_availability():
    """Test backend availability detection"""
    print("🔍 Testing backend availability...")
    
    ocr_engine = OCREngine()
    
    # Test each backend
    backends = ['tesseract', 'easyocr', 'google_vision']
    for backend in backends:
        if backend == 'tesseract':
            available = ocr_engine.is_tesseract_available()
        elif backend == 'easyocr':
            available = ocr_engine.is_easyocr_available()
        elif backend == 'google_vision':
            available = ocr_engine.is_google_vision_available()
        
        status = "✅ Available" if available else "❌ Not available"
        print(f"   {backend.title()}: {status}")
        
        if available:
            try:
                backend_info = ocr_engine.get_active_backend_info(backend)
                print(f"      Status: {backend_info['status']}")
                print(f"      Priority: {backend_info['priority']}")
            except Exception as e:
                print(f"      Error getting info: {e}")

def test_preferred_backend_selection():
    """Test preferred backend selection logic"""
    print("⚡ Testing preferred backend selection...")
    
    ocr_engine = OCREngine()
    
    try:
        preferred = ocr_engine.get_preferred_backend()
        print(f"   Preferred backend: {preferred}")
        
        available_backends = ocr_engine.get_available_backends()
        print(f"   Available backends: {available_backends}")
        
        if preferred in available_backends:
            print("   ✅ Preferred backend is available")
            return True
        else:
            print("   ❌ Preferred backend is not in available list")
            return False
            
    except Exception as e:
        print(f"   ❌ Error getting preferred backend: {e}")
        return False

def test_google_vision_backend_direct():
    """Test Google Vision backend directly"""
    print("🚀 Testing Google Vision backend directly...")
    
    try:
        # Test with no credentials (should fail gracefully)
        backend = GoogleVisionBackend({})
        
        print(f"   Is available: {backend.is_available()}")
        
        if not backend.is_available():
            print("   ✅ Correctly detected as unavailable (no credentials)")
            
            # Test connection should fail gracefully
            result = backend.test_connection()
            print(f"   Test connection result: {result}")
            
            if not result.get('success', True):
                print("   ✅ Test connection correctly failed")
                return True
            else:
                print("   ❌ Test connection should have failed")
                return False
        else:
            print("   ℹ️ Google Vision is available (has credentials)")
            return True
            
    except Exception as e:
        print(f"   ❌ Error testing Google Vision backend: {e}")
        return False

def test_ocr_with_various_configs():
    """Test OCR with different configurations"""
    print("⚙️ Testing OCR with various configurations...")
    
    test_image = create_test_image("CONFIG TEST")
    
    configs = [
        {'backend': 'auto'},
        {'backend': 'tesseract'},
        {'backend': 'google_vision'},  # Should fallback if not configured
    ]
    
    results = []
    
    for i, config in enumerate(configs, 1):
        print(f"   Test {i}: {config}")
        
        try:
            ocr_engine = OCREngine(config)
            result = ocr_engine.extract_text(test_image)
            
            backend_used = result.get('backend', 'unknown')
            fallback_used = result.get('fallback', False)
            
            print(f"      Backend used: {backend_used}")
            print(f"      Fallback: {'Yes' if fallback_used else 'No'}")
            
            if fallback_used:
                print(f"      Fallback reason: {result.get('fallback_reason', 'Unknown')}")
            
            results.append(True)
            
        except Exception as e:
            print(f"      ❌ Error: {e}")
            results.append(False)
    
    # Clean up
    Path(test_image).unlink(missing_ok=True)
    
    success_count = sum(results)
    print(f"   Results: {success_count}/{len(configs)} configurations worked")
    
    return success_count > 0

def main():
    """Run all fallback system tests"""
    print("🔧 OCR Fallback System Test Suite")
    print("=" * 50)
    
    # Set up logging to see more details
    logging.basicConfig(level=logging.INFO)
    
    tests = [
        ("Backend Availability", test_backend_availability),
        ("Preferred Backend Selection", test_preferred_backend_selection),
        ("Google Vision Backend Direct", test_google_vision_backend_direct),
        ("Various Config Tests", test_ocr_with_various_configs),
        ("Google Vision Fallback", test_google_vision_fallback),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append(result)
            
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
            results.append(False)
    
    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The fallback system is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())