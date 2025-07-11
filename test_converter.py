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
import shutil
import time
from typing import Dict, List, Any

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

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def setUp(self):
        """Set up test environment"""
        if not MODULES_AVAILABLE:
            self.skipTest("Converter modules not available")

        self.temp_dir = Path(tempfile.mkdtemp())
        self.converter = UniversalConverter()

    def tearDown(self):
        """Clean up test files"""
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_empty_file(self):
        """Test conversion of empty files"""
        empty_file = self.temp_dir / "empty.txt"
        empty_file.write_text("", encoding='utf-8')
        output_file = self.temp_dir / "empty_output.md"

        # Should not raise an error
        self.converter.convert_file(empty_file, output_file, 'txt', 'markdown')
        self.assertTrue(output_file.exists())

    def test_whitespace_only_file(self):
        """Test conversion of files with only whitespace"""
        whitespace_file = self.temp_dir / "whitespace.txt"
        whitespace_file.write_text("   \n\n  \t  \n", encoding='utf-8')
        output_file = self.temp_dir / "whitespace_output.md"

        self.converter.convert_file(whitespace_file, output_file, 'txt', 'markdown')
        self.assertTrue(output_file.exists())

    def test_very_long_lines(self):
        """Test conversion of files with very long lines"""
        long_line = "A" * 10000  # 10KB line
        long_file = self.temp_dir / "long.txt"
        long_file.write_text(long_line, encoding='utf-8')
        output_file = self.temp_dir / "long_output.md"

        self.converter.convert_file(long_file, output_file, 'txt', 'markdown')
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn("A" * 100, content)  # Check partial content

    def test_unicode_content(self):
        """Test conversion of files with Unicode characters"""
        unicode_content = "Hello 世界! 🚀 Café naïve résumé"
        unicode_file = self.temp_dir / "unicode.txt"
        unicode_file.write_text(unicode_content, encoding='utf-8')
        output_file = self.temp_dir / "unicode_output.md"

        self.converter.convert_file(unicode_file, output_file, 'txt', 'markdown')
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn("世界", content)
        self.assertIn("🚀", content)
        self.assertIn("naïve", content)

    def test_special_characters_html(self):
        """Test HTML conversion with special characters"""
        html_content = '<html><body><p>&lt;script&gt;alert("test")&lt;/script&gt;</p></body></html>'
        html_file = self.temp_dir / "special.html"
        html_file.write_text(html_content, encoding='utf-8')
        output_file = self.temp_dir / "special_output.md"

        try:
            self.converter.convert_file(html_file, output_file, 'html', 'markdown')
            self.assertTrue(output_file.exists())
            content = output_file.read_text(encoding='utf-8')
            self.assertIn("script", content)
        except ImportError:
            self.skipTest("BeautifulSoup4 not available")

    def test_nonexistent_input_file(self):
        """Test handling of nonexistent input files"""
        nonexistent_file = self.temp_dir / "nonexistent.txt"
        output_file = self.temp_dir / "output.md"

        with self.assertRaises((FileNotFoundError, OSError)):
            self.converter.convert_file(nonexistent_file, output_file, 'txt', 'markdown')

    def test_invalid_output_directory(self):
        """Test handling of invalid output directories"""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("content", encoding='utf-8')

        # Try to write to a file as if it were a directory
        invalid_output = self.temp_dir / "test.txt" / "output.md"

        with self.assertRaises((FileNotFoundError, OSError, PermissionError)):
            self.converter.convert_file(test_file, invalid_output, 'txt', 'markdown')

    def test_case_insensitive_extensions(self):
        """Test case-insensitive file extension detection"""
        test_cases = [
            ('test.TXT', 'txt'),
            ('test.HTML', 'html'),
            ('test.Docx', 'docx'),
            ('test.PDF', 'pdf'),
            ('test.RTF', 'rtf')
        ]

        for filename, expected_format in test_cases:
            with self.subTest(filename=filename):
                detected = FormatDetector.detect_format(filename)
                self.assertEqual(detected, expected_format)

