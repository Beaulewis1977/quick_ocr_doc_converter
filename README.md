# Universal Document Converter Ultimate with Advanced OCR

A powerful Python application that converts multiple document formats (PDF, DOCX, TXT, HTML, RTF, EPUB) to various output formats with advanced OCR capabilities, multi-threaded processing, and a comprehensive GUI interface.

Designed and built by Beau Lewis.

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

## Universal Document Converter Ultimate

The most feature-rich version with comprehensive functionality:

### ✅ Verified Features (All Working)
- **Multi-Format Support**: Convert between DOCX, PDF, TXT, HTML, RTF, EPUB
- **OCR Integration**: Process images (JPG, PNG, TIFF, BMP, GIF, WebP) with Tesseract
- **Thread Selection**: GUI control for 1-32 worker threads
- **Drag & Drop**: Direct file/folder dropping support
- **API Server**: REST API for remote processing (optional)
- **Advanced Settings**: Tabbed interface with comprehensive options
- **Statistics Tracking**: Monitor conversions and export metrics
- **Performance Monitoring**: Real-time memory and CPU usage display
- **Configuration Persistence**: Save all settings in JSON format

### Quick Start
```bash
# Launch the Ultimate GUI
python3 universal_document_converter_ultimate.py

# Or use the launcher
python3 launch_ultimate.py
```

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

## Installation

### System Requirements
- Python 3.6+ (tested with 3.12)
- Tkinter (GUI framework)
- Tesseract OCR (for OCR functionality)

### Quick Install

#### Step 1: Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3-tk tesseract-ocr libxcursor1

# macOS
brew install python-tk tesseract

# Windows
# Install Python from python.org (includes tkinter)
# Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
```

#### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Launch the Application
```bash
python3 universal_document_converter_ultimate.py
```

### Optional Features
```bash
# For API server functionality
pip install flask flask-cors waitress

# For enhanced OCR (multiple backends)
pip install easyocr
```

## Usage

### Basic Usage

1. **Launch the application:**
   ```bash
   python3 universal_document_converter_ultimate.py
   ```

2. **Add files:**
   - Click "Add Files" or "Add Folder" buttons
   - Or drag and drop files/folders directly onto the window

3. **Configure settings:**
   - Select output format (TXT, DOCX, PDF, HTML, RTF, EPUB)
   - Enable OCR for image files
   - Adjust thread count (1-32) for performance
   - Choose output directory

4. **Convert:**
   - Click "Start Conversion"
   - Monitor progress in real-time
   - View results when complete

### Advanced Features

- **API Server**: Enable in the API tab for REST API access
- **OCR Settings**: Configure language, preprocessing, and backends
- **Statistics**: Track conversions and export metrics
- **Performance**: Adjust cache, memory, and queue settings

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