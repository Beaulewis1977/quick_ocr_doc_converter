#!/usr/bin/env python3
"""
Universal Document Converter Launcher
Launches the complete GUI application with OCR and document conversion
"""

import os
import sys
import subprocess
from pathlib import Path

def find_main_app():
    """Find the main application file"""
    # The unified GUI application
    app_files = [
        'universal_document_converter.py'
    ]
    
    for app_file in app_files:
        if os.path.exists(app_file):
            return app_file
    
    return None

def main():
    """Main launcher function"""
    print("OCR Document Converter Launcher")
    print("=" * 40)
    
    # Find the main application
    app_file = find_main_app()
    
    if not app_file:
        print("ERROR: No application file found!")
        print("Looking for:")
        print("  - universal_document_converter_ocr.py")
        print("  - main_app.py")
        print("  - universal_document_converter.py")
        input("\nPress Enter to exit...")
        return 1
    
    print(f"Found application: {app_file}")
    print("Starting...")
    
    try:
        # Run the application
        result = subprocess.run([sys.executable, app_file], 
                              cwd=Path(__file__).parent)
        return result.returncode
    except Exception as e:
        print(f"\nERROR: Failed to start application: {e}")
        input("\nPress Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())