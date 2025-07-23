# Universal Document Converter - Complete User Guide

## 🌟 Overview

The Universal Document Converter is an enterprise-grade OCR and document conversion suite with multiple interfaces to suit different user needs. This guide covers all available tools, their capabilities, and how to use them.

## 📋 Quick Start

### System Requirements
- **Python 3.8+** (required for all tools)
- **Windows, macOS, or Linux**
- **Tesseract OCR** (for OCR functionality)
- **Additional dependencies** installed via requirements.txt

### One-Click Setup
```bash
# Windows
./install.bat

# Linux/macOS  
python3 setup_ocr_environment.py
```

---

## 🖥️ GUI Applications

### 1. **Main GUI Application** ⭐ *Recommended for most users*
**File:** `universal_document_converter.py`

**Launch:**
```bash
python3 universal_document_converter.py
# Or use launchers:
./⚡ Quick Launch.bat         # Windows
./🚀 Launch Quick Document Convertor.bat  # Windows
```

**Features:**
- **Complete enterprise solution** with tabbed interface
- **Full OCR system** with Tesseract, EasyOCR, and Google Vision API
- **Document conversion** between all major formats
- **API management** for cloud OCR services
- **Advanced settings** and configuration
- **Multi-threading** with progress tracking
- **Drag-and-drop** support
- **Professional logging** and error handling

**Use Cases:**
- Complete document processing workflows
- Enterprise users needing all features
- Users wanting a comprehensive GUI experience

---

### 2. **Specialized OCR GUI**
**File:** `gui_ocr.py`

**Launch:**
```bash
python3 gui_ocr.py
```

**Features:**
- **OCR-focused interface** for image and PDF text extraction
- **Multi-language support** (English, French, Spanish, German, Japanese)
- **Batch processing** for folders
- **Real-time progress** tracking with logs
- **Markdown output** format
- **Lightweight** alternative to main GUI

**Use Cases:**
- Users who only need OCR functionality
- Quick text extraction from images/PDFs
- Educational and research document digitization

---

### 3. **Simple Document Converter GUI**
**File:** `document_converter_gui.py`

**Launch:**
```bash
python3 document_converter_gui.py
```

**Features:**
- Basic document conversion interface
- Simple file-to-file conversion
- Minimal resource usage

---

### 4. **System Tray Application**
**File:** `enhanced_system_tray.py`

**Launch:**
```bash
python3 enhanced_system_tray.py
```

**Features:**
- **Background processing** via system tray
- **Quick access** to conversion functions
- **Minimal resource footprint**
- **Always available** in system tray

---

## 💻 Command Line Interface (CLI) Tools

### 1. **DLL Builder CLI** 🔧 *For VB6/VFP9 Developers*
**File:** `dll_builder_cli.py`

**Launch:**
```bash
python3 dll_builder_cli.py [command]
```

**Commands:**
```bash
# Build the 32-bit DLL
python3 dll_builder_cli.py build

# Check DLL status
python3 dll_builder_cli.py status

# Run comprehensive tests
python3 dll_builder_cli.py test

# Generate VB6 integration code
python3 dll_builder_cli.py vb6 generate

# Generate VFP9 integration code  
python3 dll_builder_cli.py vfp9 generate

# Create distribution package
python3 dll_builder_cli.py package

# Install DLL system-wide
python3 dll_builder_cli.py install
```

**Features:**
- **Real 32-bit DLL compilation** (not simulation)
- **VB6 and Visual FoxPro 9** integration
- **Comprehensive testing** suite
- **Automated code generation**
- **Distribution packaging**

**Use Cases:**
- Legacy system integration
- VB6/VFP9 developers
- Enterprise environments with legacy applications

---

### 2. **Document Converter CLI** 📄 *For Basic Conversion*
**File:** `legacy_dll_builder/document_converter_cli.py`

**Launch:**
```bash
python3 legacy_dll_builder/document_converter_cli.py [options] input output
```

**Examples:**
```bash
# Convert PDF to text
python3 legacy_dll_builder/document_converter_cli.py document.pdf output.txt

# Convert DOCX to markdown
python3 legacy_dll_builder/document_converter_cli.py document.docx output.md

# Convert directory recursively
python3 legacy_dll_builder/document_converter_cli.py -r input_dir/ output_dir/

# Show supported formats
python3 legacy_dll_builder/document_converter_cli.py --formats
```

**Supported Formats:**
- **Input:** PDF, DOCX, TXT, HTML, MD, RTF
- **Output:** TXT, MD, HTML, JSON

**Features:**
- **No OCR** (text extraction only)
- **VB6/VFP9 compatible** encoding
- **Recursive processing**
- **Batch conversion**
- **Windows line endings** support

