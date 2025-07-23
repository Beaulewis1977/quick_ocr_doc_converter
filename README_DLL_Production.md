# Universal Document Converter 32-bit DLL
## Production Release v3.1.0

### Overview
This package provides a production-ready 32-bit DLL (`UniversalConverter32.dll`) for integrating document conversion capabilities into legacy VB6 and VFP9 applications. The DLL provides a bridge between legacy applications and modern document conversion technology.

### What's Included

#### Core Components
- **UniversalConverter32.dll** - The main 32-bit DLL for Windows
- **cli.py** - Python CLI backend that powers the conversion
- **requirements.txt** - Python dependencies

#### Integration Modules
- **VB6_UniversalConverter_Production.bas** - Complete VB6 integration module
- **VFP9_UniversalConverter_Production.prg** - Complete VFP9 integration class

#### Build Tools
- **dll_source/UniversalConverter32.cpp** - C++ source code for the DLL
- **dll_source/UniversalConverter32.def** - Module definition file
- **dll_source/build_windows.bat** - Windows build script
- **build_dll.bat** - Master build script

#### Installation & Testing
- **install.bat** - System installation script
- **test_dll.bat** - Test conversion functionality

### System Requirements

#### For Using the DLL
- Windows 7 or later (32-bit or 64-bit)
- Python 3.7 or later
- VB6 or VFP9 development environment

#### For Building the DLL
- Windows development environment
- MinGW-w64 or Visual Studio Build Tools
- Python 3.7+ with required packages

### Installation Instructions

#### Quick Installation
1. Download the complete distribution package
2. Run `install.bat` as Administrator to install the DLL system-wide
3. Test the installation by running `test_dll.bat`

#### Manual Installation
1. Copy `UniversalConverter32.dll` to your project directory
2. Copy `cli.py` and `requirements.txt` to the same directory
3. Install Python dependencies: `pip install -r requirements.txt`
4. Add the VB6 or VFP9 integration module to your project

#### Project-Specific Installation
```cmd
REM Copy DLL and supporting files to your project
copy UniversalConverter32.dll "C:\Your\Project\Directory\"
copy cli.py "C:\Your\Project\Directory\"
copy requirements.txt "C:\Your\Project\Directory\"

REM Install Python dependencies
cd "C:\Your\Project\Directory"
pip install -r requirements.txt
```

### VB6 Integration

#### Adding to Your Project
1. Add `VB6_UniversalConverter_Production.bas` to your VB6 project
2. The module automatically declares all DLL functions
3. Use the provided wrapper functions for easy conversion

#### Basic Usage Example
```vb
' Initialize the converter
If InitializeConverter() Then
    MsgBox "Converter ready! Version: " & GetConverterVersion()
    
    ' Convert a PDF to text
    If PDFToText("C:\documents\file.pdf", "C:\documents\file.txt") Then
        MsgBox "Conversion successful!"
    Else
        MsgBox "Conversion failed: " & GetLastErrorMessage()
    End If
Else
    MsgBox "Converter not available"
End If
```

#### Advanced Usage Example
```vb
' Generic conversion with auto-format detection
Dim success As Boolean
success = ConvertDocumentFile("C:\docs\report.docx", "C:\docs\report.md")

' Batch conversion
Dim convertedCount As Long
convertedCount = ConvertDirectory("C:\PDFs", "C:\Text", "pdf", "txt")
MsgBox "Converted " & convertedCount & " files"
```

### VFP9 Integration

#### Adding to Your Project
1. Include `VFP9_UniversalConverter_Production.prg` in your VFP9 project
2. Use either the class-based or function-based approach

#### Class-Based Usage
```foxpro
* Create converter instance
loConverter = CREATEOBJECT("UniversalConverter")

IF loConverter.lInitialized
    MESSAGEBOX("Converter ready! Version: " + loConverter.GetConverterVersion())
    
    * Convert a document
    llSuccess = loConverter.ConvertDocumentFile("C:\docs\file.pdf", "C:\docs\file.txt")
    
    IF llSuccess
        MESSAGEBOX("Conversion successful!")
    ELSE
        MESSAGEBOX("Error: " + loConverter.cLastError)
    ENDIF
ELSE
    MESSAGEBOX("Converter not available")
ENDIF
```

#### Function-Based Usage
```foxpro
* Simple conversion
IF InitializeConverter()
    llSuccess = ConvertFile("C:\docs\report.docx", "C:\docs\report.txt", "docx", "txt")
    
    IF llSuccess
        MESSAGEBOX("Conversion successful!")
    ELSE
        MESSAGEBOX("Conversion failed!")
    ENDIF
ENDIF
```

### Supported Formats

#### Input Formats
- **PDF** - Portable Document Format
- **DOCX** - Microsoft Word documents
- **TXT** - Plain text files
- **HTML** - Web pages and HTML documents
- **RTF** - Rich Text Format
- **MD/Markdown** - Markdown documents

