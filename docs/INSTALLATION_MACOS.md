# macOS Installation Guide

## Quick Document Convertor - macOS Installation

This guide provides comprehensive installation instructions for macOS systems.

## 🍎 System Requirements

### Supported Versions
- **macOS 10.13** (High Sierra) or later
- **macOS 11** (Big Sur) - Recommended
- **macOS 12** (Monterey) - Recommended
- **macOS 13** (Ventura) - Recommended
- **macOS 14** (Sonoma) - Recommended

### Hardware Requirements
- **Intel-based Mac** or **Apple Silicon (M1/M2/M3)**
- **4 GB RAM** minimum, 8 GB recommended
- **100 MB** free disk space
- **Internet connection** for initial setup

### Prerequisites
- **Python 3.8+** (usually pre-installed)
- **Xcode Command Line Tools** (for development installation)

## 📦 Installation Methods

### Method 1: DMG Installer (Recommended)

#### Download and Install
```bash
# Download the DMG file
curl -L -o QuickDocumentConvertor-2.0.0.dmg \
  https://github.com/Beaulewis1977/quick_doc_convertor/releases/latest/download/QuickDocumentConvertor-2.0.0.dmg

# Mount and install
open QuickDocumentConvertor-2.0.0.dmg
```

#### Manual Installation Steps
1. **Download** the DMG file from the releases page
2. **Double-click** the DMG file to mount it
3. **Drag** "Quick Document Convertor.app" to the Applications folder
4. **Eject** the DMG file
5. **Launch** from Applications or Spotlight

### Method 2: PKG Installer

#### Enterprise/Automated Installation
```bash
# Download the PKG installer
curl -L -o QuickDocumentConvertor-2.0.0.pkg \
  https://github.com/Beaulewis1977/quick_doc_convertor/releases/latest/download/QuickDocumentConvertor-2.0.0.pkg

# Install via command line
sudo installer -pkg QuickDocumentConvertor-2.0.0.pkg -target /
```

### Method 3: Homebrew Installation

#### Using Homebrew Package Manager
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add the tap (when available)
brew tap beaulewis1977/quick-doc-convertor

# Install the application
brew install quick-document-convertor

# Or install directly from cask
brew install --cask quick-document-convertor
```

### Method 4: Source Installation

#### Prerequisites
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and dependencies
brew install python-tk
```

#### Installation Steps
```bash
# Clone the repository
git clone https://github.com/Beaulewis1977/quick_doc_convertor.git
cd quick_doc_convertor

# Install Python dependencies
pip3 install -r requirements.txt

# Install macOS-specific dependencies
pip3 install py2app

# Set up the application
python3 setup_shortcuts.py

# Run the application
python3 universal_document_converter.py
```

### Method 5: Development Installation

#### For Contributors and Developers
```bash
# Clone the repository
git clone https://github.com/Beaulewis1977/quick_doc_convertor.git
cd quick_doc_convertor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install py2app pytest pytest-cov

# Install cross-platform dependencies
python build_all_platforms.py --install-deps

# Run tests
python test_cross_platform.py

# Build macOS app bundle
python build_all_platforms.py --platform macos
```

## 🔧 App Bundle Integration

### Automatic Integration
The installation automatically provides:
- **Native .app bundle** in Applications folder
- **Dock integration** with proper icon
- **Finder integration** for file associations
- **Spotlight search** support
- **Quick Look** preview support (future feature)
- **Services menu** integration (future feature)

### File Associations
The app registers to handle these file types:
- **PDF documents** (.pdf)
- **Microsoft Word** (.docx, .doc)
- **Plain text** (.txt)
- **HTML files** (.html, .htm)
- **Rich Text Format** (.rtf)
- **EPUB e-books** (.epub)
- **OpenDocument Text** (.odt)
- **CSV files** (.csv)

### Launch Services Registration
```bash
# Manually register the app (if needed)
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f /Applications/Quick\ Document\ Convertor.app

# Reset Launch Services (if file associations are broken)
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
```

## 🚀 Usage

### Launching the Application

#### From Applications Folder
1. Open **Finder**
2. Navigate to **Applications**
3. Double-click **Quick Document Convertor**

#### From Spotlight
1. Press **⌘ + Space** to open Spotlight
2. Type "Quick Document Convertor"
3. Press **Enter** to launch

#### From Dock
1. Drag the app from Applications to Dock (optional)
2. Click the Dock icon to launch

#### From Terminal
```bash
# Launch the app bundle
open -a "Quick Document Convertor"

# Or run directly
/Applications/Quick\ Document\ Convertor.app/Contents/MacOS/Quick\ Document\ Convertor
```

### File Operations

#### Opening Files
- **Drag and drop** files onto the app icon
- **Right-click** files and choose "Open with Quick Document Convertor"
- **Double-click** associated file types
- Use **File → Open** within the application

