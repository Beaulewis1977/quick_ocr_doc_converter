# Bidirectional Conversion Features

## Overview

The Universal Document Converter now supports **bidirectional conversion**, meaning you can:

1. **Convert FROM Markdown (.md) files** to other formats
2. **Convert TO multiple output formats** (not just Markdown)
3. **OCR output to multiple formats** (not just Markdown)

## New Features

### 1. Input Format Support

The converter now accepts Markdown (.md) files as input, allowing you to convert:
- Markdown → Plain Text (.txt)
- Markdown → Word Document (.docx)
- Markdown → PDF (.pdf)
- Markdown → HTML (.html)
- Markdown → Rich Text Format (.rtf)

### 2. Multiple Output Formats

Instead of only converting TO Markdown, you can now choose your output format:

| Output Format | Extension | Description |
|--------------|-----------|-------------|
| Markdown | .md | Standard Markdown with formatting |
| Plain Text | .txt | Stripped of all formatting |
| Word Document | .docx | Microsoft Word format |
| PDF | .pdf | Portable Document Format |
| HTML | .html | Web page with styling |
| RTF | .rtf | Rich Text Format |

### 3. OCR with Multiple Output Formats

When processing images with OCR, you can now output to:
- **Plain Text**: Just the extracted text without formatting
- **Markdown**: Text with basic formatting and metadata
- **Word Document**: Properly formatted document
- **PDF**: Searchable PDF with the extracted text
- **HTML**: Web-ready format

## How It Works

### Conversion Process

1. **Input Processing**: Any supported input format (including .md files)
2. **Intermediate Format**: Converts to Markdown internally as a universal format
3. **Output Generation**: Converts from Markdown to your selected output format

### GUI Changes

The enhanced GUI includes:
- **Output Format Selector**: Dropdown menu to choose output format
- **Format Validation**: Checks if required libraries are installed
- **Smart File Extensions**: Automatically uses correct extension for output

## Usage Examples

### Example 1: Convert Markdown to PDF
```
Input: README.md
Output Format: PDF
Result: README.pdf
```

### Example 2: OCR Image to Plain Text
```
Input: scanned_document.jpg
OCR Mode: Enabled
Output Format: Plain Text
Result: scanned_document.txt (just the text, no formatting)
```

### Example 3: Convert Word to HTML
```
Input: report.docx
Output Format: HTML
Result: report.html (with CSS styling)
```

## Installation Requirements

### For Full Feature Support

```bash
# Basic requirements (already included)
pip install python-docx PyPDF2 beautifulsoup4

# For PDF output
pip install reportlab

# For enhanced Markdown processing
pip install markdown2

# For OCR support
pip install pytesseract pillow opencv-python numpy
```

## Configuration

In the GUI:
1. Select your input folder (now includes .md files)
2. Choose output format from the dropdown
3. Enable OCR if processing images
4. Click Convert

## Benefits

1. **Flexibility**: Convert between any supported formats
2. **Preservation**: Maintain document structure across conversions
3. **Accessibility**: Create plain text versions of any document
4. **Web Publishing**: Generate HTML from any document
5. **Professional Output**: Create PDFs and Word documents

## Technical Details

### Markdown as Intermediate Format

The converter uses Markdown as an intermediate format because:
- It preserves document structure (headings, lists, tables)
- It's human-readable and editable
- It can represent most document features
- It's easy to parse and convert

### Format-Specific Features

#### Plain Text Output
- Removes all formatting markers
- Preserves text content and structure
- Ideal for accessibility and simple processing

#### HTML Output
- Includes CSS styling
- Preserves tables and formatting
- Ready for web publishing

#### PDF Output
- Professional document layout
- Maintains headings and structure
- Requires `reportlab` package

#### Word Document Output
- Preserves formatting
- Compatible with Microsoft Office
- Requires `python-docx` package

## Limitations

1. **Complex Formatting**: Some advanced formatting may be simplified
2. **Images**: Currently, images are not embedded in output formats (except PDF)
3. **Tables**: Complex tables may be simplified in some formats
4. **Fonts**: Output uses standard fonts for each format

## Future Enhancements

Planned features:
- Image embedding in output documents
- Custom styling templates
- Batch format conversion
- Format-specific options
- Direct format-to-format conversion (without Markdown intermediate)