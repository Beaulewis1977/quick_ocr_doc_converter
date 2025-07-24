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
            ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.pdf', '.docx', '.html', '.htm', '.md', '.markdown', '.txt', '.rtf', '.epub', '.webp']))
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
            # Check for directory traversal attempts in the original path
            if '..' in path or path.startswith('~'):
                raise SecurityError("Potential directory traversal detected")
            
            # Normalize and resolve path
            path_obj = Path(path).resolve()
            
            # Additional security check: ensure the resolved path doesn't escape allowed directories
            # This prevents symlink-based attacks
            if self.config.get('allowed_directories'):
                allowed_dirs = [Path(d).resolve() for d in self.config['allowed_directories']]
                if not any(path_obj.is_relative_to(allowed_dir) for allowed_dir in allowed_dirs):
                    raise SecurityError("Path is outside allowed directories")
            
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
            
            # Basic file content validation (magic number check)
            if not self._validate_file_content(path_obj):
                raise SecurityError(f"File content validation failed: {path_obj.suffix}")
            
            # Verify file permissions (readable)
            if not os.access(path_obj, os.R_OK):
                raise SecurityError(f"File is not readable: {path_obj}")
            
            return True
            
        except (OSError, IOError) as e:
            raise SecurityError(f"File access error: {e}")
    
    def _validate_file_content(self, path_obj: Path) -> bool:
        """
        Validate file content using magic numbers (file signatures)
        
        Args:
            path_obj: Path object to validate
            
        Returns:
            True if file content matches expected type
        """
        try:
            # Read first few bytes to check magic numbers
            with open(path_obj, 'rb') as f:
                header = f.read(16)
            
            if not header:
                return False
            
            # Define magic number signatures for supported file types
            file_signatures = {
                '.png': [b'\x89PNG\r\n\x1a\n'],
                '.jpg': [b'\xff\xd8\xff'],
                '.jpeg': [b'\xff\xd8\xff'],
                '.pdf': [b'%PDF-'],
                '.tiff': [b'II*\x00', b'MM\x00*'],  # Little-endian and big-endian TIFF
                '.bmp': [b'BM'],
                '.docx': [b'PK\x03\x04'],  # ZIP file header (DOCX is a ZIP file)
                '.webp': [b'RIFF'],  # WebP files start with RIFF then have WEBP at offset 8
            }
            
            file_ext = path_obj.suffix.lower()
            
            # If we don't have signature validation for this type, allow it
            if file_ext not in file_signatures:
                return True
            
            # Check if file starts with any of the valid signatures for this type
            valid_signatures = file_signatures[file_ext]
            for signature in valid_signatures:
                if header.startswith(signature):
                    return True
            
            # Special case for JPEG files - they might have different headers
            if file_ext in ['.jpg', '.jpeg']:
                # JPEG files can have various markers, but should start with FFD8
                if header.startswith(b'\xff\xd8'):
                    return True
            
            # Special case for WebP files - check for WEBP at offset 8
            if file_ext == '.webp' and len(header) >= 12:
                if header.startswith(b'RIFF') and header[8:12] == b'WEBP':
                    return True
            
            self.logger.warning(f"File content doesn't match expected type: {file_ext}")
            return False
            
        except Exception as e:
            self.logger.error(f"Content validation error: {e}")
            return False  # Fail safe - reject if we can't validate
    
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
            # Check for directory traversal attempts in the original path
            if '..' in path or path.startswith('~'):
                raise SecurityError("Potential directory traversal detected in output path")
            
            path_obj = Path(path).resolve()
            
            # Additional security check for allowed directories
            if self.config.get('allowed_directories'):
                allowed_dirs = [Path(d).resolve() for d in self.config['allowed_directories']]
                if not any(path_obj.is_relative_to(allowed_dir) for allowed_dir in allowed_dirs):
                    raise SecurityError("Output path is outside allowed directories")
            
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

def validate_file_path(file_path: str) -> bool:
    """
    Validate file path for security using the global security validator
    
    Args:
        file_path: Path to validate
        
    Returns:
        True if valid
        
    Raises:
        SecurityError: If path is insecure
    """
    return security_validator.validate_input_path(file_path)

def validate_output_path(output_path: str) -> bool:
    """
    Validate output path for security using the global security validator
    
    Args:
        output_path: Output path to validate
        
    Returns:
        True if valid
        
    Raises:
        SecurityError: If path is insecure
    """
    return security_validator.validate_output_path(output_path)

def sanitize_path_for_logging(file_path: str) -> str:
    """
    Sanitize file path for safe logging, removing sensitive directory information
    
    Args:
        file_path: Full file path
        
    Returns:
        Sanitized path showing only filename and parent directory
    """
    try:
        path_obj = Path(file_path)
        
        # Only show filename and immediate parent directory
        if path_obj.parent.name:
            return f".../{path_obj.parent.name}/{path_obj.name}"
        else:
            return path_obj.name
    except Exception:
        return "[sanitized_path]"

def sanitize_error_message(error_msg: str, file_path: str = None) -> str:
    """
    Sanitize error message to remove sensitive information
    
    Args:
        error_msg: Original error message
        file_path: Optional file path to sanitize within the message
        
    Returns:
        Sanitized error message
    """
    if not isinstance(error_msg, str):
        return "Error occurred"
    
    # If a file path is provided, replace it with sanitized version
    if file_path:
        try:
            sanitized_path = sanitize_path_for_logging(file_path)
            error_msg = error_msg.replace(str(file_path), sanitized_path)
            error_msg = error_msg.replace(str(Path(file_path).resolve()), sanitized_path)
        except Exception:
            pass
    
    # Remove common sensitive patterns
    import re
    
    # Remove full Windows paths (C:\Users\username\...)
    error_msg = re.sub(r'[C-Z]:\\Users\\[^\\]+\\[^\\]*', '[user_directory]', error_msg)
    
    # Remove full Unix paths (/home/username/...)  
    error_msg = re.sub(r'/home/[^/]+/[^/]*', '[user_directory]', error_msg)
    
    # Remove temporary file paths
    error_msg = re.sub(r'/tmp/[^/\s]+', '[temp_file]', error_msg)
    error_msg = re.sub(r'\\temp\\[^\\s]+', '[temp_file]', error_msg)
    
    # Limit message length
    if len(error_msg) > 200:
        error_msg = error_msg[:197] + "..."
    
    return error_msg