"""
Image Processor for OCR - Handles image preprocessing and optimization
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance
from pathlib import Path
from typing import Optional, Dict, Any
import logging

class ImageProcessor:
    """Handles image preprocessing for optimal OCR results"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def preprocess_image(self, image_path: str, options: Dict[str, Any] = None) -> np.ndarray:
        """
        Preprocess image for optimal OCR results
        
        Args:
            image_path: Path to the image file
            options: Preprocessing options
            
        Returns:
            Preprocessed image as numpy array
        """
        options = options or {}
        
        try:
            # Load image
            image = self.load_image(image_path)
            
            # Apply preprocessing steps
            image = self.resize_image(image, options.get('max_dimension', 2048))
            image = self.enhance_contrast(image, options.get('contrast_factor', 1.5))
            image = self.denoise_image(image, options.get('denoise', True))
            
            # Convert to grayscale for OCR
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            image = self.apply_threshold(image, options.get('threshold_method', 'adaptive'))
            
            return image
            
        except Exception as e:
            self.logger.error(f"Error preprocessing image {image_path}: {str(e)}")
            raise
    
    def load_image(self, image_path: str) -> np.ndarray:
        """Load image using OpenCV"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        return image
    
    def resize_image(self, image: np.ndarray, max_dimension: int = 2048) -> np.ndarray:
        """Resize image while maintaining aspect ratio"""
        height, width = image.shape[:2]
        
        if max(height, width) > max_dimension:
            scale = max_dimension / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return image
    
    def enhance_contrast(self, image: np.ndarray, factor: float = 1.5) -> np.ndarray:
        """Enhance image contrast"""
        try:
            # Convert to PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                pil_image = Image.fromarray(image)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(pil_image)
            enhanced = enhancer.enhance(factor)
            
            # Convert back to numpy array
            if len(image.shape) == 3:
                return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)
            else:
                return np.array(enhanced)
                
        except Exception as e:
            self.logger.warning(f"Contrast enhancement failed: {str(e)}")
            return image
    
    def denoise_image(self, image: np.ndarray, apply: bool = True) -> np.ndarray:
        """Apply denoising to improve OCR accuracy"""
        if not apply:
            return image
        
        try:
            if len(image.shape) == 3:
                # Color image
                return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
            else:
                # Grayscale image
                return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
        except Exception as e:
            self.logger.warning(f"Denoising failed: {str(e)}")
            return image
    
    def apply_threshold(self, image: np.ndarray, method: str = 'adaptive') -> np.ndarray:
        """Apply thresholding to improve text contrast"""
        try:
            if method == 'adaptive':
                # Adaptive thresholding works well for varying lighting
                return cv2.adaptiveThreshold(
                    image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
            elif method == 'otsu':
                # Otsu's method for bimodal images
                _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                return thresh
            elif method == 'binary':
                # Simple binary threshold
                _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
                return thresh
            else:
                return image
                
        except Exception as e:
            self.logger.warning(f"Thresholding failed: {str(e)}")
            return image
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """Get basic information about an image file"""
        try:
            image = self.load_image(image_path)
            height, width = image.shape[:2]
            
            return {
                'width': width,
                'height': height,
                'channels': image.shape[2] if len(image.shape) == 3 else 1,
                'file_size': Path(image_path).stat().st_size
            }
            
        except Exception as e:
            return {'error': str(e)}
