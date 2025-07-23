# Universal Document Converter - DLL Package

> **📦 Important Update**: The DLL builder and VB6/VFP9 integration system has been moved to the `legacy_dll_builder/` directory for better organization and maintenance. This document describes the legacy approach. For the current implementation, please see `legacy_dll_builder/README.md`.

## Simple Document Conversion for VB6/VFP9 Integration

This package provides a simple document converter specifically designed for VB6 and Visual FoxPro 9 legacy system integration. **This version does NOT include OCR functionality** - it focuses on basic document conversion only.

### What's Included

- **dll_builder_cli.py** - Simple command-line interface for document conversion
- **vb6_integration_simple.vb** - VB6 class for easy integration
- **vfp9_integration_simple.prg** - Visual FoxPro 9 class for easy integration
- **requirements.txt** - Python dependencies
- **UniversalConverter32.dll.bat** - DLL simulator batch file

### Supported Conversions

**Input Formats:**
- PDF (text extraction without OCR)
- DOCX (Microsoft Word documents)
- HTML (web pages)
- Markdown (.md files)
- Plain text (.txt)
- RTF (Rich Text Format)

**Output Formats:**
- Plain text (.txt)
- Markdown (.md)
- HTML (.html)
- JSON (structured data)

### Requirements

- Python 3.7 or higher
- PyMuPDF (for PDF processing)
- python-docx (for DOCX processing)
- BeautifulSoup4 (for HTML processing)
- markdown (for Markdown processing)

### Installation

1. Install Python 3.7+ if not already installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Quick Start

#### Command Line Usage

```bash
# Convert PDF to text
python dll_builder_cli.py document.pdf output.txt

# Convert DOCX to Markdown
python dll_builder_cli.py report.docx report.md --format md

# Convert directory recursively
python dll_builder_cli.py input_folder/ output_folder/ --recursive --format txt

# Show supported formats
python dll_builder_cli.py --formats

# Get help
python dll_builder_cli.py --help
```

#### VB6 Integration

```vb
' Example VB6 usage
Dim Converter As New SimpleDocConverter
Converter.Initialize

' Convert PDF to text
If Converter.ConvertPdfToText("C:\docs\sample.pdf", "C:\output\sample.txt") Then
    MsgBox "Conversion successful!"
End If

' Batch convert directory
If Converter.ConvertDirectory("C:\input\", "C:\output\", "txt", True, True) Then
    MsgBox "Batch conversion completed!"
End If
```

#### Visual FoxPro 9 Integration

```foxpro
* Example VFP9 usage
oConverter = CREATEOBJECT("SimpleDocConverter")

* Convert DOCX to Markdown
llSuccess = oConverter.ConvertDocxToMarkdown("C:\docs\report.docx", "C:\output\report.md")

* Get supported formats
lcFormats = oConverter.GetSupportedFormats()
MESSAGEBOX(lcFormats)
```

### Key Features

- **No OCR Complexity** - Fast, lightweight document conversion
- **32-bit Compatible** - Works with legacy VB6/VFP9 systems
- **Thread-Safe** - Safe for multi-threaded applications
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Multiple Formats** - Supports common document formats
- **Batch Processing** - Convert entire directories
- **VB6/VFP9 Ready** - Complete integration classes provided

### Limitations

- **No OCR** - Cannot extract text from scanned images or PDFs
- **Basic PDF** - Only extracts existing text from PDFs
- **Simple Formatting** - Output formatting is basic

### For Advanced Features

If you need OCR capabilities, API integration, or advanced document processing, use the complete Universal Document Converter GUI application instead.

### Support

This package is designed for basic document conversion in legacy systems. The CLI interface is intentionally simple to ensure compatibility with VB6 and VFP9 applications.

### Version

Simple Document Converter 1.0.0 - Basic conversion for legacy integration