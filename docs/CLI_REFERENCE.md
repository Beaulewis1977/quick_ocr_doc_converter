# Universal Document Converter - CLI Reference Guide

Complete command-line interface reference for Universal Document Converter v2.1.0.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Command Structure](#command-structure)
3. [Input/Output Options](#inputoutput-options)
4. [Format Options](#format-options)
5. [OCR Options](#ocr-options)
6. [Batch Processing Options](#batch-processing-options)
7. [Quality Options](#quality-options)
8. [Document Manipulation](#document-manipulation)
9. [Advanced Options](#advanced-options)
10. [Examples](#examples)
11. [Exit Codes](#exit-codes)

## Basic Usage

### Simple Conversion
```bash
# Basic syntax
python universal_document_converter_ocr.py [INPUT] [OUTPUT] [OPTIONS]

# Examples
python universal_document_converter_ocr.py input.pdf output.docx
python universal_document_converter_ocr.py document.md document.pdf
python universal_document_converter_ocr.py scan.jpg text.txt --ocr
```

### Getting Help
```bash
# General help
python universal_document_converter_ocr.py --help
python universal_document_converter_ocr.py -h

# Version information
python universal_document_converter_ocr.py --version
python universal_document_converter_ocr.py -v

# Detailed version with system info
python universal_document_converter_ocr.py --version --verbose
```

## Command Structure

### Synopsis
```
universal_document_converter_ocr.py [GLOBAL_OPTIONS] INPUT OUTPUT [OPTIONS]
universal_document_converter_ocr.py [GLOBAL_OPTIONS] --batch INPUT_DIR OUTPUT_DIR [OPTIONS]
universal_document_converter_ocr.py [GLOBAL_OPTIONS] --merge FILE1 FILE2 ... OUTPUT [OPTIONS]
universal_document_converter_ocr.py [GLOBAL_OPTIONS] --config COMMAND [ARGS]
```

### Global Options
| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Show help message and exit |
| `--version` | `-v` | Show version number |
| `--verbose` | | Enable verbose output |
| `--quiet` | `-q` | Suppress all output except errors |
| `--debug` | | Enable debug mode with detailed logging |
| `--log FILE` | | Log output to file |
| `--config-file FILE` | | Use specific configuration file |
| `--no-config` | | Ignore all configuration files |

## Input/Output Options

### Input Specification
| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--input-format FORMAT` | `-if` | Specify input format | `--input-format pdf` |
| `--encoding ENCODING` | | Input file encoding | `--encoding utf-8` |
| `--password PASS` | | Password for encrypted files | `--password secret123` |
| `--stdin` | | Read input from stdin | `cat file.txt \| ... --stdin` |

### Output Specification
| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--output-format FORMAT` | `-of` | Specify output format | `--output-format docx` |
| `--format FORMAT` | `-f` | Shorthand for output format | `--format pdf` |
| `--output-encoding ENCODING` | | Output file encoding | `--output-encoding utf-16` |
| `--stdout` | | Write output to stdout | `--stdout > output.txt` |
| `--overwrite` | `-y` | Overwrite existing files | `--overwrite` |
| `--no-overwrite` | `-n` | Never overwrite (default) | `--no-overwrite` |
| `--backup` | | Create backup before overwrite | `--backup` |

### Format Options Table
| Option | Short | Description | Formats |
|--------|-------|-------------|---------|
| `--list-formats` | | List all supported formats | - |
| `--check-format FILE` | | Check format of a file | - |

## Format Options

### Supported Input Formats
```bash
# List all supported input formats
python universal_document_converter_ocr.py --list-input-formats

# Supported formats:
- PDF (.pdf)
- Word (.docx, .doc)
- RTF (.rtf)
- HTML (.html, .htm)
- Text (.txt)
- Markdown (.md, .markdown)
- EPUB (.epub)
- ODT (.odt)
- Images (.png, .jpg, .jpeg, .tiff, .bmp, .gif)
```

### Supported Output Formats
```bash
# List all supported output formats
python universal_document_converter_ocr.py --list-output-formats

# Supported formats:
- PDF (.pdf)
- Word (.docx)
- RTF (.rtf)
- HTML (.html)
- Text (.txt)
- Markdown (.md)
- EPUB (.epub)
```

### Format-Specific Options

#### PDF Options
| Option | Description | Default |
|--------|-------------|---------|
| `--pdf-version VERSION` | PDF version (1.4, 1.5, 1.7, 2.0) | 1.7 |
| `--compress` | Enable PDF compression | Yes |
| `--compress-level LEVEL` | Compression level (0-9) | 6 |
| `--linearize` | Optimize for web viewing | No |
| `--pdf-profile PROFILE` | PDF/A, PDF/X profile | None |

#### Word Options
| Option | Description | Default |
|--------|-------------|---------|
| `--compatibility MODE` | Word compatibility mode | Latest |
| `--track-changes` | Preserve track changes | Yes |
| `--comments` | Preserve comments | Yes |

#### Markdown Options
| Option | Description | Default |
|--------|-------------|---------|
| `--markdown-flavor FLAVOR` | Markdown flavor (gfm, commonmark, extra) | gfm |
| `--toc` | Generate table of contents | No |
| `--toc-depth DEPTH` | TOC depth (1-6) | 3 |
| `--code-style STYLE` | Code highlighting style | default |

## OCR Options

### Basic OCR Options
| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--ocr` | | Enable OCR processing | `--ocr` |
| `--ocr-lang LANGS` | `-l` | OCR languages | `--ocr-lang eng+fra+deu` |
| `--ocr-engine ENGINE` | | OCR engine (tesseract, easyocr) | `--ocr-engine tesseract` |
| `--ocr-only` | | Extract text only, no formatting | `--ocr-only` |

### Advanced OCR Options
| Option | Description | Default |
|--------|-------------|---------|
| `--ocr-dpi DPI` | Set DPI for OCR processing | 300 |
| `--ocr-psm MODE` | Tesseract page segmentation mode | 3 |
| `--ocr-confidence THRESHOLD` | Minimum confidence threshold | 0.6 |
| `--ocr-timeout SECONDS` | OCR timeout per page | 30 |

### Image Preprocessing Options
| Option | Description | Default |
|--------|-------------|---------|
| `--preprocess` | Enable all preprocessing | No |
| `--deskew` | Correct image skew | No |
| `--denoise` | Remove image noise | No |
| `--enhance-contrast` | Enhance image contrast | No |
| `--binarize` | Convert to black and white | No |
| `--remove-background` | Remove background | No |
| `--scale-factor FACTOR` | Image scaling factor | 1.0 |

### OCR Language Codes
```bash
# List available OCR languages
python universal_document_converter_ocr.py --list-ocr-languages

# Common languages:
eng - English          fra - French
deu - German          spa - Spanish
ita - Italian         por - Portuguese
rus - Russian         chi_sim - Chinese (Simplified)
jpn - Japanese        kor - Korean
ara - Arabic          hin - Hindi

# Use multiple languages
--ocr-lang eng+fra+deu
```

## Batch Processing Options

### Basic Batch Options
| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--batch` | `-b` | Enable batch mode | `--batch` |
| `--recursive` | `-r` | Include subdirectories | `--recursive` |
| `--pattern PATTERN` | `-p` | File pattern (glob) | `--pattern "*.pdf"` |
| `--exclude PATTERN` | `-x` | Exclude pattern | `--exclude "*draft*"` |

### Advanced Batch Options
| Option | Description | Default |
|--------|-------------|---------|
| `--parallel WORKERS` | Number of parallel workers | CPU count |
| `--batch-size SIZE` | Files per batch | 10 |
| `--follow-symlinks` | Follow symbolic links | No |
| `--skip-errors` | Continue on errors | Yes |
| `--error-dir DIR` | Directory for failed files | None |

### Organization Options
| Option | Description | Example |
|--------|-------------|---------|
| `--organize` | Organize output by format | Creates pdf/, docx/ subdirs |
| `--preserve-structure` | Keep directory structure | Recreates source structure |
| `--flatten` | Put all files in output root | All files in one directory |

## Quality Options

### General Quality Settings
| Option | Description | Values |
|--------|-------------|--------|
| `--quality QUALITY` | Output quality | low, medium, high |
| `--dpi DPI` | DPI for image outputs | 72-1200 |
| `--color-space SPACE` | Color space | rgb, cmyk, gray |
| `--bit-depth DEPTH` | Bit depth | 1, 8, 16, 24, 32 |

### Compression Options
| Option | Description | Default |
|--------|-------------|---------|
| `--compress` | Enable compression | Yes |
| `--compress-images` | Compress embedded images | Yes |
| `--jpeg-quality QUALITY` | JPEG quality (1-100) | 85 |
| `--png-compression LEVEL` | PNG compression (0-9) | 6 |

### Optimization Options
| Option | Description | Default |
|--------|-------------|---------|
| `--optimize` | Optimize output size | No |
| `--optimize-images` | Optimize embedded images | No |
| `--downsample-images` | Downsample large images | No |
| `--max-image-size SIZE` | Maximum image dimension | None |

## Document Manipulation

### Page Operations
| Option | Description | Example |
|--------|-------------|---------|
| `--pages RANGE` | Select page range | `--pages 1-10,15,20-25` |
| `--split` | Split into separate files | `--split` |
| `--split-size SIZE` | Pages per split file | `--split-size 50` |
| `--merge` | Merge multiple inputs | `--merge file1.pdf file2.pdf` |

### Content Operations
| Option | Description | Default |
|--------|-------------|---------|
| `--extract-text` | Extract text only | No |
| `--extract-images` | Extract images to files | No |
| `--strip-images` | Remove all images | No |
| `--strip-fonts` | Remove embedded fonts | No |

### Metadata Operations
| Option | Description | Example |
|--------|-------------|---------|
| `--preserve-metadata` | Keep document metadata | Yes |
| `--strip-metadata` | Remove all metadata | No |
| `--set-title TITLE` | Set document title | `--set-title "My Document"` |
| `--set-author AUTHOR` | Set document author | `--set-author "John Doe"` |
| `--set-subject SUBJECT` | Set document subject | `--set-subject "Report"` |
| `--set-keywords KEYWORDS` | Set keywords | `--set-keywords "pdf,report"` |

### Security Operations
| Option | Description | Example |
|--------|-------------|---------|
| `--encrypt PASSWORD` | Encrypt output PDF | `--encrypt mypass123` |
| `--decrypt` | Remove encryption | `--decrypt` |
| `--permissions PERMS` | Set PDF permissions | `--permissions print,copy` |
| `--owner-password PASS` | Set owner password | `--owner-password admin123` |
| `--user-password PASS` | Set user password | `--user-password user123` |

## Advanced Options

### Processing Options
| Option | Description | Default |
|--------|-------------|---------|
| `--timeout SECONDS` | Global timeout | 300 |
| `--max-memory MB` | Memory limit | 2048 |
| `--temp-dir DIR` | Temporary directory | System temp |
| `--cache` | Enable caching | Yes |
| `--no-cache` | Disable caching | No |

### Formatting Options
| Option | Description | Default |
|--------|-------------|---------|
| `--preserve-formatting` | Keep original formatting | Yes |
| `--preserve-layout` | Keep page layout | Yes |
| `--preserve-fonts` | Embed original fonts | Yes |
| `--font-substitution` | Allow font substitution | Yes |

### Watermark Options
| Option | Description | Example |
|--------|-------------|---------|
| `--watermark-text TEXT` | Add text watermark | `--watermark-text "DRAFT"` |
| `--watermark-image FILE` | Add image watermark | `--watermark-image logo.png` |
| `--watermark-position POS` | Watermark position | `--watermark-position center` |
| `--watermark-opacity OPACITY` | Watermark opacity (0-1) | `--watermark-opacity 0.3` |
| `--watermark-rotation ANGLE` | Watermark rotation | `--watermark-rotation 45` |

### Special Options
| Option | Description |
|--------|-------------|
| `--json-ipc` | Use JSON IPC mode |
| `--pipe-server` | Start named pipe server |
| `--com-server` | Register as COM server |
| `--api-server` | Start REST API server |
| `--check-dependencies` | Check all dependencies |
| `--self-test` | Run self-test |

## Examples

### Basic Conversions
```bash
# PDF to Word
python universal_document_converter_ocr.py document.pdf document.docx

# Markdown to PDF
python universal_document_converter_ocr.py README.md README.pdf

# RTF to Markdown
python universal_document_converter_ocr.py document.rtf document.md

# Image to text with OCR
python universal_document_converter_ocr.py scan.jpg text.txt --ocr
```

### OCR Examples
```bash
# Basic OCR
python universal_document_converter_ocr.py scan.pdf text.txt --ocr

# Multi-language OCR
python universal_document_converter_ocr.py document.pdf text.txt --ocr --ocr-lang eng+fra+deu

# OCR with preprocessing
python universal_document_converter_ocr.py poor_scan.pdf text.docx --ocr --preprocess --deskew --denoise

# OCR with specific engine
python universal_document_converter_ocr.py handwritten.jpg text.txt --ocr --ocr-engine easyocr
```

### Batch Processing Examples
```bash
# Convert all PDFs to Word
python universal_document_converter_ocr.py --batch /pdfs /docx --format docx

# Recursive with pattern
python universal_document_converter_ocr.py --batch /docs /output --recursive --pattern "*.pdf" --format txt

# Parallel processing
python universal_document_converter_ocr.py --batch /input /output --parallel 8 --format pdf

# With organization
python universal_document_converter_ocr.py --batch /docs /converted --organize --recursive
```

### Advanced Examples
```bash
# Merge multiple files
python universal_document_converter_ocr.py --merge doc1.pdf doc2.pdf doc3.pdf combined.pdf

# Split large PDF
python universal_document_converter_ocr.py large.pdf /output --split --split-size 50

# Extract specific pages
python universal_document_converter_ocr.py document.pdf excerpt.pdf --pages 1-10,15,20-25

# Add watermark
python universal_document_converter_ocr.py input.pdf output.pdf --watermark-text "CONFIDENTIAL" --watermark-opacity 0.3

# Encrypt PDF
python universal_document_converter_ocr.py input.pdf secure.pdf --encrypt "password123" --permissions print
```

### Pipeline Examples
```bash
# OCR and convert
python universal_document_converter_ocr.py scan.pdf | python universal_document_converter_ocr.py --stdin output.docx

# Chain conversions
python universal_document_converter_ocr.py input.md temp.html && python universal_document_converter_ocr.py temp.html output.pdf

# Batch with post-processing
find /docs -name "*.pdf" -exec python universal_document_converter_ocr.py {} {}.txt --ocr \;
```

### Configuration Examples
```bash
# Use specific config
python universal_document_converter_ocr.py --config-file myconfig.json input.pdf output.docx

# Override config settings
python universal_document_converter_ocr.py --config set ocr.default_engine tesseract

# Use profile
python universal_document_converter_ocr.py --config load-profile high-quality input.pdf output.pdf
```

## Exit Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 0 | Success | Conversion completed successfully |
| 1 | General error | Unspecified error occurred |
| 2 | Invalid arguments | Command line arguments invalid |
| 3 | File not found | Input file doesn't exist |
| 4 | Permission denied | No permission to read/write |
| 5 | Format error | Unsupported or invalid format |
| 6 | OCR error | OCR processing failed |
| 7 | Memory error | Out of memory |
| 8 | Timeout | Operation timed out |
| 9 | Dependency error | Required dependency missing |
| 10 | Configuration error | Invalid configuration |
| 11 | Network error | Network-related failure |
| 12 | License error | License validation failed |
| 127 | Command not found | Python or script not found |

### Using Exit Codes

#### Bash
```bash
python universal_document_converter_ocr.py input.pdf output.docx
if [ $? -eq 0 ]; then
    echo "Conversion successful"
else
    echo "Conversion failed with code: $?"
fi
```

#### Windows Batch
```batch
python universal_document_converter_ocr.py input.pdf output.docx
IF %ERRORLEVEL% EQU 0 (
    ECHO Conversion successful
) ELSE (
    ECHO Conversion failed with code: %ERRORLEVEL%
)
```

#### PowerShell
```powershell
python universal_document_converter_ocr.py input.pdf output.docx
if ($LASTEXITCODE -eq 0) {
    Write-Host "Conversion successful"
} else {
    Write-Host "Conversion failed with code: $LASTEXITCODE"
}
```

## Environment Variables

The CLI respects these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `UC_HOME` | Converter installation directory | `/opt/converter` |
| `UC_CONFIG` | Default config file path | `~/.config/uc/config.json` |
| `UC_TEMP_DIR` | Temporary files directory | `/tmp/converter` |
| `UC_LOG_LEVEL` | Default log level | `INFO` |
| `UC_PARALLEL_WORKERS` | Default worker count | `4` |
| `UC_OCR_ENGINE` | Default OCR engine | `tesseract` |
| `UC_OCR_LANGUAGES` | Default OCR languages | `eng+fra` |
| `UC_TIMEOUT` | Default timeout seconds | `300` |

## Shell Integration

### Bash Aliases
```bash
# Add to ~/.bashrc
alias pdf2docx='python /path/to/universal_document_converter_ocr.py'
alias ocr='python /path/to/universal_document_converter_ocr.py --ocr'
alias convert='python /path/to/universal_document_converter_ocr.py'

# Function for batch conversion
batch_convert() {
    python /path/to/universal_document_converter_ocr.py --batch "$1" "$2" --format "$3" --recursive
}
```

### Windows Aliases
```batch
:: Add to batch file in PATH
@echo off
python "C:\UniversalConverter\universal_document_converter_ocr.py" %*
```

### PowerShell Functions
```powershell
# Add to $PROFILE
function Convert-Document {
    param($Input, $Output, $Format = "pdf")
    python C:\UniversalConverter\universal_document_converter_ocr.py $Input $Output --format $Format
}

function Convert-WithOCR {
    param($Input, $Output)
    python C:\UniversalConverter\universal_document_converter_ocr.py $Input $Output --ocr
}
```

---

**Need more help?** Use `--help` with any command or see [USER_MANUAL.md](USER_MANUAL.md)