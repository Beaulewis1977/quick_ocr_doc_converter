# Legacy DLL Builder for VB6/VFP9 Integration

A standalone 32-bit DLL builder and integration system for Visual Basic 6 and Visual FoxPro 9 applications. This module has been separated from the main Universal Document Converter to provide a clean, focused solution for legacy system integration.

## Overview

The Legacy DLL Builder provides:
- 32-bit Windows DLL creation for VB6/VFP9 compatibility
- Production-ready integration templates
- Automated build process with compiler detection
- Comprehensive testing utilities

## Quick Start

### Requirements

- **Windows**: Required for DLL building
- **Python**: 3.8 or higher
- **Compiler**: One of the following:
  - Visual Studio 2017/2019/2022 with C++ support
  - Visual Studio Build Tools
  - MinGW-w64 (alternative)

### Installation

1. Clone or extract this directory
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Click (if not already installed):
   ```bash
   pip install click
   ```

### Basic Usage

#### Check DLL Status
```bash
python document_converter_cli.py status
```

#### Build the DLL
```bash
python document_converter_cli.py build
```

#### Generate Integration Templates
```bash
# For VB6
python document_converter_cli.py vb6 generate

# For VFP9
python document_converter_cli.py vfp9 generate
```

## Advanced CLI (Click-based)

A new enhanced CLI with better error handling and configuration support is available:

### Verify Build Tools
```bash
python dll_builder_advanced_cli.py verify-tools
```

### Build with Configuration
```bash
python dll_builder_advanced_cli.py build --source dll_source --output UniversalConverter32.dll --timeout 300
```

### Generate Templates
```bash
python dll_builder_advanced_cli.py generate-template vb6 --output MyProject.bas
python dll_builder_advanced_cli.py generate-template vfp9 --output MyProject.prg
```

### Show Configuration Options
```bash
python dll_builder_advanced_cli.py show-config
```

## Configuration

Create a `config.json` file for custom settings:

```json
{
  "compiler": {
    "type": "auto",
    "build_timeout": 300,
    "paths": {
      "vs_path": "C:\\Program Files\\Microsoft Visual Studio\\2022",
      "mingw_path": "C:\\mingw64\\bin"
    }
  },
  "dll": {
    "source_dir": "dll_source",
    "output_dir": "dist",
    "name": "UniversalConverter32.dll"
  },
  "python": {
    "executable": "python",
    "cli_path": "document_converter_cli.py"
  }
}
```

## DLL Functions

The compiled DLL exports the following functions:

### Core Functions
- `ConvertDocument(inputFile, outputFile, inputFormat, outputFormat)` - Main conversion function
- `TestConnection()` - Test if the converter system is available
- `GetVersion()` - Get DLL version
- `GetLastError()` - Get last error message

### Format-Specific Functions
- `ConvertPDFToText(inputFile, outputFile)`
- `ConvertPDFToMarkdown(inputFile, outputFile)`
- `ConvertDOCXToText(inputFile, outputFile)`
- `ConvertDOCXToMarkdown(inputFile, outputFile)`
- `ConvertMarkdownToHTML(inputFile, outputFile)`
- `ConvertHTMLToMarkdown(inputFile, outputFile)`
- `ConvertRTFToText(inputFile, outputFile)`
- `ConvertRTFToMarkdown(inputFile, outputFile)`

### Information Functions
- `GetSupportedInputFormats()` - Returns: "pdf,docx,txt,html,rtf,md,markdown"
- `GetSupportedOutputFormats()` - Returns: "txt,md,html,json"

## VB6 Integration Example

```vb
' Declare DLL functions
Private Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String, _
     ByVal inputFormat As String, ByVal outputFormat As String) As Long

Private Declare Function GetLastError Lib "UniversalConverter32.dll" () As String

' Use the converter
Dim result As Long
result = ConvertDocument("C:\input.pdf", "C:\output.txt", "pdf", "txt")

If result = 1 Then
    MsgBox "Conversion successful!"
Else
    MsgBox "Conversion failed: " & GetLastError()
End If
```

## VFP9 Integration Example

```foxpro
* Declare DLL functions
DECLARE LONG ConvertDocument IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, ;
    STRING inputFormat, STRING outputFormat

DECLARE STRING GetLastError IN UniversalConverter32.dll

* Use the converter
LOCAL lnResult
lnResult = ConvertDocument("C:\input.pdf", "C:\output.txt", "pdf", "txt")

IF lnResult = 1
    MESSAGEBOX("Conversion successful!")
ELSE
    MESSAGEBOX("Conversion failed: " + GetLastError())
ENDIF
```

## Testing

### Run DLL Tests
```bash
python document_converter_cli.py test all
```

### Test Specific Functions
```bash
python document_converter_cli.py test functions
python document_converter_cli.py test conversion --file test.pdf
python document_converter_cli.py test performance --file test.pdf --iterations 10
```

## Troubleshooting

### Compiler Not Found
If you get a "No compiler found" error:

1. **Install Visual Studio Build Tools**:
   - Download from: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
   - Install with "Desktop development with C++" workload
   - Include "MSVC v143 - VS 2022 C++ x64/x86 build tools"

2. **Or install MinGW-w64**:
   - Download from: https://www.mingw-w64.org/downloads/
   - Install with i686 (32-bit) support
   - Add to system PATH

### DLL Not Loading in VB6/VFP9
1. Ensure the DLL is 32-bit (use `dumpbin /headers UniversalConverter32.dll`)
2. Place `document_converter_cli.py` in the same directory as the DLL
3. Ensure Python is in system PATH
4. Check Windows Defender hasn't quarantined the DLL

### Python CLI Not Found
The DLL requires the Python CLI script (`document_converter_cli.py`) to be in the same directory. This is the simple document converter that the DLL calls.

## Architecture

```
legacy_dll_builder/
├── document_converter_cli.py # Main CLI interface
├── dll_builder_advanced_cli.py # Enhanced Click-based CLI
├── requirements.txt         # Python dependencies
├── config.json.example      # Configuration template
├── dll_source/              # C++ DLL source code
│   ├── UniversalConverter32.cpp
│   ├── UniversalConverter32.def
│   └── Makefile
├── src/
│   ├── cli.py              # Simple document converter
│   └── commands/           # CLI command implementations
│       ├── build.py        # DLL building logic
│       ├── integration.py  # VB6/VFP9 integration
│       └── testing.py      # Testing utilities
└── templates/              # Integration templates
    ├── VB6_UniversalConverter_Production.bas
    └── VFP9_UniversalConverter_Production.prg
```

## Security Notes

- The DLL uses `_popen()` to execute Python scripts
- Input paths should be validated before passing to the DLL
- Consider signing the DLL for production use
- Restrict DLL placement to secure directories

## License

This component is part of the Universal Document Converter project and follows the same license terms.