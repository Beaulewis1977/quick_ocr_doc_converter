# Windows Installation Guide - Updated with Fixes

## System Requirements

- Windows 10/11 (64-bit)
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space
- Internet connection (for cloud OCR features)

## Prerequisites

### 1. Python 3.8+ (For Development)
If building from source, install Python from https://python.org

### 2. Tesseract OCR (Required)
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
- During installation, select "Add to PATH"
- Note the installation directory (usually `C:\Program Files\Tesseract-OCR`)

### 3. Visual C++ Redistributables
Download if you encounter DLL errors: https://aka.ms/vs/17/release/vc_redist.x64.exe

## Installation Methods

### Method 1: Pre-built Executable (Recommended for Users)

1. Download `QuickDocumentConvertor_v3.0.0_Windows.zip`
2. Extract to desired location (e.g., `C:\Program Files\QuickDocumentConvertor`)
3. Run `QuickDocumentConvertor.exe`
4. Windows Defender may show a warning - click "More info" then "Run anyway"

### Method 2: Install from Source (For Developers)

1. **Clone the repository:**
   ```cmd
   git clone https://github.com/yourusername/enhanced-ocr-converter.git
   cd enhanced-ocr-converter
   ```

2. **Create virtual environment:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements_windows.txt
   ```

4. **Run the application:**
   ```cmd
   python enhanced_ocr_gui.py
   ```

### Method 3: Build Your Own Executable

1. **Install build dependencies:**
   ```cmd
   pip install -r requirements_windows.txt
   pip install pyinstaller==6.12.0
   ```

2. **Run the build script:**
   ```cmd
   python build_windows_executable_updated.py
   ```

3. **Find executable in:**
   ```
   dist\QuickDocumentConvertor.exe
   ```

## API Key Configuration

### Setting Up API Keys in the GUI

1. Launch the application
2. Click on the **Settings** tab
3. Configure your preferred OCR backends:

#### Free Local OCR (No API Key Required)
- Tesseract OCR works out of the box
- No configuration needed

#### Google Vision API
1. Create a Google Cloud project
2. Enable Vision API
3. Create service account and download JSON key
4. In the app, browse to select the JSON file

#### AWS Textract
1. Create AWS account
2. Get Access Key ID and Secret Access Key
3. Enter credentials in the app:
   - Access Key ID
   - Secret Access Key  
   - Region (e.g., us-east-1)

#### Azure Computer Vision
1. Create Azure account
2. Deploy Computer Vision resource
3. Enter in the app:
   - Subscription Key
   - Endpoint URL

4. Click **"Save Configuration"**
5. Click **"Test Backends"** to verify

### Using Environment Variables (Alternative)

Set these in System Properties > Environment Variables:

```cmd
# Google Vision
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\credentials.json

# AWS Textract
set AWS_ACCESS_KEY_ID=your-access-key
set AWS_SECRET_ACCESS_KEY=your-secret-key
set AWS_DEFAULT_REGION=us-east-1

# Azure
set AZURE_COGNITIVE_SERVICES_KEY=your-key
set AZURE_COGNITIVE_SERVICES_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
```

## Troubleshooting

### OCR Not Working

1. **Verify Tesseract Installation:**
   ```cmd
   tesseract --version
   ```
   Should show version 5.x.x

2. **Check Tesseract Path:**
   - Add `C:\Program Files\Tesseract-OCR` to PATH
   - Restart the application

3. **Missing Language Data:**
   - Check `C:\Program Files\Tesseract-OCR\tessdata` contains `.traineddata` files
   - Download additional languages if needed

### Application Won't Start

1. **Install Visual C++ Redistributables:**
   - Download from Microsoft
   - Install both x64 and x86 versions

2. **Run as Administrator:**
   - Right-click exe > Run as administrator

3. **Check Windows Defender:**
   - Add exception for the application folder

### API Keys Not Working

1. **Verify Credentials:**
   - Test credentials using provider's console
   - Check for typos or extra spaces

2. **Network Issues:**
   - Check firewall settings
   - Verify internet connection
   - Check proxy settings if applicable

### Performance Issues

1. **For Large Files:**
   - Use local Tesseract for better performance
   - Consider batch processing

2. **Memory Usage:**
   - Close other applications
   - Process smaller batches

## Features

### Available in Windows Version

- ✅ Local OCR with Tesseract
- ✅ Cloud OCR (Google, AWS, Azure)
- ✅ Secure API key management
- ✅ Cost tracking and optimization
- ✅ Batch processing
- ✅ Multiple output formats (JSON, DOCX, Markdown)
- ✅ Drag-and-drop interface
- ✅ Real-time progress tracking
- ✅ System tray integration

### Keyboard Shortcuts

- `Ctrl+O` - Open files
- `Ctrl+S` - Save results
- `Ctrl+Q` - Quit application
- `F1` - Help
- `F5` - Refresh backends

## Security Notes

1. **API Keys are encrypted** using Fernet encryption
2. **Stored in:** `%USERPROFILE%\.ocr_secure\`
3. **Never share** your credential files
4. **Use environment variables** for shared computers

## Performance Tips

1. **Local Processing:**
   - Use Tesseract for privacy and unlimited usage
   - No internet required

2. **Cloud Processing:**
   - Better accuracy for complex documents
   - Costs money but includes advanced features

3. **Optimization:**
   - Enable caching for repeated documents
   - Use appropriate image resolution (300 DPI recommended)

## Uninstallation

### For Executable Version:
1. Delete the application folder
2. Remove `%USERPROFILE%\.ocr_secure\` (contains encrypted credentials)
3. Remove from PATH if added

### For Source Installation:
```cmd
deactivate
rmdir /s venv
```

## Support

- **Documentation:** See README.md
- **Issues:** GitHub Issues page
- **Email:** support@terragonlabs.com

## Version History

- **v3.0.0** (Current)
  - Fixed numpy compatibility issues
  - Updated to opencv-python-headless for better compatibility
  - Enhanced credential security
  - Improved error handling

- **v2.0.0**
  - Added cloud OCR support
  - Implemented cost tracking

- **v1.0.0**
  - Initial release with Tesseract support