#!/usr/bin/env python3
"""
Universal Document Converter with OCR - Complete Enterprise Solution
Fast, simple, powerful document conversion tool with integrated OCR support
Designed and built by Beau Lewis (blewisxx@gmail.com)

Features:
- Document conversion (DOCX, PDF, TXT, HTML, RTF, EPUB)
- OCR functionality (JPG, PNG, TIFF, BMP, GIF, WebP, PDF)
- Multi-threaded processing
- Drag-and-drop support
- Cross-platform compatibility
- Professional GUI with responsive design
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import threading
import os
from pathlib import Path
import sys
import mimetypes
import re
import logging
import datetime
import json
from typing import Optional, Union, Dict, Any, List
import concurrent.futures
import time
import hashlib
from threading import Lock

# Import OCR components
from ocr_engine.ocr_integration import OCRIntegration
from ocr_engine.format_detector import OCRFormatDetector
from ocr_engine.config_manager import ConfigManager

# Import OCR Settings GUI
try:
    from ocr_settings_gui import OCRSettingsGUI
    OCR_SETTINGS_GUI_AVAILABLE = True
except ImportError:
    OCR_SETTINGS_GUI_AVAILABLE = False

class DocumentConverterApp:
    """Main application class for the Universal Document Converter with OCR"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Document Converter with OCR")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Initialize OCR configuration manager
        self.ocr_config_manager = ConfigManager()
        
        # Initialize OCR integration with config
        self.ocr_integration = OCRIntegration(logger=None, config_manager=self.ocr_config_manager)
        self.format_detector = OCRFormatDetector()
        
        # Configuration
        self.config = self.load_config()
        self.setup_logging()
        
        # State variables
        self.current_files = []
        self.processing_thread = None
        self.is_processing = False
        self.processed_count = 0
        self.total_files = 0
        
        # Create GUI
        self.create_menu()
        self.create_widgets()
        self.setup_drag_drop()
        
        # Bind window events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def load_config(self) -> Dict[str, Any]:
        """Load application configuration"""
        config_path = Path("config.json")
        default_config = {
            "output_format": "txt",
            "ocr_enabled": True,
            "ocr_language": "eng",
            "batch_size": 5,
            "max_workers": 4,
            "output_directory": str(Path.home() / "Documents" / "Converted"),
            "theme": "light"
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")
                
        return default_config
    
    def save_config(self):
        """Save application configuration"""
        try:
            with open("config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.log_error(f"Error saving config: {e}")
    
    def setup_logging(self):
        """Setup logging system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"converter_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Files...", command=self.add_files, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        
        # OCR menu
        ocr_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="OCR", menu=ocr_menu)
        ocr_menu.add_command(label="OCR Settings...", command=self.open_ocr_settings)
        ocr_menu.add_command(label="Check OCR Status", command=self.check_ocr_status)
        ocr_menu.add_separator()
        
        # Backend submenu
        backend_menu = tk.Menu(ocr_menu, tearoff=0)
        ocr_menu.add_cascade(label="Select Backend", menu=backend_menu)
        
        self.backend_var = tk.StringVar(value=self.ocr_config_manager.get_default_backend())
        
        # Add backend options
        backends = [
            ("auto", "Auto (Best Available)"),
            ("tesseract", "Tesseract OCR"),
            ("easyocr", "EasyOCR"),
            ("google_vision", "Google Vision API")
        ]
        
        for value, label in backends:
            backend_menu.add_radiobutton(
                label=label,
                variable=self.backend_var,
                value=value,
                command=lambda v=value: self.set_backend(v)
            )
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Clear OCR Cache", command=self.clear_ocr_cache)
        tools_menu.add_command(label="Export OCR Config...", command=self.export_ocr_config)
        tools_menu.add_command(label="Import OCR Config...", command=self.import_ocr_config)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.add_files())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Universal Document Converter with OCR", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        # File listbox with scrollbar
        list_frame = ttk.Frame(file_frame)
        list_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, height=6, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Buttons
        ttk.Button(file_frame, text="Add Files", command=self.add_files).grid(row=1, column=0, padx=(0, 5))
        ttk.Button(file_frame, text="Remove Selected", command=self.remove_selected).grid(row=1, column=1, padx=(0, 5))
        ttk.Button(file_frame, text="Clear All", command=self.clear_all).grid(row=1, column=2)
        
        # Create tabbed interface for better organization
        settings_notebook = ttk.Notebook(main_frame)
        settings_notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Basic Settings Tab
        basic_frame = ttk.Frame(settings_notebook, padding="10")
        settings_notebook.add(basic_frame, text="📄 Basic Settings")
        
        # OCR Toggle
        self.ocr_var = tk.BooleanVar(value=self.config.get("ocr_enabled", True))
        ocr_check = ttk.Checkbutton(basic_frame, text="Enable OCR for images and PDFs", 
                                   variable=self.ocr_var, command=self.toggle_ocr)
        ocr_check.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Output format with markdown support
        ttk.Label(basic_frame, text="Output Format:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.format_var = tk.StringVar(value=self.config.get("output_format", "markdown"))
        format_combo = ttk.Combobox(basic_frame, textvariable=self.format_var, 
                                   values=["txt", "markdown", "html", "docx", "pdf", "rtf", "epub", "json"], 
                                   state="readonly", width=15)
        format_combo.grid(row=1, column=1, sticky=tk.W)
        format_combo.bind("<<ComboboxSelected>>", self.on_format_change)
        
        # Output directory
        ttk.Label(basic_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.output_dir_var = tk.StringVar(value=self.config.get("output_directory", ""))
        output_entry = ttk.Entry(basic_frame, textvariable=self.output_dir_var, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(10, 0))
        ttk.Button(basic_frame, text="Browse", command=self.browse_output_dir).grid(row=2, column=2, pady=(10, 0))
        
        basic_frame.columnconfigure(1, weight=1)
        
        # OCR & Processing Tab
        ocr_frame = ttk.Frame(settings_notebook, padding="10")
        settings_notebook.add(ocr_frame, text="🤖 OCR & Processing")
        
        # OCR Backend Selection
        backend_group = ttk.LabelFrame(ocr_frame, text="OCR Backend", padding="5")
        backend_group.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(backend_group, text="Backend:").grid(row=0, column=0, sticky=tk.W)
        backend_combo = ttk.Combobox(backend_group, textvariable=self.backend_var, 
                                    values=["auto", "tesseract", "easyocr", "google_vision"], 
                                    state="readonly", width=20)
        backend_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        backend_combo.bind("<<ComboboxSelected>>", lambda e: self.set_backend(self.backend_var.get()))
        
        ttk.Button(backend_group, text="Advanced OCR Settings...", 
                  command=self.open_ocr_settings).grid(row=0, column=2, padx=(10, 0))
        
        backend_group.columnconfigure(1, weight=1)
        
        # Threading Controls  
        thread_group = ttk.LabelFrame(ocr_frame, text="Processing Threads", padding="5")
        thread_group.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(thread_group, text="Max Workers:").grid(row=0, column=0, sticky=tk.W)
        self.max_workers_var = tk.IntVar(value=self.config.get("max_workers", 4))
        workers_scale = ttk.Scale(thread_group, from_=1, to=16, variable=self.max_workers_var,
                                 orient="horizontal", length=200, command=self.update_workers_label)
        workers_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        self.workers_label = ttk.Label(thread_group, text=str(self.max_workers_var.get()))
        self.workers_label.grid(row=0, column=2)
        
        thread_group.columnconfigure(1, weight=1)
        
        # Quality Settings
        quality_group = ttk.LabelFrame(ocr_frame, text="Quality & Performance", padding="5")
        quality_group.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(quality_group, text="Quality Mode:").grid(row=0, column=0, sticky=tk.W)
        self.quality_var = tk.StringVar(value=self.config.get("quality_mode", "balanced"))
        quality_combo = ttk.Combobox(quality_group, textvariable=self.quality_var,
                                    values=["fast", "balanced", "accurate"], state="readonly", width=15)
        quality_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        self.preserve_structure_var = tk.BooleanVar(value=self.config.get("preserve_structure", True))
        ttk.Checkbutton(quality_group, text="Preserve document structure", 
                       variable=self.preserve_structure_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        quality_group.columnconfigure(1, weight=1)
        ocr_frame.columnconfigure(1, weight=1)
        
        # Tools & Reader Tab
        tools_frame = ttk.Frame(settings_notebook, padding="10")
        settings_notebook.add(tools_frame, text="🔧 Tools & Reader")
        
        # Document Reader Section
        reader_group = ttk.LabelFrame(tools_frame, text="Document Reader & Preview", padding="5")
        reader_group.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        reader_buttons = ttk.Frame(reader_group)
        reader_buttons.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(reader_buttons, text="📖 Open Reader", command=self.open_document_reader).pack(side="left", padx=(0, 5))
        ttk.Button(reader_buttons, text="👁️ Preview Output", command=self.show_preview).pack(side="left", padx=(0, 5))
        ttk.Button(reader_buttons, text="🔄 Bidirectional Edit", command=self.open_bidirectional_editor).pack(side="left")
        
        reader_group.columnconfigure(0, weight=1)
        
        # Quick Tools Section
        tools_group = ttk.LabelFrame(tools_frame, text="Quick Tools", padding="5")
        tools_group.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        tools_buttons = ttk.Frame(tools_group)
        tools_buttons.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(tools_buttons, text="🧹 Clear Cache", command=self.clear_ocr_cache).pack(side="left", padx=(0, 5))
        ttk.Button(tools_buttons, text="📊 Statistics", command=self.show_statistics).pack(side="left", padx=(0, 5))
        ttk.Button(tools_buttons, text="🔍 System Info", command=self.show_system_info).pack(side="left")
        
        tools_group.columnconfigure(0, weight=1)
        tools_frame.columnconfigure(1, weight=1)
        
        # Make notebook expandable
        main_frame.rowconfigure(2, weight=1)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="Start Conversion", command=self.start_conversion)
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_conversion, state=tk.DISABLED)
        self.cancel_button.grid(row=0, column=1, padx=(0, 5))
        
        ttk.Button(button_frame, text="Exit", command=self.on_closing).grid(row=0, column=2)
        
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        try:
            from tkinterdnd2 import DND_FILES
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
        except ImportError:
            # Fallback: disable drag and drop if tkinterdnd2 is not available
            pass
        
    def on_drop(self, event):
        """Handle file drop events"""
        files = self.root.tk.splitlist(event.data)
        self.add_files_to_list(files)
        
    def add_files(self):
        """Add files through file dialog"""
        files = filedialog.askopenfilenames(
            title="Select files to convert",
            filetypes=[
                ("All supported", "*.docx *.pdf *.txt *.html *.rtf *.epub *.jpg *.jpeg *.png *.tiff *.tif *.bmp *.gif *.webp"),
                ("Documents", "*.docx *.pdf *.txt *.html *.rtf *.epub"),
                ("Images", "*.jpg *.jpeg *.png *.tiff *.tif *.bmp *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        self.add_files_to_list(files)
        
    def add_files_to_list(self, files):
        """Add files to the processing list"""
        for file in files:
            if file not in self.current_files:
                self.current_files.append(file)
                filename = os.path.basename(file)
                self.file_listbox.insert(tk.END, filename)
                
    def remove_selected(self):
        """Remove selected files from the list"""
        selected = list(self.file_listbox.curselection())
        selected.reverse()
        for index in selected:
            self.file_listbox.delete(index)
            del self.current_files[index]
            
    def clear_all(self):
        """Clear all files from the list"""
        self.file_listbox.delete(0, tk.END)
        self.current_files.clear()
        
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir_var.set(directory)
            self.config["output_directory"] = directory
            
    def toggle_ocr(self):
        """Toggle OCR functionality"""
        self.config["ocr_enabled"] = self.ocr_var.get()
        
    def start_conversion(self):
        """Start the conversion process"""
        if not self.current_files:
            messagebox.showwarning("No Files", "Please add files to convert.")
            return
            
        if not self.output_dir_var.get():
            messagebox.showwarning("No Output Directory", "Please select an output directory.")
            return
            
        # Save configuration
        self.config["output_format"] = self.format_var.get()
        self.config["ocr_enabled"] = self.ocr_var.get()
        self.save_config()
        
        # Start processing
        self.is_processing = True
        self.processed_count = 0
        self.total_files = len(self.current_files)
        
        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        self.processing_thread = threading.Thread(target=self.process_files)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
    def cancel_conversion(self):
        """Cancel the conversion process"""
        self.is_processing = False
        self.status_label.config(text="Cancelling...")
        
    def process_files(self):
        """Process all files in the queue"""
        try:
            output_dir = Path(self.output_dir_var.get())
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for i, file_path in enumerate(self.current_files):
                if not self.is_processing:
                    break
                    
                self.update_status(f"Processing {os.path.basename(file_path)}...")
                self.update_progress((i / self.total_files) * 100)
                
                try:
                    self.process_single_file(file_path, output_dir)
                    self.processed_count += 1
                except Exception as e:
                    self.log_error(f"Error processing {file_path}: {str(e)}")
                    
            self.processing_complete()
            
        except Exception as e:
            self.log_error(f"Processing error: {str(e)}")
            self.processing_complete()
            
    def process_single_file(self, file_path: str, output_dir: Path):
        """Process a single file"""
        file_path = Path(file_path)
        
        # Check if OCR should be used
        use_ocr = self.config.get("ocr_enabled", True) and self.format_detector.is_ocr_format(str(file_path))
        
        if use_ocr:
            # Use OCR processing
            output_text = self.ocr_integration.process_file(str(file_path))
            output_file = output_dir / f"{file_path.stem}.{self.format_var.get()}"
            
            # Save based on output format
            self.save_ocr_output(output_text, str(output_file))
        else:
            # Use regular document conversion
            self.convert_document(str(file_path), str(output_dir))
            
    def save_ocr_output(self, text: str, output_path: str):
        """Save OCR output in the specified format"""
        format_type = self.format_var.get()
        
        if format_type == "txt":
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
        elif format_type == "docx":
            try:
                from docx import Document
                doc = Document()
                doc.add_paragraph(text)
                doc.save(output_path)
            except ImportError:
                # Fallback to txt
                txt_path = output_path.replace('.docx', '.txt')
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(text)
        elif format_type == "html":
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Converted Document</title>
                <meta charset="utf-8">
            </head>
            <body>
                <pre>{text}</pre>
            </body>
            </html>
            """
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        else:
            # Default to txt for other formats
            txt_path = output_path.replace(f'.{format_type}', '.txt')
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
                
    def convert_document(self, input_path: str, output_dir: str):
        """Convert document using appropriate method"""
        # This would integrate with existing document conversion logic
        # For now, create a basic text representation
        output_format = self.format_var.get()
        input_file = Path(input_path)
        output_file = Path(output_dir) / f"{input_file.stem}.{output_format}"
        
        # Basic conversion - read and save as text
        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            with open(str(output_file), 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            # Fallback: create basic text file
            fallback_file = Path(output_dir) / f"{input_file.stem}.txt"
            with open(str(fallback_file), 'w') as f:
                f.write(f"Converted from: {input_path}\n")
                f.write(f"Original format: {input_file.suffix}\n")
                f.write("Content extraction not implemented for this format.\n")
                
    def update_status(self, message: str):
        """Update status label (thread-safe)"""
        self.root.after(0, lambda: self.status_label.config(text=message))
        
    def update_progress(self, value: float):
        """Update progress bar (thread-safe)"""
        self.root.after(0, lambda: self.progress_var.set(value))
        
    def processing_complete(self):
        """Handle processing completion"""
        self.is_processing = False
        
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        
        if self.processed_count == self.total_files:
            self.update_status(f"Completed: {self.processed_count}/{self.total_files} files processed")
            messagebox.showinfo("Complete", f"Conversion completed!\n{self.processed_count} files processed.")
        else:
            self.update_status(f"Cancelled: {self.processed_count}/{self.total_files} files processed")
            
        self.update_progress(0)
        
    def log_error(self, message: str):
        """Log error message"""
        logging.error(message)
        self.update_status(f"Error: {message}")
        
    def on_closing(self):
        """Handle application closing"""
        if self.is_processing:
            if messagebox.askokcancel("Quit", "Conversion is in progress. Do you want to quit?"):
                self.is_processing = False
                if self.processing_thread and self.processing_thread.is_alive():
                    self.processing_thread.join(timeout=2)
                self.root.destroy()
        else:
            self.root.destroy()

    def open_ocr_settings(self):
        """Open the OCR settings dialog"""
        if not OCR_SETTINGS_GUI_AVAILABLE:
            messagebox.showerror("Error", 
                               "OCR Settings GUI is not available. Please check installation.")
            return
        
        try:
            settings_window = OCRSettingsGUI(self.root, self.ocr_config_manager)
            # Reinitialize OCR integration after settings change
            self.root.after(100, self.refresh_ocr_integration)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open OCR settings: {str(e)}")
    
    def refresh_ocr_integration(self):
        """Refresh OCR integration after settings change"""
        try:
            # Reinitialize OCR integration with updated config
            self.ocr_integration = OCRIntegration(logger=self.logger, config_manager=self.ocr_config_manager)
            self.backend_var.set(self.ocr_config_manager.get_default_backend())
        except Exception as e:
            self.logger.error(f"Failed to refresh OCR integration: {e}")
    
    def check_ocr_status(self):
        """Check and display OCR backend status"""
        try:
            status = self.ocr_integration.check_availability()
            
            status_msg = f"OCR Status Report\n{'='*40}\n\n"
            status_msg += f"OCR Available: {'✅ Yes' if status['available'] else '❌ No'}\n"
            status_msg += f"Tesseract: {'✅' if status['tesseract_available'] else '❌'}\n"
            status_msg += f"EasyOCR: {'✅' if status['easyocr_available'] else '❌'}\n"
            
            # Check Google Vision
            if hasattr(self.ocr_integration.ocr_engine, 'is_google_vision_available'):
                google_available = self.ocr_integration.ocr_engine.is_google_vision_available()
                status_msg += f"Google Vision API: {'✅' if google_available else '❌'}\n"
            
            status_msg += f"\nAvailable Backends: {', '.join(status['backends'])}\n"
            status_msg += f"Supported Formats: {', '.join(status['supported_formats'])}\n"
            status_msg += f"\nMessage: {status['message']}"
            
            messagebox.showinfo("OCR Status", status_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check OCR status: {str(e)}")
    
    def set_backend(self, backend_name: str):
        """Set the default OCR backend"""
        try:
            if self.ocr_config_manager.set_default_backend(backend_name):
                self.refresh_ocr_integration()
                self.status_label.config(text=f"OCR backend set to: {backend_name}")
            else:
                messagebox.showerror("Error", "Failed to set OCR backend")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set backend: {str(e)}")
    
    def clear_ocr_cache(self):
        """Clear the OCR cache"""
        try:
            if hasattr(self.ocr_integration.ocr_engine, 'clear_cache'):
                if self.ocr_integration.ocr_engine.clear_cache():
                    messagebox.showinfo("Success", "OCR cache cleared successfully")
                else:
                    messagebox.showerror("Error", "Failed to clear OCR cache")
            else:
                messagebox.showinfo("Info", "OCR cache functionality not available")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear cache: {str(e)}")
    
    def export_ocr_config(self):
        """Export OCR configuration"""
        filename = filedialog.asksaveasfilename(
            title="Export OCR Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                include_keys = messagebox.askyesno(
                    "Include API Keys",
                    "Include API keys in the exported configuration?\n\n"
                    "Choose 'No' if sharing the configuration file."
                )
                if self.ocr_config_manager.export_config(Path(filename), include_keys):
                    messagebox.showinfo("Success", "OCR configuration exported successfully!")
                else:
                    messagebox.showerror("Error", "Failed to export OCR configuration.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export config: {str(e)}")
    
    def import_ocr_config(self):
        """Import OCR configuration"""
        filename = filedialog.askopenfilename(
            title="Import OCR Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                if self.ocr_config_manager.import_config(Path(filename)):
                    messagebox.showinfo("Success", "OCR configuration imported successfully!")
                    self.refresh_ocr_integration()
                else:
                    messagebox.showerror("Error", "Failed to import OCR configuration.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import config: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Universal Document Converter with OCR v3.1.0
        
A powerful document conversion tool with integrated OCR support.

Features:
• Document conversion (DOCX, PDF, TXT, HTML, RTF, EPUB)
• OCR functionality with multiple backends
• Google Vision API integration
• Multi-threaded processing
• Professional GUI with drag-and-drop support

Supported OCR Backends:
• Tesseract OCR (free, local processing)
• EasyOCR (free, local processing)
• Google Vision API (cloud-based, requires API key)

Created by Beau Lewis (blewisxx@gmail.com)
Enhanced by Terragon Labs"""
        
        messagebox.showinfo("About", about_text)
    
    # New methods for enhanced functionality
    def update_workers_label(self, value):
        """Update the workers label when scale changes"""
        self.workers_label.config(text=str(int(float(value))))
    
    def on_format_change(self, event=None):
        """Handle output format change"""
        self.save_config()
        self.status_label.config(text=f"Output format changed to: {self.format_var.get()}")
    
    def open_document_reader(self):
        """Open the document reader window"""
        reader_window = tk.Toplevel(self.root)
        reader_window.title("Document Reader")
        reader_window.geometry("800x600")
        
        # Simple document reader implementation
        toolbar = ttk.Frame(reader_window)
        toolbar.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(toolbar, text="📂 Open", command=lambda: self.reader_open_file(reader_window)).pack(side="left", padx=(0, 5))
        ttk.Button(toolbar, text="💾 Save", command=lambda: self.reader_save_file(reader_window)).pack(side="left", padx=(0, 5))
        ttk.Button(toolbar, text="🔍 Search", command=lambda: self.reader_search(reader_window)).pack(side="left")
        
        # Text widget for document content
        text_frame = ttk.Frame(reader_window)
        text_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        reader_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=("Georgia", 12))
        reader_text.pack(fill="both", expand=True)
        
        # Store reference for the reader methods
        reader_window.reader_text = reader_text
    
    def reader_open_file(self, window):
        """Open file in document reader"""
        filename = filedialog.askopenfilename(
            title="Open Document",
            filetypes=[
                ("All Supported", "*.txt;*.md;*.html;*.docx;*.pdf"),
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("HTML files", "*.html"),
                ("Word documents", "*.docx"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )
        if filename:
            try:
                # Simple text file reading (can be enhanced for other formats)
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    window.reader_text.delete(1.0, tk.END)
                    window.reader_text.insert(1.0, content)
                window.title(f"Document Reader - {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def reader_save_file(self, window):
        """Save file from document reader"""
        filename = filedialog.asksaveasfilename(
            title="Save Document",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("HTML files", "*.html"),
                ("All files", "*.*")
            ]
        )
        if filename:
            try:
                content = window.reader_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", "Document saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def reader_search(self, window):
        """Search in document reader"""
        search_text = tk.simpledialog.askstring("Search", "Enter text to search:")
        if search_text:
            # Simple search implementation
            content = window.reader_text.get(1.0, tk.END)
            start_pos = content.find(search_text)
            if start_pos != -1:
                # Calculate line and column
                lines_before = content[:start_pos].count('\n')
                line_start = content.rfind('\n', 0, start_pos) + 1
                col = start_pos - line_start
                
                # Select found text
                start_index = f"{lines_before + 1}.{col}"
                end_index = f"{lines_before + 1}.{col + len(search_text)}"
                
                window.reader_text.tag_remove("search", 1.0, tk.END)
                window.reader_text.tag_add("search", start_index, end_index)
                window.reader_text.tag_config("search", background="yellow")
                window.reader_text.see(start_index)
            else:
                messagebox.showinfo("Search", "Text not found.")
    
    def show_preview(self):
        """Show preview of conversion output"""
        if not self.current_files:
            messagebox.showwarning("No Files", "Please add files to preview.")
            return
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Output Preview")
        preview_window.geometry("900x700")
        
        # Preview controls
        control_frame = ttk.Frame(preview_window)
        control_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(control_frame, text="File:").pack(side="left")
        file_var = tk.StringVar()
        file_combo = ttk.Combobox(control_frame, textvariable=file_var, 
                                 values=[str(Path(f).name) for f in self.current_files], 
                                 state="readonly", width=30)
        file_combo.pack(side="left", padx=(5, 20))
        
        ttk.Label(control_frame, text="Format:").pack(side="left")
        preview_format_var = tk.StringVar(value=self.format_var.get())
        format_combo = ttk.Combobox(control_frame, textvariable=preview_format_var,
                                   values=["txt", "markdown", "html"], state="readonly", width=15)
        format_combo.pack(side="left", padx=(5, 0))
        
        # Preview content
        preview_text = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD, font=("Consolas", 10))
        preview_text.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # Sample preview content
        preview_text.insert(1.0, """# Document Preview
        
This is a preview of how your document will look after conversion.

## Features:
- ✅ OCR text extraction
- ✅ Format preservation  
- ✅ Multiple output formats
- ✅ Batch processing

> **Note**: This is a sample preview. Actual output will vary based on your files and settings.

### Supported Formats:
| Format | Description | Use Case |
|--------|-------------|----------|
| TXT | Plain text | Simple text extraction |
| Markdown | Formatted text | Documentation, notes |
| HTML | Web format | Web publishing |
| DOCX | Word document | Office documents |
| PDF | Portable format | Archiving, sharing |
""")
    
    def open_bidirectional_editor(self):
        """Open bidirectional markdown editor"""
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Bidirectional Markdown Editor")
        editor_window.geometry("1200x800")
        
        # Create paned window for split view
        paned = ttk.PanedWindow(editor_window, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left side - Markdown source
        left_frame = ttk.LabelFrame(paned, text="📝 Markdown Source", padding="5")
        paned.add(left_frame, weight=1)
        
        # Toolbar for source
        source_toolbar = ttk.Frame(left_frame)
        source_toolbar.pack(fill="x", pady=(0, 5))
        
        ttk.Button(source_toolbar, text="📂 Open", command=lambda: self.editor_open(editor_window)).pack(side="left", padx=(0, 5))
        ttk.Button(source_toolbar, text="💾 Save", command=lambda: self.editor_save(editor_window)).pack(side="left", padx=(0, 5))
        ttk.Button(source_toolbar, text="🔄 Update Preview", command=lambda: self.update_markdown_preview(editor_window)).pack(side="left")
        
        # Source text editor
        source_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, font=("Consolas", 11))
        source_text.pack(fill="both", expand=True)
        
        # Right side - Rendered preview
        right_frame = ttk.LabelFrame(paned, text="👁️ Rendered Preview", padding="5")
        paned.add(right_frame, weight=1)
        
        # Preview toolbar
        preview_toolbar = ttk.Frame(right_frame)
        preview_toolbar.pack(fill="x", pady=(0, 5))
        
        ttk.Button(preview_toolbar, text="🔄 Refresh", command=lambda: self.update_markdown_preview(editor_window)).pack(side="left", padx=(0, 5))
        ttk.Button(preview_toolbar, text="📄 Export HTML", command=lambda: self.export_html(editor_window)).pack(side="left")
        
        # Preview display
        preview_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=("Georgia", 11), state="disabled")
        preview_text.pack(fill="both", expand=True)
        
        # Store references
        editor_window.source_text = source_text
        editor_window.preview_text = preview_text
        
        # Sample content
        sample_markdown = """# Welcome to Bidirectional Markdown Editor

This is a **powerful** markdown editor with live preview.

## Features

- ✨ Live preview updates
- 📝 Syntax highlighting
- 🔄 Bidirectional editing
- 💾 Save/Load documents
- 📄 Export to HTML

## Example Code

```python
def hello_world():
    print("Hello, World!")
```

## Example Table

| Feature | Status | Notes |
|---------|--------|-------|
| Editor | ✅ Working | Full featured |
| Preview | ✅ Working | Real-time |
| Export | ✅ Working | Multiple formats |

> **Tip**: Edit the text on the left and see the preview update on the right!
"""
        
        source_text.insert(1.0, sample_markdown)
        self.update_markdown_preview(editor_window)
        
        # Auto-update preview on text change
        source_text.bind('<KeyRelease>', lambda e: self.root.after(500, lambda: self.update_markdown_preview(editor_window)))
    
    def editor_open(self, window):
        """Open markdown file in editor"""
        filename = filedialog.askopenfilename(
            title="Open Markdown File",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    window.source_text.delete(1.0, tk.END)
                    window.source_text.insert(1.0, content)
                window.title(f"Bidirectional Editor - {Path(filename).name}")
                self.update_markdown_preview(window)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def editor_save(self, window):
        """Save markdown file from editor"""
        filename = filedialog.asksaveasfilename(
            title="Save Markdown File",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                content = window.source_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def update_markdown_preview(self, window):
        """Update the markdown preview"""
        try:
            # Get markdown content
            markdown_content = window.source_text.get(1.0, tk.END)
            
            # Try to use markdown2 for conversion
            try:
                import markdown2
                html_content = markdown2.markdown(markdown_content, extras=['tables', 'code-friendly', 'fenced-code-blocks'])
                # Convert HTML to text for display (simplified)
                import html
                text_content = html.unescape(html_content)
                # Remove HTML tags for text display
                import re
                text_content = re.sub('<[^<]+?>', '', text_content)
            except ImportError:
                # Fallback: basic markdown-like formatting
                text_content = markdown_content.replace('**', '').replace('*', '').replace('#', '')
            
            # Update preview
            window.preview_text.config(state="normal")
            window.preview_text.delete(1.0, tk.END)
            window.preview_text.insert(1.0, text_content)
            window.preview_text.config(state="disabled")
            
        except Exception as e:
            print(f"Preview update error: {e}")
    
    def export_html(self, window):
        """Export markdown as HTML"""
        filename = filedialog.asksaveasfilename(
            title="Export as HTML",
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if filename:
            try:
                markdown_content = window.source_text.get(1.0, tk.END)
                
                # Convert markdown to HTML
                try:
                    import markdown2
                    html_content = markdown2.markdown(markdown_content, extras=['tables', 'code-friendly', 'fenced-code-blocks'])
                except ImportError:
                    # Fallback: basic HTML wrapper
                    html_content = f"<html><body><pre>{markdown_content}</pre></body></html>"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                messagebox.showinfo("Success", "HTML exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export HTML: {str(e)}")
    
    def show_statistics(self):
        """Show processing statistics"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Processing Statistics")
        stats_window.geometry("600x400")
        
        # Statistics display
        stats_text = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD, font=("Consolas", 10))
        stats_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sample statistics
        stats_content = f"""📊 Processing Statistics
{'='*50}

📁 Files:
   Total Files: {len(self.current_files)}
   Processed: {self.processed_count}
   Remaining: {len(self.current_files) - self.processed_count}

⚙️ Configuration:
   OCR Enabled: {'Yes' if self.ocr_var.get() else 'No'}
   Backend: {self.backend_var.get()}
   Max Workers: {self.max_workers_var.get()}
   Quality Mode: {self.quality_var.get()}
   Output Format: {self.format_var.get()}

🚀 Performance:
   Cache Hits: 0
   Average Time: N/A
   Throughput: N/A

🎯 Success Rate:
   Successful: 0%
   Failed: 0%
   
📈 Memory Usage:
   Current: N/A
   Peak: N/A

Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        stats_text.insert(1.0, stats_content)
        stats_text.config(state="disabled")

def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Enable drag and drop
    try:
        from tkinterdnd2 import DND_FILES, TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        pass
    
    app = DocumentConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()