#!/usr/bin/env python3
"""
OCR GUI Integration Module for Quick Document Convertor
Integrates OCR functionality with the existing GUI application
Author: Beau Lewis (blewisxx@gmail.com)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import sys
from typing import List, Dict, Any, Optional

# Import OCR components
from ocr_engine.ocr_integration import OCRIntegration
from ocr_engine.format_detector import OCRFormatDetector

class OCRGUIIntegration:
    """Integrates OCR functionality into the existing GUI"""
    
    def __init__(self, parent_gui, config_manager=None):
        self.parent_gui = parent_gui
        self.config_manager = config_manager
        self.ocr_integration = OCRIntegration()
        self.is_ocr_mode = False
        
    def check_ocr_availability(self) -> Dict[str, Any]:
        """Check if OCR functionality is available"""
        return self.ocr_integration.check_availability()
    
    def create_ocr_widgets(self, parent_frame):
        """Create OCR-specific GUI widgets"""
        # OCR Mode Toggle Frame
        ocr_frame = ttk.LabelFrame(parent_frame, text="🔍 OCR Mode", padding="10")
        ocr_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # OCR Mode Toggle
        self.ocr_mode_var = tk.BooleanVar(value=False)
        self.ocr_toggle = ttk.Checkbutton(
            ocr_frame, 
            text="Enable OCR Mode (Image to Text)",
            variable=self.ocr_mode_var,
            command=self.toggle_ocr_mode
        )
        self.ocr_toggle.grid(row=0, column=0, sticky=tk.W)
        
        # OCR Settings Frame (initially hidden)
        self.ocr_settings_frame = ttk.Frame(ocr_frame)
        self.ocr_settings_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # OCR Backend Selection
        ttk.Label(self.ocr_settings_frame, text="OCR Engine:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.ocr_backend_var = tk.StringVar(value="auto")
        backends = self.get_available_backends()
        self.backend_combo = ttk.Combobox(
            self.ocr_settings_frame,
            textvariable=self.ocr_backend_var,
            values=backends,
            state='readonly',
            width=15
        )
        self.backend_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # OCR Output Format
        ttk.Label(self.ocr_settings_frame, text="Output Format:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.ocr_output_format_var = tk.StringVar(value="txt")
        output_formats = ["txt", "json", "markdown"]
        self.output_format_combo = ttk.Combobox(
            self.ocr_settings_frame,
            textvariable=self.ocr_output_format_var,
            values=output_formats,
            state='readonly',
            width=10
        )
        self.output_format_combo.grid(row=0, column=3, sticky=tk.W)
        
        # OCR Language Selection
        ttk.Label(self.ocr_settings_frame, text="Language:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0), padx=(0, 10))
        self.ocr_language_var = tk.StringVar(value="eng")
        languages = ["eng", "eng+fra", "eng+spa", "eng+deu"]
        self.language_combo = ttk.Combobox(
            self.ocr_settings_frame,
            textvariable=self.ocr_language_var,
            values=languages,
            state='readonly',
            width=15
        )
        self.language_combo.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # OCR Quality Settings
        ttk.Label(self.ocr_settings_frame, text="Quality:").grid(row=1, column=2, sticky=tk.W, pady=(5, 0), padx=(0, 10))
        self.ocr_quality_var = tk.StringVar(value="standard")
        qualities = ["fast", "standard", "accurate"]
        self.quality_combo = ttk.Combobox(
            self.ocr_settings_frame,
            textvariable=self.ocr_quality_var,
            values=qualities,
            state='readonly',
            width=10
        )
        self.quality_combo.grid(row=1, column=3, sticky=tk.W, pady=(5, 0))
        
        # Hide settings initially
        self.ocr_settings_frame.grid_remove()
        
        return ocr_frame
    
    def get_available_backends(self) -> List[str]:
        """Get list of available OCR backends"""
        availability = self.check_ocr_availability()
        backends = availability.get('backends', [])
        return ['auto'] + backends
    
    def toggle_ocr_mode(self):
        """Toggle between OCR mode and regular conversion mode"""
        self.is_ocr_mode = self.ocr_mode_var.get()
        
        if self.is_ocr_mode:
            self.ocr_settings_frame.grid()
            self.update_parent_gui_for_ocr()
        else:
            self.ocr_settings_frame.grid_remove()
            self.restore_parent_gui()
    
    def update_parent_gui_for_ocr(self):
        """Update parent GUI for OCR mode"""
        # Update format selection to show image formats
        if hasattr(self.parent_gui, 'input_format_combo'):
            self.parent_gui.input_format_combo.configure(values=['auto'])
            self.parent_gui.input_format.set('auto')
        
        # Update supported file types in file browser
        self.update_file_types_for_ocr()
        
        # Update button text
        if hasattr(self.parent_gui, 'convert_button'):
            self.parent_gui.convert_button.configure(text="🔍 Extract Text from Images")
    
    def restore_parent_gui(self):
        """Restore parent GUI to regular mode"""
        # Restore original format selection
        if hasattr(self.parent_gui, 'input_format_combo'):
            from universal_document_converter import FormatDetector
            input_formats = FormatDetector.get_input_format_list()
            self.parent_gui.input_format_combo.configure(values=[f[1] for f in input_formats])
        
        # Restore original button text
        if hasattr(self.parent_gui, 'convert_button'):
            self.parent_gui.convert_button.configure(text="🚀 Convert Documents")
    
    def update_file_types_for_ocr(self):
        """Update file types for OCR mode"""
        # This will be handled in the browse methods
        pass
    
    def get_ocr_config(self) -> Dict[str, Any]:
        """Get OCR configuration based on GUI settings"""
        quality_map = {
            'fast': {'confidence_threshold': 20, 'preprocessing': {'enhance_contrast': False}},
            'standard': {'confidence_threshold': 30, 'preprocessing': {'enhance_contrast': True}},
            'accurate': {'confidence_threshold': 50, 'preprocessing': {'enhance_contrast': True, 'denoise': True}}
        }
        
        config = {
            'backend': self.ocr_backend_var.get(),
            'languages': self.ocr_language_var.get().split('+'),
            'use_cache': True,
            'output_format': self.ocr_output_format_var.get()
        }
        
        # Add quality settings
        quality = self.ocr_quality_var.get()
        if quality in quality_map:
            config.update(quality_map[quality])
        
        return config
    
    def process_ocr_files(self, file_paths: List[str], output_dir: str, 
                         progress_callback=None) -> Dict[str, Any]:
        """Process files with OCR"""
        try:
            config = self.get_ocr_config()
            return self.ocr_integration.process_files(
                file_paths=file_paths,
                output_dir=output_dir,
                output_format=config['output_format'],
                max_workers=self.parent_gui.max_workers.get() if hasattr(self.parent_gui, 'max_workers') else 2,
                progress_callback=progress_callback
            )
        except Exception as e:
            return {
                'successful': 0,
                'failed': len(file_paths),
                'skipped': 0,
                'results': [],
                'duration': 0,
                'message': f"OCR processing failed: {str(e)}"
            }
    
    def get_supported_image_extensions(self) -> List[str]:
        """Get list of supported image extensions for OCR"""
        return list(OCRFormatDetector.get_supported_extensions())

class OCRSettingsDialog:
    """Advanced OCR settings dialog"""
    
    def __init__(self, parent, ocr_gui):
        self.parent = parent
        self.ocr_gui = ocr_gui
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("OCR Settings")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.center_dialog()
    
    def setup_ui(self):
        """Setup OCR settings UI"""
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # OCR Engine Settings
        engine_frame = ttk.LabelFrame(main_frame, text="OCR Engine", padding="10")
        engine_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        availability = self.ocr_gui.check_ocr_availability()
        
        ttk.Label(engine_frame, text=f"Status: {availability['message']}").grid(row=0, column=0, sticky=tk.W)
        
        # Cache Management
        cache_frame = ttk.LabelFrame(main_frame, text="Cache Management", padding="10")
        cache_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(cache_frame, text="Clear OCR Cache", 
                  command=self.clear_cache).grid(row=0, column=0, sticky=tk.W)
        
        # Cache Stats
        try:
            cache_stats = self.ocr_gui.ocr_integration.ocr_engine.get_cache_stats()
            if 'error' not in cache_stats:
                ttk.Label(cache_frame, 
                         text=f"Cache: {cache_stats['file_count']} files, {cache_stats['total_size_mb']} MB").grid(
                    row=1, column=0, sticky=tk.W, pady=(5, 0))
        except:
            pass
    
    def center_dialog(self):
        """Center the dialog"""
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def clear_cache(self):
        """Clear OCR cache"""
        try:
            success = self.ocr_gui.ocr_integration.ocr_engine.clear_cache()
            if success:
                messagebox.showinfo("Success", "OCR cache cleared successfully")
            else:
                messagebox.showerror("Error", "Failed to clear cache")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear cache: {str(e)}")