class TestReaderWriterClasses(unittest.TestCase):
    """Test individual reader and writer classes"""

    def setUp(self):
        """Set up test environment"""
        if not MODULES_AVAILABLE:
            self.skipTest("Converter modules not available")

        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test files"""
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_txt_reader_encoding_fallback(self):
        """Test TXT reader encoding fallback mechanism"""
        # Create file with Latin-1 encoding
        latin1_content = "Café naïve résumé"
        latin1_file = self.temp_dir / "latin1.txt"

        with open(latin1_file, 'w', encoding='latin-1') as f:
            f.write(latin1_content)

        reader = TxtReader()
        content = reader.read(latin1_file)

        self.assertIsInstance(content, list)
        self.assertGreater(len(content), 0)
        # Should contain the text (possibly with encoding differences)
        text_content = ' '.join([item[1] for item in content if item[0] == 'paragraph'])
        self.assertIn("Caf", text_content)  # Partial match to handle encoding differences

    def test_html_reader_malformed_html(self):
        """Test HTML reader with malformed HTML"""
        try:
            malformed_html = "<html><body><h1>Unclosed heading<p>Paragraph without closing"
            html_file = self.temp_dir / "malformed.html"
            html_file.write_text(malformed_html, encoding='utf-8')

            reader = HtmlReader()
            content = reader.read(html_file)

            self.assertIsInstance(content, list)
            # BeautifulSoup should handle malformed HTML gracefully

        except ImportError:
            self.skipTest("BeautifulSoup4 not available")

    def test_markdown_writer_heading_levels(self):
        """Test Markdown writer with different heading levels"""
        test_content = [
            ('heading', 1, 'Main Title'),
            ('heading', 2, 'Subtitle'),
            ('heading', 3, 'Sub-subtitle'),
            ('paragraph', 'Some content'),
            ('heading', 6, 'Deep heading')
        ]

        output_file = self.temp_dir / "headings.md"
        writer = MarkdownWriter()
        writer.write(test_content, output_file)

        content = output_file.read_text(encoding='utf-8')
        self.assertIn("# Main Title", content)
        self.assertIn("## Subtitle", content)
        self.assertIn("### Sub-subtitle", content)
        self.assertIn("###### Deep heading", content)
        self.assertIn("Some content", content)

    def test_html_writer_escaping(self):
        """Test HTML writer character escaping"""
        test_content = [
            ('paragraph', 'Text with <script>alert("xss")</script> & "quotes"'),
            ('heading', 1, 'Title with & ampersand')
        ]

        output_file = self.temp_dir / "escaped.html"
        writer = HtmlWriter()
        writer.write(test_content, output_file)

        content = output_file.read_text(encoding='utf-8')
        self.assertIn("&lt;script&gt;", content)
        self.assertIn("&amp;", content)
        self.assertIn("&quot;", content)
        self.assertNotIn("<script>", content)  # Should be escaped

    def test_rtf_writer_escaping(self):
        """Test RTF writer character escaping"""
        test_content = [
            ('paragraph', 'Text with {braces} and \\backslashes'),
            ('heading', 1, 'Title with special chars')
        ]

        output_file = self.temp_dir / "escaped.rtf"
        writer = RtfWriter()
        writer.write(test_content, output_file)

        content = output_file.read_text(encoding='utf-8')
        self.assertIn("\\{braces\\}", content)
        self.assertIn("\\\\backslashes", content)
        self.assertIn("{\\rtf1", content)  # RTF header

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

class TestErrorHandling(unittest.TestCase):
    """Test comprehensive error handling scenarios"""

    def setUp(self):
        """Set up test environment"""
        if not MODULES_AVAILABLE:
            self.skipTest("Converter modules not available")

        self.temp_dir = Path(tempfile.mkdtemp())
        self.converter = UniversalConverter()

    def tearDown(self):
        """Clean up test files"""
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_invalid_input_format(self):
        """Test handling of invalid input format specification"""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("content", encoding='utf-8')
        output_file = self.temp_dir / "output.md"

        with self.assertRaises(ValueError):
            self.converter.convert_file(test_file, output_file, 'invalid_format', 'markdown')

    def test_invalid_output_format(self):
        """Test handling of invalid output format specification"""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("content", encoding='utf-8')
        output_file = self.temp_dir / "output.invalid"

        with self.assertRaises(ValueError):
            self.converter.convert_file(test_file, output_file, 'txt', 'invalid_format')

    def test_corrupted_file_handling(self):
        """Test handling of corrupted or binary files as text"""
        # Create a file with binary content
        binary_file = self.temp_dir / "binary.txt"
        with open(binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\xFF\xFE\xFD')

        output_file = self.temp_dir / "binary_output.md"

        # Should handle gracefully or raise appropriate exception
        try:
            self.converter.convert_file(binary_file, output_file, 'txt', 'markdown')
            # If it succeeds, output should exist
            self.assertTrue(output_file.exists())
        except (UnicodeDecodeError, Exception):
            # If it fails, that's also acceptable for binary content
            pass

    def test_permission_denied_output(self):
        """Test handling of permission denied on output file"""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("content", encoding='utf-8')

        # Try to write to a directory that doesn't exist (more reliable cross-platform)
        nonexistent_dir = self.temp_dir / "nonexistent" / "deep" / "path"
        output_file = nonexistent_dir / "output.md"

        # This should raise an error because the directory doesn't exist
        # and we're not creating it
        with self.assertRaises((FileNotFoundError, OSError, PermissionError)):
            self.converter.convert_file(test_file, output_file, 'txt', 'markdown')

    def test_path_objects_vs_strings(self):
        """Test that both Path objects and strings work as input"""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("content", encoding='utf-8')

        # Test with Path objects
        output_file1 = self.temp_dir / "output1.md"
        self.converter.convert_file(test_file, output_file1, 'txt', 'markdown')
        self.assertTrue(output_file1.exists())

        # Test with strings
        output_file2 = self.temp_dir / "output2.md"
        self.converter.convert_file(str(test_file), str(output_file2), 'txt', 'markdown')
        self.assertTrue(output_file2.exists())

class TestFormatSpecificFeatures(unittest.TestCase):
    """Test format-specific features and edge cases"""

    def setUp(self):
        """Set up test environment"""
        if not MODULES_AVAILABLE:
            self.skipTest("Converter modules not available")

        self.temp_dir = Path(tempfile.mkdtemp())
        self.converter = UniversalConverter()

    def tearDown(self):
        """Clean up test files"""
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_html_with_nested_elements(self):
        """Test HTML with deeply nested elements"""
        try:
            nested_html = """
            <html>
            <body>
                <div>
                    <section>
                        <article>
                            <h1>Main Title</h1>
                            <div>
                                <p>Nested paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
                                <ul>
                                    <li>List item 1</li>
                                    <li>List item 2</li>
                                </ul>
                            </div>
                        </article>
                    </section>
                </div>
            </body>
            </html>
            """

            html_file = self.temp_dir / "nested.html"
            html_file.write_text(nested_html, encoding='utf-8')
            output_file = self.temp_dir / "nested_output.md"

            self.converter.convert_file(html_file, output_file, 'html', 'markdown')
            self.assertTrue(output_file.exists())

            content = output_file.read_text(encoding='utf-8')
            self.assertIn("# Main Title", content)
            self.assertIn("Nested paragraph", content)

        except ImportError:
            self.skipTest("BeautifulSoup4 not available")

    def test_multiple_paragraph_formats(self):
        """Test text with various paragraph separations"""
        text_content = """First paragraph.

