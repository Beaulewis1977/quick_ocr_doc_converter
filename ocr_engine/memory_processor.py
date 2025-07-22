#!/usr/bin/env python3
"""
Memory-Efficient Image Processing Module
Implements memory-safe image processing with size limits and chunking
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Generator, Tuple, Optional, Dict, Any
import logging
import tempfile
import gc

class MemoryLimitError(Exception):
    """Exception raised when memory limits are exceeded"""
    pass

class MemoryEfficientImageProcessor:
    """Memory-efficient image processing with automatic resource management"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.max_memory_mb = self.config.get('max_memory_mb', 100)
        self.max_memory_bytes = self.max_memory_mb * 1024 * 1024
        self.max_image_dimension = self.config.get('max_image_dimension', 10000)
        self.logger = logging.getLogger(__name__)
        
    def load_image_safe(self, image_path: str) -> np.ndarray:
        """
        Safely load image with memory and size checks
        
        Args:
            image_path: Path to image file
            
        Returns:
            Loaded image as numpy array
            
        Raises:
            MemoryLimitError: If image exceeds memory limits
            ValueError: If image cannot be loaded or is invalid
        """
        try:
            # Check file exists
            path_obj = Path(image_path)
            if not path_obj.exists():
                raise ValueError(f"Image file not found: {image_path}")
            
            # Get file size for preliminary check
            file_size = path_obj.stat().st_size
            if file_size > self.max_memory_bytes * 2:  # Conservative estimate
                raise MemoryLimitError(
                    f"Image file too large: {file_size} bytes exceeds limit"
                )
            
            # Load image with memory limit
            image = cv2.imread(str(path_obj))
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Check dimensions
            height, width = image.shape[:2]
            if width > self.max_image_dimension or height > self.max_image_dimension:
                raise MemoryLimitError(
                    f"Image dimensions too large: {width}x{height}"
                )
            
            # Check memory usage
            memory_usage = image.nbytes
            if memory_usage > self.max_memory_bytes:
                raise MemoryLimitError(
                    f"Image memory usage {memory_usage} exceeds limit {self.max_memory_bytes}"
                )
            
            return image
            
        except cv2.error as e:
            raise ValueError(f"OpenCV error loading image: {e}")
        except Exception as e:
            raise ValueError(f"Error loading image: {e}")
    
    def process_large_image_chunks(self, image_path: str, 
                                 chunk_size: int = 1024) -> Generator[np.ndarray, None, None]:
        """
        Process large images in memory-efficient chunks
        
        Args:
            image_path: Path to image file
            chunk_size: Size of chunks to process
            
        Yields:
            Image chunks as numpy arrays
        """
        try:
            image = self.load_image_safe(image_path)
            height, width = image.shape[:2]
            
            # If image fits in memory, return whole image
            if image.nbytes <= self.max_memory_bytes:
                yield image
                return
            
            # Calculate optimal chunk size
            chunk_height = min(chunk_size, height)
            chunk_width = min(chunk_size, width)
            
            # Process in overlapping chunks to avoid boundary issues
            overlap = min(50, chunk_height // 4, chunk_width // 4)
            
            for y in range(0, height, chunk_height - overlap):
                for x in range(0, width, chunk_width - overlap):
                    # Calculate chunk boundaries
                    y_start = max(0, y)
                    y_end = min(height, y + chunk_height)
                    x_start = max(0, x)
                    x_end = min(width, x + chunk_width)
                    
                    chunk = image[y_start:y_end, x_start:x_end]
                    
                    if chunk.size > 0:
                        yield chunk
                        
                        # Force garbage collection for large images
                        if chunk.nbytes > self.max_memory_bytes // 4:
                            gc.collect()
                            
        except Exception as e:
            self.logger.error(f"Error processing image chunks: {e}")
            raise
    
    def resize_image_if_needed(self, image: np.ndarray, 
                             max_dimension: Optional[int] = None) -> np.ndarray:
        """
        Resize image if it exceeds maximum dimensions
        
        Args:
            image: Input image as numpy array
            max_dimension: Maximum allowed dimension (width or height)
            
        Returns:
            Resized image if needed, original otherwise
        """
        if max_dimension is None:
            max_dimension = self.max_image_dimension
            
        height, width = image.shape[:2]
        
        if width <= max_dimension and height <= max_dimension:
            return image
        
        # Calculate scaling factor
        scale = min(max_dimension / width, max_dimension / height)
        
        # Calculate new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize image
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        self.logger.info(f"Resized image from {width}x{height} to {new_width}x{new_height}")
        
        return resized
    
    def create_temp_image_copy(self, image_path: str) -> str:
        """
        Create a temporary copy of image for safe processing
        
        Args:
            image_path: Original image path
            
        Returns:
            Path to temporary copy
        """
        try:
            with tempfile.NamedTemporaryFile(
                suffix='.png', 
                delete=False, 
                dir=tempfile.gettempdir()
            ) as tmp_file:
                
                image = self.load_image_safe(image_path)
                cv2.imwrite(tmp_file.name, image)
                
                return tmp_file.name
                
        except Exception as e:
            self.logger.error(f"Error creating temp image copy: {e}")
            raise
    
    def cleanup_temp_files(self, temp_paths: list):
        """Clean up temporary files"""
        for temp_path in temp_paths:
            try:
                temp_file = Path(temp_path)
                if temp_file.exists():
                    temp_file.unlink()
                    self.logger.debug(f"Cleaned up temp file: {temp_path}")
            except Exception as e:
                self.logger.warning(f"Failed to cleanup temp file {temp_path}: {e}")
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """
        Get comprehensive image information
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with image metadata
        """
        try:
            image = self.load_image_safe(image_path)
            height, width = image.shape[:2]
            
            return {
                'width': width,
                'height': height,
                'channels': image.shape[2] if len(image.shape) > 2 else 1,
                'memory_usage_bytes': image.nbytes,
                'file_size_bytes': Path(image_path).stat().st_size,
                'is_large': image.nbytes > self.max_memory_bytes,
                'needs_resize': width > self.max_image_dimension or height > self.max_image_dimension
            }
            
        except Exception as e:
            self.logger.error(f"Error getting image info: {e}")
            return {}
    
    def estimate_memory_usage(self, image_info: Dict[str, Any]) -> int:
        """
        Estimate memory usage for image processing
        
        Args:
            image_info: Image information dictionary
            
        Returns:
            Estimated memory usage in bytes
        """
        width = image_info.get('width', 0)
        height = image_info.get('height', 0)
        channels = image_info.get('channels', 3)
        
        # Base image memory
        base_memory = width * height * channels
        
        # Add processing overhead (typically 2-3x for OCR)
        processing_overhead = base_memory * 2.5
        
        return int(processing_overhead)

# Global memory-efficient processor instance
memory_processor = MemoryEfficientImageProcessor()