**Use Cases:**
- Basic document conversion without OCR
- Batch processing scripts
- Integration with other systems
- Users who don't need OCR functionality

---

### 3. **Advanced DLL Builder CLI** 🚀 *Enhanced Features*
**File:** `legacy_dll_builder/dll_builder_advanced_cli.py`

**Launch:**
```bash
python3 legacy_dll_builder/dll_builder_advanced_cli.py [command]
```

**Features:**
- Enhanced DLL building capabilities
- Advanced configuration options
- Extended testing suite

---

## 🔧 Standalone Utilities

### Conversion Tools
```bash
# Markdown converter
python3 convert_to_markdown.py input.pdf

# Recursive directory converter  
python3 convert_recursive.py /path/to/folder

# OCR launcher
python3 launch_ocr.py
```

### Setup & Installation
```bash
# Environment setup
python3 setup_ocr_environment.py

# Install OCR dependencies
python3 install_ocr_dependencies.py

# Build distribution packages
python3 build_ocr_packages.py
```

---

## 📦 Installation Guide

### Method 1: Quick Install (Windows)
1. Download the complete package: `Universal-Document-Converter-v3.1.0-Windows-Complete.zip`
2. Extract to desired folder
3. Run `install.bat`
4. Use any of the launcher scripts

### Method 2: Manual Install (All Platforms)
```bash
# Clone repository
git clone https://github.com/Beaulewis1977/quick_ocr_doc_converter.git
cd quick_ocr_doc_converter

# Install Python dependencies
pip install -r requirements.txt

# Set up OCR environment
python3 setup_ocr_environment.py

# Test installation
python3 universal_document_converter.py
```

### Method 3: Legacy DLL Only (VB6/VFP9)
1. Download: `UniversalConverter32.dll.zip`
2. Extract and run `install.bat`
3. Use `dll_builder_cli.py` for building

---

## 🎯 Which Tool Should I Use?

### **For Most Users:** Main GUI Application
- **Best choice** if you want all features
- **Complete OCR** and document conversion
- **User-friendly** tabbed interface

### **For OCR Only:** Specialized OCR GUI  
- **Perfect** if you only need text extraction
- **Lighter** than main GUI
- **Focused** on OCR tasks

### **For Automation:** Document Converter CLI
- **Best for scripts** and batch processing
- **No OCR** - basic conversion only
- **System integration** friendly

### **For Legacy Systems:** DLL Builder CLI
- **Essential** for VB6/VFP9 integration
- **Real DLL compilation**
- **Enterprise legacy** support

### **For Background Tasks:** System Tray App
- **Always available** in system tray
- **Minimal resource** usage
- **Quick access** to functions

---

## 🚀 Quick Reference

### Main GUI Tabs:
1. **📄 Document Conversion** - File conversion interface
2. **👁 OCR Processing** - OCR engine configuration  
3. **📝 Markdown** - Markdown tools and conversion
4. **🌐 API** - Cloud service API management
5. **🔧 Tools** - Additional utilities
6. **⚙️ Settings** - Application configuration

### CLI Quick Commands:
```bash
# GUI Applications
python3 universal_document_converter.py     # Main GUI
python3 gui_ocr.py                          # OCR GUI

# CLI Tools  
python3 dll_builder_cli.py --help           # DLL builder help
python3 legacy_dll_builder/document_converter_cli.py --help  # Converter help

# Utilities
python3 setup_ocr_environment.py            # Setup
python3 build_ocr_packages.py              # Build packages
```

---

## 🆘 Troubleshooting

### Common Issues:

**"python3 not found"**
- Install Python 3.8+ from python.org
- Ensure Python is in system PATH

**"Tesseract not found"**
- Install Tesseract OCR
- Run `install_tesseract.bat` (Windows)

**"Module not found"**
- Run: `pip install -r requirements.txt`
- Check Python virtual environment

**DLL compilation fails**
- Ensure Visual Studio Build Tools installed
- Run `dll_builder_cli.py requirements`

### Get Help:
- Check `TROUBLESHOOTING.md`
- Review logs in application directories
- Submit issues on GitHub repository

---

## 📈 Version Information

**Current Version:** 3.1.0  
**Python Required:** 3.8+  
**Status:** Production Ready  
**License:** MIT  

**Package Downloads:**
- Complete Application: `Universal-Document-Converter-v3.1.0-Windows-Complete.zip`
- Legacy DLL Only: `UniversalConverter32.dll.zip`

---

*This comprehensive guide covers all tools in the Universal Document Converter suite. For specific feature documentation, see individual README files in component directories.*