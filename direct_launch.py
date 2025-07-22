#!/usr/bin/env python3
"""
Direct launcher for Quick Document Convertor - Forces GUI to appear
"""
import tkinter as tk
import sys
import os
from pathlib import Path

def force_window_to_front(root):
    """Force the window to appear and come to front"""
    root.lift()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))
    root.focus_force()
    root.grab_set()
    root.after(100, lambda: root.grab_release())

def main():
    print("🚀 Direct Launch - Quick Document Convertor")
    print("=" * 50)
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    try:
        # Test basic tkinter first
        print("Testing tkinter...")
        root = tk.Tk()
        root.withdraw()  # Hide temporarily
        
        # Import the application
        print("Loading application...")
        from universal_document_converter_ocr import DocumentConverterApp
        
        # Configure the main window
        root.title("OCR Document Converter")
        root.geometry("900x700")
        
        # Force window to appear
        root.deiconify()  # Show window
        force_window_to_front(root)
        
        # Create the application
        print("Starting GUI...")
        app = DocumentConverterApp(root)
        
        # Center window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Final window setup
        root.lift()
        root.focus_force()
        
        print("✅ GUI launched successfully!")
        print("✅ Window should now be visible on your screen")
        
        # Start the main loop
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install python-docx PyPDF2 beautifulsoup4 striprtf ebooklib")
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Trying alternative method...")
        
        # Alternative: Simple tkinter window
        try:
            root = tk.Tk()
            root.title("Quick Document Convertor - Simple Mode")
            root.geometry("400x300")
            
            label = tk.Label(root, text="Quick Document Convertor\n\nIf you see this window,\ntkinter is working!", 
                           font=('Arial', 14), justify='center')
            label.pack(expand=True)
            
            force_window_to_front(root)
            root.mainloop()
            
        except Exception as e2:
            print(f"❌ Even simple tkinter failed: {e2}")
            input("Press Enter to exit...")

if __name__ == "__main__":
    main() 