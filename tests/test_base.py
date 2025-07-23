#!/usr/bin/env python3
"""
Base test classes and utilities for Universal Document Converter test suite
Provides common setup/teardown, file creation utilities, and assertion helpers
"""

import unittest
import tempfile
import shutil
import time
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
import tkinter as tk
from functools import wraps

# Try importing PIL for image tests
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class BaseTestCase(unittest.TestCase):
    """Base test case with common setup and teardown"""
    
    def setUp(self):
        """Create temporary directory and initialize common test state"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_files = []
        self.cleanup_paths = []
        
        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def tearDown(self):
        """Clean up temporary files and directories"""
        # Clean up tracked test files
        for file_path in self.test_files:
            if file_path.exists():
                file_path.unlink(missing_ok=True)
        
        # Clean up additional paths
        for path in self.cleanup_paths:
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    path.unlink(missing_ok=True)
        
        # Clean up temp directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_file(self, name: str, content: str = "Test content") -> Path:
        """Create a test file in the temporary directory"""
        file_path = self.temp_dir / name
        file_path.write_text(content, encoding='utf-8')
        self.test_files.append(file_path)
        return file_path
    
    def track_cleanup(self, path: Path):
        """Track a path for cleanup in tearDown"""
        self.cleanup_paths.append(path)


class GUITestCase(BaseTestCase):
    """Base test case for GUI components"""
    
    def setUp(self):
        """Set up GUI test environment"""
        super().setUp()
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        
    def tearDown(self):
        """Clean up GUI resources"""
        if hasattr(self, 'root') and self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
        super().tearDown()
    
    def process_gui_events(self, delay: float = 0.1):
        """Process pending GUI events"""
        self.root.update()
        time.sleep(delay)


class TestFileFactory:
    """Factory for creating various types of test files"""
    
    @staticmethod
    def create_text_file(path: Path, content: Optional[str] = None) -> Path:
        """Create a text file with optional content"""
        if content is None:
            content = "This is a test document.\n\nIt has multiple paragraphs."
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path
    
    @staticmethod
    def create_image_file(path: Path, size: tuple = (100, 100), 
                         format: str = 'PNG', color: str = 'white') -> Path:
        """Create a test image file"""
        if not PIL_AVAILABLE:
            # Create a minimal valid PNG if PIL not available
            png_header = b'\x89PNG\r\n\x1a\n'
            path.write_bytes(png_header)
            return path
        
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new('RGB', size, color)
        image.save(path, format)
        return path
    
    @staticmethod
    def create_pdf_file(path: Path, content: Optional[str] = None) -> Path:
        """Create a minimal PDF file"""
        if content is None:
            # Minimal valid PDF
            content = """%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources 4 0 R /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >>
endobj
5 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 700 Td
(Test PDF) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000229 00000 n 
0000000328 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
421
%%EOF"""
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='latin-1')
        return path
    
    @staticmethod
    def create_html_file(path: Path, content: Optional[str] = None) -> Path:
        """Create an HTML file"""
        if content is None:
            content = """<!DOCTYPE html>
<html>
<head>
    <title>Test Document</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Test Heading</h1>
    <p>This is a test paragraph.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>"""
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path
    
    @staticmethod
    def create_markdown_file(path: Path, content: Optional[str] = None) -> Path:
        """Create a Markdown file"""
        if content is None:
            content = """# Test Document

This is a **test** document with *various* markdown elements.

## Section 1

- List item 1
- List item 2

### Code Example

```python
def hello():
    print("Hello, World!")
```

## Section 2

> This is a blockquote

