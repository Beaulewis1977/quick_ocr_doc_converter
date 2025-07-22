#!/usr/bin/env python3
"""
OCR Settings GUI - Configuration interface for API keys and OCR backends
Provides a user-friendly interface for managing OCR settings and API credentials
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import threading

# Import OCR components
from ocr_engine.config_manager import ConfigManager


class OCRSettingsGUI:
    """GUI for managing OCR settings and API keys"""
    
    def __init__(self, parent=None, config_manager=None):
        """
        Initialize OCR Settings GUI
        
        Args:
            parent: Parent window (if None, creates standalone window)
            config_manager: Optional existing config manager
        """
        self.config_manager = config_manager or ConfigManager()
        self.logger = logging.getLogger("OCRSettingsGUI")
        
        # Create window
        if parent:
            self.window = tk.Toplevel(parent)
            self.window.transient(parent)
        else:
            self.window = tk.Tk()
        
        self.window.title("OCR Settings & API Configuration")
        self.window.geometry("800x700")
        self.window.minsize(600, 500)
        
        # State variables
        self.backend_status = {}
        self.test_results = {}
        
        # Create GUI
        self.create_widgets()
        self.load_settings()
        
        # Center window
        self.center_window()
        
        # Bind close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def center_window(self):
        """Center the window on the screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_backend_tab()
        self.create_google_vision_tab()
        self.create_processing_tab()
        self.create_security_tab()
        self.create_status_tab()
        
        # Create bottom frame with buttons
        self.create_bottom_frame()
    
    def create_backend_tab(self):
        """Create the backend selection tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="OCR Backends")
        
        # Default backend selection
        ttk.Label(frame, text="Default OCR Backend:", font=("TkDefaultFont", 10, "bold")).pack(
            anchor="w", padx=10, pady=(10, 5)
        )
        
        self.default_backend_var = tk.StringVar()
        backend_frame = ttk.Frame(frame)
        backend_frame.pack(fill="x", padx=10, pady=5)
        
        backends = [
            ("auto", "Auto (Best Available)"),
            ("tesseract", "Tesseract OCR"),
            ("easyocr", "EasyOCR"),
            ("google_vision", "Google Vision API")
        ]
        
        for value, text in backends:
            ttk.Radiobutton(
                backend_frame,
                text=text,
                variable=self.default_backend_var,
                value=value
            ).pack(anchor="w", pady=2)
        
        # Backend configuration
        ttk.Separator(frame, orient='horizontal').pack(fill="x", padx=10, pady=20)
        
        ttk.Label(frame, text="Backend Configuration:", font=("TkDefaultFont", 10, "bold")).pack(
            anchor="w", padx=10, pady=(0, 10)
        )
        
        # Tesseract settings
        tesseract_frame = ttk.LabelFrame(frame, text="Tesseract OCR", padding=10)
        tesseract_frame.pack(fill="x", padx=10, pady=5)
        
        self.tesseract_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(
            tesseract_frame,
            text="Enable Tesseract OCR",
            variable=self.tesseract_enabled_var
        ).pack(anchor="w")
        
        ttk.Label(tesseract_frame, text="Languages:").pack(anchor="w", pady=(10, 0))
        self.tesseract_languages_var = tk.StringVar(value="en")
        ttk.Entry(
            tesseract_frame,
            textvariable=self.tesseract_languages_var,
            width=40
        ).pack(anchor="w", pady=(5, 0))
        ttk.Label(tesseract_frame, text="(comma-separated, e.g., en,fr,de)", foreground="gray").pack(anchor="w")
        
        # EasyOCR settings
        easyocr_frame = ttk.LabelFrame(frame, text="EasyOCR", padding=10)
        easyocr_frame.pack(fill="x", padx=10, pady=5)
        
        self.easyocr_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(
            easyocr_frame,
            text="Enable EasyOCR",
            variable=self.easyocr_enabled_var
        ).pack(anchor="w")
        
        self.easyocr_gpu_var = tk.BooleanVar()
        ttk.Checkbutton(
            easyocr_frame,
            text="Use GPU acceleration (if available)",
            variable=self.easyocr_gpu_var
        ).pack(anchor="w", pady=(5, 0))
    
    def create_google_vision_tab(self):
        """Create the Google Vision API tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Google Vision API")
        
        # Enable/disable
        self.google_vision_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(
            frame,
            text="Enable Google Vision API",
            variable=self.google_vision_enabled_var,
            command=self.on_google_vision_toggle
        ).pack(anchor="w", padx=10, pady=10)
        
        # Instructions
        instructions = ttk.LabelFrame(frame, text="Setup Instructions", padding=10)
        instructions.pack(fill="x", padx=10, pady=10)
        
        instruction_text = """1. Go to Google Cloud Console (console.cloud.google.com)
2. Create a new project or select existing project
3. Enable the Vision API for your project
4. Create a service account key:
   • Go to IAM & Admin > Service Accounts
   • Create service account with Vision API permissions
   • Generate and download JSON key file
5. Upload the key file below or paste the JSON content"""
        
        ttk.Label(instructions, text=instruction_text, justify="left").pack(anchor="w")
        
        # API Key configuration
        api_config = ttk.LabelFrame(frame, text="API Configuration", padding=10)
        api_config.pack(fill="x", padx=10, pady=10)
        
        # Key file option
        key_file_frame = ttk.Frame(api_config)
        key_file_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(key_file_frame, text="Service Account Key File:").pack(anchor="w")
        
        key_input_frame = ttk.Frame(key_file_frame)
        key_input_frame.pack(fill="x", pady=(5, 0))
        
        self.key_file_var = tk.StringVar()
        self.key_file_entry = ttk.Entry(
            key_input_frame,
            textvariable=self.key_file_var,
            width=50
        )
        self.key_file_entry.pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            key_input_frame,
            text="Browse",
            command=self.browse_key_file
        ).pack(side="right", padx=(5, 0))
        
        # OR separator
        ttk.Separator(api_config, orient='horizontal').pack(fill="x", pady=10)
        ttk.Label(api_config, text="OR", font=("TkDefaultFont", 8)).pack()
        ttk.Separator(api_config, orient='horizontal').pack(fill="x", pady=(0, 10))
        
        # JSON key option
        ttk.Label(api_config, text="Paste Service Account JSON:").pack(anchor="w")
        
        self.json_text = scrolledtext.ScrolledText(
            api_config,
            height=8,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.json_text.pack(fill="both", expand=True, pady=(5, 0))
        
        # Test connection button
        test_frame = ttk.Frame(api_config)
        test_frame.pack(fill="x", pady=(10, 0))
        
        self.test_button = ttk.Button(
            test_frame,
            text="Test Connection",
            command=self.test_google_vision
        )
        self.test_button.pack(side="left")
        
        self.test_status_label = ttk.Label(test_frame, text="")
        self.test_status_label.pack(side="left", padx=(10, 0))
    
    def create_processing_tab(self):
        """Create the processing settings tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Processing")
        
        # Cache settings
        cache_frame = ttk.LabelFrame(frame, text="Cache Settings", padding=10)
        cache_frame.pack(fill="x", padx=10, pady=10)
        
        self.use_cache_var = tk.BooleanVar()
        ttk.Checkbutton(
            cache_frame,
            text="Enable OCR result caching",
            variable=self.use_cache_var
        ).pack(anchor="w")
        
        ttk.Label(cache_frame, text="Cache TTL (hours):").pack(anchor="w", pady=(10, 0))
        self.cache_ttl_var = tk.IntVar(value=24)
        ttk.Spinbox(
            cache_frame,
            from_=1,
            to=168,
            textvariable=self.cache_ttl_var,
            width=10
        ).pack(anchor="w", pady=(5, 0))
        
        # Performance settings
        perf_frame = ttk.LabelFrame(frame, text="Performance Settings", padding=10)
        perf_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(perf_frame, text="Maximum concurrent workers:").pack(anchor="w")
        self.max_workers_var = tk.IntVar(value=2)
        ttk.Spinbox(
            perf_frame,
            from_=1,
            to=8,
            textvariable=self.max_workers_var,
            width=10
        ).pack(anchor="w", pady=(5, 0))
        
        # Image preprocessing
        preproc_frame = ttk.LabelFrame(frame, text="Image Preprocessing", padding=10)
        preproc_frame.pack(fill="x", padx=10, pady=10)
        
        self.enhance_contrast_var = tk.BooleanVar()
        ttk.Checkbutton(
            preproc_frame,
            text="Enhance image contrast",
            variable=self.enhance_contrast_var
        ).pack(anchor="w")
        
        self.denoise_var = tk.BooleanVar()
        ttk.Checkbutton(
            preproc_frame,
            text="Apply noise reduction",
            variable=self.denoise_var
        ).pack(anchor="w")
        
        ttk.Label(preproc_frame, text="Maximum image size (pixels):").pack(anchor="w", pady=(10, 0))
        self.resize_max_var = tk.IntVar(value=2048)
        ttk.Spinbox(
            preproc_frame,
            from_=512,
            to=8192,
            increment=256,
            textvariable=self.resize_max_var,
            width=10
        ).pack(anchor="w", pady=(5, 0))
    
    def create_security_tab(self):
        """Create the security settings tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Security")
        
        # Encryption settings
        encryption_frame = ttk.LabelFrame(frame, text="Encryption", padding=10)
        encryption_frame.pack(fill="x", padx=10, pady=10)
        
        self.encrypt_api_keys_var = tk.BooleanVar()
        ttk.Checkbutton(
            encryption_frame,
            text="Encrypt API keys in configuration files",
            variable=self.encrypt_api_keys_var
        ).pack(anchor="w")
        
        ttk.Label(
            encryption_frame,
            text="(Recommended for security, uses local encryption key)",
            foreground="gray"
        ).pack(anchor="w")
        
        # File size limits
        limits_frame = ttk.LabelFrame(frame, text="File Limits", padding=10)
        limits_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(limits_frame, text="Maximum file size (MB):").pack(anchor="w")
        self.max_file_size_var = tk.IntVar(value=50)
        ttk.Spinbox(
            limits_frame,
            from_=1,
            to=500,
            textvariable=self.max_file_size_var,
            width=10
        ).pack(anchor="w", pady=(5, 0))
        
        # Allowed extensions
        ttk.Label(limits_frame, text="Allowed file extensions:").pack(anchor="w", pady=(10, 0))
        self.allowed_extensions_var = tk.StringVar(value=".jpg,.jpeg,.png,.tiff,.tif,.bmp,.gif,.webp")
        ttk.Entry(
            limits_frame,
            textvariable=self.allowed_extensions_var,
            width=60
        ).pack(anchor="w", pady=(5, 0))
    
    def create_status_tab(self):
        """Create the status and diagnostics tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Status")
        
        # Backend status
        status_frame = ttk.LabelFrame(frame, text="Backend Status", padding=10)
        status_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            height=15,
            wrap=tk.WORD,
            font=("Courier", 9)
        )
        self.status_text.pack(fill="both", expand=True)
        
        # Refresh button
        ttk.Button(
            status_frame,
            text="Refresh Status",
            command=self.refresh_status
        ).pack(pady=(10, 0))
    
    def create_bottom_frame(self):
        """Create the bottom frame with action buttons"""
        frame = ttk.Frame(self.window)
        frame.pack(fill="x", padx=10, pady=10)
        
        # Left side buttons
        left_frame = ttk.Frame(frame)
        left_frame.pack(side="left")
        
        ttk.Button(
            left_frame,
            text="Import Config",
            command=self.import_config
        ).pack(side="left", padx=(0, 5))
        
        ttk.Button(
            left_frame,
            text="Export Config",
            command=self.export_config
        ).pack(side="left", padx=5)
        
        ttk.Button(
            left_frame,
            text="Reset to Defaults",
            command=self.reset_to_defaults
        ).pack(side="left", padx=5)
        
        # Right side buttons
        right_frame = ttk.Frame(frame)
        right_frame.pack(side="right")
        
        ttk.Button(
            right_frame,
            text="Cancel",
            command=self.cancel
        ).pack(side="right", padx=(5, 0))
        
        ttk.Button(
            right_frame,
            text="Apply",
            command=self.apply_settings
        ).pack(side="right", padx=5)
        
        ttk.Button(
            right_frame,
            text="OK",
            command=self.save_and_close
        ).pack(side="right", padx=5)
    
    def load_settings(self):
        """Load settings from config manager"""
        config = self.config_manager.config
        
        # Backend settings
        backends = config.get("ocr_backends", {})
        self.default_backend_var.set(backends.get("default_backend", "auto"))
        
        # Tesseract
        tesseract_config = backends.get("tesseract", {})
        self.tesseract_enabled_var.set(tesseract_config.get("enabled", True))
        self.tesseract_languages_var.set(",".join(tesseract_config.get("languages", ["en"])))
        
        # EasyOCR
        easyocr_config = backends.get("easyocr", {})
        self.easyocr_enabled_var.set(easyocr_config.get("enabled", True))
        self.easyocr_gpu_var.set(easyocr_config.get("gpu", False))
        
        # Google Vision
        google_config = backends.get("google_vision", {})
        self.google_vision_enabled_var.set(google_config.get("enabled", False))
        self.key_file_var.set(google_config.get("key_file", ""))
        self.json_text.delete(1.0, tk.END)
        if google_config.get("key_json"):
            self.json_text.insert(1.0, google_config.get("key_json", ""))
        
        # Processing settings
        processing = config.get("processing", {})
        self.use_cache_var.set(processing.get("use_cache", True))
        self.cache_ttl_var.set(processing.get("cache_ttl", 86400) // 3600)  # Convert to hours
        self.max_workers_var.set(processing.get("max_workers", 2))
        
        preprocessing = processing.get("preprocessing", {})
        self.enhance_contrast_var.set(preprocessing.get("enhance_contrast", True))
        self.denoise_var.set(preprocessing.get("denoise", True))
        self.resize_max_var.set(preprocessing.get("resize_max", 2048))
        
        # Security settings
        security = config.get("security", {})
        self.encrypt_api_keys_var.set(security.get("encrypt_api_keys", True))
        self.max_file_size_var.set(security.get("max_file_size_mb", 50))
        extensions = security.get("allowed_extensions", [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".gif", ".webp"])
        self.allowed_extensions_var.set(",".join(extensions))
        
        # Refresh status
        self.refresh_status()
    
    def save_settings(self):
        """Save settings to config manager"""
        config = self.config_manager.config
        
        # Backend settings
        if "ocr_backends" not in config:
            config["ocr_backends"] = {}
        
        backends = config["ocr_backends"]
        backends["default_backend"] = self.default_backend_var.get()
        
        # Tesseract
        backends["tesseract"] = {
            "enabled": self.tesseract_enabled_var.get(),
            "languages": [lang.strip() for lang in self.tesseract_languages_var.get().split(",") if lang.strip()],
            "config": "--oem 3 --psm 6",
            "confidence_threshold": 30
        }
        
        # EasyOCR
        backends["easyocr"] = {
            "enabled": self.easyocr_enabled_var.get(),
            "languages": ["en"],  # Could be made configurable
            "gpu": self.easyocr_gpu_var.get(),
            "confidence_threshold": 30
        }
        
        # Google Vision
        json_content = self.json_text.get(1.0, tk.END).strip()
        backends["google_vision"] = {
            "enabled": self.google_vision_enabled_var.get(),
            "key_file": self.key_file_var.get(),
            "key_json": json_content if json_content else "",
            "languages": ["en"],
            "confidence_threshold": 30
        }
        
        # Processing settings
        config["processing"] = {
            "use_cache": self.use_cache_var.get(),
            "cache_ttl": self.cache_ttl_var.get() * 3600,  # Convert to seconds
            "max_workers": self.max_workers_var.get(),
            "preprocessing": {
                "enhance_contrast": self.enhance_contrast_var.get(),
                "denoise": self.denoise_var.get(),
                "resize_max": self.resize_max_var.get(),
                "threshold_method": "adaptive"
            }
        }
        
        # Security settings
        extensions = [ext.strip() for ext in self.allowed_extensions_var.get().split(",") if ext.strip()]
        config["security"] = {
            "encrypt_api_keys": self.encrypt_api_keys_var.get(),
            "max_file_size_mb": self.max_file_size_var.get(),
            "allowed_extensions": extensions
        }
        
        # Save configuration
        return self.config_manager.save_config(config)
    
    def browse_key_file(self):
        """Browse for Google Vision API key file"""
        filename = filedialog.askopenfilename(
            title="Select Google Vision API Key File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.key_file_var.set(filename)
            # Clear JSON text when file is selected
            self.json_text.delete(1.0, tk.END)
    
    def on_google_vision_toggle(self):
        """Handle Google Vision enable/disable toggle"""
        enabled = self.google_vision_enabled_var.get()
        # Could add logic to enable/disable related widgets
        pass
    
    def test_google_vision(self):
        """Test Google Vision API connection"""
        self.test_button.config(state="disabled")
        self.test_status_label.config(text="Testing...", foreground="blue")
        
        def run_test():
            try:
                # Temporarily save current Google Vision settings
                json_content = self.json_text.get(1.0, tk.END).strip()
                temp_config = {
                    "key_file": self.key_file_var.get(),
                    "key_json": json_content if json_content else "",
                    "enabled": True
                }
                
                # Create temporary backend for testing
                from ocr_engine.google_vision_backend import GoogleVisionBackend
                backend = GoogleVisionBackend(temp_config)
                
                if not backend.is_available():
                    self.window.after(0, lambda: self.test_status_label.config(
                        text="❌ Not configured", foreground="red"
                    ))
                    return
                
                result = backend.test_connection()
                
                if result.get("success"):
                    self.window.after(0, lambda: self.test_status_label.config(
                        text="✅ Connection successful", foreground="green"
                    ))
                else:
                    error_msg = result.get("error", "Unknown error")
                    self.window.after(0, lambda: self.test_status_label.config(
                        text=f"❌ {error_msg}", foreground="red"
                    ))
                    
            except Exception as e:
                self.window.after(0, lambda: self.test_status_label.config(
                    text=f"❌ Error: {str(e)}", foreground="red"
                ))
            finally:
                self.window.after(0, lambda: self.test_button.config(state="normal"))
        
        # Run test in separate thread
        threading.Thread(target=run_test, daemon=True).start()
    
    def refresh_status(self):
        """Refresh the status display"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "Checking backend status...\n\n")
        
        def update_status():
            try:
                status = self.config_manager.get_all_backend_status()
                
                status_report = "OCR Backend Status Report\n"
                status_report += "=" * 50 + "\n\n"
                
                for backend_name, info in status.items():
                    status_report += f"{backend_name.upper()}:\n"
                    status_report += f"  Available: {'✅ Yes' if info.get('available') else '❌ No'}\n"
                    status_report += f"  Enabled: {'✅ Yes' if info.get('enabled') else '❌ No'}\n"
                    
                    if info.get('version'):
                        status_report += f"  Version: {info['version']}\n"
                    if info.get('error'):
                        status_report += f"  Error: {info['error']}\n"
                    if info.get('test_result'):
                        test = info['test_result']
                        if test.get('success'):
                            status_report += f"  Test: ✅ Connection successful\n"
                        else:
                            status_report += f"  Test: ❌ {test.get('error', 'Failed')}\n"
                    
                    status_report += "\n"
                
                # Configuration summary
                summary = self.config_manager.get_config_summary()
                status_report += "Configuration Summary:\n"
                status_report += "-" * 30 + "\n"
                status_report += f"Default Backend: {summary['default_backend']}\n"
                status_report += f"Enabled Backends: {', '.join(summary['enabled_backends'])}\n"
                status_report += f"Cache Enabled: {'Yes' if summary['cache_enabled'] else 'No'}\n"
                status_report += f"Encryption Enabled: {'Yes' if summary['encryption_enabled'] else 'No'}\n"
                status_report += f"Config File Exists: {'Yes' if summary['config_file_exists'] else 'No'}\n"
                
                self.window.after(0, lambda: self.status_text.delete(1.0, tk.END))
                self.window.after(0, lambda: self.status_text.insert(1.0, status_report))
                
            except Exception as e:
                error_msg = f"Error checking status: {str(e)}"
                self.window.after(0, lambda: self.status_text.delete(1.0, tk.END))
                self.window.after(0, lambda: self.status_text.insert(1.0, error_msg))
        
        # Run in separate thread
        threading.Thread(target=update_status, daemon=True).start()
    
    def import_config(self):
        """Import configuration from file"""
        filename = filedialog.askopenfilename(
            title="Import Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            if self.config_manager.import_config(Path(filename)):
                messagebox.showinfo("Success", "Configuration imported successfully!")
                self.load_settings()
            else:
                messagebox.showerror("Error", "Failed to import configuration.")
    
    def export_config(self):
        """Export configuration to file"""
        filename = filedialog.asksaveasfilename(
            title="Export Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            include_keys = messagebox.askyesno(
                "Include API Keys",
                "Include API keys in the exported configuration?\n\n"
                "Choose 'No' if sharing the configuration file."
            )
            if self.config_manager.export_config(Path(filename), include_keys):
                messagebox.showinfo("Success", "Configuration exported successfully!")
            else:
                messagebox.showerror("Error", "Failed to export configuration.")
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno(
            "Reset to Defaults",
            "This will reset all settings to their default values.\n"
            "API keys and custom settings will be lost.\n\n"
            "Continue?"
        ):
            if self.config_manager.reset_to_defaults():
                messagebox.showinfo("Success", "Configuration reset to defaults!")
                self.load_settings()
            else:
                messagebox.showerror("Error", "Failed to reset configuration.")
    
    def apply_settings(self):
        """Apply settings without closing"""
        if self.save_settings():
            messagebox.showinfo("Success", "Settings applied successfully!")
            self.refresh_status()
        else:
            messagebox.showerror("Error", "Failed to save settings.")
    
    def save_and_close(self):
        """Save settings and close window"""
        if self.save_settings():
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Failed to save settings.")
    
    def cancel(self):
        """Cancel without saving"""
        if messagebox.askyesno("Cancel", "Close without saving changes?"):
            self.window.destroy()
    
    def on_close(self):
        """Handle window close event"""
        self.cancel()
    
    def show(self):
        """Show the settings window"""
        self.window.lift()
        self.window.focus_force()
        return self.window


def main():
    """Run the OCR Settings GUI standalone"""
    logging.basicConfig(level=logging.INFO)
    
    app = OCRSettingsGUI()
    app.window.mainloop()


if __name__ == "__main__":
    main()