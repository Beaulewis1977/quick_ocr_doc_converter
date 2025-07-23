import os
import sys
import logging
from pathlib import Path
import subprocess
from typing import Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import tesseract_config  # Auto-configure Tesseract
class OCREngine:
    """
    OCR Engine with Tesseract integration
    Handles both image and PDF OCR with configurable settings
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize OCR Engine
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.backend = None
        self.tesseract_path = None
        self._setup_tesseract()
        
    def _setup_tesseract(self) -> None:
        """Setup Tesseract with cross-platform support"""
        try:
            # Try to find Tesseract in common locations
            tesseract_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', '')),
                "/usr/bin/tesseract",
                "/usr/local/bin/tesseract",
                "/opt/homebrew/bin/tesseract"
            ]
            
            for path in tesseract_paths:
                path = os.path.expandvars(path)
                if os.path.isfile(path):
                    self.tesseract_path = path
                    self.backend = 'tesseract'
                    self.logger.info(f"Tesseract found at: {path}")
                    return
            
            # Try system PATH
            try:
                result = subprocess.run(['tesseract', '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.backend = 'tesseract'
                    self.tesseract_path = 'tesseract'
                    self.logger.info("Tesseract found in system PATH")
                    return
            except (FileNotFoundError, subprocess.CalledProcessError):
                pass
            
            self.logger.warning("Tesseract not found, OCR functionality will be limited")
            self.backend = None
            
        except Exception as e:
            self.logger.error(f"Error setting up Tesseract: {e}")
            self.backend = None
    
    def is_available(self) -> bool:
        """Check if OCR backend is available"""
        return self.backend is not None
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        if not self.is_available():
            return ['eng']
        
        try:
            # Get languages from Tesseract
            result = subprocess.run([self.tesseract_path, '--list-langs'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                # Skip header line
                languages = [lang.strip() for lang in lines[1:] if lang.strip()]
                return languages if languages else ['eng']
        except Exception as e:
            self.logger.error(f"Failed to get languages: {e}")
        
        return ['eng']
    
    def extract_text(self, image_path: str, language: str = 'eng') -> str:
        """
        Extract text from image using Tesseract CLI
        
        Args:
            image_path: Path to image file
            language: Language for OCR (default: eng)
            
        Returns:
            Extracted text string
        """
        if not self.is_available():
            self.logger.warning("No OCR backend available")
            return ""
        
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                self.logger.error(f"Image file not found: {image_path}")
                return ""
            
            # Create temporary output file
            temp_output = image_path.parent / f"{image_path.stem}_temp.txt"
            
            # Run Tesseract
            cmd = [self.tesseract_path, str(image_path), str(temp_output.with_suffix('')), 
                   '-l', language, '--psm', '6']
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Read the output
                output_file = temp_output.with_suffix('.txt')
                if output_file.exists():
                    with open(output_file, 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                    
                    # Clean up
                    output_file.unlink(missing_ok=True)
                    return text
            else:
                self.logger.error(f"Tesseract error: {result.stderr}")
                
        except Exception as e:
            self.logger.error(f"OCR extraction failed: {e}")
        
        return ""

    def extract_text_from_pdf(self, pdf_path: str, language: str = 'eng') -> str:
        """
        Extract text from PDF using OCR
        
        Args:
            pdf_path: Path to PDF file
            language: Language for OCR (default: eng)
            
        Returns:
            Extracted text string
        """
        if not self.is_available():
            self.logger.warning("No OCR backend available")
            return ""
        
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                self.logger.error(f"PDF file not found: {pdf_path}")
                return ""
            
            # Try to extract text with PyMuPDF first (faster)
            try:
                import fitz  # PyMuPDF
                with fitz.open(str(pdf_path)) as doc:
                    text = ""
                    
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        page_text = page.get_text()
                        
                        # If page has no text or very little text, use OCR
                        if not page_text.strip() or len(page_text.strip()) < 50:
                            # Convert page to image and OCR
                            pix = page.get_pixmap()
                            img_data = pix.tobytes("png")
                            
                            # Save temporary image
                            temp_image = pdf_path.parent / f"temp_page_{page_num}.png"
                            with open(temp_image, 'wb') as f:
                                f.write(img_data)
                            
                            # OCR the image
                            ocr_text = self.extract_text(temp_image, language)
                            text += f"\n--- Page {page_num + 1} ---\n{ocr_text}\n"
                            
                            # Clean up
                            temp_image.unlink(missing_ok=True)
                        else:
                            text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    
                    return text.strip()
                
            except ImportError:
                # Fallback: Convert PDF to images and OCR each page
                self.logger.info("PyMuPDF not available, using image conversion fallback")
                
                # Try with pdf2image
                try:
                    from pdf2image import convert_from_path
                    
                    # Convert PDF to images
                    images = convert_from_path(str(pdf_path))
                    text = ""
                    
                    for i, image in enumerate(images):
                        # Save temporary image
                        temp_image = pdf_path.parent / f"temp_page_{i}.png"
                        image.save(temp_image, 'PNG')
                        
                        # OCR the image
                        page_text = self.extract_text(temp_image, language)
                        text += f"\n--- Page {i + 1} ---\n{page_text}\n"
                        
                        # Clean up
                        temp_image.unlink(missing_ok=True)
                    
                    return text.strip()
                    
                except ImportError:
                    self.logger.error("Neither PyMuPDF nor pdf2image available for PDF processing")
                    return ""
                    
        except Exception as e:
            self.logger.error(f"PDF OCR extraction failed: {e}")
            return ""

# Test the OCR engine
if __name__ == "__main__":
    print("OCR Document Converter - System Check")
    print("=" * 50)
    
    # Initialize OCR
    ocr = OCREngine()
    
    # Test availability
    if ocr.is_available():
        print("✅ OCR Engine is ready!")
        print(f"   Tesseract path: {ocr.tesseract_path}")
        print(f"   Supported languages: {ocr.get_supported_languages()}")
    else:
        print("⚠️  OCR Engine setup incomplete")
        print("   Tesseract OCR is not installed or not found")
        print()
        print("📋 Installation instructions:")
        print("   Windows: winget install tesseract-ocr.tesseract-ocr")
        print("   macOS:   brew install tesseract")
        print("   Linux:   sudo apt-get install tesseract-ocr")
        print()
        print("🎯 After installation, restart your terminal and run this script again.")