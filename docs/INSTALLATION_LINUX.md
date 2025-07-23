# Linux Installation Guide

## Quick Document Convertor - Linux Installation

This guide provides comprehensive installation instructions for Linux distributions.

## 🐧 Supported Distributions

### Tested Distributions
- **Ubuntu** 20.04 LTS, 22.04 LTS, 24.04 LTS
- **Debian** 11 (Bullseye), 12 (Bookworm)
- **CentOS** 8, 9
- **RHEL** 8, 9
- **Fedora** 36, 37, 38, 39
- **Arch Linux** (current)
- **openSUSE** Leap 15.4+

### Requirements
- **Python** 3.8 or higher
- **Tkinter** (python3-tk)
- **Desktop Environment** (GNOME, KDE, XFCE, etc.)

## 📦 Installation Methods

### Method 1: Package Installation (Recommended)

#### Ubuntu/Debian (.deb package)
```bash
# Download the .deb package
wget https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/quick-document-convertor_3.1.0_all.deb

# Install the package
sudo dpkg -i quick-document-convertor_3.1.0_all.deb

# Install dependencies if needed
sudo apt-get install -f
```

#### CentOS/RHEL/Fedora (.rpm package)
```bash
# Download the .rpm package
wget https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/quick-document-convertor-3.1.0-1.noarch.rpm

# Install the package
sudo rpm -ivh quick-document-convertor-3.1.0-1.noarch.rpm

# Or using dnf (Fedora)
sudo dnf install quick-document-convertor-3.1.0-1.noarch.rpm

# Or using yum (CentOS/RHEL)
sudo yum install quick-document-convertor-3.1.0-1.noarch.rpm
```

#### Universal AppImage
```bash
# Download the AppImage
wget https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/QuickDocumentConvertor-3.1.0-x86_64.AppImage

# Make it executable
chmod +x QuickDocumentConvertor-3.1.0-x86_64.AppImage

# Run the application
./QuickDocumentConvertor-3.1.0-x86_64.AppImage

# Optional: Move to /usr/local/bin for system-wide access
sudo mv QuickDocumentConvertor-3.1.0-x86_64.AppImage /usr/local/bin/quick-document-convertor
```

### Method 2: Source Installation

#### Prerequisites
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk python3-dev git

# CentOS/RHEL/Fedora
sudo dnf install python3 python3-pip python3-tkinter python3-devel git

# Arch Linux
sudo pacman -S python python-pip tk git
```

#### Installation Steps
```bash
# Clone the repository
git clone https://github.com/Beaulewis1977/quick_ocr_doc_converter.git
cd quick_ocr_doc_converter

# Install Python dependencies
pip3 install -r requirements.txt

# Set up desktop integration
python3 setup_shortcuts.py

# Run the application
python3 universal_document_converter_ocr.py
```

### Method 3: Development Installation

#### For Contributors and Developers
```bash
# Clone the repository
git clone https://github.com/Beaulewis1977/quick_ocr_doc_converter.git
cd quick_ocr_doc_converter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Install cross-platform dependencies
python build_all_platforms.py --install-deps

# Run tests
python test_cross_platform.py

# Set up development environment
python setup_shortcuts.py
```

## 🔧 Desktop Integration

### Automatic Integration
The installation automatically creates:
- **Desktop entry** in applications menu
- **MIME type associations** for supported file formats
- **File manager integration** (right-click context menu)
- **Icon installation** in system icon theme

### Manual Integration
If automatic integration fails:

```bash
# Create desktop entry manually
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/quick-document-convertor.desktop << 'EOF'
[Desktop Entry]
Name=Quick Document Convertor
Comment=Enterprise document conversion tool
Exec=python3 /opt/quick-document-convertor/universal_document_converter.py %F
Icon=quick-document-convertor
Terminal=false
Type=Application
Categories=Office;Utility;
MimeType=application/pdf;application/vnd.openxmlformats-officedocument.wordprocessingml.document;text/plain;text/html;
StartupNotify=true
EOF

# Update desktop database
update-desktop-database ~/.local/share/applications

# Create MIME type associations
mkdir -p ~/.local/share/mime/packages
cat > ~/.local/share/mime/packages/quick-document-convertor.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="application/x-quick-document-convertor">
        <comment>Quick Document Convertor Project</comment>
        <glob pattern="*.qdc"/>
    </mime-type>
</mime-info>
EOF

