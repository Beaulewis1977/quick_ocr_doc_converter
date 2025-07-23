#!/usr/bin/env python3
"""
Document Converter - Main Entry Point
Clean GUI application without legacy DLL functionality

This is the refactored version that focuses on:
- Document conversion (DOCX, PDF, TXT, HTML, RTF, EPUB, Markdown)
- OCR functionality (Tesseract, EasyOCR, Google Vision API)
- Markdown tools and reader
- API management for cloud services
- Advanced settings and configuration

Legacy VB6/VFP9 DLL integration has been moved to legacy_dll_builder/
"""

import sys
import os
from pathlib import Path

# Add the parent directory to path to access the main GUI
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the cleaned universal document converter
from universal_document_converter import UniversalDocumentConverter

import tkinter as tk

def main():
    """Main entry point for Document Converter"""
    try:
        # Create main window
        root = tk.Tk()
        
        # Initialize the application
        app = UniversalDocumentConverter(root)
        
        # Center window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Start the application
        root.mainloop()
        
    except KeyboardInterrupt:
        print("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting Document Converter: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()