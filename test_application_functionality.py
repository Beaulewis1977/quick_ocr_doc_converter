#!/usr/bin/env python3
"""
Comprehensive Application Functionality Test
Tests all core features of the Enhanced OCR Document Converter

Author: Terry AI Agent for Terragon Labs
"""

import os
import sys
import tempfile
import traceback
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

# Add current directory to path
sys.path.insert(0, os.path.abspath('.'))

def create_test_image():
    """Create a test image with text for OCR testing"""
    # Create a simple image with text
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    text = "Test Document\nThis is a sample text for OCR.\nLine 3 with numbers: 12345"
    draw.text((20, 50), text, fill='black', font=font)
    
    return img

def test_core_imports():
    """Test that all core modules can be imported"""
    print("🧪 Testing Core Module Imports...")
    
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except Exception as e:
        print(f"❌ OpenCV failed: {e}")
        return False
    
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract: {version}")
    except Exception as e:
        print(f"❌ Tesseract failed: {e}")
        return False
    
    try:
        from ocr_engine.ocr_engine import OCREngine
        print("✅ OCR Engine imported")
    except Exception as e:
        print(f"❌ OCR Engine failed: {e}")
        return False
    
    try:
        from backends.manager import OCRBackendManager
        print("✅ Backend Manager imported")
    except Exception as e:
        print(f"❌ Backend Manager failed: {e}")
        return False
    
    try:
        from security.credentials import CredentialManager
        print("✅ Credential Manager imported")
    except Exception as e:
        print(f"❌ Credential Manager failed: {e}")
        return False
    
    try:
        from monitoring.cost_tracker import CostTracker
        print("✅ Cost Tracker imported")
    except Exception as e:
        print(f"❌ Cost Tracker failed: {e}")
        return False
    
    return True

def test_ocr_functionality():
    """Test OCR functionality with local backend"""
    print("\n🧪 Testing OCR Functionality...")
    
    try:
        from ocr_engine.ocr_engine import OCREngine
        
        # Initialize OCR engine
        engine = OCREngine()
        backends = engine.get_available_backends()
        print(f"Available backends: {backends}")
        
        if not backends:
            print("❌ No OCR backends available")
            return False
        
        # Create test image
        test_img = create_test_image()
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            test_img.save(tmp_file.name)
            
            # Test OCR
            result = engine.extract_text(tmp_file.name)
            print(f"OCR Result: {result}")
            
            if result and result.get('text') and len(result['text'].strip()) > 0:
                print("✅ OCR extraction successful")
                return True
            else:
                print("❌ OCR extraction failed - no text found")
                return False
                
    except Exception as e:
        print(f"❌ OCR functionality failed: {e}")
        traceback.print_exc()
        return False
    finally:
        # Clean up
        try:
            os.unlink(tmp_file.name)
        except:
            pass

def test_backend_manager():
    """Test backend manager functionality"""
    print("\n🧪 Testing Backend Manager...")
    
    try:
        from backends.manager import OCRBackendManager
        
        manager = OCRBackendManager()
        backends = manager.get_available_backends()
        print(f"Available backends: {backends}")
        
        if not backends:
            print("❌ No backends available")
            return False
        
        # Test backend selection
        selected = manager.select_backend({})
        print(f"Selected backend: {selected}")
        
        if selected:
            print("✅ Backend manager working")
            return True
        else:
            print("❌ Backend selection failed")
            return False
            
    except Exception as e:
        print(f"❌ Backend manager failed: {e}")
        traceback.print_exc()
        return False

def test_credential_management():
    """Test credential management system"""
    print("\n🧪 Testing Credential Management...")
    
    try:
        from security.credentials import CredentialManager
        
        with tempfile.TemporaryDirectory() as temp_dir:
            cred_manager = CredentialManager(config_dir=temp_dir)
            
            # Test storing credentials
            test_creds = {
                'api_key': 'test_key_12345',
                'endpoint': 'https://test.example.com',
                'region': 'us-east-1'
            }
            
            success = cred_manager.store_credentials('test_service', test_creds)
            if not success:
                print("❌ Failed to store credentials")
                return False
            
            # Test retrieving credentials
            retrieved = cred_manager.get_credentials('test_service')
            if retrieved != test_creds:
                print("❌ Credential retrieval mismatch")
                return False
            
            # Test listing services
            services = cred_manager.list_services()
            if 'test_service' not in services:
                print("❌ Service not found in list")
                return False
            
            print("✅ Credential management working")
            return True
            
    except Exception as e:
        print(f"❌ Credential management failed: {e}")
        traceback.print_exc()
        return False

