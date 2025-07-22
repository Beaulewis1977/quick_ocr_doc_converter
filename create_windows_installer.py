#!/usr/bin/env python3
"""
Quick Document Convertor - Windows Installer Creator
Creates a professional Windows installer with full system integration
"""

import os
import sys
import subprocess
import shutil
import tempfile
import winreg
from pathlib import Path
from typing import Dict, List, Optional
import json

class WindowsInstallerCreator:
    """Creates a professional Windows installer with full system integration"""
    
    def __init__(self):
        self.app_name = "Quick Document Convertor"
        self.app_version = "3.1.0"
        self.publisher = "Beau Lewis"
        self.app_dir = Path(__file__).parent
        self.build_dir = self.app_dir / "build_installer"
        self.dist_dir = self.app_dir / "dist_installer"
        
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if required dependencies are available"""
        deps = {
            'pyinstaller': False,
            'pywin32': False,
            'nsis': False,
            'pillow': False
        }
        
        # Check PyInstaller
        try:
            import PyInstaller
            deps['pyinstaller'] = True
        except ImportError:
            pass
            
        # Check pywin32
        try:
            import win32com.client
            deps['pywin32'] = True
        except ImportError:
            pass
            
        # Check NSIS (for professional installer)
        try:
            result = subprocess.run(['makensis', '/VERSION'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                deps['nsis'] = True
        except FileNotFoundError:
            pass
            
        # Check Pillow (for icon processing)
        try:
            import PIL
            deps['pillow'] = True
        except ImportError:
            pass
            
        return deps
    
    def install_dependencies(self) -> bool:
        """Install missing dependencies"""
        print("📦 Installing required dependencies...")
        
        packages = [
            'pyinstaller>=5.0',
            'pywin32>=304',
            'pillow>=9.0',
            'psutil>=5.9.0'
        ]
        
        try:
            for package in packages:
                print(f"Installing {package}...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package
                ])
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def create_system_tray_version(self) -> Path:
        """Create a system tray version of the application"""
        tray_script = self.build_dir / "tray_app.py"
        
        tray_code = '''#!/usr/bin/env python3
"""
Quick Document Convertor - System Tray Application
"""

import tkinter as tk
from tkinter import messagebox
import threading
import sys
import os
from pathlib import Path
import subprocess

# Add the application directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

class SystemTrayApp:
    """System tray application for Quick Document Convertor"""
    
    def __init__(self):
        self.app_dir = Path(__file__).parent
        self.main_app = self.app_dir / "universal_document_converter.py"
        self.icon = None
        self.running = False
        
    def create_icon(self):
        """Create a simple icon for the system tray"""
        # Create a simple icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw a simple document icon
        draw.rectangle([10, 10, 50, 50], fill='lightblue', outline='blue', width=2)
        draw.text((15, 25), "QDC", fill='black')
        
        return image
    
    def show_main_app(self, icon=None, item=None):
        """Show the main application"""
        try:
            if self.main_app.exists():
                subprocess.Popen([sys.executable, str(self.main_app)])
            else:
                messagebox.showerror("Error", "Main application not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start application: {e}")
    
    def show_about(self, icon=None, item=None):
        """Show about dialog"""
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("About", 
                          "Quick Document Convertor v3.1.0\\n"
                          "Enterprise document conversion tool\\n"
                          "Created by Beau Lewis")
        root.destroy()
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        self.running = False
        if self.icon:
            self.icon.stop()
    
    def run(self):
        """Run the system tray application"""
        if not TRAY_AVAILABLE:
            print("System tray not available. Install pystray and pillow.")
            return
            
        self.running = True
        
        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem("Open Quick Document Convertor", self.show_main_app, default=True),
            pystray.MenuItem("About", self.show_about),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app)
        )
        
        # Create icon
        icon_image = self.create_icon()
        self.icon = pystray.Icon("Quick Document Convertor", icon_image, menu=menu)
        
        # Run the icon
        self.icon.run()

def main():
    """Main entry point"""
    app = SystemTrayApp()
    app.run()

if __name__ == "__main__":
    main()
'''
        
        self.build_dir.mkdir(parents=True, exist_ok=True)
        with open(tray_script, 'w', encoding='utf-8') as f:
            f.write(tray_code)
            
        return tray_script
    
    def create_installer_script(self) -> Path:
        """Create NSIS installer script"""
        nsis_script = self.build_dir / "installer.nsi"
        
        nsis_code = f'''
; Quick Document Convertor Installer
; Created with NSIS

!define APPNAME "Quick Document Convertor"
!define COMPANYNAME "Beau Lewis"
!define DESCRIPTION "Enterprise document conversion tool"
!define VERSIONMAJOR 3
!define VERSIONMINOR 1
!define VERSIONBUILD 0
!define HELPURL "https://github.com/Beaulewis1977/quick_doc_convertor"
!define UPDATEURL "https://github.com/Beaulewis1977/quick_doc_convertor/releases"
!define ABOUTURL "https://github.com/Beaulewis1977/quick_doc_convertor"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${{APPNAME}}"
LicenseData "LICENSE"
Name "${{APPNAME}}"
Icon "icon.ico"
outFile "Quick_Document_Convertor_Setup.exe"

!include LogicLib.nsh

page license
page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${{If}} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740
    quit
${{EndIf}}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    setOutPath $INSTDIR
    
    ; Copy main application files
    file "Quick Document Convertor.exe"
    file "tray_app.exe"
    file /r "universal_document_converter.py"
    file "requirements.txt"
    file "README.md"
    file "LICENSE"
    
    ; Create uninstaller
    writeUninstaller "$INSTDIR\\uninstall.exe"
    
    ; Start Menu shortcuts
    createDirectory "$SMPROGRAMS\\${{APPNAME}}"
    createShortCut "$SMPROGRAMS\\${{APPNAME}}\\${{APPNAME}}.lnk" "$INSTDIR\\Quick Document Convertor.exe" "" "$INSTDIR\\icon.ico"
    createShortCut "$SMPROGRAMS\\${{APPNAME}}\\${{APPNAME}} (System Tray).lnk" "$INSTDIR\\tray_app.exe" "" "$INSTDIR\\icon.ico"
    createShortCut "$SMPROGRAMS\\${{APPNAME}}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    
    ; Desktop shortcut
    createShortCut "$DESKTOP\\${{APPNAME}}.lnk" "$INSTDIR\\Quick Document Convertor.exe" "" "$INSTDIR\\icon.ico"
    
    ; Registry for Add/Remove Programs
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "DisplayName" "${{APPNAME}}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "UninstallString" "$INSTDIR\\uninstall.exe"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "QuietUninstallString" "$INSTDIR\\uninstall.exe /S"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "InstallLocation" "$INSTDIR"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "DisplayIcon" "$INSTDIR\\icon.ico"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "Publisher" "${{COMPANYNAME}}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "HelpLink" "${{HELPURL}}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "URLUpdateInfo" "${{UPDATEURL}}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "URLInfoAbout" "${{ABOUTURL}}"
    writeRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "DisplayVersion" "${{VERSIONMAJOR}}.${{VERSIONMINOR}}.${{VERSIONBUILD}}"
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "VersionMajor" ${{VERSIONMAJOR}}
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "VersionMinor" ${{VERSIONMINOR}}
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "NoModify" 1
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "NoRepair" 1
    writeRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}" "EstimatedSize" ${{INSTALLSIZE}}
    
    ; File associations
    writeRegStr HKCR ".qdc" "" "QuickDocConvertor.Document"
    writeRegStr HKCR "QuickDocConvertor.Document" "" "Quick Document Convertor Project"
    writeRegStr HKCR "QuickDocConvertor.Document\\shell\\open\\command" "" '"$INSTDIR\\Quick Document Convertor.exe" "%1"'
    
    ; Context menu integration
    writeRegStr HKCR "*\\shell\\QuickDocConvertor" "" "Convert with Quick Document Convertor"
    writeRegStr HKCR "*\\shell\\QuickDocConvertor\\command" "" '"$INSTDIR\\Quick Document Convertor.exe" "%1"'
    
    ; Auto-start system tray (optional)
    writeRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Run" "QuickDocConvertor" "$INSTDIR\\tray_app.exe"
    
sectionEnd

section "uninstall"
    ; Remove files
    delete "$INSTDIR\\Quick Document Convertor.exe"
    delete "$INSTDIR\\tray_app.exe"
    delete "$INSTDIR\\universal_document_converter.py"
    delete "$INSTDIR\\requirements.txt"
    delete "$INSTDIR\\README.md"
    delete "$INSTDIR\\LICENSE"
    delete "$INSTDIR\\uninstall.exe"
    rmDir "$INSTDIR"
    
    ; Remove shortcuts
    delete "$SMPROGRAMS\\${{APPNAME}}\\${{APPNAME}}.lnk"
    delete "$SMPROGRAMS\\${{APPNAME}}\\${{APPNAME}} (System Tray).lnk"
    delete "$SMPROGRAMS\\${{APPNAME}}\\Uninstall.lnk"
    rmDir "$SMPROGRAMS\\${{APPNAME}}"
    delete "$DESKTOP\\${{APPNAME}}.lnk"
    
    ; Remove registry entries
    deleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APPNAME}}"
    deleteRegKey HKCR ".qdc"
    deleteRegKey HKCR "QuickDocConvertor.Document"
    deleteRegKey HKCR "*\\shell\\QuickDocConvertor"
    deleteRegValue HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Run" "QuickDocConvertor"
    
sectionEnd
'''
        
        with open(nsis_script, 'w', encoding='utf-8') as f:
            f.write(nsis_code)
            
        return nsis_script
    
    def create_executables(self) -> bool:
        """Create executable files using PyInstaller"""
        print("🔨 Creating executable files...")
        
        # Main application executable
        icon_exists = (self.build_dir / 'icon.ico').exists()
        version_exists = (self.build_dir / 'version_info.txt').exists()
        
        main_spec = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['universal_document_converter.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('requirements.txt', '.'),
        ('README.md', '.'),
        ('LICENSE', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'threading',
        'pathlib',
        'json',
        'concurrent.futures',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Quick Document Convertor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if {icon_exists} else None,
    version='version_info.txt' if {version_exists} else None,
)
'''
        
        # System tray executable
        tray_spec = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['tray_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pystray',
        'PIL',
        'tkinter',
        'subprocess',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='tray_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if {icon_exists} else None,
)
'''
        
        # Write spec files
        main_spec_file = self.build_dir / "main_app.spec"
        tray_spec_file = self.build_dir / "tray_app.spec"
        
        with open(main_spec_file, 'w') as f:
            f.write(main_spec)
        with open(tray_spec_file, 'w') as f:
            f.write(tray_spec)
        
        # Create version info file
        version_info = f'''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(3, 1, 0, 0),
    prodvers=(3, 1, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Beau Lewis'),
        StringStruct(u'FileDescription', u'Quick Document Convertor'),
        StringStruct(u'FileVersion', u'3.1.0.0'),
        StringStruct(u'InternalName', u'QuickDocConvertor'),
        StringStruct(u'LegalCopyright', u'Copyright © 2024 Beau Lewis'),
        StringStruct(u'OriginalFilename', u'Quick Document Convertor.exe'),
        StringStruct(u'ProductName', u'Quick Document Convertor'),
        StringStruct(u'ProductVersion', u'3.1.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        
        version_file = self.build_dir / "version_info.txt"
        with open(version_file, 'w') as f:
            f.write(version_info)
        
        # Copy necessary files to build directory
        # Use the main OCR GUI as the primary application
        main_app_file = self.app_dir / "universal_document_converter_ocr.py"
        if main_app_file.exists():
            shutil.copy2(main_app_file, self.build_dir / "universal_document_converter.py")
        else:
            # Fallback to basic version if OCR version doesn't exist
            fallback_file = self.app_dir / "universal_document_converter.py"
            if fallback_file.exists():
                shutil.copy2(fallback_file, self.build_dir)
        
        # Copy icon if exists
        icon_file = self.app_dir / "icon.ico"
        if not icon_file.exists():
            # Create a simple icon
            self.create_simple_icon(icon_file)
        shutil.copy2(icon_file, self.build_dir)
        
        # Copy other files
        for file in ["requirements.txt", "README.md", "LICENSE"]:
            src = self.app_dir / file
            if src.exists():
                shutil.copy2(src, self.build_dir)
        
        # Build executables
        try:
            os.chdir(self.build_dir)
            
            # Build main application
            subprocess.check_call([
                sys.executable, '-m', 'PyInstaller', 
                '--clean', str(main_spec_file)
            ])
            
            # Build tray application
            subprocess.check_call([
                sys.executable, '-m', 'PyInstaller', 
                '--clean', str(tray_spec_file)
            ])
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create executables: {e}")
            return False
        finally:
            os.chdir(self.app_dir)
    
    def create_simple_icon(self, icon_path: Path):
        """Create a simple icon file"""
        try:
            from PIL import Image, ImageDraw
            
            # Create a 32x32 icon
            img = Image.new('RGB', (32, 32), color='white')
            draw = ImageDraw.Draw(img)
            
            # Draw a simple document icon
            draw.rectangle([4, 4, 28, 28], fill='lightblue', outline='blue', width=2)
            draw.text((8, 12), "QDC", fill='black')
            
            # Save as ICO
            img.save(icon_path, format='ICO')
            
        except ImportError:
            # Fallback: create empty icon file
            icon_path.touch()
    
    def build_installer(self) -> bool:
        """Build the complete installer"""
        print("🏗️  Building Windows installer...")
        
        # Check dependencies
        deps = self.check_dependencies()
        missing = [k for k, v in deps.items() if not v]
        
        if missing:
            print(f"❌ Missing dependencies: {', '.join(missing)}")
            if not self.install_dependencies():
                return False
        
        # Create system tray version
        tray_script = self.create_system_tray_version()
        print(f"✅ Created system tray application: {tray_script}")
        
        # Create executables
        if not self.create_executables():
            return False
        print("✅ Created executable files")
        
        # Create NSIS installer script
        nsis_script = self.create_installer_script()
        print(f"✅ Created installer script: {nsis_script}")
        
        # Build installer with NSIS (if available)
        if deps.get('nsis', False):
            try:
                subprocess.check_call(['makensis', str(nsis_script)])
                print("✅ Created NSIS installer")
            except subprocess.CalledProcessError:
                print("⚠️  NSIS installer creation failed, creating batch installer instead")
                self.create_batch_installer()
        else:
            print("⚠️  NSIS not available, creating batch installer")
            self.create_batch_installer()
        
        return True
    
    def create_batch_installer(self):
        """Create a batch file installer as fallback"""
        batch_installer = self.dist_dir / "install.bat"
        self.dist_dir.mkdir(parents=True, exist_ok=True)
        
        batch_code = f'''@echo off
echo Installing {self.app_name}...

REM Create installation directory
set INSTALL_DIR=%PROGRAMFILES%\\{self.app_name}
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
copy "Quick Document Convertor.exe" "%INSTALL_DIR%\\"
copy "tray_app.exe" "%INSTALL_DIR%\\"
copy "universal_document_converter.py" "%INSTALL_DIR%\\"
copy "requirements.txt" "%INSTALL_DIR%\\"
copy "README.md" "%INSTALL_DIR%\\"
copy "LICENSE" "%INSTALL_DIR%\\"

REM Create shortcuts
echo Creating shortcuts...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\{self.app_name}.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\Quick Document Convertor.exe'; $Shortcut.Save()"

REM Create Start Menu shortcut
if not exist "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{self.app_name}" mkdir "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{self.app_name}"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{self.app_name}\\{self.app_name}.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\Quick Document Convertor.exe'; $Shortcut.Save()"

echo Installation complete!
echo.
echo You can now:
echo - Find the app in Start Menu
echo - Use the desktop shortcut
echo - Pin to taskbar by right-clicking the shortcut
echo.
pause
'''
        
        with open(batch_installer, 'w') as f:
            f.write(batch_code)
        
        print(f"✅ Created batch installer: {batch_installer}")

def main():
    """Main function"""
    print("🚀 Quick Document Convertor - Windows Installer Creator")
    print("=" * 60)
    
    creator = WindowsInstallerCreator()
    
    if creator.build_installer():
        print("\n🎉 Windows installer created successfully!")
        print("\nInstaller features:")
        print("  ✅ Professional exe-style installer")
        print("  ✅ System tray integration")
        print("  ✅ Start Menu shortcuts")
        print("  ✅ Desktop shortcuts")
        print("  ✅ Taskbar pinning support")
        print("  ✅ File associations")
        print("  ✅ Context menu integration")
        print("  ✅ Add/Remove Programs entry")
        print("  ✅ Automatic uninstaller")
        
        print(f"\nFiles created in: {creator.dist_dir}")
        print("\nTo install:")
        print("  1. Run the installer as Administrator")
        print("  2. Follow the installation wizard")
        print("  3. Pin to taskbar by right-clicking the shortcut")
        print("  4. System tray app will auto-start")
        
    else:
        print("❌ Failed to create installer")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 