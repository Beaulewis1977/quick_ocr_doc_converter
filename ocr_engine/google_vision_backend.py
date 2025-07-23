#!/usr/bin/env python3
"""
Google Vision API Backend for OCR Engine
Provides Google Cloud Vision API integration for OCR functionality
"""

import os
import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import tempfile

try:
    from google.cloud import vision
    from google.oauth2 import service_account
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False

from .error_handler import OCRError, OCRErrorType


class GoogleVisionBackend:
    """Google Vision API backend for OCR processing"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None):
        """
        Initialize Google Vision backend
        
        Args:
            config: Configuration dictionary with API credentials
            logger: Optional logger instance
        """
        self.config = config or {}
        self.logger = logger or logging.getLogger("GoogleVisionBackend")
        self.client = None
        self.available = False
        
        # Initialize client if credentials are available
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Vision API client"""
        if not GOOGLE_VISION_AVAILABLE:
            self.logger.warning("Google Cloud Vision library not installed")
            return
        
        try:
            # Try multiple credential sources
            credentials = self._get_credentials()
            if credentials:
                self.client = vision.ImageAnnotatorClient(credentials=credentials)
                self.available = True
                self.logger.info("Google Vision API client initialized successfully")
            else:
                self.logger.warning("Google Vision API credentials not found")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Vision client: {e}")
            self.available = False
    
    def _get_credentials(self):
        """Get Google Vision API credentials from multiple sources"""
        # 1. Try service account key from config
        if 'google_vision_key_file' in self.config:
            key_file = Path(self.config['google_vision_key_file'])
            if key_file.exists():
                try:
                    return service_account.Credentials.from_service_account_file(str(key_file))
                except Exception as e:
                    self.logger.error(f"Failed to load service account file {key_file}: {e}")
        
        # 2. Try service account JSON from config
        if 'google_vision_key_json' in self.config:
            try:
                key_info = json.loads(self.config['google_vision_key_json'])
                return service_account.Credentials.from_service_account_info(key_info)
            except Exception as e:
                self.logger.error(f"Failed to load service account JSON: {e}")
        
        # 3. Try environment variable for service account file
        if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
            try:
                return service_account.Credentials.from_service_account_file(
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS']
                )
            except Exception as e:
                self.logger.error(f"Failed to load credentials from GOOGLE_APPLICATION_CREDENTIALS: {e}")
        
        # 4. Try default credentials (for Google Cloud environments)
        try:
            from google.auth import default
            credentials, project = default()
            return credentials
        except Exception as e:
            self.logger.debug(f"Default credentials not available: {e}")
        
        return None
    
    def is_available(self) -> bool:
        """Check if Google Vision API is available"""
        return self.available and self.client is not None
    
    def extract_text(self, image_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract text from image using Google Vision API
        
        Args:
            image_path: Path to the image file
            options: OCR options (languages, etc.)
            
        Returns:
            Dictionary with extracted text and metadata
        """
        if not self.is_available():
            raise OCRError(
                "Google Vision API not available",
                OCRErrorType.API_ERROR,
                suggestion="Check API credentials and configuration"
            )
        
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                raise OCRError(
                    f"Image file not found: {image_path}",
                    OCRErrorType.IMAGE_NOT_FOUND
                )
            
            # Read image file
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            # Create Vision API image object
            image = vision.Image(content=content)
            
            # Configure text detection
            features = [vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION)]
            
            # Set language hints if provided
            image_context = None
            if options and 'languages' in options:
                # Convert language codes to Google Vision format
                language_hints = self._convert_language_codes(options['languages'])
                if language_hints:
                    image_context = vision.ImageContext(language_hints=language_hints)
            
            # Perform text detection
            if image_context:
                request = vision.AnnotateImageRequest(
                    image=image,
                    features=features,
                    image_context=image_context
                )
                response = self.client.annotate_image(request=request)
            else:
                response = self.client.text_detection(image=image)
            
            # Check for errors
            if response.error.message:
                raise OCRError(
                    f"Google Vision API error: {response.error.message}",
                    OCRErrorType.API_ERROR
                )
            
            # Extract text and confidence
            text_annotations = response.text_annotations
            if not text_annotations:
                return {
                    'text': '',
                    'confidence': 0,
                    'source': 'google_vision',
                    'word_count': 0,
                    'character_count': 0
                }
            
            # First annotation contains the full text
            full_text = text_annotations[0].description
            
            # Calculate average confidence from individual words
            confidences = []
            for annotation in text_annotations[1:]:  # Skip first one (full text)
                if hasattr(annotation, 'confidence'):
                    confidences.append(annotation.confidence * 100)
            
            avg_confidence = sum(confidences) / len(confidences) if confidences else None
            
            return {
                'text': full_text.strip() if full_text else '',
                'confidence': avg_confidence,
                'source': 'google_vision',
                'word_count': len(full_text.split()) if full_text else 0,
                'character_count': len(full_text) if full_text else 0,
                'raw_response': response  # For advanced use cases
            }
            
        except OCRError:
            raise
        except Exception as e:
            raise OCRError(
                f"Google Vision API processing failed: {e}",
                OCRErrorType.API_ERROR,
                original_error=e
            )
    
    def _convert_language_codes(self, languages: List[str]) -> List[str]:
        """
        Convert common language codes to Google Vision format
        
        Args:
            languages: List of language codes (tesseract format)
            
        Returns:
            List of Google Vision compatible language codes
        """
        # Mapping from common codes to Google Vision codes
        language_mapping = {
            'eng': 'en',
            'fra': 'fr',
            'deu': 'de',
            'spa': 'es',
            'ita': 'it',
            'por': 'pt',
            'rus': 'ru',
            'jpn': 'ja',
            'kor': 'ko',
            'chi_sim': 'zh-Hans',
            'chi_tra': 'zh-Hant',
            'ara': 'ar',
            'hin': 'hi',
            'ben': 'bn',
            'tha': 'th',
            'vie': 'vi',
        }
        
        converted = []
        for lang in languages:
            # Convert if mapping exists, otherwise use as-is
            converted_lang = language_mapping.get(lang, lang)
            if converted_lang not in converted:
                converted.append(converted_lang)
        
        return converted
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported languages
        
        Returns:
            List of supported language codes
        """
        # Google Vision supports many languages, here are the most common ones
        return [
            'en', 'fr', 'de', 'es', 'it', 'pt', 'ru', 'ja', 'ko', 
            'zh-Hans', 'zh-Hant', 'ar', 'hi', 'bn', 'th', 'vi',
            'nl', 'pl', 'tr', 'cs', 'da', 'sv', 'no', 'fi', 'hu'
        ]
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Google Vision API connection
        
        Returns:
            Dictionary with test results
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'Google Vision API not available',
                'details': 'Check credentials and configuration'
            }
        
        try:
            # Create a simple test image
            from PIL import Image, ImageDraw
            
            # Create a temporary test image
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                # Create simple test image with text
                img = Image.new('RGB', (200, 100), color='white')
                draw = ImageDraw.Draw(img)
                draw.text((10, 40), "TEST", fill='black')
                img.save(temp_file.name, 'PNG')
                temp_path = temp_file.name
            
            try:
                # Test OCR on the image
                result = self.extract_text(temp_path)
                success = 'TEST' in result.get('text', '').upper()
                
                return {
                    'success': success,
                    'text_detected': result.get('text', ''),
                    'confidence': result.get('confidence'),
                    'message': 'Connection test successful' if success else 'Connection test partial'
                }
                
            finally:
                # Clean up temp file
                Path(temp_path).unlink(missing_ok=True)
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'details': 'Failed to perform connection test'
            }
    
    def get_usage_info(self) -> Dict[str, Any]:
        """
        Get API usage information (if available)
        
        Returns:
            Dictionary with usage information
        """
        return {
            'backend': 'google_vision',
            'available': self.is_available(),
            'features': [
                'Text detection',
                'Multi-language support',
                'High accuracy',
                'Cloud-based processing'
            ],
            'pricing_info': 'Usage-based pricing - see Google Cloud Vision pricing',
            'rate_limits': 'Varies by quota configuration'
        }