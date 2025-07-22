# Cross-Platform Integration Guide

## Quick Document Convertor - Linux & macOS Optimization

This guide covers the comprehensive cross-platform features implemented in the Quick Document Convertor, providing native integration for Windows, Linux, and macOS platforms.

## 🌍 Platform Support

### Supported Platforms
- **Windows** 10/11 (Enhanced support)
- **Linux** (Ubuntu, Debian, CentOS, RHEL, Arch)
- **macOS** 10.13+ (High Sierra and later)

### Platform Detection
The application automatically detects the current platform and provides appropriate functionality:

```python
import cross_platform

platform = cross_platform.get_platform()  # 'windows', 'linux', 'macos'
is_supported = cross_platform.is_supported_platform()
platform_info = cross_platform.get_platform_info()
```

## 🐧 Linux Integration

### Desktop Integration
- **XDG-compliant .desktop files** for applications menu
- **MIME type registration** for file associations
- **File manager integration** (Nautilus, Dolphin, etc.)
- **Icon installation** with multiple sizes
- **System tray support** (where available)

### Package Formats
- **.deb packages** for Debian/Ubuntu systems
- **.rpm packages** for Red Hat/CentOS/Fedora
- **AppImage** for universal distribution
- **Tarball archives** as fallback

### File Associations
Supports opening these formats directly:
- PDF documents
- Microsoft Word documents (.docx)
- Plain text files (.txt)
- HTML files
- Rich Text Format (.rtf)
- EPUB e-books
- OpenDocument Text (.odt)
- CSV files

### Installation Locations
- **Application**: `/opt/quick-document-convertor/`
- **Desktop file**: `~/.local/share/applications/`
- **Icons**: `~/.local/share/icons/hicolor/`
- **MIME types**: `~/.local/share/mime/`
- **Configuration**: `~/.config/quick-document-convertor/`
- **Data**: `~/.local/share/quick-document-convertor/`
- **Cache**: `~/.cache/quick-document-convertor/`

## 🍎 macOS Integration

### App Bundle Creation
- **Native .app bundles** using py2app or PyInstaller
- **Info.plist configuration** with file associations
- **UTI (Uniform Type Identifier)** registration
- **Dock and Finder integration**
- **Spotlight search support**

### Package Formats
- **.app bundles** for direct installation
- **.dmg installers** with professional layout
- **.pkg installers** for enterprise deployment

### File Associations
Uses UTI system for native file associations:
- `com.adobe.pdf` (PDF documents)
- `org.openxmlformats.wordprocessingml.document` (Word documents)
- `public.plain-text` (Text files)
- `public.html` (HTML files)
- `public.rtf` (Rich Text Format)
- `org.idpf.epub-container` (EPUB e-books)
- `org.oasis-open.opendocument.text` (OpenDocument)
- `public.comma-separated-values-text` (CSV files)

### Installation Locations
- **Application**: `/Applications/Quick Document Convertor.app`
- **Configuration**: `~/Library/Application Support/Quick Document Convertor/`
- **Logs**: `~/Library/Logs/Quick Document Convertor/`
- **Cache**: `~/Library/Caches/Quick Document Convertor/`

## 🖥️ Enhanced Windows Integration

### Improved Features
- **Enhanced shortcuts** with proper file associations
- **Registry integration** for file types
- **Context menu entries** ("Convert with Quick Document Convertor")
- **Programs and Features** listing
- **Uninstaller creation**
- **Start Menu and Desktop shortcuts**

### Package Formats
- **PyInstaller executables** (single file or directory)
- **NSIS installers** with professional UI
- **MSI packages** using WiX Toolset

## 🔧 Building Packages

### Universal Build Script
Use the `build_all_platforms.py` script to create packages for all platforms:

```bash
# Build for current platform
python build_all_platforms.py

# Build for specific platform
python build_all_platforms.py --platform linux

# Build with custom options
python build_all_platforms.py --platform all --version 2.1.0 --icon app_icon.ico --install-deps
```

### Platform-Specific Building

#### Linux Package Building
```python
from packaging.build_linux import build_all_linux_packages

app_dir = Path("./")
output_dir = Path("./dist")
packages = build_all_linux_packages(app_dir, output_dir, "2.0.0")
```