Second paragraph after double newline.


Third paragraph after triple newline.

    Indented paragraph.

Final paragraph."""

        txt_file = self.temp_dir / "paragraphs.txt"
        txt_file.write_text(text_content, encoding='utf-8')
        output_file = self.temp_dir / "paragraphs_output.md"

        self.converter.convert_file(txt_file, output_file, 'txt', 'markdown')
        self.assertTrue(output_file.exists())

        content = output_file.read_text(encoding='utf-8')
        self.assertIn("First paragraph", content)
        self.assertIn("Second paragraph", content)
        self.assertIn("Indented paragraph", content)

    def test_output_format_extensions(self):
        """Test that output files get correct extensions"""
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("content", encoding='utf-8')

        format_extensions = {
            'markdown': '.md',
            'txt': '.txt',
            'html': '.html',
            'rtf': '.rtf'
        }

        for output_format, expected_ext in format_extensions.items():
            with self.subTest(format=output_format):
                output_file = self.temp_dir / f"test_output{expected_ext}"
                self.converter.convert_file(test_file, output_file, 'txt', output_format)
                self.assertTrue(output_file.exists())

                # Verify content is appropriate for format
                content = output_file.read_text(encoding='utf-8')
                if output_format == 'html':
                    self.assertIn('<!DOCTYPE html>', content)
                elif output_format == 'rtf':
                    self.assertIn('{\\rtf1', content)

class TestLoggingAndErrorHandling(unittest.TestCase):
    """TDD: Test-driven development for enhanced logging and error handling"""

    def setUp(self):
        """Set up test environment"""
        if not MODULES_AVAILABLE:
            self.skipTest("Converter modules not available")

        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up test files"""
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_logger_initialization(self):
        """Test that logger can be initialized and configured"""
        # This test will fail until we implement ConverterLogger
        try:
            from universal_document_converter import ConverterLogger
            logger_instance = ConverterLogger("TestLogger")
            logger = logger_instance.get_logger()

            self.assertIsNotNone(logger)
            self.assertEqual(logger.name, "TestLogger")
            self.assertTrue(len(logger.handlers) > 0)
        except ImportError:
            self.fail("ConverterLogger not implemented yet")

    def test_custom_exceptions_exist(self):
        """Test that custom exception classes are defined"""
        try:
            from universal_document_converter import (
                DocumentConverterError, UnsupportedFormatError,
                FileProcessingError, DependencyError
            )

            # Test exception hierarchy
            self.assertTrue(issubclass(UnsupportedFormatError, DocumentConverterError))
            self.assertTrue(issubclass(FileProcessingError, DocumentConverterError))
            self.assertTrue(issubclass(DependencyError, DocumentConverterError))

            # Test exceptions can be raised and caught
            with self.assertRaises(UnsupportedFormatError):
                raise UnsupportedFormatError("Test unsupported format")

        except ImportError:
            self.fail("Custom exception classes not implemented yet")

    def test_enhanced_error_messages(self):
        """Test that error messages are informative and user-friendly"""
        converter = UniversalConverter()

        # Test unsupported format error message
        test_file = self.temp_dir / "test.unknown"
        test_file.write_text("content")
        output_file = self.temp_dir / "output.md"

        try:
            converter.convert_file(test_file, output_file, 'auto', 'markdown')
            self.fail("Should have raised an exception for unsupported format")
        except Exception as e:
            # Error message should be informative
            error_msg = str(e).lower()
            self.assertTrue(
                any(word in error_msg for word in ['unsupported', 'format', 'unknown']),
                f"Error message not informative enough: {e}"
            )

    def test_file_processing_error_handling(self):
        """Test handling of file processing errors with proper logging"""
        # Create a file that will cause processing errors
        problematic_file = self.temp_dir / "problematic.txt"

        # Write binary content to a .txt file to cause encoding issues
        with open(problematic_file, 'wb') as f:
            f.write(b'\x00\x01\x02\xFF\xFE\xFD')

        output_file = self.temp_dir / "output.md"
        converter = UniversalConverter()

        # Should handle gracefully and provide useful error info
        try:
            converter.convert_file(problematic_file, output_file, 'txt', 'markdown')
        except Exception as e:
            # Error should be informative about the encoding issue
            error_msg = str(e).lower()
            self.assertTrue(
                any(word in error_msg for word in ['encoding', 'decode', 'file']),
                f"Error message should mention encoding issue: {e}"
            )

    def test_dependency_error_handling(self):
        """Test handling of missing dependencies"""
        # This test verifies that missing dependencies are handled gracefully
        # We'll test this by temporarily making a dependency unavailable

        # For now, just test that the dependency check mechanism exists
        try:
            from universal_document_converter import UniversalDocumentConverterGUI

            # Create a mock root for testing
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Hide the window

            try:
                gui = UniversalDocumentConverterGUI(root)
                # Should have a method to check dependencies
                self.assertTrue(hasattr(gui, 'check_dependencies'))

                # Should handle missing dependencies gracefully
                # (This is more of an integration test)

            finally:
                root.destroy()

        except Exception as e:
            self.fail(f"Dependency checking not properly implemented: {e}")

    def test_logging_levels_and_formatting(self):
        """Test that different log levels work and formatting is appropriate"""
        try:
            from universal_document_converter import ConverterLogger

            logger_instance = ConverterLogger("TestFormatter")
            logger = logger_instance.get_logger()

            # Test that we can log at different levels
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            # If we get here without errors, logging is working
            self.assertTrue(True)

        except ImportError:
            self.fail("Enhanced logging not implemented yet")

    def test_error_context_preservation(self):
        """Test that error context (stack traces, file info) is preserved"""
        converter = UniversalConverter()

        # Create a scenario that will fail
        nonexistent_file = self.temp_dir / "nonexistent.txt"
        output_file = self.temp_dir / "output.md"

        try:
            converter.convert_file(nonexistent_file, output_file, 'txt', 'markdown')
            self.fail("Should have raised an exception for nonexistent file")
        except Exception as e:
            # Error should preserve useful context
            error_msg = str(e)
            self.assertIn("nonexistent.txt", error_msg)

