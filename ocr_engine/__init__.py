"""
OCR Engine Package for Quick Document Convertor

This package provides comprehensive OCR (Optical Character Recognition) functionality
for converting images to text with support for multiple OCR backends and formats.

Author: Beau Lewis (blewisxx@gmail.com)
Version: 3.1.0
"""

from .ocr_engine import OCREngine
from .image_processor import ImageProcessor
from .format_detector import OCRFormatDetector
from .ocr_integration import OCRIntegration

__all__ = ['OCREngine', 'ImageProcessor', 'OCRFormatDetector', 'OCRIntegration']

# Version information
__version__ = '3.1.0'
__author__ = 'Beau Lewis'
__email__ = 'blewisxx@gmail.com'
