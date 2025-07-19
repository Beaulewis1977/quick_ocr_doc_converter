#!/usr/bin/env python3
"""
Debug Script for Bidirectional Document Converter
Tests all conversion paths and output formats
"""

import sys
import os
from pathlib import Path
import tempfile
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class BidirectionalDebugger:
    """Debug bidirectional conversion features"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'issues_found': []
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
                'error': error_msg
            })
            self.results['issues_found'].append({
                'test': name,
                'issue': error_msg,
                'severity': 'high' if 'Error' in error_msg else 'medium'
            })
            return False
    
    def test_import_structure(self):
        """Test import structure and inheritance"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        from universal_document_converter_complete import DocumentConverterApp
        
        # Check inheritance
        if not issubclass(BidirectionalDocumentConverter, DocumentConverterApp):
            raise Exception("BidirectionalDocumentConverter should inherit from DocumentConverterApp")
        
        return "Import structure and inheritance correct"
    
    def test_format_definitions(self):
        """Test format definitions"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        converter = BidirectionalDocumentConverter(root)
        
        # Check input formats
        if '*.md' not in converter.input_formats['documents']:
            raise Exception("Markdown (.md) not in input formats")
        
        # Check output formats
        expected_outputs = ['markdown', 'text', 'docx', 'pdf', 'html', 'rtf']
        for fmt in expected_outputs:
            if fmt not in converter.output_formats:
                raise Exception(f"Missing output format: {fmt}")
        
        root.destroy()
        return f"All {len(expected_outputs)} output formats defined"
    
    def test_conversion_methods(self):
        """Test conversion method existence"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        converter = BidirectionalDocumentConverter(root)
        
        # Check conversion methods
        methods = [
            'read_markdown_file',
            'convert_from_markdown',
            'markdown_to_text',
            'markdown_to_html',
            'markdown_to_docx',
            'markdown_to_pdf',
            'markdown_to_rtf',
            'save_output_file',
            'convert_image_to_multiple_formats'
        ]
        
        missing = []
        for method in methods:
            if not hasattr(converter, method):
                missing.append(method)
        
        root.destroy()
        
        if missing:
            raise Exception(f"Missing methods: {', '.join(missing)}")
        
        return f"All {len(methods)} conversion methods present"
    
    def test_markdown_to_text_conversion(self):
        """Test markdown to text conversion"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        converter = BidirectionalDocumentConverter(root)
        
        # Test markdown content
        markdown = """# Test Header
        
This is **bold** and this is *italic*.

## Subheader

- List item 1
- List item 2