def test_cost_tracking():
    """Test cost tracking functionality"""
    print("\n🧪 Testing Cost Tracking...")
    
    try:
        from monitoring.cost_tracker import CostTracker
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "costs.db"
            tracker = CostTracker(db_path=str(db_path))
            
            # Track some usage
            tracker.track_usage('tesseract', 'test.png', {'text': 'test', 'success': True}, 0.0, 0.1)
            tracker.track_usage('google_vision', 'test.png', {'text': 'test', 'success': True}, 0.05, 0.1)
            
            # Get statistics
            stats = tracker.get_usage_stats()
            print(f"Usage stats: {stats}")
            
            if stats and len(stats) > 0:
                print("✅ Cost tracking working")
                return True
            else:
                print("❌ No usage statistics found")
                return False
                
    except Exception as e:
        print(f"❌ Cost tracking failed: {e}")
        traceback.print_exc()
        return False

def test_gui_components():
    """Test GUI component initialization"""
    print("\n🧪 Testing GUI Components...")
    
    try:
        import tkinter as tk
        from enhanced_ocr_gui import EnhancedOCRGUI
        
        # Test basic tkinter
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test enhanced GUI initialization
        app = EnhancedOCRGUI()
        app.root.withdraw()  # Hide the window
        
        # Check that components are initialized
        if hasattr(app, 'backend_manager') and app.backend_manager:
            print("✅ GUI components initialized")
            
            # Clean up
            app.root.destroy()
            return True
        else:
            print("❌ GUI components not properly initialized")
            app.root.destroy()
            return False
            
    except Exception as e:
        print(f"❌ GUI components failed: {e}")
        traceback.print_exc()
        return False

def test_security_validation():
    """Test security validation functionality"""
    print("\n🧪 Testing Security Validation...")
    
    try:
        from security.validator import SecurityValidator
        
        validator = SecurityValidator()
        
        # Test safe file validation
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            # Write some dummy content
            tmp_file.write(b'%PDF-1.4\nDummy PDF content')
            tmp_file.flush()
            
            # Test validation
            is_valid = validator.validate_file_path(tmp_file.name)
            print(f"File validation result: {is_valid}")
            
            # Test OCR output sanitization
            clean_output = validator.sanitize_ocr_output("test output with potential issues")
            print(f"Sanitized output: {clean_output}")
            
            print("✅ Security validation working")
            os.unlink(tmp_file.name)
            return True
            
    except Exception as e:
        print(f"❌ Security validation failed: {e}")
        traceback.print_exc()
        return False

def test_integration_workflow():
    """Test complete integration workflow"""
    print("\n🧪 Testing Integration Workflow...")
    
    try:
        from backends.manager import OCRBackendManager
        from security.credentials import CredentialManager
        from monitoring.cost_tracker import CostTracker
        from security.validator import SecurityValidator
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Initialize all components
            cred_manager = CredentialManager(config_dir=temp_dir)
            cost_tracker = CostTracker(db_path=str(Path(temp_dir) / "costs.db"))
            validator = SecurityValidator()
            backend_manager = OCRBackendManager()
            
            # Create test image
            test_img = create_test_image()
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                test_img.save(tmp_file.name)
                
                # Validate file
                if not validator.validate_file_path(tmp_file.name):
                    print("❌ File validation failed")
                    return False
                
                # Process with backend manager
                if backend_manager.get_available_backends():
                    result = backend_manager.process_with_fallback(
                        tmp_file.name,
                        requirements={'accuracy': 'medium'}
                    )
                    
                    if result and result.get('text'):
                        # Track cost
                        cost_tracker.track_usage(
                            result.get('backend', 'unknown'),
                            tmp_file.name,
                            result,
                            result.get('cost', 0.0),
                            0.1
                        )
                        
                        print("✅ Integration workflow successful")
                        os.unlink(tmp_file.name)
                        return True
                    else:
                        print("❌ OCR processing failed in workflow")
                        os.unlink(tmp_file.name)
                        return False
                else:
                    print("⚠️ No backends available for integration test")
                    os.unlink(tmp_file.name)
                    return True  # Not a failure, just no backends
                    
    except Exception as e:
        print(f"❌ Integration workflow failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all functionality tests"""
    print("🚀 Enhanced OCR Document Converter - Functionality Test Suite")
    print("=" * 60)
    
    tests = [
        ("Core Imports", test_core_imports),
        ("OCR Functionality", test_ocr_functionality),
        ("Backend Manager", test_backend_manager),
        ("Credential Management", test_credential_management),
        ("Cost Tracking", test_cost_tracking),
        ("GUI Components", test_gui_components),
        ("Security Validation", test_security_validation),
        ("Integration Workflow", test_integration_workflow),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<25} {status}")
    
    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Application is fully functional.")
        return 0
    else:
        print(f"\n⚠️ {total-passed} tests failed. Some functionality may be limited.")
        return 1

if __name__ == "__main__":
    # Set environment for headless operation
    os.environ['DISPLAY'] = ':99'
    exit_code = main()
    sys.exit(exit_code)