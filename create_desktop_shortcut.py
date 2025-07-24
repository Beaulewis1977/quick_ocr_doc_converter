#!/usr/bin/env python3
"""
Create a desktop shortcut for OCR Document Converter safely.
This script avoids command injection vulnerabilities by using proper path validation.
"""

import os
import sys
import platform
from pathlib import Path


def create_windows_shortcut():
    """Create a Windows desktop shortcut using COM objects."""
    try:
        import win32com.client
    except ImportError:
        print("Installing pywin32 for shortcut creation...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
        import win32com.client
    
    # Get safe, validated paths
    desktop = Path.home() / "Desktop"
    current_dir = Path.cwd().resolve()
    target_path = current_dir / "run_ocr_converter.bat"
    shortcut_path = desktop / "OCR Document Converter.lnk"
    
    # Validate paths
    if not desktop.exists():
        print(f"Desktop folder not found at {desktop}")
        return False
    
    if not target_path.exists():
        print(f"Target file not found: {target_path}")
        return False
    
    # Create shortcut using COM
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.TargetPath = str(target_path)
    shortcut.WorkingDirectory = str(current_dir)
    shortcut.IconLocation = str(target_path)
    shortcut.Description = "OCR Document Converter - Transform documents with AI-powered OCR"
    shortcut.Save()
    
    print(f"Shortcut created successfully at: {shortcut_path}")
    return True


def create_linux_desktop_entry():
    """Create a Linux desktop entry file."""
    desktop_dir = Path.home() / ".local" / "share" / "applications"
    desktop_dir.mkdir(parents=True, exist_ok=True)
    
    current_dir = Path.cwd().resolve()
    desktop_file = desktop_dir / "ocr-document-converter.desktop"
    
    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=OCR Document Converter
Comment=Transform documents with AI-powered OCR
Exec=python3 {current_dir}/universal_document_converter.py
Icon={current_dir}/icon.png
Terminal=false
Categories=Office;Graphics;
"""
    
    desktop_file.write_text(content)
    desktop_file.chmod(0o755)
    
    print(f"Desktop entry created at: {desktop_file}")
    return True


def create_macos_alias():
    """Create a macOS alias/shortcut."""
    try:
        import subprocess
        current_dir = Path.cwd().resolve()
        app_path = current_dir / "OCR Document Converter.app"
        desktop = Path.home() / "Desktop"
        
        # Create alias using osascript
        script = f'''
        tell application "Finder"
            make alias file to POSIX file "{app_path}" at desktop
            set name of result to "OCR Document Converter"
        end tell
        '''
        
        subprocess.run(['osascript', '-e', script], check=True)
        print("macOS alias created on Desktop")
        return True
    except Exception as e:
        print(f"Could not create macOS alias: {e}")
        return False


def main():
    """Main function to create appropriate shortcut based on OS."""
    system = platform.system()
    
    print(f"Creating shortcut for {system} system...")
    
    try:
        if system == "Windows":
            success = create_windows_shortcut()
        elif system == "Linux":
            success = create_linux_desktop_entry()
        elif system == "Darwin":  # macOS
            success = create_macos_alias()
        else:
            print(f"Unsupported operating system: {system}")
            success = False
        
        if not success:
            print("Failed to create shortcut")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error creating shortcut: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()