class TestGUIImprovements(unittest.TestCase):
    """TDD: Test-driven development for GUI improvements and responsiveness"""

    def setUp(self):
        """Set up test environment"""
        if not MODULES_AVAILABLE:
            self.skipTest("Converter modules not available")

        # Create a test root window
        import tkinter as tk
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing

    def tearDown(self):
        """Clean up test environment"""
        if hasattr(self, 'root'):
            self.root.destroy()

    def test_modern_styling_applied(self):
        """Test that modern styling is applied to GUI elements"""
        try:
            from universal_document_converter import UniversalDocumentConverterGUI

            gui = UniversalDocumentConverterGUI(self.root)

            # Test that GUI has modern styling attributes
            self.assertTrue(hasattr(gui, 'apply_modern_styling'))

            # Test that color scheme is defined
            self.assertTrue(hasattr(gui, 'color_scheme'))
            self.assertIsInstance(gui.color_scheme, dict)

            # Test that modern fonts are used
            self.assertTrue(hasattr(gui, 'font_scheme'))
            self.assertIsInstance(gui.font_scheme, dict)

        except ImportError:
            self.fail("Modern styling not implemented yet")

    def test_responsive_layout(self):
        """Test that the layout responds to window resizing"""
        try:
            from universal_document_converter import UniversalDocumentConverterGUI

            gui = UniversalDocumentConverterGUI(self.root)

            # Test initial size
            initial_width = self.root.winfo_reqwidth()
            initial_height = self.root.winfo_reqheight()

            # Test minimum size constraints
            self.assertGreaterEqual(initial_width, 600)
            self.assertGreaterEqual(initial_height, 500)

            # Test that layout adapts to different sizes
            self.root.geometry("800x700")
            self.root.update_idletasks()

            # Should have responsive grid configuration
            self.assertTrue(hasattr(gui, 'configure_responsive_layout'))

        except Exception as e:
            self.fail(f"Responsive layout not properly implemented: {e}")

    def test_improved_visual_hierarchy(self):
        """Test that visual hierarchy is improved with better spacing and grouping"""
        try:
            from universal_document_converter import UniversalDocumentConverterGUI

            gui = UniversalDocumentConverterGUI(self.root)

            # Test that sections are properly grouped
            self.assertTrue(hasattr(gui, 'create_section_frames'))

            # Test that spacing is consistent
            self.assertTrue(hasattr(gui, 'apply_consistent_spacing'))

            # Test that visual indicators are present
            self.assertTrue(hasattr(gui, 'add_visual_indicators'))

        except ImportError:
            self.fail("Visual hierarchy improvements not implemented yet")

    def test_enhanced_progress_feedback(self):
        """Test that progress feedback is enhanced with better indicators"""
        try:
            from universal_document_converter import UniversalDocumentConverterGUI

            gui = UniversalDocumentConverterGUI(self.root)

            # Test that enhanced progress bar exists
            self.assertTrue(hasattr(gui, 'progress_bar'))

            # Test that detailed status display exists
            self.assertTrue(hasattr(gui, 'detailed_status_display'))

            # Test that progress animation is available
            self.assertTrue(hasattr(gui, 'animate_progress'))

        except ImportError:
            self.fail("Enhanced progress feedback not implemented yet")

    def test_improved_button_styling(self):
        """Test that buttons have improved styling and hover effects"""
        try:
            from universal_document_converter import UniversalDocumentConverterGUI

            gui = UniversalDocumentConverterGUI(self.root)

            # Test that button styling is enhanced
            self.assertTrue(hasattr(gui, 'style_buttons'))

            # Test that hover effects are implemented
            self.assertTrue(hasattr(gui, 'add_hover_effects'))

            # Test that button states are properly managed
            self.assertTrue(hasattr(gui, 'update_button_states'))

        except ImportError:
            self.fail("Button styling improvements not implemented yet")

    def test_dark_mode_support(self):
        """Test that dark mode theming is supported"""
        try:
            from universal_document_converter import UniversalDocumentConverterGUI

            gui = UniversalDocumentConverterGUI(self.root)

            # Test that theme switching is available
            self.assertTrue(hasattr(gui, 'toggle_theme'))

            # Test that dark theme colors are defined
            self.assertTrue(hasattr(gui, 'dark_theme'))
            self.assertIsInstance(gui.dark_theme, dict)

            # Test that light theme colors are defined
            self.assertTrue(hasattr(gui, 'light_theme'))
            self.assertIsInstance(gui.light_theme, dict)

        except ImportError:
            self.fail("Dark mode support not implemented yet")

    def test_accessibility_improvements(self):
        """Test that accessibility features are implemented"""
        try:
            from universal_document_converter import UniversalDocumentConverterGUI

            gui = UniversalDocumentConverterGUI(self.root)

            # Test that keyboard navigation is supported
            self.assertTrue(hasattr(gui, 'setup_keyboard_navigation'))

            # Test that tooltips are available
            self.assertTrue(hasattr(gui, 'add_tooltips'))

            # Test that high contrast mode is available
            self.assertTrue(hasattr(gui, 'high_contrast_mode'))

        except ImportError:
            self.fail("Accessibility improvements not implemented yet")

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
        suite.addTest(loader.loadTestsFromTestCase(TestEdgeCases))
        suite.addTest(loader.loadTestsFromTestCase(TestReaderWriterClasses))
        suite.addTest(loader.loadTestsFromTestCase(TestPerformance))
        suite.addTest(loader.loadTestsFromTestCase(TestErrorHandling))
        suite.addTest(loader.loadTestsFromTestCase(TestFormatSpecificFeatures))
        suite.addTest(loader.loadTestsFromTestCase(TestLoggingAndErrorHandling))
        suite.addTest(loader.loadTestsFromTestCase(TestGUIImprovements))

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