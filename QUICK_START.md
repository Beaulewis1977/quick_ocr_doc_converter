# Quick Document Convertor - Quick Start Guide

## 🚀 Instant Launch Options

### Option 1: Double-Click Launch
- **Windows**: Double-click `run_converter.bat`
- **PowerShell**: Right-click `run_converter.ps1` → "Run with PowerShell"

### Option 2: Command Line
```bash
# From project folder
python universal_document_converter.py

# Or use the launchers
run_converter.bat
run_converter.ps1
```

### Option 3: Install & Run
```bash
# Install dependencies and create shortcuts
python install_converter.py

# Then run from Start Menu or desktop
```

## 📋 First-Time Setup

1. **Install Python** (if not already installed):
   - Download from https://www.python.org/downloads/
   - **Important**: Check "Add Python to PATH" during installation

2. **Install Dependencies**:
   ```bash
   python install_converter.py
   ```

3. **Launch Application**:
   - Double-click `run_converter.bat` (recommended)
   - Or use any method above

## 🔧 Troubleshooting

### Python Not Found
- Install Python 3.6+ from python.org
- Restart your computer after installation
- Verify: `python --version`

### Missing Dependencies
Run: `python install_converter.py`

### Application Won't Start
- Check `TROUBLESHOOTING.md` for detailed solutions
- Verify all files are in the same folder
- Try running from command line to see error messages

## 📁 File Structure
```
quick_doc_convertor/
├── run_converter.bat          # Windows launcher
├── run_converter.ps1          # PowerShell launcher
├── install_converter.py       # Dependency installer
├── universal_document_converter.py  # Main application
├── icon.ico                   # Application icon
└── README.md                  # Full documentation
