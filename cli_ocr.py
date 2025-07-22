#!/usr/bin/env python3
"""
Enhanced CLI for OCR Document Converter
Integrates OCR functionality with document conversion
"""

import argparse
import sys
import os
from pathlib import Path
import logging
from typing import List, Optional
import json
import time

# Import OCR functionality
try:
    from ocr_engine import OCREngine
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    OCREngine = None

# Import converter
# Import converter functions
try:
    from convert_to_markdown import convert_pdf_to_markdown
    from convert_recursive import convert_directory
except ImportError:
    # Fallback if modules not available
    def convert_pdf_to_markdown(input_path, output_path):
        """Fallback PDF conversion"""
        with open(output_path, 'w') as f:
            f.write("# PDF Conversion\n\nPDF conversion module not available.")
    
    def convert_directory(input_dir, output_dir, recursive=False):
        """Fallback directory conversion"""
        return 0

class OCRCLI:
    """Enhanced CLI with OCR capabilities"""
    
    def __init__(self):
        self.ocr = OCREngine() if HAS_OCR and OCREngine else None
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_parser(self):
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            description="OCR Document Converter - Convert documents with OCR support",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s file.pdf -o output.md                    # Convert PDF with OCR
  %(prog)s *.png -o output.md --ocr                 # Convert images with OCR
  %(prog)s input_dir/ -o output/ --recursive --ocr  # Batch convert with OCR
  %(prog)s --setup                                  # Run system setup
  %(prog)s --check-ocr                              # Check OCR availability
            """
        )
        
        # Basic arguments
        parser.add_argument('input', nargs='*', 
                          help='Input file(s) or directory to convert')
        parser.add_argument('-o', '--output', 
                          help='Output file or directory')
        
        # OCR options
        parser.add_argument('--ocr', action='store_true',
                          help='Enable OCR for images and PDFs')
        parser.add_argument('--ocr-lang', default='eng',
                          help='OCR language (default: eng)')
        parser.add_argument('--check-ocr', action='store_true',
                          help='Check OCR availability and exit')
        
        # Processing options
        parser.add_argument('--recursive', '-r', action='store_true',
                          help='Process directories recursively')
        parser.add_argument('--overwrite', action='store_true',
                          help='Overwrite existing files')
        parser.add_argument('--workers', type=int, default=1,
                          help='Number of worker processes')
        
        # Setup and verification
        parser.add_argument('--setup', action='store_true',
                          help='Run system setup (install dependencies)')
        parser.add_argument('--version', action='version', version='OCR Document Converter 3.1.0')
        
        # Logging
        parser.add_argument('--verbose', '-v', action='store_true',
                          help='Enable verbose logging')
        parser.add_argument('--quiet', '-q', action='store_true',
                          help='Suppress output except errors')
        
        return parser
    
    def check_ocr_status(self):
        """Check OCR availability"""
        if not self.ocr:
            print("❌ OCR Engine not available")
            print("   Tesseract OCR is not installed or not found")
            return False
        
        if self.ocr.is_available():
            print("✅ OCR Engine is ready")
            langs = self.ocr.get_supported_languages()
            print(f"   Supported languages: {', '.join(langs)}")
            return True
        else:
            print("❌ OCR Engine not ready")
            print("   Tesseract OCR is not installed or not accessible")
            return False
    
    def run_setup(self):
        """Run system setup"""
        try:
            from setup_ocr import OCRSetup
            setup = OCRSetup()
            setup.print_instructions()
            return setup.run_setup()
        except ImportError:
            print("Setup module not found. Manual installation required:")
            print("1. Install Tesseract OCR:")
            print("   - Windows: winget install tesseract-ocr.tesseract-ocr")
            print("   - macOS: brew install tesseract")
            print("   - Linux: sudo apt-get install tesseract-ocr")
            print("2. Install Python packages: pip install -r requirements_updated.txt")
            return False
    
    def convert_file_with_ocr(self, input_path: str, output_path: str, 
                            ocr_enabled: bool = False, ocr_lang: str = 'eng') -> bool:
        """Convert single file with optional OCR"""
        try:
            input_path = Path(input_path)
            output_path = Path(output_path)
            
            if not input_path.exists():
                self.logger.error(f"Input file not found: {input_path}")
                return False
            
            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Check file type
            file_ext = input_path.suffix.lower()
            
            # Handle image files with OCR
            if ocr_enabled and file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']:
                if not self.ocr or not self.ocr.is_available():
                    self.logger.error("OCR requested but not available")
                    return False
                
                self.logger.info(f"Processing image with OCR: {input_path}")
                text = self.ocr.extract_text(str(input_path), ocr_lang)
                
                # Save as markdown
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {input_path.stem}\n\n")
                    f.write(text)
                
                return True
            
            # Handle PDF files with OCR
            elif ocr_enabled and file_ext == '.pdf':
                if not self.ocr or not self.ocr.is_available():
                    self.logger.error("OCR requested but not available")
                    return False
                
                self.logger.info(f"Processing PDF with OCR: {input_path}")
                text = self.ocr.extract_text_from_pdf(str(input_path), ocr_lang)
                
                # Save as markdown
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {input_path.stem}\n\n")
                    f.write(text)
                
                return True
            
            # Regular conversion without OCR
            else:
                self.logger.info(f"Converting without OCR: {input_path}")
                convert_to_markdown(str(input_path), str(output_path))
                return True
                
        except Exception as e:
            self.logger.error(f"Conversion failed: {e}")
            return False
    
    def collect_files(self, paths: List[str], recursive: bool = False) -> List[Path]:
        """Collect all files to process"""
        files = []
        supported_exts = ['.pdf', '.txt', '.docx', '.html', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']
        
        for path in paths:
            path_obj = Path(path)
            
            if path_obj.is_file():
                files.append(path_obj)
            elif path_obj.is_dir():
                if recursive:
                    for ext in supported_exts:
                        files.extend(path_obj.rglob(f"*{ext}"))
                else:
                    for ext in supported_exts:
                        files.extend(path_obj.glob(f"*{ext}"))
        
        return list(set(files))  # Remove duplicates
    
    def run_conversion(self, args):
        """Run conversion based on arguments"""
        if not args.input:
            print("Error: No input files specified")
            return 1
        
        # Collect files
        files = self.collect_files(args.input, args.recursive)
        
        if not files:
            print("Error: No supported files found")
            return 1
        
        # Determine output
        if len(files) == 1 and not Path(args.output).is_dir():
            # Single file output
            output_file = Path(args.output)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            success = self.convert_file_with_ocr(
                str(files[0]), str(output_file), 
                args.ocr, args.ocr_lang
            )
            
            if success:
                print(f"✅ Converted: {files[0].name} -> {output_file.name}")
                return 0
            else:
                print(f"❌ Failed: {files[0].name}")
                return 1
        
        else:
            # Batch processing
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            successful = 0
            failed = 0
            
            print(f"Processing {len(files)} files...")
            
            for i, file in enumerate(files, 1):
                output_file = output_dir / f"{file.stem}.md"
                
                if output_file.exists() and not args.overwrite:
                    print(f"⏭️  Skipping (exists): {file.name}")
                    continue
                
                print(f"[{i}/{len(files)}] Processing: {file.name}")
                
                success = self.convert_file_with_ocr(
                    str(file), str(output_file),
                    args.ocr, args.ocr_lang
                )
                
                if success:
                    successful += 1
                else:
                    failed += 1
            
            print(f"\n✅ Completed: {successful} successful, {failed} failed")
            return 0 if failed == 0 else 1
    
    def run(self, args=None):
        """Main CLI execution"""
        parser = self.create_parser()
        args = parser.parse_args(args)
        
        # Handle setup
        if args.setup:
            return 0 if self.run_setup() else 1
        
        # Handle OCR check
        if args.check_ocr:
            return 0 if self.check_ocr_status() else 1
        
        # Handle conversion
        return self.run_conversion(args)

def main():
    """Main entry point for CLI"""
    cli = OCRCLI()
    sys.exit(cli.run())

if __name__ == "__main__":
    main()