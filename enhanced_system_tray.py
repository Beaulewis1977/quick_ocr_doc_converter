#!/usr/bin/env python3
"""
Quick Document Convertor - Enhanced System Tray Application
Provides system tray integration with quick access to conversion features
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import sys
import os
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any

# Try to import system tray dependencies
try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

# Try to import psutil for system monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class QuickConverterTray:
    """Enhanced system tray application for Quick Document Convertor"""
    
    def __init__(self):
        self.app_dir = Path(__file__).parent
        self.main_app = self.app_dir / "universal_document_converter.py"
        self.config_file = self.app_dir / "tray_config.json"
        self.icon = None
        self.running = False
        self.main_window = None
        self.config = self.load_config()
        
        # Add current directory to path
        sys.path.insert(0, str(self.app_dir))
        
    def load_config(self) -> Dict[str, Any]:
        """Load tray configuration"""
        default_config = {
            "auto_start": True,
            "show_notifications": True,
            "default_output_format": "markdown",
            "quick_convert_enabled": True,
            "minimize_to_tray": True
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults
                    default_config.update(config)
                    return default_config
            except Exception:
                pass
        
        return default_config
    
    def save_config(self):
        """Save tray configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass
    
    def create_icon_image(self) -> Image.Image:
        """Create a professional icon for the system tray"""
        width = 64
        height = 64
        
        # Create image with transparent background
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw document icon with gradient effect
        # Main document body
        draw.rectangle([12, 8, 52, 56], fill=(70, 130, 180, 255), outline=(25, 25, 112, 255), width=2)
        
        # Document fold corner
        draw.polygon([(42, 8), (52, 8), (52, 18), (42, 8)], fill=(135, 206, 235, 255))
        draw.line([(42, 8), (42, 18), (52, 18)], fill=(25, 25, 112, 255), width=1)
        
        # Document lines
        for i in range(3):
            y = 20 + i * 6
            draw.line([(18, y), (46, y)], fill=(255, 255, 255, 200), width=2)
        
        # Conversion arrow
        draw.polygon([(28, 42), (36, 42), (32, 48)], fill=(255, 215, 0, 255))
        
        return image
    
    def show_notification(self, title: str, message: str):
        """Show system notification"""
        if not self.config.get("show_notifications", True):
            return
            
        if self.icon:
            self.icon.notify(message, title)
    
    def show_main_app(self, icon=None, item=None):
        """Show the main application window"""
        try:
            if self.main_app.exists():
                # Check if already running
                if self.main_window and self.main_window.poll() is None:
                    # Already running, just show notification
                    self.show_notification("Quick Document Convertor", "Application is already running")
                    return
                
                # Start new instance
                self.main_window = subprocess.Popen([
                    sys.executable, str(self.main_app)
                ])
                self.show_notification("Quick Document Convertor", "Application started")
            else:
                self.show_error("Main application not found!", f"Could not find: {self.main_app}")
        except Exception as e:
            self.show_error("Launch Error", f"Failed to start application: {e}")
    
    def quick_convert_file(self, icon=None, item=None):
        """Quick convert a single file"""
        try:
            # Create a temporary tkinter window for file dialog
            root = tk.Tk()
            root.withdraw()
            
            # File dialog
            file_path = filedialog.askopenfilename(
                title="Select file to convert",
                filetypes=[
                    ("All supported", "*.docx;*.pdf;*.txt;*.html;*.rtf;*.epub"),
                    ("Word documents", "*.docx"),
                    ("PDF files", "*.pdf"),
                    ("Text files", "*.txt"),
                    ("HTML files", "*.html"),
                    ("RTF files", "*.rtf"),
                    ("EPUB files", "*.epub"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                # Quick convert using CLI
                output_format = self.config.get("default_output_format", "markdown")
                output_file = Path(file_path).with_suffix(f".{output_format}")
                
                # Try to use CLI for conversion
                cli_script = self.app_dir / "cli.py"
                if cli_script.exists():
                    result = subprocess.run([
                        sys.executable, str(cli_script),
                        file_path, "-o", str(output_file),
                        "-t", output_format
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        self.show_notification("Conversion Complete", 
                                             f"File converted to: {output_file.name}")
                    else:
                        self.show_error("Conversion Failed", result.stderr or "Unknown error")
                else:
                    self.show_error("CLI Not Found", "Command-line interface not available")
            
            root.destroy()
            
        except Exception as e:
            self.show_error("Quick Convert Error", f"Failed to convert file: {e}")
    
    def show_settings(self, icon=None, item=None):
        """Show settings dialog"""
        settings_window = tk.Toplevel()
        settings_window.title("Tray Settings")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)
        
        # Make window stay on top
        settings_window.attributes('-topmost', True)
        
        # Center window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (settings_window.winfo_width() // 2)
        y = (settings_window.winfo_screenheight() // 2) - (settings_window.winfo_height() // 2)
        settings_window.geometry(f"+{x}+{y}")
        
        # Settings frame
        main_frame = ttk.Frame(settings_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="System Tray Settings", 
                               font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Auto-start checkbox
        auto_start_var = tk.BooleanVar(value=self.config.get("auto_start", True))
        auto_start_cb = ttk.Checkbutton(main_frame, text="Start with Windows", 
                                       variable=auto_start_var)
        auto_start_cb.pack(anchor=tk.W, pady=2)
        
        # Show notifications checkbox
        notifications_var = tk.BooleanVar(value=self.config.get("show_notifications", True))
        notifications_cb = ttk.Checkbutton(main_frame, text="Show notifications", 
                                          variable=notifications_var)
        notifications_cb.pack(anchor=tk.W, pady=2)
        
        # Quick convert checkbox
        quick_convert_var = tk.BooleanVar(value=self.config.get("quick_convert_enabled", True))
        quick_convert_cb = ttk.Checkbutton(main_frame, text="Enable quick convert", 
                                          variable=quick_convert_var)
        quick_convert_cb.pack(anchor=tk.W, pady=2)
        
        # Default output format
        ttk.Label(main_frame, text="Default output format:").pack(anchor=tk.W, pady=(10, 2))
        format_var = tk.StringVar(value=self.config.get("default_output_format", "markdown"))
        format_combo = ttk.Combobox(main_frame, textvariable=format_var,
                                   values=["markdown", "txt", "html", "rtf", "epub"],
                                   state="readonly")
        format_combo.pack(anchor=tk.W, pady=2)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        def save_settings():
            self.config["auto_start"] = auto_start_var.get()
            self.config["show_notifications"] = notifications_var.get()
            self.config["quick_convert_enabled"] = quick_convert_var.get()
            self.config["default_output_format"] = format_var.get()
            self.save_config()
            
            # Update Windows startup registry
            self.update_startup_registry(auto_start_var.get())
            
            messagebox.showinfo("Settings", "Settings saved successfully!")
            settings_window.destroy()
        
        def cancel_settings():
            settings_window.destroy()
        
        ttk.Button(buttons_frame, text="Save", command=save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(buttons_frame, text="Cancel", command=cancel_settings).pack(side=tk.RIGHT)
        
        # Show window
        settings_window.mainloop()
    
    def update_startup_registry(self, enable: bool):
        """Update Windows startup registry"""
        try:
            import winreg
            
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "QuickDocConvertor"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                if enable:
                    exe_path = Path(__file__).parent / "tray_app.exe"
                    if exe_path.exists():
                        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, str(exe_path))
                else:
                    try:
                        winreg.DeleteValue(key, app_name)
                    except FileNotFoundError:
                        pass
        except Exception:
            pass
    
    def show_about(self, icon=None, item=None):
        """Show about dialog"""
        about_window = tk.Toplevel()
        about_window.title("About Quick Document Convertor")
        about_window.geometry("400x250")
        about_window.resizable(False, False)
        about_window.attributes('-topmost', True)
        
        # Center window
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (about_window.winfo_width() // 2)
        y = (about_window.winfo_screenheight() // 2) - (about_window.winfo_height() // 2)
        about_window.geometry(f"+{x}+{y}")
        
        # Content frame
        content_frame = ttk.Frame(about_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # App info
        info_text = """Quick Document Convertor v2.0.0
Enterprise Document Conversion Tool

Created by Beau Lewis
blewisxx@gmail.com

Features:
• Convert between 6 input formats
• 5 output formats supported
• System tray integration
• Batch processing
• Cross-platform support

© 2024 Beau Lewis. All rights reserved."""
        
        info_label = ttk.Label(content_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(pady=10)
        
        # Close button
        ttk.Button(content_frame, text="Close", 
                  command=about_window.destroy).pack(side=tk.BOTTOM, pady=10)
        
        about_window.mainloop()
    
    def show_error(self, title: str, message: str):
        """Show error dialog"""
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    
    def quit_app(self, icon=None, item=None):
        """Quit the tray application"""
        self.running = False
        if self.icon:
            self.icon.stop()
    
    def create_menu(self):
        """Create the system tray menu"""
        menu_items = [
            pystray.MenuItem("Open Quick Document Convertor", self.show_main_app, default=True),
        ]
        
        # Add quick convert if enabled
        if self.config.get("quick_convert_enabled", True):
            menu_items.append(pystray.MenuItem("Quick Convert File...", self.quick_convert_file))
        
        menu_items.extend([
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Settings", self.show_settings),
            pystray.MenuItem("About", self.show_about),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app)
        ])
        
        return pystray.Menu(*menu_items)
    
    def run(self):
        """Run the system tray application"""
        if not TRAY_AVAILABLE:
            self.show_error("System Tray Error", 
                          "System tray not available. Please install pystray and pillow:\n"
                          "pip install pystray pillow")
            return
        
        self.running = True
        
        # Create menu
        menu = self.create_menu()
        
        # Create icon
        icon_image = self.create_icon_image()
        self.icon = pystray.Icon("Quick Document Convertor", icon_image, menu=menu)
        
        # Show startup notification
        if self.config.get("show_notifications", True):
            # Delay notification to ensure tray is ready
            def show_startup_notification():
                import time
                time.sleep(2)
                self.show_notification("Quick Document Convertor", "System tray loaded")
            
            threading.Thread(target=show_startup_notification, daemon=True).start()
        
        # Run the icon
        try:
            self.icon.run()
        except Exception as e:
            self.show_error("Tray Error", f"System tray failed: {e}")

def main():
    """Main entry point"""
    # Check if already running
    if PSUTIL_AVAILABLE:
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if (proc.info['pid'] != current_pid and 
                    proc.info['name'] and 
                    'python' in proc.info['name'].lower() and
                    proc.info['cmdline'] and
                    any('tray_app' in arg for arg in proc.info['cmdline'])):
                    print("Tray application already running")
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    # Create and run tray application
    app = QuickConverterTray()
    app.run()

if __name__ == "__main__":
    main() 