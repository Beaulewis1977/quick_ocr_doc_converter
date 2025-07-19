#!/usr/bin/env python3
"""
Debug Script for Universal Document Converter
Thoroughly tests all components and features
"""

import sys
import os
from pathlib import Path
import traceback
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class ConverterDebugger:
    """Debug and test the document converter"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version,
            'platform': sys.platform,
            'tests': []
        }
        self.passed = 0
        self.failed = 0
    
    def test(self, name, func):
        """Run a test and record results"""
        print(f"\n🧪 Testing: {name}")
        try:
            result = func()
            self.passed += 1
            print(f"   ✅ PASSED: {result}")
            self.results['tests'].append({
                'name': name,
                'status': 'passed',
                'result': result
            })
            return True
        except Exception as e:
            self.failed += 1
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"   ❌ FAILED: {error_msg}")
            self.results['tests'].append({
                'name': name,
                'status': 'failed',
                'error': error_msg,
                'traceback': traceback.format_exc()
            })
            return False
    
    def test_python_version(self):
        """Test Python version requirement"""
        if sys.version_info >= (3, 7):
            return f"Python {sys.version.split()[0]} meets requirement (>= 3.7)"
        else:
            raise Exception(f"Python {sys.version.split()[0]} is below minimum requirement (3.7)")
    
    def test_core_imports(self):
        """Test core Python imports"""
        imports = [
            'tkinter',
            'threading',
            'pathlib',
            'json',
            'concurrent.futures',
            'logging'
        ]
        for module in imports:
            __import__(module)
        return f"All {len(imports)} core modules imported successfully"
    
    def test_document_dependencies(self):
        """Test document processing dependencies"""
        deps = []
        optional = []
        
        # Required dependencies
        try:
            import docx
            deps.append('python-docx')
        except ImportError:
            raise Exception("python-docx not installed (required)")
        
        try:
            import PyPDF2
            deps.append('PyPDF2')
        except ImportError:
            raise Exception("PyPDF2 not installed (required)")
        
        # Optional dependencies
        try:
            import bs4
            optional.append('beautifulsoup4')
        except ImportError:
            pass
        
        try:
            import striprtf
            optional.append('striprtf')
        except ImportError:
            pass
        
        try:
            import tkinterdnd2
            optional.append('tkinterdnd2')
        except ImportError:
            pass
        
        return f"Required: {', '.join(deps)}. Optional: {', '.join(optional) if optional else 'none'}"
    
    def test_ocr_dependencies(self):
        """Test OCR dependencies"""
        ocr_deps = []
        missing = []
        
        try:
            import pytesseract
            ocr_deps.append('pytesseract')
        except ImportError:
            missing.append('pytesseract')
        
        try:
            import PIL
            ocr_deps.append('Pillow')
        except ImportError:
            missing.append('Pillow')
        
        try:
            import cv2
            ocr_deps.append('opencv-python')
        except ImportError:
            missing.append('opencv-python')
        
        try:
            import numpy
            ocr_deps.append('numpy')
        except ImportError:
            missing.append('numpy')
        
        if missing:
            return f"OCR available: {', '.join(ocr_deps)}. Missing: {', '.join(missing)}"
        else:
            return f"All OCR dependencies available: {', '.join(ocr_deps)}"
    
    def test_ocr_engine(self):
        """Test OCR engine components"""
        from ocr_engine.ocr_integration import OCRIntegration
        from ocr_engine.format_detector import OCRFormatDetector
        
        ocr = OCRIntegration()
        detector = OCRFormatDetector()
        
        # Check availability
        availability = ocr.check_availability()
        
        # Check supported formats
        formats = list(detector.get_supported_extensions())
        
        return f"OCR status: {availability['message']}. Supports {len(formats)} image formats"
    
    def test_gui_initialization(self):
        """Test GUI initialization without display"""
        # Import with display check
        import tkinter as tk
        
        # Test basic GUI creation
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Import main app
        from universal_document_converter_complete import DocumentConverterApp
        
        # Create app instance
        app = DocumentConverterApp(root)
        
        # Check key attributes
        attrs = ['config_manager', 'ocr_integration', 'file_tree', 'progress_bar']
        missing = [attr for attr in attrs if not hasattr(app, attr)]
        
        root.destroy()
        
        if missing:
            raise Exception(f"Missing attributes: {', '.join(missing)}")
        
        return "GUI initialized successfully with all components"
    
    def test_configuration_manager(self):
        """Test configuration management"""
        from universal_document_converter_complete import ConfigurationManager
        
        config = ConfigurationManager()
        
        # Test default values
        defaults = ['theme', 'max_workers', 'output_format', 'preserve_structure']
        for key in defaults:
            if key not in config.config:
                raise Exception(f"Missing default config: {key}")
        
        # Test get/set
        test_key = 'test_value'
        test_val = 'test123'
        config.set(test_key, test_val)
        if config.get(test_key) != test_val:
            raise Exception("Config get/set failed")
        
        return f"Config manager working with {len(config.config)} settings"
    
    def test_file_conversions(self):
        """Test file conversion methods"""
        from universal_document_converter_complete import DocumentConverterApp
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        app = DocumentConverterApp(root)
        
        # Test method existence
        methods = [
            'convert_docx_to_markdown',
            'convert_pdf_to_markdown',
            'convert_txt_to_markdown',
            'convert_html_to_markdown',
            'convert_rtf_to_markdown',
            'convert_image_to_markdown',
            'is_pdf_image_based'
        ]
        
        missing = [m for m in methods if not hasattr(app, m)]
        
        root.destroy()
        
        if missing:
            raise Exception(f"Missing conversion methods: {', '.join(missing)}")
        
        return f"All {len(methods)} conversion methods available"
    
    def test_threading_support(self):
        """Test threading and concurrent processing"""
        import concurrent.futures
        import threading
        
        # Test thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = []
            for i in range(4):
                future = executor.submit(lambda x: x * 2, i)
                futures.append(future)
            
            results = [f.result() for f in futures]
            if results != [0, 2, 4, 6]:
                raise Exception("Thread pool execution failed")
        
        # Test threading event
        event = threading.Event()
        event.set()
        if not event.is_set():
            raise Exception("Threading event failed")
        
        return "Threading and concurrent processing working correctly"
    
    def test_memory_monitoring(self):
        """Test memory monitoring capability"""
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            return f"Memory monitoring available. Current usage: {memory_mb:.1f} MB"
        except ImportError:
            return "psutil not installed - memory monitoring disabled"
    
    def test_drag_drop_support(self):
        """Test drag and drop support"""
        try:
            import tkinterdnd2
            return "Drag and drop support available via tkinterdnd2"
        except ImportError:
            return "tkinterdnd2 not installed - drag and drop disabled"
    
    def test_file_system_operations(self):
        """Test file system operations"""
        test_dir = Path("debug_test_temp")
        test_file = test_dir / "test.txt"
        
        try:
            # Create directory
            test_dir.mkdir(exist_ok=True)
            
            # Write file
            test_file.write_text("Test content")
            
            # Read file
            content = test_file.read_text()
            if content != "Test content":
                raise Exception("File read/write mismatch")
            
            # Check file size
            size = test_file.stat().st_size
            
            # Clean up
            test_file.unlink()
            test_dir.rmdir()
            
            return "File system operations working correctly"
            
        except Exception as e:
            # Clean up on error
            if test_file.exists():
                test_file.unlink()
            if test_dir.exists():
                test_dir.rmdir()
            raise e
    
    def test_logging_system(self):
        """Test logging system"""
        import logging
        from datetime import datetime
        
        # Create test logger
        logger = logging.getLogger('test_logger')
        logger.setLevel(logging.INFO)
        
        # Test log message
        test_msg = f"Test log at {datetime.now()}"
        logger.info(test_msg)
        
        return "Logging system configured and working"
    
    def test_error_handling(self):
        """Test custom error handling"""
        from universal_document_converter_complete import (
            DocumentConverterError,
            UnsupportedFormatError,
            FileProcessingError
        )
        
        # Test exception hierarchy
        try:
            raise UnsupportedFormatError("Test error")
        except DocumentConverterError:
            pass  # Should catch as parent class
        except Exception:
            raise Exception("Exception hierarchy broken")
        
        return "Custom error classes working correctly"
    
    def run_all_tests(self):
        """Run all tests"""
        print("🔍 Universal Document Converter - Debug Report")
        print("=" * 60)
        
        # Core tests
        self.test("Python Version", self.test_python_version)
        self.test("Core Imports", self.test_core_imports)
        self.test("Document Dependencies", self.test_document_dependencies)
        self.test("OCR Dependencies", self.test_ocr_dependencies)
        
        # Component tests
        self.test("OCR Engine", self.test_ocr_engine)
        self.test("GUI Initialization", self.test_gui_initialization)
        self.test("Configuration Manager", self.test_configuration_manager)
        self.test("File Conversions", self.test_file_conversions)
        
        # System tests
        self.test("Threading Support", self.test_threading_support)
        self.test("Memory Monitoring", self.test_memory_monitoring)
        self.test("Drag & Drop Support", self.test_drag_drop_support)
        self.test("File System Operations", self.test_file_system_operations)
        self.test("Logging System", self.test_logging_system)
        self.test("Error Handling", self.test_error_handling)
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.passed} passed, {self.failed} failed")
        
        # Save results
        with open('debug_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📝 Detailed report saved to: debug_report.json")
        
        if self.failed == 0:
            print("\n✅ All tests passed! The converter is ready to use.")
        else:
            print("\n❌ Some tests failed. Check the report for details.")
            print("   Run: pip install -r requirements.txt")
        
        return self.failed == 0

def main():
    """Main debug entry point"""
    debugger = ConverterDebugger()
    success = debugger.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()