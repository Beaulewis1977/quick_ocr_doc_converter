#!/usr/bin/env python3
"""
Universal Document Converter Bidirectional - Fixed Version
Complete document conversion tool with proper bidirectional support
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Import the base converter
from universal_document_converter_complete import (
    DocumentConverterApp, ConfigurationManager,
    FileProcessingError, OCR_AVAILABLE
)

# Optional imports with fallbacks
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import markdown2
    MARKDOWN2_AVAILABLE = True
except ImportError:
    MARKDOWN2_AVAILABLE = False

class BidirectionalDocumentConverter(DocumentConverterApp):
    """Extended converter with bidirectional support"""
    
    def __init__(self, root):
        # Add output format variable before parent init
        self.output_format_var = tk.StringVar(value="markdown")
        
        # Initialize parent class
        super().__init__(root)
        
        # Update title
        self.root.title("Universal Document Converter - Bidirectional Edition")
        
        # Update supported formats
        self.input_formats = {
            'documents': ['*.docx', '*.pdf', '*.txt', '*.md', '*.rtf', '*.odt', 
                         '*.html', '*.htm', '*.epub', '*.xml', '*.json', '*.csv'],
            'images': ['*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif', '*.bmp', 
                      '*.gif', '*.webp']
        }
        
        self.output_formats = {
            'markdown': {'ext': '.md', 'name': 'Markdown'},
            'text': {'ext': '.txt', 'name': 'Plain Text'},
            'docx': {'ext': '.docx', 'name': 'Word Document'},
            'pdf': {'ext': '.pdf', 'name': 'PDF'},
            'html': {'ext': '.html', 'name': 'HTML'},
            'rtf': {'ext': '.rtf', 'name': 'Rich Text Format'}
        }
    
    def create_settings_section(self, parent):
        """Override to add output format selector"""
        # Call parent method first
        super().create_settings_section(parent)
        
        # Add output format selector
        format_frame = ttk.LabelFrame(parent, text="Output Format", padding=10)
        format_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(format_frame, text="Convert to:").pack(side=tk.LEFT, padx=5)
        
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.output_format_var,
            values=[fmt['name'] for fmt in self.output_formats.values()],
            state='readonly',
            width=20
        )
        format_combo.pack(side=tk.LEFT, padx=5)
        
        # Update combo to use format keys
        format_combo['values'] = list(self.output_formats.keys())
        
        # Bind change event
        format_combo.bind('<<ComboboxSelected>>', self.on_format_change)
        
        # Add info label
        self.format_info_label = ttk.Label(format_frame, text="", foreground='blue')
        self.format_info_label.pack(side=tk.LEFT, padx=10)
        
        self.on_format_change()  # Initialize
    
    def on_format_change(self, event=None):
        """Handle output format change"""
        format_name = self.output_format_var.get()
        format_info = self.output_formats.get(format_name, {})
        
        # Update info label
        info_text = f"Output: {format_info.get('ext', '.?')}"
        
        # Check dependencies
        if format_name == 'pdf' and not REPORTLAB_AVAILABLE:
            info_text += " (⚠️ reportlab required)"
        elif format_name == 'docx' and not DOCX_AVAILABLE:
            info_text += " (⚠️ python-docx required)"
        
        self.format_info_label.config(text=info_text)
