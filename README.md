# Quick Document Convertor 🚀

<div align="center">

![Quick Document Convertor](https://img.shields.io/badge/Quick-Document%20Convertor-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.6+-green?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-48%2F48%20Passing-brightgreen?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0%20Enterprise-purple?style=for-the-badge)

**Enterprise-Grade • Cross-Platform • Multi-Threading • System Integration • Professional GUI**

A lightning-fast, enterprise-ready document conversion tool with native desktop integration for Windows, Linux, and macOS. Features advanced cross-platform packaging, file associations, system tray integration, and professional deployment options.

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [📄 Formats](#-supported-formats) • [🛠️ Installation](#️-installation) • [📖 Usage](#-usage) • [🖥️ Windows Installer](#️-windows-installer-new) • [🤝 Contributing](#-contributing)

</div>

---

## 🎯 **What is Quick Document Convertor?**

Quick Document Convertor is a **professional-grade, enterprise-ready document conversion application** that transforms documents between multiple formats with a modern GUI and powerful command-line interface. Built for speed, reliability, and ease of use.

### 🌟 **Why Choose Quick Document Convertor?**

- **🚀 Lightning Fast**: Multi-threaded processing with intelligent caching
- **🎯 Universal Support**: Convert between 6 input and 5 output formats (30 combinations)
- **🖥️ Cross-Platform**: Native integration on Windows, macOS, and Linux
- **🔧 Zero Dependencies**: Works completely offline without external APIs
- **🏢 Enterprise Ready**: Professional logging, configuration management, and deployment
- **🎨 Modern UI**: Clean, responsive interface with drag-and-drop support
- **⚡ System Integration**: Tray app, file associations, and context menus

---

## 🚀 **Quick Start**

### 🖱️ **Easiest Way - Just Double-Click!**

1. **Download/Clone** this repository to your computer
2. **Double-click** one of these files:
   - `run_app.py` - Universal launcher (works on all systems)
   - `Quick Document Convertor.bat` - Windows batch launcher
3. **That's it!** The app will start and install any missing dependencies automatically

### 🖥️ **Create Desktop Shortcuts & Taskbar Pinning**

1. **Double-click** `setup_shortcuts.py`
2. **Follow the prompts** - it will automatically:
   - ✅ Install all required packages
   - ✅ Create desktop shortcut
   - ✅ Add to Start Menu (Windows) or Applications (Linux/Mac)
   - ✅ Set up file associations
3. **Pin to taskbar**: Right-click the desktop shortcut → "Pin to taskbar"

### 📦 **Create Standalone Executable (No Python Required)**

1. **Double-click** `create_executable.py`
2. **Wait for compilation** (creates a single .exe file)
3. **Share the .exe** - works on any Windows computer without Python!

### ⚡ **Manual Launch (Advanced Users)**

```bash
python universal_document_converter.py
```

---

## ✨ **Features**

### 🚀 **Core Conversion Features**
- **📄 Universal Format Support**: Convert between 6 input and 5 output formats (30 combinations)
- **⚡ Lightning Fast**: Multi-threaded processing with intelligent caching
- **🖱️ Drag & Drop**: Intuitive interface with enhanced file/folder drag-and-drop
- **📁 Batch Processing**: Convert entire folders recursively with progress tracking
- **🎯 Smart Detection**: Automatic file format detection with fallback support
- **🔧 Zero APIs**: Works completely offline without external dependencies

### ⚙️ **Enterprise Configuration Management**
- **🛠️ Advanced Settings**: Comprehensive configuration system with GUI settings panel
- **💾 Settings Persistence**: Automatic saving of user preferences and window positions
- **📋 Profile Management**: Multiple configuration profiles for different use cases
- **🔄 Import/Export**: Share configurations between installations
- **⚡ CLI Configuration**: Full command-line configuration support with profiles

### 🏗️ **Performance & Reliability**
- **🚀 Multi-Threading**: 2-4x performance improvement with configurable worker threads
- **🧠 Intelligent Caching**: Prevents redundant conversions of unchanged files
- **📊 Memory Optimization**: 50-80% memory reduction for large files through streaming
- **📈 Real-time Progress**: Visual progress tracking with detailed conversion results
- **🔍 Professional Logging**: Enterprise-grade logging system with file rotation

### 🌍 **Cross-Platform Excellence**
- **🖥️ Native Windows Integration**: Start Menu shortcuts, taskbar pinning, registry file associations
- **🐧 Linux Desktop Integration**: .desktop files, MIME types, applications menu, file manager integration
- **🍎 macOS App Bundle**: Native .app bundles, Dock integration, Finder associations, Spotlight search
- **📦 Universal Packaging**: .deb, .rpm, AppImage, .dmg, .pkg, and .msi installers
- **🔧 Platform Detection**: Automatic platform-specific paths and configurations

### 🎨 **User Experience**
- **🖥️ Modern GUI**: Clean, responsive interface with tabbed settings
- **🔗 Desktop Integration**: Native shortcuts and file associations on all platforms
- **📖 File Opening**: Built-in file opening with default applications
- **🎯 Drag & Drop**: Enhanced file and folder drag-and-drop support
- **🔒 Privacy First**: All processing happens locally on your machine

---

## 📄 **Supported Formats**

| **Input Formats (6)** | **Output Formats (5)** |
|----------------------|------------------------|
| **DOCX** - Microsoft Word Documents | **Markdown** - GitHub-flavored markdown |
| **PDF** - Portable Document Format | **TXT** - Plain text with formatting |
| **TXT** - Plain text files | **HTML** - Clean, semantic HTML |
| **HTML** - Web pages and documents | **RTF** - Rich Text Format |
| **RTF** - Rich Text Format | **EPUB** - Electronic Publication (eBooks) |
| **EPUB** - Electronic Publication (eBooks) | |

**Total Conversion Combinations: 30** *(6 × 5)*

### 📚 **EPUB Support Features**
- **📖 Full EPUB Reading**: Extracts text
