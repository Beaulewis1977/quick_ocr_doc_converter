#!/usr/bin/env python3
"""
Comprehensive Error Handling System for OCR Reader
Provides structured error handling with retry logic and user-friendly messages
"""

import time
import logging
import traceback
from typing import Dict, Any, Optional, Callable, Type
from enum import Enum
import json

class OCRErrorType(Enum):
    """Enumeration of OCR error types"""
    TESSERACT_NOT_FOUND = "tesseract_not_found"
    TESSERACT_ERROR = "tesseract_error"
    IMAGE_NOT_FOUND = "image_not_found"
    INVALID_IMAGE = "invalid_image"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    SECURITY_VIOLATION = "security_violation"
    NETWORK_ERROR = "network_error"
    API_ERROR = "api_error"
    CONFIGURATION_ERROR = "configuration_error"
    PERMISSION_DENIED = "permission_denied"
    FILE_TOO_LARGE = "file_too_large"
    UNSUPPORTED_FORMAT = "unsupported_format"
    TRANSIENT_ERROR = "transient_error"
    PERMANENT_ERROR = "permanent_error"
    UNKNOWN_ERROR = "unknown_error"

class OCRError(Exception):
    """Base OCR error class with detailed context"""
    
    def __init__(self, 
                 message: str,
                 error_type: OCRErrorType,
                 details: Optional[Dict[str, Any]] = None,
                 suggestion: Optional[str] = None,
                 original_error: Optional[Exception] = None):
        super().__init__(message)
        self.error_type = error_type
        self.details = details or {}
        self.suggestion = suggestion
        self.original_error = original_error
        self.timestamp = time.time()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging/serialization"""
        return {
            'message': str(self),
            'error_type': self.error_type.value,
            'details': self.details,
            'suggestion': self.suggestion,
            'timestamp': self.timestamp,
            'original_error': str(self.original_error) if self.original_error else None
        }
    
    def __str__(self) -> str:
        base_message = super().__str__()
        if self.suggestion:
            return f"{base_message} Suggestion: {self.suggestion}"
        return base_message

class TransientOCRError(OCRError):
    """Error that may be resolved by retrying"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, OCRErrorType.TRANSIENT_ERROR, **kwargs)

class PermanentOCRError(OCRError):
    """Error that won't be resolved by retrying"""
    def __init__(self, message: str, **kwargs):
        super().__init__(message, OCRErrorType.PERMANENT_ERROR, **kwargs)

