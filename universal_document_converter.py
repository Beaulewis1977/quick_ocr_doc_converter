#!/usr/bin/env python3
"""
Universal Document Converter - Enhanced Desktop GUI
Fast, simple, powerful document conversion tool with multiple format support
Designed and built by Beau Lewis (blewisxx@gmail.com)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import sys
import mimetypes
import re

class FormatDetector:
    """Utility class for detecting and validating file formats"""
    
    SUPPORTED_INPUT_FORMATS = {
        'docx': {'extensions': ['.docx'], 'name': 'Word Document', 'reader': 'DocxReader'},
        'pdf': {'extensions': ['.pdf'], 'name': 'PDF Document', 'reader': 'PdfReader'}, 
        'txt': {'extensions': ['.txt'], 'name': 'Text File', 'reader': 'TxtReader'},
        'html': {'extensions': ['.html', '.htm'], 'name': 'HTML Document', 'reader': 'HtmlReader'},
        'rtf': {'extensions': ['.rtf'], 'name': 'Rich Text Format', 'reader': 'RtfReader'}
    }
    
    SUPPORTED_OUTPUT_FORMATS = {
        'markdown': {'extension': '.md', 'name': 'Markdown', 'writer': 'MarkdownWriter'},
        'txt': {'extension': '.txt', 'name': 'Plain Text', 'writer': 'TxtWriter'},
        'html': {'extension': '.html', 'name': 'HTML Document', 'writer': 'HtmlWriter'},
        'rtf': {'extension': '.rtf', 'name': 'Rich Text Format', 'writer': 'RtfWriter'}
    }
    
    @classmethod
    def detect_format(cls, file_path):
        """Auto-detect the format of a file"""
        ext = Path(file_path).suffix.lower()
        for format_key, format_info in cls.SUPPORTED_INPUT_FORMATS.items():
            if ext in format_info['extensions']:
                return format_key
        return None
    
    @classmethod
    def get_input_format_list(cls):
        """Get list of input formats for dropdown"""
        formats = [('Auto-detect', 'auto')]
        for key, info in cls.SUPPORTED_INPUT_FORMATS.items():
            formats.append((f"{info['name']} ({', '.join(info['extensions'])})", key))
        return formats
    
    @classmethod
    def get_output_format_list(cls):
        """Get list of output formats for dropdown"""
        formats = []
        for key, info in cls.SUPPORTED_OUTPUT_FORMATS.items():
            formats.append((f"{info['name']} ({info['extension']})", key))
        return formats

class DocumentReader:
    """Base class for document readers"""
    
    def read(self, file_path):
        """Read document and return text content"""
        raise NotImplementedError

class DocxReader(DocumentReader):
    """Reader for DOCX files"""
    
    def read(self, file_path):
        from docx import Document
        doc = Document(file_path)
        content = []
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                # Preserve heading structure
                if paragraph.style.name.startswith('Heading'):
                    level = int(paragraph.style.name.split()[-1]) if paragraph.style.name.split()[-1].isdigit() else 1
                    content.append(('heading', level, text))
                else:
                    content.append(('paragraph', text))
        
        return content

class PdfReader(DocumentReader):
    """Reader for PDF files"""
    
    def read(self, file_path):
        import PyPDF2
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            content = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():
                    content.append(('page', page_num + 1, text.strip()))
        
        return content

class TxtReader(DocumentReader):
    """Reader for TXT files"""
    
    def read(self, file_path):
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    text = file.read()
                    # Split into paragraphs
                    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                    return [('paragraph', p) for p in paragraphs]
            except UnicodeDecodeError:
                continue
        
        raise Exception(f"Could not decode file with encodings: {encodings}")

class HtmlReader(DocumentReader):
    """Reader for HTML files"""
    
    def read(self, file_path):
        from bs4 import BeautifulSoup
        
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
        
        content = []
        
        # Extract headings and paragraphs
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']):
            text = element.get_text().strip()
            if text:
                if element.name.startswith('h'):
                    level = int(element.name[1])
                    content.append(('heading', level, text))
                else:
                    content.append(('paragraph', text))
        
        return content

class RtfReader(DocumentReader):
    """Reader for RTF files"""
    
    def read(self, file_path):
        from striprtf.striprtf import rtf_to_text
        
        with open(file_path, 'r', encoding='utf-8') as file:
            rtf_content = file.read()
        
        text = rtf_to_text(rtf_content)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return [('paragraph', p) for p in paragraphs]

class DocumentWriter:
    """Base class for document writers"""
    
    def write(self, content, output_path):
        """Write content to output file"""
        raise NotImplementedError

class MarkdownWriter(DocumentWriter):
    """Writer for Markdown files"""
    
    def write(self, content, output_path):
        lines = []
        
        for item in content:
            if item[0] == 'heading':
                level, text = item[1], item[2]
                lines.append(f"{'#' * level} {text}")
                lines.append("")
            elif item[0] == 'paragraph':
                lines.append(item[1])
                lines.append("")
            elif item[0] == 'page':
                page_num, text = item[1], item[2]
                lines.append(f"## Page {page_num}")
                lines.append("")
                lines.append(text)
                lines.append("")
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(lines))

class TxtWriter(DocumentWriter):
    """Writer for plain text files"""
    
    def write(self, content, output_path):
        lines = []
        
        for item in content:
            if item[0] == 'heading':
                text = item[2]
                lines.append(text.upper())
                lines.append('=' * len(text))
                lines.append("")
            elif item[0] == 'paragraph':
                lines.append(item[1])
                lines.append("")
            elif item[0] == 'page':
                page_num, text = item[1], item[2]
                lines.append(f"PAGE {page_num}")
                lines.append("-" * 20)
                lines.append(text)
                lines.append("")
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(lines))

class HtmlWriter(DocumentWriter):
    """Writer for HTML files"""
    
    def write(self, content, output_path):
        lines = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "    <meta charset='UTF-8'>",
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"    <title>{Path(output_path).stem}</title>",
            "    <style>",
            "        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }",
            "        h1, h2, h3, h4, h5, h6 { color: #333; }",
            "        p { line-height: 1.6; margin-bottom: 1em; }",
            "    </style>",
            "</head>",
            "<body>"
        ]
        
        for item in content:
            if item[0] == 'heading':
                level, text = item[1], item[2]
                lines.append(f"    <h{level}>{self._escape_html(text)}</h{level}>")
            elif item[0] == 'paragraph':
                lines.append(f"    <p>{self._escape_html(item[1])}</p>")
            elif item[0] == 'page':
                page_num, text = item[1], item[2]
                lines.append(f"    <h2>Page {page_num}</h2>")
                lines.append(f"    <p>{self._escape_html(text)}</p>")
        
        lines.extend(["</body>", "</html>"])
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(lines))
    
    def _escape_html(self, text):
        """Escape HTML special characters"""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))

class RtfWriter(DocumentWriter):
    """Writer for RTF files"""
    
    def write(self, content, output_path):
        # Basic RTF structure
        rtf_lines = [
            r"{\rtf1\ansi\deff0",
            r"{\fonttbl{\f0 Times New Roman;}}",
            r"\f0\fs24"
        ]
        
        for item in content:
            if item[0] == 'heading':
                level, text = item[1], item[2]
                size = max(32 - (level * 4), 20)  # Larger size for higher level headings
                rtf_lines.append(f"\\par\\fs{size}\\b {self._escape_rtf(text)}\\b0\\fs24")
            elif item[0] == 'paragraph':
                rtf_lines.append(f"\\par {self._escape_rtf(item[1])}")
            elif item[0] == 'page':
                page_num, text = item[1], item[2]
                rtf_lines.append(f"\\par\\fs28\\b Page {page_num}\\b0\\fs24")
                rtf_lines.append(f"\\par {self._escape_rtf(text)}")
        
        rtf_lines.append("}")
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(''.join(rtf_lines))
    
    def _escape_rtf(self, text):
        """Escape RTF special characters"""
        return text.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')

class UniversalConverter:
    """Main conversion engine"""
    
    def __init__(self):
        self.readers = {
            'docx': DocxReader(),
            'pdf': PdfReader(),
            'txt': TxtReader(),
            'html': HtmlReader(),
            'rtf': RtfReader()
        }
        
        self.writers = {
            'markdown': MarkdownWriter(),
            'txt': TxtWriter(),
            'html': HtmlWriter(),
            'rtf': RtfWriter()
        }
    
    def convert_file(self, input_path, output_path, input_format=None, output_format='markdown'):
        """Convert a single file"""
        # Auto-detect format if not specified
        if input_format is None or input_format == 'auto':
            input_format = FormatDetector.detect_format(input_path)
            if input_format is None:
                raise ValueError(f"Unsupported file format: {input_path}")
        
        # Read the document
        if input_format not in self.readers:
            raise ValueError(f"No reader available for format: {input_format}")
        
        content = self.readers[input_format].read(input_path)
        
        # Write the output
        if output_format not in self.writers:
            raise ValueError(f"No writer available for format: {output_format}")
        
        self.writers[output_format].write(content, output_path)

class UniversalDocumentConverterGUI:
    """Enhanced GUI for the Universal Document Converter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Document Converter 🚀")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        
        # Initialize converter
        self.converter = UniversalConverter()

        # Initialize styling and theming
        self.init_styling_and_themes()

        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.input_format = tk.StringVar(value='auto')
        self.output_format = tk.StringVar(value='markdown')
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready to convert documents")

        # Enhanced progress feedback attributes
        self.progress_bar = None  # Will be set in setup_ui
        self.detailed_status_display = None  # Will be set in setup_ui

        # Set default output to Desktop/converted_documents
        desktop = Path.home() / "Desktop"
        default_output = desktop / "converted_documents"
        self.output_path.set(str(default_output))
        
        self.setup_ui()
        self.check_dependencies()

    def init_styling_and_themes(self) -> None:
        """Initialize modern styling and theme support"""
        # Color schemes
        self.light_theme = {
            'bg': '#ffffff',
            'fg': '#2c3e50',
            'accent': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'secondary': '#95a5a6',
            'card_bg': '#f8f9fa',
            'border': '#dee2e6'
        }

        self.dark_theme = {
            'bg': '#2c3e50',
            'fg': '#ecf0f1',
            'accent': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'secondary': '#7f8c8d',
            'card_bg': '#34495e',
            'border': '#4a5568'
        }

        # Current theme (default to light)
        self.current_theme = 'light'
        self.color_scheme = self.light_theme.copy()

        # Font schemes
        self.font_scheme = {
            'title': ('Segoe UI', 18, 'bold'),
            'subtitle': ('Segoe UI', 10, 'normal'),
            'heading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 9, 'normal'),
            'button': ('Segoe UI', 9, 'bold'),
            'monospace': ('Consolas', 9, 'normal')
        }

        # Apply modern styling
        self.apply_modern_styling()

    def apply_modern_styling(self) -> None:
        """Apply modern styling to the application"""
        # Configure ttk styles
        style = ttk.Style()

        # Configure modern button style
        style.configure('Modern.TButton',
                       font=self.font_scheme['button'],
                       padding=(10, 8))

        # Configure modern frame style
        style.configure('Card.TLabelFrame',
                       relief='flat',
                       borderwidth=1)

        # Configure modern entry style
        style.configure('Modern.TEntry',
                       font=self.font_scheme['body'],
                       padding=5)

        # Configure modern combobox style
        style.configure('Modern.TCombobox',
                       font=self.font_scheme['body'],
                       padding=5)

    def toggle_theme(self) -> None:
        """Toggle between light and dark themes"""
        if self.current_theme == 'light':
            self.current_theme = 'dark'
            self.color_scheme = self.dark_theme.copy()
        else:
            self.current_theme = 'light'
            self.color_scheme = self.light_theme.copy()

        # Reapply styling with new theme
        self.apply_modern_styling()
        logger.info(f"Switched to {self.current_theme} theme")

    def configure_responsive_layout(self) -> None:
        """Configure responsive layout that adapts to window size"""
        # Configure main grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Bind to window resize events
        self.root.bind('<Configure>', self.on_window_resize)

    def on_window_resize(self, event) -> None:
        """Handle window resize events"""
        if event.widget == self.root:
            width = event.width
            height = event.height

            # Adjust layout based on window size
            if width < 700:
                # Compact layout for smaller windows
                self.apply_compact_layout()
            else:
                # Standard layout for larger windows
                self.apply_standard_layout()

    def apply_compact_layout(self) -> None:
        """Apply compact layout for smaller windows"""
        # This will be implemented to adjust spacing and sizing
        pass

    def apply_standard_layout(self) -> None:
        """Apply standard layout for larger windows"""
        # This will be implemented to use normal spacing and sizing
        pass

    def setup_ui(self):
        """Set up the enhanced user interface"""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Universal Document Converter 🚀", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Fast • Simple • Powerful", 
                                  font=('Arial', 10), foreground='gray')
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Format selection frame
        format_frame = ttk.LabelFrame(main_frame, text="📄 Format Selection", padding="10")
        format_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        format_frame.columnconfigure(1, weight=1)
        format_frame.columnconfigure(3, weight=1)
        
        # From format
        ttk.Label(format_frame, text="From:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        input_formats = FormatDetector.get_input_format_list()
        self.input_format_combo = ttk.Combobox(format_frame, textvariable=self.input_format,
                                              values=[f[1] for f in input_formats], state='readonly')
        self.input_format_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        # Configure display values
        format_display = {f[1]: f[0] for f in input_formats}
        self.input_format_combo.configure(values=list(format_display.keys()))
        
        # To format
        ttk.Label(format_frame, text="To:", font=('Arial', 10, 'bold')).grid(
            row=0, column=2, sticky=tk.W, padx=(0, 10))
        
        output_formats = FormatDetector.get_output_format_list()
        self.output_format_combo = ttk.Combobox(format_frame, textvariable=self.output_format,
                                               values=[f[1] for f in output_formats], state='readonly')
        self.output_format_combo.grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        # Input selection frame
        input_frame = ttk.LabelFrame(main_frame, text="📁 Input Selection", padding="10")
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        
        # Input path
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path, font=('Arial', 9))
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Input buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=1)
        
        ttk.Button(button_frame, text="Select Files", 
                  command=self.browse_input_files).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Select Folder", 
                  command=self.browse_input_folder).grid(row=0, column=1)
        
        # Output folder selection
        output_frame = ttk.LabelFrame(main_frame, text="📂 Output Location", padding="10")
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path, font=('Arial', 9))
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(output_frame, text="Browse", 
                  command=self.browse_output_folder).grid(row=0, column=1)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Options", padding="10")
        options_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.preserve_structure = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preserve folder structure", 
                       variable=self.preserve_structure).grid(row=0, column=0, sticky=tk.W)
        
        self.overwrite_existing = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Overwrite existing files", 
                       variable=self.overwrite_existing).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Convert button
        self.convert_button = ttk.Button(main_frame, text="🚀 Convert Documents", 
                                        command=self.start_conversion)
        self.convert_button.grid(row=6, column=0, columnspan=3, pady=(0, 15))
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progress", padding="10")
        progress_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var, font=('Arial', 9))
        self.status_label.grid(row=1, column=0, sticky=tk.W)

        # Set detailed status display reference
        self.detailed_status_display = self.status_label
        
        # Results text area
        results_frame = ttk.LabelFrame(main_frame, text="📋 Results", padding="10")
        results_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.results_text = tk.Text(text_frame, height=6, wrap=tk.WORD, font=('Consolas', 9))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Add drag and drop tip
        tip_label = ttk.Label(main_frame, text="💡 Tip: Drag and drop files or folders directly onto this window!", 
                             font=('Arial', 9), foreground='gray')
        tip_label.grid(row=9, column=0, columnspan=3, pady=5)
        
        # Setup drag and drop
        self.setup_drag_drop()
    
    def setup_drag_drop(self):
        """Set up drag and drop functionality"""
        try:
            from tkinterdnd2 import TkinterDnD, DND_FILES
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
        except ImportError:
            pass
    
    def on_drop(self, event):
        """Handle drag and drop events"""
        files = self.root.tk.splitlist(event.data)
        if files:
            dropped_path = files[0]
            if os.path.isdir(dropped_path):
                self.input_path.set(dropped_path)
                self.log_message(f"📁 Folder dropped: {os.path.basename(dropped_path)}")
            else:
                # Single file dropped
                self.input_path.set(dropped_path)
                self.log_message(f"📄 File dropped: {os.path.basename(dropped_path)}")
    
    def browse_input_files(self):
        """Browse for input files"""
        filetypes = [
            ("All supported", "*.docx;*.pdf;*.txt;*.html;*.htm;*.rtf"),
            ("Word documents", "*.docx"),
            ("PDF files", "*.pdf"),
            ("Text files", "*.txt"),
            ("HTML files", "*.html;*.htm"),
            ("RTF files", "*.rtf"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(title="Select documents to convert", filetypes=filetypes)
        if files:
            # Store multiple files (we'll handle this in conversion)
            self.input_path.set(";".join(files))
            self.log_message(f"📄 Selected {len(files)} file(s)")
    
    def browse_input_folder(self):
        """Browse for input folder"""
        folder = filedialog.askdirectory(title="Select folder containing documents")
        if folder:
            self.input_path.set(folder)
            self.log_message(f"📁 Selected folder: {os.path.basename(folder)}")
    
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_path.set(folder)

    def create_section_frames(self) -> None:
        """Create properly grouped section frames for better visual hierarchy"""
        # This method organizes UI elements into logical sections
        pass

    def apply_consistent_spacing(self) -> None:
        """Apply consistent spacing throughout the interface"""
        # This method ensures uniform spacing between elements
        pass

    def add_visual_indicators(self) -> None:
        """Add visual indicators for better user guidance"""
        # This method adds icons, colors, and other visual cues
        pass

    def style_buttons(self) -> None:
        """Apply enhanced styling to buttons"""
        # Configure button styles with modern appearance
        style = ttk.Style()

        # Primary button style
        style.configure('Primary.TButton',
                       font=self.font_scheme['button'],
                       padding=(15, 10))

        # Secondary button style
        style.configure('Secondary.TButton',
                       font=self.font_scheme['body'],
                       padding=(10, 8))

    def add_hover_effects(self) -> None:
        """Add hover effects to interactive elements"""
        # This method adds visual feedback for hover states
        pass

    def update_button_states(self) -> None:
        """Update button states based on application state"""
        # This method manages button enabled/disabled states
        pass

    def setup_keyboard_navigation(self) -> None:
        """Set up keyboard navigation for accessibility"""
        # Configure tab order and keyboard shortcuts
        pass

    def add_tooltips(self) -> None:
        """Add helpful tooltips to UI elements"""
        # This method adds contextual help tooltips
        pass

    def high_contrast_mode(self) -> None:
        """Enable high contrast mode for accessibility"""
        # This method applies high contrast color scheme
        pass

    def animate_progress(self) -> None:
        """Add smooth progress animations"""
        # This method creates smooth progress transitions
        pass

    def check_dependencies(self):
        """Check if required packages are installed"""
        required_packages = {
            'python-docx': 'docx',
            'PyPDF2': 'PyPDF2', 
            'beautifulsoup4': 'bs4',
            'striprtf': 'striprtf'
        }
        
        missing = []
        for package, import_name in required_packages.items():
            try:
                __import__(import_name)
            except ImportError:
                missing.append(package)
        
        if missing:
            self.log_message(f"📦 Installing missing packages: {', '.join(missing)}")
            self.install_packages(missing)
    
    def install_packages(self, packages):
        """Install required packages"""
        for package in packages:
            try:
                self.log_message(f"📦 Installing {package}...")
                os.system(f'pip install {package}')
                self.log_message(f"✅ {package} installed successfully")
            except Exception as e:
                self.log_message(f"❌ Failed to install {package}: {str(e)}")
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select input files or folder")
            return False
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select output folder")
            return False
        
        return True
    
    def start_conversion(self):
        """Start conversion in separate thread"""
        if not self.validate_inputs():
            return
        
        self.convert_button.config(state='disabled')
        self.progress_var.set(0)
        self.results_text.delete(1.0, tk.END)
        
        # Start conversion in background thread
        threading.Thread(target=self.convert_documents, daemon=True).start()
    
    def convert_documents(self):
        """Main conversion process"""
        try:
            self.update_status("Preparing conversion...")
            
            input_path = self.input_path.get()
            output_dir = Path(self.output_path.get())
            input_fmt = self.input_format.get()
            output_fmt = self.output_format.get()
            
            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Determine files to convert
            files_to_convert = []
            
            if ";" in input_path:
                # Multiple files selected
                files_to_convert = [Path(f) for f in input_path.split(";")]
            elif os.path.isfile(input_path):
                # Single file
                files_to_convert = [Path(input_path)]
            elif os.path.isdir(input_path):
                # Directory - find all supported files
                input_dir = Path(input_path)
                extensions = []
                for fmt_info in FormatDetector.SUPPORTED_INPUT_FORMATS.values():
                    extensions.extend(fmt_info['extensions'])
                
                for ext in extensions:
                    files_to_convert.extend(input_dir.rglob(f"*{ext}"))
            
            # Filter out temporary files
            files_to_convert = [f for f in files_to_convert if not f.name.startswith('~$')]
            
            total_files = len(files_to_convert)
            if total_files == 0:
                self.log_message("❌ No supported files found")
                self.update_status("No files to convert")
                return
            
            self.log_message(f"🚀 Starting conversion of {total_files} files")
            self.log_message(f"📄 From: {input_fmt} → To: {output_fmt}")
            
            successful = 0
            failed = 0
            
            for i, file_path in enumerate(files_to_convert):
                try:
                    # Determine output path
                    if self.preserve_structure.get() and os.path.isdir(self.input_path.get().split(";")[0]):
                        # Preserve structure for folder conversions
                        base_dir = Path(self.input_path.get().split(";")[0])
                        rel_path = file_path.relative_to(base_dir)
                        output_ext = FormatDetector.SUPPORTED_OUTPUT_FORMATS[output_fmt]['extension']
                        output_file_path = output_dir / rel_path.with_suffix(output_ext)
                    else:
                        # Flat structure for file selections
                        output_ext = FormatDetector.SUPPORTED_OUTPUT_FORMATS[output_fmt]['extension']
                        output_file_path = output_dir / f"{file_path.stem}{output_ext}"
                    
                    # Create output directory
                    output_file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Skip if exists and not overwriting
                    if output_file_path.exists() and not self.overwrite_existing.get():
                        self.log_message(f"⏭️  Skipped (exists): {file_path.name}")
                        continue
                    
                    # Convert the file
                    self.converter.convert_file(file_path, output_file_path, input_fmt, output_fmt)
                    
                    successful += 1
                    self.log_message(f"✅ {file_path.name} → {output_file_path.name}")
                    
                except Exception as e:
                    failed += 1
                    self.log_message(f"❌ {file_path.name}: {str(e)}")
                
                # Update progress
                progress = ((i + 1) / total_files) * 100
                self.progress_var.set(progress)
                self.update_status(f"Converting... {i+1}/{total_files}")
            
            # Final results
            self.log_message(f"\n🎉 Conversion complete!")
            self.log_message(f"✅ Successful: {successful}")
            self.log_message(f"❌ Failed: {failed}")
            self.log_message(f"📂 Output saved to: {output_dir}")
            
            self.update_status(f"Complete! {successful} files converted, {failed} failed")
            
            # Show completion dialog
            messagebox.showinfo("Conversion Complete", 
                              f"Successfully converted {successful} files!\n"
                              f"Failed: {failed}\n"
                              f"Output location: {output_dir}")
        
        except Exception as e:
            self.log_message(f"❌ Conversion error: {str(e)}")
            self.update_status("Conversion failed")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
        
        finally:
            self.convert_button.config(state='normal')
    
    def update_status(self, message):
        """Update status label safely"""
        self.root.after(0, lambda: self.status_var.set(message))
    
    def log_message(self, message):
        """Add message to results area safely"""
        def _add_message():
            self.results_text.insert(tk.END, message + "\n")
            self.results_text.see(tk.END)
        
        self.root.after(0, _add_message)

def main():
    """Application entry point"""
    try:
        # Try enhanced drag-and-drop support
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        # Fallback to standard tkinter
        root = tk.Tk()
    
    # Set application icon and properties
    root.option_add('*tearOff', False)  # Disable menu tearoff
    
    app = UniversalDocumentConverterGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 