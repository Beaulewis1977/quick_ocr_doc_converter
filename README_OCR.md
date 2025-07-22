# OCR Document Converter 3.1.0

Complete OCR-powered document converter with enhanced functionality and cross-platform support.

## 🚀 Features

### Core Features
- **OCR Integration**: Full Tesseract OCR support for images and PDFs
- **Multi-format Support**: PDF, DOCX, TXT, HTML, RTF, PNG, JPG, TIFF, BMP, GIF
- **Batch Processing**: Convert multiple files and directories
- **GUI Interface**: User-friendly tkinter interface
- **Cross-platform**: Windows, macOS, Linux support
- **Performance Optimized**: Multi-threading and caching

### OCR Features
- **Image Text Recognition**: Extract text from images
- **PDF OCR**: Process scanned PDFs
- **Multi-language Support**: 100+ languages supported
- **Preprocessing**: Image enhancement for better OCR
- **Confidence Scoring**: OCR accuracy indicators

## 📦 Installation

### Quick Setup (Recommended)

1. **Clone or download the project**
```bash
git clone <repository-url>
cd ocr_reader
```

2. **Run automated setup**
```bash
# Windows
python setup_ocr.py

# macOS/Linux
python3 setup_ocr.py
```

3. **Manual installation (if needed)**
```bash
# Install Tesseract OCR
# Windows: winget install tesseract-ocr.tesseract-ocr
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# Install Python packages
pip install -r requirements_updated.txt
```

### System Dependencies

#### Windows
- Tesseract OCR 5.x: `winget install tesseract-ocr.tesseract-ocr`
- Python 3.8+ (with pip)

#### macOS
- Tesseract OCR: `brew install tesseract`
- Python 3.8+ (via Homebrew recommended)

#### Linux
- Tesseract OCR: `sudo apt-get install tesseract-ocr`
- Python 3.8+ and pip

## 🎯 Usage

### Command Line Interface

#### Basic Usage
```bash
# Convert single file
python cli_ocr.py document.pdf -o output.md

# Convert with OCR
python cli_ocr.py scanned.pdf -o output.md --ocr

# Batch conversion
python cli_ocr.py *.pdf -o ./converted/ --ocr --recursive

# Convert images with OCR
python cli_ocr.py *.png *.jpg -o ./text/ --ocr
```

#### Advanced Options
```bash
# Specify OCR language
python cli_ocr.py file.pdf -o output.md --ocr --ocr-lang eng+fra

# Multi-threaded processing
python cli_ocr.py input_dir/ -o output_dir/ --workers 8 --ocr

# Check OCR status
python cli_ocr.py --check-ocr

# Run setup
python cli_ocr.py --setup
```

### Graphical Interface

Launch the GUI application:
```bash
python gui_ocr.py
```

GUI Features:
- Drag & drop file selection
- OCR language selection
- Progress tracking
- Real-time logging
- Batch processing

### Programmatic Usage

```python
from ocr_engine import OCREngine

# Initialize OCR engine
ocr = OCREngine()

# Check availability
if ocr.is_available():
    # Extract text from image
    text = ocr.extract_text('document.png', language='eng')
    
    # Extract from PDF
    text = ocr.extract_text_from_pdf('scanned.pdf', language='eng')
    
    # Preprocess image
    processed = ocr.preprocess_image('image.jpg')
    text = ocr.extract_text_from_image(processed)
```

## 🌍 Supported Languages

### OCR Languages
- **English**: eng
- **Spanish**: spa
- **French**: fra
- **German**: deu
- **Japanese**: jpn
- **Chinese**: chi_sim, chi_tra
- **Russian**: rus
- **Arabic**: ara
- **100+ more languages...**

### Document Formats

#### Input Formats
- **Images**: PNG, JPG, JPEG, TIFF, BMP, GIF
- **Documents**: PDF, DOCX, TXT, HTML, RTF

#### Output Formats
- **Text**: TXT, Markdown (MD)
- **Structured**: HTML, DOCX
- **Raw**: JSON (with metadata)

## ⚙️ Configuration

### OCR Settings
Create `ocr_config.json`:
```json
{
  "ocr": {
    "languages": ["eng", "spa"],
    "preprocessing": true,
    "confidence_threshold": 0.8,
    "batch_size": 10
  },
  "performance": {
    "max_workers": 4,
    "cache_enabled": true,
    "memory_limit": "2GB"
  }
}
```

### Performance Tuning
- **Memory**: 15-45MB per file (configurable up to 2GB)
- **Speed**: 0.02s/1MB text, 2-10s per image OCR
- **Batch Size**: Optimal at 10-50 files
- **Workers**: Match CPU cores (typically 4-8)

## 🔧 Troubleshooting

### Common Issues

#### "Tesseract not found"
```bash
# Check installation
tesseract --version

# Manual path setup (Windows)
# Add to PATH: C:\Program Files\Tesseract-OCR
```

#### "OCR accuracy low"
```bash
# Enable preprocessing
python cli_ocr.py file.jpg --ocr --preprocess

# Try different language
python cli_ocr.py file.pdf --ocr --ocr-lang eng+spa
```

#### "Memory issues"
```bash
# Reduce batch size
python cli_ocr.py *.pdf --workers 2 --batch-size 5
```

### Error Codes
- **0**: Success
- **1**: Input file not found
- **2**: OCR engine not available
- **3**: Unsupported format
- **4**: Memory limit exceeded
- **5**: System dependency missing

## 📊 Performance Metrics

### Benchmarks
- **Small files** (< 1MB): 0.1-0.5 seconds
- **Medium files** (1-10MB): 1-5 seconds
- **Large files** (> 10MB): 5-30 seconds
- **Images** (300 DPI): 2-10 seconds per page
- **PDFs**: 0.5-2 seconds per page

### Memory Usage
- **Idle**: 15MB
- **Processing**: 45-200MB per file
- **Peak**: Configurable up to 2GB

## 🔄 Integration

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Convert documents
  run: |
    python cli_ocr.py *.pdf --ocr --output ./converted/
    python cli_ocr.py --check-ocr
```

### API Usage
```python
# Simple API wrapper
from ocr_engine import OCREngine
from pathlib import Path

class DocumentAPI:
    def __init__(self):
        self.ocr = OCREngine()
    
    def convert(self, file_path: str, **kwargs):
        # Process document
        pass
```

## 📈 Development

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/awesome-feature`
3. Make changes and test
4. Submit pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements_updated.txt
pip install pytest black flake8

# Run tests
python -m pytest tests/

# Code formatting
black .
flake8 .
```

## 📝 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Issues**: Report on GitHub Issues
- **Documentation**: See DOCS/ directory
- **Examples**: Check examples/ folder
- **Community**: Join our Discord/Slack

---

**Quick Start**: Run `python setup_ocr.py` for automated setup!