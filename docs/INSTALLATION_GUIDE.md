# Universal Document Converter - Complete Installation Guide

This guide covers all installation methods for the Universal Document Converter v2.1.0 on Windows, macOS, and Linux systems.

## Table of Contents
1. [Quick Install (Windows)](#quick-install-windows)
2. [Detailed Windows Installation](#detailed-windows-installation)
3. [macOS Installation](#macos-installation)
4. [Linux Installation](#linux-installation)
5. [Python Source Installation](#python-source-installation)
6. [VFP9/VB6 Integration Setup](#vfp9vb6-integration-setup)
7. [OCR Setup](#ocr-setup)
8. [Verifying Installation](#verifying-installation)
9. [Uninstallation](#uninstallation)

## Quick Install (Windows)

### Option 1: Complete Package (Recommended)
1. Download [Universal-Document-Converter-v2.1.0-Windows-Complete.zip](https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/Universal-Document-Converter-v2.1.0-Windows-Complete.zip)
2. Extract to desired location (e.g., `C:\Program Files\UniversalConverter`)
3. Double-click `run_converter.bat`
4. Done! The GUI will open.

### Option 2: Using PowerShell (One-liner)
```powershell
# Run this in PowerShell as Administrator
Invoke-WebRequest -Uri "https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/Universal-Document-Converter-v2.1.0-Windows-Complete.zip" -OutFile "$env:TEMP\UDC.zip"; Expand-Archive -Path "$env:TEMP\UDC.zip" -DestinationPath "C:\UniversalConverter" -Force; Start-Process "C:\UniversalConverter\run_converter.bat"
```

## Detailed Windows Installation

### Prerequisites
- Windows 7 or later (32-bit or 64-bit)
- Optional: Python 3.8+ (only if installing from source)
- Optional: Administrator rights (for system-wide installation)

### Step-by-Step Installation

#### 1. Download the Package
- Go to [Releases Page](https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest)
- Download `Universal-Document-Converter-v2.1.0-Windows-Complete.zip` (63 KB)
- Save to your Downloads folder

#### 2. Extract the Files
- Navigate to Downloads folder
- Right-click on the ZIP file
- Select "Extract All..."
- Choose destination:
  - User install: `C:\Users\%USERNAME%\AppData\Local\UniversalConverter`
  - System install: `C:\Program Files\UniversalConverter` (requires admin)
- Click "Extract"

#### 3. Create Desktop Shortcut (Optional)
- Navigate to extraction folder
- Right-click on `run_converter.bat`
- Select "Send to" → "Desktop (create shortcut)"
- Rename shortcut to "Universal Document Converter"

#### 4. Add to PATH (Optional, for CLI access)
1. Press `Win + X`, select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", select "Path" and click "Edit"
5. Click "New" and add your installation path
6. Click "OK" to save

#### 5. First Run
- Double-click `run_converter.bat` or desktop shortcut
- Windows Defender may show a warning - click "More info" → "Run anyway"
- The GUI should open showing the drag-and-drop interface

### Installing Additional Components

#### MSI Installer Method
If you prefer a traditional installer:
```bash
# From the source directory
python create_windows_installer.py
# This creates an MSI installer in the dist folder
```

#### Installing 32-bit DLL for VFP9/VB6
1. Download [UniversalConverter32.dll.zip](https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/UniversalConverter32.dll.zip)
2. Extract to your application directory
3. Register if needed: `regsvr32 UniversalConverter32.dll`

## macOS Installation

### Using Homebrew (Recommended)
```bash
# Install Python if not already installed
brew install python@3.11

# Clone the repository
git clone https://github.com/Beaulewis1977/quick_ocr_doc_converter.git
cd quick_ocr_doc_converter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install OCR support
brew install tesseract
pip install pytesseract easyocr

# Create alias for easy access
echo "alias udc='python $(pwd)/universal_document_converter_ocr.py'" >> ~/.zshrc
source ~/.zshrc
```

### Manual Installation
1. Download source code from [GitHub](https://github.com/Beaulewis1977/quick_ocr_doc_converter/archive/refs/heads/main.zip)
2. Extract to `~/Applications/UniversalConverter`
3. Open Terminal and navigate to the directory
4. Run: `pip3 install -r requirements.txt`
5. Run: `python3 universal_document_converter_ocr.py`

### Creating macOS App Bundle
```bash
# Install py2app
pip install py2app

# Create setup file
cat > setup.py << EOF
from setuptools import setup

APP = ['universal_document_converter_ocr.py']
DATA_FILES = ['ocr_engine', 'icon.ico']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'PIL', 'docx', 'PyPDF2', 'markdown'],
    'iconfile': 'icon.ico',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
EOF

# Build the app
python setup.py py2app

# The app will be in dist/universal_document_converter_ocr.app
```

## Linux Installation

### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv python3-tk

# Install system dependencies for OCR
sudo apt install tesseract-ocr tesseract-ocr-eng

# Clone repository
git clone https://github.com/Beaulewis1977/quick_ocr_doc_converter.git
cd quick_ocr_doc_converter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install pytesseract easyocr

# Create desktop entry
cat > ~/.local/share/applications/universal-converter.desktop << EOF
[Desktop Entry]
Type=Application
Name=Universal Document Converter
Comment=Convert documents between formats with OCR support
Exec=/path/to/venv/bin/python /path/to/universal_document_converter_ocr.py
Icon=/path/to/icon.ico
Terminal=false
Categories=Office;Utility;
EOF

# Make it executable
chmod +x ~/.local/share/applications/universal-converter.desktop
```

### Fedora/RHEL/CentOS
```bash
# Install dependencies
sudo dnf install python3 python3-pip python3-tkinter tesseract tesseract-langpack-eng

# Follow the same steps as Ubuntu from "Clone repository" onwards
```

### Arch Linux
```bash
# Install dependencies
sudo pacman -S python python-pip tk tesseract tesseract-data-eng

# Install from AUR (if available) or follow manual steps
yay -S universal-document-converter

# Or manual installation following Ubuntu steps
```

## Python Source Installation

### For Developers and Advanced Users

#### 1. Prerequisites
- Python 3.8 or higher
- Git (optional, for cloning)
- pip (Python package manager)

#### 2. Get the Source Code
```bash
# Option A: Clone with Git
git clone https://github.com/Beaulewis1977/quick_ocr_doc_converter.git
cd quick_ocr_doc_converter

# Option B: Download ZIP
# Download from https://github.com/Beaulewis1977/quick_ocr_doc_converter/archive/main.zip
# Extract and navigate to the directory
```

#### 3. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
# Basic installation
pip install -r requirements.txt

# Full installation with OCR
pip install -r requirements.txt
pip install pytesseract easyocr

# Development installation (includes testing tools)
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 5. Install as Package (Optional)
```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

## VFP9/VB6 Integration Setup

### Installing the 32-bit DLL

#### For VFP9 Developers
1. Download [UniversalConverter32.dll.zip](https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/UniversalConverter32.dll.zip)
2. Extract contents to your VFP9 project directory
3. Copy `UniversalConverter_VFP9.prg` to your project
4. In VFP9, run:
   ```foxpro
   SET PROCEDURE TO UniversalConverter_VFP9.prg ADDITIVE
   ```

#### For VB6 Developers
1. Download the DLL package (same as above)
2. Extract to your VB6 project directory
3. Add `VB6_UniversalConverter.bas` to your project
4. In VB6 IDE:
   - Project → Add Module → Existing
   - Select `VB6_UniversalConverter.bas`
5. Register DLL (if using COM):
   ```cmd
   regsvr32 UniversalConverter32.dll
   ```

### Testing the Integration
```vb
' VB6 Test
Private Sub TestConverter()
    If IsConverterAvailable() Then
        MsgBox "Converter is ready!"
        Dim success As Boolean
        success = ConvertMarkdownToRTF("test.md", "test.rtf")
        If success Then
            MsgBox "Conversion successful!"
        End If
    End If
End Sub
```

## OCR Setup

### Windows OCR Setup

#### Installing Tesseract
1. Download Tesseract installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer (tesseract-ocr-w64-setup-5.x.x.exe)
3. During installation, select additional languages if needed
4. Add Tesseract to PATH:
   - Default path: `C:\Program Files\Tesseract-OCR`
   - Add to system PATH as described earlier

#### Installing EasyOCR (Optional)
```bash
# Requires Python installation
pip install easyocr

# First run will download models (may take time)
python -c "import easyocr; reader = easyocr.Reader(['en'])"
```

### macOS OCR Setup
```bash
# Using Homebrew
brew install tesseract
brew install tesseract-lang  # For additional languages

# Verify installation
tesseract --version
```

### Linux OCR Setup
```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-fra  # French
sudo apt install tesseract-ocr-deu  # German
sudo apt install tesseract-ocr-spa  # Spanish

# List available languages
apt-cache search tesseract-ocr-

# Verify installation
tesseract --list-langs
```

## Verifying Installation

### Basic Verification
```bash
# Check if the converter runs
python universal_document_converter_ocr.py --version

# Test conversion
python universal_document_converter_ocr.py test.txt test.pdf

# Test OCR
python universal_document_converter_ocr.py scan.pdf text.txt --ocr
```

### Running Test Suite
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python test_converter.py

# Run integration tests
python test_all_integration_methods.py
```

### GUI Verification
1. Run `run_converter.bat` (Windows) or `python universal_document_converter_ocr.py`
2. The GUI should open
3. Try dragging a file onto the window
4. Check that format dropdown shows all options
5. Test a simple conversion

## Uninstallation

### Windows Uninstallation
1. **For ZIP installation**:
   - Delete the installation folder
   - Remove desktop shortcuts
   - Remove from PATH if added

2. **For MSI installation**:
   - Go to Control Panel → Programs and Features
   - Find "Universal Document Converter"
   - Click Uninstall

### macOS Uninstallation
```bash
# Remove application folder
rm -rf ~/Applications/UniversalConverter

# Remove command alias
sed -i '' '/alias udc=/d' ~/.zshrc

# Remove app bundle if created
rm -rf /Applications/universal_document_converter_ocr.app
```

### Linux Uninstallation
```bash
# Remove application folder
rm -rf ~/UniversalConverter

# Remove desktop entry
rm ~/.local/share/applications/universal-converter.desktop

# Remove virtual environment
rm -rf /path/to/venv
```

## Troubleshooting Installation

### Common Issues

1. **"Python not found"**
   - Install Python from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **"pip: command not found"**
   ```bash
   # Windows
   python -m ensurepip --upgrade
   
   # Linux/macOS
   python3 -m ensurepip --upgrade
   ```

3. **"No module named tkinter"**
   ```bash
   # Ubuntu/Debian
   sudo apt install python3-tk
   
   # Fedora
   sudo dnf install python3-tkinter
   
   # macOS (should be included)
   brew install python-tk
   ```

4. **Permission errors during installation**
   - Use `pip install --user` instead of `pip install`
   - Or use a virtual environment (recommended)

5. **Antivirus blocking the executable**
   - Add an exception for the installation folder
   - Temporarily disable antivirus during installation
   - Download from official GitHub releases only

### Getting Help
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions
- Visit [GitHub Issues](https://github.com/Beaulewis1977/quick_ocr_doc_converter/issues)
- See [FAQ.md](FAQ.md) for common questions

---

**Installation Complete!** 🎉 See [USER_MANUAL.md](USER_MANUAL.md) for usage instructions.