[Link](https://example.com)
"""
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path
    
    @staticmethod
    def create_corrupted_file(path: Path, size: int = 1024) -> Path:
        """Create a corrupted/binary file for error testing"""
        import random
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate random binary data
        data = bytes(random.randint(0, 255) for _ in range(size))
        path.write_bytes(data)
        return path


class TestData:
    """Common test data and content"""
    
    # Text content variations
    SIMPLE_TEXT = "This is a simple test document."
    
    MULTILINE_TEXT = """This is a test document.

It has multiple paragraphs with different content.

And a third paragraph for good measure."""
    
    UNICODE_TEXT = "Hello 世界! 🚀 Café naïve résumé Привет мир"
    
    # Special characters that often cause issues
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    
    # HTML variations
    SIMPLE_HTML = "<p>Simple HTML content</p>"
    
    COMPLEX_HTML = """<html>
<body>
    <h1>Test Document</h1>
    <p>Paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>"""
    
    MALFORMED_HTML = "<p>Unclosed paragraph <div>Unclosed div"
    
    # Common test filenames
    TEST_FILENAMES = [
        "test.txt",
        "test with spaces.txt",
        "test_unicode_文件.txt",
        "test.special!@#$.txt"
    ]


class CustomAssertions:
    """Custom assertion methods for common test patterns"""
    
    @staticmethod
    def assertFileCreated(test_case: unittest.TestCase, filepath: Path, 
                         message: Optional[str] = None):
        """Assert that a file was created"""
        if not filepath.exists():
            test_case.fail(message or f"File not created: {filepath}")
        
        if not filepath.is_file():
            test_case.fail(f"Path exists but is not a file: {filepath}")
    
    @staticmethod
    def assertFileContains(test_case: unittest.TestCase, filepath: Path, 
                          expected_content: str, encoding: str = 'utf-8'):
        """Assert that a file contains expected content"""
        CustomAssertions.assertFileCreated(test_case, filepath)
        
        actual_content = filepath.read_text(encoding=encoding)
        test_case.assertIn(expected_content, actual_content, 
                          f"Expected content not found in {filepath}")
    
    @staticmethod
    def assertConversionSuccessful(test_case: unittest.TestCase, 
                                 input_file: Path, output_file: Path,
                                 check_content: bool = True):
        """Assert that a conversion was successful"""
        # Check input exists
        test_case.assertTrue(input_file.exists(), f"Input file missing: {input_file}")
        
        # Check output created
        CustomAssertions.assertFileCreated(test_case, output_file,
                                         f"Conversion failed to create output: {output_file}")
        
        # Check output has content
        if check_content:
            size = output_file.stat().st_size
            test_case.assertGreater(size, 0, f"Output file is empty: {output_file}")
    
    @staticmethod
    def assertModuleImportable(test_case: unittest.TestCase, module_name: str,
                             required_attributes: Optional[List[str]] = None):
        """Assert that a module can be imported with required attributes"""
        try:
            import importlib
            module = importlib.import_module(module_name)
            
            if required_attributes:
                for attr in required_attributes:
                    test_case.assertTrue(hasattr(module, attr),
                                       f"Module {module_name} missing attribute: {attr}")
        except ImportError as e:
            test_case.fail(f"Failed to import {module_name}: {e}")


def time_limit(seconds: float):
    """Decorator to ensure test completes within time limit"""
    def decorator(test_func: Callable):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = test_func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            if elapsed > seconds:
                # Get test case instance
                test_case = args[0] if args and isinstance(args[0], unittest.TestCase) else None
                if test_case:
                    test_case.fail(f"Test exceeded time limit: {elapsed:.2f}s > {seconds}s")
            
            return result
        return wrapper
    return decorator


def requires_module(module_name: str, skip_message: Optional[str] = None):
    """Decorator to skip test if module not available"""
    def decorator(test_item):
        try:
            import importlib
            importlib.import_module(module_name)
            return test_item
        except ImportError:
            message = skip_message or f"Requires {module_name} module"
            return unittest.skip(message)(test_item)
    return decorator


def requires_gui():
    """Decorator to skip test if GUI not available"""
    def decorator(test_item):
        try:
            import tkinter
            root = tkinter.Tk()
            root.destroy()
            return test_item
        except:
            return unittest.skip("Requires GUI support")(test_item)
    return decorator


class MockProgress:
    """Mock progress tracker for testing"""
    
    def __init__(self):
        self.updates = []
        self.current = 0
        self.total = 100
        
    def update(self, current: int, total: int, message: str = ""):
        """Record progress update"""
        self.current = current
        self.total = total
        self.updates.append({
            'current': current,
            'total': total,
            'message': message,
            'timestamp': time.time()
        })
    
    def reset(self):
        """Reset progress tracker"""
        self.updates.clear()
        self.current = 0
        self.total = 100