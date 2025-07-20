"""
Abstract base class for OCR backends

Provides a common interface for all OCR backend implementations
including local (Tesseract, EasyOCR) and cloud-based services.

Author: Terry AI Agent for Terragon Labs
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path

class OCRBackend(ABC):
    """
    Abstract base class for all OCR backends
    
    This class defines the common interface that all OCR backends
    must implement, ensuring consistent behavior across different
    OCR services and engines.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the OCR backend
        
        Args:
            config: Backend-specific configuration
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        
    @abstractmethod
    def extract_text(self, image_path: str, language: str = 'en') -> Dict[str, Any]:
        """
        Extract text from an image
        
        Args:
            image_path: Path to the image file
            language: Language code for OCR (e.g., 'en', 'es', 'fr')
            
        Returns:
            Dictionary containing:
                - text: Extracted text
                - confidence: Confidence score (0-100)
                - backend: Name of the backend used
                - language: Language used for OCR
                - success: Boolean indicating success
                - error: Error message if success is False
                - metadata: Additional backend-specific metadata
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the backend is available and properly configured
        
        Returns:
            True if backend is available, False otherwise
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported language codes
        
        Returns:
            List of supported language codes
        """
        pass
    
    def get_backend_info(self) -> Dict[str, Any]:
        """
        Get information about the backend
        
        Returns:
            Dictionary with backend information
        """
        return {
            'name': self.name,
            'available': self.is_available(),
            'supported_languages': self.get_supported_languages(),
            'config': self.config
        }
    
    def validate_language(self, language: str) -> bool:
        """
        Check if a language is supported by this backend
        
        Args:
            language: Language code to check
            
        Returns:
            True if language is supported
        """
        return language in self.get_supported_languages()
    
    def get_cost_estimate(self, image_path: str) -> Optional[float]:
        """
        Estimate the cost for processing an image (for cloud backends)
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Estimated cost in USD, or None for free backends
        """
        return None  # Default implementation for free backends
    
    def preprocess_image(self, image_path: str) -> str:
        """
        Preprocess image if needed by the backend
        
        Args:
            image_path: Path to the original image
            
        Returns:
            Path to the processed image (may be the same as input)
        """
        return image_path  # Default: no preprocessing
    
    def cleanup(self):
        """
        Cleanup resources used by the backend
        """
        pass  # Default: no cleanup needed

class LocalOCRBackend(OCRBackend):
    """
    Base class for local OCR backends (Tesseract, EasyOCR, etc.)
    """
    
    def get_cost_estimate(self, image_path: str) -> Optional[float]:
        """Local backends are free"""
        return 0.0

class CloudOCRBackend(OCRBackend):
    """
    Base class for cloud-based OCR backends
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.request_count = 0
        self.total_cost = 0.0
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the cloud service
        
        Returns:
            True if authentication successful
        """
        pass
    
    def track_usage(self, cost: float):
        """
        Track usage and cost for the backend
        
        Args:
            cost: Cost of the operation
        """
        self.request_count += 1
        self.total_cost += cost
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics for the backend
        
        Returns:
            Dictionary with usage statistics
        """
        return {
            'request_count': self.request_count,
            'total_cost': self.total_cost,
            'average_cost_per_request': self.total_cost / max(1, self.request_count)
        }