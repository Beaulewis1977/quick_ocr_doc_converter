"""
Enhanced OCR GUI with Multi-Backend Support

Advanced GUI application with support for multiple OCR backends,
cost tracking, security features, and comprehensive settings.

Author: Terry AI Agent for Terragon Labs
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List
import json
import logging

# Import our enhanced OCR system
from backends import OCRBackendManager
from security import SecurityValidator, CredentialManager
from monitoring import CostTracker

class EnhancedOCRGUI:
    """
    Enhanced OCR GUI with multi-backend support
    
    Features:
    - Multiple OCR backend selection
    - Real-time cost tracking
    - Security validation
    - Batch processing
    - Progress monitoring
    - Configuration management
    """
    
    def __init__(self):
        """Initialize the enhanced OCR GUI"""
        self.setup_logging()
        
        # Initialize components
        self.security_validator = SecurityValidator()
        self.credential_manager = CredentialManager()
        self.cost_tracker = CostTracker()
        self.backend_manager = None
        
        # GUI state
        self.processing = False
        self.current_files = []
        self.results = []
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Enhanced OCR Document Converter")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize backend manager
        self.init_backend_manager()
        
        # Create GUI components
        self.create_widgets()
        self.setup_drag_drop()
        
    def setup_logging(self):
        """Setup logging for the GUI"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("EnhancedOCRGUI")
    
    def init_backend_manager(self):
        """Initialize the OCR backend manager"""
        try:
            self.backend_manager = OCRBackendManager()
            available_backends = self.backend_manager.get_available_backends()
            
            if not available_backends:
                messagebox.showwarning(
                    "No OCR Backends",
                    "No OCR backends are available. Please check your installation and configuration."
                )
            else:
                self.logger.info(f"Available backends: {available_backends}")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize backend manager: {e}")
            messagebox.showerror("Initialization Error", f"Failed to initialize OCR backends: {e}")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main processing tab
        self.create_main_tab()
        
        # Settings tab
        self.create_settings_tab()
        
        # Cost tracking tab
        self.create_cost_tab()
        
        # Backend status tab
        self.create_status_tab()
    
    def create_main_tab(self):
        """Create the main OCR processing tab"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="OCR Processing")
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # File selection buttons
        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Select Files", command=self.select_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_files).pack(side=tk.LEFT, padx=5)
        
        # File list
        self.file_listbox = tk.Listbox(file_frame, height=6)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Backend selection section
        backend_frame = ttk.LabelFrame(main_frame, text="OCR Backend", padding=10)
        backend_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Backend selection
        tk.Label(backend_frame, text="Backend:").pack(side=tk.LEFT)
        self.backend_var = tk.StringVar(value="auto")
        self.backend_combo = ttk.Combobox(backend_frame, textvariable=self.backend_var, state="readonly")
        self.backend_combo.pack(side=tk.LEFT, padx=5)
        self.update_backend_list()
        
        # Language selection
        tk.Label(backend_frame, text="Language:").pack(side=tk.LEFT, padx=(20, 5))
        self.language_var = tk.StringVar(value="en")
        language_combo = ttk.Combobox(backend_frame, textvariable=self.language_var, 
                                    values=["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja"], 
                                    state="readonly", width=5)
        language_combo.pack(side=tk.LEFT, padx=5)
        
        # Processing options
        options_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Quality options
        self.high_accuracy_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="High Accuracy Mode", 
                       variable=self.high_accuracy_var).pack(side=tk.LEFT)
        
        self.offline_only_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Offline Only", 
                       variable=self.offline_only_var).pack(side=tk.LEFT, padx=10)
        
        # Output format
        tk.Label(options_frame, text="Output:").pack(side=tk.LEFT, padx=(20, 5))
        self.output_format_var = tk.StringVar(value="txt")
        format_combo = ttk.Combobox(options_frame, textvariable=self.output_format_var,
                                  values=["txt", "json", "markdown"], state="readonly", width=8)
        format_combo.pack(side=tk.LEFT, padx=5)
        
        # Process button and progress
        process_frame = tk.Frame(main_frame)
        process_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.process_btn = ttk.Button(process_frame, text="Start OCR Processing", 
                                    command=self.start_processing)
        self.process_btn.pack(side=tk.LEFT)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(process_frame, variable=self.progress_var, 
                                          maximum=100, length=300)
        self.progress_bar.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.status_label = tk.Label(process_frame, text="Ready", fg="green")
        self.status_label.pack(side=tk.RIGHT)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Cost info
        cost_frame = tk.Frame(main_frame)
        cost_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.cost_label = tk.Label(cost_frame, text="Current session cost: $0.00", fg="blue")
        self.cost_label.pack(side=tk.LEFT)
        
        ttk.Button(cost_frame, text="Save Results", command=self.save_results).pack(side=tk.RIGHT)
    
    def create_settings_tab(self):
        """Create the settings configuration tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Backend configuration
        backend_config_frame = ttk.LabelFrame(settings_frame, text="Backend Configuration", padding=10)
        backend_config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Google Vision settings
        google_frame = ttk.LabelFrame(backend_config_frame, text="Google Cloud Vision", padding=5)
        google_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(google_frame, text="Credentials File:").pack(side=tk.LEFT)
        self.google_creds_var = tk.StringVar()
        ttk.Entry(google_frame, textvariable=self.google_creds_var, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(google_frame, text="Browse", 
                  command=lambda: self.browse_credentials("google")).pack(side=tk.LEFT)
        
        # AWS Textract settings
        aws_frame = ttk.LabelFrame(backend_config_frame, text="AWS Textract", padding=5)
        aws_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(aws_frame, text="Access Key:").pack(side=tk.LEFT)
        self.aws_key_var = tk.StringVar()
        ttk.Entry(aws_frame, textvariable=self.aws_key_var, width=20, show="*").pack(side=tk.LEFT, padx=5)
        
        tk.Label(aws_frame, text="Secret Key:").pack(side=tk.LEFT, padx=(10, 5))
        self.aws_secret_var = tk.StringVar()
        ttk.Entry(aws_frame, textvariable=self.aws_secret_var, width=20, show="*").pack(side=tk.LEFT, padx=5)
        
        # Azure settings
        azure_frame = ttk.LabelFrame(backend_config_frame, text="Azure Cognitive Services", padding=5)
        azure_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(azure_frame, text="Subscription Key:").pack(side=tk.LEFT)
        self.azure_key_var = tk.StringVar()
        ttk.Entry(azure_frame, textvariable=self.azure_key_var, width=30, show="*").pack(side=tk.LEFT, padx=5)
        
        tk.Label(azure_frame, text="Endpoint:").pack(side=tk.LEFT, padx=(10, 5))
        self.azure_endpoint_var = tk.StringVar()
        ttk.Entry(azure_frame, textvariable=self.azure_endpoint_var, width=30).pack(side=tk.LEFT, padx=5)
        
        # Save/Load configuration
        config_buttons = tk.Frame(backend_config_frame)
        config_buttons.pack(fill=tk.X, pady=10)
        
        ttk.Button(config_buttons, text="Save Configuration", 
                  command=self.save_configuration).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_buttons, text="Load Configuration", 
                  command=self.load_configuration).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_buttons, text="Test Backends", 
                  command=self.test_backends).pack(side=tk.LEFT, padx=5)
        
        # Security settings
        security_frame = ttk.LabelFrame(settings_frame, text="Security Settings", padding=10)
        security_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.pii_masking_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="Enable PII Masking", 
                       variable=self.pii_masking_var).pack(anchor=tk.W)
        
        self.validate_files_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="Validate File Types and Paths", 
                       variable=self.validate_files_var).pack(anchor=tk.W)
        
        # Performance settings
        perf_frame = ttk.LabelFrame(settings_frame, text="Performance Settings", padding=10)
        perf_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(perf_frame, text="Max Concurrent Operations:").pack(side=tk.LEFT)
        self.max_workers_var = tk.IntVar(value=2)
        tk.Spinbox(perf_frame, from_=1, to=8, textvariable=self.max_workers_var, width=5).pack(side=tk.LEFT, padx=5)
        
        tk.Label(perf_frame, text="Cache Size (MB):").pack(side=tk.LEFT, padx=(20, 5))
        self.cache_size_var = tk.IntVar(value=500)
        tk.Spinbox(perf_frame, from_=100, to=2000, increment=100, 
                  textvariable=self.cache_size_var, width=8).pack(side=tk.LEFT, padx=5)
    
    def create_cost_tab(self):
        """Create the cost tracking tab"""
        cost_frame = ttk.Frame(self.notebook)
        self.notebook.add(cost_frame, text="Cost Tracking")
        
        # Current month summary
        summary_frame = ttk.LabelFrame(cost_frame, text="Current Month Summary", padding=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.current_cost_label = tk.Label(summary_frame, text="Total Cost: $0.00", 
                                         font=("Arial", 14, "bold"))
        self.current_cost_label.pack()
        
        self.current_requests_label = tk.Label(summary_frame, text="Total Requests: 0")
        self.current_requests_label.pack()
        
        # Backend breakdown
        breakdown_frame = ttk.LabelFrame(cost_frame, text="Backend Cost Breakdown", padding=10)
        breakdown_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for cost breakdown
        columns = ("Backend", "Requests", "Cost", "Avg Cost/Request", "Success Rate")
        self.cost_tree = ttk.Treeview(breakdown_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.cost_tree.heading(col, text=col)
            self.cost_tree.column(col, width=120)
        
        self.cost_tree.pack(fill=tk.BOTH, expand=True)
        
        # Cost controls
        controls_frame = tk.Frame(cost_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Refresh Stats", 
                  command=self.refresh_cost_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Export Report", 
                  command=self.export_cost_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Set Budgets", 
                  command=self.set_budgets).pack(side=tk.LEFT, padx=5)
        
        # Recommendations
        rec_frame = ttk.LabelFrame(cost_frame, text="Cost Optimization Recommendations", padding=10)
        rec_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.recommendations_text = scrolledtext.ScrolledText(rec_frame, height=6)
        self.recommendations_text.pack(fill=tk.BOTH, expand=True)
    
    def create_status_tab(self):
        """Create the backend status tab"""
        status_frame = ttk.Frame(self.notebook)
        self.notebook.add(status_frame, text="Backend Status")
        
        # Backend status
        backend_status_frame = ttk.LabelFrame(status_frame, text="Backend Availability", padding=10)
        backend_status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Status treeview
        status_columns = ("Backend", "Status", "Type", "Priority", "Cost/Request")
        self.status_tree = ttk.Treeview(backend_status_frame, columns=status_columns, 
                                       show="headings", height=6)
        
        for col in status_columns:
            self.status_tree.heading(col, text=col)
            self.status_tree.column(col, width=120)
        
        self.status_tree.pack(fill=tk.BOTH, expand=True)
        
        # Performance stats
        perf_frame = ttk.LabelFrame(status_frame, text="Performance Statistics", padding=10)
        perf_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.performance_text = scrolledtext.ScrolledText(perf_frame, height=10)
        self.performance_text.pack(fill=tk.BOTH, expand=True)
        
        # Refresh button
        ttk.Button(status_frame, text="Refresh Status", 
                  command=self.refresh_backend_status).pack(pady=5)
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        # This would require tkinterdnd2 or similar library
        # For now, we'll just bind double-click to select files
        self.file_listbox.bind("<Double-Button-1>", lambda e: self.select_files())
    
    def update_backend_list(self):
        """Update the backend selection combo box"""
        if self.backend_manager:
            backends = ["auto"] + self.backend_manager.get_available_backends()
            self.backend_combo['values'] = backends
    
    def select_files(self):
        """Select files for OCR processing"""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp *.gif"),
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select files for OCR",
            filetypes=filetypes
        )
        
        for file in files:
            if file not in self.current_files:
                self.current_files.append(file)
                self.file_listbox.insert(tk.END, Path(file).name)
    
    def clear_files(self):
        """Clear the file list"""
        self.current_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.results.clear()
        self.results_text.delete(1.0, tk.END)
    
    def start_processing(self):
        """Start OCR processing in a separate thread"""
        if not self.current_files:
            messagebox.showwarning("No Files", "Please select files to process.")
            return
        
        if self.processing:
            messagebox.showinfo("Processing", "OCR processing is already in progress.")
            return
        
        # Start processing in background thread
        self.processing = True
        self.process_btn.config(state="disabled", text="Processing...")
        self.progress_var.set(0)
        self.status_label.config(text="Processing...", fg="orange")
        
        thread = threading.Thread(target=self.process_files)
        thread.daemon = True
        thread.start()
    
    def process_files(self):
        """Process files using selected backend"""
        try:
            total_files = len(self.current_files)
            session_cost = 0.0
            
            # Get processing requirements
            requirements = {
                'high_accuracy': self.high_accuracy_var.get(),
                'offline_only': self.offline_only_var.get()
            }
            
            language = self.language_var.get()
            
            for i, file_path in enumerate(self.current_files):
                try:
                    # Update progress
                    progress = (i / total_files) * 100
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    
                    # Validate file if security is enabled
                    if self.validate_files_var.get():
                        self.security_validator.validate_file_path(file_path)
                    
                    # Process with backend manager
                    if self.backend_manager:
                        result = self.backend_manager.process_with_fallback(
                            file_path, language, requirements
                        )
                        
                        # Track cost
                        cost = result.get('cost', 0.0)
                        session_cost += cost
                        
                        # Track usage
                        file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
                        self.cost_tracker.track_usage(
                            result.get('backend_used', 'unknown'),
                            file_path,
                            result,
                            cost,
                            file_size_mb
                        )
                        
                        # Sanitize output if enabled
                        text = result.get('text', '')
                        if self.pii_masking_var.get():
                            text = self.security_validator.sanitize_ocr_output(text)
                            result['text'] = text
                        
                        self.results.append(result)
                        
                        # Update results display
                        self.root.after(0, lambda r=result, f=file_path: self.update_results_display(r, f))
                        
                    else:
                        raise Exception("Backend manager not available")
                        
                except Exception as e:
                    error_result = {
                        'text': '',
                        'success': False,
                        'error': str(e),
                        'file_path': file_path
                    }
                    self.results.append(error_result)
                    self.root.after(0, lambda r=error_result, f=file_path: self.update_results_display(r, f))
            
            # Update final progress and cost
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda c=session_cost: self.cost_label.config(text=f"Current session cost: ${c:.4f}"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Processing Error", f"An error occurred: {e}"))
        finally:
            # Reset UI state
            self.root.after(0, self.processing_complete)
    
    def update_results_display(self, result: Dict[str, Any], file_path: str):
        """Update the results display"""
        filename = Path(file_path).name
        
        if result.get('success', False):
            text = result.get('text', '')
            confidence = result.get('confidence', 0)
            backend = result.get('backend_used', 'unknown')
            
            self.results_text.insert(tk.END, f"\n{'='*50}\n")
            self.results_text.insert(tk.END, f"File: {filename}\n")
            self.results_text.insert(tk.END, f"Backend: {backend}\n")
            self.results_text.insert(tk.END, f"Confidence: {confidence:.1f}%\n")
            self.results_text.insert(tk.END, f"{'='*50}\n")
            self.results_text.insert(tk.END, f"{text}\n")
        else:
            error = result.get('error', 'Unknown error')
            self.results_text.insert(tk.END, f"\n{'='*50}\n")
            self.results_text.insert(tk.END, f"File: {filename}\n")
            self.results_text.insert(tk.END, f"ERROR: {error}\n")
        
        self.results_text.see(tk.END)
    
    def processing_complete(self):
        """Called when processing is complete"""
        self.processing = False
        self.process_btn.config(state="normal", text="Start OCR Processing")
        self.status_label.config(text="Complete", fg="green")
        self.refresh_cost_stats()
    
    def save_results(self):
        """Save OCR results to file"""
        if not self.results:
            messagebox.showwarning("No Results", "No results to save.")
            return
        
        output_format = self.output_format_var.get()
        
        if output_format == "json":
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, indent=2, default=str)
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for result in self.results:
                        f.write(f"File: {result.get('file_path', 'Unknown')}\n")
                        f.write(f"Backend: {result.get('backend_used', 'Unknown')}\n")
                        f.write(f"Success: {result.get('success', False)}\n")
                        if result.get('success'):
                            f.write(f"Text:\n{result.get('text', '')}\n")
                        else:
                            f.write(f"Error: {result.get('error', '')}\n")
                        f.write("\n" + "="*50 + "\n\n")
        
        messagebox.showinfo("Saved", f"Results saved to {file_path}")
    
    def browse_credentials(self, service: str):
        """Browse for credentials file"""
        file_path = filedialog.askopenfilename(
            title=f"Select {service} credentials file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if service == "google":
                self.google_creds_var.set(file_path)
    
    def save_configuration(self):
        """Save backend configuration"""
        try:
            # Save Google Vision credentials
            if self.google_creds_var.get():
                google_creds = {'credentials_path': self.google_creds_var.get()}
                self.credential_manager.store_credentials('google_vision', google_creds)
            
            # Save AWS credentials
            if self.aws_key_var.get() and self.aws_secret_var.get():
                aws_creds = {
                    'access_key_id': self.aws_key_var.get(),
                    'secret_access_key': self.aws_secret_var.get(),
                    'region': 'us-east-1'
                }
                self.credential_manager.store_credentials('aws_textract', aws_creds)
            
            # Save Azure credentials
            if self.azure_key_var.get() and self.azure_endpoint_var.get():
                azure_creds = {
                    'subscription_key': self.azure_key_var.get(),
                    'endpoint': self.azure_endpoint_var.get()
                }
                self.credential_manager.store_credentials('azure_vision', azure_creds)
            
            # Reinitialize backend manager
            self.init_backend_manager()
            self.update_backend_list()
            
            messagebox.showinfo("Saved", "Configuration saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def load_configuration(self):
        """Load backend configuration"""
        try:
            # Load Google Vision credentials
            google_creds = self.credential_manager.get_credentials('google_vision')
            if google_creds and 'credentials_path' in google_creds:
                self.google_creds_var.set(google_creds['credentials_path'])
            
            # Load AWS credentials (don't show actual keys for security)
            aws_creds = self.credential_manager.get_credentials('aws_textract')
            if aws_creds:
                self.aws_key_var.set("*" * 10 if aws_creds.get('access_key_id') else "")
                self.aws_secret_var.set("*" * 10 if aws_creds.get('secret_access_key') else "")
            
            # Load Azure credentials
            azure_creds = self.credential_manager.get_credentials('azure_vision')
            if azure_creds:
                self.azure_key_var.set("*" * 10 if azure_creds.get('subscription_key') else "")
                self.azure_endpoint_var.set(azure_creds.get('endpoint', ''))
            
            messagebox.showinfo("Loaded", "Configuration loaded successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
    
    def test_backends(self):
        """Test all configured backends"""
        if not self.backend_manager:
            messagebox.showerror("Error", "Backend manager not available")
            return
        
        results = []
        status = self.backend_manager.get_backend_status()
        
        for backend_name, info in status.items():
            availability = "Available" if info['available'] else "Not Available"
            results.append(f"{backend_name}: {availability}")
        
        messagebox.showinfo("Backend Test Results", "\n".join(results))
    
    def refresh_cost_stats(self):
        """Refresh cost tracking statistics"""
        try:
            # Update current month summary
            current_cost = self.cost_tracker.get_current_month_cost()
            current_requests = self.cost_tracker.get_current_month_requests()
            
            self.current_cost_label.config(text=f"Total Cost: ${current_cost:.2f}")
            self.current_requests_label.config(text=f"Total Requests: {current_requests}")
            
            # Update backend breakdown
            self.cost_tree.delete(*self.cost_tree.get_children())
            
            backend_costs = self.cost_tracker.get_backend_costs(30)
            stats = self.cost_tracker.get_usage_stats(30)
            backend_stats = stats.get('backend_stats', {})
            
            for backend, cost in backend_costs.items():
                backend_info = backend_stats.get(backend, {})
                requests = backend_info.get('requests', 0)
                avg_cost = backend_info.get('cost_per_request', 0)
                success_rate = f"{(requests / max(1, requests)) * 100:.1f}%"
                
                self.cost_tree.insert('', tk.END, values=(
                    backend, requests, f"${cost:.4f}", f"${avg_cost:.4f}", success_rate
                ))
            
            # Update recommendations
            recommendations = self.cost_tracker.get_cost_optimization_recommendations()
            self.recommendations_text.delete(1.0, tk.END)
            
            if recommendations:
                for rec in recommendations:
                    self.recommendations_text.insert(tk.END, f"• {rec['title']}\n")
                    self.recommendations_text.insert(tk.END, f"  {rec['description']}\n")
                    if rec.get('potential_savings', 0) > 0:
                        self.recommendations_text.insert(tk.END, 
                            f"  Potential savings: ${rec['potential_savings']:.2f}\n")
                    self.recommendations_text.insert(tk.END, "\n")
            else:
                self.recommendations_text.insert(tk.END, "No recommendations at this time.")
                
        except Exception as e:
            self.logger.error(f"Failed to refresh cost stats: {e}")
    
    def export_cost_report(self):
        """Export detailed cost report"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if file_path:
            if self.cost_tracker.export_usage_report(file_path):
                messagebox.showinfo("Exported", f"Cost report exported to {file_path}")
            else:
                messagebox.showerror("Error", "Failed to export cost report")
    
    def set_budgets(self):
        """Open budget setting dialog"""
        # This would open a new dialog window for setting budgets
        messagebox.showinfo("Budget Setting", "Budget setting feature coming soon!")
    
    def refresh_backend_status(self):
        """Refresh backend status information"""
        if not self.backend_manager:
            return
        
        try:
            # Update status tree
            self.status_tree.delete(*self.status_tree.get_children())
            
            status = self.backend_manager.get_backend_status()
            for backend_name, info in status.items():
                status_text = "Available" if info['available'] else "Not Available"
                backend_type = info['type'].title()
                priority = str(info['priority'])
                cost = f"${info['cost_per_request']:.4f}"
                
                self.status_tree.insert('', tk.END, values=(
                    backend_name, status_text, backend_type, priority, cost
                ))
            
            # Update performance stats
            self.performance_text.delete(1.0, tk.END)
            
            for backend_name, info in status.items():
                perf_stats = info.get('performance_stats', {})
                self.performance_text.insert(tk.END, f"{backend_name}:\n")
                self.performance_text.insert(tk.END, f"  Total Requests: {perf_stats.get('total_requests', 0)}\n")
                self.performance_text.insert(tk.END, f"  Successful: {perf_stats.get('successful_requests', 0)}\n")
                self.performance_text.insert(tk.END, f"  Failed: {perf_stats.get('failed_requests', 0)}\n")
                self.performance_text.insert(tk.END, f"  Avg Duration: {perf_stats.get('avg_duration', 0):.2f}s\n\n")
                
        except Exception as e:
            self.logger.error(f"Failed to refresh backend status: {e}")
    
    def run(self):
        """Start the GUI application"""
        # Initial refresh of data
        self.refresh_cost_stats()
        self.refresh_backend_status()
        
        # Start the main loop
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = EnhancedOCRGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start Enhanced OCR GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()