#!/usr/bin/env python3
"""
Simple Document Converter CLI - VB6/VFP9 Compatible
Basic document conversion without OCR for 32-bit DLL integration
Designed and built by Beau Lewis (blewisxx@gmail.com)
"""

import argparse
import sys
import os
from pathlib import Path
import logging
from typing import List, Optional, Dict
import json
import time
import threading

# Import basic conversion functions
try:
    from docx import Document
    import fitz  # PyMuPDF
    from bs4 import BeautifulSoup
    import markdown
    HAS_CONVERTERS = True
except ImportError:
    HAS_CONVERTERS = False

class SimpleDocumentConverter:
    """Simple CLI for basic document conversion without OCR"""
    
    def __init__(self):
        self.setup_logging()
        self._conversion_lock = threading.Lock()
        
        # Supported formats for basic conversion
        self.supported_formats = {
            'input': ['.pdf', '.docx', '.txt', '.html', '.md', '.rtf'],
            'output': ['.txt', '.md', '.html', '.json']
        }
    
    def setup_logging(self):
        """Setup basic logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_parser(self):
        """Create argument parser for simple CLI"""
        parser = argparse.ArgumentParser(
            description="Simple Document Converter - Basic conversion for VB6/VFP9 integration",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s document.pdf output.txt     # Convert PDF to text
  %(prog)s document.docx output.md     # Convert DOCX to markdown
  %(prog)s input_dir/ output_dir/      # Convert directory
  %(prog)s --formats                   # Show supported formats
            """
        )
        
        # Basic arguments
        parser.add_argument('input', nargs='?', 
                          help='Input file or directory to convert')
        parser.add_argument('output', nargs='?',
                          help='Output file or directory')
        
        # Format options (DLL-compatible)
        parser.add_argument('--format', '-f', '-t',
                          choices=['txt', 'md', 'html', 'json'],
                          default='txt',
                          help='Output format (default: txt)')
        parser.add_argument('-o', '--output-file',
                          help='Output file (alternative to positional argument)')
        parser.add_argument('--formats', action='store_true',
                          help='Show supported input/output formats')
        
        # Processing options
        parser.add_argument('--recursive', '-r', action='store_true',
                          help='Process directories recursively')
        parser.add_argument('--overwrite', action='store_true',
                          help='Overwrite existing files')
        
        # VB6/VFP9 compatibility options
        parser.add_argument('--encoding', default='utf-8',
                          help='Text encoding (default: utf-8)')
        parser.add_argument('--line-endings', choices=['windows', 'unix', 'mac'],
                          default='windows',
                          help='Line ending style (default: windows)')
        
        # System info
        parser.add_argument('--version', action='version', 
                          version='Simple Document Converter 1.0.0')
        parser.add_argument('--verbose', '-v', action='store_true',
                          help='Enable verbose logging')
        parser.add_argument('--quiet', '-q', action='store_true',
                          help='Suppress output except errors')
        
        return parser
    
    def show_supported_formats(self):
        """Display supported file formats"""
        print("Supported Input Formats:")
        for fmt in self.supported_formats['input']:
            print(f"  {fmt}")
        
        print("\nSupported Output Formats:")
        for fmt in self.supported_formats['output']:
            print(f"  {fmt}")
        
        return True
    
    def convert_pdf_to_text(self, pdf_path: str) -> str:
        """Convert PDF to plain text without OCR"""
        try:
            if not HAS_CONVERTERS:
                raise ImportError("PDF conversion libraries not available")
            
            with fitz.open(pdf_path) as doc:
                text = ""
                
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    text += page.get_text()
                    text += "\n\n"
                
                return text.strip()
            
        except Exception as e:
            self.logger.error(f"PDF conversion failed: {e}")
            return f"Error converting PDF: {e}"
    
    def convert_docx_to_text(self, docx_path: str) -> str:
        """Convert DOCX to plain text"""
        try:
            if not HAS_CONVERTERS:
                raise ImportError("DOCX conversion libraries not available")
            
            doc = Document(docx_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"DOCX conversion failed: {e}")
            return f"Error converting DOCX: {e}"
    
    def convert_html_to_text(self, html_path: str) -> str:
        """Convert HTML to plain text"""
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            if HAS_CONVERTERS:
                soup = BeautifulSoup(html_content, 'html.parser')
                return soup.get_text()
            else:
                # Basic HTML tag removal
                import re
                text = re.sub('<[^<]+?>', '', html_content)
                return text.strip()
                
        except Exception as e:
            self.logger.error(f"HTML conversion failed: {e}")
            return f"Error converting HTML: {e}"
    
    def convert_markdown_to_text(self, md_path: str) -> str:
        """Convert Markdown to plain text"""
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            if HAS_CONVERTERS:
                html = markdown.markdown(md_content)
                soup = BeautifulSoup(html, 'html.parser')
                return soup.get_text()
            else:
                # Basic markdown cleanup
                import re
                text = re.sub(r'[#*`_~\[\]()]+', '', md_content)
                return text.strip()
                
        except Exception as e:
            self.logger.error(f"Markdown conversion failed: {e}")
            return f"Error converting Markdown: {e}"
    
    def convert_to_format(self, text: str, output_format: str, source_file: str = "") -> str:
        """Convert text to specified output format"""
        if output_format == 'txt':
            return text
        
        elif output_format == 'md':
            title = Path(source_file).stem if source_file else "Document"
            return f"# {title}\n\n{text}"
        
        elif output_format == 'html':
            title = Path(source_file).stem if source_file else "Document"
            html_text = text.replace('\n', '<br>\n')
            return f"<!DOCTYPE html>\n<html>\n<head>\n<title>{title}</title>\n</head>\n<body>\n<h1>{title}</h1>\n<p>{html_text}</p>\n</body>\n</html>"
        
        elif output_format == 'json':
            return json.dumps({
                'source': source_file,
                'content': text,
                'timestamp': time.time()
            }, indent=2)
        
        return text
    
    def apply_line_endings(self, text: str, line_ending_style: str) -> str:
        """Apply appropriate line endings for compatibility"""
        # Normalize to \n first
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        if line_ending_style == 'windows':
            return text.replace('\n', '\r\n')
        elif line_ending_style == 'mac':
            return text.replace('\n', '\r')
        else:  # unix
            return text
    
    def convert_single_file(self, input_path: str, output_path: str, 
                           output_format: str = 'txt', encoding: str = 'utf-8',
                           line_endings: str = 'windows') -> bool:
        """Convert a single file"""
        try:
            with self._conversion_lock:
                input_path = Path(input_path)
                output_path = Path(output_path)
                
                if not input_path.exists():
                    self.logger.error(f"Input file not found: {input_path}")
                    return False
                
                # Create output directory
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Get file extension
                file_ext = input_path.suffix.lower()
                
                # Convert based on input type
                if file_ext == '.pdf':
                    text = self.convert_pdf_to_text(str(input_path))
                elif file_ext == '.docx':
                    text = self.convert_docx_to_text(str(input_path))
                elif file_ext == '.html':
                    text = self.convert_html_to_text(str(input_path))
                elif file_ext == '.md':
                    text = self.convert_markdown_to_text(str(input_path))
                elif file_ext in ['.txt', '.rtf']:
                    with open(input_path, 'r', encoding=encoding) as f:
                        text = f.read()
                else:
                    self.logger.error(f"Unsupported file format: {file_ext}")
                    return False
                
                # Convert to output format
                converted_text = self.convert_to_format(text, output_format, str(input_path))
                
                # Apply line endings
                converted_text = self.apply_line_endings(converted_text, line_endings)
                
                # Write output
                with open(output_path, 'w', encoding=encoding) as f:
                    f.write(converted_text)
                
                self.logger.info(f"Converted: {input_path.name} -> {output_path.name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Conversion failed for {input_path}: {e}")
            return False
    
    def collect_files(self, input_path: str, recursive: bool = False) -> List[Path]:
        """Collect files to process"""
        path_obj = Path(input_path)
        files = []
        
        if path_obj.is_file():
            files.append(path_obj)
        elif path_obj.is_dir():
            pattern = "**/*" if recursive else "*"
            for ext in self.supported_formats['input']:
                files.extend(path_obj.glob(f"{pattern}{ext}"))
        
        return files
    
    def run_conversion(self, args) -> int:
        """Run the conversion process"""
        if not args.input:
            print("Error: No input specified")
            return 1
        
        # Handle output argument (support both positional and -o)
        output = args.output or getattr(args, 'output_file', None)
        if not output:
            print("Error: No output specified")
            return 1
        
        input_path = Path(args.input)
        output_path = Path(output)
        
        if input_path.is_file():
            # Single file conversion
            success = self.convert_single_file(
                str(input_path), str(output_path),
                args.format, args.encoding, args.line_endings
            )
            return 0 if success else 1
        
        elif input_path.is_dir():
            # Directory conversion
            files = self.collect_files(str(input_path), args.recursive)
            
            if not files:
                print("Error: No supported files found")
                return 1
            
            # Ensure output is directory
            output_path.mkdir(parents=True, exist_ok=True)
            
            successful = 0
            failed = 0
            
            print(f"Processing {len(files)} files...")
            
            for file in files:
                output_file = output_path / f"{file.stem}.{args.format}"
                
                if output_file.exists() and not args.overwrite:
                    print(f"Skipping (exists): {file.name}")
                    continue
                
                success = self.convert_single_file(
                    str(file), str(output_file),
                    args.format, args.encoding, args.line_endings
                )
                
                if success:
                    successful += 1
                    print(f"✓ {file.name}")
                else:
                    failed += 1
                    print(f"✗ {file.name}")
            
            print(f"\nCompleted: {successful} successful, {failed} failed")
            return 0 if failed == 0 else 1
        
        else:
            print(f"Error: Input path not found: {input_path}")
            return 1
    
    def run(self, args=None) -> int:
        """Main CLI execution"""
        parser = self.create_parser()
        args = parser.parse_args(args)
        
        # Set logging level
        if args.quiet:
            logging.getLogger().setLevel(logging.ERROR)
        elif args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Handle format listing
        if args.formats:
            self.show_supported_formats()
            return 0
        
        # Run conversion
        return self.run_conversion(args)


def main():
    """Main entry point for simple CLI"""
    converter = SimpleDocumentConverter()
    sys.exit(converter.run())


if __name__ == "__main__":
    main()