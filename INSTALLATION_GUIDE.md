# OCR Document Converter v3.1.0 - Installation Guide

## 🚀 Quick Start (Easiest Method)

### For End Users (No Technical Knowledge Required)

1. **Download the complete package** from [GitHub Releases](https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest)
2. **Extract all files** to a folder
3. **Double-click one of these files**:
   - `⚡ Quick Launch OCR.bat` - Windows launcher with enhanced features
   - `run_ocr_converter.bat` - Main Windows launcher
   - `run_converter.sh` - Linux/macOS launcher
4. **That's it!** The OCR Document Converter will start automatically

### For Desktop Shortcuts & Taskbar Pinning

1. **Run the installer** `install.bat` (Windows) or `setup_shortcuts.py` (Linux/Mac)
2. **Follow the prompts** - it will automatically:
   - Install all required Python packages including OCR dependencies
   - Create desktop shortcut for "OCR Document Converter"
   - Add to Start Menu (Windows) or Applications menu (Linux/Mac)
   - Set up Google Vision API support (optional)
3. **Pin to taskbar** (Windows):
   - Right-click the desktop shortcut
   - Select "Pin to taskbar"
4. **Pin to dock** (Mac):
   - Drag the application to your dock

---

## 🔧 Advanced Installation Options

### Option 1: Create Windows Installer (No Python Required)

**Perfect for distribution to users without Python installed**

1. **Run the Windows installer creator**:
   ```bash
   setup_windows_installer.bat
   ```
2. **Wait for compilation** (may take a few minutes)
3. **Find your installer** in the `dist_installer/` folder
4. **Distribute the installer** - it works on any Windows computer with admin rights!

**Benefits:**
- ✅ No Python installation required on target computers
- ✅ Professional Windows installer with shortcuts
- ✅ Automatic dependency installation
- ✅ Can be pinned to taskbar/start menu
- ✅ Professional deployment with uninstaller

### Option 2: Manual Python Setup

**For developers or advanced users**