#### macOS Package Building
```python
from packaging.build_macos import build_all_macos_packages

script_path = Path("./universal_document_converter.py")
output_dir = Path("./dist")
packages = build_all_macos_packages(script_path, output_dir, "2.0.0")
```

#### Windows Package Building
```python
from packaging.build_windows import build_all_windows_packages

script_path = Path("./universal_document_converter.py")
output_dir = Path("./dist")
packages = build_all_windows_packages(script_path, output_dir, "2.0.0")
```

## 📦 Dependencies

### Core Dependencies
- **PyInstaller** >= 5.0 (cross-platform packaging)
- **Pillow** >= 9.0 (image processing for icons)

### Platform-Specific Dependencies

#### Linux
- **python-dbus** (desktop integration)
- **update-desktop-database** (desktop file registration)
- **update-mime-database** (MIME type registration)
- **dpkg-dev** (for .deb packages)
- **rpm-build** (for .rpm packages)

#### macOS
- **py2app** >= 0.28 (app bundle creation)
- **hdiutil** (DMG creation)
- **pkgbuild** (PKG installer creation)

#### Windows
- **pywin32** (Windows API access)
- **NSIS** (installer creation)
- **WiX Toolset** (MSI creation)

## 🧪 Testing

### Running Cross-Platform Tests
```bash
# Run all cross-platform tests
python test_cross_platform.py

# Run with pytest for detailed output
python -m pytest test_cross_platform.py -v
```

### Test Coverage
- Platform detection and directory handling
- File format support and associations
- Package creation and validation
- Desktop integration functionality
- Cross-platform compatibility

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Install base dependencies
pip install -r requirements.txt

# Install platform-specific dependencies (automatic)
python build_all_platforms.py --install-deps
```

### 2. Set Up Desktop Integration
```bash
# Enhanced setup with cross-platform support
python setup_shortcuts.py
```

### 3. Build Packages
```bash
# Build for all platforms
python build_all_platforms.py --platform all --install-deps

# Build for current platform only
python build_all_platforms.py
```

### 4. Test Installation
```bash
# Test cross-platform functionality
python test_cross_platform.py

# Test the application
python universal_document_converter.py
```

## 📋 Configuration

### Platform-Specific Paths
The application automatically uses appropriate directories for each platform:

```python
import cross_platform

config_dir = cross_platform.get_config_dir()
data_dir = cross_platform.get_data_dir()
cache_dir = cross_platform.get_cache_dir()
log_dir = cross_platform.get_log_dir()
```

### File Format Support
```python
formats = cross_platform.get_supported_file_formats()
# Returns: {'input': [...], 'output': [...]}
```

## 🔍 Troubleshooting

### Common Issues

#### Linux
- **Missing desktop integration tools**: Install `desktop-file-utils`
- **MIME type issues**: Run `update-mime-database ~/.local/share/mime`
- **Permission errors**: Ensure user has write access to `~/.local/share/`

#### macOS
- **py2app not found**: Install with `pip install py2app`
- **Code signing issues**: Set up Apple Developer account for distribution
- **Permission errors**: Grant Full Disk Access in System Preferences

#### Windows
- **pywin32 not found**: Install with `pip install pywin32`
- **Registry access denied**: Run as administrator for system-wide installation
- **Antivirus blocking**: Add exception for the application directory

### Debug Mode
Enable verbose output for troubleshooting:
```bash
python build_all_platforms.py --verbose
```

## 📚 API Reference

See the individual module documentation:
- `cross_platform/__init__.py` - Core platform detection
- `cross_platform/linux_integration.py` - Linux-specific features
- `cross_platform/macos_integration.py` - macOS-specific features
- `cross_platform/windows_integration.py` - Windows-specific features
- `packaging/` - Package building modules

## 🤝 Contributing

When adding new platform features:
1. Add tests to `test_cross_platform.py`
2. Update this documentation
3. Ensure backward compatibility
4. Test on target platforms

## 📄 License

This cross-platform integration is part of the Quick Document Convertor project and is licensed under the MIT License.
