#!/usr/bin/env python3
"""
Comprehensive OCR Integration Test Suite
Tests all aspects of the OCR functionality in the Universal Document Converter
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
import json
from PIL import Image
import numpy as np

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ocr_engine.ocr_engine import OCREngine
from ocr_engine.ocr_integration import OCRIntegration
from ocr_engine.format_detector import OCRFormatDetector
from ocr_engine.image_processor import ImageProcessor

class TestOCREngine(unittest.TestCase):
    """Test the core OCR engine functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.ocr_engine = OCREngine()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_engine_initialization(self):
        """Test OCR engine initialization"""
        self.assertIsNotNone(self.ocr_engine)
        self.assertTrue(hasattr(self.ocr_engine, 'extract_text'))
        
    def test_text_extraction_from_image(self):
        """Test text extraction from a simple image"""
        # Create a simple test image with text
        img = Image.new('RGB', (200, 50), color='white')
        
        # Save test image
        test_image_path = os.path.join(self.temp_dir, 'test_text.png')
        img.save(test_image_path)
        
        # Test extraction (should return empty string for blank image)
        result = self.ocr_engine.extract_text(test_image_path)
        self.assertIsInstance(result, str)
        
    def test_unsupported_format_handling(self):
        """Test handling of unsupported formats"""
        # Create an invalid file
        invalid_file = os.path.join(self.temp_dir, 'invalid.xyz')
        with open(invalid_file, 'w') as f:
            f.write('not an image')
            
        result = self.ocr_engine.extract_text(invalid_file)
        self.assertEqual(result, "")

class TestOCRIntegration(unittest.TestCase):
    """Test the OCR integration layer"""
    
    def setUp(self):
        """Set up test environment"""
        self.ocr_integration = OCRIntegration()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_integration_initialization(self):
        """Test OCR integration initialization"""
        self.assertIsNotNone(self.ocr_integration)
        self.assertTrue(hasattr(self.ocr_integration, 'process_file'))
        
    def test_supported_formats(self):
        """Test supported format detection"""
        supported_formats = ['jpg', 'jpeg', 'png', 'tiff', 'tif', 'bmp', 'gif', 'webp', 'pdf']
        
        for fmt in supported_formats:
            test_file = os.path.join(self.temp_dir, f'test.{fmt}')
            # Create minimal valid file for testing
            if fmt == 'pdf':
                with open(test_file, 'w') as f:
                    f.write('%PDF-1.4\n%%EOF')
            else:
                img = Image.new('RGB', (10, 10), color='white')
                img.save(test_file)
                
            # Test that format is detected
            detector = OCRFormatDetector()
            self.assertTrue(detector.is_ocr_format(test_file))

class TestFormatDetector(unittest.TestCase):
    """Test the format detection functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.detector = OCRFormatDetector()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_image_format_detection(self):
        """Test image format detection"""
        formats_to_test = ['jpg', 'png', 'tiff', 'bmp', 'gif', 'webp']
        
        for fmt in formats_to_test:
            test_file = os.path.join(self.temp_dir, f'test.{fmt}')
            img = Image.new('RGB', (10, 10), color='white')
            img.save(test_file)
            
            self.assertTrue(self.detector.is_ocr_format(test_file))
            
    def test_document_format_detection(self):
        """Test document format detection"""
        doc_formats = ['docx', 'txt', 'html', 'rtf', 'epub']
        
        for fmt in doc_formats:
            test_file = os.path.join(self.temp_dir, f'test.{fmt}')
            with open(test_file, 'w') as f:
                f.write('test content')
                
            self.assertFalse(self.detector.is_ocr_format(test_file))
            
    def test_nonexistent_file(self):
        """Test handling of nonexistent files"""
        nonexistent = os.path.join(self.temp_dir, 'nonexistent.jpg')
        self.assertFalse(self.detector.is_ocr_format(nonexistent))

class TestImageProcessor(unittest.TestCase):
    """Test the image processing functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.processor = ImageProcessor()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_image_preprocessing(self):
        """Test image preprocessing pipeline"""
        # Create test image
        img = Image.new('RGB', (100, 100), color='white')
        test_image = os.path.join(self.temp_dir, 'test_preprocess.png')
        img.save(test_image)
        
        # Test preprocessing
        processed = self.processor.preprocess_image(test_image)
        self.assertIsNotNone(processed)
        
    def test_image_enhancement(self):
        """Test image enhancement features"""
        # Create test image
        img_array = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        test_image = os.path.join(self.temp_dir, 'test_enhance.png')
        img.save(test_image)
        
        # Test enhancement
        enhanced = self.processor.enhance_image(test_image)
        self.assertIsNotNone(enhanced)

class TestConfiguration(unittest.TestCase):
    """Test configuration and settings"""
    
    def test_config_file_creation(self):
        """Test configuration file creation"""
        config_path = os.path.join(tempfile.mkdtemp(), 'test_config.json')
        test_config = {
            "ocr_enabled": True,
            "ocr_language": "eng",
            "batch_size": 5,
            "max_workers": 4
        }
        
        with open(config_path, 'w') as f:
            json.dump(test_config, f, indent=2)
            
        self.assertTrue(os.path.exists(config_path))
        
        # Test loading
        with open(config_path, 'r') as f:
            loaded_config = json.load(f)
            
        self.assertEqual(loaded_config["ocr_enabled"], True)
        self.assertEqual(loaded_config["ocr_language"], "eng")

class TestBatchProcessing(unittest.TestCase):
    """Test batch processing functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.ocr_integration = OCRIntegration()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_batch_processing(self):
        """Test processing multiple files"""
        # Create test images
        test_files = []
        for i in range(3):
            img = Image.new('RGB', (50, 20), color='white')
            test_file = os.path.join(self.temp_dir, f'test_{i}.png')
            img.save(test_file)
            test_files.append(test_file)
            
        # Test batch processing
        results = self.ocr_integration.process_batch(test_files)
        self.assertEqual(len(results), len(test_files))
        
        for result in results:
            self.assertIsInstance(result, str)

class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.ocr_integration = OCRIntegration()
        
    def test_corrupted_image_handling(self):
        """Test handling of corrupted images"""
        # Create corrupted image file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            f.write(b'This is not a valid PNG file')
            corrupted_file = f.name
            
        try:
            result = self.ocr_integration.process_file(corrupted_file)
            self.assertIsInstance(result, str)
        finally:
            os.unlink(corrupted_file)
            
    def test_empty_file_handling(self):
        """Test handling of empty files"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            empty_file = f.name
            
        try:
            result = self.ocr_integration.process_file(empty_file)
            self.assertIsInstance(result, str)
        finally:
            os.unlink(empty_file)

def create_test_suite():
    """Create comprehensive test suite"""
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTest(unittest.makeSuite(TestOCREngine))
    suite.addTest(unittest.makeSuite(TestOCRIntegration))
    suite.addTest(unittest.makeSuite(TestFormatDetector))
    suite.addTest(unittest.makeSuite(TestImageProcessor))
    suite.addTest(unittest.makeSuite(TestConfiguration))
    suite.addTest(unittest.makeSuite(TestBatchProcessing))
    suite.addTest(unittest.makeSuite(TestErrorHandling))
    
    return suite

def run_tests():
    """Run all tests and generate report"""
    print("=" * 60)
    print("OCR Integration Test Suite")
    print("=" * 60)
    
    # Create test suite
    suite = create_test_suite()
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
            
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
            
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)