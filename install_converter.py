#!/usr/bin/env python3
"""
Document Converter Installer
Sets up the document converter with all dependencies and desktop shortcuts
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def install_packages():
    """Install required Python packages"""
    packages = [
        'python-docx',
        'PyPDF2',
        'tkinterdnd2',
        'winshell',
        'pywin32'
    ]
    
    print("📦 Installing required packages...")
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"   ✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")
            # Continue with other packages
    
def create_desktop_shortcut():
    """Create a desktop shortcut (Windows)"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Document Converter.lnk")
        target = os.path.abspath(os.path.join(os.path.dirname(__file__), "run_converter.bat"))
        wDir = os.getcwd()
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print(f"✓ Desktop shortcut created: {path}")
        
    except ImportError:
        print("⚠️  Could not create desktop shortcut (winshell not available)")
        print("   You can manually create a shortcut to run_converter.bat")
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")

def create_start_menu_shortcut():
    """Create a start menu shortcut (Windows)"""
    try:
        start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
        shortcut_path = start_menu / "Document Converter.lnk"
        
        # Copy the batch file to a more permanent location
        app_dir = Path.home() / "AppData/Local/DocumentConverter"
        app_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy necessary files
        files_to_copy = [
            "document_converter_gui.py",
            "run_converter.bat"
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, app_dir / file)
        
        print(f"✓ App files copied to: {app_dir}")
        
    except Exception as e:
        print(f"⚠️  Could not set up start menu shortcut: {e}")

def main():
    """Main installer function"""
    print("🚀 Document to Markdown Converter - Installer")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install packages
    install_packages()
    
    # Create shortcuts (Windows only)
    if os.name == 'nt':
        print("\n📱 Creating shortcuts...")
        create_desktop_shortcut()
        create_start_menu_shortcut()
    
    print("\n🎉 Installation complete!")
    print("\nTo use the converter:")
    print("  • Double-click 'run_converter.bat'")
    print("  • Or run: python document_converter_gui.py")
    if os.name == 'nt':
        print("  • Or use the desktop/start menu shortcut")
    
    print("\n💡 Features:")
    print("  ✓ Convert DOCX, PDF, and TXT files to Markdown")
    print("  ✓ Batch process entire directories")
    print("  ✓ Preserve folder structure")
    print("  ✓ Drag and drop support")
    print("  ✓ Progress tracking")
    print("  ✓ Error handling and reporting")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
