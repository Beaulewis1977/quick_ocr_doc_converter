#!/usr/bin/env python3
"""
Universal Document Converter - Quick Launch Script
Designed and built by Beau Lewis (blewisxx@gmail.com)

Simple launcher that checks dependencies and starts the GUI application.
"""

import sys
import os
import subprocess

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    required_packages = [
        'python-docx',
        'PyPDF2', 
        'beautifulsoup4',
        'striprtf',
        'tkinterdnd2'
    ]
    
    for package in required_packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"   ⚠️  Warning: Could not install {package}")
    
    print("✅ Dependencies installation complete")

def check_dependencies():
    """Check if all dependencies are available"""
    dependencies = {
        'python-docx': 'docx',
        'PyPDF2': 'PyPDF2',
        'beautifulsoup4': 'bs4', 
        'striprtf': 'striprtf',
        'tkinterdnd2': 'tkinterdnd2'
    }
    
    missing = []
    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)
    
    return missing

def main():
    """Main launcher function"""
    print("🚀 Universal Document Converter")
    print("Designed and built by Beau Lewis (blewisxx@gmail.com)")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"📦 Missing dependencies: {', '.join(missing)}")
        response = input("Install missing dependencies? (y/n): ").lower().strip()
        
        if response in ['y', 'yes', '']:
            install_dependencies()
        else:
            print("⚠️  Some features may not work without all dependencies")
    
    # Start the GUI application
    print("🚀 Starting Universal Document Converter...")
    try:
        # Import and run the main application
        from universal_document_converter import main as run_converter
        run_converter()
    except ImportError as e:
        print(f"❌ Error: Could not start converter: {e}")
        print("   Make sure 'universal_document_converter.py' is in the same directory")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 