#!/usr/bin/env python3
"""
Quick Document Convertor - System Tray Application
"""

import tkinter as tk
from tkinter import messagebox
import threading
import sys
import os
from pathlib import Path
import subprocess

# Add the application directory to Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

class SystemTrayApp:
    """System tray application for Quick Document Convertor"""
    
    def __init__(self):
        self.app_dir = Path(__file__).parent
        self.main_app = self.app_dir / "universal_document_converter_ocr.py"
        self.icon = None
        self.running = False
        
    def create_icon(self):
        """Create a simple icon for the system tray"""
        # Create a simple icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw a simple document icon
        draw.rectangle([10, 10, 50, 50], fill='lightblue', outline='blue', width=2)
        draw.text((15, 25), "QDC", fill='black')
        
        return image
    
    def show_main_app(self, icon=None, item=None):
        """Show the main application"""
        try:
            if self.main_app.exists():
                subprocess.Popen([sys.executable, str(self.main_app)])
            else:
                messagebox.showerror("Error", "Main application not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start application: {e}")
    
    def show_about(self, icon=None, item=None):
        """Show about dialog"""
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("About", 
                          "Quick Document Convertor v3.1.0\n"
                          "Enterprise document conversion tool\n"
                          "Created by Beau Lewis")
        root.destroy()
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        self.running = False
        if self.icon:
            self.icon.stop()
    
    def run(self):
        """Run the system tray application"""
        if not TRAY_AVAILABLE:
            print("System tray not available. Install pystray and pillow.")
            return
            
        self.running = True
        
        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem("Open Quick Document Convertor", self.show_main_app, default=True),
            pystray.MenuItem("About", self.show_about),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app)
        )
        
        # Create icon
        icon_image = self.create_icon()
        self.icon = pystray.Icon("Quick Document Convertor", icon_image, menu=menu)
        
        # Run the icon
        self.icon.run()

def main():
    """Main entry point"""
    app = SystemTrayApp()
    app.run()

if __name__ == "__main__":
    main()
