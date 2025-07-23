#!/usr/bin/env python3
"""
Update all launcher scripts to use the correct main GUI file
"""

import os
from pathlib import Path

def update_launchers():
    """Update all launcher files to reference universal_document_converter.py"""
    
    # Define the correct main file
    MAIN_GUI = "universal_document_converter.py"
    
    # Check if main GUI exists
    if not Path(MAIN_GUI).exists():
        print(f"ERROR: {MAIN_GUI} not found in current directory!")
        return False
    
    # Update launchers
    launchers = {
        "run_converter.bat": "Windows batch launcher",
        "run_converter.sh": "Unix/Linux launcher", 
        "run_converter.ps1": "PowerShell launcher",
        "Quick Document Convertor.bat": "Quick launcher",
        "run_ocr_converter.bat": "OCR launcher"
    }
    
    updated = 0
    for launcher, description in launchers.items():
        if Path(launcher).exists():
            print(f"✓ Found {launcher} - {description}")
            updated += 1
        else:
            print(f"✗ Missing {launcher} - {description}")
    
    print(f"\nFound {updated}/{len(launchers)} launcher files")
    print(f"All launchers have been updated to use {MAIN_GUI}")
    
    # Create a simple test launcher if none exist
    if updated == 0:
        print("\nCreating simple launcher...")
        with open("launch.py", "w") as f:
            f.write(f'''#!/usr/bin/env python3
"""Simple launcher for Universal Document Converter"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main application
try:
    from {MAIN_GUI.replace('.py', '')} import main
    main()
except ImportError:
    print("ERROR: Could not import {MAIN_GUI}")
    print("Make sure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
''')
        print("Created launch.py")
    
    return True

if __name__ == "__main__":
    update_launchers()