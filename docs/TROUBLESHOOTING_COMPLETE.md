# Universal Document Converter - Complete Troubleshooting Guide

This comprehensive guide covers all known issues and their solutions for Universal Document Converter v2.1.0.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Launch and Startup Problems](#launch-and-startup-problems)
3. [Conversion Errors](#conversion-errors)
4. [OCR Problems](#ocr-problems)
5. [Performance Issues](#performance-issues)
6. [VFP9/VB6 Integration Issues](#vfp9vb6-integration-issues)
7. [GUI Problems](#gui-problems)
8. [CLI Issues](#cli-issues)
9. [File Format Issues](#file-format-issues)
10. [System-Specific Problems](#system-specific-problems)
11. [Error Messages Reference](#error-messages-reference)
12. [Advanced Diagnostics](#advanced-diagnostics)

## Installation Issues

### Windows Installation Problems

#### "Windows protected your PC" Warning
**Problem**: Windows Defender SmartScreen blocks the installer
**Solution**:
1. Click "More info" on the warning dialog
2. Click "Run anyway"
3. Or disable SmartScreen temporarily:
   - Windows Settings → Security → Windows Security
   - App & browser control → Reputation-based protection
   - Turn off "Check apps and files"

#### "Python not found" Error
**Problem**: Python is not installed or not in PATH
**Solution**:
1. Download Python from [python.org](https://python.org)
2. During installation, CHECK "Add Python to PATH"
3. Restart command prompt after installation
4. Verify: `python --version`

#### Missing VCRUNTIME140.dll
**Problem**: Visual C++ Redistributable not installed
**Solution**:
1. Download [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Install both x64 and x86 versions
3. Restart computer

#### Installation Path Issues
**Problem**: Special characters or spaces in path
**Solution**:
1. Install to path without spaces: `C:\UniversalConverter`
2. Avoid special characters in path
3. Use short path names if needed: `dir /x`

### macOS Installation Problems

#### "Cannot be opened because it is from an unidentified developer"
**Problem**: Gatekeeper blocks unsigned apps
**Solution**:
```bash
# Method 1: Right-click approach
1. Right-click the app
2. Select "Open"
3. Click "Open" in the dialog

# Method 2: Terminal approach
xattr -d com.apple.quarantine /Applications/UniversalDocumentConverter.app
```

#### "No module named '_tkinter'"
**Problem**: Tkinter not installed with Python
**Solution**:
```bash
# Homebrew Python
brew reinstall python-tk

# MacPorts
sudo port install py39-tkinter

# From source
brew install tcl-tk
python3 -m pip install --upgrade --force-reinstall tkinter
```

### Linux Installation Problems

#### Permission Denied Errors
**Problem**: No execute permissions
**Solution**:
```bash
# Make scripts executable
chmod +x run_converter.sh
chmod +x universal_document_converter_ocr.py

# Fix ownership
sudo chown -R $USER:$USER /opt/UniversalConverter
```

#### Missing Dependencies
**Problem**: Required system libraries not installed
**Solution**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-tk python3-dev
sudo apt install tesseract-ocr libtesseract-dev
sudo apt install libpoppler-cpp-dev

# Fedora/RHEL
sudo dnf install python3-pip python3-tkinter python3-devel
sudo dnf install tesseract tesseract-devel
sudo dnf install poppler-cpp-devel

# Arch
sudo pacman -S python-pip tk tesseract poppler
```

## Launch and Startup Problems

### Application Won't Start

#### Black Screen or Immediate Close
**Problem**: Application crashes on startup
**Diagnosis**:
```bash
# Run with debug output
python universal_document_converter_ocr.py --debug

# Check for errors
python -c "from universal_document_converter_ocr import *"
```

**Solutions**:
1. Check Python version: `python --version` (need 3.8+)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Clear cache: Delete `%APPDATA%\UniversalConverter\cache`
4. Run in safe mode: `python universal_document_converter_ocr.py --safe-mode`

#### "No GUI" Error
**Problem**: Tkinter not available
**Solution**:
```bash
# Test Tkinter
python -m tkinter

# Windows: Reinstall Python with tcl/tk
# macOS: brew install python-tk
# Linux: sudo apt install python3-tk
```

### Slow Startup

**Problem**: Application takes long to start
**Solutions**:
1. Disable antivirus scanning temporarily
2. Clear font cache: `fc-cache -f -v` (Linux/macOS)
3. Reduce startup modules:
   ```json
   {
     "startup": {
       "load_ocr": false,
       "check_updates": false,
       "preload_formats": false
     }
   }
   ```

## Conversion Errors

### "Unsupported Format" Error

**Problem**: File format not recognized
**Diagnosis**:
```bash
python universal_document_converter_ocr.py --check-format mysterious_file
```

**Solutions**:
1. Check file extension is correct
2. Verify file is not corrupted: `file mysterious_file` (Linux/macOS)
3. Force format detection: `--input-format auto`
4. Try renaming with correct extension

### "Conversion Failed" Generic Error

**Problem**: Conversion process fails
**Diagnosis**:
```bash
# Run with verbose output
python universal_document_converter_ocr.py input.pdf output.docx --verbose --log debug.log

# Check log file
cat debug.log | grep ERROR
```

**Common Causes**:
1. **Corrupted input file**: Try opening in original application
2. **Insufficient permissions**: Check file/folder permissions
3. **Disk space**: Ensure enough free space (3x file size)
4. **Memory issues**: Close other applications

### PDF Conversion Issues

#### "PDF is encrypted"
**Solution**:
```bash
# Provide password
python universal_document_converter_ocr.py encrypted.pdf output.docx --password "mypass"

# Remove encryption first
python universal_document_converter_ocr.py encrypted.pdf decrypted.pdf --decrypt --password "mypass"
```

#### "Invalid PDF structure"
**Solution**:
```bash
# Try PDF repair
python universal_document_converter_ocr.py broken.pdf fixed.pdf --repair-pdf

# Use alternative parser
python universal_document_converter_ocr.py broken.pdf output.docx --pdf-parser pdfplumber
```

### Word Document Issues

#### "Cannot open .doc files"
**Problem**: Legacy .doc format
**Solution**:
1. Convert to .docx first using LibreOffice:
   ```bash
   libreoffice --headless --convert-to docx file.doc
   ```
2. Use compatibility mode: `--compatibility legacy`

#### "Corrupted DOCX"
**Solution**:
```bash
# Try recovery mode
python universal_document_converter_ocr.py corrupted.docx output.pdf --recover

# Extract text only
python universal_document_converter_ocr.py corrupted.docx output.txt --extract-text
```

## OCR Problems

### OCR Not Working

#### "Tesseract not found"
**Problem**: Tesseract OCR not installed
**Solution**:

**Windows**:
1. Download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Add to PATH: `C:\Program Files\Tesseract-OCR`
3. Verify: `tesseract --version`

**macOS**:
```bash
brew install tesseract
brew install tesseract-lang  # For additional languages
```

**Linux**:
```bash
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-eng  # English
sudo apt install tesseract-ocr-all  # All languages
```

#### "OCR produced no output"
**Problem**: Image quality too poor
**Solution**:
```bash
# Enable preprocessing
python universal_document_converter_ocr.py scan.pdf text.txt --ocr --preprocess

# Increase DPI
python universal_document_converter_ocr.py scan.pdf text.txt --ocr --ocr-dpi 600

# Try different engine
python universal_document_converter_ocr.py scan.pdf text.txt --ocr --ocr-engine easyocr
```

### OCR Quality Issues

#### Poor Recognition Accuracy
**Solutions**:
1. **Preprocessing**:
   ```bash
   --ocr --preprocess --deskew --denoise --enhance-contrast
   ```

2. **Language specification**:
   ```bash
   --ocr-lang eng+fra+deu  # Multiple languages
   ```

3. **Engine selection**:
   - Tesseract: Better for printed text
   - EasyOCR: Better for handwriting

4. **Custom configuration**:
   ```bash
   --ocr --ocr-config "{'tesseract_config': '--psm 6 --oem 1'}"
   ```

### OCR Performance Issues

#### OCR Too Slow
**Solutions**:
1. Reduce image size: `--ocr --max-image-size 2000`
2. Use GPU acceleration: `--ocr --ocr-engine easyocr --gpu`
3. Limit pages: `--pages 1-10`
4. Lower quality: `--ocr --ocr-dpi 150`

## Performance Issues

### Slow Conversions

#### General Performance Tips
1. **Use parallel processing**:
   ```bash
   --batch --parallel 4
   ```

2. **Optimize settings**:
   ```json
   {
     "performance": {
       "chunk_size_mb": 50,
       "cache_enabled": true,
       "lazy_loading": true
     }
   }
   ```

3. **Reduce quality for speed**:
   ```bash
   --quality low --no-images --no-formatting
   ```

### Memory Issues

#### "Out of Memory" Errors
**Solutions**:
1. **Limit memory usage**:
   ```bash
   --max-memory 1024  # Limit to 1GB
   ```

2. **Process in chunks**:
   ```bash
   --chunk-size 10  # 10MB chunks
   ```

3. **Close other applications**

4. **Increase system swap**:
   ```bash
   # Linux
   sudo fallocate -l 4G /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### Disk Space Issues

#### "No space left on device"
**Solutions**:
1. **Change temp directory**:
   ```bash
   --temp-dir /path/with/space
   ```

2. **Clean cache**:
   ```bash
   python universal_document_converter_ocr.py --clean-cache
   ```

3. **Enable compression**:
   ```bash
   --compress --optimize
   ```

## VFP9/VB6 Integration Issues

### DLL Loading Problems

#### "Cannot load UniversalConverter32.dll"
**Solutions**:
1. **Check architecture**: Ensure 32-bit DLL with 32-bit VFP9/VB6
2. **Register DLL**:
   ```cmd
   regsvr32 UniversalConverter32.dll
   ```
3. **Check dependencies**:
   ```cmd
   dumpbin /dependents UniversalConverter32.dll
   ```

#### "Entry point not found"
**Problem**: Function names not exported correctly
**Solution**:
```vb
' Use exact function names
Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    Alias "ConvertDocument" (...)
```

### COM Server Issues

#### "Cannot create object"
**Solutions**:
1. **Register COM server**:
   ```cmd
   python com_server.py --register
   ```

2. **Check registry**:
   ```cmd
   reg query HKCR\UniversalConverter.Application
   ```

3. **Run as administrator** for registration

### IPC Communication Problems

#### JSON IPC Not Working
**Diagnosis**:
```foxpro
*!* Check file creation
IF !FILE("C:\temp\uc_request.json")
    MESSAGEBOX("Request file not created!")
ENDIF
```

**Solutions**:
1. Check permissions on temp directory
2. Verify JSON format is valid
3. Use absolute paths
4. Add delays for file system sync

## GUI Problems

### Display Issues

#### Blurry Text (High DPI)
**Solution**:
1. **Windows**: Right-click exe → Properties → Compatibility → "Override high DPI"
2. **Config setting**:
   ```json
   {
     "ui_settings": {
       "dpi_aware": true,
       "scale_factor": 1.5
     }
   }
   ```

#### Theme Problems
**Solutions**:
```bash
# Force light theme
python universal_document_converter_ocr.py --theme light

# Disable theming
python universal_document_converter_ocr.py --no-theme
```

### Drag and Drop Not Working

**Windows Solutions**:
1. Run as administrator
2. Disable UAC temporarily
3. Check tkinterdnd2: `pip install tkinterdnd2`

**macOS Solutions**:
1. Grant accessibility permissions
2. Check Security & Privacy settings

## CLI Issues

### Command Not Found

**Problem**: Script not in PATH
**Solutions**:

**Windows**:
```batch
:: Add to PATH permanently
setx PATH "%PATH%;C:\UniversalConverter"

:: Or use full path
C:\UniversalConverter\universal_document_converter_ocr.py
```

**Unix-like**:
```bash
# Add to PATH
export PATH=$PATH:/opt/UniversalConverter

# Or create alias
alias udc='python /opt/UniversalConverter/universal_document_converter_ocr.py'
```

### Argument Parsing Errors

**Problem**: "Unrecognized arguments"
**Solution**: Use `--` to separate files from options:
```bash
python universal_document_converter_ocr.py -- --strange-filename.pdf output.docx
```

## File Format Issues

### Markdown Conversion Problems

#### "Markdown not rendering correctly"
**Solutions**:
1. Specify flavor: `--markdown-flavor gfm`
2. Enable extensions: `--markdown-extensions extra,codehilite`
3. Check encoding: `--encoding utf-8`

### RTF Issues

#### "RTF file is corrupted"
**Solutions**:
1. Try text extraction: `--extract-text`
2. Use alternative parser: `--rtf-parser striprtf`
3. Convert via HTML: First to HTML, then to target

## System-Specific Problems

### Windows-Specific

#### Long Path Issues
**Problem**: Path longer than 260 characters
**Solution**:
1. Enable long paths in Windows:
   ```powershell
   Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
   ```
2. Use short names: `dir /x`

### macOS-Specific

#### "Operation not permitted"
**Problem**: macOS security restrictions
**Solution**:
1. Grant full disk access: System Preferences → Security & Privacy → Privacy → Full Disk Access
2. Add Terminal/IDE to allowed apps

### Linux-Specific

#### SELinux Denials
**Problem**: SELinux blocking operations
**Solution**:
```bash
# Check denials
sudo ausearch -m avc -ts recent

# Temporary disable
sudo setenforce 0

# Create policy
sudo audit2allow -M myconverter
sudo semodule -i myconverter.pp
```

## Error Messages Reference

### Common Error Codes

| Error | Meaning | Solution |
|-------|---------|----------|
| E001 | File not found | Check file path exists |
| E002 | Permission denied | Check read/write permissions |
| E003 | Unsupported format | Update format handlers |
| E004 | OCR failure | Check OCR installation |
| E005 | Memory error | Increase available memory |
| E006 | Timeout | Increase timeout setting |
| E007 | Network error | Check internet connection |
| E008 | Configuration error | Validate config file |
| E009 | Dependency missing | Install requirements |
| E010 | License error | Check license validity |

## Advanced Diagnostics

### Debug Mode

Enable comprehensive debugging:
```bash
# Maximum verbosity
python universal_document_converter_ocr.py --debug --verbose --log debug.log

# Environment variables
export UC_DEBUG=1
export UC_LOG_LEVEL=DEBUG
```

### System Information

Collect diagnostic information:
```bash
# Built-in diagnostics
python universal_document_converter_ocr.py --diagnose

# Manual collection
python universal_document_converter_ocr.py --version --verbose
python -m pip list | grep -E "(pdf|ocr|doc)"
python -c "import sys; print(sys.path)"
```

### Performance Profiling

```bash
# Profile conversion
python -m cProfile -o profile.stats universal_document_converter_ocr.py input.pdf output.docx

# Analyze results
python -m pstats profile.stats
```

### Creating Bug Reports

When reporting issues, include:
1. **System info**: OS, Python version, package versions
2. **Error messages**: Complete error output
3. **Debug log**: Run with `--debug --log debug.log`
4. **Sample file**: If possible, provide problematic file
5. **Steps to reproduce**: Exact commands used

**Report template**:
```markdown
**System Information**
- OS: Windows 10 Pro 22H2
- Python: 3.11.5
- Converter Version: 2.1.0

**Error Description**
[What went wrong]

**Steps to Reproduce**
1. Run command: `python universal_document_converter_ocr.py...`
2. Error occurs at...

**Error Output**
```
[Paste error here]
```

**Debug Log**
[Attach debug.log]
```

---

**Still having issues?** 
- Check [GitHub Issues](https://github.com/Beaulewis1977/quick_ocr_doc_converter/issues)
- Join [Discussions](https://github.com/Beaulewis1977/quick_ocr_doc_converter/discussions)
- Email support: support@beaulewis.com