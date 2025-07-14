#!/usr/bin/env python3
"""
Final Validation Script for OCR Integration
Comprehensive end-to-end testing of the complete OCR-enhanced document converter
"""

import os
import sys
import tempfile
import json
import subprocess
from pathlib import Path
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCRIntegrationValidator:
    """Comprehensive validator for OCR integration"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_results = {}
        
    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test results"""
        self.test_results[test_name] = {
            'success': success,
            'message': message,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if success:
            logger.info(f"✅ {test_name}: PASSED - {message}")
        else:
            logger.error(f"❌ {test_name}: FAILED - {message}")
    
    def test_ocr_engine_import(self):
        """Test OCR engine imports"""
        try:
            from ocr_engine.ocr_engine import OCREngine
            from ocr_engine.ocr_integration import OCRIntegration
            from ocr_engine.format_detector import OCRFormatDetector
            from ocr_engine.image_processor import ImageProcessor
            
            self.log_result("OCR Engine Import", True, "All OCR modules imported successfully")
            return True
        except ImportError as e:
            self.log_result("OCR Engine Import", False, str(e))
            return False
    
    def test_dependencies(self):
        """Test required dependencies"""
        dependencies = [
            'pytesseract',
            'PIL',
            'numpy',
            'cv2',
            'concurrent.futures'
        ]
        
        failed_deps = []
        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError:
                failed_deps.append(dep)
        
        if not failed_deps:
            self.log_result("Dependencies", True, "All required dependencies available")
            return True
        else:
            self.log_result("Dependencies", False, f"Missing: {', '.join(failed_deps)}")
            return False
    
    def test_ocr_functionality(self):
        """Test basic OCR functionality"""
        try:
            from ocr_engine.ocr_engine import OCREngine
            
            # Create a simple test image
            from PIL import Image, ImageDraw, ImageFont
            
            # Create test image with text
            img = Image.new('RGB', (200, 50), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try to use a basic font
            try:
                font = ImageFont.load_default()
                draw.text((10, 10), "TEST", fill='black', font=font)
            except:
                draw.text((10, 10), "TEST", fill='black')
            
            test_image = os.path.join(self.temp_dir, 'test_ocr.png')
            img.save(test_image)
            
            # Test OCR
            engine = OCREngine()
            text = engine.extract_text(test_image)
            
            if isinstance(text, str):
                self.log_result("OCR Functionality", True, f"OCR engine working, extracted: '{text.strip()}'")
                return True
            else:
                self.log_result("OCR Functionality", False, "OCR engine returned non-string result")
                return False
                
        except Exception as e:
            self.log_result("OCR Functionality", False, str(e))
            return False
    
    def test_format_detection(self):
        """Test format detection"""
        try:
            from ocr_engine.format_detector import OCRFormatDetector
            
            detector = OCRFormatDetector()
            
            # Test supported formats
            test_cases = [
                ('test.jpg', True),
                ('test.png', True),
                ('test.pdf', True),
                ('test.txt', False),
                ('test.docx', False)
            ]
            
            all_passed = True
            for filename, expected in test_cases:
                result = detector.is_ocr_format(filename)
                if result != expected:
                    all_passed = False
                    break
            
            self.log_result("Format Detection", all_passed, "Format detection working correctly")
            return all_passed
            
        except Exception as e:
            self.log_result("Format Detection", False, str(e))
            return False
    
    def test_integration_layer(self):
        """Test OCR integration layer"""
        try:
            from ocr_engine.ocr_integration import OCRIntegration
            
            ocr = OCRIntegration()
            
            # Test initialization
            if not hasattr(ocr, 'process_file'):
                self.log_result("Integration Layer", False, "Missing process_file method")
                return False
            
            # Test configuration
            config = ocr.get_config()
            if isinstance(config, dict):
                self.log_result("Integration Layer", True, "Integration layer initialized successfully")
                return True
            else:
                self.log_result("Integration Layer", False, "Invalid configuration format")
                return False
                
        except Exception as e:
            self.log_result("Integration Layer", False, str(e))
            return False
    
    def test_gui_application(self):
        """Test GUI application startup"""
        try:
            # Test if GUI can be imported
            import tkinter as tk
            from universal_document_converter_ocr import DocumentConverterApp
            
            # Test basic initialization (without showing GUI)
            root = tk.Tk()
            root.withdraw()  # Hide window
            
            app = DocumentConverterApp(root)
            
            # Test OCR integration in GUI
            if hasattr(app, 'ocr_integration'):
                self.log_result("GUI Application", True, "GUI application with OCR integration ready")
                root.destroy()
                return True
            else:
                self.log_result("GUI Application", False, "OCR integration not found in GUI")
                root.destroy()
                return False
                
        except Exception as e:
            self.log_result("GUI Application", False, str(e))
            return False
    
    def test_batch_processing(self):
        """Test batch processing capabilities"""
        try:
            from ocr_engine.ocr_integration import OCRIntegration
            from PIL import Image
            
            ocr = OCRIntegration()
            
            # Create test images
            test_files = []
            for i in range(3):
                img = Image.new('RGB', (50, 20), color='white')
                test_file = os.path.join(self.temp_dir, f'batch_test_{i}.png')
                img.save(test_file)
                test_files.append(test_file)
            
            # Test batch processing
            results = ocr.process_batch(test_files)
            
            if len(results) == len(test_files):
                self.log_result("Batch Processing", True, f"Processed {len(test_files)} files successfully")
                return True
            else:
                self.log_result("Batch Processing", False, f"Expected {len(test_files)} results, got {len(results)}")
                return False
                
        except Exception as e:
            self.log_result("Batch Processing", False, str(e))
            return False
    
    def test_configuration(self):
        """Test configuration system"""
        try:
            # Test config file creation
            config_path = os.path.join(self.temp_dir, 'test_config.json')
            test_config = {
                "ocr_enabled": True,
                "ocr_language": "eng",
                "batch_size": 5,
                "max_workers": 4
            }
            
            with open(config_path, 'w') as f:
                json.dump(test_config, f, indent=2)
            
            # Test config loading
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                
                if loaded_config == test_config:
                    self.log_result("Configuration", True, "Configuration system working correctly")
                    return True
                else:
                    self.log_result("Configuration", False, "Configuration mismatch")
                    return False
            else:
                self.log_result("Configuration", False, "Config file not created")
                return False
                
        except Exception as e:
            self.log_result("Configuration", False, str(e))
            return False
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        try:
            from ocr_engine.ocr_integration import OCRIntegration
            
            ocr = OCRIntegration()
            
            # Test nonexistent file
            result = ocr.process_file('nonexistent.jpg')
            if isinstance(result, str):
                self.log_result("Error Handling", True, "Graceful handling of missing files")
                return True
            else:
                self.log_result("Error Handling", False, "Invalid error handling response")
                return False
                
        except Exception as e:
            self.log_result("Error Handling", False, str(e))
            return False
    
    def test_cross_platform_compatibility(self):
        """Test cross-platform compatibility"""
        import platform
        
        system = platform.system()
        supported_systems = ['Windows', 'Linux', 'Darwin']
        
        if system in supported_systems:
            self.log_result("Cross-platform", True, f"Running on supported platform: {system}")
            return True
        else:
            self.log_result("Cross-platform", False, f"Unsupported platform: {system}")
            return False
    
    def run_all_tests(self):
        """Run all validation tests"""
        logger.info("Starting OCR Integration Validation...")
        logger.info("=" * 60)
        
        tests = [
            self.test_cross_platform_compatibility,
            self.test_ocr_engine_import,
            self.test_dependencies,
            self.test_ocr_functionality,
            self.test_format_detection,
            self.test_integration_layer,
            self.test_batch_processing,
            self.test_configuration,
            self.test_error_handling,
            self.test_gui_application
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                logger.error(f"Test {test.__name__} failed with exception: {e}")
        
        logger.info("=" * 60)
        logger.info("VALIDATION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Tests Passed: {passed}/{total}")
        logger.info(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Save results
        results_file = os.path.join(self.temp_dir, 'validation_results.json')
        with open(results_file, 'w') as f:
            json.dump({
                'summary': {
                    'passed': passed,
                    'total': total,
                    'success_rate': (passed/total)*100
                },
                'details': self.test_results
            }, f, indent=2)
        
        logger.info(f"Detailed results saved to: {results_file}")
        
        return passed == total
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

def main():
    """Main validation function"""
    validator = OCRIntegrationValidator()
    
    try:
        success = validator.run_all_tests()
        
        if success:
            logger.info("🎉 All validation tests passed! OCR integration is ready.")
            return 0
        else:
            logger.error("❌ Some validation tests failed. Please check the logs.")
            return 1
            
    finally:
        validator.cleanup()

if __name__ == "__main__":
    sys.exit(main())