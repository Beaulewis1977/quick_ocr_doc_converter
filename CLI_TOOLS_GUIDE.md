# 📚 Complete CLI Tools Guide for OCR Document Converter

## 🎯 Table of Contents
- [Overview of CLI Tools](#overview-of-cli-tools)
- [Legacy VB6/VFP9 Integration System](#legacy-vb6vfp9-integration-system)
- [Installation Guide for Legacy Systems](#installation-guide-for-legacy-systems)
- [Step-by-Step Usage Instructions](#step-by-step-usage-instructions)
- [All Available CLI Tools](#all-available-cli-tools)
- [Troubleshooting](#troubleshooting)

---

## 🔍 Overview of CLI Tools

This project includes **8 main CLI tools** designed for different purposes:

### 🏛️ **Legacy System Integration (VB6/VFP9)**
1. **dll_builder_cli.py** - Main 32-bit DLL builder for VB6/VFP9
2. **document_converter_cli.py** - Document converter that works with the DLL
3. **dll_builder_advanced_cli.py** - Enhanced DLL builder with Click framework

### 📄 **Document Conversion Tools**
4. **convert_to_markdown.py** - Convert DOCX/PDF/TXT to Markdown
5. **convert_recursive.py** - Recursive document converter with folder structure

### 🚀 **Development & Testing**
6. **run_benchmarks.py** - Performance benchmarking tool
7. **build_all_platforms.py** - Cross-platform package builder
8. **launch_ocr.py** - GUI launcher (not really a CLI tool)

---

## 🏛️ Legacy VB6/VFP9 Integration System

### **What It Does**
The legacy DLL builder creates a **32-bit Windows DLL** that allows Visual Basic 6 and Visual FoxPro 9 applications to:
- Convert documents (PDF, DOCX, RTF, HTML, TXT) to various formats
- Extract text from documents
- Process documents without requiring Python installation on end-user machines
- Integrate modern document conversion into legacy applications

### **Key Features**
- ✅ True 32-bit DLL for legacy compatibility
- ✅ No Python required on target machines
- ✅ Simple function calls from VB6/VFP9
- ✅ Error handling and status reporting
- ✅ Production-ready templates included
- ✅ Comprehensive test suite
- ✅ Multiple output formats (TXT, Markdown, HTML, JSON)

---

## 📦 Installation Guide for Legacy Systems

### **Prerequisites**
1. **Windows OS** (Windows 7 or later)
2. **Python 3.8+** (for building, not for deployment)
3. **C++ Compiler** (one of these):
   - Visual Studio 2017/2019/2022 with C++ support
   - Visual Studio Build Tools
   - MinGW-w64 (alternative)

### **Required Files (In Order)**

1. **Core Files**:
   ```
   legacy_dll_builder/
   ├── document_converter_cli.py    # Main converter CLI (required)
   ├── dll_builder_cli.py          # DLL builder
   ├── requirements.txt            # Python dependencies
   └── dll_source/                 # C++ source code
       ├── UniversalConverter32.cpp
       ├── UniversalConverter32.def
       └── Makefile
   ```

2. **Supporting Files**:
   ```
   ├── src/
   │   ├── cli.py                 # Document converter implementation
   │   └── commands/              # Build commands
   └── templates/                 # VB6/VFP9 templates
       ├── VB6_UniversalConverter_Production.bas
       └── VFP9_UniversalConverter_Production.prg
   ```

### **Installation Steps**

```bash
# 1. Navigate to the legacy DLL builder directory
cd legacy_dll_builder

# 2. Install Python dependencies
pip install -r requirements.txt
pip install click colorama

# 3. Verify your build tools are installed
python dll_builder_cli.py status

# 4. Build the 32-bit DLL
python dll_builder_cli.py build

# 5. Test the DLL
python dll_builder_cli.py test all

# 6. Generate VB6/VFP9 integration code
python dll_builder_cli.py vb6 generate
python dll_builder_cli.py vfp9 generate

# 7. Create distribution package
python dll_builder_cli.py package
```

---

## 📖 Step-by-Step Usage Instructions

### **For VB6 Integration**

1. **Copy Required Files to Your VB6 Project**:
   - `UniversalConverter32.dll`
   - `document_converter_cli.py`
   - `VB6_UniversalConverter_Production.bas` (generated template)

2. **Add the .bas Module to Your VB6 Project**:
   - Project → Add Module → Existing → Select the .bas file

3. **Use in Your VB6 Code**:
   ```vb
   ' Test the connection
   If TestConverterConnection() Then
       MsgBox "Converter is ready!"
   End If
   
   ' Convert a PDF to text
   Dim success As Boolean
   success = ConvertPDFToText("C:\input.pdf", "C:\output.txt")
   
   If success Then
       MsgBox "Conversion successful!"
   Else
       MsgBox "Error: " & GetLastConverterError()
   End If
   ```

### **For VFP9 Integration**

1. **Copy Required Files to Your VFP9 Project Directory**:
   - `UniversalConverter32.dll`
   - `document_converter_cli.py`
   - `VFP9_UniversalConverter_Production.prg` (generated template)

2. **Add to Your VFP9 Project**:
   ```foxpro
   SET PROCEDURE TO VFP9_UniversalConverter_Production.prg ADDITIVE
   ```

3. **Use in Your VFP9 Code**:
   ```foxpro
   * Create converter object
   oConverter = CREATEOBJECT("UniversalDocumentConverter")
   
   * Test connection
   IF oConverter.TestConnection()
       MESSAGEBOX("Converter is ready!")
   ENDIF
   
   * Convert a document
   IF oConverter.ConvertDocument("C:\input.pdf", "C:\output.txt", "pdf", "txt")
       MESSAGEBOX("Conversion successful!")
   ELSE
       MESSAGEBOX("Error: " + oConverter.GetLastError())
   ENDIF
   ```

---

## 🛠️ All Available CLI Tools

### **1. dll_builder_cli.py** (Main DLL Builder)
```bash
# Check status
python dll_builder_cli.py status

# Build DLL
python dll_builder_cli.py build

# Run tests
python dll_builder_cli.py test all
python dll_builder_cli.py test functions
python dll_builder_cli.py test conversion --file sample.pdf

# Generate integration code
python dll_builder_cli.py vb6 generate
python dll_builder_cli.py vfp9 generate

# Create package
python dll_builder_cli.py package

# Install system-wide
python dll_builder_cli.py install
```

### **2. document_converter_cli.py** (Document Converter)
```bash
# Convert single file
python document_converter_cli.py input.pdf output.txt

# Specify format
python document_converter_cli.py input.pdf output.md --format markdown

# Convert directory recursively
python document_converter_cli.py input_dir/ output_dir/ --recursive

# Use specific encoding
python document_converter_cli.py input.txt output.txt --encoding utf-8

# Windows line endings for VB6/VFP9
python document_converter_cli.py input.txt output.txt --line-endings windows
```

### **3. dll_builder_advanced_cli.py** (Enhanced Builder)
```bash
# Verify tools
python dll_builder_advanced_cli.py verify-tools

# Build with options
python dll_builder_advanced_cli.py build --compiler vs --timeout 300

# Generate templates
python dll_builder_advanced_cli.py generate-template vb6 --output MyModule.bas
python dll_builder_advanced_cli.py generate-template vfp9 --output MyClass.prg

# Show configuration
python dll_builder_advanced_cli.py show-config

# Test DLL
python dll_builder_advanced_cli.py test --dll-path UniversalConverter32.dll
```

### **4. convert_to_markdown.py** (Markdown Converter)
```bash
# Convert single file
python convert_to_markdown.py document.pdf -o output.md

# Convert directory
python convert_to_markdown.py documents/ -o markdown/

# Install dependencies first
python convert_to_markdown.py --install
```

### **5. convert_recursive.py** (Recursive Converter)
```bash
# Convert with folder structure
python convert_recursive.py input_folder/ -o output_folder/

# Flatten output (no subdirectories)
python convert_recursive.py input_folder/ -o output_folder/ --flat
```

### **6. run_benchmarks.py** (Performance Testing)
```bash
# Run all benchmarks
python run_benchmarks.py --benchmarks all

# Specific benchmarks
python run_benchmarks.py --benchmarks file-size
python run_benchmarks.py --benchmarks format
python run_benchmarks.py --benchmarks batch
python run_benchmarks.py --benchmarks memory

# Custom output directory
python run_benchmarks.py --output-dir results/
```

### **7. build_all_platforms.py** (Package Builder)
```bash
# Build for all platforms
python build_all_platforms.py --platform all

# Build for specific platform
python build_all_platforms.py --platform windows
python build_all_platforms.py --platform linux
python build_all_platforms.py --platform macos

# Specify version
python build_all_platforms.py --version 3.1.0 --platform windows
```

---

## 🔧 Troubleshooting

### **Common Issues**

1. **"No compiler found" Error**:
   - Install Visual Studio Build Tools 2022
   - Or install MinGW-w64
   - Run `python dll_builder_cli.py status` to check

2. **DLL Won't Load in VB6/VFP9**:
   - Ensure it's a 32-bit DLL (check with `dumpbin /headers UniversalConverter32.dll`)
   - Place `document_converter_cli.py` in same directory as DLL
   - Check if Windows Defender quarantined the DLL

3. **"Python not found" from DLL**:
   - Add Python to system PATH
   - Or specify full path in config.json

4. **Conversion Fails**:
   - Check input file exists and is readable
   - Ensure output directory exists
   - Check file format is supported
   - Look at error message from `GetLastError()`

### **Testing Your Setup**

```bash
# 1. Test Python CLI directly
python document_converter_cli.py test.pdf test.txt

# 2. Test DLL functions
python dll_builder_cli.py test functions

# 3. Test from VB6/VFP9
# Use the TestConnection() function first
```

---

## 🎉 Demo Script for Your Friend

Here's a quick demo sequence to show your friend:

```bash
# 1. Show the status
python dll_builder_cli.py status

# 2. Build the DLL (if needed)
python dll_builder_cli.py build

# 3. Run tests to show it works
python dll_builder_cli.py test all

# 4. Convert a sample document
python document_converter_cli.py sample.pdf output.txt

# 5. Show the VB6 code template
type templates\VB6_UniversalConverter_Production.bas

# 6. Show the VFP9 code template  
type templates\VFP9_UniversalConverter_Production.prg
```

Then open VB6 or VFP9 and show the integration working live!

---

## 📞 Support

The DLL builder has been tested with:
- Visual Basic 6.0 SP6
- Visual FoxPro 9.0 SP2
- Windows 7, 8, 10, 11 (32-bit and 64-bit OS)

For modern applications, use the main GUI or the OCR-enabled CLI tools instead.