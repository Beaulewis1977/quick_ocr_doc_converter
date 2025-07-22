import os
import sys
import subprocess
from pathlib import Path

def create_installer():
    print("📦 Creating Windows Installer...")
    
    # Path to Inno Setup compiler (common install locations)
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe"
    ]
    
    # Find Inno Setup compiler
    iscc = None
    for path in inno_paths:
        if Path(path).exists():
            iscc = path
            break
            
    if not iscc:
        print("❌ Inno Setup not found! Please install from:")
        print("   https://jrsoftware.org/isdl.php")
        print("   Then re-run this script")
        return False
        
    # Create installer script
    iss_content = f"""; Quick Document Convertor Installer

[Setup]
AppName=Quick Document Convertor
AppVersion=3.1.0
DefaultDirName={{autopf}}\\QuickDocumentConvertor
DefaultGroupName=Quick Document Convertor
UninstallDisplayIcon={{app}}\\Quick Document Convertor.exe
OutputDir=dist
OutputBaseFilename=QuickDocumentConvertor_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
LicenseFile=LICENSE

[Files]
Source: "dist\\Quick Document Convertor.exe"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{group}}\\Quick Document Convertor"; Filename: "{{app}}\\Quick Document Convertor.exe"
Name: "{{commondesktop}}\\Quick Document Convertor"; Filename: "{{app}}\\Quick Document Convertor.exe"

[Run]
Filename: "{{app}}\\Quick Document Convertor.exe"; Description: "Run application now"; Flags: postinstall nowait

[UninstallDelete]
Type: files; Name: "{{app}}\\*.*"
Type: dirifempty; Name: "{{app}}"
"""

    # Write ISS file
    with open("installer.iss", "w") as f:
        f.write(iss_content)
    
    # Compile installer
    try:
        subprocess.check_call([iscc, "installer.iss"])
        print("✅ Installer created in dist directory")
        print("   File: dist\\QuickDocumentConvertor_Setup.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create installer: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Quick Document Convertor - Installer Creator")
    print("=" * 50)
    
    # Verify executable exists
    exe_path = Path("dist") / "Quick Document Convertor.exe"
    if not exe_path.exists():
        print("❌ Main executable not found! First run:")
        print("   python create_executable.py")
        sys.exit(1)
        
    create_installer()
    input("\nPress Enter to exit...")
