# Document to Markdown Converter

A simple, user-friendly desktop application for converting documents (DOCX, PDF, TXT) to Markdown format with batch processing capabilities.

## 🚀 Quick Start

### Option 1: Simple Launch (Recommended)
1. **Double-click** `run_converter.bat` 
2. The GUI will open automatically

### Option 2: PowerShell Launch
1. **Right-click** `run_converter.ps1` → "Run with PowerShell"
2. The GUI will open with better error handling

### Option 3: Python Direct
```bash
python document_converter_gui.py
```

## 📦 Installation & Setup

### First Time Setup
1. **Run the installer** (optional but recommended):
   ```bash
   python install_converter.py
   ```
   This will:
   - Install all required dependencies
   - Create desktop shortcuts (Windows)
   - Set up the application properly

### Manual Setup
If you prefer manual setup:
```bash
pip install python-docx PyPDF2 tkinterdnd2
```

## 🎯 Features

### ✅ What It Does
- **Converts**: DOCX, PDF, and TXT files to Markdown (.md)
- **Batch Processing**: Convert entire directories at once
- **Folder Structure**: Preserves original folder organization
- **Drag & Drop**: Simply drag folders onto the app window
- **Progress Tracking**: Real-time conversion progress
- **Error Handling**: Detailed error reporting and recovery
- **Smart Filtering**: Automatically skips temporary files (like ~$files.docx)

### 📁 Supported Formats
| Input Format | Output | Notes |
|-------------|--------|-------|
| `.docx` | `.md` | Full document structure preserved |
| `.pdf` | `.md` | Text extraction with basic formatting |
| `.txt` | `.md` | Smart encoding detection (UTF-8, Latin-1, etc.) |

## 💻 How to Use

### Method 1: Browse for Folders
1. **Launch the app** using any of the methods above
2. **Click "Browse"** next to "Source Folder" 
3. **Select the folder** containing your documents
4. **Click "Browse"** next to "Output Folder" (or use the default)
5. **Click "Convert Documents"**
6. **Watch the progress** and review results

### Method 2: Drag & Drop (If supported)
1. **Launch the app**
2. **Drag your document folder** directly onto the app window
3. **Adjust output folder** if needed
4. **Click "Convert Documents"**

### Options Available
- ☑️ **Preserve folder structure**: Maintains your original organization
- ☐ **Overwrite existing files**: Replace files that already exist

## 📊 Example Results

```
Found 89 files to convert:

✅ Constitutional Amendments 21_250424_214250.docx
✅ Medicare for All_ A Comprehensive Single-Payer Healthcare System.pdf
✅ Policy Areas for White Papers.txt
⏭️  Skipped (exists): already_converted_file.md
❌ ~$temporary_file.docx: File is not a zip file

🎉 Conversion complete!
✅ Successful: 84
❌ Failed: 5
📁 Output saved to: C:\Users\YourName\Desktop\markdown_output
```

## 🛠️ Technical Details

### Files in This Package
- **`document_converter_gui.py`** - Main GUI application
- **`run_converter.bat`** - Simple Windows launcher
- **`run_converter.ps1`** - PowerShell launcher with error handling
- **`install_converter.py`** - One-time setup installer
- **`convert_recursive.py`** - Command-line version (backup)

### Dependencies
- **Python 3.6+** (already installed on your system)
- **python-docx** - For DOCX file processing
- **PyPDF2** - For PDF text extraction  
- **tkinterdnd2** - For drag & drop functionality (optional)

### Default Output Location
- **Windows**: `C:\Users\[YourName]\Desktop\markdown_output`
- **Custom**: You can choose any folder you want

## 🔧 Advanced Usage

### Command Line Version
If you prefer command line:
```bash
python convert_recursive.py "C:\path\to\documents" -o "C:\path\to\output"
```

### Batch Automation
Create your own batch script:
```batch
@echo off
python convert_recursive.py "C:\MyDocuments" -o "C:\MyMarkdownFiles"
echo Conversion complete!
pause
```

## ❓ Troubleshooting

### Common Issues

**"Python not found"**
- Make sure Python is installed and added to PATH
- Try using the installer: `python install_converter.py`

**"Module not found" errors**
- Run: `pip install python-docx PyPDF2 tkinterdnd2`
- Or use the installer: `python install_converter.py`

**Some files failed to convert**
- **Temporary files** (starting with ~$): Normal, these are skipped
- **Encoding errors**: Some text files use special characters
- **Corrupted files**: Some files may be damaged

**Drag & drop not working**
- This feature requires `tkinterdnd2` package
- Use the Browse buttons instead
- Or run: `pip install tkinterdnd2`

### Getting Help
1. **Check the Results area** in the app for detailed error messages
2. **Look for specific error patterns** in the troubleshooting section above
3. **Try the command line version** for more detailed error output

## 🎉 Success Tips

1. **Test with a small folder first** to make sure everything works
2. **Keep original documents** - the converter never modifies source files
3. **Use meaningful output folder names** like "Converted_Markdown_2024"
4. **Check the results summary** to see what succeeded and what failed
5. **For large batches**, be patient - PDF conversion can take time

## 📝 Notes

- **Original files are never modified** - only copies are created
- **Folder structure is preserved** by default
- **Progress is shown in real-time**
- **Results are logged** for your review
- **Works offline** - no internet connection required

Enjoy your new document conversion tool! 🚀 