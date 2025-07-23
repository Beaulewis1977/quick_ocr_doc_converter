#!/usr/bin/env python3
"""
Unified OCR Document Converter - Main Application
Modern, thread-safe GUI with tabbed interface for OCR and document conversion
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import queue
from pathlib import Path
import sys
import json
import logging
import datetime
from typing import Optional, List, Dict, Any, Union
import time

# Import our core modules
try:
    from ocr_engine import OCREngine
except ImportError:
    print("Warning: OCR engine not available")
    OCREngine = None

try:
    from universal_document_converter import UniversalDocumentConverter
except ImportError:
    print("Warning: Universal document converter not available")
    UniversalDocumentConverter = None

class ThreadSafeGUI:
    """Thread-safe GUI update manager"""
    
    def __init__(self, root):
        self.root = root
        self.update_queue = queue.Queue()
        self.root.after(10, self.process_updates)
    
    def process_updates(self):
        """Process queued GUI updates"""
        try:
            while True:
                func, args, kwargs = self.update_queue.get_nowait()
                func(*args, **kwargs)
        except queue.Empty:
            pass
        finally:
            self.root.after(10, self.process_updates)
    
    def schedule_update(self, func, *args, **kwargs):
        """Schedule a GUI update from any thread"""
        self.update_queue.put((func, args, kwargs))

class MainApplication:
    """Main application class with unified OCR and document conversion"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Document Converter - Unified Application")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Initialize thread-safe GUI manager
        self.gui_manager = ThreadSafeGUI(root)
        
        # Initialize core components
        self.ocr_engine = OCREngine() if OCREngine else None
        self.document_converter = UniversalDocumentConverter() if UniversalDocumentConverter else None
        
        # Configuration
        self.config = self.load_config()
        self.setup_logging()
        
        # State variables
        self.current_files = []
        self.processing_thread = None
        self.is_processing = False
        self.cancel_requested = False
        self.processed_count = 0
        self.total_files = 0
        self.current_operation = "idle"  # idle, ocr, convert, batch
        
        # Create GUI
        self.create_gui()
        self.setup_drag_drop()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Check OCR availability
        self.check_ocr_status()
        
        # Log successful initialization
        self.logger.info("Application initialized successfully")
    
    def load_config(self) -> Dict[str, Any]:
        """Load application configuration"""
        config_path = Path("config.json")
        default_config = {
            "output_format": "txt",
            "ocr_enabled": True,
            "ocr_language": "eng",
            "batch_size": 5,
            "max_workers": 4,
            "output_directory": str(Path.home() / "Documents" / "OCR_Converted"),
            "theme": "default",
            "window_size": "1200x800",
            "auto_detect_format": True,
            "preserve_structure": True,
            "enable_cloud_ocr": False
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                self.log_message(f"Error loading config: {e}", "ERROR")
                
        return default_config
    
    def save_config(self):
        """Save application configuration"""
        try:
            # Update config with current values
            self.config["output_format"] = self.format_var.get()
            self.config["ocr_enabled"] = self.ocr_var.get()
            self.config["ocr_language"] = self.language_var.get()
            self.config["output_directory"] = self.output_dir_var.get()
            self.config["auto_detect_format"] = self.auto_detect_var.get()
            self.config["preserve_structure"] = self.preserve_structure_var.get()
            
            with open("config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.log_message(f"Error saving config: {e}", "ERROR")
    
    def setup_logging(self):
        """Setup logging system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"ocr_converter_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Application started")
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title and status bar
        self.create_header(main_frame)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create tabs
        self.create_ocr_tab()
        self.create_convert_tab()
        self.create_batch_tab()
        self.create_settings_tab()
        
        # Progress and control frame
        self.create_progress_frame(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create header with title and OCR status"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="OCR Document Converter", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # OCR Status
        self.ocr_status_label = ttk.Label(header_frame, text="OCR Status: Checking...", 
                                         foreground="blue")
        self.ocr_status_label.grid(row=0, column=1, sticky=tk.E)
    
    def create_ocr_tab(self):
        """Create OCR processing tab"""
        ocr_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(ocr_frame, text="OCR Processing")
        
        # File selection
        file_frame = ttk.LabelFrame(ocr_frame, text="Image/PDF Files", padding="10")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(0, weight=1)
        
        # File listbox
        self.create_file_listbox(file_frame, "ocr")
        
        # OCR options
        options_frame = ttk.LabelFrame(ocr_frame, text="OCR Options", padding="10")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # OCR Language
        ttk.Label(options_frame, text="Language:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.language_var = tk.StringVar(value=self.config.get("ocr_language", "eng"))
        lang_combo = ttk.Combobox(options_frame, textvariable=self.language_var,
                                 values=self.get_available_languages(),
                                 state="readonly", width=15)
        lang_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Output format for OCR
        ttk.Label(options_frame, text="Output Format:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.ocr_format_var = tk.StringVar(value="txt")
        ocr_format_combo = ttk.Combobox(options_frame, textvariable=self.ocr_format_var,
                                       values=["txt", "docx", "html", "rtf", "markdown"],
                                       state="readonly", width=15)
        ocr_format_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Configure grid weights
        ocr_frame.columnconfigure(0, weight=1)
        ocr_frame.rowconfigure(0, weight=1)
    
    def create_convert_tab(self):
        """Create document conversion tab"""
        convert_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(convert_frame, text="Document Conversion")
        
        # File selection
        file_frame = ttk.LabelFrame(convert_frame, text="Document Files", padding="10")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(0, weight=1)
        
        # File listbox
        self.create_file_listbox(file_frame, "convert")
        
        # Conversion options
        options_frame = ttk.LabelFrame(convert_frame, text="Conversion Options", padding="10")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Auto-detect format
        self.auto_detect_var = tk.BooleanVar(value=self.config.get("auto_detect_format", True))
        ttk.Checkbutton(options_frame, text="Auto-detect input format", 
                       variable=self.auto_detect_var).grid(row=0, column=0, sticky=tk.W)
        
        # Preserve structure
        self.preserve_structure_var = tk.BooleanVar(value=self.config.get("preserve_structure", True))
        ttk.Checkbutton(options_frame, text="Preserve document structure", 
                       variable=self.preserve_structure_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Output format
        ttk.Label(options_frame, text="Output Format:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.format_var = tk.StringVar(value=self.config.get("output_format", "txt"))
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var,
                                   values=["txt", "docx", "pdf", "html", "rtf", "epub", "markdown"],
                                   state="readonly", width=15)
        format_combo.grid(row=1, column=1, sticky=tk.W, pady=(10, 0), padx=(20, 0))
        
        # Configure grid weights
        convert_frame.columnconfigure(0, weight=1)
        convert_frame.rowconfigure(0, weight=1)
    
    def create_batch_tab(self):
        """Create batch processing tab"""
        batch_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(batch_frame, text="Batch Processing")
        
        # File selection
        file_frame = ttk.LabelFrame(batch_frame, text="Batch Files", padding="10")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(0, weight=1)
        
        # File listbox
        self.create_file_listbox(file_frame, "batch")
        
        # Batch options
        options_frame = ttk.LabelFrame(batch_frame, text="Batch Options", padding="10")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Mixed processing
        self.mixed_processing_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Auto-detect OCR vs conversion for each file", 
                       variable=self.mixed_processing_var).grid(row=0, column=0, sticky=tk.W)
        
        # Batch size
        ttk.Label(options_frame, text="Batch Size:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.batch_size_var = tk.IntVar(value=self.config.get("batch_size", 5))
        batch_spin = ttk.Spinbox(options_frame, from_=1, to=20, textvariable=self.batch_size_var, width=10)
        batch_spin.grid(row=1, column=1, sticky=tk.W, pady=(10, 0), padx=(10, 0))
        
        # Configure grid weights
        batch_frame.columnconfigure(0, weight=1)
        batch_frame.rowconfigure(0, weight=1)
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(settings_frame, text="Settings")
        
        # General settings
        general_frame = ttk.LabelFrame(settings_frame, text="General Settings", padding="10")
        general_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        general_frame.columnconfigure(1, weight=1)
        
        # Output directory
        ttk.Label(general_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.output_dir_var = tk.StringVar(value=self.config.get("output_directory", ""))
        output_entry = ttk.Entry(general_frame, textvariable=self.output_dir_var, width=60)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(0, 5))
        ttk.Button(general_frame, text="Browse", command=self.browse_output_dir).grid(row=0, column=2, pady=(0, 5))
        
        # OCR settings
        ocr_frame = ttk.LabelFrame(settings_frame, text="OCR Settings", padding="10")
        ocr_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Enable OCR
        self.ocr_var = tk.BooleanVar(value=self.config.get("ocr_enabled", True))
        ttk.Checkbutton(ocr_frame, text="Enable OCR processing", 
                       variable=self.ocr_var).grid(row=0, column=0, sticky=tk.W)
        
        # Cloud OCR (placeholder for future implementation)
        self.cloud_ocr_var = tk.BooleanVar(value=self.config.get("enable_cloud_ocr", False))
        ttk.Checkbutton(ocr_frame, text="Enable cloud OCR backends (future feature)", 
                       variable=self.cloud_ocr_var, state="disabled").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Performance settings
        perf_frame = ttk.LabelFrame(settings_frame, text="Performance Settings", padding="10")
        perf_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Max workers
        ttk.Label(perf_frame, text="Max Workers:").grid(row=0, column=0, sticky=tk.W)
        self.max_workers_var = tk.IntVar(value=self.config.get("max_workers", 4))
        workers_spin = ttk.Spinbox(perf_frame, from_=1, to=16, textvariable=self.max_workers_var, width=10)
        workers_spin.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Configure grid weights
        settings_frame.columnconfigure(0, weight=1)
    
    def create_file_listbox(self, parent, tab_type):
        """Create file listbox with controls"""
        # Listbox frame
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create listbox for this tab
        listbox = tk.Listbox(list_frame, height=8, selectmode=tk.EXTENDED)
        listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        listbox.configure(yscrollcommand=scrollbar.set)
        
        # Store listbox reference
        setattr(self, f"{tab_type}_listbox", listbox)
        
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=1, column=0, sticky=tk.W)
        
        # Buttons
        ttk.Button(button_frame, text="Add Files", 
                  command=lambda: self.add_files(tab_type)).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Add Folder", 
                  command=lambda: self.add_folder(tab_type)).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="Remove Selected", 
                  command=lambda: self.remove_selected(tab_type)).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(button_frame, text="Clear All", 
                  command=lambda: self.clear_all(tab_type)).grid(row=0, column=3)
    
    def create_progress_frame(self, parent):
        """Create progress and control frame"""
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(progress_frame)
        button_frame.grid(row=2, column=0, pady=(10, 0))
        
        self.start_button = ttk.Button(button_frame, text="Start Processing", 
                                      command=self.start_processing)
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", 
                                       command=self.cancel_processing, state=tk.DISABLED)
        self.cancel_button.grid(row=0, column=1, padx=(0, 5))
        
        ttk.Button(button_frame, text="Save Settings", 
                  command=self.save_config).grid(row=0, column=2, padx=(0, 5))
        
        ttk.Button(button_frame, text="Exit", 
                  command=self.on_closing).grid(row=0, column=3)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        self.status_bar = ttk.Label(parent, text="Ready", relief=tk.SUNKEN)
        self.status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E))
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        try:
            from tkinterdnd2 import DND_FILES
            # Enable drag and drop for the main window
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
        except ImportError:
            self.log_message("Drag and drop not available (tkinterdnd2 not installed)", "WARNING")
    
    def on_drop(self, event):
        """Handle file drop events"""
        files = self.root.tk.splitlist(event.data)
        # Add to current tab
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        if "OCR" in current_tab:
            self.add_files_to_tab(files, "ocr")
        elif "Document" in current_tab:
            self.add_files_to_tab(files, "convert")
        else:
            self.add_files_to_tab(files, "batch")
    
    def get_available_languages(self) -> List[str]:
        """Get available OCR languages"""
        try:
            languages = self.ocr_engine.get_supported_languages()
            return languages if languages else ["eng"]
        except Exception:
            return ["eng"]
    
    def check_ocr_status(self):
        """Check OCR availability and update status"""
        def update_status():
            if self.ocr_engine.is_available():
                self.ocr_status_label.config(text="OCR Status: Ready", foreground="green")
            else:
                self.ocr_status_label.config(text="OCR Status: Not Available", foreground="red")
        
        self.gui_manager.schedule_update(update_status)
    
    def add_files(self, tab_type):
        """Add files through file dialog"""
        if tab_type == "ocr":
            filetypes = [
                ("Image files", "*.jpg *.jpeg *.png *.tiff *.tif *.bmp *.gif *.webp"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        else:
            filetypes = [
                ("Document files", "*.docx *.pdf *.txt *.html *.rtf *.epub *.odt"),
                ("All files", "*.*")
            ]
        
        files = filedialog.askopenfilenames(
            title=f"Select files for {tab_type}",
            filetypes=filetypes
        )
        
        if files:
            self.add_files_to_tab(files, tab_type)
    
    def add_folder(self, tab_type):
        """Add all files from a folder"""
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            folder_path = Path(folder)
            if tab_type == "ocr":
                extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.gif', '.webp', '.pdf']
            else:
                extensions = ['.docx', '.pdf', '.txt', '.html', '.rtf', '.epub', '.odt']
            
            files = []
            for ext in extensions:
                files.extend(folder_path.rglob(f"*{ext}"))
            
            if files:
                self.add_files_to_tab([str(f) for f in files], tab_type)
    
    def add_files_to_tab(self, files: List[str], tab_type: str):
        """Add files to specified tab"""
        listbox = getattr(self, f"{tab_type}_listbox")
        
        # Get current files to avoid duplicates
        current_files = [listbox.get(i) for i in range(listbox.size())]
        
        added_count = 0
        for file_path in files:
            filename = os.path.basename(file_path)
            if filename not in current_files:
                listbox.insert(tk.END, filename)
                # Store full path in a data structure
                if not hasattr(self, f"{tab_type}_files"):
                    setattr(self, f"{tab_type}_files", [])
                getattr(self, f"{tab_type}_files").append(file_path)
                added_count += 1
        
        if added_count > 0:
            self.update_status_bar(f"Added {added_count} files to {tab_type} tab")
    
    def remove_selected(self, tab_type):
        """Remove selected files from tab"""
        listbox = getattr(self, f"{tab_type}_listbox")
        files_list = getattr(self, f"{tab_type}_files", [])
        
        selected = list(listbox.curselection())
        selected.reverse()  # Remove from end to avoid index issues
        
        for index in selected:
            listbox.delete(index)
            if index < len(files_list):
                del files_list[index]
        
        if selected:
            self.update_status_bar(f"Removed {len(selected)} files from {tab_type} tab")
    
    def clear_all(self, tab_type):
        """Clear all files from tab"""
        listbox = getattr(self, f"{tab_type}_listbox")
        count = listbox.size()
        
        listbox.delete(0, tk.END)
        setattr(self, f"{tab_type}_files", [])
        
        if count > 0:
            self.update_status_bar(f"Cleared {count} files from {tab_type} tab")
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir_var.set(directory)
            self.update_status_bar(f"Output directory set to: {directory}")
    
    def start_processing(self):
        """Start processing files"""
        # Get current tab
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if "OCR" in current_tab:
            self.current_operation = "ocr"
            files = getattr(self, "ocr_files", [])
        elif "Document" in current_tab:
            self.current_operation = "convert"
            files = getattr(self, "convert_files", [])
        else:
            self.current_operation = "batch"
            files = getattr(self, "batch_files", [])
        
        if not files:
            messagebox.showwarning("No Files", "Please add files to process.")
            return
        
        if not self.output_dir_var.get():
            messagebox.showwarning("No Output Directory", "Please select an output directory.")
            return
        
        # Prepare for processing
        self.current_files = files
        self.is_processing = True
        self.cancel_requested = False
        self.processed_count = 0
        self.total_files = len(files)
        
        # Update UI
        self.gui_manager.schedule_update(self.start_button.config, state=tk.DISABLED)
        self.gui_manager.schedule_update(self.cancel_button.config, state=tk.NORMAL)
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self.process_files_thread, daemon=True)
        self.processing_thread.start()
    
    def cancel_processing(self):
        """Cancel current processing"""
        self.cancel_requested = True
        self.gui_manager.schedule_update(self.update_status, "Cancelling...")
        self.gui_manager.schedule_update(self.cancel_button.config, state=tk.DISABLED)
    
    def process_files_thread(self):
        """Process files in background thread"""
        try:
            output_dir = Path(self.output_dir_var.get())
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for i, file_path in enumerate(self.current_files):
                if self.cancel_requested:
                    break
                
                filename = os.path.basename(file_path)
                self.gui_manager.schedule_update(self.update_status, f"Processing {filename}...")
                progress = (i / self.total_files) * 100
                self.gui_manager.schedule_update(self.update_progress, progress)
                
                try:
                    self.process_single_file(file_path, output_dir)
                    self.processed_count += 1
                    self.log_message(f"Successfully processed: {filename}", "INFO")
                except Exception as e:
                    self.log_message(f"Error processing {filename}: {str(e)}", "ERROR")
            
            # Processing complete
            self.gui_manager.schedule_update(self.processing_complete)
            
        except Exception as e:
            self.log_message(f"Processing thread error: {str(e)}", "ERROR")
            self.gui_manager.schedule_update(self.processing_complete)
    
    def process_single_file(self, file_path: str, output_dir: Path):
        """Process a single file"""
        file_path = Path(file_path)
        
        if self.current_operation == "ocr":
            # OCR processing
            text = self.ocr_engine.extract_text(str(file_path), self.language_var.get())
            if text:
                output_format = self.ocr_format_var.get()
                output_file = output_dir / f"{file_path.stem}.{output_format}"
                self.save_text_output(text, str(output_file), output_format)
            else:
                raise Exception("OCR extraction failed")
                
        elif self.current_operation == "convert":
            # Document conversion
            # This would use the document converter
            # For now, basic text handling
            output_format = self.format_var.get()
            output_file = output_dir / f"{file_path.stem}.{output_format}"
            
            # Basic conversion logic
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            self.save_text_output(content, str(output_file), output_format)
        
        else:
            # Batch processing - auto-detect
            if self.is_image_file(file_path) or file_path.suffix.lower() == '.pdf':
                # Use OCR
                text = self.ocr_engine.extract_text(str(file_path), self.language_var.get())
                if text:
                    output_file = output_dir / f"{file_path.stem}.txt"
                    self.save_text_output(text, str(output_file), "txt")
            else:
                # Use document conversion
                output_file = output_dir / f"{file_path.stem}.txt"
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                self.save_text_output(content, str(output_file), "txt")
    
    def is_image_file(self, file_path: Path) -> bool:
        """Check if file is an image"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.gif', '.webp'}
        return file_path.suffix.lower() in image_extensions
    
    def save_text_output(self, text: str, output_path: str, format_type: str):
        """Save text in specified format"""
        if format_type == "txt":
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
        elif format_type == "markdown":
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Converted Document\n\n{text}")
        elif format_type == "html":
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Converted Document</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Converted Document</h1>
    <pre>{text}</pre>
</body>
</html>"""
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
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
        else:
            # Default to txt
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
    
    def processing_complete(self):
        """Handle processing completion (called from main thread)"""
        self.is_processing = False
        
        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.update_progress(100)
        
        if self.cancel_requested:
            status_msg = f"Cancelled: {self.processed_count}/{self.total_files} files processed"
            self.update_status(status_msg)
            self.update_status_bar(status_msg)
        else:
            status_msg = f"Completed: {self.processed_count}/{self.total_files} files processed"
            self.update_status(status_msg)
            self.update_status_bar(status_msg)
            messagebox.showinfo("Complete", f"Processing completed!\\n{self.processed_count} files processed.")
        
        # Reset progress
        self.root.after(3000, lambda: self.update_progress(0))
    
    def update_status(self, message: str):
        """Update status label (thread-safe)"""
        self.status_label.config(text=message)
    
    def update_progress(self, value: float):
        """Update progress bar (thread-safe)"""
        self.progress_var.set(value)
    
    def update_status_bar(self, message: str):
        """Update status bar (thread-safe)"""
        self.status_bar.config(text=message)
    
    def log_message(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {level}: {message}"
        
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        else:
            self.logger.info(message)
        
        # Update status bar
        self.gui_manager.schedule_update(self.update_status_bar, log_msg)
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_processing:
            if messagebox.askokcancel("Quit", "Processing is in progress. Do you want to quit?"):
                self.cancel_requested = True
                self.is_processing = False
                if self.processing_thread and self.processing_thread.is_alive():
                    self.processing_thread.join(timeout=2)
                self.save_config()
                self.root.destroy()
        else:
            self.save_config()
            self.root.destroy()

def main():
    """Main application entry point"""
    # Create root window
    root = tk.Tk()
    
    # Try to enable drag and drop
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        print("Warning: tkinterdnd2 not available. Drag and drop will be disabled.")
    
    # Create and run application
    app = MainApplication(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()