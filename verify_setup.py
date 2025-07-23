#!/usr/bin/env python3
"""
Verify that all files are properly configured for Universal Document Converter
"""

import os
import sys
from pathlib import Path

def verify_setup():
    """Verify that all components are properly set up"""
    
    print("Universal Document Converter - Setup Verification")
    print("=" * 50)
    
    # Check main files
    main_files = {
        "universal_document_converter.py": "Main GUI application",
        "cli.py": "Command-line interface",
        "requirements.txt": "Python dependencies"
    }
    
    print("\n1. Checking main files...")
    missing_files = []
    for file, description in main_files.items():
        if Path(file).exists():
            print(f"  ✓ {file} - {description}")
        else:
            print(f"  ✗ {file} - {description} [MISSING]")
            missing_files.append(file)
    
    # Check launchers
    print("\n2. Checking launcher scripts...")
    launchers = {
        "run_converter.bat": "Windows batch launcher",
        "run_converter.sh": "Unix/Linux launcher",
        "run_converter.ps1": "PowerShell launcher",
        "Quick Document Convertor.bat": "Quick launcher",
        "run_ocr_converter.bat": "OCR launcher"
    }
    
    for launcher, description in launchers.items():
        if Path(launcher).exists():
            # Verify it references the correct main file
            with open(launcher, 'r') as f:
                content = f.read()
                if "universal_document_converter.py" in content:
                    print(f"  ✓ {launcher} - {description} [CORRECT]")
                elif "universal_document_converter_ocr.py" in content:
                    print(f"  ❌ {launcher} - {description} [OUTDATED - NEEDS UPDATE]")
                else:
                    print(f"  ? {launcher} - {description}")
        else:
            print(f"  - {launcher} - {description} [NOT FOUND]")
    
    # Check OCR engine
    print("\n3. Checking OCR engine...")
    if Path("ocr_engine").is_dir():
        print("  ✓ OCR engine directory found")
        ocr_files = ["ocr_engine.py", "ocr_integration.py", "format_detector.py"]
        for file in ocr_files:
            if Path(f"ocr_engine/{file}").exists():
                print(f"    ✓ {file}")
            else:
                print(f"    ✗ {file} [MISSING]")
    else:
        print("  ✗ OCR engine directory not found")
    
    # Check documentation
    print("\n4. Checking documentation...")
    docs = ["README.md", "OCR_README.md", "INSTALLATION_GUIDE.md"]
    for doc in docs:
        if Path(doc).exists():
            print(f"  ✓ {doc}")
        else:
            print(f"  - {doc} [NOT FOUND]")
    
    # Summary
    print("\n" + "=" * 50)
    if missing_files:
        print("⚠ WARNING: Some required files are missing!")
        print("Missing files:", ", ".join(missing_files))
        return False
    else:
        print("✅ All core files are present!")
        print("\nTo run the application:")
        print("  GUI: python universal_document_converter.py")
        print("  CLI: python cli.py <input_file> -o <output_file>")
        return True

if __name__ == "__main__":
    sys.exit(0 if verify_setup() else 1)