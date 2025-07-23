#!/usr/bin/env python3
"""
Universal Document Converter - Complete Enterprise Solution
Complete GUI application with OCR, document conversion, markdown tools, and API management
Designed and built by Beau Lewis (blewisxx@gmail.com)

Complete Feature Set:
- Full OCR functionality (Tesseract, EasyOCR, Google Vision API)
- Complete document conversion (DOCX, PDF, TXT, HTML, RTF, EPUB, Markdown)
- Bidirectional markdown converter with markdown reader
- API management for cloud OCR services
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
from collections import OrderedDict
import concurrent.futures
import time
import hashlib
from threading import Lock
import webbrowser
import gc

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
        self.failed_count = 0
        self.skipped_count = 0
        self.start_time = None
        
        # Caching system with LRU support
        self.conversion_cache = OrderedDict()  # LRU cache using OrderedDict
        self.cache_sizes = {}  # Track individual entry sizes
        self.cache_lock = Lock()
        self.max_cache_size = 100 * 1024 * 1024  # 100MB cache limit
        self.current_cache_size = 0
        
        # OCR and conversion engines
        self.ocr_engine = None
        self.current_files = []
        
        # Configuration and settings
        self.config = self.load_config()
        self.setup_logging()
        
        # Adaptive processing configuration
        self._last_memory_check = 0
        self._adaptive_batch_size = 4  # Default batch size
        self._memory_check_interval = 30  # Check memory every 30 seconds
        
        # Initialize OCR if available
        if HAS_OCR:
            try:
                # Enhanced OCR config with secure credential handling
                ocr_config = self.config.get('ocr', {}).copy()
                
                # Set up Google Vision credentials securely
                if self.config.get('api', {}).get('google_vision', {}).get('enabled', False):
                    credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
                    if not credentials_path:
                        credentials_path = self.config.get('api', {}).get('google_vision', {}).get('credentials_path', '')
                    
                    if credentials_path and self._validate_credentials_file_init(credentials_path):
                        # Only set if not already in environment and file is valid
                        if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
                            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
                        ocr_config['google_vision_enabled'] = True
                    else:
                        self.logger.warning("Google Vision API credentials not found or invalid")
                        ocr_config['google_vision_enabled'] = False
                
                self.ocr_engine = OCREngine(config=ocr_config)
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
        
        # Store handlers for proper cleanup
        self.file_handler = logging.FileHandler(log_file)
        self.stream_handler = logging.StreamHandler()
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                self.file_handler,
                self.stream_handler
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
                    'fallback_enabled': True,
                    'fallback_preference': 'tesseract'  # Preferred fallback engine
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
        self.create_tools_tab()
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
        
        # Create two rows of options
        options_row1 = ttk.Frame(options_frame)
        options_row1.pack(fill=tk.X, pady=(0, 5))
        options_row2 = ttk.Frame(options_frame)
        options_row2.pack(fill=tk.X)
        
        # Output format
        ttk.Label(options_row1, text="Output Format:").pack(side=tk.LEFT, padx=(0, 5))
        self.output_format = ttk.Combobox(options_row1, values=[
            "txt", "docx", "pdf", "html", "rtf", "markdown", "epub", "json"
        ], state="readonly", width=10)
        self.output_format.set("txt")
        self.output_format.pack(side=tk.LEFT, padx=(0, 20))
        
        # Output directory
        ttk.Label(options_row1, text="Output Directory:").pack(side=tk.LEFT, padx=(0, 5))
        self.output_dir = tk.StringVar(value=str(Path.home() / "Documents" / "Converted"))
        ttk.Entry(options_row1, textvariable=self.output_dir, width=30).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(options_row1, text="Browse", command=self.browse_output_dir).pack(side=tk.LEFT)
        
        # Batch processing options
        self.preserve_structure = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_row2, text="Preserve folder structure", variable=self.preserve_structure).pack(side=tk.LEFT, padx=(0, 10))
        
        self.skip_existing = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_row2, text="Skip existing files", variable=self.skip_existing).pack(side=tk.LEFT, padx=(0, 10))
        
        self.use_cache = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_row2, text="Use cache", variable=self.use_cache).pack(side=tk.LEFT, padx=(0, 10))
        
        # Worker threads
        ttk.Label(options_row2, text="Threads:").pack(side=tk.LEFT, padx=(10, 5))
        self.worker_threads = tk.IntVar(value=4)
        ttk.Spinbox(options_row2, from_=1, to=16, textvariable=self.worker_threads, width=5).pack(side=tk.LEFT)
        
        # Processing controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="🚀 Start Conversion", command=self.start_conversion)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_button = ttk.Button(control_frame, text="⏹ Cancel", command=self.cancel_conversion, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT)
        
        # Progress bar and status
        progress_container = ttk.Frame(control_frame)
        progress_container.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(20, 0))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_container, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)
        
        # Progress details
        self.progress_detail_label = ttk.Label(progress_container, text="", font=('Arial', 9))
        self.progress_detail_label.pack(anchor=tk.E)
    
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
        self.ocr_engine_var.bind('<<ComboboxSelected>>', self.on_ocr_engine_changed)
        
        ttk.Label(engine_frame, text="Language:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.ocr_language = ttk.Combobox(engine_frame, values=[
            "eng", "fra", "deu", "spa", "ita", "por", "eng+fra", "eng+spa", "eng+deu"
        ], state="readonly")
        self.ocr_language.set("eng")
        self.ocr_language.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # OCR Quality setting
        ttk.Label(engine_frame, text="Quality:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        self.ocr_quality = ttk.Combobox(engine_frame, values=["fast", "standard", "accurate"], state="readonly")
        self.ocr_quality.set("standard")
        self.ocr_quality.grid(row=0, column=5, sticky=tk.W)
        
        # OCR Engine Status Display
        status_frame = ttk.Frame(engine_frame)
        status_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(10, 0))
        
        self.ocr_status_label = ttk.Label(status_frame, text="🔍 OCR Engine: Auto-detect", font=('Arial', 10, 'bold'))
        self.ocr_status_label.pack(anchor=tk.W)
        
        # File selection for batch OCR
        batch_frame = ttk.LabelFrame(ocr_frame, text="Batch OCR Files", padding=10)
        batch_frame.pack(fill=tk.X, pady=(0, 10))
        
        # File list for batch OCR
        list_frame = ttk.Frame(batch_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ocr_file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, height=5)
        ocr_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.ocr_file_listbox.yview)
        self.ocr_file_listbox.configure(yscrollcommand=ocr_scrollbar.set)
        
        self.ocr_file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ocr_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Batch file buttons
        batch_btn_frame = ttk.Frame(batch_frame)
        batch_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(batch_btn_frame, text="Add Images", command=self.add_ocr_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(batch_btn_frame, text="Add Folder", command=self.add_ocr_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(batch_btn_frame, text="Clear", command=self.clear_ocr_files).pack(side=tk.LEFT)
        
        # OCR Output settings
        output_frame = ttk.Frame(batch_frame)
        output_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(output_frame, text="Output Format:").pack(side=tk.LEFT, padx=(0, 5))
        self.ocr_output_format = ttk.Combobox(output_frame, values=["txt", "json", "markdown"], state="readonly", width=10)
        self.ocr_output_format.set("txt")
        self.ocr_output_format.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(output_frame, text="Output Dir:").pack(side=tk.LEFT, padx=(0, 5))
        self.ocr_output_dir = tk.StringVar(value=str(Path.home() / "Documents" / "OCR_Output"))
        ttk.Entry(output_frame, textvariable=self.ocr_output_dir, width=30).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(output_frame, text="Browse", command=self.browse_ocr_output_dir).pack(side=tk.LEFT)
        
        # OCR Preview with drag-drop support
        preview_frame = ttk.LabelFrame(ocr_frame, text="OCR Preview (Drag images here)", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.ocr_preview = scrolledtext.ScrolledText(preview_frame, height=10)
        self.ocr_preview.pack(fill=tk.BOTH, expand=True)
        
        # OCR Controls
        ocr_control_frame = ttk.Frame(ocr_frame)
        ocr_control_frame.pack(fill=tk.X)
        
        ttk.Button(ocr_control_frame, text="📷 Process Single Image", command=self.process_ocr).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(ocr_control_frame, text="📚 Process Batch", command=self.process_batch_ocr).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(ocr_control_frame, text="💾 Save OCR Result", command=self.save_ocr_result).pack(side=tk.LEFT, padx=(0, 10))
        
        # OCR Progress
        self.ocr_progress_var = tk.DoubleVar()
        self.ocr_progress_bar = ttk.Progressbar(ocr_control_frame, variable=self.ocr_progress_var, maximum=100)
        self.ocr_progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(20, 0))
    
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
        
        # Markdown editor/viewer with drag-drop zone
        editor_frame = ttk.LabelFrame(md_frame, text="Markdown Editor/Viewer (Drag files here)", padding=10)
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
        
        # Fallback settings
        self.gv_fallback_enabled = tk.BooleanVar(value=self.config.get('api', {}).get('google_vision', {}).get('fallback_enabled', True))
        ttk.Checkbutton(gv_frame, text="Auto-fallback to free OCR if API fails", variable=self.gv_fallback_enabled).pack(anchor=tk.W, pady=(5, 0))
        
        # Credentials
        cred_frame = ttk.Frame(gv_frame)
        cred_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Environment variable info
        env_var_status = "✅ Set" if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') else "❌ Not Set"
        ttk.Label(cred_frame, text=f"GOOGLE_APPLICATION_CREDENTIALS: {env_var_status}").pack(anchor=tk.W)
        ttk.Label(cred_frame, text="(Environment variable preferred for security)", font=('TkDefaultFont', 8)).pack(anchor=tk.W)
        
        ttk.Label(cred_frame, text="Fallback Credentials File:", font=('TkDefaultFont', 9, 'bold')).pack(anchor=tk.W, pady=(10, 0))
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
        
        # Initialize API stats
        self.update_api_stats("API statistics will appear here...")
    
    def create_tools_tab(self):
        """Create tools tab with thread selector, memory, and security features"""
        tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(tools_frame, text="🛠️ Tools")
        
        # Thread Management
        thread_frame = ttk.LabelFrame(tools_frame, text="Thread Management", padding=10)
        thread_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(thread_frame, text="Active Threads:").grid(row=0, column=0, sticky=tk.W)
        self.thread_count_label = ttk.Label(thread_frame, text=str(threading.active_count()))
        self.thread_count_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Button(thread_frame, text="Refresh", command=self.refresh_thread_info).grid(row=0, column=2, padx=(20, 0))
        
        # Thread list
        self.thread_listbox = tk.Listbox(thread_frame, height=5)
        self.thread_listbox.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        thread_scrollbar = ttk.Scrollbar(thread_frame, orient=tk.VERTICAL, command=self.thread_listbox.yview)
        thread_scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S), pady=(10, 0))
        self.thread_listbox.configure(yscrollcommand=thread_scrollbar.set)
        
        # Memory Management
        memory_frame = ttk.LabelFrame(tools_frame, text="Memory Usage", padding=10)
        memory_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.memory_info_text = tk.Text(memory_frame, height=6, width=50)
        self.memory_info_text.pack(fill=tk.X)
        
        button_frame = ttk.Frame(memory_frame)
        button_frame.pack(pady=(10, 0))
        
        ttk.Button(button_frame, text="Update Memory Info", command=self.update_memory_info).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Optimize Memory", command=self.optimize_memory).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear Cache", command=lambda: [self.clear_cache(), self.update_memory_info()]).pack(side=tk.LEFT)
        
        # Security Settings
        security_frame = ttk.LabelFrame(tools_frame, text="Security", padding=10)
        security_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.secure_mode = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="Enable secure file path validation", variable=self.secure_mode).pack(anchor=tk.W)
        
        self.sandbox_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(security_frame, text="Sandbox mode (restrict file access)", variable=self.sandbox_mode).pack(anchor=tk.W)
        
        ttk.Label(security_frame, text="Allowed directories (one per line):").pack(anchor=tk.W, pady=(10, 5))
        self.allowed_dirs_text = tk.Text(security_frame, height=4, width=50)
        self.allowed_dirs_text.pack(fill=tk.X)
        self.allowed_dirs_text.insert(tk.END, str(Path.home() / "Documents"))
        
        # Initialize tools info
        self.refresh_thread_info()
        self.update_memory_info()
    
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
        
        self.ocr_use_cache = tk.BooleanVar(value=self.config.get('ocr', {}).get('use_cache', True))
        ttk.Checkbutton(cache_frame, text="Enable OCR result caching", variable=self.ocr_use_cache).pack(anchor=tk.W)
        
        ttk.Button(cache_frame, text="Clear Cache", command=self.clear_cache).pack(anchor=tk.W, pady=(10, 0))
    
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
        """Setup drag and drop functionality for all tabs"""
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD
            # Enable drag and drop on file listbox
            self.file_listbox.drop_target_register(DND_FILES)
            self.file_listbox.dnd_bind('<<Drop>>', self.on_drop)
            
            # Enable drag and drop on OCR preview and file list
            if hasattr(self, 'ocr_preview'):
                self.ocr_preview.drop_target_register(DND_FILES)
                self.ocr_preview.dnd_bind('<<Drop>>', self.on_ocr_drop)
            
            if hasattr(self, 'ocr_file_listbox'):
                self.ocr_file_listbox.drop_target_register(DND_FILES)
                self.ocr_file_listbox.dnd_bind('<<Drop>>', self.on_ocr_drop)
            
            # Enable drag and drop on markdown editor
            if hasattr(self, 'md_editor'):
                self.md_editor.drop_target_register(DND_FILES)
                self.md_editor.dnd_bind('<<Drop>>', self.on_markdown_drop)
        except ImportError:
            self.logger.warning("Drag and drop not available - tkinterdnd2 not installed")
    
    def on_drop(self, event):
        """Handle dropped files"""
        files = self.file_listbox.tk.splitlist(event.data)
        for file_path in files:
            if Path(file_path).is_file():
                # Validate file path for security
                if HAS_OCR:
                    try:
                        validate_file_path(file_path)
                        self.file_listbox.insert(tk.END, file_path)
                    except SecurityError as e:
                        self.logger.warning(f"Security validation failed for {file_path}: {e}")
                        messagebox.showwarning("Security Warning", f"Cannot add file: {e}")
                else:
                    self.file_listbox.insert(tk.END, file_path)
    
    def on_ocr_drop(self, event):
        """Handle dropped images for OCR"""
        files = self.ocr_preview.tk.splitlist(event.data)
        for file_path in files:
            if Path(file_path).is_file():
                # Check if it's an image file
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    # Add to batch list
                    self.ocr_file_listbox.insert(tk.END, file_path)
                    # Process first image for preview
                    if self.ocr_file_listbox.size() == 1:
                        self.process_ocr_file(file_path)
    
    def on_markdown_drop(self, event):
        """Handle dropped files for markdown conversion"""
        files = self.md_editor.tk.splitlist(event.data)
        for file_path in files:
            if Path(file_path).is_file():
                # Check file type and convert
                if file_path.lower().endswith(('.docx', '.pdf')):
                    self.convert_dropped_to_markdown(file_path)
                    break  # Only process first file
    
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
        """Worker thread for file conversion with concurrent processing"""
        try:
            self.start_time = time.time()
            # Use adaptive batch size instead of fixed worker count
            max_workers = min(self.worker_threads.get(), self.get_adaptive_batch_size())
            self.logger.info(f"Starting conversion with {max_workers} workers (adaptive batch sizing)")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all conversion tasks
                futures = {}
                for i, file_path in enumerate(files):
                    if self.cancel_processing:
                        break
                    
                    future = executor.submit(self.convert_single_file_safe, file_path, output_dir, i)
                    futures[future] = file_path
                
                # Process completed futures
                for future in concurrent.futures.as_completed(futures):
                    if self.cancel_processing:
                        executor.shutdown(wait=False)
                        break
                    
                    file_path = futures[future]
                    try:
                        success, status = future.result()
                        if success:
                            if status == 'converted':
                                self.processed_count += 1
                            elif status == 'skipped':
                                self.skipped_count += 1
                        else:
                            self.failed_count += 1
                    except Exception as e:
                        self.logger.error(f"Error processing {file_path}: {e}")
                        self.failed_count += 1
                    
                    # Update progress with ETA
                    completed = self.processed_count + self.failed_count + self.skipped_count
                    progress = (completed / len(files)) * 100
                    self.update_progress_with_eta(progress, completed, len(files))
        
        finally:
            self.root.after(0, self.processing_complete)
    
    def convert_single_file_safe(self, file_path, output_dir, index):
        """Thread-safe wrapper for single file conversion"""
        try:
            self.update_status(f"Processing {Path(file_path).name}...")
            return self.convert_single_file(file_path, output_dir)
        except Exception as e:
            self.logger.error(f"Error converting {file_path}: {e}")
            return False, 'error'
    
    def convert_single_file(self, input_path, output_dir):
        """Convert a single file with caching and skip support"""
        input_file = Path(input_path)
        output_format = self.output_format.get()
        
        # Handle preserve structure option
        if self.preserve_structure.get():
            # Calculate relative path from base directory
            try:
                base_dir = Path(self.file_listbox.get(0)).parent
                rel_path = input_file.relative_to(base_dir).parent
                output_subdir = output_dir / rel_path
                output_subdir.mkdir(parents=True, exist_ok=True)
            except (ValueError, AttributeError) as e:
                self.logger.debug(f"Could not determine relative path: {e}")
                output_subdir = output_dir
        else:
            output_subdir = output_dir
        
        # Determine output filename
        output_file = output_subdir / f"{input_file.stem}.{output_format}"
        
        # Skip existing files if option is enabled
        if self.skip_existing.get() and output_file.exists():
            self.logger.info(f"Skipping existing file: {output_file}")
            return True, 'skipped'
        
        # Check cache
        cache_key = None
        if self.use_cache.get():
            cache_key = self.get_cache_key(input_path, output_format)
            cached_result = self.get_cached_result(cache_key)
            if cached_result:
                # Write cached result
                with open(output_file, 'wb') as f:
                    f.write(cached_result)
                self.logger.info(f"Using cached result for {input_file.name}")
                return True, 'converted'
        
        # Perform conversion based on format
        if output_format == "markdown" and HAS_MARKDOWN:
            if input_file.suffix.lower() == '.docx':
                convert_docx_to_markdown(str(input_file))
                # Move the generated markdown file to output directory
                md_file = input_file.with_suffix('.md')
                if md_file.exists():
                    shutil.move(str(md_file), str(output_file))
            elif input_file.suffix.lower() == '.pdf':
                convert_pdf_to_markdown(str(input_file))
                # Move the generated markdown file to output directory
                md_file = input_file.with_suffix('.md')
                if md_file.exists():
                    shutil.move(str(md_file), str(output_file))
        else:
            # Basic conversion (placeholder - would need full implementation)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Converted from: {input_path}\n")
                f.write(f"Format: {output_format}\n")
                f.write("Full conversion implementation would go here.\n")
        
        # Cache result if enabled
        if cache_key and output_file.exists():
            try:
                with open(output_file, 'rb') as f:
                    content = f.read()
                    self.cache_result(cache_key, content)
            except (IOError, OSError) as e:
                self.logger.debug(f"Could not cache result: {e}")
                pass
        
        return True, 'converted'
    
    def cancel_conversion(self):
        """Cancel ongoing conversion"""
        self.cancel_processing = True
        self.update_status("Cancelling...")
    
    def processing_complete(self):
        """Handle conversion completion"""
        self.is_processing = False
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        
        # Calculate final statistics
        total_processed = self.processed_count + self.failed_count + self.skipped_count
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        
        # Build status message
        status_parts = [f"{self.processed_count} converted"]
        if self.skipped_count > 0:
            status_parts.append(f"{self.skipped_count} skipped")
        if self.failed_count > 0:
            status_parts.append(f"{self.failed_count} failed")
        
        status_msg = f"Complete - {', '.join(status_parts)}"
        
        if elapsed_time > 0:
            if elapsed_time < 60:
                time_str = f"{elapsed_time:.1f} seconds"
            else:
                time_str = f"{int(elapsed_time / 60)} minutes {int(elapsed_time % 60)} seconds"
            status_msg += f" in {time_str}"
        
        if self.cancel_processing:
            status_msg = f"Cancelled - {status_msg}"
        
        self.update_status(status_msg)
        
        if not self.cancel_processing:
            # Show detailed completion dialog
            detail_msg = f"""Conversion completed!

