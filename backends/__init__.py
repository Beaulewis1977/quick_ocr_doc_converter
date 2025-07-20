"""
OCR Backends Module

Provides a unified interface for multiple OCR backends including
local engines (Tesseract, EasyOCR) and cloud services (Google Vision,
AWS Textract, Azure Cognitive Services).
"""

from .base import OCRBackend, LocalOCRBackend, CloudOCRBackend
from .google_vision import GoogleVisionBackend
from .aws_textract import AWSTextractBackend
from .azure_vision import AzureVisionBackend
from .manager import OCRBackendManager, BackendSelectionError

__all__ = [
    'OCRBackend', 'LocalOCRBackend', 'CloudOCRBackend',
    'GoogleVisionBackend', 'AWSTextractBackend', 'AzureVisionBackend',
    'OCRBackendManager', 'BackendSelectionError'
]