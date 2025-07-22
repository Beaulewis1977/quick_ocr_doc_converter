#!/usr/bin/env python3
"""
Minimal OCR Engine - Fallback implementation
Provides basic OCR functionality without external dependencies
"""

import os
import logging
from pathlib import Path

class MinimalOCREngine:
    """Minimal OCR engine that provides basic functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.available = False
        self.engine_name = "Minimal"
        
    def extract_text(self, image_path):
        """Extract text from image - fallback implementation"""
        try:
            # Check if we can use a real OCR engine
            if self._try_tesseract():
                return self._extract_with_tesseract(image_path)
            elif self._try_easyocr():
                return self._extract_with_easyocr(image_path)
            else:
                return self._fallback_text_extraction(image_path)
                
        except Exception as e:
            self.logger.error(f"OCR extraction failed: {e}")
            return f"[OCR not available - {str(e)}]"
    
    def _try_tesseract(self):
        """Try to import and use Tesseract"""
        try:
            import pytesseract
            return True
        except ImportError:
            return False
    
    def _try_easyocr(self):
        """Try to import and use EasyOCR"""
        try:
            import easyocr
            return True
        except ImportError:
            return False
    
    def _extract_with_tesseract(self, image_path):
        """Extract text using Tesseract"""
        try:
            import pytesseract
            from PIL import Image
            
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
            
        except Exception as e:
            return f"[Tesseract error: {str(e)}]"
    
    def _extract_with_easyocr(self, image_path):
        """Extract text using EasyOCR"""
        try:
            import easyocr
            
            reader = easyocr.Reader(['en'])
            results = reader.readtext(image_path)
            text = ' '.join([result[1] for result in results])
            return text.strip()
            
        except Exception as e:
            return f"[EasyOCR error: {str(e)}]"
    
    def _fallback_text_extraction(self, image_path):
        """Fallback text extraction for demo purposes"""
        filename = Path(image_path).name
        return f"[OCR placeholder for {filename} - Install pytesseract for real OCR]"

class MinimalOCRIntegration:
    """Minimal OCR integration layer"""
    
    def __init__(self):
        self.engine = MinimalOCREngine()
        self.logger = logging.getLogger(__name__)
    
    def process_file(self, file_path, **kwargs):
        """Process a single file"""
        if not os.path.exists(file_path):
            return f"[File not found: {file_path}]"
        
        return self.engine.extract_text(file_path)
    
    def process_batch(self, file_paths, **kwargs):
        """Process multiple files"""
        results = []
        for file_path in file_paths:
            text = self.process_file(file_path)
            results.append(text)
        return results
    
    def get_config(self):
        """Return configuration"""
        return {
            "engine": "minimal",
            "available": self.engine.available,
            "dependencies": ["pytesseract", "PIL", "easyocr"]
        }

# Global instance for easy access
minimal_ocr = MinimalOCRIntegration()