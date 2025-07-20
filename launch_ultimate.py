#!/usr/bin/env python3
"""
Launch Universal Document Converter Ultimate
The most feature-rich version with all tools and settings
"""

import os
import sys
import subprocess

def main():
    print("🚀 Launching Universal Document Converter Ultimate...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6+ required")
        sys.exit(1)
    
    # Launch the ultimate version
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ultimate_path = os.path.join(script_dir, "universal_document_converter_ultimate.py")
        
        # Run with python3 explicitly
        subprocess.run([sys.executable, ultimate_path])
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure tkinter is installed: sudo apt-get install python3-tk")
        print("2. For drag & drop: pip install tkinterdnd2")
        print("3. For API server: pip install flask flask-cors waitress")
        print("4. For full OCR: pip install easyocr")
        sys.exit(1)

if __name__ == "__main__":
    main()