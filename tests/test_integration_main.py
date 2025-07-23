#!/usr/bin/env python3
"""
Integration tests for the main Universal Document Converter application
"""

import unittest
import sys
import subprocess
import json
import time
from pathlib import Path
from typing import List, Dict, Any

from .test_base import BaseTestCase, TestFileFactory, CustomAssertions
from .test_fixtures import DOCUMENT_TEMPLATES, create_test_environment


class MainApplicationIntegrationTest(BaseTestCase):
    """Integration tests for the main document converter"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.test_env = create_test_environment(Path("test_integration_env"))
        cls.app_path = Path(__file__).parent.parent / "universal_document_converter.py"
        
        # Verify main application exists
        if not cls.app_path.exists():
            raise FileNotFoundError(f"Main application not found at {cls.app_path}")
    
    def run_converter(self, args: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
        """Run the converter with given arguments"""
        cmd = [sys.executable, str(self.app_path)] + args
        
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
    
    def test_basic_text_conversion(self):
        """Test basic text file conversion"""
        # Create input file
        input_file = self.create_test_file("input.txt", "Hello, World!")
        output_file = self.temp_dir / "output.txt"
        
        # Run conversion
        result = self.run_converter([
            str(input_file),
            "-o", str(output_file),
            "-t", "txt"
        ])
        
        # Check results
        self.assertEqual(result.returncode, 0, f"Conversion failed: {result.stderr}")
        CustomAssertions.assertFileCreated(self, output_file)
        CustomAssertions.assertFileContains(self, output_file, "Hello, World!")
    
    def test_pdf_to_text_conversion(self):
        """Test PDF to text conversion"""
        # Create PDF file
        input_file = TestFileFactory.create_pdf_file(
            self.temp_dir / "test.pdf"
        )
        output_file = self.temp_dir / "output.txt"
        
        # Run conversion
        result = self.run_converter([
            str(input_file),
            "-o", str(output_file),
            "-t", "txt"
        ])
        
        # Check results
        self.assertEqual(result.returncode, 0, f"Conversion failed: {result.stderr}")
        CustomAssertions.assertFileCreated(self, output_file)
        
        # PDF should contain "Test PDF" text
        content = output_file.read_text()
        self.assertIn("Test", content.lower())
    
    def test_html_to_markdown_conversion(self):
        """Test HTML to Markdown conversion"""
        # Create HTML file
        input_file = TestFileFactory.create_html_file(
            self.temp_dir / "test.html"
        )
        output_file = self.temp_dir / "output.md"
        
        # Run conversion
        result = self.run_converter([
            str(input_file),
            "-o", str(output_file),
            "-t", "md"
        ])
        
        # Check results
        self.assertEqual(result.returncode, 0, f"Conversion failed: {result.stderr}")
        CustomAssertions.assertFileCreated(self, output_file)
        
        # Check markdown formatting
        content = output_file.read_text()
        self.assertIn("# Test Heading", content)
        self.assertIn("- Item 1", content)
    
    def test_batch_conversion(self):
        """Test batch file conversion"""
        # Create multiple input files
        input_files = []
        for i in range(5):
            file = self.create_test_file(f"file_{i}.txt", f"Content {i}")
            input_files.append(file)
        
        output_dir = self.temp_dir / "batch_output"
        output_dir.mkdir()
        
        # Run batch conversion
        result = self.run_converter([
            str(self.temp_dir),
            "-o", str(output_dir),
            "-t", "md",
            "--batch"
        ])
        
        # Check results
        self.assertEqual(result.returncode, 0, f"Batch conversion failed: {result.stderr}")
        
        # Verify all files were converted
        output_files = list(output_dir.glob("*.md"))
        self.assertEqual(len(output_files), 5)
    
    def test_ocr_functionality(self):
        """Test OCR functionality with image input"""
        # Create image with text
        input_file = TestFileFactory.create_image_file(
            self.temp_dir / "test_image.png"
        )
        output_file = self.temp_dir / "ocr_output.txt"
        
        # Run OCR conversion
        result = self.run_converter([
            str(input_file),
            "-o", str(output_file),
            "-t", "txt",
            "--ocr"
        ])
        
        # Check if OCR is available
        if "OCR functionality not available" in result.stderr:
            self.skipTest("OCR not available in test environment")
        
        # Check results
        self.assertEqual(result.returncode, 0, f"OCR conversion failed: {result.stderr}")
        CustomAssertions.assertFileCreated(self, output_file)
    
    def test_error_handling_invalid_input(self):
        """Test error handling for invalid input"""
        # Non-existent file
        result = self.run_converter([
            "/nonexistent/file.txt",
            "-o", "output.txt"
        ])
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())
    
    def test_error_handling_unsupported_format(self):
        """Test error handling for unsupported format"""
        # Create file with unsupported extension
        input_file = self.create_test_file("test.xyz", "Content")
        output_file = self.temp_dir / "output.txt"
        
        result = self.run_converter([
            str(input_file),
            "-o", str(output_file)
        ])
        
        # Should either convert as text or show unsupported format error
        if result.returncode != 0:
            self.assertIn("unsupported", result.stderr.lower())
    
    def test_unicode_content_handling(self):
        """Test Unicode content handling"""
        # Create file with Unicode content
        unicode_content = "Hello 世界! 🚀 Café naïve résumé"
        input_file = self.create_test_file("unicode.txt", unicode_content)
        output_file = self.temp_dir / "unicode_output.txt"
        
        # Run conversion
        result = self.run_converter([
            str(input_file),
            "-o", str(output_file),
            "-t", "txt"
        ])
        
        # Check results
        self.assertEqual(result.returncode, 0)
        CustomAssertions.assertFileContains(self, output_file, "世界")
        CustomAssertions.assertFileContains(self, output_file, "🚀")
    
    def test_large_file_handling(self):
        """Test handling of large files"""
        # Create 10MB file
        large_content = "x" * (10 * 1024 * 1024)
        input_file = self.create_test_file("large.txt", large_content)
        output_file = self.temp_dir / "large_output.txt"
        
        # Run conversion with timeout
        result = self.run_converter([
            str(input_file),
            "-o", str(output_file),
            "-t", "txt"
        ], timeout=60)
        
        # Check results
        self.assertEqual(result.returncode, 0)
        CustomAssertions.assertFileCreated(self, output_file)
        
        # Verify file size is reasonable
        output_size = output_file.stat().st_size
        self.assertGreater(output_size, 1024 * 1024)  # At least 1MB
    
    def test_concurrent_conversions(self):
        """Test concurrent file conversions"""
        import threading
        
        # Create test files
        files = []
        for i in range(10):
            file = self.create_test_file(f"concurrent_{i}.txt", f"Content {i}")
            files.append(file)
        
        results = []
        threads = []
        
        def convert_file(input_file, index):
            output_file = self.temp_dir / f"concurrent_output_{index}.txt"
            result = self.run_converter([
                str(input_file),
                "-o", str(output_file),
                "-t", "txt"
            ])
            results.append((index, result.returncode))
        
        # Start concurrent conversions
        for i, file in enumerate(files):
            thread = threading.Thread(target=convert_file, args=(file, i))
            thread.start()
            threads.append(thread)
        
        # Wait for all to complete
        for thread in threads:
            thread.join(timeout=30)
        
        # Check all succeeded
        for index, returncode in results:
            self.assertEqual(returncode, 0, f"Conversion {index} failed")
    
    def test_configuration_handling(self):
        """Test configuration file handling"""
        # Create config file
        config = {
            "max_file_size_mb": 50,
            "supported_formats": ["txt", "pdf", "html"],
            "output": {
                "default_format": "txt",
                "preserve_formatting": True
            }
        }
        
        config_file = self.temp_dir / "config.json"
        config_file.write_text(json.dumps(config))
        
        # Run with config
        input_file = self.create_test_file("test.txt", "Content")
        output_file = self.temp_dir / "output.txt"
        
        result = self.run_converter([
            str(input_file),
            "-o", str(output_file),
            "--config", str(config_file)
        ])
        
        # Should succeed with custom config
        self.assertEqual(result.returncode, 0)
    
    def test_progress_reporting(self):
        """Test progress reporting functionality"""
        # Create multiple files for batch processing
        for i in range(5):
            self.create_test_file(f"progress_{i}.txt", f"Content {i}")
        
        output_dir = self.temp_dir / "progress_output"
        output_dir.mkdir()
        
        # Run with verbose/progress flag
        result = self.run_converter([
            str(self.temp_dir),
            "-o", str(output_dir),
            "--batch",
            "--verbose"
        ])
        
        # Check for progress indicators in output
        self.assertEqual(result.returncode, 0)
        self.assertIn("Processing", result.stdout)
    
    def test_help_and_version(self):
        """Test help and version commands"""
        # Test help
        result = self.run_converter(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage", result.stdout.lower())
        
        # Test version
        result = self.run_converter(["--version"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("version", result.stdout.lower())


class GUIIntegrationTest(BaseTestCase):
    """Integration tests for GUI functionality"""
    
    def setUp(self):
        """Set up GUI test environment"""
        super().setUp()
        
        # Only run GUI tests if display is available
        try:
            import tkinter
            root = tkinter.Tk()
            root.destroy()
        except:
            self.skipTest("GUI not available in test environment")
    
    def test_gui_launch(self):
        """Test GUI application launch"""
        # Launch GUI in test mode
        cmd = [
            sys.executable,
            str(self.app_path),
            "--gui",
            "--test-mode"  # Hypothetical test mode that exits after launch
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # GUI should launch without errors
        self.assertIn("GUI", result.stdout, "GUI did not launch properly")


if __name__ == '__main__':
    unittest.main()