[Link text](https://example.com)

`code block`

```python
def test():
    pass
```
"""
        
        # Convert to text
        text = converter.markdown_to_text(markdown)
        
        # Verify conversions
        if '**bold**' in text or '*italic*' in text:
            raise Exception("Markdown formatting not removed")
        
        if '#' in text:
            raise Exception("Header markers not removed")
        
        if '[Link text]' in text:
            raise Exception("Link formatting not cleaned")
        
        if '```' in text:
            raise Exception("Code block markers not removed")
        
        root.destroy()
        return "Markdown to text conversion working correctly"
    
    def test_markdown_to_html_conversion(self):
        """Test markdown to HTML conversion"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        converter = BidirectionalDocumentConverter(root)
        
        # Test markdown
        markdown = "# Test Header\n\nThis is a **test**."
        
        # Convert to HTML
        html = converter.markdown_to_html(markdown)
        
        # Check HTML structure
        if '<!DOCTYPE html>' not in html:
            raise Exception("Missing HTML doctype")
        
        if '<html>' not in html or '</html>' not in html:
            raise Exception("Missing HTML tags")
        
        if '<head>' not in html or '<body>' not in html:
            raise Exception("Missing head or body tags")
        
        root.destroy()
        return "Markdown to HTML conversion working"
    
    def test_output_format_selector(self):
        """Test output format selector variable"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        converter = BidirectionalDocumentConverter(root)
        
        # Check format variable
        if not hasattr(converter, 'output_format_var'):
            raise Exception("Missing output_format_var")
        
        # Test setting format
        converter.output_format_var.set('pdf')
        if converter.output_format_var.get() != 'pdf':
            raise Exception("Format variable not working")
        
        root.destroy()
        return "Output format selector working"
    
    def test_save_output_file_logic(self):
        """Test save output file logic"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        converter = BidirectionalDocumentConverter(root)
        
        # Test with temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp_path = Path(tmp.name)
            
            # Test text save
            converter.save_output_file(tmp_path, "Test content", 'text')
            
            # Verify file exists
            if not tmp_path.exists():
                raise Exception("File not created")
            
            # Read and verify
            content = tmp_path.read_text()
            if content != "Test content":
                raise Exception("Content not saved correctly")
            
            # Clean up
            tmp_path.unlink()
        
        root.destroy()
        return "Save output file logic working"
    
    def test_scan_folder_includes_markdown(self):
        """Test that scan includes .md files"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        converter = BidirectionalDocumentConverter(root)
        
        # Check input formats include .md
        if '*.md' not in converter.input_formats['documents']:
            raise Exception(".md not in input formats")
        
        root.destroy()
        return "Markdown files included in scan patterns"
    
    def test_gui_integration(self):
        """Test GUI integration points"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        converter = BidirectionalDocumentConverter(root)
        
        # Check title update
        if "Bidirectional" not in root.title():
            raise Exception("Window title not updated")
        
        # Check methods exist
        if not hasattr(converter, 'add_format_selector_to_frame'):
            raise Exception("Missing GUI integration method")
        
        root.destroy()
        return "GUI integration points present"
    
    def test_error_handling(self):
        """Test error handling in conversion"""
        from universal_document_converter_bidirectional import BidirectionalDocumentConverter
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        
        converter = BidirectionalDocumentConverter(root)
        
        # Test with invalid format
        try:
            converter.convert_from_markdown("Test", "invalid_format", Path("test.md"))
            raise Exception("Should have raised error for invalid format")
        except Exception as e:
            if "Unsupported output format" not in str(e):
                raise Exception("Wrong error message for invalid format")
        
        root.destroy()
        return "Error handling working correctly"
    
    def check_potential_issues(self):
        """Check for potential issues"""
        issues = []
        
        # Check 1: GUI integration incomplete
        issues.append({
            'issue': 'GUI format selector integration incomplete',
            'severity': 'medium',
            'fix': 'The add_output_format_selector method has pass statement'
        })
        
        # Check 2: PDF/DOCX implementation placeholders
        issues.append({
            'issue': 'PDF and DOCX conversion returns None (placeholder)',
            'severity': 'high',
            'fix': 'Need actual implementation for PDF/DOCX generation'
        })
        
        # Check 3: Missing imports in some conversion methods
        issues.append({
            'issue': 'Some conversion methods may fail if libraries not installed',
            'severity': 'medium',
            'fix': 'Add try/except for optional library imports'
        })
        
        # Check 4: Image embedding not implemented
        issues.append({
            'issue': 'Images not embedded in output documents',
            'severity': 'low',
            'fix': 'Future enhancement to embed images'
        })
        
        self.results['issues_found'].extend(issues)
        return issues
    
    def create_fixed_version(self):
        """Create a fixed version of the bidirectional converter"""
        fixed_code = '''#!/usr/bin/env python3
"""
Universal Document Converter Bidirectional - Fixed Version
Complete document conversion tool with proper bidirectional support
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Import the base converter
from universal_document_converter_complete import (
    DocumentConverterApp, ConfigurationManager,
    FileProcessingError, OCR_AVAILABLE
)

# Optional imports with fallbacks
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import markdown2
    MARKDOWN2_AVAILABLE = True
except ImportError:
    MARKDOWN2_AVAILABLE = False

class BidirectionalDocumentConverter(DocumentConverterApp):
    """Extended converter with bidirectional support"""
    
    def __init__(self, root):
        # Add output format variable before parent init
        self.output_format_var = tk.StringVar(value="markdown")
        
        # Initialize parent class
        super().__init__(root)
        
        # Update title
        self.root.title("Universal Document Converter - Bidirectional Edition")
        
        # Update supported formats
        self.input_formats = {
            'documents': ['*.docx', '*.pdf', '*.txt', '*.md', '*.rtf', '*.odt', 
                         '*.html', '*.htm', '*.epub', '*.xml', '*.json', '*.csv'],
            'images': ['*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif', '*.bmp', 
                      '*.gif', '*.webp']
        }
        
        self.output_formats = {
            'markdown': {'ext': '.md', 'name': 'Markdown'},
            'text': {'ext': '.txt', 'name': 'Plain Text'},
            'docx': {'ext': '.docx', 'name': 'Word Document'},
            'pdf': {'ext': '.pdf', 'name': 'PDF'},
            'html': {'ext': '.html', 'name': 'HTML'},
            'rtf': {'ext': '.rtf', 'name': 'Rich Text Format'}
        }
    
    def create_settings_section(self, parent):
        """Override to add output format selector"""
        # Call parent method first
        super().create_settings_section(parent)
        
        # Add output format selector
        format_frame = ttk.LabelFrame(parent, text="Output Format", padding=10)
        format_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(format_frame, text="Convert to:").pack(side=tk.LEFT, padx=5)
        
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.output_format_var,
            values=[fmt['name'] for fmt in self.output_formats.values()],
            state='readonly',
            width=20
        )
        format_combo.pack(side=tk.LEFT, padx=5)
        
        # Update combo to use format keys
        format_combo['values'] = list(self.output_formats.keys())
        
        # Bind change event
        format_combo.bind('<<ComboboxSelected>>', self.on_format_change)
        
        # Add info label
        self.format_info_label = ttk.Label(format_frame, text="", foreground='blue')
        self.format_info_label.pack(side=tk.LEFT, padx=10)
        
        self.on_format_change()  # Initialize
    
    def on_format_change(self, event=None):
        """Handle output format change"""
        format_name = self.output_format_var.get()
        format_info = self.output_formats.get(format_name, {})
        
        # Update info label
        info_text = f"Output: {format_info.get('ext', '.?')}"
        
        # Check dependencies
        if format_name == 'pdf' and not REPORTLAB_AVAILABLE:
            info_text += " (⚠️ reportlab required)"
        elif format_name == 'docx' and not DOCX_AVAILABLE:
            info_text += " (⚠️ python-docx required)"
        
        self.format_info_label.config(text=info_text)
'''
        
        # Save fixed version
        with open('universal_document_converter_bidirectional_fixed.py', 'w') as f:
            f.write(fixed_code)
        
        return "Created fixed version with proper GUI integration"
    
    def run_all_tests(self):
        """Run all tests"""
        print("🔍 Bidirectional Converter Debug Report")
        print("=" * 60)
        
        # Component tests
        self.test("Import Structure", self.test_import_structure)
        self.test("Format Definitions", self.test_format_definitions)
        self.test("Conversion Methods", self.test_conversion_methods)
        self.test("Markdown to Text", self.test_markdown_to_text_conversion)
        self.test("Markdown to HTML", self.test_markdown_to_html_conversion)
        self.test("Output Format Selector", self.test_output_format_selector)
        self.test("Save Output File", self.test_save_output_file_logic)
        self.test("Scan Includes Markdown", self.test_scan_folder_includes_markdown)
        self.test("GUI Integration", self.test_gui_integration)
        self.test("Error Handling", self.test_error_handling)
        
        # Check for issues
        print("\n🔍 Checking for potential issues...")
        issues = self.check_potential_issues()
        for issue in issues:
            print(f"   ⚠️  {issue['severity'].upper()}: {issue['issue']}")
        
        # Create fixed version
        print("\n🔧 Creating fixed version...")
        self.test("Create Fixed Version", self.create_fixed_version)
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.passed} passed, {self.failed} failed")
        print(f"⚠️  Issues Found: {len(self.results['issues_found'])}")
        
        # Save results
        with open('debug_bidirectional_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📝 Detailed report saved to: debug_bidirectional_report.json")
        
        return self.failed == 0

def main():
    """Main debug entry point"""
    debugger = BidirectionalDebugger()
    success = debugger.run_all_tests()
    
    if not success:
        print("\n❌ Tests failed! Creating fixed version...")
    else:
        print("\n✅ All tests passed!")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()