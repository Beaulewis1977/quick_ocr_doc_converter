#!/usr/bin/env python3
"""
Quick Document Convertor - Shortcut Setup
Creates desktop shortcuts and start menu entries for easy access
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess

def check_python_packages():
    """Check and install required packages"""
    required_packages = [
        'python-docx',
        'PyPDF2', 
        'beautifulsoup4',
        'striprtf',
        'ebooklib',
        'tkinterdnd2'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'python-docx':
                import docx
            elif package == 'PyPDF2':
                import PyPDF2
            elif package == 'beautifulsoup4':
                from bs4 import BeautifulSoup
            elif package == 'striprtf':
                from striprtf.striprtf import rtf_to_text
            elif package == 'ebooklib':
                import ebooklib
            elif package == 'tkinterdnd2':
                import tkinterdnd2
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("📦 Installing missing packages...")
        for package in missing_packages:
            try:
                print(f"   Installing {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"   ✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to install {package}: {e}")
        print()

def create_windows_shortcuts():
    """Create Windows shortcuts and start menu entries"""
    try:
        # Get current directory
        app_dir = Path(__file__).parent.absolute()
        app_file = app_dir / "universal_document_converter.py"
        batch_file = app_dir / "Quick Document Convertor.bat"
        
        if not app_file.exists():
            print("❌ Application file not found!")
            return False
        
        # Create desktop shortcut
        desktop = Path.home() / "Desktop"
        desktop_shortcut = desktop / "Quick Document Convertor.lnk"
        
        # Create start menu shortcut
        start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
        start_menu_shortcut = start_menu / "Quick Document Convertor.lnk"
        
        # Try to create shortcuts using Windows COM
        try:
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # Desktop shortcut
            shortcut = shell.CreateShortCut(str(desktop_shortcut))
            shortcut.Targetpath = str(batch_file)
            shortcut.WorkingDirectory = str(app_dir)
            shortcut.Description = "Quick Document Convertor - Convert documents between multiple formats"
            shortcut.save()
            print(f"✅ Desktop shortcut created: {desktop_shortcut}")
            
            # Start menu shortcut
            shortcut = shell.CreateShortCut(str(start_menu_shortcut))
            shortcut.Targetpath = str(batch_file)
            shortcut.WorkingDirectory = str(app_dir)
            shortcut.Description = "Quick Document Convertor - Convert documents between multiple formats"
            shortcut.save()
            print(f"✅ Start menu shortcut created: {start_menu_shortcut}")
            
            return True
            
        except ImportError:
            print("⚠️  pywin32 not available, installing...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywin32'])
                print("✅ pywin32 installed, please run this script again")
                return False
            except subprocess.CalledProcessError:
                print("❌ Failed to install pywin32")
                return False
                
    except Exception as e:
        print(f"❌ Failed to create Windows shortcuts: {e}")
        return False

def create_unix_shortcuts():
    """Create Unix/Linux desktop entries"""
    try:
        app_dir = Path(__file__).parent.absolute()
        app_file = app_dir / "universal_document_converter.py"
        
        if not app_file.exists():
            print("❌ Application file not found!")
            return False
        
        # Create .desktop file
        desktop_entry = f"""[Desktop Entry]
Name=Quick Document Convertor
Comment=Convert documents between multiple formats
Exec=python3 "{app_file}"
Path={app_dir}
Icon=text-x-generic
Terminal=false
Type=Application
Categories=Office;Utility;
"""
        
        # Save to desktop
        desktop = Path.home() / "Desktop"
        desktop_file = desktop / "Quick Document Convertor.desktop"
        
        with open(desktop_file, 'w') as f:
            f.write(desktop_entry)
        
        # Make executable
        os.chmod(desktop_file, 0o755)
        print(f"✅ Desktop entry created: {desktop_file}")
        
        # Also save to applications directory
        apps_dir = Path.home() / ".local/share/applications"
        apps_dir.mkdir(parents=True, exist_ok=True)
        apps_file = apps_dir / "quick-document-convertor.desktop"
        
        with open(apps_file, 'w') as f:
            f.write(desktop_entry)
        
        os.chmod(apps_file, 0o755)
        print(f"✅ Application entry created: {apps_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create Unix shortcuts: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Quick Document Convertor - Enhanced Setup")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        sys.exit(1)

    print(f"✅ Python {sys.version.split()[0]} detected")

    # Check and install packages
    check_python_packages()

    # Try to use enhanced cross-platform integration
    try:
        import cross_platform

        platform = cross_platform.get_platform()
        print(f"🌍 Platform detected: {platform}")

        # Create platform directories
        if cross_platform.create_platform_directories():
            print("✅ Platform directories created")

        # Get platform integration
        integration = cross_platform.get_platform_integration()

        if integration:
            print(f"🔧 Using enhanced {platform} integration...")

            app_path = Path(__file__).parent / "universal_document_converter.py"
            icon_path = None

            # Look for icon file
            for icon_file in ["icon.ico", "icon.png", "app_icon.ico"]:
                icon_candidate = Path(__file__).parent / icon_file
                if icon_candidate.exists():
                    icon_path = icon_candidate
                    break

            if platform == 'windows':
                results = integration.setup_windows_integration(app_path, icon_path)
                success = results.get('shortcuts', {}).get('desktop', False)
            elif platform == 'linux':
                results = integration.setup_linux_integration(app_path, icon_path)
                success = results.get('desktop_file', False)
            elif platform == 'macos':
                # For macOS, we'll use the basic setup for now
                success = create_unix_shortcuts()
            else:
                success = False

            if success:
                print("✅ Enhanced integration completed successfully!")
            else:
                print("⚠️  Enhanced integration had some issues, falling back to basic setup")
                success = create_basic_shortcuts()
        else:
            print("⚠️  Enhanced integration not available, using basic setup")
            success = create_basic_shortcuts()

    except ImportError:
        print("⚠️  Cross-platform modules not available, using basic setup")
        success = create_basic_shortcuts()

    if success:
        print("\n🎉 Setup completed successfully!")
        print("\nYou can now:")
        if os.name == 'nt':
            print("  • Double-click the desktop shortcut")
            print("  • Find 'Quick Document Convertor' in Start Menu")
            print("  • Pin the shortcut to taskbar (right-click → Pin to taskbar)")
            print("  • Run 'Quick Document Convertor.bat' directly")
        else:
            print("  • Double-click the desktop icon")
            print("  • Find 'Quick Document Convertor' in applications menu")
            print("  • Run the Python script directly")

        print(f"  • Or run: python universal_document_converter.py")
    else:
        print("\n⚠️  Setup completed with some issues")
        print("You can still run the application with:")
        print("  python universal_document_converter.py")

    input("\nPress Enter to exit...")


def create_basic_shortcuts():
    """Create basic shortcuts using the original method"""
    if os.name == 'nt':  # Windows
        print("🖥️  Setting up Windows shortcuts...")
        return create_windows_shortcuts()
    else:  # Unix/Linux/macOS
        print("🐧 Setting up Unix shortcuts...")
        return create_unix_shortcuts()

if __name__ == "__main__":
    main()