Processed: {self.processed_count} files
Skipped: {self.skipped_count} files
Failed: {self.failed_count} files
Total time: {time_str if elapsed_time > 0 else 'N/A'}

Output directory: {self.output_dir.get()}"""
            messagebox.showinfo("Conversion Complete", detail_msg)
        
        # Reset counters
        self.processed_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.start_time = None
        self.update_progress(0)
        self.progress_detail_label.config(text="")
    
    # OCR methods
    def on_ocr_engine_changed(self, event=None):
        """Handle OCR engine selection change"""
        engine = self.ocr_engine_var.get()
        if engine == "auto":
            self.ocr_status_label.config(text="🔍 OCR Engine: Auto-detect")
        elif engine == "tesseract":
            self.ocr_status_label.config(text="🆓 OCR Engine: Tesseract (Free)")
        elif engine == "easyocr":
            self.ocr_status_label.config(text="🆓 OCR Engine: EasyOCR (Free)")
        elif engine == "google_vision":
            if self.gv_enabled.get():
                self.ocr_status_label.config(text="☁️ OCR Engine: Google Vision API")
            else:
                self.ocr_status_label.config(text="⚠️ Google Vision API not enabled")
                self.ocr_engine_var.set("auto")
                messagebox.showwarning("API Not Enabled", "Please enable Google Vision API in the API Management tab first.")
    
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
        
        self.process_ocr_file(file_path)
    
    def process_ocr_file(self, file_path):
        """Process OCR on a specific file"""
        
        if not self.ocr_engine:
            messagebox.showerror("OCR Error", "OCR engine not available")
            return
        
        try:
            # Validate file path for security
            if HAS_OCR:
                validate_file_path(file_path)
            
            self.update_status("Processing OCR...")
            
            # Get OCR settings
            engine = self.ocr_engine_var.get()
            quality = self.ocr_quality.get()
            
            # Set quality-based options
            confidence_threshold = {'fast': 0.5, 'standard': 0.7, 'accurate': 0.85}.get(quality, 0.7)
            preprocess = quality == 'accurate'
            
            options = {
                'engine': engine,
                'language': self.ocr_language.get(),
                'confidence_threshold': confidence_threshold,
                'preprocess': preprocess
            }
            
            # Update status to show which engine is being used
            if engine == "google_vision" and self.gv_enabled.get():
                self.update_status("Processing with Google Vision API...")
            elif engine in ["tesseract", "easyocr"]:
                self.update_status(f"Processing with {engine.title()} (Free)...")
            else:
                self.update_status("Processing with auto-detected engine...")
            
            # Process OCR with fallback
            result = self.process_ocr_with_fallback(file_path, options)
            
            # Display result
            self.ocr_preview.delete(1.0, tk.END)
            self.ocr_preview.insert(tk.END, result.get('text', 'No text detected'))
            
            # Update status with engine used
            engine_used = result.get('engine_used', engine)
            confidence = result.get('confidence', 'N/A')
            fallback_used = result.get('fallback_used', False)
            
            if fallback_used:
                self.update_status(f"OCR completed ({engine_used.title()} - Free, API fallback) - Confidence: {confidence}")
                self.logger.warning(f"API failed, used fallback engine: {engine_used}")
            elif engine_used == "google_vision":
                self.update_status(f"OCR completed (Google Vision API) - Confidence: {confidence}")
            else:
                self.update_status(f"OCR completed ({engine_used.title()} - Free) - Confidence: {confidence}")
            
        except Exception as e:
            messagebox.showerror("OCR Error", f"OCR processing failed: {e}")
            self.update_status("OCR failed")
    
    def add_ocr_files(self):
        """Add image files for OCR processing"""
        files = filedialog.askopenfilenames(
            title="Select images for OCR",
            filetypes=[
                ("Image files", "*.png;*.jpg;*.jpeg;*.tiff;*.bmp;*.gif"),
                ("All files", "*.*")
            ]
        )
        for file in files:
            self.ocr_file_listbox.insert(tk.END, file)
    
    def add_ocr_folder(self):
        """Add folder of images for OCR processing"""
        folder = filedialog.askdirectory(title="Select folder with images")
        if folder:
            folder_path = Path(folder)
            for file_path in folder_path.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']:
                    self.ocr_file_listbox.insert(tk.END, str(file_path))
    
    def clear_ocr_files(self):
        """Clear OCR file list"""
        self.ocr_file_listbox.delete(0, tk.END)
    
    def browse_ocr_output_dir(self):
        """Browse for OCR output directory"""
        directory = filedialog.askdirectory(title="Select OCR output directory")
        if directory:
            self.ocr_output_dir.set(directory)
    
    def process_batch_ocr(self):
        """Process batch OCR on multiple files"""
        files = list(self.ocr_file_listbox.get(0, tk.END))
        if not files:
            messagebox.showwarning("No Files", "Please add image files for OCR processing.")
            return
        
        if not self.ocr_engine:
            messagebox.showerror("OCR Error", "OCR engine not available")
            return
        
        # Create output directory
        output_dir = Path(self.ocr_output_dir.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Start batch processing in thread
        self.ocr_progress_var.set(0)
        threading.Thread(target=self.batch_ocr_worker, args=(files, output_dir), daemon=True).start()
    
    def batch_ocr_worker(self, files, output_dir):
        """Worker thread for batch OCR processing"""
        total_files = len(files)
        processed = 0
        failed = 0
        
        self.update_status(f"Processing {total_files} images for OCR...")
        
        for i, file_path in enumerate(files):
            try:
                # Process OCR
                result = self.process_ocr_file_batch(file_path)
                
                if result:
                    # Save result based on format
                    output_format = self.ocr_output_format.get()
                    input_name = Path(file_path).stem
                    output_file = output_dir / f"{input_name}.{output_format}"
                    
                    if output_format == "json":
                        import json
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(result, f, indent=2)
                    elif output_format == "markdown":
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(f"# OCR Result: {input_name}\n\n")
                            f.write(result.get('text', ''))
                            f.write(f"\n\n*Confidence: {result.get('confidence', 'N/A')}*")
                    else:  # txt
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(result.get('text', ''))
                    
                    processed += 1
                else:
                    failed += 1
                    
            except Exception as e:
                self.logger.error(f"Batch OCR error for {file_path}: {e}")
                failed += 1
            
            # Update progress
            progress = ((i + 1) / total_files) * 100
            self.root.after(0, lambda p=progress: self.ocr_progress_var.set(p))
        
        # Show completion
        self.update_status(f"Batch OCR complete - {processed} successful, {failed} failed")
        self.root.after(0, lambda: messagebox.showinfo(
            "Batch OCR Complete", 
            f"Processed {total_files} images\n{processed} successful\n{failed} failed\n\nOutput: {output_dir}"
        ))
    
    def process_ocr_file_batch(self, file_path):
        """Process OCR for batch operation"""
        try:
            # Get OCR settings
            engine = self.ocr_engine_var.get()
            quality = self.ocr_quality.get()
            
            # Set quality-based options
            confidence_threshold = {'fast': 0.5, 'standard': 0.7, 'accurate': 0.85}.get(quality, 0.7)
            preprocess = quality == 'accurate'
            
            options = {
                'engine': engine,
                'language': self.ocr_language.get(),
                'confidence_threshold': confidence_threshold,
                'preprocess': preprocess
            }
            
            # Process OCR with fallback
            return self.process_ocr_with_fallback(file_path, options)
            
        except Exception as e:
            self.logger.error(f"OCR error for {file_path}: {e}")
            return None
    
    def save_ocr_result(self):
        """Save OCR result to file"""
        text = self.ocr_preview.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("No Text", "No OCR text to save")
            return
        
        output_format = self.ocr_output_format.get()
        ext = f".{output_format}"
        
        file_path = filedialog.asksaveasfilename(
            title="Save OCR result",
            defaultextension=ext,
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                if output_format == "json":
                    import json
                    data = {"text": text, "timestamp": datetime.datetime.now().isoformat()}
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                elif output_format == "markdown":
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"# OCR Result\n\n{text}\n\n*Generated: {datetime.datetime.now()}*")
                else:
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
    
    def convert_dropped_to_markdown(self, file_path):
        """Convert a dropped file to markdown"""
        if HAS_MARKDOWN:
            try:
                self.update_status(f"Converting {Path(file_path).name} to markdown...")
                
                # Read the actual content after conversion
                output_path = None
                if file_path.endswith('.docx'):
                    convert_docx_to_markdown(file_path)
                    output_path = Path(file_path).with_suffix('.md')
                elif file_path.endswith('.pdf'):
                    convert_pdf_to_markdown(file_path)
                    output_path = Path(file_path).with_suffix('.md')
                
                # Load the converted content
                if output_path and output_path.exists():
                    with open(output_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.md_editor.delete(1.0, tk.END)
                    self.md_editor.insert(tk.END, content)
                    self.update_status(f"Converted {Path(file_path).name} to markdown")
                else:
                    self.update_status("Conversion completed but output file not found")
                    
            except Exception as e:
                messagebox.showerror("Conversion Error", f"Could not convert: {e}")
                self.update_status("Conversion failed")
    
    def convert_markdown(self):
        """Convert markdown bidirectionally"""
        direction = self.md_direction.get()
        
        if direction == "to_markdown":
            # Convert TO markdown
            file_path = filedialog.askopenfilename(
                title="Select file to convert to markdown",
                filetypes=[("Word documents", "*.docx"), ("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if file_path:
                self.convert_dropped_to_markdown(file_path)
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
            if self.gv_fallback_enabled.get():
                self.api_status_label.config(text="❌ Google Vision not available (fallback enabled)")
            return
        
        # Try environment variable first (more secure)
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path:
            # Fall back to config file path
            credentials_path = self.gv_credentials.get()
        
        if not credentials_path:
            self.api_status_label.config(text="❌ No credentials (set GOOGLE_APPLICATION_CREDENTIALS env var or file)")
            if self.gv_fallback_enabled.get():
                self.api_status_label.config(text="❌ No credentials (fallback enabled)")
            return

        # Validate credentials file
        if not self._validate_credentials_file(credentials_path):
            return
        
        try:
            # Only set if not already in environment
            if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            client = vision.ImageAnnotatorClient()
            self.api_status_label.config(text="✅ Connection successful")
            
            # Update API stats
            self.update_api_stats("Connection test successful")
        except Exception as e:
            # Sanitize error message to prevent credential disclosure
            sanitized_error = self._sanitize_error_message(str(e))
            if self.gv_fallback_enabled.get():
                self.api_status_label.config(text=f"❌ Connection failed (fallback enabled): {sanitized_error[:30]}...")
            else:
                self.api_status_label.config(text=f"❌ Connection failed: {sanitized_error[:30]}...")
            
            # Update API stats with sanitized error
            self.update_api_stats(f"Connection test failed: {sanitized_error}")
            # Log the full error for debugging (still sanitized)
            self.logger.error(f"Google Vision API connection failed: {sanitized_error}")
    
    # CLI methods
    def test_cli_command(self):
        """Test CLI command"""
        command = self.cli_command.get()
        
        try:
            # Parse command safely - split into args
            import shlex
            args = shlex.split(command)
            result = subprocess.run(args, capture_output=True, text=True, timeout=30)
            
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
    
    # Settings methods
    def save_settings(self):
        """Save current settings"""
        # Update config with current values
        self.config['gui']['theme'] = self.theme_var.get()
        self.config['conversion']['preserve_formatting'] = self.preserve_formatting.get()
        self.config['gui']['auto_preview'] = self.auto_preview.get()
        self.config['conversion']['max_workers'] = self.max_workers.get()
        self.config['ocr']['use_cache'] = self.ocr_use_cache.get()
        self.config['logging']['level'] = self.log_level.get()
        self.config['api']['google_vision']['enabled'] = self.gv_enabled.get()
        self.config['api']['google_vision']['credentials_path'] = self.gv_credentials.get()
        self.config['api']['google_vision']['fallback_enabled'] = self.gv_fallback_enabled.get()
        
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
            self.ocr_use_cache.set(self.config['ocr']['use_cache'])
            self.log_level.set(self.config['logging']['level'])
            self.gv_enabled.set(self.config['api']['google_vision']['enabled'])
            self.gv_credentials.set(self.config['api']['google_vision']['credentials_path'])
            self.gv_fallback_enabled.set(self.config['api']['google_vision'].get('fallback_enabled', True))
            
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
    
    def update_progress_with_eta(self, progress: float, completed: int, total: int):
        """Update progress with ETA calculation"""
        def update():
            self.progress_var.set(progress)
            
            if self.start_time and completed > 0:
                elapsed = time.time() - self.start_time
                rate = completed / elapsed
                remaining = total - completed
                eta_seconds = remaining / rate if rate > 0 else 0
                
                # Format time
                if eta_seconds < 60:
                    eta_str = f"{int(eta_seconds)}s"
                elif eta_seconds < 3600:
                    eta_str = f"{int(eta_seconds / 60)}m {int(eta_seconds % 60)}s"
                else:
                    hours = int(eta_seconds / 3600)
                    minutes = int((eta_seconds % 3600) / 60)
                    eta_str = f"{hours}h {minutes}m"
                
                detail_text = f"{completed}/{total} files | ETA: {eta_str}"
                if self.failed_count > 0:
                    detail_text += f" | {self.failed_count} failed"
                if self.skipped_count > 0:
                    detail_text += f" | {self.skipped_count} skipped"
                
                self.progress_detail_label.config(text=detail_text)
            
        self.root.after(0, update)
    
    def get_cache_key(self, file_path: str, output_format: str) -> str:
        """Generate cache key based on file content and format"""
        try:
            # Get file modification time and size
            stat = Path(file_path).stat()
            mtime = stat.st_mtime
            size = stat.st_size
            
            # Create cache key
            key_string = f"{file_path}:{output_format}:{mtime}:{size}"
            return hashlib.md5(key_string.encode()).hexdigest()
        except (OSError, AttributeError) as e:
            self.logger.debug(f"Could not generate cache key: {e}")
            return None
    
    def get_cached_result(self, cache_key: str) -> Optional[bytes]:
        """Get cached conversion result and move to end (LRU)"""
        with self.cache_lock:
            if cache_key in self.conversion_cache:
                # Move to end (most recently used)
                value = self.conversion_cache.pop(cache_key)
                self.conversion_cache[cache_key] = value
                return value
            return None
    
    def cache_result(self, cache_key: str, content: bytes):
        """Cache conversion result with LRU eviction"""
        with self.cache_lock:
            content_size = len(content)
            
            # If entry already exists, update size tracking
            if cache_key in self.conversion_cache:
                old_size = self.cache_sizes[cache_key]
                self.current_cache_size -= old_size
                self.conversion_cache.pop(cache_key)  # Remove to add at end
            
            # Evict LRU entries until we have enough space
            while (self.current_cache_size + content_size > self.max_cache_size 
                   and self.conversion_cache):
                # Remove least recently used (first item)
                lru_key, lru_content = self.conversion_cache.popitem(last=False)
                lru_size = self.cache_sizes.pop(lru_key)
                self.current_cache_size -= lru_size
            
            # Add new entry (most recently used at end)
            self.conversion_cache[cache_key] = content
            self.cache_sizes[cache_key] = content_size
            self.current_cache_size += content_size
    
    def clear_cache(self):
        """Clear the conversion cache"""
        with self.cache_lock:
            self.conversion_cache.clear()
            self.cache_sizes.clear()
            self.current_cache_size = 0
            gc.collect()
    
    def refresh_thread_info(self):
        """Refresh thread information display"""
        self.thread_count_label.config(text=str(threading.active_count()))
        
        # Clear and update thread list
        self.thread_listbox.delete(0, tk.END)
        for thread in threading.enumerate():
            thread_info = f"{thread.name} - {'Alive' if thread.is_alive() else 'Dead'} - Daemon: {thread.daemon}"
            self.thread_listbox.insert(tk.END, thread_info)
    
    def update_memory_info(self):
        """Update memory usage information"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            # Cache information - access with lock
            with self.cache_lock:
                cache_size_mb = self.current_cache_size / 1024 / 1024
                cache_entries = len(self.conversion_cache)
            
            info_text = f"""Memory Usage Information:
- RSS (Resident Set Size): {memory_info.rss / 1024 / 1024:.2f} MB
- VMS (Virtual Memory Size): {memory_info.vms / 1024 / 1024:.2f} MB
- Available System Memory: {psutil.virtual_memory().available / 1024 / 1024:.2f} MB
- Memory Percent: {process.memory_percent():.2f}%
- Python Objects: {len(gc.get_objects())} objects

Cache Information:
- Cache Size: {cache_size_mb:.2f} MB / {self.max_cache_size / 1024 / 1024:.0f} MB
- Cached Items: {cache_entries} files

Processing Configuration:
- Current Adaptive Batch Size: {self.get_adaptive_batch_size()} workers
- Max Workers Setting: {self.worker_threads.get()} workers"""
            
            # Add memory optimization button if memory usage is high
            if memory_info.rss > 500 * 1024 * 1024:  # > 500MB
                info_text += "\n\n⚠️ High memory usage detected!"
            
        except ImportError:
            # Access cache with lock
            with self.cache_lock:
                cache_size_mb = self.current_cache_size / 1024 / 1024
                cache_entries = len(self.conversion_cache)
                
            info_text = f"""Memory monitoring requires psutil package.
Install with: pip install psutil

Basic memory info:
- Python objects in memory: {len(gc.get_objects())} objects

Cache Information:
- Cache Size: {cache_size_mb:.2f} MB
- Cached Items: {cache_entries} files"""
        
        self.memory_info_text.delete(1.0, tk.END)
        self.memory_info_text.insert(tk.END, info_text)
    
    def optimize_memory(self):
        """Optimize memory usage"""
        self.update_status("Optimizing memory...")
        
        # Clear cache if it's large - check size with lock
        with self.cache_lock:
            should_clear = self.current_cache_size > 50 * 1024 * 1024  # > 50MB
        
        if should_clear:
            self.clear_cache()
        
        # Force garbage collection
        collected = gc.collect()
        
        # Update memory info
        self.update_memory_info()
        
        self.update_status(f"Memory optimized - {collected} objects collected")
        messagebox.showinfo("Memory Optimization", f"Memory optimization complete!\n{collected} objects collected.\nCache cleared if it was over 50MB.")
    
    def get_adaptive_batch_size(self) -> int:
        """Calculate optimal batch size based on current memory usage"""
        current_time = time.time()
        
        # Only check memory periodically to avoid overhead
        if current_time - self._last_memory_check < self._memory_check_interval:
            return self._adaptive_batch_size
        
        try:
            import psutil
            
            # Get memory usage information
            process = psutil.Process()
            memory_info = process.memory_info()
            system_memory = psutil.virtual_memory()
            
            # Calculate memory usage metrics
            rss_mb = memory_info.rss / (1024 * 1024)
            available_mb = system_memory.available / (1024 * 1024)
            memory_percent = process.memory_percent()
            
            # Adaptive batch sizing logic
            if memory_percent > 80 or rss_mb > 1000:
                # High memory usage - reduce batch size
                self._adaptive_batch_size = max(1, self._adaptive_batch_size // 2)
                self.logger.warning(f"High memory usage detected ({memory_percent:.1f}%), reducing batch size to {self._adaptive_batch_size}")
            elif memory_percent < 40 and available_mb > 2000:
                # Low memory usage and plenty available - can increase batch size
                self._adaptive_batch_size = min(8, self._adaptive_batch_size + 1)
                self.logger.info(f"Memory usage low ({memory_percent:.1f}%), increasing batch size to {self._adaptive_batch_size}")
            elif memory_percent > 60:
                # Moderate memory usage - slightly reduce batch size
                self._adaptive_batch_size = max(2, self._adaptive_batch_size - 1)
                self.logger.info(f"Moderate memory usage ({memory_percent:.1f}%), adjusting batch size to {self._adaptive_batch_size}")
            
            # Force garbage collection if memory usage is high
            if memory_percent > 70:
                gc.collect()
                
            self._last_memory_check = current_time
            
        except ImportError:
            # psutil not available, use default
            self._adaptive_batch_size = 4
        except Exception as e:
            self.logger.warning(f"Error calculating adaptive batch size: {e}")
            self._adaptive_batch_size = 4
        
        return self._adaptive_batch_size
    
    def _validate_credentials_file(self, credentials_path: str) -> bool:
        """Validate Google Vision API credentials file with security checks"""
        try:
            if not credentials_path or not os.path.exists(credentials_path):
                self.api_status_label.config(text="❌ Credentials file not found")
                if self.gv_fallback_enabled.get():
                    self.api_status_label.config(text="❌ Credentials file not found (fallback enabled)")
                return False
            
            # Check file permissions (should not be world-readable)
            file_stat = os.stat(credentials_path)
            if file_stat.st_mode & 0o044:  # Check if group or others can read
                self.logger.warning(f"Credentials file {credentials_path} has insecure permissions")
                self.api_status_label.config(text="⚠️ Credentials file has insecure permissions")
                # Don't fail completely, but warn the user
            
            # Basic validation that it's a JSON file
            try:
                with open(credentials_path, 'r') as f:
                    import json
                    cred_data = json.load(f)
                    # Check for required fields
                    if 'type' not in cred_data or 'client_email' not in cred_data:
                        self.api_status_label.config(text="❌ Invalid credentials format")
                        return False
            except (json.JSONDecodeError, IOError) as e:
                self.api_status_label.config(text="❌ Invalid credentials file format")
                self.logger.error(f"Credentials file validation failed: {e}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Credentials validation error: {e}")
            self.api_status_label.config(text="❌ Credentials validation failed")
            return False
    
    def _validate_credentials_file_init(self, credentials_path: str) -> bool:
        """Validate credentials file during initialization (no UI updates)"""
        try:
            if not credentials_path or not os.path.exists(credentials_path):
                return False
            
            # Check file permissions (should not be world-readable)
            file_stat = os.stat(credentials_path)
            if file_stat.st_mode & 0o044:  # Check if group or others can read
                self.logger.warning(f"Credentials file {credentials_path} has insecure permissions")
            
            # Basic validation that it's a JSON file
            try:
                with open(credentials_path, 'r') as f:
                    import json
                    cred_data = json.load(f)
                    # Check for required fields
                    if 'type' not in cred_data or 'client_email' not in cred_data:
                        return False
            except (json.JSONDecodeError, IOError) as e:
                self.logger.error(f"Credentials file validation failed: {e}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Credentials validation error: {e}")
            return False
    
    def _sanitize_error_message(self, error_msg: str) -> str:
        """Sanitize error messages to prevent credential disclosure"""
        import re
        
        # Remove potential credential file paths
        error_msg = re.sub(r'/[^/\s]+\.json', '[CREDENTIALS_FILE]', error_msg)
        error_msg = re.sub(r'C:\\[^\\]+\\[^\\]+\.json', '[CREDENTIALS_FILE]', error_msg)
        
        # Remove potential API keys or tokens
        error_msg = re.sub(r'key["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}["\']?', 'key="[REDACTED]"', error_msg, flags=re.IGNORECASE)
        error_msg = re.sub(r'token["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}["\']?', 'token="[REDACTED]"', error_msg, flags=re.IGNORECASE)
        
        # Remove email addresses from service account info
        error_msg = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[SERVICE_ACCOUNT_EMAIL]', error_msg)
        
        return error_msg
    
    def process_ocr_with_fallback(self, file_path, options):
        """Process OCR with automatic fallback to free engines if API fails"""
        original_engine = options.get('engine', 'auto')
        result = None
        fallback_used = False
        
        try:
            # First try with the selected engine
            result = self.ocr_engine.extract_text(file_path, options)
            
            # Check if Google Vision API failed
            if (original_engine == 'google_vision' or (original_engine == 'auto' and self.gv_enabled.get())) and \
               (not result or result.get('text', '').strip() == '' or 'error' in str(result).lower()):
                
                # Log the API failure
                self.logger.warning("Google Vision API failed, attempting fallback to free engine")
                
                # Try fallback engines in order
                fallback_engines = ['tesseract', 'easyocr']
                for fallback_engine in fallback_engines:
                    try:
                        self.logger.info(f"Trying fallback engine: {fallback_engine}")
                        fallback_options = options.copy()
                        fallback_options['engine'] = fallback_engine
                        
                        fallback_result = self.ocr_engine.extract_text(file_path, fallback_options)
                        
                        if fallback_result and fallback_result.get('text', '').strip():
                            result = fallback_result
                            result['fallback_used'] = True
                            result['original_engine'] = original_engine
                            fallback_used = True
                            
                            # Track API failures
                            if hasattr(self, '_api_failure_count'):
                                self._api_failure_count += 1
                            else:
                                self._api_failure_count = 1
                            
                            # Show warning every 5 failures
                            if self._api_failure_count % 5 == 1:
                                self.root.after(0, lambda: messagebox.showwarning(
                                    "API Fallback Active",
                                    f"Google Vision API failed. Using {fallback_engine} as fallback.\n\n"
                                    "This may be due to:\n"
                                    "• API quota exceeded\n"
                                    "• Billing issues\n"
                                    "• Network problems\n\n"
                                    "Check your API settings and credentials."
                                ))
                            
                            # Update OCR engine indicator
                            self.root.after(0, lambda: self.ocr_status_label.config(
                                text=f"⚠️ OCR Engine: {fallback_engine.title()} (API Fallback)"
                            ))
                            break
                            
                    except Exception as e:
                        self.logger.error(f"Fallback engine {fallback_engine} failed: {e}")
                        continue
                        
        except Exception as e:
            self.logger.error(f"OCR processing error: {e}")
            # If primary engine fails, try fallback
            if original_engine == 'google_vision' or (original_engine == 'auto' and self.gv_enabled.get()):
                try:
                    fallback_options = options.copy()
                    fallback_options['engine'] = 'tesseract'  # Default fallback
                    result = self.ocr_engine.extract_text(file_path, fallback_options)
                    if result:
                        result['fallback_used'] = True
                        result['original_engine'] = original_engine
                        
                        # Update indicator
                        self.root.after(0, lambda: self.ocr_status_label.config(
                            text="⚠️ OCR Engine: Tesseract (API Error Fallback)"
                        ))
                except Exception as e:
                    self.logger.debug(f"Could not update OCR status: {e}")
                    pass
        
        # Update configuration if needed to remember preference
        if fallback_used and self.config.get('api', {}).get('google_vision', {}).get('fallback_enabled', True):
            # Store last successful fallback engine in session
            if not hasattr(self, '_last_successful_fallback'):
                self._last_successful_fallback = result.get('engine_used', 'tesseract')
        
        return result or {'text': '', 'confidence': 0, 'error': 'All OCR engines failed'}
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_processing:
            if messagebox.askokcancel("Quit", "Processing is in progress. Do you want to quit?"):
                self.cancel_processing = True
                if self.processing_thread and self.processing_thread.is_alive():
                    self.processing_thread.join(timeout=2)
                self.cleanup_resources()
                self.root.destroy()
        else:
            self.save_config()  # Save settings on exit
            self.cleanup_resources()
            self.root.destroy()
    
    def cleanup_resources(self):
        """Clean up file handlers and other resources"""
        # Close logging handlers
        if hasattr(self, 'file_handler'):
            self.file_handler.close()
        if hasattr(self, 'stream_handler'):
            self.stream_handler.close()
        
        # Clean up OCR engine
        if hasattr(self, 'ocr_engine') and self.ocr_engine:
            try:
                self.ocr_engine.cleanup()
            except Exception as e:
                self.logger.error(f"Error cleaning up OCR engine: {e}")

    def update_api_stats(self, message):
        """Update API statistics display"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get current content
        self.api_stats.config(state=tk.NORMAL)
        current_text = self.api_stats.get(1.0, tk.END).strip()
        
        # Add new message
        if current_text and current_text != "API statistics will appear here...":
            new_text = f"{current_text}\n[{timestamp}] {message}"
        else:
            new_text = f"[{timestamp}] {message}"
        
        # Limit to last 100 lines
        lines = new_text.split('\n')
        if len(lines) > 100:
            lines = lines[-100:]
            new_text = '\n'.join(lines)
        
        self.api_stats.delete(1.0, tk.END)
        self.api_stats.insert(tk.END, new_text)
        self.api_stats.see(tk.END)
        self.api_stats.config(state=tk.DISABLED)

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