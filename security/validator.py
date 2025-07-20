"""
Security validation module for OCR system

Provides comprehensive input validation, path traversal protection,
and output sanitization to ensure secure operation.

Author: Terry AI Agent for Terragon Labs
"""

import os
import re
import html
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional
try:
    import magic  # python-magic for MIME type detection
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False

class SecurityError(Exception):
    """Raised when security validation fails"""
    pass

class SecurityValidator:
    """
    Comprehensive security validator for OCR operations
    
    Features:
    - Path traversal protection
    - File type and size validation
    - MIME type verification
    - Output sanitization
    - PII detection and masking
    """
    
    # Allowed file extensions for OCR processing
    ALLOWED_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp', '.pdf'
    }
    
    # Maximum file size (50MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024
    
    # Allowed MIME types
    ALLOWED_MIME_TYPES = {
        'image/jpeg', 'image/png', 'image/bmp', 'image/tiff', 
        'image/gif', 'image/webp', 'application/pdf'
    }
    
    # PII patterns for detection and masking
    PII_PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
    }
    
    def __init__(self, enable_pii_masking: bool = True):
        """
        Initialize security validator
        
        Args:
            enable_pii_masking: Whether to enable PII detection and masking
        """
        self.enable_pii_masking = enable_pii_masking
        
    def validate_file_path(self, file_path: str) -> bool:
        """
        Validate file path for security issues
        
        Args:
            file_path: Path to validate
            
        Returns:
            True if path is safe
            
        Raises:
            SecurityError: If path is unsafe
        """
        try:
            # Convert to Path object and resolve
            path_obj = Path(file_path).resolve()
            
            # Check if file exists
            if not path_obj.exists():
                raise SecurityError(f"File does not exist: {file_path}")
            
            # Check for directory traversal
            if '..' in str(path_obj) or '..' in file_path:
                raise SecurityError("Directory traversal detected in path")
            
            # Check for null bytes and control characters
            if '\0' in file_path or any(ord(c) < 32 for c in file_path if c not in '\t\n\r'):
                raise SecurityError("Invalid characters detected in path")
            
            # Validate file extension
            if path_obj.suffix.lower() not in self.ALLOWED_EXTENSIONS:
                raise SecurityError(f"Unsupported file type: {path_obj.suffix}")
            
            # Check file size
            file_size = path_obj.stat().st_size
            if file_size > self.MAX_FILE_SIZE:
                size_mb = file_size / (1024 * 1024)
                raise SecurityError(f"File too large: {size_mb:.1f}MB (max: {self.MAX_FILE_SIZE / (1024 * 1024)}MB)")
            
            # Verify MIME type matches extension
            self._validate_mime_type(str(path_obj))
            
            return True
            
        except SecurityError:
            raise
        except Exception as e:
            raise SecurityError(f"Path validation failed: {e}")
    
    def _validate_mime_type(self, file_path: str) -> None:
        """
        Validate MIME type matches file extension
        
        Args:
            file_path: Path to file
            
        Raises:
            SecurityError: If MIME type is invalid
        """
        try:
            # Get MIME type using python-magic if available
            if HAS_MAGIC:
                mime_type = magic.from_file(file_path, mime=True)
                
                if mime_type not in self.ALLOWED_MIME_TYPES:
                    raise SecurityError(f"Invalid MIME type: {mime_type}")
            else:
                # Fallback to basic mimetypes if magic is not available
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type and mime_type not in self.ALLOWED_MIME_TYPES:
                    raise SecurityError(f"Invalid MIME type: {mime_type}")
            
            # Additional check: ensure MIME type matches extension (only if magic is available)
            if HAS_MAGIC:
                path_obj = Path(file_path)
                expected_mime, _ = mimetypes.guess_type(str(path_obj))
                
                if expected_mime and expected_mime != mime_type:
                    # Allow some common variations
                    allowed_variations = {
                        ('image/jpeg', 'image/jpg'),
                        ('image/tiff', 'image/tif'),
                    }
                    
                    if not any((mime_type, expected_mime) in variation or 
                              (expected_mime, mime_type) in variation 
                              for variation in allowed_variations):
                        raise SecurityError(f"MIME type mismatch: file extension suggests {expected_mime}, but file is {mime_type}")
                    
        except SecurityError:
            raise
        except Exception as e:
            raise SecurityError(f"MIME type validation failed: {e}")
    
    def sanitize_ocr_output(self, text: str) -> str:
        """
        Sanitize OCR output for safe display and storage
        
        Args:
            text: Raw OCR text output
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # HTML escape to prevent XSS
        sanitized = html.escape(text)
        
        # Remove potentially dangerous script-like patterns
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'data:text/html',
            r'vbscript:',
            r'on\w+\s*=',  # HTML event handlers
        ]
        
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        
        # Mask PII if enabled
        if self.enable_pii_masking:
            sanitized = self._mask_pii(sanitized)
        
        return sanitized
    
    def _mask_pii(self, text: str) -> str:
        """
        Detect and mask PII in text
        
        Args:
            text: Text to process
            
        Returns:
            Text with PII masked
        """
        masked_text = text
        
        for pii_type, pattern in self.PII_PATTERNS.items():
            def mask_match(match):
                matched_text = match.group()
                if pii_type == 'email':
                    # Keep first letter and domain
                    parts = matched_text.split('@')
                    if len(parts) == 2:
                        return f"{parts[0][0]}***@{parts[1]}"
                elif pii_type == 'phone':
                    # Keep area code
                    return re.sub(r'\d', '*', matched_text, count=7)
                elif pii_type == 'ssn':
                    # Mask middle digits
                    return re.sub(r'\d{3}-(\d{2})-\d{4}', r'***-\1-****', matched_text)
                elif pii_type == 'credit_card':
                    # Keep last 4 digits
                    digits = re.findall(r'\d', matched_text)
                    if len(digits) >= 4:
                        masked_digits = ['*'] * (len(digits) - 4) + digits[-4:]
                        return re.sub(r'\d', lambda m: masked_digits.pop(0), matched_text)
                
                return '*' * len(matched_text)
            
            masked_text = re.sub(pattern, mask_match, masked_text)
        
        return masked_text
    
    def validate_output_path(self, output_path: str) -> bool:
        """
        Validate output path for security
        
        Args:
            output_path: Output path to validate
            
        Returns:
            True if path is safe
            
        Raises:
            SecurityError: If path is unsafe
        """
        try:
            path_obj = Path(output_path).resolve()
            
            # Check for directory traversal
            if '..' in str(path_obj) or '..' in output_path:
                raise SecurityError("Directory traversal detected in output path")
            
            # Check for null bytes and control characters
            if '\0' in output_path or any(ord(c) < 32 for c in output_path if c not in '\t\n\r'):
                raise SecurityError("Invalid characters detected in output path")
            
            # Ensure parent directory exists or can be created
            parent_dir = path_obj.parent
            if not parent_dir.exists():
                try:
                    parent_dir.mkdir(parents=True, exist_ok=True)
                except PermissionError:
                    raise SecurityError("Insufficient permissions to create output directory")
                except Exception as e:
                    raise SecurityError(f"Cannot create output directory: {e}")
            
            return True
            
        except SecurityError:
            raise
        except Exception as e:
            raise SecurityError(f"Output path validation failed: {e}")
    
    def get_safe_filename(self, filename: str) -> str:
        """
        Generate a safe filename by removing/replacing unsafe characters
        
        Args:
            filename: Original filename
            
        Returns:
            Safe filename
        """
        # Remove or replace unsafe characters
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        safe_filename = re.sub(r'[^\x20-\x7E]', '_', safe_filename)  # Remove non-printable chars
        safe_filename = safe_filename.strip('. ')  # Remove leading/trailing dots and spaces
        
        # Ensure filename is not empty
        if not safe_filename:
            safe_filename = "sanitized_file"
        
        # Limit length
        if len(safe_filename) > 255:
            name, ext = os.path.splitext(safe_filename)
            safe_filename = name[:255-len(ext)] + ext
        
        return safe_filename
    
    def check_file_permissions(self, file_path: str) -> Dict[str, bool]:
        """
        Check file permissions
        
        Args:
            file_path: Path to check
            
        Returns:
            Dictionary with permission flags
        """
        try:
            path_obj = Path(file_path)
            return {
                'readable': os.access(str(path_obj), os.R_OK),
                'writable': os.access(str(path_obj), os.W_OK),
                'executable': os.access(str(path_obj), os.X_OK),
                'exists': path_obj.exists()
            }
        except Exception:
            return {
                'readable': False,
                'writable': False,
                'executable': False,
                'exists': False
            }
    
    def get_pii_patterns(self) -> Dict[str, Any]:
        """
        Get PII detection patterns
        
        Returns:
            Dictionary of PII patterns
        """
        import re
        return {name: re.compile(pattern) for name, pattern in self.PII_PATTERNS.items()}