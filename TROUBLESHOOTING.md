# Quick Document Convertor - Troubleshooting Guide

## Common Issues & Solutions

### PyInstaller Issues (Python 3.13 Compatibility)
**Problem**: `ModuleNotFoundError: No module named 'packaging.requirements'`
**Solution**: Use the portable package instead of executable creation
**Status**: Known PyInstaller/Python 3.13 compatibility issue

### Windows Installation Issues

#### Desktop Shortcuts & Taskbar Pinning
**Windows**:
- **Desktop Shortcut**: Created automatically by installer
- **Start Menu**: Added to "Quick Document Convertor" folder
- **Taskbar Pin**: Right-click running app → "Pin to taskbar"

#### macOS Installation
**macOS**:
- **Applications Folder**: Drag app to `/Applications`
- **Dock**: Drag app to dock or right-click → "Keep in dock"
- **Launchpad**: App appears automatically in Launchpad

#### Linux Installation
**Linux**:
- **Desktop Entry**: Created in `~/.local/share/applications/`
- **Menu**: Appears in applications menu
- **Dock**: Right-click → "Add to favorites"

### Launch Issues

#### "Python not found"
```bash
# Windows
python --version
# If not found, install from https://www.python.org/downloads/

# macOS
python3 --version
# Install via: brew install python3

# Linux
python3 --version
# Install via: sudo apt install python3
```

#### "Permission denied" (macOS/Linux)
```bash
chmod +x run_converter.sh
```

### Cross-Platform Launch Commands

#### Windows
```cmd
.\run_converter.bat
```

#### macOS
```bash
./run_converter.sh
```

#### Linux
```bash
./run_converter.sh
```

### File Association Issues
If documents don't open with the converter:
1. Right-click document → "Open with"
2. Browse to converter executable
3. Check "Always use this app"

### Performance Issues
- **Large files**: Use drag-and-drop instead of file browser
- **Memory**: Close other applications for large documents
- **Speed**: Enable "Fast mode" in settings

### Error Messages
- "File not found": Ensure file exists and isn't open in another program
- "Conversion failed": Check file format support
- "Permission denied": Run as administrator or check file permissions

## Getting Help
- **GitHub Issues**: https://github.com/Beaulewis1977/quick_doc_convertor/issues
- **Documentation**: See README.md for detailed setup
- **Community**: Check discussions tab on GitHub
