#!/usr/bin/env python3
"""
Quick Document Convertor - Executable Creator
Creates a standalone executable using PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    try:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install PyInstaller: {e}")
        return False

def create_icon():
    """Create a simple icon file"""
    icon_content = """
# This would be an actual icon file in a real implementation
# For now, we'll use the default Python icon
"""
    # Note: In a real implementation, you'd want to include an actual .ico file
    # For now, PyInstaller will use the default Python icon
    return None

def create_executable():
    """Create standalone executable"""
    app_dir = Path(__file__).parent
    main_script = app_dir / "universal_document_converter.py"
    
    if not main_script.exists():
        print("❌ Main application script not found!")
        return False
    
    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', 'Quick Document Convertor',
        '--distpath', str(app_dir / 'dist'),
        '--workpath', str(app_dir / 'build'),
        '--specpath', str(app_dir),
        '--add-data', f'{app_dir / "icon.ico"};.',
        '--hidden-import', 'tkinterdnd2',
        '--hidden-import', 'pywin32',
        str(main_script)
    ]
    
    # Add icon if available
    icon_file = app_dir / "icon.ico"
    if icon_file.exists():
        cmd.extend(['--icon', str(icon_file)])
    else:
        print("⚠️  Icon file not found - using default icon")
    
    print("Creating executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to create executable: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Quick Document Convertor - Executable Creator")
    print("=" * 55)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        if not install_pyinstaller():
            print("❌ Failed to install PyInstaller")
            input("Press Enter to exit...")
            return
    
    print("✅ PyInstaller available")
    
    # Create executable
    print("\n📦 Creating standalone executable...")
    if create_executable():
        print("\n🎉 Executable created successfully!")
        
        dist_dir = Path(__file__).parent / 'dist'
        exe_file = dist_dir / 'Quick Document Convertor.exe'
        
        if exe_file.exists():
            print(f"📁 Location: {exe_file}")
            print(f"📏 Size: {exe_file.stat().st_size / 1024 / 1024:.1f} MB")
            print("\nYou can now:")
            print("  • Double-click the .exe file to run")
            print("  • Copy it to any Windows computer (no Python needed)")
            print("  • Pin it to taskbar or start menu")
            print("  • Create shortcuts anywhere")
            
            # Ask if user wants to create desktop shortcut
            response = input("\nCreate desktop shortcut for the executable? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                try:
                    desktop = Path.home() / "Desktop"
                    shortcut_path = desktop / "Quick Document Convertor.lnk"
                    
                    # Try to create shortcut
                    import win32com.client
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(str(shortcut_path))
                    shortcut.Targetpath = str(exe_file)
                    shortcut.WorkingDirectory = str(exe_file.parent)
                    shortcut.Description = "Quick Document Convertor - Standalone Executable"
                    shortcut.save()
                    
                    print(f"✅ Desktop shortcut created: {shortcut_path}")
                    
                except Exception as e:
                    print(f"⚠️  Could not create shortcut: {e}")
                    print("You can manually create a shortcut by right-clicking the .exe file")
        
    else:
        print("❌ Failed to create executable")
        print("\nTroubleshooting:")
        print("  • Make sure all dependencies are installed")
        print("  • Try running: pip install pyinstaller")
        print("  • Check that universal_document_converter.py exists")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
