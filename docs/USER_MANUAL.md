# Universal Document Converter v2.1.0 - User Manual

Welcome to the complete user manual for Universal Document Converter. This guide covers all features, interfaces, and usage scenarios.

## Table of Contents

1. [Getting Started](#getting-started)
2. [GUI Application Guide](#gui-application-guide)
3. [Command Line Interface (CLI)](#command-line-interface-cli)
4. [Supported Formats](#supported-formats)
5. [OCR Features](#ocr-features)
6. [Batch Processing](#batch-processing)
7. [Markdown Conversion](#markdown-conversion)
8. [VFP9/VB6 Integration](#vfp9vb6-integration)
9. [Python API](#python-api)
10. [Advanced Features](#advanced-features)
11. [Performance Optimization](#performance-optimization)
12. [Troubleshooting](#troubleshooting)

## Getting Started

### Quick Start (GUI)
1. Launch the application:
   - Windows: Double-click `run_converter.bat`
   - macOS/Linux: Run `python universal_document_converter_ocr.py`
2. Drag and drop files onto the window
3. Select output format from dropdown
4. Click "Convert" or files convert automatically

### Quick Start (CLI)
```bash
# Simple conversion
python universal_document_converter_ocr.py input.pdf output.docx

# With OCR
python universal_document_converter_ocr.py scan.pdf text.txt --ocr

# Batch convert folder
python universal_document_converter_ocr.py /docs /output --batch --format pdf
```

## GUI Application Guide

### Main Window Features

#### 1. Drag & Drop Area
- **Single File**: Drag one file to convert it
- **Multiple Files**: Drag multiple files for batch conversion
- **Folders**: Drag entire folders (processes all supported files)

#### 2. Control Panel
- **Input Format**: Auto-detected or manually selectable
- **Output Format**: Dropdown with all supported formats
- **OCR Toggle**: Enable/disable OCR processing
- **Options Button**: Access advanced settings

#### 3. Progress Display
- **Overall Progress**: Shows total batch progress
- **Current File**: Displays file being processed
- **Time Remaining**: Estimated completion time
- **Cancel Button**: Stop current operation

### Menu Options

#### File Menu
- **Open File(s)**: Browse for files to convert
- **Open Folder**: Select folder for batch processing
- **Recent Files**: Quick access to recent conversions
- **Exit**: Close application

#### Edit Menu
- **Preferences**: Application settings
- **Clear History**: Remove recent files list
- **Reset Settings**: Restore defaults

#### Tools Menu
- **OCR Settings**: Configure OCR languages and engines
- **Batch Settings**: Configure batch processing options
- **Format Options**: Format-specific settings

#### Help Menu
- **User Manual**: Open this guide
- **Keyboard Shortcuts**: View shortcuts
- **Check for Updates**: Check for new versions
- **About**: Version and license information

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| Ctrl+O | Open files |
| Ctrl+Shift+O | Open folder |
| Ctrl+V | Paste files from clipboard |
| Ctrl+Q | Quit application |
| F1 | Open help |
| F5 | Refresh file list |
| Space | Start/pause conversion |
| Esc | Cancel operation |

## Command Line Interface (CLI)

### Basic Syntax
```bash
python universal_document_converter_ocr.py [INPUT] [OUTPUT] [OPTIONS]
```

### Common Commands

#### Single File Conversion
```bash
# Auto-detect formats
python universal_document_converter_ocr.py input.docx output.pdf

# Specify formats explicitly
python universal_document_converter_ocr.py input.file output.file -if docx -of pdf

# With OCR enabled
python universal_document_converter_ocr.py scan.pdf text.docx --ocr
```

#### Batch Conversion
```bash
# Convert all files in directory
python universal_document_converter_ocr.py /input/dir /output/dir --batch

# Specific format only
python universal_document_converter_ocr.py /docs /pdfs --batch --pattern "*.docx" --format pdf

# Recursive with subdirectories
python universal_document_converter_ocr.py /docs /output --batch --recursive
```

#### OCR Processing
```bash
# Basic OCR
python universal_document_converter_ocr.py image.png text.txt --ocr

# Multiple languages
python universal_document_converter_ocr.py scan.pdf text.txt --ocr --ocr-lang eng+fra+deu

# With preprocessing
python universal_document_converter_ocr.py poor_scan.pdf text.docx --ocr --preprocess

# Choose OCR engine
python universal_document_converter_ocr.py scan.pdf text.txt --ocr --ocr-engine easyocr
```

### Complete CLI Options

```
Options:
  -h, --help            Show help message and exit
  -v, --version         Show version number
  
Input/Output:
  -if, --input-format   Input format (auto-detected if not specified)
  -of, --output-format  Output format (required for batch mode)
  --format FORMAT       Shorthand for output format
  
OCR Options:
  --ocr                 Enable OCR processing
  --ocr-lang LANGS      OCR languages (e.g., eng+fra+deu)
  --ocr-engine ENGINE   OCR engine: tesseract or easyocr
  --preprocess          Preprocess images for better OCR
  --deskew              Deskew tilted images
  --denoise             Remove noise from images
  
Batch Options:
  --batch               Process entire directory
  --recursive           Include subdirectories
  --pattern PATTERN     File pattern (e.g., "*.pdf")
  --exclude PATTERN     Exclude pattern
  --parallel N          Number of parallel workers
  
Quality Options:
  --quality QUALITY     Output quality: low, medium, high
  --dpi DPI            DPI for image outputs (default: 300)
  --compress           Compress output files
  --optimize           Optimize for file size
  
Document Options:
  --merge              Merge multiple inputs into one
  --split              Split multi-page documents
  --pages RANGE        Page range (e.g., 1-10,15,20-25)
  --password PASS      Password for encrypted PDFs
  --encrypt PASS       Encrypt output PDF
  
Processing Options:
  --preserve-formatting Keep original formatting
  --preserve-metadata   Keep document metadata
  --strip-images       Remove images from output
  --extract-images     Extract images to separate files
  --watermark FILE     Add watermark image/text
  
Output Options:
  --overwrite          Overwrite existing files
  --timestamp          Add timestamp to filenames
  --organize           Organize by format in subdirs
  --verbose            Detailed output
  --quiet              Suppress output
  --log FILE           Log to file
```

### CLI Examples

#### Advanced Conversions
```bash
# Convert specific pages with watermark
python universal_document_converter_ocr.py input.pdf output.pdf --pages 1-10 --watermark logo.png

# Merge multiple files
python universal_document_converter_ocr.py file1.pdf file2.docx file3.rtf merged.pdf --merge

# Split large document
python universal_document_converter_ocr.py large.pdf output_dir --split --pages-per-file 50

# Password-protected PDF
python universal_document_converter_ocr.py encrypted.pdf output.docx --password "secret123"

# Create encrypted PDF
python universal_document_converter_ocr.py input.docx secure.pdf --encrypt "newpass123"
```

#### Batch Processing Examples
```bash
# Convert all Word docs to PDF with timestamp
python universal_document_converter_ocr.py /docs /pdfs --batch --pattern "*.doc*" --format pdf --timestamp

# OCR all images in folder
python universal_document_converter_ocr.py /scans /text --batch --pattern "*.png,*.jpg" --format txt --ocr

# Recursive conversion with organization
python universal_document_converter_ocr.py /documents /converted --batch --recursive --organize

# Parallel processing
python universal_document_converter_ocr.py /input /output --batch --parallel 4
```

## Supported Formats

### Input Formats
| Format | Extensions | Description | OCR Support |
|--------|------------|-------------|-------------|
| **PDF** | .pdf | Portable Document Format | ✅ Yes |
| **Word** | .docx, .doc | Microsoft Word | ❌ No |
| **RTF** | .rtf | Rich Text Format | ❌ No |
| **HTML** | .html, .htm | Web Pages | ❌ No |
| **Text** | .txt | Plain Text | ❌ No |
| **Markdown** | .md, .markdown | Markdown Files | ❌ No |
| **EPUB** | .epub | E-book Format | ❌ No |
| **ODT** | .odt | OpenDocument Text | ❌ No |
| **Images** | .png, .jpg, .jpeg, .tiff, .bmp | Image Files | ✅ Yes |

### Output Formats
| Format | Extension | Best For |
|--------|-----------|----------|
| **PDF** | .pdf | Preserving layout, sharing |
| **Word** | .docx | Editing, collaboration |
| **RTF** | .rtf | Compatible rich text |
| **HTML** | .html | Web publishing |
| **Text** | .txt | Plain text extraction |
| **Markdown** | .md | Documentation, notes |
| **EPUB** | .epub | E-books |

### Format-Specific Features

#### PDF Options
- Password protection
- Encryption
- Compression levels
- Page manipulation
- Form preservation
- Annotations

#### Word Options
- Style preservation
- Table formatting
- Header/footer support
- Track changes removal
- Template support

#### Markdown Options
- GitHub Flavored Markdown
- Table support
- Code block syntax
- Front matter preservation
- Wiki links

## OCR Features

### OCR Engines

#### Tesseract OCR
- **Pros**: Fast, accurate for printed text, 100+ languages
- **Cons**: Requires separate installation
- **Best for**: Scanned documents, clear text

#### EasyOCR
- **Pros**: Better for handwriting, GPU acceleration
- **Cons**: Larger download, slower CPU processing
- **Best for**: Mixed content, poor quality scans

### Language Support

Common languages with codes:
| Language | Code | Language | Code |
|----------|------|----------|------|
| English | eng | Spanish | spa |
| French | fra | German | deu |
| Italian | ita | Portuguese | por |
| Russian | rus | Chinese (Simplified) | chi_sim |
| Japanese | jpn | Korean | kor |
| Arabic | ara | Hindi | hin |

### OCR Best Practices

1. **Image Quality**
   - Use 300 DPI or higher
   - Ensure good contrast
   - Avoid skewed images

2. **Preprocessing**
   ```bash
   # Enable all preprocessing
   python universal_document_converter_ocr.py scan.pdf text.txt --ocr --preprocess --deskew --denoise
   ```

3. **Language Selection**
   ```bash
   # Multiple languages improve accuracy
   python universal_document_converter_ocr.py multilingual.pdf text.txt --ocr --ocr-lang eng+fra+deu
   ```

4. **Engine Selection**
   ```bash
   # For handwriting
   python universal_document_converter_ocr.py handwritten.jpg text.txt --ocr --ocr-engine easyocr
   
   # For printed text
   python universal_document_converter_ocr.py scan.pdf text.txt --ocr --ocr-engine tesseract
   ```

## Batch Processing

### GUI Batch Mode

1. **Drag Multiple Files**
   - Select multiple files in Explorer/Finder
   - Drag onto application window
   - All files process sequentially

2. **Folder Processing**
   - Drag entire folder
   - Optionally include subfolders
   - Filter by file type

3. **Queue Management**
   - View processing queue
   - Reorder items
   - Remove items
   - Pause/resume processing

### CLI Batch Mode

#### Basic Batch Conversion
```bash
# Convert directory
python universal_document_converter_ocr.py /input /output --batch

# With specific format
python universal_document_converter_ocr.py /docs /pdfs --batch --format pdf
```

#### Advanced Batch Options
```bash
# Parallel processing (4 workers)
python universal_document_converter_ocr.py /input /output --batch --parallel 4

# Pattern matching
python universal_document_converter_ocr.py /docs /output --batch --pattern "*.doc*,*.rtf"

# Exclude pattern
python universal_document_converter_ocr.py /input /output --batch --exclude "*draft*,*temp*"

# Recursive with organization
python universal_document_converter_ocr.py /docs /converted --batch --recursive --organize
```

### Batch Performance Tips

1. **Use Parallel Processing**
   ```bash
   # Optimal for CPU count
   python universal_document_converter_ocr.py /input /output --batch --parallel $(nproc)
   ```

2. **Memory Management**
   - Large files: Process sequentially
   - Small files: Use more workers
   - Monitor memory usage

3. **Error Handling**
   - Failed conversions logged
   - Processing continues
   - Retry failed items

## Markdown Conversion

### Markdown to Other Formats

#### Markdown → RTF
```bash
python universal_document_converter_ocr.py document.md document.rtf

# With enhanced formatting
python universal_document_converter_ocr.py document.md document.rtf --preserve-formatting
```

#### Markdown → PDF
```bash
python universal_document_converter_ocr.py README.md README.pdf

# With custom styling
python universal_document_converter_ocr.py doc.md doc.pdf --style github
```

#### Markdown → HTML
```bash
python universal_document_converter_ocr.py doc.md doc.html

# With table of contents
python universal_document_converter_ocr.py doc.md doc.html --toc
```

### RTF to Markdown

#### Basic Conversion
```bash
python universal_document_converter_ocr.py document.rtf document.md
```

#### Advanced Options
```bash
# Preserve tables
python universal_document_converter_ocr.py doc.rtf doc.md --preserve-tables

# Extract images
python universal_document_converter_ocr.py doc.rtf doc.md --extract-images
```

### Markdown Features Supported

- **Headings**: All levels (# to ######)
- **Emphasis**: Bold, italic, strikethrough
- **Lists**: Ordered, unordered, nested
- **Links**: Inline and reference style
- **Images**: Inline and reference style
- **Code**: Inline and fenced blocks
- **Tables**: GitHub Flavored Markdown
- **Blockquotes**: Nested quotes
- **Horizontal rules**: ---
- **HTML**: Inline HTML preserved

## VFP9/VB6 Integration

### Overview
Five integration methods available:
1. Command Line Interface
2. JSON File IPC
3. Named Pipes
4. COM Server
5. DLL Wrapper

### Method 1: Command Line Interface

#### VFP9 Example
```foxpro
*!* Simple conversion
lcCmd = "python universal_document_converter_ocr.py input.rtf output.pdf"
RUN /N &lcCmd

*!* With error checking
lcCmd = "python universal_document_converter_ocr.py input.rtf output.pdf"
lnResult = ShellExecute(0, "open", "cmd.exe", "/c " + lcCmd, "", 0)
IF lnResult > 32
    MESSAGEBOX("Conversion started successfully")
ELSE
    MESSAGEBOX("Conversion failed: " + STR(lnResult))
ENDIF
```

#### VB6 Example
```vb
' Simple conversion
Shell "python universal_document_converter_ocr.py input.rtf output.pdf", vbNormalFocus

' With wait for completion
Dim wsh As Object
Set wsh = CreateObject("WScript.Shell")
Dim result As Integer
result = wsh.Run("python universal_document_converter_ocr.py input.rtf output.pdf", 0, True)
If result = 0 Then
    MsgBox "Conversion successful!"
Else
    MsgBox "Conversion failed with code: " & result
End If
```

### Method 2: JSON File IPC

#### VFP9 Implementation
```foxpro
*!* Create request
TEXT TO lcRequest NOSHOW TEXTMERGE
{
    "action": "convert",
    "input_file": "<<lcInputFile>>",
    "output_file": "<<lcOutputFile>>",
    "input_format": "rtf",
    "output_format": "pdf",
    "options": {
        "ocr": false,
        "quality": "high"
    }
}
ENDTEXT

*!* Write request
STRTOFILE(lcRequest, "C:\temp\uc_request.json")

*!* Call converter
RUN /N python universal_document_converter_ocr.py --json-ipc

*!* Read response
DO WHILE !FILE("C:\temp\uc_response.json")
    WAIT WINDOW "Processing..." TIMEOUT 1
ENDDO

lcResponse = FILETOSTR("C:\temp\uc_response.json")
*!* Parse JSON response...
```

#### VB6 Implementation
```vb
' Create request
Dim request As String
request = "{" & vbCrLf & _
    """action"": ""convert""," & vbCrLf & _
    """input_file"": """ & inputFile & """," & vbCrLf & _
    """output_file"": """ & outputFile & """," & vbCrLf & _
    """input_format"": ""rtf""," & vbCrLf & _
    """output_format"": ""pdf""" & vbCrLf & _
    "}"

' Write request
Open "C:\temp\uc_request.json" For Output As #1
Print #1, request
Close #1

' Call converter
Shell "python universal_document_converter_ocr.py --json-ipc"

' Wait and read response
' ... (implement wait loop and JSON parsing)
```

### Method 3: Named Pipes

#### Start Pipe Server
```bash
python pipe_server.py
```

#### VFP9 Client
```foxpro
*!* See VFP9_PipeClient.prg for full implementation
DO VFP9_PipeClient WITH "input.rtf", "output.pdf", "rtf", "pdf"
```

### Method 4: COM Server

#### Register COM Server
```bash
python com_server.py --register
```

#### VB6 Usage
```vb
' Create COM object
Dim converter As Object
Set converter = CreateObject("UniversalConverter.Application")

' Simple conversion
converter.ConvertFile "input.rtf", "output.pdf"

' With options
converter.ConvertFileEx "input.rtf", "output.pdf", "rtf", "pdf", True, "high"

' Batch conversion
Dim files As Variant
files = Array("file1.rtf", "file2.rtf", "file3.rtf")
converter.BatchConvert files, "pdf", "C:\Output"
```

### Method 5: DLL Wrapper

#### VFP9 Usage
```foxpro
*!* Declare DLL functions
DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, ;
    STRING inputFormat, STRING outputFormat

DECLARE INTEGER TestConnection IN UniversalConverter32.dll

*!* Test connection
IF TestConnection() = 1
    *!* Perform conversion
    lnResult = ConvertDocument("input.rtf", "output.pdf", "rtf", "pdf")
    IF lnResult = 1
        MESSAGEBOX("Conversion successful!")
    ENDIF
ENDIF
```

#### VB6 Usage
```vb
' Module declarations (in VB6_UniversalConverter.bas)
Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String, _
     ByVal inputFormat As String, ByVal outputFormat As String) As Long

' Usage in form
Private Sub ConvertFile()
    Dim result As Long
    result = ConvertDocument("input.rtf", "output.pdf", "rtf", "pdf")
    
    Select Case result
        Case 1
            MsgBox "Success!"
        Case 0
            MsgBox "Conversion failed"
        Case -1
            MsgBox "Error occurred"
    End Select
End Sub
```

## Python API

### Basic Usage

```python
from universal_document_converter_ocr import UniversalConverter

# Initialize converter
converter = UniversalConverter("MyApp")

# Simple conversion
converter.convert_file("input.pdf", "output.docx")

# With options
converter.convert_file(
    "scan.pdf",
    "text.docx",
    input_format="pdf",
    output_format="docx",
    ocr_enabled=True,
    ocr_language="eng"
)
```

### Advanced API Usage

#### Batch Processing
```python
# Batch convert with callback
def progress_callback(current, total, filename):
    print(f"Processing {filename}: {current}/{total}")

results = converter.batch_convert(
    input_dir="/documents",
    output_dir="/converted",
    output_format="pdf",
    pattern="*.doc*",
    recursive=True,
    parallel_workers=4,
    progress_callback=progress_callback
)

# Check results
for file, success in results.items():
    if not success:
        print(f"Failed: {file}")
```

#### Custom Processing
```python
# Process with custom options
options = {
    'ocr_enabled': True,
    'ocr_language': 'eng+fra',
    'quality': 'high',
    'dpi': 300,
    'preserve_formatting': True,
    'watermark': 'CONFIDENTIAL'
}

converter.convert_file("input.pdf", "output.docx", **options)
```

#### Format Detection
```python
# Detect format
format_info = converter.detect_format("mystery_file")
print(f"Format: {format_info['format']}")
print(f"Confidence: {format_info['confidence']}")

# Get supported formats
input_formats = converter.get_supported_input_formats()
output_formats = converter.get_supported_output_formats()
```

### Event Handling

```python
# Custom converter with events
class MyConverter(UniversalConverter):
    def on_start(self, filename):
        print(f"Starting: {filename}")
    
    def on_complete(self, filename, success):
        print(f"Completed: {filename} - {'Success' if success else 'Failed'}")
    
    def on_error(self, filename, error):
        print(f"Error in {filename}: {error}")

# Use custom converter
converter = MyConverter("MyApp")
converter.convert_file("input.pdf", "output.docx")
```

## Advanced Features

### Document Merging

#### GUI Method
1. Select multiple files
2. Right-click → "Merge Documents"
3. Choose output format
4. Set merge options

#### CLI Method
```bash
# Basic merge
python universal_document_converter_ocr.py file1.pdf file2.pdf merged.pdf --merge

# Mixed formats
python universal_document_converter_ocr.py doc.docx data.xlsx report.pdf combined.pdf --merge

# With page ranges
python universal_document_converter_ocr.py file1.pdf[1-10] file2.pdf[5-15] merged.pdf --merge
```

### Document Splitting

```bash
# Split by page count
python universal_document_converter_ocr.py large.pdf output_dir --split --pages-per-file 50

# Split by file size
python universal_document_converter_ocr.py huge.pdf output_dir --split --max-size 10MB

# Extract specific pages
python universal_document_converter_ocr.py document.pdf page5.pdf --pages 5
```

### Watermarking

#### Text Watermark
```bash
python universal_document_converter_ocr.py input.pdf output.pdf --watermark-text "CONFIDENTIAL" --watermark-position center
```

#### Image Watermark
```bash
python universal_document_converter_ocr.py input.pdf output.pdf --watermark-image logo.png --watermark-opacity 0.3
```

### Metadata Handling

```bash
# Preserve all metadata
python universal_document_converter_ocr.py input.pdf output.pdf --preserve-metadata

# Strip metadata
python universal_document_converter_ocr.py input.pdf output.pdf --strip-metadata

# Set custom metadata
python universal_document_converter_ocr.py input.pdf output.pdf --set-title "My Document" --set-author "John Doe"
```

## Performance Optimization

### Multi-threading Settings

#### GUI Settings
1. Tools → Preferences → Performance
2. Set "Worker Threads" (default: CPU count)
3. Set "Max Memory Usage"
4. Enable "GPU Acceleration" (if available)

#### CLI Settings
```bash
# Use all CPU cores
python universal_document_converter_ocr.py /input /output --batch --parallel $(nproc)

# Limit to 4 threads
python universal_document_converter_ocr.py /input /output --batch --parallel 4

# Single thread (for debugging)
python universal_document_converter_ocr.py /input /output --batch --parallel 1
```

### Memory Management

1. **Large Files**
   ```bash
   # Process in chunks
   python universal_document_converter_ocr.py large.pdf output.pdf --chunk-size 10MB
   ```

2. **Batch Processing**
   ```bash
   # Limit concurrent files
   python universal_document_converter_ocr.py /input /output --batch --max-concurrent 3
   ```

3. **OCR Optimization**
   ```bash
   # Reduce memory usage
   python universal_document_converter_ocr.py scan.pdf text.txt --ocr --low-memory
   ```

### Performance Tips

1. **SSD vs HDD**
   - Use SSD for temp files
   - Set temp directory: `--temp-dir /fast/ssd/path`

2. **Network Drives**
   - Process locally, then copy
   - Avoid direct network conversion

3. **Format Selection**
   - PDF → DOCX: Slower but preserves layout
   - PDF → TXT: Fastest, text only
   - Image → PDF: Use appropriate DPI

## Troubleshooting

### Common Issues

#### 1. OCR Not Working
```bash
# Check OCR installation
python universal_document_converter_ocr.py --check-ocr

# Install missing components
pip install pytesseract
# Install Tesseract binary separately
```

#### 2. Memory Errors
```bash
# Reduce memory usage
python universal_document_converter_ocr.py large.pdf output.pdf --low-memory --chunk-size 5MB
```

#### 3. Permission Errors
- Run as administrator (Windows)
- Check file permissions
- Ensure output directory exists

#### 4. Format Not Supported
```bash
# Check supported formats
python universal_document_converter_ocr.py --list-formats

# Force format detection
python universal_document_converter_ocr.py input.xyz output.pdf --input-format auto
```

### Debug Mode

```bash
# Enable debug logging
python universal_document_converter_ocr.py input.pdf output.docx --debug

# Verbose output
python universal_document_converter_ocr.py input.pdf output.docx --verbose

# Log to file
python universal_document_converter_ocr.py input.pdf output.docx --log debug.log
```

### Getting Help

1. **Built-in Help**
   ```bash
   python universal_document_converter_ocr.py --help
   python universal_document_converter_ocr.py convert --help
   ```

2. **Online Resources**
   - GitHub Issues: Report bugs
   - GitHub Discussions: Ask questions
   - Wiki: Additional guides

3. **Diagnostic Tools**
   ```bash
   # System check
   python universal_document_converter_ocr.py --system-check
   
   # Version info
   python universal_document_converter_ocr.py --version --verbose
   ```

---

**Need more help?** Check our [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide or visit the [GitHub repository](https://github.com/Beaulewis1977/quick_ocr_doc_converter).