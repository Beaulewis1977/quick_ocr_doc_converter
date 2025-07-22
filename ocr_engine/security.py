#!/usr/bin/env python3
"""
Security Hardening Module for OCR Reader
Implements comprehensive security validation and sanitization
"""

import re
import html
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib
import logging

class SecurityError(Exception):
    """Custom exception for security-related errors"""
    pass

class OCRSecurityValidator:
    """Comprehensive security validation for OCR operations"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.max_file_size = self.config.get('max_file_size_mb', 50) * 1024 * 1024  # 50MB default
        self.allowed_extensions = set(self.config.get('allowed_extensions', 
            ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.pdf']))
        self.allowed_mime_types = {
            'image/png', 'image/jpeg', 'image/tiff', 'image/bmp', 'application/pdf'
        }
        self.logger = logging.getLogger(__name__)
    
    def validate_input_path(self, path: str) -> bool:
        """
        Comprehensive input validation for file paths
        
        Args:
            path: File path to validate
            
        Returns:
            True if path is valid
            
        Raises:
            SecurityError: If path contains security risks
        """
        try:
            # Normalize and resolve path
            path_obj = Path(path).resolve()
            
            # Check for directory traversal attacks
            if '..' in str(path_obj) or str(path_obj).startswith('..'):
                raise SecurityError("Directory traversal detected")
            
            # Ensure file exists and is actually a file
            if not path_obj.exists():
                raise SecurityError(f"File does not exist: {path_obj}")
            
            if not path_obj.is_file():
                raise SecurityError(f"Path is not a file: {path_obj}")
            
            # Validate file extension
            if path_obj.suffix.lower() not in self.allowed_extensions:
                raise SecurityError(f"Unsupported file type: {path_obj.suffix}")
            
            # Check file size
            file_size = path_obj.stat().st_size
            if file_size > self.max_file_size:
                raise SecurityError(
                    f"File too large: {file_size} bytes > {self.max_file_size} bytes"
                )
            
            # Verify file permissions (readable)
            if not os.access(path_obj, os.R_OK):
                raise SecurityError(f"File is not readable: {path_obj}")
            
            return True
            
        except (OSError, IOError) as e:
            raise SecurityError(f"File access error: {e}")
    
    def validate_output_path(self, path: str) -> bool:
        """
        Validate output path for security and writability
        
        Args:
            path: Output path to validate
            
        Returns:
            True if path is valid for output
            
        Raises:
            SecurityError: If path is insecure or not writable
        """
        try:
            path_obj = Path(path).resolve()
            
            # Prevent directory traversal
            if '..' in str(path_obj):
                raise SecurityError("Directory traversal detected in output path")
            
            # Check directory permissions
            parent_dir = path_obj.parent
            if not parent_dir.exists():
                try:
                    parent_dir.mkdir(parents=True, exist_ok=True)
                except (OSError, IOError) as e:
                    raise SecurityError(f"Cannot create output directory: {e}")
            
            if not os.access(parent_dir, os.W_OK):
                raise SecurityError(f"Output directory not writable: {parent_dir}")
            
            return True
            
        except (OSError, IOError) as e:
            raise SecurityError(f"Output path validation error: {e}")
    
    def sanitize_ocr_output(self, text: str) -> str:
        """
        Sanitize OCR output to prevent XSS and injection attacks
        
        Args:
            text: Raw OCR text to sanitize
            
        Returns:
            Sanitized text safe for display/storage
        """
        if not isinstance(text, str):
            return ""
        
        # Remove potential XSS patterns
        # Remove script tags and JavaScript handlers
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', text, flags=re.IGNORECASE)
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        
        # HTML escape to prevent injection
        text = html.escape(text)
        
        # Remove control characters except newlines and tabs
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Limit excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def generate_safe_filename(self, original_filename: str) -> str:
        """
        Generate a safe filename from original
        
        Args:
            original_filename: Original filename
            
        Returns:
            Safe filename with only alphanumeric characters
        """
        # Remove path components
        filename = os.path.basename(original_filename)
        
        # Remove extension temporarily
        name, ext = os.path.splitext(filename)
        
        # Sanitize name - keep only alphanumeric, spaces, hyphens, underscores
        safe_name = re.sub(r'[^\w\s-]', '', name)
        safe_name = re.sub(r'\s+', '_', safe_name.strip())
        
        # Ensure not empty
        if not safe_name:
            safe_name = "ocr_output"
        
        # Limit length
        safe_name = safe_name[:50]
        
        # Reconstruct with safe extension
        safe_ext = ext.lower()
        if safe_ext not in {'.txt', '.md', '.json'}:
            safe_ext = '.txt'
        
        return f"{safe_name}{safe_ext}"
    
    def _generate_cache_key(self, image_path: str, language: str, backend: str) -> str:
        """Generate unique cache key for file"""
        try:
            path_obj = Path(image_path)
            
            # Use file content hash for cache key
            hasher = hashlib.md5()
            hasher.update(str(path_obj.resolve()).encode())
            hasher.update(str(path_obj.stat().st_mtime).encode())
            hasher.update(language.encode())
            hasher.update(backend.encode())
            
            return hasher.hexdigest()
        except Exception as e:
            self.logger.warning(f"Failed to generate cache key: {e}")
            return f"{Path(image_path).stem}_{language}_{backend}"

# Global security validator instance
security_validator = OCRSecurityValidator()