1. **Install Python 3.8+** from [python.org](https://python.org)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install OCR dependencies**:
   ```bash
   python install_ocr_dependencies.py
   ```
4. **Run the application**:
   ```bash
   python universal_document_converter_ocr.py
   ```

### Option 3: Virtual Environment (Recommended for Developers)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install OCR dependencies
python install_ocr_dependencies.py

# Run application
python universal_document_converter_ocr.py
```

### Option 4: Chocolatey Installation (Windows)

```bash
# Install via Chocolatey (when available)
choco install ocr-document-converter

# Or from local package
choco install ocr-document-converter --source .
```

---

## 🆕 **New Features in v3.1.0**

### Google Vision API Integration
- **Cloud-based OCR** with superior accuracy
- **Automatic fallback** to free OCR engines if API fails
- **Real-time engine status** in GUI
- **Cost optimization** with intelligent usage

### Enhanced User Interface
- **Input format selection** for better processing accuracy
- **Legacy Integration tab** for VB6/VFP9 development
- **Real-time OCR engine switching**
- **Improved batch processing**

### Additional Output Formats
- **Markdown** (.md) - GitHub-flavored markdown
- **HTML** (.html) - Web-ready documents
- **EPUB** (.epub) - E-book format

---

## 📱 Platform-Specific Instructions

### Windows

**Easiest Methods:**
1. Double-click `⚡ Quick Launch OCR.bat` (enhanced launcher)
2. Double-click `run_ocr_converter.bat` (main launcher)
3. Run `install.bat` as Administrator for permanent installation with shortcuts

**Professional Installation:**
- Run `setup_windows_installer.bat` to create distributable installer
- Use Chocolatey package for enterprise deployment

**File Associations:**
- The app will help you set up OCR and document conversion associations
- Use Tools → Setup File Associations for guidance

**Taskbar Pinning:**
- Right-click any shortcut → "Pin to taskbar"

### macOS

**Easiest Methods:**
1. Double-click `run_converter.sh` (after making executable with `chmod +x`)
2. Run `setup_shortcuts.py` for Applications menu entry
3. Use `python3 universal_document_converter_ocr.py` from terminal

**OCR Dependencies:**
```bash
# Install Tesseract via Homebrew
brew install tesseract

# Install additional OCR dependencies
python3 install_ocr_dependencies.py
```

**Dock Pinning:**
- Drag the application icon to your dock while it's running

### Linux

**Easiest Methods:**
1. Double-click `run_converter.sh` (if GUI file manager supports it)
2. Run `setup_shortcuts.py` for desktop entry
3. Terminal: `python3 universal_document_converter_ocr.py`
4. Install OCR dependencies: `python3 install_ocr_dependencies.py`

**OCR Dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# CentOS/RHEL/Fedora
sudo dnf install tesseract

# Then install Python OCR dependencies
python3 install_ocr_dependencies.py
```

**Desktop Integration:**
- The setup script creates proper .desktop files
- Applications will appear in your applications menu

---

## 🔍 Troubleshooting

### "Python is not recognized"
- **Solution**: Install Python 3.8+ from [python.org](https://python.org)
- **Windows**: Make sure to check "Add Python to PATH" during installation

### "No module named 'tkinter'"
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **CentOS/RHEL**: `sudo yum install tkinter`
- **macOS**: Usually included with Python

### Google Vision API Setup Issues
- **Missing API Key**: Follow the Google Vision API setup guide
- **Permission Errors**: Ensure service account has Vision API User role
- **Network Issues**: Check firewall settings and internet connection

### OCR Dependencies Missing
- **Automatic**: Run `install_ocr_dependencies.py`
- **Manual Tesseract**: Download from [GitHub](https://github.com/tesseract-ocr/tesseract)
- **EasyOCR Issues**: Ensure sufficient RAM (4GB+ recommended)

### "Permission denied" (Linux/Mac)
```bash
chmod +x run_converter.sh
chmod +x setup_shortcuts.py
```

### Missing Dependencies
- **Automatic**: Run `install.bat` (Windows) or `setup_shortcuts.py` (Linux/Mac)
- **Manual**: `pip install -r requirements.txt`
- **OCR specific**: `python install_ocr_dependencies.py`

### Legacy Integration Issues (VB6/VFP9)
- See [Legacy Integration Guide](LEGACY_INTEGRATION_GUIDE.md)
- Use the Legacy Integration tab in the GUI for automated setup
- Check VB6/VFP9 integration documentation

---

## 📦 Distribution Options

### For Personal Use
- Use `⚡ Quick Launch OCR.bat` or `run_ocr_converter.bat`
- Run `install.bat` once for permanent installation with shortcuts

### For Team/Organization Distribution
1. **Create installer**: Run `setup_windows_installer.bat`
2. **Distribute the installer** from the `dist_installer/` folder
3. **No Python required** on target computers

### For Chocolatey Distribution
1. **Build package**: Use files in `chocolatey/` folder
2. **Test locally**: `choco install ocr-document-converter --source .`
3. **Submit to Chocolatey**: Follow Chocolatey submission guidelines

### For Developers
- Clone the repository
- Set up virtual environment
- Install in development mode

---

## 🎯 Quick Reference

| Method | Best For | Requirements | Features |
|--------|----------|--------------|----------|
| `⚡ Quick Launch OCR.bat` | Windows users | Python installed | Enhanced features, OCR |
| `run_ocr_converter.bat` | Windows users | Python installed | Full functionality |
| `install.bat` | Permanent installation | Admin rights | Desktop shortcuts, Start Menu |
| `setup_windows_installer.bat` | Distribution | PyInstaller | No Python required on target |
| Manual Python | Developers | Python + packages | Full control |

---

## 💡 Tips

- **First time users**: Start with `⚡ Quick Launch OCR.bat` (Windows) or download complete package
- **Want desktop shortcut**: Use `install.bat` (Windows) or `setup_shortcuts.py` (Linux/Mac)
- **Distributing to others**: Use `setup_windows_installer.bat`
- **Development**: Use virtual environment setup
- **OCR not working**: Run `install_ocr_dependencies.py`
- **Need Google Vision API**: See Google Vision API setup guide
- **Legacy VB6/VFP9**: Use Legacy Integration tab in GUI
- **Having issues**: Check the troubleshooting section above

## 🔗 Additional Resources

- **Main Documentation**: [README.md](README.md)
- **Legacy Integration**: [LEGACY_INTEGRATION_GUIDE.md](LEGACY_INTEGRATION_GUIDE.md)
- **Google Vision Setup**: [GOOGLE_VISION_SETUP.md](GOOGLE_VISION_SETUP.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **VB6/VFP9 Integration**: [VFP9_VB6_INTEGRATION_GUIDE.md](VFP9_VB6_INTEGRATION_GUIDE.md)

The application is designed to be as easy as possible to run - just download, extract, and launch!