class OCRErrorHandler:
    """Comprehensive error handling with retry logic"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.retry_attempts = self.config.get('retry_attempts', 3)
        self.retry_delay = self.config.get('retry_delay', 1.0)
        self.max_retry_delay = self.config.get('max_retry_delay', 10.0)
        self.backoff_multiplier = self.config.get('backoff_multiplier', 2.0)
        self.logger = logging.getLogger(__name__)
        
        # Error type to retry mapping
        self.retryable_errors = {
            OCRErrorType.TESSERACT_ERROR,
            OCRErrorType.NETWORK_ERROR,
            OCRErrorType.TRANSIENT_ERROR,
            OCRErrorType.API_ERROR,
        }
    
    def with_retry(self, 
                   func: Callable,
                   *args,
                   retry_attempts: Optional[int] = None,
                   retry_delay: Optional[float] = None,
                   **kwargs) -> Any:
        """
        Execute function with intelligent retry logic
        
        Args:
            func: Function to execute
            *args: Function arguments
            retry_attempts: Override default retry attempts
            retry_delay: Override default retry delay
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            OCRError: Last error if all retries failed
        """
        max_attempts = retry_attempts or self.retry_attempts
        current_delay = retry_delay or self.retry_delay
        
        last_error = None
        
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
                
            except OCRError as e:
                last_error = e
                
                # Don't retry permanent errors
                if e.error_type not in self.retryable_errors:
                    self.logger.error(f"Non-retryable error: {e}")
                    raise e
                
                # Don't retry if this was the last attempt
                if attempt == max_attempts - 1:
                    self.logger.error(f"All retry attempts exhausted: {e}")
                    raise e
                
                # Log retry attempt
                self.logger.warning(
                    f"Attempt {attempt + 1} failed, retrying in {current_delay}s: {e}"
                )
                
                time.sleep(current_delay)
                current_delay = min(
                    current_delay * self.backoff_multiplier,
                    self.max_retry_delay
                )
                
            except Exception as e:
                # Convert unknown errors to OCR errors
                last_error = self._create_error_from_exception(e)
                
                if attempt == max_attempts - 1:
                    self.logger.error(f"Unknown error after retries: {e}")
                    raise last_error
                
                self.logger.warning(
                    f"Unknown error on attempt {attempt + 1}, retrying: {e}"
                )
                time.sleep(current_delay)
                current_delay = min(
                    current_delay * self.backoff_multiplier,
                    self.max_retry_delay
                )
        
        # Should never reach here
        raise last_error or PermanentOCRError("Unexpected error in retry logic")
    
    def create_user_friendly_error(self, error: OCRError) -> Dict[str, Any]:
        """
        Create user-friendly error message with troubleshooting steps
        
        Args:
            error: OCR error instance
            
        Returns:
            Dictionary with user-friendly information
        """
        error_mappings = {
            OCRErrorType.TESSERACT_NOT_FOUND: {
                "title": "Tesseract OCR Not Found",
                "description": "Tesseract OCR engine is not installed or not found in system PATH.",
                "troubleshooting": [
                    "Install Tesseract OCR: https://github.com/tesseract-ocr/tesseract",
                    "Add Tesseract to your system PATH",
                    "Use --tesseract-path to specify Tesseract location",
                    "Try: apt-get install tesseract-ocr (Linux)",
                    "Try: brew install tesseract (macOS)",
                    "Try: winget install tesseract-ocr.tesseract-ocr (Windows)"
                ]
            },
            OCRErrorType.IMAGE_NOT_FOUND: {
                "title": "Image File Not Found",
                "description": "The specified image file could not be accessed.",
                "troubleshooting": [
                    "Check that the file path is correct",
                    "Verify the file exists and is readable",
                    "Check file permissions",
                    "Ensure the file is not locked by another application"
                ]
            },
            OCRErrorType.MEMORY_LIMIT_EXCEEDED: {
                "title": "Memory Limit Exceeded",
                "description": "The image is too large to process with available memory.",
                "troubleshooting": [
                    "Reduce image resolution before processing",
                    "Process smaller image sections",
                    "Increase system memory",
                    "Use --max-memory option to increase memory limit"
                ]
            },
            OCRErrorType.SECURITY_VIOLATION: {
                "title": "Security Violation",
                "description": "The file contains potentially unsafe content.",
                "troubleshooting": [
                    "Verify the file is from a trusted source",
                    "Check file extension and format",
                    "Scan the file for malware",
                    "Use a different file"
                ]
            },
            OCRErrorType.FILE_TOO_LARGE: {
                "title": "File Too Large",
                "description": "The file exceeds the maximum allowed size.",
                "troubleshooting": [
                    "Compress the image to reduce file size",
                    "Split large PDFs into smaller files",
                    "Use --max-file-size to increase size limit",
                    "Process files in smaller batches"
                ]
            },
            OCRErrorType.NETWORK_ERROR: {
                "title": "Network Error",
                "description": "Failed to connect to OCR service.",
                "troubleshooting": [
                    "Check internet connection",
                    "Verify firewall settings",
                    "Check API credentials",
                    "Try again later (temporary network issue)"
                ]
            },
            OCRErrorType.API_ERROR: {
                "title": "API Error",
                "description": "The OCR service returned an error.",
                "troubleshooting": [
                    "Check API credentials and configuration",
                    "Verify API service is available",
                    "Check usage limits and quotas",
                    "Try using a different OCR backend"
                ]
            }
        }
        
        # Get specific error mapping or use generic
        mapping = error_mappings.get(
            error.error_type,
            {
                "title": "OCR Processing Error",
                "description": str(error),
                "troubleshooting": [error.suggestion or "Please check the error details"]
            }
        )
        
        return {
            "error": True,
            "error_type": error.error_type.value,
            "title": mapping["title"],
            "description": mapping["description"],
            "troubleshooting": mapping["troubleshooting"],
            "details": error.details if self.config.get('debug', False) else None,
            "timestamp": error.timestamp
        }
    
    def _create_error_from_exception(self, exception: Exception) -> OCRError:
        """Convert generic exception to OCR error"""
        error_type = OCRErrorType.UNKNOWN_ERROR
        suggestion = None
        
        # Map common exceptions to OCR error types
        if isinstance(exception, FileNotFoundError):
            error_type = OCRErrorType.IMAGE_NOT_FOUND
            suggestion = "Check file path and permissions"
        elif isinstance(exception, PermissionError):
            error_type = OCRErrorType.PERMISSION_DENIED
            suggestion = "Check file and directory permissions"
        elif isinstance(exception, MemoryError):
            error_type = OCRErrorType.MEMORY_LIMIT_EXCEEDED
            suggestion = "Reduce image size or increase memory limit"
        elif "tesseract" in str(exception).lower():
            if "not found" in str(exception).lower():
                error_type = OCRErrorType.TESSERACT_NOT_FOUND
                suggestion = "Install Tesseract OCR engine"
            else:
                error_type = OCRErrorType.TESSERACT_ERROR
                suggestion = "Check Tesseract configuration"
        
        return OCRError(
            str(exception),
            error_type,
            suggestion=suggestion,
            original_error=exception
        )
    
    def log_error(self, error: OCRError, context: Optional[Dict[str, Any]] = None):
        """Log error with context"""
        log_entry = {
            'error': error.to_dict(),
            'context': context or {},
            'stack_trace': traceback.format_exc()
        }
        
        self.logger.error(f"OCR Error: {json.dumps(log_entry, indent=2)}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of recent errors for monitoring"""
        # This would typically integrate with monitoring systems
        return {
            'error_types_count': {},
            'retry_success_rate': 0.0,
            'total_errors': 0,
            'last_error_time': None
        }

