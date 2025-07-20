#!/usr/bin/env python3
"""
Implementation validation script for Enhanced OCR System

Validates that all components are properly implemented and can be imported.
This script runs without external dependencies.

Author: Terry AI Agent for Terragon Labs
"""

import sys
import os
from pathlib import Path
import traceback
import tempfile


def validate_imports():
    """Validate that all modules can be imported"""
    print("🔍 Validating module imports...")
    
    modules_to_test = [
        'security.validator',
        'security.credentials', 
        'backends.base',
        'backends.google_vision',
        'backends.aws_textract',
        'backends.azure_vision',
        'backends.manager',
        'monitoring.cost_tracker'
    ]
    
    success_count = 0
    total_count = len(modules_to_test)
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
            success_count += 1
        except ImportError as e:
            print(f"  ❌ {module_name}: {e}")
        except Exception as e:
            print(f"  ⚠️  {module_name}: {e}")
    
    print(f"\nImport Results: {success_count}/{total_count} modules imported successfully")
    return success_count == total_count


def validate_security_components():
    """Validate security components"""
    print("\n🔒 Validating security components...")
    
    try:
        from security import SecurityValidator, CredentialManager
        
        # Test SecurityValidator
        validator = SecurityValidator()
        print("  ✅ SecurityValidator initialized")
        
        # Test basic validation (should pass)
        test_patterns = validator.get_pii_patterns()
        print(f"  ✅ PII patterns loaded: {len(test_patterns)} patterns")
        
        # Test CredentialManager
        with tempfile.TemporaryDirectory() as temp_dir:
            cred_manager = CredentialManager(config_dir=temp_dir)
            print("  ✅ CredentialManager initialized")
            
            # Test storing and retrieving credentials
            test_creds = {"test_key": "test_value"}
            success = cred_manager.store_credentials("test_service", test_creds)
            if success:
                retrieved = cred_manager.get_credentials("test_service")
                if retrieved == test_creds:
                    print("  ✅ Credential storage and retrieval working")
                else:
                    print("  ❌ Credential retrieval mismatch")
                    return False
            else:
                print("  ❌ Credential storage failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Security validation failed: {e}")
        traceback.print_exc()
        return False


def validate_backend_components():
    """Validate backend components"""
    print("\n🚀 Validating backend components...")
    
    try:
        from backends import OCRBackendManager
        
        # Test backend manager initialization
        manager = OCRBackendManager()
        print("  ✅ OCRBackendManager initialized")
        
        # Test backend status
        status = manager.get_backend_status()
        print(f"  ✅ Backend status retrieved: {len(status)} backends")
        
        # Test available backends
        available = manager.get_available_backends()
        print(f"  ✅ Available backends: {available}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Backend validation failed: {e}")
        traceback.print_exc()
        return False


def validate_monitoring_components():
    """Validate monitoring components"""
    print("\n📊 Validating monitoring components...")
    
    try:
        from monitoring import CostTracker, UsageRecord
        from datetime import datetime
        
        # Test CostTracker
        with tempfile.TemporaryDirectory() as temp_dir:
            tracker = CostTracker(db_path=str(Path(temp_dir) / "test_costs.db"))
            print("  ✅ CostTracker initialized")
            
            # Test usage tracking
            test_result = {
                'text': 'Test OCR result',
                'confidence': 90.0,
                'success': True,
                'duration': 1.5
            }
            
            tracker.track_usage(
                backend='local',
                image_path='/test/image.png',
                result=test_result,
                cost=0.0
            )
            print("  ✅ Usage tracking working")
            
            # Test statistics
            stats = tracker.get_usage_stats(30)
            print(f"  ✅ Usage statistics retrieved: {stats['total_stats']['total_requests']} requests")
            
            # Test recommendations
            recommendations = tracker.get_cost_optimization_recommendations()
            print(f"  ✅ Cost recommendations: {len(recommendations)} recommendations")
        
        # Test UsageRecord
        record = UsageRecord(
            timestamp=datetime.now(),
            backend='test',
            image_path='/test/path.png',
            image_size_mb=1.0,
            processing_time=1.0,
            cost=0.001,
            success=True,
            confidence=90.0,
            character_count=100
        )
        
        record_dict = record.to_dict()
        print("  ✅ UsageRecord creation and serialization working")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Monitoring validation failed: {e}")
        traceback.print_exc()
        return False


def validate_gui_components():
    """Validate GUI components (optional)"""
    print("\n🖥️  Validating GUI components...")
    
    try:
        # Try to import GUI without actually creating windows
        import enhanced_ocr_gui
        print("  ✅ Enhanced OCR GUI module available")
        return True
        
    except ImportError as e:
        print(f"  ⚠️  GUI components not available: {e}")
        print("     (This is acceptable - GUI may have additional dependencies)")
        return True  # GUI is optional
    except Exception as e:
        print(f"  ❌ GUI validation failed: {e}")
        return False


def validate_file_structure():
    """Validate that all expected files exist"""
    print("\n📁 Validating file structure...")
    
    expected_files = [
        'security/__init__.py',
        'security/validator.py',
        'security/credentials.py',
        'backends/__init__.py',
        'backends/base.py',
        'backends/google_vision.py',
        'backends/aws_textract.py',
        'backends/azure_vision.py',
        'backends/manager.py',
        'monitoring/__init__.py',
        'monitoring/cost_tracker.py',
        'enhanced_ocr_gui.py',
        'tests/__init__.py',
        'tests/conftest.py',
        'tests/test_security.py',
        'tests/test_backends.py',
        'tests/test_cost_tracking.py',
        'tests/test_gui.py',
        'tests/test_integration.py',
        'run_tests.py'
    ]
    
    missing_files = []
    present_files = 0
    
    for file_path in expected_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
            present_files += 1
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    print(f"\nFile Structure: {present_files}/{len(expected_files)} files present")
    
    if missing_files:
        print(f"Missing files: {missing_files}")
        return False
    
    return True


def main():
    """Main validation function"""
    print("🚀 Enhanced OCR System Implementation Validation")
    print("=" * 60)
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    validation_results = []
    
    # Run all validations
    validation_results.append(("File Structure", validate_file_structure()))
    validation_results.append(("Module Imports", validate_imports()))
    validation_results.append(("Security Components", validate_security_components()))
    validation_results.append(("Backend Components", validate_backend_components()))
    validation_results.append(("Monitoring Components", validate_monitoring_components()))
    validation_results.append(("GUI Components", validate_gui_components()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 VALIDATION SUMMARY")
    print("=" * 60)
    
    total_passed = 0
    total_tests = len(validation_results)
    
    for test_name, result in validation_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            total_passed += 1
    
    print("-" * 60)
    print(f"Overall Result: {total_passed}/{total_tests} validations passed")
    
    if total_passed == total_tests:
        print("\n🎉 All validations passed! Implementation is ready for testing.")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} validations failed. Please check the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())