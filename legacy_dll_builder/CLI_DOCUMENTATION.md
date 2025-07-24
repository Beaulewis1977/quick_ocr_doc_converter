# Legacy CLI System Documentation

## Overview

The legacy CLI system provides command-line interfaces for document conversion and DLL building functionality. It's designed for integration with legacy systems like VB6 and VFP9.

## CLI Tools

### 1. **document_converter_cli.py** - Simple Document Converter

**Purpose**: Basic document conversion for VB6/VFP9 integration

**Usage**:
```bash
python document_converter_cli.py [input] [output] [options]
```

**Options**:
- `-f, --format, -t {txt,md,html,json}` - Output format (default: txt)
- `-o, --output-file` - Output file path
- `-r, --recursive` - Process directories recursively
- `--overwrite` - Overwrite existing files
- `--encoding` - Text encoding (default: utf-8)
- `--line-endings {windows,unix,mac}` - Line ending style
- `-v, --verbose` - Enable verbose logging
- `-q, --quiet` - Suppress output except errors

**Examples**:
```bash
# Convert PDF to text
python document_converter_cli.py document.pdf output.txt

# Convert DOCX to markdown
python document_converter_cli.py document.docx output.md -f md

# Convert entire directory
python document_converter_cli.py input_dir/ output_dir/ --recursive

# Show supported formats
python document_converter_cli.py --formats
```

**Supported Input Formats**:
- PDF (.pdf)
- Word Documents (.docx, .doc)
- Text Files (.txt)
- HTML Files (.html, .htm)
- Rich Text Format (.rtf)
- Markdown (.md)
- EPUB (.epub)

**Supported Output Formats**:
- Plain Text (.txt)
- Markdown (.md)
- HTML (.html)
- JSON (.json)

### 2. **dll_builder_advanced_cli.py** - Legacy DLL Builder

**Purpose**: Build 32-bit DLLs for VB6/VFP9 integration

**Usage**:
```bash
python dll_builder_advanced_cli.py [COMMAND] [OPTIONS]
```

**Commands**:

#### `build` - Build 32-bit DLL from source
```bash
python dll_builder_advanced_cli.py build --source dll_source/UniversalConverter32.cpp
```

Options:
- `--source` - Source C++ file
- `--output` - Output DLL name
- `--compiler` - Compiler to use (gcc, msvc)
- `--arch` - Architecture (x86, x64)

#### `generate-template` - Generate VB6/VFP9 integration templates
```bash
python dll_builder_advanced_cli.py generate-template --type vb6 --output MyModule.bas
```

Options:
- `--type {vb6,vfp9}` - Template type
- `--output` - Output file path
- `--functions` - Functions to include

#### `show-config` - Show build configuration options
```bash
python dll_builder_advanced_cli.py show-config
```

#### `test` - Test DLL functionality
```bash
python dll_builder_advanced_cli.py test --dll UniversalConverter32.dll
```

#### `verify-tools` - Verify compiler tools are available
```bash
python dll_builder_advanced_cli.py verify-tools
```

### 3. **dll_builder_cli.py** - Compatibility Redirect

**Purpose**: Backward compatibility redirect to the correct CLI tools

This file exists for users who expect the old filename. It will:
1. Show a notice about the new CLI structure
2. Suggest the correct command based on arguments
3. Exit with instructions

## Integration Examples

### VB6 Integration

1. **Build the DLL**:
```bash
python dll_builder_advanced_cli.py build
```

2. **Generate VB6 module**:
```bash
python dll_builder_advanced_cli.py generate-template --type vb6
```

3. **Use in VB6**:
```vb
' Include the generated module
' UniversalConverter.bas

Private Sub ConvertDocument()
    Dim result As String
    result = ConvertFile("input.pdf", "output.txt", "txt")
    If result = "Success" Then
        MsgBox "Conversion completed!"
    End If
End Sub
```

### VFP9 Integration

1. **Generate VFP9 template**:
```bash
python dll_builder_advanced_cli.py generate-template --type vfp9
```

2. **Use in VFP9**:
```foxpro
* Load the DLL
DECLARE ConvertFile IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, STRING format

* Convert a file
lcResult = ConvertFile("input.pdf", "output.txt", "txt")
IF lcResult = "Success"
    MESSAGEBOX("Conversion completed!")
ENDIF
```

## Batch Processing

### Using the CLI in Scripts

**Windows Batch Script**:
```batch
@echo off
REM Convert all PDFs in a folder
for %%f in (*.pdf) do (
    python document_converter_cli.py "%%f" "%%~nf.txt"
)
```

**PowerShell Script**:
```powershell
# Convert documents with error handling
Get-ChildItem -Filter *.pdf | ForEach-Object {
    $output = $_.BaseName + ".txt"
    python document_converter_cli.py $_.FullName $output
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Converted: $_" -ForegroundColor Green
    } else {
        Write-Host "Failed: $_" -ForegroundColor Red
    }
}
```

**Linux/macOS Shell Script**:
```bash
#!/bin/bash
# Batch convert with progress
total=$(ls *.pdf 2>/dev/null | wc -l)
current=0

for file in *.pdf; do
    if [ -f "$file" ]; then
        ((current++))
        echo "[$current/$total] Converting $file..."
        python document_converter_cli.py "$file" "${file%.pdf}.txt"
    fi
done
```

## Configuration

### Config File (config.json)

Create a `config.json` in the same directory:

```json
{
    "conversion": {
        "default_format": "txt",
        "encoding": "utf-8",
        "preserve_formatting": true,
        "line_endings": "windows"
    },
    "dll_builder": {
        "compiler": "gcc",
        "architecture": "x86",
        "optimization": "-O2",
        "include_debug": false
    },
    "logging": {
        "level": "INFO",
        "file": "conversion.log"
    }
}
```

### Environment Variables

- `CONVERTER_CONFIG` - Path to config file
- `CONVERTER_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `CONVERTER_OUTPUT_DIR` - Default output directory

## Error Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Invalid arguments |
| 2 | Input file not found |
| 3 | Output directory not writable |
| 4 | Unsupported format |
| 5 | Conversion failed |
| 6 | DLL build failed |
| 7 | Missing dependencies |

## Troubleshooting

### Common Issues

1. **"Python not found"**
   - Ensure Python 3.8+ is installed and in PATH
   - Try using `python3` instead of `python`

2. **"Module not found"**
   - Install requirements: `pip install -r requirements.txt`
   - Check you're in the correct directory

3. **"DLL build failed"**
   - Install MinGW-w64 or Visual Studio
   - Run `verify-tools` command to check

4. **"Conversion failed"**
   - Check input file is not corrupted
   - Verify output directory exists and is writable
   - Check logs for specific error

### Debug Mode

Enable debug logging:
```bash
python document_converter_cli.py input.pdf output.txt --verbose
```

Or set environment variable:
```bash
export CONVERTER_LOG_LEVEL=DEBUG
```

## Performance Tips

1. **Batch Processing**: Process multiple files in one command
2. **Use Native Formats**: TXT to TXT is fastest
3. **Disable Logging**: Use `--quiet` for production
4. **Parallel Processing**: Use GNU Parallel or similar tools

## Security Considerations

1. **Input Validation**: All inputs are sanitized
2. **Path Traversal**: Protected against directory traversal attacks
3. **File Size Limits**: Default 100MB limit (configurable)
4. **Sandboxing**: Consider running in isolated environment

## Support

For issues or questions:
1. Check this documentation
2. Review error messages and logs
3. Contact: blewisxx@gmail.com