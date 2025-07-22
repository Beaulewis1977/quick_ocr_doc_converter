# Quick Document Convertor - Installation Guide

## 🚀 Quick Start (Easiest Method)

### For End Users (No Technical Knowledge Required)

1. **Download the project** to your computer
2. **Double-click one of these files**:
   - `run_app.py` - Universal launcher (works on all systems)
   - `Quick Document Convertor.bat` - Windows-only launcher
3. **That's it!** The app will start automatically

### For Desktop Shortcuts & Taskbar Pinning

1. **Double-click** `setup_shortcuts.py`
2. **Follow the prompts** - it will automatically:
   - Install all required Python packages
   - Create desktop shortcut
   - Add to Start Menu (Windows) or Applications menu (Linux/Mac)
3. **Pin to taskbar** (Windows):
   - Right-click the desktop shortcut
   - Select "Pin to taskbar"
4. **Pin to dock** (Mac):
   - Drag the application to your dock

---

## 🔧 Advanced Installation Options

### Option 1: Create Standalone Executable (No Python Required)

**Perfect for distribution to users without Python installed**

1. **Run the executable creator**:
   ```bash
   python create_executable.py
   ```
2. **Wait for compilation** (may take a few minutes)
3. **Find your executable** in the `dist/` folder
4. **Distribute the .exe file** - it works on any Windows computer!

**Benefits:**
- ✅ No Python installation required on target computers
- ✅ Single file distribution
- ✅ Can be pinned to taskbar/start menu
- ✅ Professional deployment

### Option 2: Manual Python Setup

**For developers or advanced users**

1. **Install Python 3.6+** from [python.org](https://python.org)
2. **Install dependencies**:
   ```bash
   pip install python-docx PyPDF2 beautifulsoup4 striprtf ebooklib tkinterdnd2
   ```
3. **Run the application**:
   ```bash
   python universal_document_converter.py
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

# Run application
python universal_document_converter.py
```

### Option 4: Create Windows Installer (Professional)

```bash
# Create a professional Windows installer
setup_windows_installer.bat
```

---

## 📱 Platform-Specific Instructions

### Windows

**Easiest Methods:**
1. Double-click `Quick Document Convertor.bat`
2. Double-click `run_app.py`
3. Run `setup_shortcuts.py` for permanent installation

**File Associations:**
- The app will help you set up EPUB readers
- Use Tools → Setup File Associations for guidance

**Taskbar Pinning:**
- Right-click any shortcut → "Pin to taskbar"

### macOS

**Easiest Methods:**
1. Double-click `run_app.py`
2. Run `setup_shortcuts.py` for Applications menu entry

**Dock Pinning:**
- Drag the application icon to your dock while it's running

### Linux

**Easiest Methods:**
1. Double-click `run_app.py` (if GUI file manager supports it)
2. Run `setup_shortcuts.py` for desktop entry
3. Terminal: `python3 universal_document_converter.py`

**Desktop Integration:**
- The setup script creates proper .desktop files
- Applications will appear in your applications menu

---

## 🔍 Troubleshooting

### "Python is not recognized"
- **Solution**: Install Python from [python.org](https://python.org)
- **Windows**: Make sure to check "Add Python to PATH" during installation

### "No module named 'tkinter'"
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **CentOS/RHEL**: `sudo yum install tkinter`
- **macOS**: Usually included with Python

### "Permission denied" (Linux/Mac)
```bash
chmod +x run_app.py
chmod +x setup_shortcuts.py
```

### Missing Dependencies
- **Automatic**: Run `setup_shortcuts.py` - it installs everything
- **Manual**: `pip install python-docx PyPDF2 beautifulsoup4 striprtf ebooklib`

### EPUB Files Won't Open
- **Install an EPUB reader**: Calibre (recommended), Adobe Digital Editions
- **Use the built-in help**: Tools → Setup File Associations

---

## 📦 Distribution Options

### For Personal Use
- Use `Quick Document Convertor.bat` or `run_app.py`
- Run `setup_shortcuts.py` once for permanent installation

### For Team/Organization Distribution
1. **Create executable**: Run `create_executable.py`
2. **Distribute the .exe file** from the `dist/` folder
3. **No Python required** on target computers

### For Developers
- Clone the repository
- Set up virtual environment
- Install in development mode

---

## 🎯 Quick Reference

| Method | Best For | Requirements |
|--------|----------|--------------|
| `run_app.py` | Everyone | Python installed |
| `Quick Document Convertor.bat` | Windows users | Python installed |
| `setup_shortcuts.py` | Permanent installation | Python installed |
| `create_executable.py` | Distribution | PyInstaller |
| Manual Python | Developers | Python + packages |

---

## 💡 Tips

- **First time users**: Start with `run_app.py`
- **Want desktop shortcut**: Use `setup_shortcuts.py`
- **Distributing to others**: Use `create_executable.py`
- **Development**: Use virtual environment setup
- **Having issues**: Check the troubleshooting section above

The application is designed to be as easy as possible to run - just double-click and go!
