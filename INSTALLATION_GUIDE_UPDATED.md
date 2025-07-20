# Enhanced OCR Document Converter - Complete Installation Guide

## 🚀 Quick Start

### Windows Users
1. Download the latest release: `QuickDocumentConvertor_v3.0.0_Windows.zip`
2. Extract and run `QuickDocumentConvertor.exe`
3. Install Tesseract OCR from [here](https://github.com/UB-Mannheim/tesseract/wiki)

### Linux/Mac Users
```bash
git clone https://github.com/yourusername/enhanced-ocr-converter.git
cd enhanced-ocr-converter
pip install -r requirements.txt
python enhanced_ocr_gui.py
```

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Ubuntu 20.04+, macOS 10.15+
- **RAM**: 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Python**: 3.8+ (for source installation)
- **Display**: 1024x768 minimum resolution

### Additional Requirements
- **Tesseract OCR**: v5.0+ (for local OCR)
- **Internet**: Required for cloud OCR features

## 🔧 Installation Methods

### Method 1: Pre-built Executables (Easiest)

#### Windows
1. Download `QuickDocumentConvertor_Windows.zip` from releases
2. Extract to desired location
3. Run `QuickDocumentConvertor.exe`
4. If Windows Defender warns, click "More info" → "Run anyway"

#### Linux (AppImage)
```bash
wget https://github.com/.../QuickDocumentConvertor-linux.AppImage
chmod +x QuickDocumentConvertor-linux.AppImage
./QuickDocumentConvertor-linux.AppImage
```

#### macOS
1. Download `QuickDocumentConvertor.dmg`
2. Open DMG and drag to Applications
3. Right-click → Open (first time only)

### Method 2: Install from Source

#### 1. Prerequisites

**All Platforms:**
```bash
# Install Python 3.8+
python --version  # Should show 3.8 or higher
```

**Platform-specific:**

**Windows:**
- Install [Visual C++ Redistributables](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install -y python3-pip python3-tk tesseract-ocr
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender1
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install -y python3-pip python3-tkinter tesseract
sudo dnf install -y mesa-libGL glib2 libSM libXext libXrender
```

**macOS:**
```bash
brew install python@3.11 tesseract
```

#### 2. Clone Repository
```bash
git clone https://github.com/yourusername/enhanced-ocr-converter.git
cd enhanced-ocr-converter
```

#### 3. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies

**Automated Installation:**

**Windows:**
```batch
# Run the batch file
install_dependencies_windows.bat

# Or use PowerShell
powershell -ExecutionPolicy Bypass -File install_dependencies_windows.ps1
```

**Linux/Mac:**
```bash
pip install -r requirements.txt
```

**Manual Installation (if automated fails):**
```bash
# CRITICAL: Install in this order for compatibility
pip install numpy==1.26.4  # Must be <2.0
pip install opencv-python-headless==4.8.1.78  # Linux/Server
# OR
pip install opencv-python==4.8.1.78  # Windows/Desktop

pip install pytesseract==0.3.13
pip install packaging==25.0
pip install Pillow==10.4.0
pip install cryptography>=41.0.0

# Then install remaining packages
pip install -r requirements.txt
```

#### 5. Run the Application

**With GUI (Desktop):**
```bash
python enhanced_ocr_gui.py
```

**Headless/Server Mode:**
```bash
# Linux - Use virtual display
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
python enhanced_ocr_gui.py
```

**Command Line Only:**
```bash
python cli.py input.pdf -o output.json
```

### Method 3: Docker Installation

```dockerfile
# Dockerfile included in repository
docker build -t ocr-converter .
docker run -p 8080:8080 ocr-converter
```

## 🔑 API Key Configuration

### Using the GUI (Recommended)

1. Launch the application
2. Click **Settings** tab
3. Configure your OCR backends:

#### Free Local OCR (No API Key Required)
- Tesseract works out of the box
- Unlimited usage, no internet required

#### Google Vision API
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create project and enable Vision API
3. Create service account → Download JSON key
4. In app: Browse and select the JSON file

#### AWS Textract
1. Go to [AWS Console](https://aws.amazon.com)
2. Create IAM user with Textract permissions
3. Get Access Key ID and Secret Key
4. In app: Enter credentials and region

#### Azure Computer Vision
1. Go to [Azure Portal](https://portal.azure.com)
2. Create Computer Vision resource
3. Get key and endpoint from Keys and Endpoint page
4. In app: Enter subscription key and endpoint URL

5. Click **"Save Configuration"**
6. Click **"Test Backends"** to verify

### Using Environment Variables

**Windows (Command Prompt):**
```batch
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\credentials.json
set AWS_ACCESS_KEY_ID=your-key-id
set AWS_SECRET_ACCESS_KEY=your-secret-key
set AZURE_COGNITIVE_SERVICES_KEY=your-key
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\credentials.json"
$env:AWS_ACCESS_KEY_ID="your-key-id"
$env:AWS_SECRET_ACCESS_KEY="your-secret-key"
$env:AZURE_COGNITIVE_SERVICES_KEY="your-key"
```

**Linux/Mac:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
export AWS_ACCESS_KEY_ID="your-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AZURE_COGNITIVE_SERVICES_KEY="your-key"
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### "No module named 'cv2'" or OpenCV errors
```bash
# Uninstall and reinstall with correct version
pip uninstall opencv-python opencv-python-headless
pip install opencv-python-headless==4.8.1.78  # For servers
# OR
pip install opencv-python==4.8.1.78  # For desktop
```

#### "numpy.core.multiarray failed to import"
```bash
# Downgrade numpy
pip install numpy==1.26.4
```

#### Tesseract not found
**Windows:**
- Add `C:\Program Files\Tesseract-OCR` to system PATH
- Set environment variable: `set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe`

**Linux:**
```bash
sudo apt install tesseract-ocr
# Or
sudo dnf install tesseract
```

**Mac:**
```bash
brew install tesseract
```

#### GUI not showing on Linux server
```bash
# Install and use Xvfb
sudo apt install xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
python enhanced_ocr_gui.py
```

#### Permission denied errors
**Linux/Mac:**
```bash
chmod +x enhanced_ocr_gui.py
# Run with proper permissions
```

**Windows:**
- Run as Administrator
- Check antivirus exclusions

### Platform-Specific Issues

#### Windows
- **DLL errors**: Install Visual C++ Redistributables
- **Windows Defender**: Add exception for app folder
- **Path too long**: Install closer to drive root

#### Linux
- **No display**: Use Xvfb for headless systems
- **Permission denied**: Check file permissions
- **Missing libraries**: Install system dependencies

#### macOS
- **"Unidentified developer"**: Right-click → Open
- **Camera/Files access**: Grant permissions in System Preferences

## 📊 Performance Optimization

### For Best Performance

1. **Use appropriate backends:**
   - Local files: Use Tesseract (free, fast)
   - Complex documents: Use cloud OCR (costs money)

2. **Optimize images:**
   - 300 DPI recommended
   - Convert to grayscale if color not needed
   - Use PNG for text, JPEG for photos

3. **System settings:**
   - Close unnecessary applications
   - Process in batches for large volumes
   - Enable result caching

## 🔒 Security Notes

- API keys are encrypted using Fernet encryption
- Stored in user-specific secure directory
- Never commit credentials to version control
- Use environment variables for CI/CD

## 📱 Support

- **Documentation**: See README.md
- **Issues**: GitHub Issues page
- **Email**: support@terragonlabs.com
- **Wiki**: Project Wiki for detailed guides

## 🔄 Updating

### From Executable
1. Download new version
2. Replace old executable
3. Keep configuration files

### From Source
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## ✅ Verification

After installation, verify everything works:

```bash
# Test Python environment
python -c "import cv2, pytesseract, numpy; print('All modules loaded!')"

# Test Tesseract
tesseract --version

# Run functionality test
python test_application_functionality.py
```

## 📄 License

This software is provided under the MIT License. See LICENSE file for details.