#### Output Formats
- **TXT** - Plain text
- **MD** - Markdown
- **HTML** - Web page format
- **JSON** - Structured data format

### DLL Functions Reference

#### Core Functions
```c
// Main conversion function
LONG ConvertDocument(const char* inputFile, const char* outputFile, 
                    const char* inputFormat, const char* outputFormat);

// Test system availability
LONG TestConnection();

// Get version information
const char* GetVersion();

// Get error information
const char* GetLastError();
```

#### Convenience Functions
```c
// Format-specific conversions
LONG ConvertPDFToText(const char* inputFile, const char* outputFile);
LONG ConvertPDFToMarkdown(const char* inputFile, const char* outputFile);
LONG ConvertDOCXToText(const char* inputFile, const char* outputFile);
LONG ConvertDOCXToMarkdown(const char* inputFile, const char* outputFile);
LONG ConvertMarkdownToHTML(const char* inputFile, const char* outputFile);
LONG ConvertHTMLToMarkdown(const char* inputFile, const char* outputFile);
LONG ConvertRTFToText(const char* inputFile, const char* outputFile);
LONG ConvertRTFToMarkdown(const char* inputFile, const char* outputFile);
```

#### Information Functions
```c
// Get supported formats
const char* GetSupportedInputFormats();
const char* GetSupportedOutputFormats();

// Get file information
LONG GetFileInfo(const char* filePath, char* infoBuffer, int bufferSize);
```

### Return Codes
- **1 (UC_SUCCESS)** - Operation completed successfully
- **0 (UC_FAILURE)** - Operation failed but system is functional
- **-1 (UC_ERROR)** - System error occurred

### Error Handling

#### Best Practices
1. Always check return codes from DLL functions
2. Use `GetLastError()` to retrieve detailed error messages
3. Validate file paths before attempting conversion
4. Test system availability with `TestConnection()` before use

#### Common Errors
- **Python not available** - Install Python 3.7+
- **CLI script not found** - Ensure `cli.py` is in the DLL directory
- **Input file not found** - Verify file path and permissions
- **Permission denied** - Run with appropriate file permissions

### Building from Source

#### Prerequisites
- Windows development environment
- MinGW-w64 or Visual Studio Build Tools
- Python 3.7+ development headers

#### Build Process
```cmd
REM Clone the repository
git clone [repository_url]
cd repo

REM Build the DLL
build_dll.bat

REM The DLL and distribution package will be created in the dist/ folder
```

#### Manual Build
```cmd
cd dll_source

REM Using MinGW
g++ -m32 -O2 -std=c++17 -shared -DWIN32 -D_WIN32 -DNDEBUG ^
    -Wl,--enable-stdcall-fixup -Wl,--kill-at ^
    -o UniversalConverter32.dll UniversalConverter32.cpp UniversalConverter32.def

REM Using Visual Studio
cl /LD /O2 /DWIN32 /D_WIN32 /DNDEBUG UniversalConverter32.cpp ^
   /Fe:UniversalConverter32.dll /link /DEF:UniversalConverter32.def
```

### Performance Considerations

#### Optimization Tips
- Keep the DLL and CLI script in the same directory for best performance
- Use batch conversion functions for multiple files
- Pre-validate file paths to avoid unnecessary DLL calls
- Cache conversion results when possible

#### Resource Usage
- The DLL itself is lightweight (< 1MB)
- Memory usage depends on document size and complexity
- Python subprocess is created for each conversion operation

### Troubleshooting

#### DLL Not Loading
1. Verify the DLL is 32-bit compatible with your application
2. Check that all dependencies are installed
3. Ensure the DLL is in the correct location

#### Conversion Failures
1. Test with `test_dll.bat` to verify system functionality
2. Check Python installation and dependencies
3. Verify input file format and accessibility
4. Review error messages from `GetLastError()`

#### Python Issues
1. Ensure Python is in the system PATH
2. Install required packages: `pip install -r requirements.txt`
3. Test CLI directly: `python cli.py --help`

### Technical Details

#### Architecture
- **DLL Layer** - C++ wrapper providing Windows-compatible interface
- **CLI Layer** - Python script handling actual document conversion
- **Integration Layer** - VB6/VFP9 modules with error handling and utilities

#### Security Features
- Input validation and path sanitization
- File size limits and type checking
- Error handling prevents system crashes
- No eval() or unsafe operations

#### Threading
- DLL functions are thread-safe
- Multiple conversions can run simultaneously
- Proper resource cleanup and error handling

### License and Support

This software is provided under the terms specified in the LICENSE file. For technical support, integration assistance, or bug reports, please refer to the project documentation.

### Version History

#### v3.1.0 (Current)
- Production-ready 32-bit DLL
- Complete VB6/VFP9 integration modules
- Comprehensive error handling
- Thread-safe operations
- Full format support

---

**Note**: This is a production-ready implementation designed for real-world legacy system integration. All code has been tested for compatibility with VB6 and VFP9 environments.