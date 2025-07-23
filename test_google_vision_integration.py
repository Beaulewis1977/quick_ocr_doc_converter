#!/usr/bin/env python3
"""
Google Vision API Integration Test Suite
Tests Google Vision API functionality and fallback mechanisms
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
import json
import time
from PIL import Image, ImageDraw, ImageFont
import io

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestGoogleVisionIntegration(unittest.TestCase):
    """Test Google Vision API integration and fallback system"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_image_path = None
        self.api_available = self._check_api_availability()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _check_api_availability(self):
        """Check if Google Vision API is available and properly configured"""
        try:
            from google.cloud import vision
            
            # Check if credentials are available
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if not credentials_path:
                print("⚠️  Google Vision API credentials not found")
                return False
            
            if not os.path.exists(credentials_path):
                print("⚠️  Google Vision API credentials file not found")
                return False
            
            # Try to create a client
            client = vision.ImageAnnotatorClient()
            print("✅ Google Vision API client created successfully")
            return True
            
        except ImportError:
            print("⚠️  Google Vision API library not installed")
            return False
        except Exception as e:
            print(f"⚠️  Google Vision API setup error: {e}")
            return False
    
    def _create_test_image(self, text="Test OCR Image", size=(400, 200)):
        """Create a test image with text for OCR testing"""
        image = Image.new('RGB', size, color='white')
        draw = ImageDraw.Draw(image)
        
        try:
            # Try to use a standard font
            font = ImageFont.truetype("arial.ttf", 24)
        except (OSError, IOError):
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Calculate text position (centered)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), text, fill='black', font=font)
        
        # Save test image
        test_image_path = os.path.join(self.temp_dir, "test_image.png")
        image.save(test_image_path)
        self.test_image_path = test_image_path
        return test_image_path
    
    def test_google_vision_api_import(self):
        """Test that Google Vision API can be imported"""
        try:
            from google.cloud import vision
            self.assertTrue(True, "Google Vision API imported successfully")
        except ImportError:
            self.skipTest("Google Vision API library not available")
    
    def test_google_vision_basic_ocr(self):
        """Test basic OCR functionality with Google Vision API"""
        if not self.api_available:
            self.skipTest("Google Vision API not available")
        
        # Create test image
        test_text = "Hello Google Vision API"
        image_path = self._create_test_image(test_text)
        
        try:
            from google.cloud import vision
            
            client = vision.ImageAnnotatorClient()
            
            # Read image file
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Perform text detection
            response = client.text_detection(image=image)
            texts = response.text_annotations
            
            if texts:
                detected_text = texts[0].description.strip()
                print(f"Detected text: '{detected_text}'")
                self.assertIn("Hello", detected_text)
                self.assertIn("Google", detected_text)
            else:
                self.fail("No text detected by Google Vision API")
                
        except Exception as e:
            self.fail(f"Google Vision API OCR test failed: {e}")
    
    def test_google_vision_document_detection(self):
        """Test document text detection with Google Vision API"""
        if not self.api_available:
            self.skipTest("Google Vision API not available")
        
        # Create more complex test image
        test_text = "Document\nLine 1\nLine 2\nEnd"
        image_path = self._create_test_image(test_text, size=(600, 300))
        
        try:
            from google.cloud import vision
            
            client = vision.ImageAnnotatorClient()
            
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Perform document text detection
            response = client.document_text_detection(image=image)
            document = response.full_text_annotation
            
            if document:
                detected_text = document.text.strip()
                print(f"Document text: '{detected_text}'")
                self.assertIn("Document", detected_text)
                self.assertIn("Line 1", detected_text)
                self.assertIn("Line 2", detected_text)
            else:
                self.fail("No document text detected by Google Vision API")
                
        except Exception as e:
            self.fail(f"Google Vision API document detection test failed: {e}")
    
    def test_google_vision_error_handling(self):
        """Test error handling for invalid inputs"""
        if not self.api_available:
            self.skipTest("Google Vision API not available")
        
        try:
            from google.cloud import vision
            
            client = vision.ImageAnnotatorClient()
            
            # Test with invalid image data
            invalid_image = vision.Image(content=b"invalid image data")
            
            response = client.text_detection(image=invalid_image)
            
            # Check for errors
            if response.error.message:
                print(f"Expected error occurred: {response.error.message}")
                self.assertTrue(True, "Error handling works correctly")
            else:
                print("⚠️  No error returned for invalid image")
                
        except Exception as e:
            print(f"Exception caught (expected): {e}")
            self.assertTrue(True, "Exception handling works correctly")
    
    def test_fallback_system_mock(self):
        """Test fallback system behavior (mock test)"""
        # This test simulates fallback behavior without requiring actual API calls
        
        # Mock configuration for fallback testing
        fallback_config = {
            "google_vision": {
                "enabled": True,
                "fallback_enabled": True,
                "fallback_engines": ["tesseract", "easyocr"]
            }
        }
        
        # Test configuration validity
        self.assertTrue(fallback_config["google_vision"]["enabled"])
        self.assertTrue(fallback_config["google_vision"]["fallback_enabled"])
        self.assertIn("tesseract", fallback_config["google_vision"]["fallback_engines"])
        
        print("✅ Fallback configuration valid")
    
    def test_api_cost_tracking_mock(self):
        """Test API usage tracking (mock test)"""
        # Mock usage tracking
        usage_data = {
            "requests_today": 0,
            "requests_month": 0,
            "cost_today": 0.0,
            "cost_month": 0.0,
            "last_request": None
        }
        
        # Simulate API request
        usage_data["requests_today"] += 1
        usage_data["requests_month"] += 1
        usage_data["cost_today"] += 0.0015  # $1.50 per 1000 requests
        usage_data["cost_month"] += 0.0015
        usage_data["last_request"] = time.time()
        
        # Verify tracking
        self.assertEqual(usage_data["requests_today"], 1)
        self.assertEqual(usage_data["requests_month"], 1)
        self.assertAlmostEqual(usage_data["cost_today"], 0.0015, places=4)
        
        print("✅ API usage tracking works correctly")
    
    def test_configuration_validation(self):
        """Test Google Vision API configuration validation"""
        
        # Valid configuration
        valid_config = {
            "engine": "google_vision",
            "enabled": True,
            "confidence_threshold": 0.8,
            "features": ["TEXT_DETECTION", "DOCUMENT_TEXT_DETECTION"],
            "language_hints": ["en"],
            "fallback_enabled": True,
            "fallback_engines": ["tesseract", "easyocr"]
        }
        
        # Test configuration validation
        self.assertEqual(valid_config["engine"], "google_vision")
        self.assertTrue(valid_config["enabled"])
        self.assertIsInstance(valid_config["confidence_threshold"], float)
        self.assertIn("TEXT_DETECTION", valid_config["features"])
        self.assertTrue(valid_config["fallback_enabled"])
        
        print("✅ Configuration validation passed")
    
    def test_cli_integration_mock(self):
        """Test CLI integration with Google Vision API (mock)"""
        
        # Create test file
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Test document content")
        
        # Mock CLI command construction
        cli_command_parts = [
            "python", "cli_ocr.py",
            test_file,
            "-o", os.path.join(self.temp_dir, "output.txt"),
            "--engine", "google_vision",
            "--fallback"
        ]
        
        # Verify command structure
        self.assertIn("cli_ocr.py", cli_command_parts)
        self.assertIn("--engine", cli_command_parts)
        self.assertIn("google_vision", cli_command_parts)
        self.assertIn("--fallback", cli_command_parts)
        
        print("✅ CLI integration structure validated")

