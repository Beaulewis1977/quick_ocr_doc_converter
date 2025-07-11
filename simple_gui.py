#!/usr/bin/env python3
"""
Simple GUI version of Universal Document Converter
Guaranteed to work without complex dependencies
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path

# Import the converter
try:
    from universal_document_converter import UniversalConverter, FormatDetector
    CONVERTER_AVAILABLE = True
except ImportError:
    CONVERTER_AVAILABLE = False

class SimpleConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Document Convertor")
        self.root.geometry("600x500")
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.input_format = tk.StringVar(value='auto')
        self.output_format = tk.StringVar(value='markdown')
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready to convert documents")
        
        # Set default output
        desktop = Path.home() / "Desktop" / "converted_documents"
        self.output_path.set(str(desktop))
        
        if CONVERTER_AVAILABLE:
            self.converter = UniversalConverter()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title = ttk.Label(main_frame, text="Quick Document Convertor",
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input selection
        ttk.Label(main_frame, text="Input Files/Folder:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(input_frame, text="Browse Files", 
                  command=self.browse_files).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(input_frame, text="Browse Folder", 
                  command=self.browse_folder).grid(row=0, column=2)
        
        # Output selection
        ttk.Label(main_frame, text="Output Folder:", font=('Arial', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(output_frame, text="Browse", 
                  command=self.browse_output).grid(row=0, column=1)
        
        # Format selection
        format_frame = ttk.LabelFrame(main_frame, text="Format Options", padding="10")
        format_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        format_frame.columnconfigure(1, weight=1)
        format_frame.columnconfigure(3, weight=1)
        
        ttk.Label(format_frame, text="From:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        input_formats = ['auto', 'docx', 'pdf', 'txt', 'html', 'rtf']
        self.input_combo = ttk.Combobox(format_frame, textvariable=self.input_format,
                                       values=input_formats, state='readonly')
        self.input_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        ttk.Label(format_frame, text="To:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        
        output_formats = ['markdown', 'txt', 'html', 'rtf']
        self.output_combo = ttk.Combobox(format_frame, textvariable=self.output_format,
                                        values=output_formats, state='readonly')
        self.output_combo.grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert Documents",
                                     command=self.start_conversion)
        self.convert_btn.grid(row=6, column=0, columnspan=3, pady=(0, 15))
        
        # Progress
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Results
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        self.results_text = tk.Text(results_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Check if converter is available
        if not CONVERTER_AVAILABLE:
            self.log_message("ERROR: Converter module not available. Please check installation.")
            self.convert_btn.config(state='disabled')
        else:
            self.log_message("SUCCESS: Quick Document Convertor ready!")
    
    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Select files to convert",
            filetypes=[
                ("All supported", "*.docx;*.pdf;*.txt;*.html;*.htm;*.rtf;*.epub"),
                ("All files", "*.*")
            ]
        )
        if files:
            self.input_path.set(";".join(files))
            self.log_message(f"Selected {len(files)} file(s)")
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            self.input_path.set(folder)
            self.log_message(f"Selected folder: {os.path.basename(folder)}")
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_path.set(folder)
    
    def log_message(self, message):
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def start_conversion(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select input files or folder")
            return
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select output folder")
            return
        
        self.convert_btn.config(state='disabled')
        self.progress_var.set(0)
        self.results_text.delete(1.0, tk.END)
        
        # Start conversion in thread
        thread = threading.Thread(target=self.convert_documents)
        thread.daemon = True
        thread.start()
    
    def convert_documents(self):
        try:
            if not CONVERTER_AVAILABLE:
                self.log_message("ERROR: Converter not available")
                return
            
            input_path = self.input_path.get()
            output_dir = Path(self.output_path.get())
            input_fmt = self.input_format.get()
            output_fmt = self.output_format.get()
            
            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine files to convert
            files_to_convert = []
            
            if ";" in input_path:
                # Multiple files
                files_to_convert = [Path(f) for f in input_path.split(";")]
            elif os.path.isfile(input_path):
                # Single file
                files_to_convert = [Path(input_path)]
            elif os.path.isdir(input_path):
                # Directory
                input_dir = Path(input_path)
                for ext in ['.docx', '.pdf', '.txt', '.html', '.htm', '.rtf']:
                    files_to_convert.extend(input_dir.rglob(f"*{ext}"))
            
            if not files_to_convert:
                self.log_message("ERROR: No supported files found")
                return

            self.log_message(f"Converting {len(files_to_convert)} files...")
            
            successful = 0
            failed = 0
            
            for i, file_path in enumerate(files_to_convert):
                try:
                    # Generate output path
                    if output_fmt == 'markdown':
                        output_ext = '.md'
                    elif output_fmt == 'txt':
                        output_ext = '.txt'
                    elif output_fmt == 'html':
                        output_ext = '.html'
                    elif output_fmt == 'rtf':
                        output_ext = '.rtf'
                    
                    output_file = output_dir / f"{file_path.stem}{output_ext}"
                    
                    # Convert
                    self.converter.convert_file(file_path, output_file, input_fmt, output_fmt)
                    
                    successful += 1
                    self.log_message(f"SUCCESS: {file_path.name} -> {output_file.name}")

                except Exception as e:
                    failed += 1
                    self.log_message(f"ERROR: {file_path.name}: {str(e)}")
                
                # Update progress
                progress = ((i + 1) / len(files_to_convert)) * 100
                self.progress_var.set(progress)
                self.update_status(f"Converting... {i+1}/{len(files_to_convert)}")
            
            # Final results
            self.log_message(f"\nConversion complete!")
            self.log_message(f"Successful: {successful}")
            self.log_message(f"Failed: {failed}")
            self.log_message(f"Output: {output_dir}")
            
            self.update_status(f"Complete! {successful} converted, {failed} failed")
            
            messagebox.showinfo("Complete", f"Converted {successful} files!\nFailed: {failed}")
            
        except Exception as e:
            self.log_message(f"ERROR: {str(e)}")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
        
        finally:
            self.convert_btn.config(state='normal')

def main():
    root = tk.Tk()
    app = SimpleConverterGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
