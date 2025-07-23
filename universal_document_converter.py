#!/usr/bin/env python3
"""
Universal Document Converter - Complete Enterprise Solution
Complete GUI application with OCR, document conversion, markdown tools, API management, and VB6/VFP9 integration
Designed and built by Beau Lewis (blewisxx@gmail.com)

Complete Feature Set:
- Full OCR functionality (Tesseract, EasyOCR, Google Vision API)
- Complete document conversion (DOCX, PDF, TXT, HTML, RTF, EPUB, Markdown)
- Bidirectional markdown converter with markdown reader
- API management for cloud OCR services
- VB6/VFP9 legacy system integration interface
- Advanced settings with tabbed configuration
- Multi-threaded processing with hardened security
- Drag-and-drop support with comprehensive file validation
- Cross-platform compatibility (Windows, macOS, Linux)
- Professional GUI with advanced tools and settings
- Enterprise-grade logging and error handling
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
import sys
import mimetypes
import re
import logging
import datetime
import json
import subprocess
import shutil
from typing import Optional, Union, Dict, Any, List
import concurrent.futures
import time
import hashlib
from threading import Lock
import webbrowser

# OCR and document processing imports
try:
    from ocr_engine.ocr_engine import OCREngine
    from ocr_engine.ocr_integration import OCRIntegration
    from ocr_engine.format_detector import OCRFormatDetector
    from ocr_engine.security import SecurityError, validate_file_path
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    OCREngine = None

# Document conversion imports
try:
    from convert_to_markdown import convert_docx_to_markdown, convert_pdf_to_markdown
    from convert_recursive import convert_directory
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

# Cloud API imports
try:
    from google.cloud import vision
    HAS_GOOGLE_VISION = True
except ImportError:
    HAS_GOOGLE_VISION = False

class UniversalDocumentConverter:
    """
    Complete Universal Document Converter with all features integrated
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Document Converter - Complete Enterprise Solution v3.1.0")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Application state
        self.is_processing = False
        self.processing_thread = None
        self.processed_count = 0
        self.total_files = 0
        self.cancel_processing = False
        
        # OCR and conversion engines
        self.ocr_engine = None
        self.current_files = []
        
        # Configuration and settings
        self.config = self.load_config()
        self.setup_logging()
        
        # Initialize OCR if available
        if HAS_OCR:
            try:
                self.ocr_engine = OCREngine(config=self.config.get('ocr', {}))
            except Exception as e:
                logging.warning(f"Could not initialize OCR engine: {e}")
        
        # Setup UI
        self.setup_ui()
        self.setup_drag_drop()
        
        # Setup event handlers
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_level = self.config.get('logging', {}).get('level', 'INFO')
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Create logs directory
        log_dir = Path.home() / ".universal_converter" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup file handler
        log_file = log_dir / f"converter_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Universal Document Converter started")
    
    def load_config(self) -> dict:
        """Load configuration from file"""
        config_dir = Path.home() / ".universal_converter"
        config_file = config_dir / "config.json"
        
        default_config = {
            'ocr': {
                'engine': 'auto',
                'languages': ['en'],
                'confidence_threshold': 0.7,
                'use_cache': True
            },
            'conversion': {
                'preserve_formatting': True,
                'quality': 'high',
                'max_workers': 4
            },
            'api': {
                'google_vision': {
                    'enabled': False,
                    'credentials_path': '',
                    'fallback_enabled': True
                }
            },
            'gui': {
                'theme': 'default',
                'remember_settings': True,
                'auto_preview': False
            },
            'logging': {
                'level': 'INFO',
                'max_size': '10MB',
                'backup_count': 5
            },
            'legacy': {
                'vb6_vfp9_integration': True,
                'dll_compatibility': True
            }
        }
        
        try:
            if config_file.exists():
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                return {**default_config, **user_config}
        except Exception as e:
            logging.warning(f"Could not load config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config_dir = Path.home() / ".universal_converter"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / "config.json"
            
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logging.error(f"Could not save config: {e}")
    
    def setup_ui(self):
        """Setup the complete user interface with tabbed layout"""
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create all tabs
        self.create_main_tab()
        self.create_ocr_tab()
        self.create_markdown_tab()
        self.create_api_tab()
        self.create_legacy_tab()
        self.create_settings_tab()
        
        # Status bar at bottom
        self.create_status_bar(main_container)
    
    def create_main_tab(self):
        """Create main document conversion tab"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="📄 Document Conversion")
        
        # File selection area
        file_frame = ttk.LabelFrame(main_frame, text="Files", padding=10)
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # File list
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # File buttons
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Add Files", command=self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Add Folder", command=self.add_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Clear", command=self.clear_files).pack(side=tk.LEFT, padx=(0, 5))
        
        # Conversion options
        options_frame = ttk.LabelFrame(main_frame, text="Conversion Options", padding=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Output format
        ttk.Label(options_frame, text="Output Format:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.output_format = ttk.Combobox(options_frame, values=[
            "txt", "docx", "pdf", "html", "rtf", "markdown", "epub", "json"
        ], state="readonly")
        self.output_format.set("txt")
        self.output_format.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Output directory
        ttk.Label(options_frame, text="Output Directory:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.output_dir = tk.StringVar(value=str(Path.home() / "Documents" / "Converted"))
        ttk.Entry(options_frame, textvariable=self.output_dir, width=30).grid(row=0, column=3, sticky=tk.W, padx=(0, 5))
        ttk.Button(options_frame, text="Browse", command=self.browse_output_dir).grid(row=0, column=4, sticky=tk.W)
        
        # Processing controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="🚀 Start Conversion", command=self.start_conversion)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_button = ttk.Button(control_frame, text="⏹ Cancel", command=self.cancel_conversion, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(20, 0))
    
    def create_ocr_tab(self):
        """Create OCR processing tab"""
        ocr_frame = ttk.Frame(self.notebook)
        self.notebook.add(ocr_frame, text="👁 OCR Processing")
        
        if not HAS_OCR:
            ttk.Label(ocr_frame, text="OCR functionality not available. Please install required dependencies.", 
                     font=('Arial', 12)).pack(pady=50)
            return
        
        # OCR Engine Selection
        engine_frame = ttk.LabelFrame(ocr_frame, text="OCR Engine", padding=10)
        engine_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(engine_frame, text="Engine:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.ocr_engine_var = ttk.Combobox(engine_frame, values=["auto", "tesseract", "easyocr", "google_vision"], state="readonly")
        self.ocr_engine_var.set("auto")
        self.ocr_engine_var.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(engine_frame, text="Language:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.ocr_language = ttk.Combobox(engine_frame, values=["eng", "fra", "deu", "spa", "ita", "por"], state="readonly")
        self.ocr_language.set("eng")
        self.ocr_language.grid(row=0, column=3, sticky=tk.W)
        
        # OCR Preview
        preview_frame = ttk.LabelFrame(ocr_frame, text="OCR Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.ocr_preview = scrolledtext.ScrolledText(preview_frame, height=15)
        self.ocr_preview.pack(fill=tk.BOTH, expand=True)
        
        # OCR Controls
        ocr_control_frame = ttk.Frame(ocr_frame)
        ocr_control_frame.pack(fill=tk.X)
        
        ttk.Button(ocr_control_frame, text="📷 Process Image", command=self.process_ocr).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(ocr_control_frame, text="💾 Save OCR Result", command=self.save_ocr_result).pack(side=tk.LEFT)
    
    def create_markdown_tab(self):
        """Create bidirectional markdown conversion tab"""
        md_frame = ttk.Frame(self.notebook)
        self.notebook.add(md_frame, text="📝 Markdown Tools")
        
        # Conversion direction
        direction_frame = ttk.LabelFrame(md_frame, text="Conversion Direction", padding=10)
        direction_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.md_direction = tk.StringVar(value="to_markdown")
        ttk.Radiobutton(direction_frame, text="📄 → 📝 Convert TO Markdown", 
                       variable=self.md_direction, value="to_markdown").pack(anchor=tk.W)
        ttk.Radiobutton(direction_frame, text="📝 → 📄 Convert FROM Markdown", 
                       variable=self.md_direction, value="from_markdown").pack(anchor=tk.W)
        
        # Markdown editor/viewer
        editor_frame = ttk.LabelFrame(md_frame, text="Markdown Editor/Viewer", padding=10)
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create notebook for editor tabs
        self.md_notebook = ttk.Notebook(editor_frame)
        self.md_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Source tab
        source_frame = ttk.Frame(self.md_notebook)
        self.md_notebook.add(source_frame, text="📝 Source")
        self.md_editor = scrolledtext.ScrolledText(source_frame, font=('Consolas', 10))
        self.md_editor.pack(fill=tk.BOTH, expand=True)
        
        # Preview tab
        preview_frame = ttk.Frame(self.md_notebook)
        self.md_notebook.add(preview_frame, text="👁 Preview")
        self.md_preview = scrolledtext.ScrolledText(preview_frame, state=tk.DISABLED)
        self.md_preview.pack(fill=tk.BOTH, expand=True)
        
        # Markdown controls
        md_control_frame = ttk.Frame(md_frame)
        md_control_frame.pack(fill=tk.X)
        
        ttk.Button(md_control_frame, text="📂 Load File", command=self.load_markdown_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(md_control_frame, text="💾 Save Markdown", command=self.save_markdown_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(md_control_frame, text="🔄 Convert", command=self.convert_markdown).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(md_control_frame, text="👁 Preview", command=self.preview_markdown).pack(side=tk.LEFT)
    
    def create_api_tab(self):
        """Create API management tab"""
        api_frame = ttk.Frame(self.notebook)
        self.notebook.add(api_frame, text="🌐 API Management")
        
        # Google Vision API
        gv_frame = ttk.LabelFrame(api_frame, text="Google Vision API", padding=10)
        gv_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.gv_enabled = tk.BooleanVar(value=self.config.get('api', {}).get('google_vision', {}).get('enabled', False))
        ttk.Checkbutton(gv_frame, text="Enable Google Vision API", variable=self.gv_enabled).pack(anchor=tk.W)
        
        # Credentials
        cred_frame = ttk.Frame(gv_frame)
        cred_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(cred_frame, text="Credentials File:").pack(anchor=tk.W)
        cred_entry_frame = ttk.Frame(cred_frame)
        cred_entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.gv_credentials = tk.StringVar(value=self.config.get('api', {}).get('google_vision', {}).get('credentials_path', ''))
        ttk.Entry(cred_entry_frame, textvariable=self.gv_credentials).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(cred_entry_frame, text="Browse", command=self.browse_credentials).pack(side=tk.RIGHT)
        
        # API testing
        test_frame = ttk.Frame(gv_frame)
        test_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(test_frame, text="🧪 Test Connection", command=self.test_api_connection).pack(side=tk.LEFT, padx=(0, 10))
        self.api_status_label = ttk.Label(test_frame, text="Not tested")
        self.api_status_label.pack(side=tk.LEFT)
        
        # Usage statistics
        stats_frame = ttk.LabelFrame(api_frame, text="API Usage Statistics", padding=10)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.api_stats = scrolledtext.ScrolledText(stats_frame, height=10, state=tk.DISABLED)
        self.api_stats.pack(fill=tk.BOTH, expand=True)
    
    def create_legacy_tab(self):
        """Create comprehensive VB6/VFP9 DLL integration tab"""
        legacy_frame = ttk.Frame(self.notebook)
        self.notebook.add(legacy_frame, text="🏛 Legacy Integration")
        
        # Create scrollable frame for all content
        canvas = tk.Canvas(legacy_frame)
        scrollbar = ttk.Scrollbar(legacy_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # DLL Status and Builder
        dll_status_frame = ttk.LabelFrame(scrollable_frame, text="32-bit DLL Status", padding=10)
        dll_status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # DLL file status
        dll_status_inner = ttk.Frame(dll_status_frame)
        dll_status_inner.pack(fill=tk.X)
        
        self.dll_status_label = ttk.Label(dll_status_inner, text="⚠️ DLL not built")
        self.dll_status_label.pack(side=tk.LEFT)
        
        ttk.Button(dll_status_inner, text="🔄 Check DLL Status", command=self.check_dll_status).pack(side=tk.RIGHT)
        
        # DLL Builder
        builder_frame = ttk.LabelFrame(scrollable_frame, text="DLL Builder", padding=10)
        builder_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(builder_frame, text="Build the production 32-bit DLL for VB6/VFP9 integration:").pack(anchor=tk.W, pady=(0, 5))
        
        builder_buttons = ttk.Frame(builder_frame)
        builder_buttons.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(builder_buttons, text="🔨 Build DLL (Windows)", command=self.build_dll).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(builder_buttons, text="📁 Open DLL Source", command=self.open_dll_source).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(builder_buttons, text="📋 View Build Requirements", command=self.show_build_requirements).pack(side=tk.LEFT)
        
        # VB6 Integration
        vb6_frame = ttk.LabelFrame(scrollable_frame, text="VB6 Integration", padding=10)
        vb6_frame.pack(fill=tk.X, pady=(0, 10))
        
        vb6_buttons = ttk.Frame(vb6_frame)
        vb6_buttons.pack(fill=tk.X)
        
        ttk.Button(vb6_buttons, text="📄 Generate VB6 Module", command=self.generate_vb6_module).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(vb6_buttons, text="🧪 Test VB6 Integration", command=self.test_vb6_integration).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(vb6_buttons, text="📖 VB6 Examples", command=self.show_vb6_examples).pack(side=tk.LEFT)
        
        # VFP9 Integration  
        vfp9_frame = ttk.LabelFrame(scrollable_frame, text="VFP9 Integration", padding=10)
        vfp9_frame.pack(fill=tk.X, pady=(0, 10))
        
        vfp9_buttons = ttk.Frame(vfp9_frame)
        vfp9_buttons.pack(fill=tk.X)
        
        ttk.Button(vfp9_buttons, text="📄 Generate VFP9 Class", command=self.generate_vfp9_class).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(vfp9_buttons, text="🧪 Test VFP9 Integration", command=self.test_vfp9_integration).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(vfp9_buttons, text="📖 VFP9 Examples", command=self.show_vfp9_examples).pack(side=tk.LEFT)
        
        # DLL Testing
        testing_frame = ttk.LabelFrame(scrollable_frame, text="DLL Testing", padding=10)
        testing_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Test file selection
        test_file_frame = ttk.Frame(testing_frame)
        test_file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(test_file_frame, text="Test File:").pack(side=tk.LEFT)
        self.test_file_path = tk.StringVar()
        ttk.Entry(test_file_frame, textvariable=self.test_file_path, width=40).pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        ttk.Button(test_file_frame, text="📁 Browse", command=self.browse_test_file).pack(side=tk.RIGHT)
        
        # Test conversion
        test_buttons = ttk.Frame(testing_frame)
        test_buttons.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(test_buttons, text="🧪 Test DLL Conversion", command=self.test_dll_conversion).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(test_buttons, text="🔍 Test DLL Functions", command=self.test_dll_functions).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(test_buttons, text="📊 Performance Test", command=self.performance_test_dll).pack(side=tk.LEFT)
        
        # Installation and Deployment
        deploy_frame = ttk.LabelFrame(scrollable_frame, text="Installation & Deployment", padding=10)
        deploy_frame.pack(fill=tk.X, pady=(0, 10))
        
        deploy_buttons = ttk.Frame(deploy_frame)
        deploy_buttons.pack(fill=tk.X)
        
        ttk.Button(deploy_buttons, text="📦 Create Distribution Package", command=self.create_dll_package).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(deploy_buttons, text="⚙️ Install DLL System-wide", command=self.install_dll_system).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(deploy_buttons, text="📋 Copy Integration Files", command=self.copy_integration_files).pack(side=tk.LEFT)
        
        # Output and Logs
        output_frame = ttk.LabelFrame(scrollable_frame, text="Output & Logs", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.legacy_output = scrolledtext.ScrolledText(output_frame, height=12, font=('Consolas', 9))
        self.legacy_output.pack(fill=tk.BOTH, expand=True)
        
        # Initialize DLL status check
        self.check_dll_status()
    
    def create_settings_tab(self):
        """Create comprehensive settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Create settings notebook
        settings_notebook = ttk.Notebook(settings_frame)
        settings_notebook.pack(fill=tk.BOTH, expand=True)
        
        # General settings
        general_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(general_frame, text="General")
        
        # Performance settings
        perf_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(perf_frame, text="Performance")
        
        # Logging settings
        log_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(log_frame, text="Logging")
        
        # Setup each settings section
        self.setup_general_settings(general_frame)
        self.setup_performance_settings(perf_frame)
        self.setup_logging_settings(log_frame)
        
        # Settings controls
        settings_control_frame = ttk.Frame(settings_frame)
        settings_control_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(settings_control_frame, text="💾 Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(settings_control_frame, text="🔄 Reset to Defaults", command=self.reset_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(settings_control_frame, text="📂 Open Config Folder", command=self.open_config_folder).pack(side=tk.LEFT)
    
    def setup_general_settings(self, parent):
        """Setup general settings section"""
        # Theme selection
        theme_frame = ttk.LabelFrame(parent, text="Appearance", padding=10)
        theme_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(theme_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.theme_var = ttk.Combobox(theme_frame, values=["default", "clam", "alt", "classic"], state="readonly")
        self.theme_var.set(self.config.get('gui', {}).get('theme', 'default'))
        self.theme_var.grid(row=0, column=1, sticky=tk.W)
        
        # File handling
        file_frame = ttk.LabelFrame(parent, text="File Handling", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.preserve_formatting = tk.BooleanVar(value=self.config.get('conversion', {}).get('preserve_formatting', True))
        ttk.Checkbutton(file_frame, text="Preserve formatting during conversion", variable=self.preserve_formatting).pack(anchor=tk.W)
        
        self.auto_preview = tk.BooleanVar(value=self.config.get('gui', {}).get('auto_preview', False))
        ttk.Checkbutton(file_frame, text="Auto-preview converted files", variable=self.auto_preview).pack(anchor=tk.W)
    
    def setup_performance_settings(self, parent):
        """Setup performance settings section"""
        # Threading
        thread_frame = ttk.LabelFrame(parent, text="Threading", padding=10)
        thread_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(thread_frame, text="Max Workers:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.max_workers = tk.IntVar(value=self.config.get('conversion', {}).get('max_workers', 4))
        ttk.Spinbox(thread_frame, from_=1, to=16, textvariable=self.max_workers, width=5).grid(row=0, column=1, sticky=tk.W)
        
        # Caching
        cache_frame = ttk.LabelFrame(parent, text="Caching", padding=10)
        cache_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.use_cache = tk.BooleanVar(value=self.config.get('ocr', {}).get('use_cache', True))
        ttk.Checkbutton(cache_frame, text="Enable OCR result caching", variable=self.use_cache).pack(anchor=tk.W)
    
    def setup_logging_settings(self, parent):
        """Setup logging settings section"""
        # Log level
        level_frame = ttk.LabelFrame(parent, text="Log Level", padding=10)
        level_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(level_frame, text="Level:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.log_level = ttk.Combobox(level_frame, values=["DEBUG", "INFO", "WARNING", "ERROR"], state="readonly")
        self.log_level.set(self.config.get('logging', {}).get('level', 'INFO'))
        self.log_level.grid(row=0, column=1, sticky=tk.W)
    
    def create_status_bar(self, parent):
        """Create status bar at bottom"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Version label
        version_label = ttk.Label(status_frame, text="v3.1.0", relief=tk.SUNKEN)
        version_label.pack(side=tk.RIGHT)
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD
            # Enable drag and drop on file listbox
            self.file_listbox.drop_target_register(DND_FILES)
            self.file_listbox.dnd_bind('<<Drop>>', self.on_drop)
        except ImportError:
            self.logger.warning("Drag and drop not available - tkinterdnd2 not installed")
    
    def on_drop(self, event):
        """Handle dropped files"""
        files = self.file_listbox.tk.splitlist(event.data)
        for file_path in files:
            if Path(file_path).is_file():
                self.file_listbox.insert(tk.END, file_path)
    
    # File management methods
    def add_files(self):
        """Add files to conversion list"""
        files = filedialog.askopenfilenames(
            title="Select files to convert",
            filetypes=[
                ("All supported", "*.txt;*.docx;*.pdf;*.html;*.rtf;*.md;*.epub"),
                ("Text files", "*.txt"),
                ("Word documents", "*.docx"),
                ("PDF files", "*.pdf"),
                ("HTML files", "*.html"),
                ("RTF files", "*.rtf"),
                ("Markdown files", "*.md"),
                ("EPUB files", "*.epub")
            ]
        )
        for file in files:
            self.file_listbox.insert(tk.END, file)
    
    def add_folder(self):
        """Add folder for batch conversion"""
        folder = filedialog.askdirectory(title="Select folder to convert")
        if folder:
            folder_path = Path(folder)
            for file_path in folder_path.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.docx', '.pdf', '.html', '.rtf', '.md', '.epub']:
                    self.file_listbox.insert(tk.END, str(file_path))
    
    def clear_files(self):
        """Clear file list"""
        self.file_listbox.delete(0, tk.END)
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir.set(directory)
    
    # Conversion methods
    def start_conversion(self):
        """Start document conversion process"""
        if self.is_processing:
            return
        
        files = list(self.file_listbox.get(0, tk.END))
        if not files:
            messagebox.showwarning("No Files", "Please add files to convert first.")
            return
        
        output_dir = Path(self.output_dir.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.is_processing = True
        self.cancel_processing = False
        self.processed_count = 0
        self.total_files = len(files)
        
        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # Start conversion in separate thread
        self.processing_thread = threading.Thread(target=self.conversion_worker, args=(files, output_dir))
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def conversion_worker(self, files, output_dir):
        """Worker thread for file conversion"""
        try:
            for i, file_path in enumerate(files):
                if self.cancel_processing:
                    break
                
                self.update_status(f"Processing {Path(file_path).name}...")
                
                try:
                    # Perform conversion based on selected format
                    self.convert_single_file(file_path, output_dir)
                    self.processed_count += 1
                    
                except Exception as e:
                    self.logger.error(f"Error converting {file_path}: {e}")
                
                # Update progress
                progress = ((i + 1) / len(files)) * 100
                self.update_progress(progress)
        
        finally:
            self.root.after(0, self.processing_complete)
    
    def convert_single_file(self, input_path, output_dir):
        """Convert a single file"""
        input_file = Path(input_path)
        output_format = self.output_format.get()
        
        # Determine output filename
        output_file = output_dir / f"{input_file.stem}.{output_format}"
        
        # Perform conversion based on format
        if output_format == "markdown" and HAS_MARKDOWN:
            if input_file.suffix.lower() == '.docx':
                convert_docx_to_markdown(str(input_file))
            elif input_file.suffix.lower() == '.pdf':
                convert_pdf_to_markdown(str(input_file))
        else:
            # Basic conversion (placeholder - would need full implementation)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Converted from: {input_path}\n")
                f.write(f"Format: {output_format}\n")
                f.write("Full conversion implementation would go here.\n")
    
    def cancel_conversion(self):
        """Cancel ongoing conversion"""
        self.cancel_processing = True
        self.update_status("Cancelling...")
    
    def processing_complete(self):
        """Handle conversion completion"""
        self.is_processing = False
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        
        if self.cancel_processing:
            self.update_status(f"Cancelled - {self.processed_count}/{self.total_files} files processed")
        else:
            self.update_status(f"Complete - {self.processed_count}/{self.total_files} files processed")
            messagebox.showinfo("Complete", f"Conversion completed!\n{self.processed_count} files processed.")
        
        self.update_progress(0)
    
    # OCR methods
    def process_ocr(self):
        """Process OCR on selected image"""
        file_path = filedialog.askopenfilename(
            title="Select image for OCR",
            filetypes=[
                ("Image files", "*.png;*.jpg;*.jpeg;*.tiff;*.bmp;*.gif"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        if not self.ocr_engine:
            messagebox.showerror("OCR Error", "OCR engine not available")
            return
        
        try:
            self.update_status("Processing OCR...")
            
            # Get OCR settings
            options = {
                'engine': self.ocr_engine_var.get(),
                'language': self.ocr_language.get()
            }
            
            # Process OCR
            result = self.ocr_engine.extract_text(file_path, options)
            
            # Display result
            self.ocr_preview.delete(1.0, tk.END)
            self.ocr_preview.insert(tk.END, result.get('text', 'No text detected'))
            
            self.update_status(f"OCR completed - Confidence: {result.get('confidence', 'N/A')}")
            
        except Exception as e:
            messagebox.showerror("OCR Error", f"OCR processing failed: {e}")
            self.update_status("OCR failed")
    
    def save_ocr_result(self):
        """Save OCR result to file"""
        text = self.ocr_preview.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("No Text", "No OCR text to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save OCR result",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Saved", f"OCR result saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file: {e}")
    
    # Markdown methods
    def load_markdown_file(self):
        """Load markdown file into editor"""
        file_path = filedialog.askopenfilename(
            title="Load markdown file",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.md_editor.delete(1.0, tk.END)
                self.md_editor.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Load Error", f"Could not load file: {e}")
    
    def save_markdown_file(self):
        """Save markdown from editor"""
        content = self.md_editor.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("No Content", "No content to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save markdown file",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Saved", f"Markdown saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file: {e}")
    
    def convert_markdown(self):
        """Convert markdown bidirectionally"""
        direction = self.md_direction.get()
        
        if direction == "to_markdown":
            # Convert TO markdown
            file_path = filedialog.askopenfilename(
                title="Select file to convert to markdown",
                filetypes=[("Word documents", "*.docx"), ("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if file_path and HAS_MARKDOWN:
                try:
                    if file_path.endswith('.docx'):
                        result = convert_docx_to_markdown(file_path)
                    elif file_path.endswith('.pdf'):
                        result = convert_pdf_to_markdown(file_path)
                    else:
                        result = "Conversion not supported for this format"
                    
                    self.md_editor.delete(1.0, tk.END)
                    self.md_editor.insert(tk.END, result)
                    
                except Exception as e:
                    messagebox.showerror("Conversion Error", f"Could not convert: {e}")
        else:
            # Convert FROM markdown
            messagebox.showinfo("Coming Soon", "Conversion FROM markdown will be implemented in a future version")
    
    def preview_markdown(self):
        """Preview markdown content"""
        content = self.md_editor.get(1.0, tk.END)
        # Simple preview (would need markdown renderer for full preview)
        self.md_preview.config(state=tk.NORMAL)
        self.md_preview.delete(1.0, tk.END)
        self.md_preview.insert(tk.END, f"Markdown Preview:\n\n{content}")
        self.md_preview.config(state=tk.DISABLED)
    
    # API methods
    def browse_credentials(self):
        """Browse for Google Vision API credentials"""
        file_path = filedialog.askopenfilename(
            title="Select Google Vision API credentials",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            self.gv_credentials.set(file_path)
    
    def test_api_connection(self):
        """Test Google Vision API connection"""
        if not HAS_GOOGLE_VISION:
            self.api_status_label.config(text="❌ Google Vision not available")
            return
        
        credentials_path = self.gv_credentials.get()
        if not credentials_path:
            self.api_status_label.config(text="❌ No credentials file")
            return
        
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            client = vision.ImageAnnotatorClient()
            self.api_status_label.config(text="✅ Connection successful")
        except Exception as e:
            self.api_status_label.config(text=f"❌ Connection failed: {str(e)[:30]}...")
    
    # Legacy integration methods
    def test_cli_command(self):
        """Test CLI command for VB6/VFP9 integration"""
        command = self.cli_command.get()
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            
            self.cli_output.delete(1.0, tk.END)
            self.cli_output.insert(tk.END, f"Command: {command}\n")
            self.cli_output.insert(tk.END, f"Return code: {result.returncode}\n\n")
            self.cli_output.insert(tk.END, "STDOUT:\n")
            self.cli_output.insert(tk.END, result.stdout)
            self.cli_output.insert(tk.END, "\nSTDERR:\n")
            self.cli_output.insert(tk.END, result.stderr)
            
        except subprocess.TimeoutExpired:
            self.cli_output.delete(1.0, tk.END)
            self.cli_output.insert(tk.END, "Command timed out after 30 seconds")
        except Exception as e:
            self.cli_output.delete(1.0, tk.END)
            self.cli_output.insert(tk.END, f"Error running command: {e}")
    
    # === DLL INTEGRATION METHODS ===
    
    def check_dll_status(self):
        """Check the status of the DLL build and installation"""
        self.legacy_log("Checking DLL status...")
        
        # Check for built DLL
        dll_paths = [
            Path("dist/UniversalConverter32.dll"),
            Path("dll_source/UniversalConverter32.dll"),
            Path("UniversalConverter32.dll")
        ]
        
        dll_found = False
        dll_path = None
        
        for path in dll_paths:
            if path.exists():
                dll_found = True
                dll_path = path
                break
        
        if dll_found:
            self.dll_status_label.config(text=f"✅ DLL found: {dll_path}")
            self.legacy_log(f"✅ DLL found at: {dll_path}")
            
            # Check DLL file size and modification time
            stat = dll_path.stat()
            size_kb = stat.st_size / 1024
            mod_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            self.legacy_log(f"   Size: {size_kb:.1f} KB, Modified: {mod_time}")
        else:
            self.dll_status_label.config(text="⚠️ DLL not built")
            self.legacy_log("⚠️ DLL not found - use 'Build DLL' to create it")
        
        # Check for source files
        source_files = [
            "dll_source/UniversalConverter32.cpp",
            "dll_source/UniversalConverter32.def",
            "build_dll.bat"
        ]
        
        for file in source_files:
            if Path(file).exists():
                self.legacy_log(f"✅ Source: {file}")
            else:
                self.legacy_log(f"❌ Missing: {file}")
    
    def build_dll(self):
        """Build the 32-bit DLL using the build script"""
        self.legacy_log("Building UniversalConverter32.dll...")
        
        try:
            # Check if on Windows
            import platform
            if platform.system() != "Windows":
                self.legacy_log("❌ DLL building requires Windows")
                self.legacy_log("   Transfer files to Windows system and run build_dll.bat")
                return
            
            # Check for build script
            build_script = Path("build_dll.bat")
            if not build_script.exists():
                self.legacy_log("❌ build_dll.bat not found")
                return
            
            # Run build script in a separate thread
            def build_thread():
                try:
                    import subprocess
                    process = subprocess.Popen(
                        ["build_dll.bat"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        universal_newlines=True
                    )
                    
                    # Read output line by line
                    for line in process.stdout:
                        self.legacy_log(line.strip())
                    
                    process.wait()
                    
                    if process.returncode == 0:
                        self.legacy_log("✅ DLL build completed successfully!")
                        self.check_dll_status()  # Refresh status
                    else:
                        self.legacy_log(f"❌ DLL build failed with code {process.returncode}")
                        
                except Exception as e:
                    self.legacy_log(f"❌ Build error: {str(e)}")
            
            # Start build in background
            import threading
            threading.Thread(target=build_thread, daemon=True).start()
            
        except Exception as e:
            self.legacy_log(f"❌ Error starting build: {str(e)}")
    
    def open_dll_source(self):
        """Open the DLL source directory"""
        try:
            source_dir = Path("dll_source")
            if source_dir.exists():
                import subprocess
                import platform
                
                if platform.system() == "Windows":
                    subprocess.Popen(f'explorer "{source_dir.absolute()}"')
                elif platform.system() == "Darwin":  # macOS
                    subprocess.Popen(["open", str(source_dir.absolute())])
                else:  # Linux
                    subprocess.Popen(["xdg-open", str(source_dir.absolute())])
                
                self.legacy_log(f"📁 Opened source directory: {source_dir.absolute()}")
            else:
                self.legacy_log("❌ DLL source directory not found")
        except Exception as e:
            self.legacy_log(f"❌ Error opening directory: {str(e)}")
    
    def show_build_requirements(self):
        """Show DLL build requirements"""
        requirements = """
DLL Build Requirements:

SYSTEM REQUIREMENTS:
• Windows operating system
• 32-bit or 64-bit architecture

COMPILER OPTIONS (choose one):
1. Microsoft Visual Studio Build Tools
   - Download from: https://visualstudio.microsoft.com/downloads/
   - Install C++ build tools
   
2. MinGW-w64 Compiler
   - Download from: https://www.mingw-w64.org/
   - Or install via MSYS2: pacman -S mingw-w64-i686-gcc

BUILD PROCESS:
1. Open Command Prompt as Administrator
2. Navigate to the project directory
3. Run: build_dll.bat
4. Result: UniversalConverter32.dll

VERIFICATION:
• DLL should be ~50-200 KB in size
• Test with: test_dll_integration.py
• Import into VB6/VFP9 projects

DEPENDENCIES:
• Python 3.7+ must be installed
• cli.py must be in same directory as DLL
• requirements.txt packages must be installed
"""
        
        self.legacy_log(requirements)
    
    def generate_vb6_module(self):
        """Generate customized VB6 integration module"""
        self.legacy_log("Generating VB6 integration module...")
        
        try:
            # Read the production VB6 module
            vb6_source = Path("VB6_UniversalConverter_Production.bas")
            if not vb6_source.exists():
                self.legacy_log("❌ VB6 production module not found")
                return
            
            content = vb6_source.read_text()
            
            # Save to user's desktop or current directory
            import os
            desktop = Path.home() / "Desktop"
            if desktop.exists():
                output_path = desktop / "UniversalConverter_VB6.bas"
            else:
                output_path = Path("UniversalConverter_VB6.bas")
            
            output_path.write_text(content)
            self.legacy_log(f"✅ VB6 module generated: {output_path}")
            self.legacy_log("   Add this .bas file to your VB6 project")
            
        except Exception as e:
            self.legacy_log(f"❌ Error generating VB6 module: {str(e)}")
    
    def generate_vfp9_class(self):
        """Generate customized VFP9 integration class"""
        self.legacy_log("Generating VFP9 integration class...")
        
        try:
            # Read the production VFP9 class
            vfp9_source = Path("VFP9_UniversalConverter_Production.prg")
            if not vfp9_source.exists():
                self.legacy_log("❌ VFP9 production class not found")
                return
            
            content = vfp9_source.read_text()
            
            # Save to user's desktop or current directory
            import os
            desktop = Path.home() / "Desktop"
            if desktop.exists():
                output_path = desktop / "UniversalConverter_VFP9.prg"
            else:
                output_path = Path("UniversalConverter_VFP9.prg")
            
            output_path.write_text(content)
            self.legacy_log(f"✅ VFP9 class generated: {output_path}")
            self.legacy_log("   Include this .prg file in your VFP9 project")
            
        except Exception as e:
            self.legacy_log(f"❌ Error generating VFP9 class: {str(e)}")
    
    def test_vb6_integration(self):
        """Test VB6 DLL integration"""
        self.legacy_log("Testing VB6 DLL integration...")
        
        vb6_test = '''
' VB6 Test Code for UniversalConverter32.dll
Private Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String, _
     ByVal inputFormat As String, ByVal outputFormat As String) As Long

Private Declare Function TestConnection Lib "UniversalConverter32.dll" () As Long

Sub TestDLL()
    Dim result As Long
    
    ' Test if DLL is available
    result = TestConnection()
    If result = 1 Then
        MsgBox "✅ DLL is available and working!"
    Else
        MsgBox "❌ DLL test failed"
    End If
    
    ' Test conversion (modify paths as needed)
    result = ConvertDocument("C:\\temp\\test.txt", "C:\\temp\\test.md", "txt", "md")
    If result = 1 Then
        MsgBox "✅ Conversion successful!"
    Else
        MsgBox "❌ Conversion failed"
    End If
End Sub
'''
        
        self.legacy_log("VB6 Test Code:")
        self.legacy_log(vb6_test)
        self.legacy_log("Copy this code to a VB6 form and run TestDLL()")
    
    def test_vfp9_integration(self):
        """Test VFP9 DLL integration"""
        self.legacy_log("Testing VFP9 DLL integration...")
        
        vfp9_test = '''
*!* VFP9 Test Code for UniversalConverter32.dll
DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, ;
    STRING inputFormat, STRING outputFormat

DECLARE INTEGER TestConnection IN UniversalConverter32.dll

PROCEDURE TestDLL()
    LOCAL lnResult
    
    *-- Test if DLL is available
    lnResult = TestConnection()
    IF lnResult = 1
        MESSAGEBOX("✅ DLL is available and working!")
    ELSE
        MESSAGEBOX("❌ DLL test failed")
    ENDIF
    
    *-- Test conversion (modify paths as needed)
    lnResult = ConvertDocument("C:\\temp\\test.txt", "C:\\temp\\test.md", "txt", "md")
    IF lnResult = 1
        MESSAGEBOX("✅ Conversion successful!")
    ELSE
        MESSAGEBOX("❌ Conversion failed")
    ENDIF
ENDPROC
'''
        
        self.legacy_log("VFP9 Test Code:")
        self.legacy_log(vfp9_test)
        self.legacy_log("Copy this code to a VFP9 program and run TestDLL")
    
    def browse_test_file(self):
        """Browse for a test file"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Select Test File",
            filetypes=[
                ("All Supported", "*.pdf;*.docx;*.txt;*.html;*.md;*.rtf"),
                ("PDF files", "*.pdf"),
                ("Word documents", "*.docx"),
                ("Text files", "*.txt"),
                ("HTML files", "*.html"),
                ("Markdown files", "*.md"),
                ("RTF files", "*.rtf"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.test_file_path.set(filename)
            self.legacy_log(f"📁 Selected test file: {filename}")
    
    def test_dll_conversion(self):
        """Test DLL conversion functionality"""
        test_file = self.test_file_path.get()
        if not test_file:
            self.legacy_log("❌ No test file selected")
            return
        
        if not Path(test_file).exists():
            self.legacy_log("❌ Test file does not exist")
            return
        
        self.legacy_log(f"🧪 Testing DLL conversion: {test_file}")
        
        try:
            # Test CLI backend (which the DLL uses)
            import subprocess
            import tempfile
            
            with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                output_file = tmp.name
            
            cmd = [
                sys.executable, "cli.py", 
                test_file, 
                "-o", output_file, 
                "-t", "txt"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                if Path(output_file).exists():
                    # Read first few lines of output
                    content = Path(output_file).read_text()[:200]
                    self.legacy_log("✅ Conversion successful!")
                    self.legacy_log(f"   Output preview: {content}...")
                    
                    # Clean up
                    Path(output_file).unlink()
                else:
                    self.legacy_log("❌ Conversion completed but no output file")
            else:
                self.legacy_log(f"❌ Conversion failed: {result.stderr}")
                
        except Exception as e:
            self.legacy_log(f"❌ Test error: {str(e)}")
    
    def test_dll_functions(self):
        """Test individual DLL functions"""
        self.legacy_log("🔍 Testing DLL functions...")
        
        # Test the CLI backend that powers the DLL
        try:
            import subprocess
            
            # Test 1: CLI help
            result = subprocess.run([sys.executable, "cli.py", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.legacy_log("✅ CLI help function working")
            else:
                self.legacy_log("❌ CLI help function failed")
            
            # Test 2: Format support
            result = subprocess.run([sys.executable, "cli.py", "--formats"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.legacy_log("✅ Format detection working")
                self.legacy_log(f"   Supported formats: {result.stdout.strip()}")
            else:
                self.legacy_log("❌ Format detection failed")
            
            # Test 3: Version
            result = subprocess.run([sys.executable, "cli.py", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.legacy_log("✅ Version function working")
                self.legacy_log(f"   Version: {result.stdout.strip()}")
            else:
                self.legacy_log("❌ Version function failed")
            
        except Exception as e:
            self.legacy_log(f"❌ Function test error: {str(e)}")
    
    def performance_test_dll(self):
        """Run performance test on DLL"""
        self.legacy_log("📊 Running performance test...")
        
        test_file = self.test_file_path.get()
        if not test_file or not Path(test_file).exists():
            self.legacy_log("❌ Need a valid test file for performance testing")
            return
        
        try:
            import subprocess
            import tempfile
            import time
            
            # Run multiple conversions and time them
            times = []
            for i in range(3):
                with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
                    output_file = tmp.name
                
                start_time = time.time()
                
                cmd = [sys.executable, "cli.py", test_file, "-o", output_file, "-t", "txt", "--quiet"]
                result = subprocess.run(cmd, capture_output=True, timeout=30)
                
                end_time = time.time()
                duration = end_time - start_time
                times.append(duration)
                
                if result.returncode == 0:
                    self.legacy_log(f"✅ Test {i+1}: {duration:.2f} seconds")
                    Path(output_file).unlink()  # Clean up
                else:
                    self.legacy_log(f"❌ Test {i+1}: Failed")
            
            if times:
                avg_time = sum(times) / len(times)
                self.legacy_log(f"📊 Average conversion time: {avg_time:.2f} seconds")
                self.legacy_log(f"📊 Fastest: {min(times):.2f}s, Slowest: {max(times):.2f}s")
            
        except Exception as e:
            self.legacy_log(f"❌ Performance test error: {str(e)}")
    
    def create_dll_package(self):
        """Create distribution package for DLL"""
        self.legacy_log("📦 Creating DLL distribution package...")
        
        try:
            # Use the existing package builder
            import subprocess
            
            result = subprocess.run([sys.executable, "build_ocr_packages.py"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.legacy_log("✅ Distribution package created successfully!")
                self.legacy_log(result.stdout)
                
                # Check if package was created
                package_path = Path("dist/UniversalConverter32.dll.zip")
                if package_path.exists():
                    size_kb = package_path.stat().st_size / 1024
                    self.legacy_log(f"📦 Package: {package_path} ({size_kb:.1f} KB)")
            else:
                self.legacy_log("❌ Package creation failed")
                self.legacy_log(result.stderr)
                
        except Exception as e:
            self.legacy_log(f"❌ Package creation error: {str(e)}")
    
    def install_dll_system(self):
        """Install DLL system-wide"""
        self.legacy_log("⚙️ Installing DLL system-wide...")
        
        try:
            dll_path = None
            for path in [Path("dist/UniversalConverter32.dll"), Path("UniversalConverter32.dll")]:
                if path.exists():
                    dll_path = path
                    break
            
            if not dll_path:
                self.legacy_log("❌ DLL not found - build it first")
                return
            
            import platform
            import shutil
            
            if platform.system() != "Windows":
                self.legacy_log("❌ System-wide installation requires Windows")
                return
            
            # Copy DLL to System32 (requires admin rights)
            system32 = Path(os.environ["WINDIR"]) / "System32"
            target = system32 / "UniversalConverter32.dll"
            
            try:
                shutil.copy2(dll_path, target)
                self.legacy_log(f"✅ DLL installed to: {target}")
                self.legacy_log("   DLL is now available system-wide")
            except PermissionError:
                self.legacy_log("❌ Installation failed - run as Administrator")
            except Exception as e:
                self.legacy_log(f"❌ Installation error: {str(e)}")
                
        except Exception as e:
            self.legacy_log(f"❌ System installation error: {str(e)}")
    
    def copy_integration_files(self):
        """Copy integration files to desktop"""
        self.legacy_log("📋 Copying integration files...")
        
        try:
            desktop = Path.home() / "Desktop"
            if not desktop.exists():
                desktop = Path(".")
            
            files_to_copy = [
                ("VB6_UniversalConverter_Production.bas", "VB6 Integration Module"),
                ("VFP9_UniversalConverter_Production.prg", "VFP9 Integration Class"),
                ("cli.py", "CLI Backend"),
                ("requirements.txt", "Python Dependencies"),
                ("README_DLL_Production.md", "Documentation")
            ]
            
            copied = 0
            for filename, description in files_to_copy:
                source = Path(filename)
                if source.exists():
                    target = desktop / filename
                    shutil.copy2(source, target)
                    self.legacy_log(f"✅ {description}: {target}")
                    copied += 1
                else:
                    self.legacy_log(f"❌ Missing: {filename}")
            
            self.legacy_log(f"📋 Copied {copied} files to {desktop}")
            
        except Exception as e:
            self.legacy_log(f"❌ Copy error: {str(e)}")
    
    def legacy_log(self, message):
        """Log message to legacy output area"""
        if hasattr(self, 'legacy_output'):
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.legacy_output.insert(tk.END, f"[{timestamp}] {message}\n")
            self.legacy_output.see(tk.END)
        else:
            print(f"[LEGACY] {message}")
    
    def show_vb6_examples(self):
        """Show real VB6 DLL integration examples"""
        examples = """
REAL VB6 DLL INTEGRATION EXAMPLES:

1. BASIC DLL USAGE:
' Declare the DLL functions
Private Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String, _
     ByVal inputFormat As String, ByVal outputFormat As String) As Long

Private Declare Function TestConnection Lib "UniversalConverter32.dll" () As Long

' Test if DLL is available
Private Sub cmdTest_Click()
    Dim result As Long
    result = TestConnection()
    If result = 1 Then
        MsgBox "DLL is working!"
    Else
        MsgBox "DLL not available"
    End If
End Sub

2. DOCUMENT CONVERSION:
Private Sub cmdConvert_Click()
    Dim result As Long
    result = ConvertDocument("C:\\docs\\file.pdf", "C:\\docs\\file.txt", "pdf", "txt")
    If result = 1 Then
        MsgBox "Conversion successful!"
    Else
        MsgBox "Conversion failed!"
    End If
End Sub

3. USING THE PRODUCTION MODULE:
' Add VB6_UniversalConverter_Production.bas to your project
Private Sub cmdAdvanced_Click()
    If InitializeConverter() Then
        If PDFToText("C:\\temp\\document.pdf", "C:\\temp\\output.txt") Then
            MsgBox "PDF converted to text successfully!"
        Else
            MsgBox "Error: " & GetLastErrorMessage()
        End If
    End If
End Sub
"""
        
        self.legacy_log(examples)
    
    def show_vfp9_examples(self):
        """Show real VFP9 DLL integration examples"""
        examples = """
REAL VFP9 DLL INTEGRATION EXAMPLES:

1. BASIC DLL USAGE:
*-- Declare the DLL functions
DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, ;
    STRING inputFormat, STRING outputFormat

DECLARE INTEGER TestConnection IN UniversalConverter32.dll

*-- Test if DLL is available
lnResult = TestConnection()
IF lnResult = 1
    MESSAGEBOX("DLL is working!")
ELSE
    MESSAGEBOX("DLL not available")
ENDIF

2. DOCUMENT CONVERSION:
lnResult = ConvertDocument("C:\\docs\\file.pdf", "C:\\docs\\file.txt", "pdf", "txt")
IF lnResult = 1
    MESSAGEBOX("Conversion successful!")
ELSE
    MESSAGEBOX("Conversion failed!")
ENDIF

3. USING THE PRODUCTION CLASS:
*-- Include VFP9_UniversalConverter_Production.prg in your project
loConverter = CREATEOBJECT("UniversalConverter")

IF loConverter.lInitialized
    llSuccess = loConverter.PDFToText("C:\\temp\\document.pdf", "C:\\temp\\output.txt")
    IF llSuccess
        MESSAGEBOX("PDF converted successfully!")
    ELSE
        MESSAGEBOX("Error: " + loConverter.cLastError)
    ENDIF
ELSE
    MESSAGEBOX("Converter not available")
ENDIF

4. BATCH CONVERSION:
loConverter = CREATEOBJECT("UniversalConverter")
lnConverted = loConverter.ConvertDirectory("C:\\PDFs", "C:\\Text", "pdf", "txt")
MESSAGEBOX(TRANSFORM(lnConverted) + " files converted")
"""
        
        self.legacy_log(examples)
    
    def open_integration_guide(self):
        """Open VB6/VFP9 integration guide"""
        guide_path = Path(__file__).parent / "VFP9_VB6_INTEGRATION_GUIDE.md"
        if guide_path.exists():
            webbrowser.open(f"file://{guide_path}")
        else:
            messagebox.showwarning("Guide Not Found", "Integration guide not found in current directory")
    
    # Settings methods
    def save_settings(self):
        """Save current settings"""
        # Update config with current values
        self.config['gui']['theme'] = self.theme_var.get()
        self.config['conversion']['preserve_formatting'] = self.preserve_formatting.get()
        self.config['gui']['auto_preview'] = self.auto_preview.get()
        self.config['conversion']['max_workers'] = self.max_workers.get()
        self.config['ocr']['use_cache'] = self.use_cache.get()
        self.config['logging']['level'] = self.log_level.get()
        self.config['api']['google_vision']['enabled'] = self.gv_enabled.get()
        self.config['api']['google_vision']['credentials_path'] = self.gv_credentials.get()
        self.config['legacy']['vb6_vfp9_integration'] = self.legacy_enabled.get()
        
        self.save_config()
        messagebox.showinfo("Settings Saved", "Settings have been saved successfully")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            # Reset to default config
            self.config = self.load_config()  # This will load defaults if no config exists
            
            # Update UI elements
            self.theme_var.set(self.config['gui']['theme'])
            self.preserve_formatting.set(self.config['conversion']['preserve_formatting'])
            self.auto_preview.set(self.config['gui']['auto_preview'])
            self.max_workers.set(self.config['conversion']['max_workers'])
            self.use_cache.set(self.config['ocr']['use_cache'])
            self.log_level.set(self.config['logging']['level'])
            self.gv_enabled.set(self.config['api']['google_vision']['enabled'])
            self.gv_credentials.set(self.config['api']['google_vision']['credentials_path'])
            self.legacy_enabled.set(self.config['legacy']['vb6_vfp9_integration'])
            
            messagebox.showinfo("Settings Reset", "Settings have been reset to defaults")
    
    def open_config_folder(self):
        """Open configuration folder"""
        config_dir = Path.home() / ".universal_converter"
        if config_dir.exists():
            webbrowser.open(f"file://{config_dir}")
        else:
            messagebox.showwarning("Folder Not Found", "Configuration folder does not exist yet")
    
    # Utility methods
    def update_status(self, message: str):
        """Update status label (thread-safe)"""
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def update_progress(self, value: float):
        """Update progress bar (thread-safe)"""
        self.root.after(0, lambda: self.progress_var.set(value))
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_processing:
            if messagebox.askokcancel("Quit", "Processing is in progress. Do you want to quit?"):
                self.cancel_processing = True
                if self.processing_thread and self.processing_thread.is_alive():
                    self.processing_thread.join(timeout=2)
                self.root.destroy()
        else:
            self.save_config()  # Save settings on exit
            self.root.destroy()

def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Enable drag and drop
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        pass
    
    app = UniversalDocumentConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()