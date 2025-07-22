import os
import sys
import logging
from pathlib import Path
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCREngine:
    """
    OCR Engine with Tesseract integration
    Handles both image and PDF OCR with configurable settings
    """
    
    def __init__(self, logger=None):
        """
        Initialize OCR Engine
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.backend = None
        self.config = {}
        self._setup_tesseract()
        
    def _setup_tesseract(self):
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
            
            tesseract_path = None
            for path in tesseract_paths:
                path = os.path.expandvars(path)
                if os.path.isfile(path):
                    tesseract_path = path
                    break
            
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
                self.backend = 'tesseract'
                self.logger.info(f"Tesseract found at: {tesseract_path}")
            else:
                self.logger.warning("Tesseract not found, OCR functionality will be limited")
                self.backend = None
                
        except Exception as e:
            self.logger.error(f"Error setting up Tesseract: {e}")
            self.backend = None
    
    def extract_text(self, image_path, language='eng'):
        """
        Extract text from image using OCR
        
        Args:
            image_path: Path to image file
            language: Language for OCR (default: eng)
            
        Returns:
            Extracted text string
        """
        if not self.backend:
            self.logger.warning("No OCR backend available")
            return ""
        
        try:
            # Open image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text
            text = pytesseract.image_to_string(image, lang=language)
            
            self.logger.info(f"OCR completed for: {image_path}")
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"OCR extraction failed: {e}")
            return ""
    
    def is_available(self):
        """Check if OCR backend is available"""
        return self.backend is not None
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        if not self.backend:
            return ['eng']
        
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception as e:
            self.logger.error(f"Failed to get languages: {e}")
            return ['eng']  # Default

# Test the OCR engine
if __name__ == "__main__":
    # Initialize OCR
    ocr = OCREngine()
    
    # Test availability
    if ocr.is_available():
        print("✅ OCR Engine is ready!")
        print(f"Supported languages: {ocr.get_supported_languages()}")
    else:
        print("⚠️  OCR Engine setup incomplete - Tesseract not found")
        print("Please install Tesseract OCR for full functionality")
        print("\nInstallation instructions:")
        print("  Windows: winget install tesseract-ocr.tesseract-ocr")
        print("  macOS: brew install tesseract")
        print("  Linux: sudo apt-get install tesseract-ocr")