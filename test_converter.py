#!/usr/bin/env python3
"""
Test Suite for Universal Document Converter
Designed and built by Beau Lewis (blewisxx@gmail.com)
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from universal_document_converter import (
        FormatDetector, UniversalConverter,
        DocxReader, PdfReader, TxtReader, HtmlReader, RtfReader,
        MarkdownWriter, TxtWriter, HtmlWriter, RtfWriter
    )
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import converter modules: {e}")
    MODULES_AVAILABLE = False

class TestFormatDetector(unittest.TestCase):
    """Test the format detection functionality"""
    
    def setUp(self):
        """Set up test environment"""
        if not MODULES_AVAILABLE:
            self.skipTest("Converter modules not available")
    
    def test_format_detection(self):
        """Test automatic format detection"""
        test_cases = [
            ('document.docx', 'docx'),
            ('file.pdf', 'pdf'),
            ('text.txt', 'txt'),
            ('page.html', 'html'),
            ('page.htm', 'html'),
            ('rich.rtf', 'rtf'),
            ('unknown.xyz', None)
        ]
        
        for filename, expected in test_cases:
            with self.subTest(filename=filename):
                result = FormatDetector.detect_format(filename)
                self.assertEqual(result, expected)
    
    def test_format_lists(self):
        """Test format list generation"""
        input_formats = FormatDetector.get_input_format_list()
        output_formats = FormatDetector.get_output_format_list()
        
        # Check that we have expected formats
        self.assertGreater(len(input_formats), 0)
        self.assertGreater(len(output_formats), 0)
        
        # Check auto-detect is first in input formats
        self.assertEqual(input_formats[0][1], 'auto')

class TestConverters(unittest.TestCase):
    """Test the conversion functionality"""
    
    def setUp(self):
        """Set up test environment"""
        if not MODULES_AVAILABLE:
            self.skipTest("Converter modules not available")
        
        self.temp_dir = Path(tempfile.mkdtemp())
        self.converter = UniversalConverter()
    
    def tearDown(self):
        """Clean up test files"""
        if hasattr(self, 'temp_dir'):
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_txt_file(self, content="Test content\n\nSecond paragraph"):
        """Create a test text file"""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text(content, encoding='utf-8')
        return test_file
    
    def create_test_html_file(self, content="<html><body><h1>Test</h1><p>Content</p></body></html>"):
        """Create a test HTML file"""
        test_file = self.temp_dir / "test.html"
        test_file.write_text(content, encoding='utf-8')
        return test_file
    
    def test_txt_to_markdown(self):
        """Test TXT to Markdown conversion"""
        try:
            # Create test file
            test_file = self.create_test_txt_file()
            output_file = self.temp_dir / "output.md"
            
            # Convert
            self.converter.convert_file(test_file, output_file, 'txt', 'markdown')
            
            # Verify output exists and has content
            self.assertTrue(output_file.exists())
            content = output_file.read_text(encoding='utf-8')
            self.assertIn("Test content", content)
            
        except Exception as e:
            self.fail(f"TXT to Markdown conversion failed: {e}")
    
    def test_txt_to_html(self):
        """Test TXT to HTML conversion"""
        try:
            # Create test file
            test_file = self.create_test_txt_file()
            output_file = self.temp_dir / "output.html"
            
            # Convert
            self.converter.convert_file(test_file, output_file, 'txt', 'html')
            
            # Verify output
            self.assertTrue(output_file.exists())
            content = output_file.read_text(encoding='utf-8')
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("Test content", content)
            
        except Exception as e:
            self.fail(f"TXT to HTML conversion failed: {e}")
    
    def test_html_to_markdown(self):
        """Test HTML to Markdown conversion"""
        try:
            # Check if BeautifulSoup is available
            from bs4 import BeautifulSoup
            
            # Create test file
            test_file = self.create_test_html_file()
            output_file = self.temp_dir / "output.md"
            
            # Convert
            self.converter.convert_file(test_file, output_file, 'html', 'markdown')
            
            # Verify output
            self.assertTrue(output_file.exists())
            content = output_file.read_text(encoding='utf-8')
            self.assertIn("# Test", content)
            
        except ImportError:
            self.skipTest("BeautifulSoup4 not available")
        except Exception as e:
            self.fail(f"HTML to Markdown conversion failed: {e}")
    
    def test_auto_format_detection(self):
        """Test automatic format detection during conversion"""
        try:
            # Create test file
            test_file = self.create_test_txt_file()
            output_file = self.temp_dir / "output.md"
            
            # Convert with auto-detection
            self.converter.convert_file(test_file, output_file, 'auto', 'markdown')
            
            # Verify output
            self.assertTrue(output_file.exists())
            
        except Exception as e:
            self.fail(f"Auto-detection conversion failed: {e}")
    
    def test_unsupported_format(self):
        """Test handling of unsupported formats"""
        test_file = self.temp_dir / "test.xyz"
        test_file.write_text("content")
        output_file = self.temp_dir / "output.md"
        
        with self.assertRaises(ValueError):
            self.converter.convert_file(test_file, output_file, 'auto', 'markdown')

class TestPerformance(unittest.TestCase):
    """Test conversion performance"""
    
    def setUp(self):
        """Set up performance test environment"""
        if not MODULES_AVAILABLE:
            self.skipTest("Converter modules not available")
    
    def test_large_text_file_performance(self):
        """Test performance with large text files"""
        import time
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create a large test file (1MB of text)
            large_content = "Test line with some content.\n" * 50000  # ~1MB
            test_file = temp_path / "large_test.txt"
            test_file.write_text(large_content, encoding='utf-8')
            
            output_file = temp_path / "large_output.md"
            converter = UniversalConverter()
            
            # Time the conversion
            start_time = time.time()
            converter.convert_file(test_file, output_file, 'txt', 'markdown')
            end_time = time.time()
            
            # Verify it completed in reasonable time (should be very fast)
            conversion_time = end_time - start_time
            self.assertLess(conversion_time, 5.0, "Conversion took too long (>5 seconds)")
            
            # Verify output exists and has content
            self.assertTrue(output_file.exists())
            self.assertGreater(output_file.stat().st_size, 100000)  # Should be substantial

def run_dependency_check():
    """Check and report on dependency availability"""
    print("🔍 Dependency Check Report")
    print("=" * 50)
    
    dependencies = {
        'python-docx': 'docx',
        'PyPDF2': 'PyPDF2',
        'beautifulsoup4': 'bs4',
        'striprtf': 'striprtf',
        'tkinterdnd2': 'tkinterdnd2'
    }
    
    available = []
    missing = []
    
    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
            available.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} (pip install {package})")
    
    print(f"\n📊 Summary: {len(available)}/{len(dependencies)} dependencies available")
    
    if missing:
        print(f"\n📦 To install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        return False
    else:
        print("\n🎉 All dependencies are available!")
        return True

def run_format_compatibility_test():
    """Test format compatibility matrix"""
    if not MODULES_AVAILABLE:
        print("❌ Cannot run compatibility test - modules not available")
        return
    
    print("\n🔄 Format Compatibility Test")
    print("=" * 50)
    
    input_formats = ['txt', 'html']  # Safe formats we can test
    output_formats = ['markdown', 'txt', 'html', 'rtf']
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = UniversalConverter()
        
        # Create test files
        test_files = {
            'txt': temp_path / "test.txt",
            'html': temp_path / "test.html"
        }
        
        test_files['txt'].write_text("Test content\n\nSecond paragraph", encoding='utf-8')
        test_files['html'].write_text("<html><body><h1>Test</h1><p>Content</p></body></html>", encoding='utf-8')
        
        compatibility_matrix = {}
        
        for input_fmt in input_formats:
            compatibility_matrix[input_fmt] = {}
            for output_fmt in output_formats:
                try:
                    output_file = temp_path / f"test_{input_fmt}_to_{output_fmt}.{output_fmt}"
                    converter.convert_file(test_files[input_fmt], output_file, input_fmt, output_fmt)
                    
                    if output_file.exists() and output_file.stat().st_size > 0:
                        compatibility_matrix[input_fmt][output_fmt] = "✅"
                    else:
                        compatibility_matrix[input_fmt][output_fmt] = "❌"
                        
                except Exception as e:
                    compatibility_matrix[input_fmt][output_fmt] = "❌"
    
    # Print compatibility matrix
    print(f"{'Format':<8} {'→MD':<4} {'→TXT':<5} {'→HTML':<6} {'→RTF':<5}")
    print("-" * 32)
    
    for input_fmt in input_formats:
        row = f"{input_fmt.upper():<8}"
        for output_fmt in output_formats:
            status = compatibility_matrix[input_fmt].get(output_fmt, "❌")
            if output_fmt == 'markdown':
                row += f" {status:<4}"
            elif output_fmt == 'txt':
                row += f" {status:<5}"
            elif output_fmt == 'html':
                row += f" {status:<6}"
            elif output_fmt == 'rtf':
                row += f" {status:<5}"
        print(row)

def main():
    """Run all tests and checks"""
    print("🚀 Universal Document Converter Test Suite")
    print("Designed and built by Beau Lewis (blewisxx@gmail.com)")
    print("=" * 60)
    
    # 1. Dependency check
    deps_ok = run_dependency_check()
    
    # 2. Format compatibility test
    run_format_compatibility_test()
    
    # 3. Unit tests
    if MODULES_AVAILABLE:
        print("\n🧪 Running Unit Tests")
        print("=" * 50)
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Add test cases
        suite.addTest(loader.loadTestsFromTestCase(TestFormatDetector))
        suite.addTest(loader.loadTestsFromTestCase(TestConverters))
        suite.addTest(loader.loadTestsFromTestCase(TestPerformance))
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Summary
        print(f"\n📊 Test Results Summary")
        print(f"   Tests run: {result.testsRun}")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
        print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0:.1f}%")
        
        if result.wasSuccessful():
            print("🎉 All tests passed!")
        else:
            print("❌ Some tests failed. Check output above for details.")
            
        return result.wasSuccessful()
    else:
        print("\n❌ Skipping unit tests - modules not available")
        return deps_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 