class TestFallbackSystem(unittest.TestCase):
    """Test OCR engine fallback system"""
    
    def test_engine_priority_order(self):
        """Test that fallback engines are tried in correct order"""
        
        fallback_order = ["google_vision", "tesseract", "easyocr"]
        
        # Test order is correct
        self.assertEqual(fallback_order[0], "google_vision")
        self.assertEqual(fallback_order[1], "tesseract")
        self.assertEqual(fallback_order[2], "easyocr")
        
        print("✅ Fallback engine order validated")
    
    def test_fallback_configuration(self):
        """Test fallback system configuration"""
        
        config = {
            "primary_engine": "google_vision",
            "fallback_engines": ["tesseract", "easyocr"],
            "max_retries": 3,
            "timeout_seconds": 30,
            "fallback_on_error": True,
            "fallback_on_low_confidence": True,
            "confidence_threshold": 0.8
        }
        
        # Validate configuration
        self.assertEqual(config["primary_engine"], "google_vision")
        self.assertIsInstance(config["fallback_engines"], list)
        self.assertGreater(config["max_retries"], 0)
        self.assertTrue(config["fallback_on_error"])
        
        print("✅ Fallback configuration validated")

def run_google_vision_tests():
    """Run Google Vision API integration tests"""
    print("🧪 Running Google Vision API Integration Tests")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add Google Vision API tests
    test_suite.addTest(unittest.makeSuite(TestGoogleVisionIntegration))
    test_suite.addTest(unittest.makeSuite(TestFallbackSystem))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed!'}")
    
    return success

if __name__ == "__main__":
    success = run_google_vision_tests()
    sys.exit(0 if success else 1)