# Update MIME database
update-mime-database ~/.local/share/mime
```

## 🚀 Usage

### Launching the Application

#### From Applications Menu
1. Open your applications menu (Activities, Application Launcher, etc.)
2. Search for "Quick Document Convertor"
3. Click the application icon

#### From Command Line
```bash
# If installed via package
quick-document-convertor

# If installed from source
python3 /path/to/quick_doc_convertor/universal_document_converter.py

# If using AppImage
./QuickDocumentConvertor-3.1.0-x86_64.AppImage
```

#### From File Manager
1. Right-click on a supported document file
2. Select "Open with Quick Document Convertor"
3. Or choose "Convert with Quick Document Convertor" from context menu

### File Associations
The application can open these file types directly:
- **PDF documents** (.pdf)
- **Microsoft Word** (.docx, .doc)
- **Plain text** (.txt)
- **HTML files** (.html, .htm)
- **Rich Text Format** (.rtf)
- **EPUB e-books** (.epub)
- **OpenDocument Text** (.odt)
- **CSV files** (.csv)

## 🔍 Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check Python version
python3 --version

# Check if tkinter is installed
python3 -c "import tkinter; print('Tkinter is available')"

# Install missing dependencies
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora/CentOS
```

#### Desktop Integration Issues
```bash
# Check if desktop file exists
ls ~/.local/share/applications/quick-document-convertor.desktop

# Verify desktop file is valid
desktop-file-validate ~/.local/share/applications/quick-document-convertor.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications
```

#### Permission Issues
```bash
# Fix permissions for user directories
chmod -R u+w ~/.local/share/applications
chmod -R u+w ~/.local/share/mime
chmod -R u+w ~/.config/quick-document-convertor
```

#### Missing Dependencies
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip python3-tk python3-dev

# CentOS/RHEL
sudo yum install python3-pip python3-tkinter python3-devel

# Fedora
sudo dnf install python3-pip python3-tkinter python3-devel

# Arch Linux
sudo pacman -S python-pip tk
```

### Log Files
Check log files for detailed error information:
```bash
# Application logs
tail -f ~/.local/share/quick-document-convertor/logs/app.log

# System logs
journalctl -u quick-document-convertor
```

## 🔄 Updating

### Package Update
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get upgrade quick-document-convertor

# CentOS/RHEL/Fedora
sudo dnf update quick-document-convertor
```

### Source Update
```bash
cd quick_doc_convertor
git pull origin main
pip3 install -r requirements.txt --upgrade
python3 setup_shortcuts.py
```

### AppImage Update
```bash
# Download new version
wget https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/QuickDocumentConvertor-3.1.0-x86_64.AppImage

# Replace old version
chmod +x QuickDocumentConvertor-3.1.0-x86_64.AppImage
sudo mv QuickDocumentConvertor-3.1.0-x86_64.AppImage /usr/local/bin/quick-document-convertor
```

## 🗑️ Uninstallation

### Package Removal
```bash
# Ubuntu/Debian
sudo apt-get remove quick-document-convertor
sudo apt-get purge quick-document-convertor  # Remove config files too

# CentOS/RHEL/Fedora
sudo rpm -e quick-document-convertor
```

### Manual Removal
```bash
# Remove application files
sudo rm -rf /opt/quick-document-convertor

# Remove desktop integration
rm ~/.local/share/applications/quick-document-convertor.desktop
rm ~/.local/share/mime/packages/quick-document-convertor.xml
rm -rf ~/.local/share/icons/hicolor/*/apps/quick-document-convertor.*

# Remove user data (optional)
rm -rf ~/.config/quick-document-convertor
rm -rf ~/.local/share/quick-document-convertor
rm -rf ~/.cache/quick-document-convertor

# Update databases
update-desktop-database ~/.local/share/applications
update-mime-database ~/.local/share/mime
```

## 📞 Support

### Getting Help
- **GitHub Issues**: https://github.com/Beaulewis1977/quick_ocr_doc_converter/issues
- **Documentation**: https://github.com/Beaulewis1977/quick_ocr_doc_converter/docs
- **Email**: blewisxx@gmail.com

### Reporting Bugs
When reporting issues, please include:
- Linux distribution and version
- Python version (`python3 --version`)
- Desktop environment (GNOME, KDE, etc.)
- Error messages or log files
- Steps to reproduce the issue

### Contributing
See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines.
