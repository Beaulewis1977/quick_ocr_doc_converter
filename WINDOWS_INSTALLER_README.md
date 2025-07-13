# Windows Installer for Quick Document Convertor

## 🚀 **Professional Windows Installation Package**

This installer creates a professional Windows installation package for Quick Document Convertor with full system integration including:

- ✅ **EXE-style installer** with GUI wizard
- ✅ **System tray integration** with quick access
- ✅ **Start Menu shortcuts** and folders
- ✅ **Desktop shortcuts** for easy access
- ✅ **Taskbar pinning support**
- ✅ **File associations** for supported formats
- ✅ **Context menu integration** (right-click to convert)
- ✅ **Add/Remove Programs** entry
- ✅ **Automatic uninstaller**
- ✅ **Auto-start with Windows** (optional)

## 📋 **Prerequisites**

Before creating the installer, ensure you have:

1. **Python 3.6+** installed
2. **Internet connection** for downloading dependencies
3. **Administrator privileges** (for some operations)

## 🛠️ **Quick Setup (Recommended)**

### **Option 1: One-Click Setup**

1. **Double-click** `setup_windows_installer.bat`
2. **Wait for completion** (may take 5-10 minutes)
3. **Run the installer** from the `dist_installer` folder

### **Option 2: Manual Setup**

1. **Install dependencies**:
   ```bash
   pip install -r requirements_installer.txt
   ```

2. **Create icon file**:
   ```bash
   python create_icon.py
   ```

3. **Build installer**:
   ```bash
   python create_windows_installer.py
   ```

## 📦 **What Gets Created**

The installer creation process generates:

```
dist_installer/
├── Quick_Document_Convertor_Setup.exe    # Professional installer
├── Quick Document Convertor.exe          # Main application
├── tray_app.exe                          # System tray application
├── install.bat                           # Fallback batch installer
└── uninstall.bat                         # Uninstaller script
```

## 🎯 **Installation Features**

### **System Integration**
- **Program Files Installation**: Installs to `C:\Program Files\Quick Document Convertor\`
- **Start Menu**: Creates folder with shortcuts and uninstaller
- **Desktop Shortcut**: Quick access from desktop
- **System Tray**: Minimizes to tray with quick actions

### **File Associations**
The installer registers the following file types:
- `.pdf` - PDF documents
- `.docx` - Word documents
- `.txt` - Text files
- `.html` - HTML files
- `.rtf` - Rich Text Format
- `.epub` - eBook files

### **Context Menu Integration**
Right-click any supported file and select:
- **"Convert with Quick Document Convertor"**
- **"Open with Quick Document Convertor"**

## 🖥️ **System Tray Features**

The system tray application provides:

### **Quick Access Menu**
- **Open Main Application** (default action)
- **Quick Convert File...** (file dialog for instant conversion)
- **Settings** (configure tray behavior)
- **About** (application information)
- **Quit** (exit tray application)

### **Tray Settings**
- ☑️ **Start with Windows** (auto-start on boot)
- ☑️ **Show notifications** (conversion status updates)
- ☑️ **Enable quick convert** (right-click file conversion)
- 🎛️ **Default output format** (markdown, txt, html, rtf, epub)

### **Notifications**
- Application startup confirmation
- Conversion completion status
- Error notifications with details

## 📌 **Taskbar Pinning Instructions**

### **Method 1: From Desktop Shortcut**
1. **Right-click** the desktop shortcut
2. **Select** "Pin to taskbar"
3. **Done!** The app is now pinned

### **Method 2: From Start Menu**
1. **Click** Start Menu
2. **Find** "Quick Document Convertor"
3. **Right-click** → "Pin to taskbar"

### **Method 3: From Running Application**
1. **Start** the application
2. **Right-click** the taskbar icon
3. **Select** "Pin to taskbar"

## 🔧 **Advanced Configuration**

### **Registry Entries**
The installer creates registry entries for:
- File associations
- Context menu integration
- Add/Remove Programs listing
- Auto-start configuration

### **Installation Directories**
- **Application**: `C:\Program Files\Quick Document Convertor\`
- **User Data**: `%APPDATA%\Quick Document Convertor\`
- **Logs**: `%LOCALAPPDATA%\Quick Document Convertor\Logs\`
- **Cache**: `%LOCALAPPDATA%\Quick Document Convertor\Cache\`

## 🚨 **Troubleshooting**

### **Common Issues**

#### **"Python not found" Error**
- **Solution**: Install Python from https://python.org
- **Ensure**: Python is added to PATH during installation

#### **"Dependencies failed to install"**
- **Check**: Internet connection
- **Try**: `pip install --upgrade pip`
- **Manual**: Install each package individually

#### **"Administrator privileges required"**
- **Solution**: Right-click installer → "Run as administrator"
- **Alternative**: Use the batch installer instead

#### **"System tray not working"**
- **Check**: `pystray` and `pillow` are installed
- **Install**: `pip install pystray pillow`
- **Restart**: Windows after installation

### **Uninstallation**

#### **Method 1: Control Panel**
1. **Open** Control Panel → Programs
2. **Find** "Quick Document Convertor"
3. **Click** "Uninstall"

#### **Method 2: Start Menu**
1. **Go to** Start Menu → Quick Document Convertor
2. **Click** "Uninstall"

#### **Method 3: Application Folder**
1. **Navigate to** installation folder
2. **Run** `uninstall.exe`

## 🎨 **Customization**

### **Change Icon**
1. **Replace** `icon.ico` with your custom icon
2. **Rebuild** installer with `python create_windows_installer.py`

### **Modify Installer**
1. **Edit** `create_windows_installer.py`
2. **Customize** NSIS script or batch installer
3. **Rebuild** with your changes

### **Tray Configuration**
- **Config file**: `tray_config.json` in application folder
- **Modify** settings programmatically
- **Restart** tray application to apply changes

## 📞 **Support**

For issues or questions:
- **GitHub**: [Repository Issues](https://github.com/Beaulewis1977/quick_doc_convertor/issues)
- **Email**: blewisxx@gmail.com
- **Documentation**: Check the main README.md

## 🏆 **Professional Features**

This installer provides enterprise-grade features:
- **Silent installation** support
- **Group Policy** deployment ready
- **MSI package** creation (with NSIS)
- **Digital signature** support (configure in NSIS)
- **Multi-language** support framework
- **Automatic updates** infrastructure

---

**Created by Beau Lewis** | **Quick Document Convertor v2.0.0** | **© 2024 All Rights Reserved** 