# Global error handler instance
error_handler = OCRErrorHandler()

# Convenience functions for common error creation
def create_tesseract_error(message: str, **kwargs) -> OCRError:
    """Create Tesseract-specific error"""
    return OCRError(message, OCRErrorType.TESSERACT_ERROR, **kwargs)

def create_security_error(message: str, **kwargs) -> OCRError:
    """Create security-specific error"""
    return OCRError(message, OCRErrorType.SECURITY_VIOLATION, **kwargs)

def create_memory_error(message: str, **kwargs) -> OCRError:
    """Create memory-specific error"""
    return OCRError(message, OCRErrorType.MEMORY_LIMIT_EXCEEDED, **kwargs)

# Context manager for automatic error handling
class OCRContext:
    """Context manager for OCR operations with automatic error handling"""
    
    def __init__(self, operation_name: str, error_handler: OCRErrorHandler = None):
        self.operation_name = operation_name
        self.error_handler = error_handler or OCRErrorHandler()
        self.logger = logging.getLogger(__name__)
    
    def __enter__(self):
        self.logger.info(f"Starting OCR operation: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            if issubclass(exc_type, OCRError):
                self.error_handler.log_error(exc_val, {'operation': self.operation_name})
            else:
                # Convert unknown exceptions
                error = self.error_handler._create_error_from_exception(exc_val)
                self.error_handler.log_error(error, {'operation': self.operation_name})
        
        self.logger.info(f"Completed OCR operation: {self.operation_name}")
        return False  # Don't suppress exceptions