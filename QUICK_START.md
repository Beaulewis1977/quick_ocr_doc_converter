# OCR Document Converter v3.1.0 - Quick Start Guide

## 🚀 Instant Launch Options

### Option 1: Double-Click Launch (Recommended)
- **Windows**: Double-click `⚡ Quick Launch OCR.bat` (enhanced features)
- **Windows**: Double-click `run_ocr_converter.bat` (main launcher)
- **Linux/macOS**: Double-click `run_converter.sh` (make executable first: `chmod +x run_converter.sh`)

### Option 2: Command Line
```bash
# From project folder
python universal_document_converter_ocr.py

# Or use the launchers
# Windows:
⚡ Quick Launch OCR.bat
run_ocr_converter.bat

# Linux/macOS:
./run_converter.sh
```

### Option 3: Install & Run (Permanent Installation)
```bash
# Windows (Run as Administrator)
install.bat

# Linux/macOS
python3 setup_shortcuts.py

# Then run from Start Menu or desktop shortcut
```

## 📋 First-Time Setup

1. **Install Python** (if not already installed):
   - Download from https://www.python.org/downloads/
   - **Important**: Check "Add Python to PATH" during installation
   - Minimum version: Python 3.8+

2. **Download Complete Package**:
   - Get latest from [GitHub Releases](https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest)
   - Extract all files to a folder

3. **Install Dependencies**:
   ```bash
   # Automatic installation (recommended)
   python install_converter.py
   
   # Or install OCR dependencies separately
   python install_ocr_dependencies.py
   ```

4. **Launch Application**:
   - Double-click `⚡ Quick Launch OCR.bat` (Windows, recommended)
   - Or use any method above

## 🆕 **New in v3.1.0**

### Google Vision API Support
- **Cloud OCR** with superior accuracy
- **Automatic fallback** to free engines
- **Setup**: Use GUI → Settings → Google Vision API tab

### Enhanced Features
- **Input format selection** for better accuracy
- **Markdown output** support (.md files)
- **Legacy Integration tab** for VB6/VFP9
- **Real-time OCR engine status**

## 🎯 Quick Usage Guide

### Basic Document Conversion
1. **Launch** the application
2. **Select files** (drag & drop or click "Select Files")
3. **Choose output format** (txt, docx, pdf, markdown, etc.)
4. **Click Convert**

### OCR (Image to Text)
1. **Enable OCR** in settings or use OCR tab
2. **Select images** (jpg, png, pdf with images)
3. **Choose OCR engine**:
   - **Tesseract** (free, good quality)
   - **EasyOCR** (free, better for handwriting)
   - **Google Vision API** (premium, best quality)
4. **Convert** and save

### Batch Processing
1. **Select multiple files** (Ctrl+click or Shift+click)
2. **Set output folder**
3. **Choose format and OCR settings**
4. **Process all** with one click

## 🔧 Troubleshooting

### Python Not Found
- Install Python 3.8+ from python.org
- Restart your computer after installation
- Verify: `python --version`

### Missing Dependencies
```bash
# Automatic fix
python install_converter.py

# Or manual installation
pip install -r requirements.txt
python install_ocr_dependencies.py
```

### OCR Not Working
```bash
# Install OCR dependencies
python install_ocr_dependencies.py

# Windows - Install Tesseract manually if needed
# Download from: https://github.com/tesseract-ocr/tesseract
```

### Google Vision API Setup
1. **Create Google Cloud account**
2. **Enable Vision API**
3. **Create service account and download JSON key**
4. **In app**: Settings → Google Vision API → Upload key file

### Application Won't Start
- Check `TROUBLESHOOTING.md` for detailed solutions
- Verify all files are in the same folder
- Try running from command line to see error messages
- Ensure Python is in system PATH

### Legacy Integration (VB6/VFP9)
- Use **Legacy Integration tab** in GUI
- See [LEGACY_INTEGRATION_GUIDE.md](LEGACY_INTEGRATION_GUIDE.md)
- Automated code generation and testing available

## 📁 File Structure
```
ocr_document_converter/
├── ⚡ Quick Launch OCR.bat     # Enhanced Windows launcher
├── run_ocr_converter.bat       # Main Windows launcher  
├── run_converter.sh            # Linux/macOS launcher
├── install.bat                 # Windows installer
├── install_converter.py        # Dependency installer
├── install_ocr_dependencies.py # OCR-specific installer
├── universal_document_converter_ocr.py  # Main application
├── setup_shortcuts.py          # Desktop integration
├── icon.ico                    # Application icon
├── requirements.txt            # Python dependencies
└── README.md                   # Full documentation
```

## 🎛️ **Settings and Configuration**

### OCR Settings
- **Engine selection**: Tesseract, EasyOCR, Google Vision API
- **Language settings**: Multiple language support
- **Quality settings**: DPI, preprocessing options

### Output Settings
- **Format selection**: txt, docx, pdf, markdown, html, epub
- **Quality settings**: Formatting preservation
- **Batch processing**: Folder organization

### Google Vision API Settings
- **API key management**: Secure storage
- **Cost controls**: Usage limits
- **Fallback settings**: Automatic engine switching

## 🚀 **Advanced Features**

### Legacy System Integration
- **VB6/VFP9 support**: Complete integration package
- **DLL generation**: Automated build tools
- **Code examples**: Ready-to-use templates
- **Testing tools**: Validation and debugging

### Batch Operations
- **Folder processing**: Convert entire directories
- **Format preservation**: Maintain document structure
- **Progress tracking**: Real-time status updates

### Cloud Integration
- **Google Vision API**: Premium OCR service
- **Cost optimization**: Intelligent API usage
- **Offline fallback**: No service interruption

## 💡 Pro Tips

- **First time**: Start with `⚡ Quick Launch OCR.bat`
- **Permanent setup**: Run `install.bat` as Administrator
- **Best OCR quality**: Use Google Vision API
- **Free OCR**: Tesseract for documents, EasyOCR for handwriting
- **Batch processing**: Use input format selection for consistency
- **Legacy apps**: Use Legacy Integration tab for VB6/VFP9
- **Troubleshooting**: Check logs in application folder

## 🔗 **Need More Help?**

- **Full Documentation**: [README.md](README.md)
- **Installation Guide**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Legacy Integration**: [LEGACY_INTEGRATION_GUIDE.md](LEGACY_INTEGRATION_GUIDE.md)
- **Google Vision Setup**: [GOOGLE_VISION_SETUP.md](GOOGLE_VISION_SETUP.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **GitHub Issues**: [Report Problems](https://github.com/Beaulewis1977/quick_ocr_doc_converter/issues)

---

**Ready to convert? Just double-click `⚡ Quick Launch OCR.bat` and start converting!**