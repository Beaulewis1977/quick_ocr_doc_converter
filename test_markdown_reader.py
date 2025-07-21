#!/usr/bin/env python3
"""
Test file for Markdown Reader implementation
Following TDD approach - write tests first
"""

import unittest
import tempfile
import os
from pathlib import Path


class TestMarkdownReader(unittest.TestCase):
    """Test cases for MarkdownReader class"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_test_file(self, content, filename="test.md"):
        """Helper to create test markdown files"""
        filepath = Path(self.test_dir) / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(filepath)
    
    def test_simple_headings_and_paragraphs(self):
        """Test basic markdown with headings and paragraphs"""
        markdown_content = """# Main Title

This is a paragraph under the main title.

## Subtitle

Another paragraph here.

### Sub-subtitle

Final paragraph.
"""
        filepath = self.create_test_file(markdown_content)
        
        # Import here so test can run before implementation
        try:
            from universal_document_converter import MarkdownReader
            reader = MarkdownReader()
            result = reader.read(filepath)
            
            # Expected structure: [('heading', level, text), ('paragraph', text), ...]
            expected = [
                ('heading', 1, 'Main Title'),
                ('paragraph', 'This is a paragraph under the main title.'),
                ('heading', 2, 'Subtitle'),
                ('paragraph', 'Another paragraph here.'),
                ('heading', 3, 'Sub-subtitle'),
                ('paragraph', 'Final paragraph.')
            ]
            
            self.assertEqual(result, expected)
        except ImportError:
            self.skipTest("MarkdownReader not yet implemented")
    
    def test_empty_file(self):
        """Test empty markdown file"""
        filepath = self.create_test_file("")
        
        try:
            from universal_document_converter import MarkdownReader
            reader = MarkdownReader()
            result = reader.read(filepath)
            self.assertEqual(result, [])
        except ImportError:
            self.skipTest("MarkdownReader not yet implemented")
    
    def test_only_paragraphs(self):
        """Test markdown with only paragraphs (no headings)"""
        markdown_content = """This is the first paragraph.

This is the second paragraph.

This is the third paragraph.
"""
        filepath = self.create_test_file(markdown_content)
        
        try:
            from universal_document_converter import MarkdownReader
            reader = MarkdownReader()
            result = reader.read(filepath)
            
            expected = [
                ('paragraph', 'This is the first paragraph.'),
                ('paragraph', 'This is the second paragraph.'),
                ('paragraph', 'This is the third paragraph.')
            ]
            
            self.assertEqual(result, expected)
        except ImportError:
            self.skipTest("MarkdownReader not yet implemented")
    
    def test_only_headings(self):
        """Test markdown with only headings (no paragraphs)"""
        markdown_content = """# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
"""
        filepath = self.create_test_file(markdown_content)
        
        try:
            from universal_document_converter import MarkdownReader
            reader = MarkdownReader()
            result = reader.read(filepath)
            
            expected = [
                ('heading', 1, 'Heading 1'),
                ('heading', 2, 'Heading 2'),
                ('heading', 3, 'Heading 3'),
                ('heading', 4, 'Heading 4'),
                ('heading', 5, 'Heading 5'),
                ('heading', 6, 'Heading 6')
            ]
            
            self.assertEqual(result, expected)
        except ImportError:
            self.skipTest("MarkdownReader not yet implemented")
    
    def test_format_detection(self):
        """Test that .md files are properly detected"""
        try:
            from universal_document_converter import FormatDetector
            
            # Test .md extension
            self.assertEqual(FormatDetector.detect_format("test.md"), "markdown")
            
            # Test .markdown extension  
            self.assertEqual(FormatDetector.detect_format("test.markdown"), "markdown")
            
            # Test format appears in input format list
            input_formats = FormatDetector.get_input_format_list()
            markdown_formats = [f for f in input_formats if 'markdown' in f[1]]
            self.assertTrue(len(markdown_formats) > 0)
            
        except ImportError:
            self.skipTest("FormatDetector markdown support not yet implemented")


if __name__ == '__main__':
    unittest.main()