#### Converting Documents
1. Launch the application
2. Click "Select Files" or drag files into the window
3. Choose output format and location
4. Click "Convert" to process files

## 🔍 Troubleshooting

### Common Issues

#### App Won't Open - Security Warning
```bash
# If you see "App can't be opened because it's from an unidentified developer"
# Right-click the app and select "Open"
# Or use the command line:
sudo spctl --master-disable  # Disable Gatekeeper temporarily
open -a "Quick Document Convertor"
sudo spctl --master-enable   # Re-enable Gatekeeper
```

#### Python Not Found
```bash
# Install Python via Homebrew
brew install python

# Or download from python.org
# https://www.python.org/downloads/macos/
```

#### Missing Dependencies
```bash
# Install missing Python packages
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Install Tkinter if missing
brew install python-tk
```

#### File Association Issues
```bash
# Reset file associations
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user

# Re-register the application
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f /Applications/Quick\ Document\ Convertor.app
```

#### Permission Issues
```bash
# Fix app permissions
sudo chmod -R 755 /Applications/Quick\ Document\ Convertor.app

# Grant Full Disk Access (if needed)
# System Preferences → Security & Privacy → Privacy → Full Disk Access
# Add Quick Document Convertor to the list
```

### Log Files
Check log files for detailed error information:
```bash
# Application logs
tail -f ~/Library/Logs/Quick\ Document\ Convertor/app.log

# System logs
log show --predicate 'process == "Quick Document Convertor"' --last 1h
```

## 🔄 Updating

### DMG/PKG Update
1. Download the latest DMG or PKG file
2. Install over the existing version
3. The app will be automatically updated

### Homebrew Update
```bash
# Update Homebrew
brew update

# Upgrade the application
brew upgrade quick-document-convertor
```

### Source Update
```bash
cd quick_doc_convertor
git pull origin main
pip3 install -r requirements.txt --upgrade
python3 setup_shortcuts.py
```

## 🗑️ Uninstallation

### Complete Removal
```bash
# Remove the application
sudo rm -rf /Applications/Quick\ Document\ Convertor.app

# Remove user data (optional)
rm -rf ~/Library/Application\ Support/Quick\ Document\ Convertor
rm -rf ~/Library/Logs/Quick\ Document\ Convertor
rm -rf ~/Library/Caches/Quick\ Document\ Convertor

# Remove preferences (optional)
defaults delete com.beaulewis.quickdocumentconvertor

# Reset Launch Services
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
```

### Homebrew Removal
```bash
# Uninstall via Homebrew
brew uninstall quick-document-convertor

# Remove the tap
brew untap beaulewis1977/quick-doc-convertor
```

## 🔐 Security and Privacy

### Code Signing
The application is signed with a Developer ID certificate for security:
- **Developer**: Beau Lewis
- **Team ID**: [To be added when available]

### Privacy Permissions
The app may request access to:
- **Files and Folders** - To read and convert documents
- **Network** - For checking updates (optional)

### Notarization
The app is notarized by Apple for additional security verification.

## 🛠️ Building from Source

### Creating App Bundle
```bash
# Using py2app
python setup_macos.py py2app

# Using PyInstaller
pyinstaller --windowed --onedir --name "Quick Document Convertor" universal_document_converter.py

# Using the build script
python build_all_platforms.py --platform macos
```

### Creating DMG Installer
```bash
# Create DMG with proper layout
python -c "
from packaging.build_macos import create_standalone_dmg
from pathlib import Path
app_bundle = Path('dist/Quick Document Convertor.app')
dmg_path = Path('dist/QuickDocumentConvertor-2.0.0.dmg')
create_standalone_dmg(app_bundle, dmg_path)
"
```

## 📞 Support

### Getting Help
- **GitHub Issues**: https://github.com/Beaulewis1977/quick_doc_convertor/issues
- **Documentation**: https://github.com/Beaulewis1977/quick_doc_convertor/docs
- **Email**: blewisxx@gmail.com

### Reporting Bugs
When reporting issues, please include:
- macOS version (`sw_vers`)
- Hardware type (Intel/Apple Silicon)
- Python version (`python3 --version`)
- Error messages or crash logs
- Steps to reproduce the issue

### Contributing
See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines.

## 🎯 Tips and Tricks

### Performance Optimization
- Keep the app in Applications folder for best performance
- Grant Full Disk Access for faster file operations
- Use SSD storage for better conversion speeds

### Workflow Integration
- Add to Dock for quick access
- Use Spotlight to quickly find and launch
- Set up file associations for seamless workflow
- Use drag-and-drop for batch operations

### Keyboard Shortcuts
- **⌘ + O** - Open files
- **⌘ + S** - Save converted files
- **⌘ + Q** - Quit application
- **⌘ + ,** - Open preferences (future feature)
