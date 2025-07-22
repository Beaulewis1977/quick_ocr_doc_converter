"""
OCR Format Detector - Detects supported image formats for OCR
"""

from pathlib import Path
from typing import Set, List
import mimetypes

class OCRFormatDetector:
    """Detects and validates image formats for OCR processing"""
    
    # Supported image formats for OCR
    SUPPORTED_IMAGE_FORMATS = {
        '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp'
    }
    
    # MIME types for supported formats
    SUPPORTED_MIME_TYPES = {
        'image/jpeg',
        'image/png',
        'image/bmp',
        'image/tiff',
        'image/gif',
        'image/webp'
    }
    
    @classmethod
    def is_ocr_supported(cls, file_path: str) -> bool:
        """
        Check if a file format is supported for OCR
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if format is supported for OCR
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            # Check by extension
            extension = path.suffix.lower()
            if extension in cls.SUPPORTED_IMAGE_FORMATS:
                return True
            
            # Check by MIME type
            mime_type, _ = mimetypes.guess_type(str(path))
            if mime_type in cls.SUPPORTED_MIME_TYPES:
                return True
            
            return False
            
        except Exception:
            return False
    
    @classmethod
    def get_supported_extensions(cls) -> Set[str]:
        """Get all supported file extensions"""
        return cls.SUPPORTED_IMAGE_FORMATS.copy()
    
    @classmethod
    def get_supported_formats(cls) -> List[dict]:
        """Get detailed information about supported formats"""
        return [
            {
                'extension': '.jpg',
                'name': 'JPEG Image',
                'mime_type': 'image/jpeg',
                'description': 'Joint Photographic Experts Group format'
            },
            {
                'extension': '.jpeg',
                'name': 'JPEG Image',
                'mime_type': 'image/jpeg',
                'description': 'Joint Photographic Experts Group format'
            },
            {
                'extension': '.png',
                'name': 'PNG Image',
                'mime_type': 'image/png',
                'description': 'Portable Network Graphics format'
            },
            {
                'extension': '.bmp',
                'name': 'BMP Image',
                'mime_type': 'image/bmp',
                'description': 'Bitmap image format'
            },
            {
                'extension': '.tiff',
                'name': 'TIFF Image',
                'mime_type': 'image/tiff',
                'description': 'Tagged Image File Format'
            },
            {
                'extension': '.tif',
                'name': 'TIFF Image',
                'mime_type': 'image/tiff',
                'description': 'Tagged Image File Format'
            },
            {
                'extension': '.gif',
                'name': 'GIF Image',
                'mime_type': 'image/gif',
                'description': 'Graphics Interchange Format'
            },
            {
                'extension': '.webp',
                'name': 'WebP Image',
                'mime_type': 'image/webp',
                'description': 'WebP image format'
            }
        ]
    
    @classmethod
    def filter_supported_files(cls, file_paths: List[str]) -> List[str]:
        """
        Filter a list of files to only include OCR-supported formats
        
        Args:
            file_paths: List of file paths
            
        Returns:
            List of supported file paths
        """
        return [path for path in file_paths if cls.is_ocr_supported(path)]
