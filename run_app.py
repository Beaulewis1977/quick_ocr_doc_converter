#!/usr/bin/env python3
"""
Quick Document Convertor - Simple Launcher
This is a simple launcher that can be easily run by double-clicking
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []
    
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter (usually comes with Python)")
    
    # Check optional dependencies
    optional_deps = {
        'python-docx': 'docx',
        'PyPDF2': 'PyPDF2', 
        'beautifulsoup4': 'bs4',
        'striprtf': 'striprtf',
        'ebooklib': 'ebooklib'
    }
    
    missing_optional = []
    for package, module in optional_deps.items():
        try:
            if '.' in module:
                parts = module.split('.')
                mod = __import__(parts[0])
                for part in parts[1:]:
                    mod = getattr(mod, part)
            else:
                __import__(module)
        except ImportError:
            missing_optional.append(package)
    
    return missing, missing_optional

def install_missing_packages(packages):
    """Install missing packages"""
    if not packages:
        return True
    
    print(f"Installing missing packages: {', '.join(packages)}")
    try:
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")
        return False

def main():
    """Main launcher function"""
    print("Quick Document Convertor")
    print("=" * 30)
    
    # Check if we're in the right directory
    app_file = Path(__file__).parent / "universal_document_converter.py"
    if not app_file.exists():
        print("ERROR: Application file not found!")
        print("Make sure this launcher is in the same folder as universal_document_converter.py")
        input("Press Enter to exit...")
        return
    
    # Check dependencies
    missing, missing_optional = check_dependencies()
    
    if missing:
        print(f"ERROR: Required dependencies missing: {', '.join(missing)}")
        print("Please install Python with tkinter support")
        input("Press Enter to exit...")
        return
    
    if missing_optional:
        print(f"Optional dependencies missing: {', '.join(missing_optional)}")
        response = input("Install them now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            if not install_missing_packages(missing_optional):
                print("Some packages failed to install, but the app may still work")
                input("Press Enter to continue...")
    
    # Launch the application
    print("Starting Quick Document Convertor...")
    try:
        # Import and run the application
        sys.path.insert(0, str(Path(__file__).parent))
        from universal_document_converter import main
        main()
    except Exception as e:
        print(f"Error starting application: {e}")
        print("\nTrying alternative launch method...")
        try:
            subprocess.run([sys.executable, str(app_file)])
        except Exception as e2:
            print(f"Alternative launch also failed: {e2}")
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()
