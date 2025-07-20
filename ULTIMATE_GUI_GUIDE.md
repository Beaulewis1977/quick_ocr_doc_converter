# Universal Document Converter Ultimate - Complete Guide

## Overview
The Universal Document Converter Ultimate is the most feature-rich version of the application, combining all functionality into a single, comprehensive GUI.

## Features

### ✅ Core Features (Working)
- **Document Conversion**: DOCX, PDF, TXT, HTML, RTF, EPUB
- **OCR Support**: Process images (JPG, PNG, TIFF, BMP, GIF, WebP) and scanned PDFs
- **Multi-threaded Processing**: GUI control for 1-32 threads
- **Drag & Drop**: Direct file/folder dropping onto the window
- **Advanced Settings**: Comprehensive configuration options
- **Statistics Tracking**: Monitor conversion metrics and export data
- **Performance Monitoring**: Real-time memory and CPU usage display

### 🔧 Advanced Features
1. **Thread Selection System**
   - Adjustable worker threads (1-32) via GUI spinbox
   - Shows available CPU cores for reference
   - Optimal performance based on system capabilities

2. **OCR Configuration**
   - Multiple backends: Pytesseract (available), EasyOCR (optional)
   - Language selection (eng, spa, fra, deu, chi_sim, jpn, kor)
   - Preprocessing options: deskew, denoise, contrast enhancement
   - Multi-backend support for better accuracy

3. **API Server** (requires flask, flask-cors, waitress)
   - REST API for remote document conversion
   - Endpoints: /api/convert, /api/formats, /api/health, /api/status
   - Configurable host and port
   - Built-in API documentation and examples

4. **Tools & Settings**
   - **File Handling**: Preserve folder structure, overwrite control, auto-open output
   - **Performance**: Caching, memory threshold, queue size configuration
   - **Format-specific**: PDF image extraction, DOCX style preservation
   - **Theme Support**: Light/dark mode toggle
   - **Logging**: Comprehensive logging with viewer and retention settings

## Installation

### Required Dependencies
```bash
# System dependencies
sudo apt-get update
sudo apt-get install python3-tk tesseract-ocr xvfb libxcursor1

# Python dependencies (core)
pip install tkinterdnd2 python-docx PyPDF2 beautifulsoup4 striprtf ebooklib
pip install pytesseract opencv-python numpy Pillow

# Optional dependencies
pip install flask flask-cors waitress  # For API server
pip install easyocr                     # For additional OCR backend
pip install reportlab psutil            # For PDF generation and monitoring
```

## Running the Application

### Method 1: Direct Launch
```bash
python3 universal_document_converter_ultimate.py
```

### Method 2: Using Launcher
```bash
python3 launch_ultimate.py
```

### Method 3: For Testing/Headless
```bash
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
python3 universal_document_converter_ultimate.py
```

## GUI Layout

### Main Tab: Document Conversion
- **File Management**: Add files/folders, remove selected, clear all
- **File List**: Shows all queued files with selection support
- **Quick Settings**: Output format, OCR toggle, thread count
- **Output Directory**: Browse and set output location
- **Progress Tracking**: Real-time progress bar and status
- **Control Buttons**: Start, Pause, Cancel operations

### Advanced Settings Tab
- **OCR Settings**: Backend selection, language, preprocessing options
- **Performance Settings**: Cache, memory, queue configuration
- **File Handling**: Structure preservation, overwrite behavior
- **Format-specific Settings**: PDF and DOCX options

### API Server Tab
- **Server Control**: Start/stop API server
- **Configuration**: Host and port settings
- **Documentation**: Usage examples and test functionality
- **Status Display**: Current server state and URL

### Statistics Tab
- **Overall Metrics**: Total processed, success rate, processing time
- **Format Statistics**: Per-format conversion metrics
- **Export Options**: Save statistics as CSV or JSON
- **Real-time Updates**: Auto-refresh during processing

## Usage Examples

### Basic Document Conversion
1. Launch the application
2. Add files using "Add Files" button or drag & drop
3. Select output format (txt, docx, pdf, html, rtf, epub)
4. Choose output directory
5. Click "Start Conversion"

### OCR Processing
1. Enable OCR checkbox
2. Add image files or scanned PDFs
3. Configure OCR settings if needed (Settings tab)
4. Process as normal - OCR will automatically detect and process images

### API Usage
1. Enable API server in API tab
2. Start the server
3. Use curl or any HTTP client:
```bash
curl -X POST -F "file=@document.pdf" -F "format=txt" -F "ocr=true" \
  http://localhost:5000/api/convert -o output.txt
```

### Batch Processing with Custom Threads
1. Add multiple files or entire folders
2. Adjust thread count based on your CPU (e.g., 8 threads for 8-core CPU)
3. Enable caching for repeated conversions
4. Monitor progress and performance metrics

## Troubleshooting

### Common Issues
1. **"No module named tkinter"**: Install python3-tk
2. **Drag & drop not working**: Install tkinterdnd2
3. **OCR not working**: Install tesseract-ocr system package
4. **API server fails**: Install flask, flask-cors, waitress

### Performance Tips
- Use thread count = CPU cores for optimal performance
- Enable caching for repeated conversions
- Increase memory threshold for large files
- Use appropriate output formats (txt is fastest)

## Configuration File
Settings are saved in `config_ultimate.json` including:
- Output preferences
- OCR configuration  
- Performance settings
- API configuration
- Window geometry
- Theme preference

## Keyboard Shortcuts
- **Ctrl+O**: Add files
- **Ctrl+D**: Add folder
- **Ctrl+Q**: Exit application

## Notes
- The application gracefully handles missing optional dependencies
- Drag & drop works on Windows, macOS, and Linux
- API server runs in background thread
- All processing is non-blocking with progress tracking
- Logs are stored in the `logs/` directory

## Support
For issues or questions:
- Check the logs in the `logs/` directory
- Use the built-in log viewer (Tools → View Logs)
- Review the troubleshooting section above

---
Created by Beau Lewis (blewisxx@gmail.com)
Universal Document Converter Ultimate v1.0.0