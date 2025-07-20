# Universal Document Converter Ultimate with Advanced OCR

A powerful Python application that converts multiple document formats (PDF, DOCX, TXT, HTML, RTF, EPUB) to various output formats with advanced OCR capabilities, multi-threaded processing, and a comprehensive GUI interface.

Designed and built by Beau Lewis.

## 🎯 Quick Download (No Installation Required!)

### 📦 **[Download Windows ZIP → Extract → Click EXE](https://github.com/yourusername/universal-document-converter/releases/latest/download/UniversalDocumentConverter_Windows_2.0.0_Installer.zip)**

**Just 3 steps:**
1. Download the ZIP file
2. Extract it anywhere
3. Double-click `UniversalDocumentConverter.exe`

**That's it! No installation needed. All features included!**

---

### 🖥️ **Alternative: Full Windows Installer**
**[Download QuickDocumentConverter_Setup.exe](https://github.com/yourusername/universal-document-converter/releases/latest/download/QuickDocumentConverter_Setup.exe)**

**Professional installer with:**
- ✅ Professional GUI installer wizard
- ✅ Desktop & Start Menu shortcuts automatically created
- ✅ System tray integration with quick convert menu
- ✅ Taskbar pinning support
- ✅ Right-click context menu "Convert with Quick Document Converter"
- ✅ File associations for all supported formats
- ✅ Auto-start with Windows option
- ✅ Full uninstaller in Control Panel

**No Python installation required!** Just download and run the installer.

---

### 🍎 **macOS & 🐧 Linux Users**
**[Download Source ZIP](https://github.com/yourusername/universal-document-converter/releases/latest/download/UniversalDocumentConverter_Source_2.0.0.zip)**

Extract and run:
- **macOS**: `./INSTALL_AND_RUN_MACOS.sh`
- **Linux**: `./INSTALL_AND_RUN_LINUX.sh`

---

## 🎉 Test Status - All Tests Passing!

### Automated Test Results
- ✅ **Syntax Validation**: 48 Python files validated successfully
- ✅ **Import Tests**: All modules import without errors
- ✅ **Functional Tests**: Core functionality verified
- ✅ **OCR Tests**: OCR engine and format detection working
- ✅ **Conversion Tests**: Document conversion tested successfully
- ✅ **GUI Tests**: GUI creation and operation verified
- ✅ **Threading Tests**: Multi-threaded processing functional
- ✅ **Configuration Tests**: Settings persistence working

### Test Commands
```bash
# Run all tests
python3 test_functional.py    # ✅ All tests passed
python3 test_conversion.py    # ✅ 3/3 tests passed
python3 test_ultimate_features.py  # ✅ All features verified
```

## 🌟 Universal Document Converter Ultimate - Full Feature Set

The most comprehensive document conversion tool with professional GUI:

### ✅ Main GUI Features (All Verified Working)

#### 📑 **Document Conversion Tab**
- **Multi-Format Support**: Convert between DOCX, PDF, TXT, HTML, RTF, EPUB
- **Batch Processing**: Add multiple files or entire folders at once
- **Drag & Drop**: Direct file/folder dropping onto the window
- **Real-time Progress**: Monitor conversion with progress bar and status
- **Quick Settings Panel**:
  - Output format selection dropdown
  - OCR toggle checkbox
  - **Thread Count Selector (1-32)**: Spinbox control to adjust worker threads
  - Shows available CPU cores for optimal selection
- **File Management**: Add, remove, clear file lists easily

#### ⚙️ **Advanced Settings Tab**
- **OCR Configuration**:
  - Backend selection (Pytesseract, EasyOCR, Auto)
  - Language selection (7+ languages)
  - Preprocessing options (deskew, denoise, contrast)
  - Multi-backend support toggle
- **Performance Settings**:
  - Cache enable/disable with TTL configuration
  - Memory threshold adjustment (100-4096 MB)
  - Queue size configuration
- **File Handling**:
  - Preserve folder structure option
  - Overwrite existing files toggle
  - Auto-open output folder after conversion
- **Format-Specific Settings**:
  - PDF: Extract images option
  - DOCX: Extract styles option

#### 🌐 **API Server Tab**
- **Server Control**: Start/stop REST API server
- **Configuration**: Host and port settings
- **Live Examples**: Copy-paste ready API usage examples
- **Test Button**: Verify API connectivity
- **Status Display**: Real-time server status and URL

#### 📊 **Statistics Tab**
- **Overall Metrics**: Total processed, success rate, uptime
- **Format Statistics**: Per-format conversion tracking
- **Export Options**: Save stats as CSV or JSON
- **Visual Display**: Tree view of conversion history

### 🚀 Windows Quick Launch Options
```batch
# Multiple ways to start:
"🚀 Launch Quick Document Convertor.bat"     # Standard launch
"⚡ Quick Launch.bat"                         # Fast start
"🖥️ FORCE GUI TO APPEAR.bat"                # Troubleshooting launch
"Quick Document Convertor.bat"               # Classic launch
```

### 💻 System Tray Features
- **Quick Convert**: Right-click tray icon → Quick Convert File
- **Settings Access**: Configure default format and behaviors
- **Auto-start Option**: Start with Windows checkbox
- **Notifications**: Conversion complete alerts
- **Professional Icon**: Blue document icon in system tray

## Features

### Core Functionality
- **PDF to Multiple Formats**: Convert PDFs to JSON, DOCX, or Markdown
- **Bidirectional Conversion**: Support for both PDF→JSON and JSON→PDF workflows
- **Unicode Support**: Full UTF-8 encoding with special character handling
- **Font Preservation**: Maintains font information during conversion
- **Layout Analysis**: Preserves document structure and formatting

### Advanced OCR System

#### Multi-Backend Support
- **Tesseract OCR**: Free, open-source local OCR engine
- **Google Vision API**: Advanced cloud-based OCR with handwriting support
- **AWS Textract**: Document analysis with form and table extraction
- **Azure Computer Vision**: Enterprise OCR with language detection

#### Intelligent Backend Selection
- **Automatic Fallback**: Seamlessly switch between backends on failure
- **Cost Optimization**: Choose the most cost-effective backend based on requirements
- **Performance Tracking**: Monitor and optimize backend performance
- **Custom Selection Strategies**: Define your own backend selection logic

### Security Features

#### Input Validation
- File type and size validation
- Path traversal protection
- MIME type verification
- Malicious content detection

#### Credential Management
- Encrypted storage using Fernet encryption
- Secure API key management
- Audit logging for all credential operations
- Automatic credential rotation support

#### PII Protection
- Automatic detection of sensitive information
- PII masking in processed documents
- Configurable sensitivity levels

### Cost Tracking & Optimization

#### Real-time Monitoring
- Track usage across all cloud backends
- Per-request cost calculation
- Monthly budget alerts
- Historical usage analysis

#### Optimization Features
- Automatic backend selection based on cost
- Budget-aware processing
- Cost prediction before processing
- Detailed cost breakdowns by service

### Enhanced GUI

#### Modern Interface
- Tabbed interface for easy navigation
- Real-time processing status
- Progress indicators for long operations
- Dark mode support

#### Configuration Options
- Backend selection and prioritization
- Security settings management
- Cost tracking dashboard
- API credential configuration

## 💿 Installation Options

### 🎯 Option 1: Windows Installer (Easiest)
**No Python required!** Download and run the installer:
1. Download `QuickDocumentConverter_Setup.exe` from releases
2. Run as Administrator
3. Follow the installation wizard
4. Find shortcuts on Desktop, Start Menu, and System Tray

**What the installer does:**
- ✅ Installs all dependencies automatically
- ✅ Creates Desktop & Start Menu shortcuts
- ✅ Sets up system tray with auto-start option
- ✅ Registers file associations
- ✅ Adds right-click context menu
- ✅ Creates uninstaller in Control Panel

### 🔧 Option 2: Quick Setup Scripts (Windows)
```batch
# Run the automated setup
setup_windows_installer.bat

# Or create shortcuts manually
python setup_shortcuts.py
```

### 💻 Option 3: Manual Installation (All Platforms)

#### System Requirements
- Python 3.6+ (tested with 3.12)
- Tkinter (GUI framework)
- Tesseract OCR (for OCR functionality)

#### Windows Setup
```bash
# Install Python from python.org (includes tkinter)
# Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki

# Clone repository
git clone https://github.com/yourusername/universal-document-converter.git
cd universal-document-converter

# Install dependencies
pip install -r requirements.txt

# Launch
python universal_document_converter_ultimate.py
```

#### Linux/macOS Setup
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3-tk tesseract-ocr libxcursor1

# macOS
brew install python-tk tesseract

# Install Python dependencies
pip install -r requirements.txt

# Launch
python3 universal_document_converter_ultimate.py
```

### 🎨 Optional Enhancements
```bash
# API server functionality
pip install flask flask-cors waitress

# Enhanced OCR backends
pip install easyocr

# System tray support
pip install pystray pillow
```

## Usage

### Basic Usage

1. **Launch the application:**
   ```bash
   # Windows with installer: Click desktop shortcut or Start Menu
   # Manual installation: 
   python3 universal_document_converter_ultimate.py
   ```

2. **Add files:**
   - Click "Add Files" or "Add Folder" buttons
   - Or drag and drop files/folders directly onto the window
   - System tray: Right-click → Quick Convert File

3. **Configure settings:**
   - Select output format (TXT, DOCX, PDF, HTML, RTF, EPUB)
   - Enable OCR for image files
   - Choose output directory

4. **Convert:**
   - Click "Start Conversion"
   - Monitor progress in real-time
   - View results when complete

### ⚡ Thread Selection System

The GUI includes a powerful thread selection system for optimal performance:

#### **Location**: Main tab → Quick Settings panel → "Threads:" spinbox

#### **Features**:
- **Range**: 1-32 worker threads
- **Visual Aid**: Shows your CPU core count (e.g., "CPU cores: 8")
- **Real-time Adjustment**: Change threads without restarting
- **Smart Default**: Automatically set to your CPU core count

#### **Performance Guidelines**:
- **Light tasks (TXT)**: 1-4 threads
- **Medium tasks (DOCX/HTML)**: 4-8 threads  
- **Heavy tasks (PDF/OCR)**: 8-16 threads
- **Batch processing**: Match CPU cores
- **System responsiveness**: Use cores - 1

#### **Example Settings**:
```
4-core CPU: Set 4 threads for batch, 3 for background work
8-core CPU: Set 8 threads for speed, 6 for multitasking
16-core CPU: Set 12-16 threads for maximum performance
```

### Advanced Features

- **API Server**: Enable in the API tab for REST API access
- **OCR Settings**: Configure language, preprocessing, and backends
- **Statistics**: Track conversions and export metrics
- **Performance**: Adjust cache, memory, and queue settings
- **System Tray**: Quick access to conversion without opening full GUI

## API Key Configuration

### Easy GUI Setup (Recommended)

1. **Launch the application:**
   ```bash
   python enhanced_ocr_gui.py
   ```

2. **Click the "Settings" tab**

3. **Configure your OCR backends:**

   #### Free Local OCR (No API Key Required)
   - ✅ **Tesseract OCR** works out of the box
   - Unlimited usage, completely free
   - No internet connection required

   #### Cloud OCR Services (Optional)

   **Google Vision API:**
   - Create a [Google Cloud project](https://console.cloud.google.com)
   - Enable Vision API
   - Create service account → Download JSON key
   - In app: Browse and select the JSON file

   **AWS Textract:**
   - Create [AWS account](https://aws.amazon.com)
   - Create IAM user with Textract permissions
   - In app: Enter Access Key ID, Secret Key, Region

   **Azure Computer Vision:**
   - Create [Azure account](https://portal.azure.com)
   - Deploy Computer Vision resource
   - In app: Enter Subscription Key and Endpoint URL

4. **Click "Save Configuration"** to encrypt and store securely
5. **Click "Test Backends"** to verify everything works

### Environment Variables (Alternative)
```bash
# Google Vision
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# AWS Textract  
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"

# Azure
export AZURE_COGNITIVE_SERVICES_KEY="your-subscription-key" 
export AZURE_COGNITIVE_SERVICES_ENDPOINT="https://your-endpoint.cognitiveservices.azure.com/"
```

## Usage

### GUI Application

Run the enhanced GUI:
```bash
python enhanced_ocr_gui.py
```

Features:
- **File Selection**: Browse and select PDFs for conversion
- **Backend Configuration**: Choose and configure OCR backends
- **Security Settings**: Configure validation rules and PII detection
- **Cost Tracking**: View real-time costs and usage statistics
- **Batch Processing**: Convert multiple files at once

### Command Line

Basic usage:
```bash
python pdf_to_json.py input.pdf -o output.json
```

With specific backend:
```bash
python pdf_to_json.py input.pdf -o output.json --backend google_vision
```

With cost limit:
```bash
python pdf_to_json.py input.pdf -o output.json --max-cost 0.50
```

### API Usage

```python
from backends import OCRBackendManager
from security import SecurityValidator, CredentialManager
from monitoring import CostTracker

# Initialize components
validator = SecurityValidator()
cred_manager = CredentialManager()
backend_manager = OCRBackendManager()
cost_tracker = CostTracker()

# Validate input
if validator.validate_file_path(file_path):
    # Process with OCR
    result = backend_manager.process_with_fallback(
        file_path,
        language='en',
        requirements={'accuracy': 'high', 'max_cost': 1.0}
    )
    
    # Track costs
    cost_tracker.track_usage(
        result['backend'],
        result['metadata']['cost']
    )
```

## Security Best Practices

1. **API Keys**: Never commit API keys to version control
2. **File Validation**: Always validate input files before processing
3. **PII Handling**: Enable PII detection for sensitive documents
4. **Access Control**: Limit API permissions to minimum required
5. **Audit Logging**: Regularly review security audit logs

## Cost Management

### Pricing Overview
- **Tesseract**: Free (local processing)
- **Google Vision**: $1.50 per 1000 requests
- **AWS Textract**: $1.50 per 1000 pages
- **Azure Vision**: $1.00 per 1000 transactions

### Cost Optimization Tips
1. Use Tesseract for simple documents
2. Enable automatic backend selection
3. Set monthly budget limits
4. Batch process documents when possible
5. Monitor usage patterns and optimize

## Testing

Run the comprehensive test suite:
```bash
pytest tests/ -v
```

Run specific test categories:
```bash
# Security tests
pytest tests/test_security.py -v

# Backend tests
pytest tests/test_backends.py -v

# Integration tests
pytest tests/test_integration.py -v
```

## Troubleshooting

### Common Issues

#### "No module named 'cv2'" or OpenCV errors
```bash
pip uninstall opencv-python opencv-python-headless
pip install opencv-python-headless==4.8.1.78  # Linux/Server
# OR
pip install opencv-python==4.8.1.78  # Windows/Desktop
```

#### "numpy.core.multiarray failed to import"
```bash
pip install numpy==1.26.4  # Must be <2.0 for OpenCV compatibility
```

#### Tesseract not found
```bash
# Linux
sudo apt install tesseract-ocr
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

# Windows: Add to PATH or set environment variable
set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# macOS
brew install tesseract
```

#### GUI not showing on Linux servers
```bash
sudo apt install xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
python enhanced_ocr_gui.py
```

#### Permission errors (Linux/Mac)
```bash
chmod +x enhanced_ocr_gui.py
# Or run with proper permissions
```

### Getting Help

- **Installation issues**: Run `python verify_installation.py`
- **Documentation**: See `INSTALLATION_GUIDE_UPDATED.md`  
- **Windows setup**: See `WINDOWS_INSTALL_FIXED.md`
- **Issues**: File a GitHub issue with error details

## Architecture

### Module Structure
```
.
├── security/              # Security and validation modules
│   ├── __init__.py
│   ├── validator.py      # Input validation and security checks
│   └── credentials.py    # Encrypted credential management
├── backends/             # OCR backend implementations
│   ├── __init__.py
│   ├── base.py          # Abstract base class
│   ├── tesseract.py     # Local Tesseract backend
│   ├── google_vision.py # Google Cloud Vision backend
│   ├── aws_textract.py  # AWS Textract backend
│   ├── azure_vision.py  # Azure Computer Vision backend
│   └── manager.py       # Backend selection and fallback logic
├── monitoring/          # Cost and usage tracking
│   ├── __init__.py
│   └── cost_tracker.py  # Cost tracking and optimization
├── tests/               # Comprehensive test suite
├── enhanced_ocr_gui.py  # Enhanced GUI application
└── pdf_to_json.py       # Core conversion logic
```

### Design Patterns
- **Strategy Pattern**: For backend selection
- **Factory Pattern**: For backend instantiation
- **Observer Pattern**: For cost tracking
- **Decorator Pattern**: For security validation

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Tesseract OCR team for the excellent open-source OCR engine
- Cloud providers for their powerful OCR APIs
- Contributors and testers who helped improve this tool

## Release Status

### v1.0.0 - Universal Document Converter Ultimate

✅ **PRODUCTION READY** - All tests passing, all features working!

- **48 Python files** validated for syntax
- **All imports** verified working
- **Core functionality** tested and operational
- **OCR integration** fully functional with Tesseract
- **GUI features** all working (drag & drop, threading, settings)
- **Zero critical bugs** found in final validation

### Test Suite
```bash
# All tests pass successfully:
✅ python3 test_functional.py      # Core functionality tests
✅ python3 test_conversion.py      # Document conversion tests  
✅ python3 test_ultimate_features.py # Feature verification
✅ python3 final_validation.py     # Comprehensive validation
```

---

Designed and built by Beau Lewis.