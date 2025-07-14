import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import logging
from ocr_engine import OCREngine

class OCRGUI:
    """
    Enhanced GUI for OCR Document Converter
    Integrates OCR functionality with user-friendly interface
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OCR Document Converter")
        self.root.geometry("800x600")
        
        # Initialize OCR engine
        self.ocr = OCREngine()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="OCR Document Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # OCR Status
        self.ocr_status = ttk.Label(main_frame, text="OCR Status: Checking...",
                                   foreground="blue")
        self.ocr_status.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # File entry
        ttk.Label(file_frame, text="Select files or folder:").grid(row=0, column=0, sticky=tk.W)
        self.file_path = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.grid(row=0, column=1, padx=(5, 5))
        
        # Browse buttons
        ttk.Button(file_frame, text="Browse Files", command=self.browse_files).grid(row=0, column=2, padx=(5, 0))
        ttk.Button(file_frame, text="Browse Folder", command=self.browse_folder).grid(row=0, column=3, padx=(5, 0))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Conversion Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # OCR options
        self.use_ocr = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Enable OCR for images/PDFs", 
                       variable=self.use_ocr).grid(row=0, column=0, sticky=tk.W)
        
        # Language selection
        ttk.Label(options_frame, text="OCR Language:").grid(row=0, column=1, padx=(20, 5))
        self.language_var = tk.StringVar(value="eng")
        language_combo = ttk.Combobox(options_frame, textvariable=self.language_var, 
                                     values=["eng", "eng+fra", "eng+spa", "deu", "jpn"], width=15)
        language_combo.grid(row=0, column=2)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        # Progress label
        self.progress_label = ttk.Label(progress_frame, text="Ready")
        self.progress_label.grid(row=1, column=0, columnspan=2)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Log text area with scrollbar
        log_scroll = ttk.Scrollbar(log_frame)
        log_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.log_text = tk.Text(log_frame, height=10, width=80, yscrollcommand=log_scroll.set)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scroll.config(command=self.log_text.yview)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Start Conversion", 
                  command=self.start_conversion).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).grid(row=0, column=2)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Update OCR status
        self.update_ocr_status()
        
    def update_ocr_status(self):
        """Update OCR status label"""
        if self.ocr.is_available():
            self.ocr_status.config(text="OCR Status: Ready", foreground="green")
        else:
            self.ocr_status.config(text="OCR Status: Tesseract not found - OCR disabled", 
                                 foreground="red")
    
    def browse_files(self):
        """Browse for individual files"""
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[
                ("Supported files", "*.pdf *.png *.jpg *.jpeg *.tiff *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        if files:
            self.file_path.set(";".join(files))
    
    def browse_folder(self):
        """Browse for folder"""
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            self.file_path.set(folder)
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)
    
    def start_conversion(self):
        """Start the conversion process"""
        path = self.file_path.get()
        if not path:
            messagebox.showwarning("Warning", "Please select files or folder first!")
            return
        
        # Start conversion in separate thread
        thread = threading.Thread(target=self.convert_files, args=(path,))
        thread.daemon = True
        thread.start()
    
    def convert_files(self, path):
        """Convert files with progress tracking"""
        try:
            # Determine files to process
            files_to_process = []
            
            if os.path.isfile(path):
                files_to_process = [path]
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                            files_to_process.append(os.path.join(root, file))
            else:
                # Multiple files from browse
                files_to_process = path.split(';')
            
            if not files_to_process:
                self.log_message("No supported files found!")
                return
            
            total_files = len(files_to_process)
            self.log_message(f"Found {total_files} files to process")
            
            # Process files
            for i, file_path in enumerate(files_to_process, 1):
                self.log_message(f"Processing file {i}/{total_files}: {os.path.basename(file_path)}")
                
                # Update progress
                self.progress['value'] = (i / total_files) * 100
                self.progress_label.config(text=f"Processing {i}/{total_files}")
                
                try:
                    # Convert file
                    output_path = self.convert_single_file(file_path)
                    if output_path:
                        self.log_message(f"✓ Converted: {os.path.basename(file_path)} -> {os.path.basename(output_path)}")
                    else:
                        self.log_message(f"✗ Failed to convert: {os.path.basename(file_path)}")
                
                except Exception as e:
                    self.log_message(f"Error processing {file_path}: {str(e)}")
            
            self.log_message("Conversion completed!")
            self.progress['value'] = 100
            self.progress_label.config(text="Complete")
            
            messagebox.showinfo("Complete", f"Processed {total_files} files!")
            
        except Exception as e:
            self.log_message(f"Conversion error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def convert_single_file(self, file_path):
        """Convert a single file"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']:
                # Image file - use OCR if enabled
                if self.use_ocr.get() and self.ocr.is_available():
                    text = self.ocr.extract_text(file_path, self.language_var.get())
                else:
                    # Basic conversion without OCR
                    return None
                
                # Save as markdown
                output_path = file_path.rsplit('.', 1)[0] + '.md'
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {os.path.basename(file_path)}\n\n")
                    f.write(text)
                
                return output_path
            
            elif file_ext == '.pdf':
                # PDF file - use OCR if enabled
                if self.use_ocr.get() and self.ocr.is_available():
                    text = self.ocr.extract_text_from_pdf(file_path, self.language_var.get())
                else:
                    # Basic PDF text extraction
                    try:
                        import fitz
                        doc = fitz.open(file_path)
                        text = ""
                        for page in doc:
                            text += page.get_text()
                        doc.close()
                    except ImportError:
                        return None
                
                # Save as markdown
                output_path = file_path.rsplit('.', 1)[0] + '.md'
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {os.path.basename(file_path)}\n\n")
                    f.write(text)
                
                return output_path
            
            return None
            
        except Exception as e:
            self.log_message(f"Error converting {file_path}: {str(e)}")
            return None
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = OCRGUI()
    app.run()