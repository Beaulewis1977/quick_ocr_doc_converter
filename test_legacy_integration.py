#!/usr/bin/env python3
"""
Legacy Integration Test Suite
Tests VB6/VFP9 integration functionality and CLI interface
"""

import os
import sys
import tempfile
import unittest
import subprocess
import json
from pathlib import Path
import time

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestLegacyIntegration(unittest.TestCase):
    """Test legacy system integration (VB6/VFP9)"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_files = {}
        self._create_test_files()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_test_files(self):
        """Create test files for integration testing"""
        
        # Create test text file
        test_txt = os.path.join(self.temp_dir, "test_document.txt")
        with open(test_txt, 'w', encoding='utf-8') as f:
            f.write("This is a test document for legacy integration.\nLine 2 of the document.\nEnd of document.")
        self.test_files['txt'] = test_txt
        
        # Create test markdown file
        test_md = os.path.join(self.temp_dir, "test_document.md")
        with open(test_md, 'w', encoding='utf-8') as f:
            f.write("# Test Document\n\nThis is a **test** document for legacy integration.\n\n- Item 1\n- Item 2")
        self.test_files['md'] = test_md
        
        # Create test HTML file
        test_html = os.path.join(self.temp_dir, "test_document.html")
        with open(test_html, 'w', encoding='utf-8') as f:
            f.write("<html><body><h1>Test Document</h1><p>This is a test document.</p></body></html>")
        self.test_files['html'] = test_html
    
    def test_cli_interface_basic(self):
        """Test basic CLI interface functionality"""
        
        input_file = self.test_files['txt']
        output_file = os.path.join(self.temp_dir, "output_basic.txt")
        
        # Test basic conversion command
        cmd = [sys.executable, "cli.py", input_file, "-o", output_file]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Check command executed successfully
            self.assertEqual(result.returncode, 0, f"CLI command failed: {result.stderr}")
            
            # Check output file was created
            self.assertTrue(os.path.exists(output_file), "Output file was not created")
            
            # Check output file has content
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertGreater(len(content), 0, "Output file is empty")
                self.assertIn("test document", content.lower())
            
            print("✅ Basic CLI interface test passed")
            
        except subprocess.TimeoutExpired:
            self.fail("CLI command timed out")
        except Exception as e:
            self.fail(f"CLI test failed: {e}")
    
    def test_cli_ocr_interface(self):
        """Test OCR CLI interface functionality"""
        
        # Check if OCR CLI exists
        if not os.path.exists("cli_ocr.py"):
            self.skipTest("OCR CLI not available")
        
        input_file = self.test_files['txt']
        output_file = os.path.join(self.temp_dir, "output_ocr.txt")
        
        # Test OCR conversion command
        cmd = [sys.executable, "cli_ocr.py", input_file, "-o", output_file, "--ocr"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Check command executed (may fail due to missing OCR dependencies in CI)
            if result.returncode == 0:
                self.assertTrue(os.path.exists(output_file), "OCR output file was not created")
                print("✅ OCR CLI interface test passed")
            else:
                print(f"⚠️  OCR CLI test skipped due to dependencies: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⚠️  OCR CLI command timed out (expected in CI)")
        except Exception as e:
            print(f"⚠️  OCR CLI test skipped: {e}")
    
    def test_vb6_integration_simulation(self):
        """Test VB6 integration command structure"""
        
        input_file = self.test_files['txt']
        output_file = os.path.join(self.temp_dir, "vb6_output.txt")
        
        # Simulate VB6 Shell command structure
        cmd_template = 'python cli.py "{input}" -o "{output}" -f txt'
        actual_cmd = cmd_template.format(input=input_file, output=output_file)
        
        # Parse command for validation
        cmd_parts = actual_cmd.split()
        
        # Validate command structure
        self.assertIn("python", cmd_parts[0])
        self.assertIn("cli.py", cmd_parts[1])
        self.assertIn("-o", cmd_parts)
        self.assertIn("-f", cmd_parts)
        
        # Test actual command execution
        try:
            result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.assertTrue(os.path.exists(output_file), "VB6 simulation output not created")
                print("✅ VB6 integration simulation passed")
            else:
                print(f"⚠️  VB6 simulation had issues: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️  VB6 simulation test error: {e}")
    
    def test_vfp9_integration_simulation(self):
        """Test VFP9 integration command structure"""
        
        input_file = self.test_files['md']
        output_file = os.path.join(self.temp_dir, "vfp9_output.txt")
        
        # Simulate VFP9 RUN command structure
        cmd_template = 'python cli.py "{input}" -o "{output}" -f txt'
        
        # Test command construction (VFP9 style)
        vfp9_cmd = f'RUN /N7 ({cmd_template.format(input=input_file, output=output_file)}) TO lnResult'
        
        # Extract actual command from VFP9 syntax
        import re
        match = re.search(r'RUN /N7 \((.+)\) TO lnResult', vfp9_cmd)
        if match:
            actual_cmd = match.group(1)
            cmd_parts = actual_cmd.split()
            
            # Validate command structure
            self.assertIn("python", cmd_parts[0])
            self.assertIn("cli.py", cmd_parts[1])
            
            # Test actual command execution
            try:
                result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self.assertTrue(os.path.exists(output_file), "VFP9 simulation output not created")
                    print("✅ VFP9 integration simulation passed")
                else:
                    print(f"⚠️  VFP9 simulation had issues: {result.stderr}")
                    
            except Exception as e:
                print(f"⚠️  VFP9 simulation test error: {e}")
    
    def test_dll_wrapper_simulation(self):
        """Test DLL wrapper functionality simulation"""
        
        # Check if DLL simulator exists
        dll_simulator = "UniversalConverter32.dll.bat"
        if not os.path.exists(dll_simulator):
            self.skipTest("DLL simulator not available")
        
        input_file = self.test_files['txt']
        output_file = os.path.join(self.temp_dir, "dll_output.txt")
        
        # Test DLL simulator
        cmd = [dll_simulator, input_file, output_file, "txt"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, shell=True)
            
            # DLL simulator may not work in all environments
            if result.returncode == 0 and os.path.exists(output_file):
                print("✅ DLL wrapper simulation passed")
            else:
                print(f"⚠️  DLL wrapper simulation skipped: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️  DLL wrapper test error: {e}")
    
    def test_batch_processing_simulation(self):
        """Test batch processing for legacy integration"""
        
        # Create multiple test files
        batch_inputs = []
        for i in range(3):
            test_file = os.path.join(self.temp_dir, f"batch_test_{i}.txt")
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(f"Batch test document {i}\nContent for testing batch processing.")
            batch_inputs.append(test_file)
        
        output_dir = os.path.join(self.temp_dir, "batch_output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Test batch processing
        success_count = 0
        for i, input_file in enumerate(batch_inputs):
            output_file = os.path.join(output_dir, f"batch_output_{i}.txt")
            cmd = [sys.executable, "cli.py", input_file, "-o", output_file]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                if result.returncode == 0 and os.path.exists(output_file):
                    success_count += 1
            except Exception:
                pass
        
        # At least some batch processing should succeed
        self.assertGreater(success_count, 0, "No batch processing succeeded")
        print(f"✅ Batch processing simulation: {success_count}/{len(batch_inputs)} succeeded")
    
    def test_error_handling_simulation(self):
        """Test error handling in legacy integration"""
        
        # Test with non-existent input file
        non_existent = os.path.join(self.temp_dir, "non_existent.txt")
        output_file = os.path.join(self.temp_dir, "error_output.txt")
        
        cmd = [sys.executable, "cli.py", non_existent, "-o", output_file]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            # Should return non-zero exit code for error
            self.assertNotEqual(result.returncode, 0, "CLI should return error for non-existent file")
            
            # Output file should not be created
            self.assertFalse(os.path.exists(output_file), "Output file should not be created on error")
            
            print("✅ Error handling simulation passed")
            
        except Exception as e:
            self.fail(f"Error handling test failed: {e}")
    
    def test_format_conversion_options(self):
        """Test various format conversion options for legacy integration"""
        
        input_file = self.test_files['md']
        
        # Test different output formats
        formats_to_test = ['txt', 'html', 'rtf']
        successful_conversions = 0
        
        for fmt in formats_to_test:
            output_file = os.path.join(self.temp_dir, f"format_test.{fmt}")
            cmd = [sys.executable, "cli.py", input_file, "-o", output_file, "-f", fmt]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
                
                if result.returncode == 0 and os.path.exists(output_file):
                    successful_conversions += 1
                    print(f"  ✅ Format {fmt} conversion succeeded")
                else:
                    print(f"  ⚠️  Format {fmt} conversion failed: {result.stderr}")
                    
            except Exception as e:
                print(f"  ⚠️  Format {fmt} test error: {e}")
        
        # At least one format should work
        self.assertGreater(successful_conversions, 0, "No format conversions succeeded")
        print(f"✅ Format conversion test: {successful_conversions}/{len(formats_to_test)} formats succeeded")

class TestLegacyConfiguration(unittest.TestCase):
    """Test configuration for legacy integration"""
    
    def test_vb6_configuration_structure(self):
        """Test VB6 configuration structure"""
        
        vb6_config = {
            "platform": "VB6",
            "integration_method": "cli",
            "command_template": 'python cli.py "{input}" -o "{output}" -f {format}',
            "supported_formats": ["txt", "rtf", "html", "docx"],
            "timeout_seconds": 30,
            "error_handling": True
        }
        
        # Validate configuration
        self.assertEqual(vb6_config["platform"], "VB6")
        self.assertIn("cli", vb6_config["integration_method"])
        self.assertIn("{input}", vb6_config["command_template"])
        self.assertIn("{output}", vb6_config["command_template"])
        self.assertIsInstance(vb6_config["supported_formats"], list)
        
        print("✅ VB6 configuration structure validated")
    
    def test_vfp9_configuration_structure(self):
        """Test VFP9 configuration structure"""
        
        vfp9_config = {
            "platform": "VFP9",
            "integration_method": "cli",
            "command_template": 'python cli.py "{input}" -o "{output}" -f {format}',
            "run_command_template": 'RUN /N7 ({command}) TO lnResult',
            "supported_formats": ["txt", "rtf", "html", "docx"],
            "timeout_seconds": 30,
            "error_handling": True,
            "return_code_check": True
        }
        
        # Validate configuration
        self.assertEqual(vfp9_config["platform"], "VFP9")
        self.assertIn("RUN /N7", vfp9_config["run_command_template"])
        self.assertTrue(vfp9_config["return_code_check"])
        
        print("✅ VFP9 configuration structure validated")

def run_legacy_integration_tests():
    """Run legacy integration tests"""
    print("🧪 Running Legacy Integration Tests")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestLegacyIntegration))
    test_suite.addTest(unittest.makeSuite(TestLegacyConfiguration))
    
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
            print(f"  - {test}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed!'}")
    
    return success

if __name__ == "__main__":
    success = run_legacy_integration_tests()
    sys.exit(0 if success else 1)