# Universal Document Converter Complete

A powerful, feature-rich document and image conversion tool with OCR support, multi-threading, and an intuitive GUI.

![Version](https://img.shields.io/badge/version-3.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-purple)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## 🌟 Features

### Core Features
- **Universal Format Support**: Convert DOCX, PDF, TXT, RTF, ODT, HTML, EPUB, XML, JSON, CSV to Markdown
- **OCR Integration**: Extract text from images (JPG, PNG, TIFF, BMP, GIF, WebP) and scanned PDFs
- **Multi-threaded Processing**: Concurrent file conversion with configurable thread count
- **Batch Processing**: Convert entire folders while preserving directory structure
- **Drag & Drop**: Simply drag folders onto the application window
- **Smart Detection**: Automatically identifies scanned PDFs that need OCR

### Advanced Features
- **Configuration Management**: Save and load custom settings profiles
- **Memory Monitoring**: Real-time memory usage tracking with automatic cleanup
- **Progress Tracking**: Detailed progress bars and file-by-file status updates
- **Compression Support**: Optional output file compression to save space
- **Logging System**: Comprehensive logging for debugging and audit trails
- **Recent Folders**: Quick access to recently used directories
- **Keyboard Shortcuts**: Efficient workflow with keyboard navigation

### GUI Features
- **Modern Interface**: Clean, intuitive design with tabbed settings
- **File Preview**: Tree view of files to be converted with status indicators
- **Real-time Statistics**: Live conversion statistics and time tracking
- **Context Menus**: Right-click options for file management
- **Responsive Design**: Adapts to different screen sizes
- **Dark Mode Support**: Easy on the eyes during extended use (coming soon)

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB for installation + space for converted files

### Python Dependencies

#### Core Dependencies (Required)
```
python-docx>=0.8.11
PyPDF2>=3.0.0
beautifulsoup4>=4.11.0
```

#### OCR Dependencies (Optional)
```
pytesseract>=0.3.10
Pillow>=9.0.0
opencv-python>=4.5.0
numpy>=1.21.0
```

#### Enhanced Features (Optional)
```
psutil>=5.9.0          # Memory monitoring
tkinterdnd2>=0.3.0     # Drag & drop support
striprtf>=0.0.22       # RTF support
html2text>=2020.1.16   # Better HTML conversion
ebooklib>=0.18         # EPUB support
odfpy>=1.4.1          # ODT support
```

## 🚀 Installation

### Method 1: Windows Installer (Recommended for Windows)

1. Download the latest installer from the releases page:
   - `UniversalDocumentConverter_Setup.exe` - Full installer
   - `UniversalDocumentConverter_Portable.zip` - Portable version

2. Run the installer and follow the setup wizard

3. Launch from Start Menu or Desktop shortcut

### Method 2: Python Installation (All Platforms)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/universal-document-converter.git
   cd universal-document-converter
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   # Basic installation (document conversion only)
   pip install -r requirements_basic.txt
   
   # Full installation (with OCR support)
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR (for OCR support):**
   
   **Windows:**
   - Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
   - Add Tesseract to PATH or set TESSDATA_PREFIX environment variable
   
   **macOS:**
   ```bash
   brew install tesseract
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr
   ```

5. **Run the application:**
   ```bash
   python universal_document_converter_complete.py
   ```

### Method 3: Build from Source (Windows Executable)

1. **Install build dependencies:**
   ```bash
   pip install pyinstaller
   ```

2. **Run the build script:**
   ```bash
   python build_windows_executable.py
   ```

3. **Find the executable in:**
   - `dist/UniversalDocumentConverter.exe`
   - `UniversalDocumentConverter_Portable.zip`

## 📖 Usage Guide

### Basic Usage

1. **Launch the application**
   - Windows: Double-click the desktop shortcut or .exe file
   - Command line: `python universal_document_converter_complete.py`

2. **Select input folder**
   - Click "Browse" next to Input Folder
   - Or drag and drop a folder onto the window
   - Or use Ctrl+O

3. **Select output folder**
   - Click "Browse" next to Output Folder
   - Or use Ctrl+S

4. **Configure settings**
   - Enable/disable OCR mode for image processing
   - Set thread count for parallel processing
   - Choose whether to preserve folder structure
   - Select overwrite behavior

5. **Start conversion**
   - Click "Convert" button
   - Or press Ctrl+R
   - Monitor progress in real-time

### OCR Mode

1. **Enable OCR**
   - Check "Enable OCR for images" in the OCR tab
   - Verify OCR status shows green checkmark

2. **Configure OCR settings**
   - Select language (Tools → OCR Settings)
   - Adjust confidence threshold
   - Choose processing options

3. **Supported image formats**
   - JPG/JPEG
   - PNG
   - TIFF/TIF
   - BMP
   - GIF
   - WebP
   - Scanned PDFs (auto-detected)

### Advanced Features

#### Thread Configuration
- Adjust worker threads based on your CPU
- Default: 4 threads
- Recommended: Number of CPU cores

#### Batch Processing
- Process multiple folders using Tools → Batch Convert
- Create processing queues
- Schedule conversions

#### Memory Management
- Monitor memory usage in toolbar
- Set memory limits in Advanced settings
- Automatic cleanup between batches

#### Keyboard Shortcuts
- `Ctrl+O` - Select input folder
- `Ctrl+S` - Select output folder
- `Ctrl+R` - Start conversion
- `Escape` - Stop conversion
- `F1` - Show help

## ⚙️ Configuration

### Settings Location
- Windows: `%USERPROFILE%\.document_converter\settings.json`
- macOS: `~/Library/Application Support/document_converter/settings.json`
- Linux: `~/.config/document_converter/settings.json`

### Configuration Options

```json
{
  "theme": "default",
  "max_workers": 4,
  "output_format": "markdown",
  "preserve_structure": true,
  "overwrite_existing": false,
  "ocr_enabled": false,
  "ocr_language": "eng",
  "ocr_confidence_threshold": 60,
  "compression_enabled": false,
  "compression_level": 6,
  "logging_enabled": true,
  "log_level": "INFO",
  "auto_open_output": true,
  "notification_enabled": true,
  "batch_size": 10,
  "memory_limit_mb": 500,
  "cache_enabled": true,
  "cache_size_mb": 100
}
```

### OCR Languages

Supported languages (install additional language packs for Tesseract):
- `eng` - English
- `fra` - French
- `deu` - German
- `spa` - Spanish
- `ita` - Italian
- `por` - Portuguese
- `rus` - Russian
- `jpn` - Japanese
- `chi_sim` - Chinese Simplified

## 🔧 Troubleshooting

### Common Issues

#### "OCR not available"
1. Install Tesseract OCR for your platform
2. Install Python dependencies: `pip install pytesseract pillow opencv-python`
3. Restart the application

#### "No module named tkinter"
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Tkinter is included with Python

#### "Permission denied" errors
- Run as administrator (Windows)
- Check folder permissions
- Disable antivirus temporarily

#### Slow conversion
- Reduce thread count if system is overloaded
- Enable compression for large files
- Process in smaller batches

### Debug Mode

Run the debug script to check your installation:
```bash
python debug_converter.py
```

This will test:
- Python version compatibility
- Required dependencies
- OCR functionality
- File system permissions
- Threading support

## 📊 Performance Tips

1. **Optimal Thread Count**
   - CPU-bound tasks: Use CPU core count
   - I/O-bound tasks: Use 2x CPU core count
   - Mixed workload: Use 1.5x CPU core count

2. **Memory Management**
   - Close other applications during large conversions
   - Increase memory limit for better performance
   - Enable compression for output files

3. **OCR Optimization**
   - Pre-process images for better quality
   - Use appropriate language packs
   - Adjust confidence threshold based on image quality

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `python debug_converter.py`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- Designed and built by **Beau Lewis** (blewisxx@gmail.com)
- OCR powered by Tesseract
- GUI framework: Tkinter
- Document processing libraries: python-docx, PyPDF2
- Special thanks to all contributors and testers

## 📧 Contact

- **Email**: blewisxx@gmail.com
- **GitHub**: [Universal Document Converter](https://github.com/yourusername/universal-document-converter)
- **Issues**: [Report bugs or request features](https://github.com/yourusername/universal-document-converter/issues)

## 🔄 Version History

### Version 3.0 (Current)
- Complete rewrite with enhanced GUI
- OCR integration for image processing
- Multi-threading support
- Advanced configuration management
- Memory monitoring and optimization
- Comprehensive error handling

### Version 2.0
- Added batch processing
- Improved PDF handling
- Basic GUI implementation

### Version 1.0
- Initial release
- Basic document conversion
- Command-line interface

---

Made with ❤️ by Beau Lewis