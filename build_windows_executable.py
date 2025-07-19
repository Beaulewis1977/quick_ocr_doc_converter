#!/usr/bin/env python3
"""
Windows Executable Builder for Universal Document Converter
Creates a standalone Windows executable with all dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import zipfile

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def create_spec_file():
    """Create PyInstaller spec file with all options"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['universal_document_converter_complete.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ocr_engine', 'ocr_engine'),
        ('icon.ico', '.'),
        ('README.md', '.'),
        ('requirements.txt', '.')
    ],
    hiddenimports=[
        'docx',
        'PyPDF2',
        'beautifulsoup4',
        'bs4',
        'striprtf',
        'tkinterdnd2',
        'pytesseract',
        'PIL',
        'cv2',
        'numpy',
        'psutil',
        'html2text',
        'ebooklib',
        'odf',
        'xml.etree.ElementTree',
        'csv',
        'json',
        'gzip'
    ],
    hookspath=[],
    hooksconfig={},
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
    name='UniversalDocumentConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version='version_info.txt'
)
'''
    
    with open('universal_converter.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ Created PyInstaller spec file")

def create_version_info():
    """Create version info file for Windows executable"""
    version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(3, 0, 0, 0),
    prodvers=(3, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Beau Lewis'),
        StringStruct(u'FileDescription', u'Universal Document Converter - Convert documents and images to Markdown'),
        StringStruct(u'FileVersion', u'3.0.0.0'),
        StringStruct(u'InternalName', u'UniversalDocumentConverter'),
        StringStruct(u'LegalCopyright', u'© 2024 Beau Lewis. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'UniversalDocumentConverter.exe'),
        StringStruct(u'ProductName', u'Universal Document Converter Complete'),
        StringStruct(u'ProductVersion', u'3.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w') as f:
        f.write(version_info)
    
    print("✓ Created version info file")

def build_executable():
    """Build the Windows executable"""
    print("\n🔨 Building Windows executable...")
    
    # Run PyInstaller
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "universal_converter.spec"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Successfully built executable")
        return True
    else:
        print("✗ Failed to build executable")
        print(result.stderr)
        return False

def create_installer_script():
    """Create NSIS installer script"""
    nsis_script = '''!define APP_NAME "Universal Document Converter"
!define COMP_NAME "Beau Lewis"
!define VERSION "3.0.0.0"
!define COPYRIGHT "© 2024 Beau Lewis"
!define DESCRIPTION "Convert documents and images to Markdown format"
!define INSTALLER_NAME "UniversalDocumentConverter_Setup.exe"
!define MAIN_APP_EXE "UniversalDocumentConverter.exe"
!define INSTALL_TYPE "SetShellVarContext current"
!define REG_ROOT "HKCU"
!define REG_APP_PATH "Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\${MAIN_APP_EXE}"
!define UNINSTALL_PATH "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}"

!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

!include "MUI2.nsh"

Name "${APP_NAME}"
Caption "${APP_NAME} ${VERSION} Setup"
OutFile "${INSTALLER_NAME}"
BrandingText "${APP_NAME} ${VERSION}"
InstallDirRegKey "${REG_ROOT}" "${REG_APP_PATH}" ""
InstallDir "$PROGRAMFILES\\Universal Document Converter"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Main Application" SecMain
    SetOutPath "$INSTDIR"
    File "dist\\UniversalDocumentConverter.exe"
    File "icon.ico"
    File "README.md"
    File "LICENSE"
    
    # Create shortcuts
    CreateDirectory "$SMPROGRAMS\\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\${MAIN_APP_EXE}" "" "$INSTDIR\\icon.ico"
    CreateShortCut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\${MAIN_APP_EXE}" "" "$INSTDIR\\icon.ico"
    CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
    
    # Write registry keys
    WriteRegStr ${REG_ROOT} "${REG_APP_PATH}" "" "$INSTDIR\\${MAIN_APP_EXE}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "DisplayName" "${APP_NAME}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "DisplayIcon" "$INSTDIR\\icon.ico"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "DisplayVersion" "${VERSION}"
    WriteRegStr ${REG_ROOT} "${UNINSTALL_PATH}" "Publisher" "${COMP_NAME}"
    
    # Create uninstaller
    WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\${MAIN_APP_EXE}"
    Delete "$INSTDIR\\icon.ico"
    Delete "$INSTDIR\\README.md"
    Delete "$INSTDIR\\LICENSE"
    Delete "$INSTDIR\\uninstall.exe"
    
    Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\\${APP_NAME}\\Uninstall.lnk"
    Delete "$DESKTOP\\${APP_NAME}.lnk"
    
    RMDir "$SMPROGRAMS\\${APP_NAME}"
    RMDir "$INSTDIR"
    
    DeleteRegKey ${REG_ROOT} "${REG_APP_PATH}"
    DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}"
SectionEnd
'''
    
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)
    
    print("✓ Created NSIS installer script")

def create_portable_zip():
    """Create a portable ZIP version"""
    print("\n📦 Creating portable ZIP version...")
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("✗ No dist directory found. Build the executable first.")
        return
    
    # Create portable directory
    portable_dir = Path("portable")
    portable_dir.mkdir(exist_ok=True)
    
    # Copy executable and required files
    shutil.copy2("dist/UniversalDocumentConverter.exe", portable_dir)
    if Path("icon.ico").exists():
        shutil.copy2("icon.ico", portable_dir)
    if Path("README.md").exists():
        shutil.copy2("README.md", portable_dir)
    if Path("LICENSE").exists():
        shutil.copy2("LICENSE", portable_dir)
    
    # Create batch file for portable version
    batch_content = '''@echo off
echo Starting Universal Document Converter...
start "" "UniversalDocumentConverter.exe"
'''
    
    with open(portable_dir / "Start_Converter.bat", 'w') as f:
        f.write(batch_content)
    
    # Create ZIP file
    zip_name = "UniversalDocumentConverter_Portable.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in portable_dir.rglob("*"):
            zipf.write(file, file.relative_to(portable_dir))
    
    print(f"✓ Created portable ZIP: {zip_name}")
    
    # Clean up
    shutil.rmtree(portable_dir)

def main():
    """Main build process"""
    print("🚀 Universal Document Converter - Windows Build Script")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required")
        sys.exit(1)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("✗ Failed to setup PyInstaller")
        sys.exit(1)
    
    # Create required files
    create_version_info()
    create_spec_file()
    
    # Build executable
    if build_executable():
        print("\n✅ Build completed successfully!")
        print(f"   Executable: dist/UniversalDocumentConverter.exe")
        
        # Create portable ZIP
        create_portable_zip()
        
        # Create installer script
        create_installer_script()
        print("\n📝 Next steps:")
        print("   1. Install NSIS: https://nsis.sourceforge.io/")
        print("   2. Right-click installer.nsi and select 'Compile NSIS Script'")
        print("   3. Your installer will be created: UniversalDocumentConverter_Setup.exe")
        
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()