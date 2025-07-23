#!/usr/bin/env python3
"""
Configuration Manager for OCR Engine
Manages API keys and settings for various OCR backends
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import base64
import hashlib

try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    ENCRYPTION_AVAILABLE = False
    Fernet = None


class ConfigManager:
    """Manages OCR configuration including API keys and settings"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration manager
        
        Args:
            config_dir: Optional custom config directory
        """
        self.config_dir = config_dir or Path.home() / ".quick_document_convertor"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "ocr_config.json"
        self.encrypted_config_file = self.config_dir / "ocr_config.enc"
        self.key_file = self.config_dir / ".key"
        
        self.logger = logging.getLogger("ConfigManager")
        
        # Default configuration
        self.default_config = {
            "ocr_backends": {
                "default_backend": "auto",
                "tesseract": {
                    "enabled": True,
                    "languages": ["en"],
                    "config": "--oem 3 --psm 6",
                    "confidence_threshold": 30
                },
                "easyocr": {
                    "enabled": True,
                    "languages": ["en"],
                    "gpu": False,
                    "confidence_threshold": 30
                },
                "google_vision": {
                    "enabled": False,
                    "key_file": "",
                    "key_json": "",
                    "languages": ["en"],
                    "confidence_threshold": 30
                }
            },
            "processing": {
                "use_cache": True,
                "cache_ttl": 86400,
                "max_workers": 2,
                "preprocessing": {
                    "enhance_contrast": True,
                    "denoise": True,
                    "resize_max": 2048,
                    "threshold_method": "adaptive"
                }
            },
            "security": {
                "encrypt_api_keys": True,
                "max_file_size_mb": 50,
                "allowed_extensions": [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".gif", ".webp"]
            }
        }
        
        # Load configuration
        self.config = self.load_config()
    
    def _get_encryption_key(self) -> bytes:
        """Get or create encryption key for sensitive data"""
        if not ENCRYPTION_AVAILABLE:
            return b"dummy_key"  # Fallback when encryption is not available
        
        if self.key_file.exists():
            try:
                with open(self.key_file, 'rb') as f:
                    return f.read()
            except Exception as e:
                self.logger.warning(f"Failed to read encryption key: {e}")
        
        # Generate new key
        key = Fernet.generate_key()
        try:
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Make key file readable only by owner
            os.chmod(self.key_file, 0o600)
            return key
        except Exception as e:
            self.logger.error(f"Failed to save encryption key: {e}")
            return key
    
    def _encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data like API keys"""
        if not ENCRYPTION_AVAILABLE:
            self.logger.warning("Encryption not available, storing data unencrypted")
            return data
        
        try:
            key = self._get_encryption_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data.encode())
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            self.logger.error(f"Failed to encrypt data: {e}")
            return data  # Return unencrypted as fallback
    
    def _decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data like API keys"""
        if not ENCRYPTION_AVAILABLE:
            return encrypted_data
        
        try:
            key = self._get_encryption_key()
            fernet = Fernet(key)
            decoded = base64.b64decode(encrypted_data.encode())
            decrypted = fernet.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            self.logger.error(f"Failed to decrypt data: {e}")
            return encrypted_data  # Return as-is if decryption fails
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        config = self.default_config.copy()
        
        # Try to load encrypted config first
        if self.encrypted_config_file.exists():
            try:
                with open(self.encrypted_config_file, 'r') as f:
                    encrypted_data = f.read()
                decrypted_data = self._decrypt_sensitive_data(encrypted_data)
                loaded_config = json.loads(decrypted_data)
                self._deep_update(config, loaded_config)
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load encrypted config: {e}")
        
        # Fallback to unencrypted config
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                self._deep_update(config, loaded_config)
            except Exception as e:
                self.logger.error(f"Failed to load config: {e}")
        
        return config
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        try:
            # Save encrypted if encryption is enabled and available
            if config.get("security", {}).get("encrypt_api_keys", True) and ENCRYPTION_AVAILABLE:
                config_json = json.dumps(config, indent=2)
                encrypted_data = self._encrypt_sensitive_data(config_json)
                with open(self.encrypted_config_file, 'w') as f:
                    f.write(encrypted_data)
                # Remove unencrypted file if it exists
                if self.config_file.exists():
                    self.config_file.unlink()
            else:
                # Save unencrypted (either disabled or encryption not available)
                with open(self.config_file, 'w') as f:
                    json.dump(config, f, indent=2)
                # Remove encrypted file if it exists
                if self.encrypted_config_file.exists():
                    self.encrypted_config_file.unlink()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            return False
    
    def _deep_update(self, base_dict: Dict[str, Any], update_dict: Dict[str, Any]):
        """Deep update one dictionary with another"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def get_backend_config(self, backend_name: str) -> Dict[str, Any]:
        """Get configuration for a specific OCR backend"""
        return self.config.get("ocr_backends", {}).get(backend_name, {})
    
    def set_backend_config(self, backend_name: str, config: Dict[str, Any]) -> bool:
        """Set configuration for a specific OCR backend"""
        if "ocr_backends" not in self.config:
            self.config["ocr_backends"] = {}
        
        self.config["ocr_backends"][backend_name] = config
        return self.save_config()
    
    def get_google_vision_config(self) -> Dict[str, Any]:
        """Get Google Vision API configuration"""
        return self.get_backend_config("google_vision")
    
    def set_google_vision_key_file(self, key_file_path: str) -> bool:
        """Set Google Vision API key file path"""
        config = self.get_google_vision_config()
        config["key_file"] = key_file_path
        config["enabled"] = bool(key_file_path)
        return self.set_backend_config("google_vision", config)
    
    def set_google_vision_key_json(self, key_json: str) -> bool:
        """Set Google Vision API key JSON"""
        config = self.get_google_vision_config()
        config["key_json"] = key_json
        config["enabled"] = bool(key_json)
        return self.set_backend_config("google_vision", config)
    
    def is_backend_enabled(self, backend_name: str) -> bool:
        """Check if a backend is enabled"""
        return self.get_backend_config(backend_name).get("enabled", False)
    
    def enable_backend(self, backend_name: str, enabled: bool = True) -> bool:
        """Enable or disable a backend"""
        config = self.get_backend_config(backend_name)
        config["enabled"] = enabled
        return self.set_backend_config(backend_name, config)
    
    def get_default_backend(self) -> str:
        """Get the default OCR backend"""
        return self.config.get("ocr_backends", {}).get("default_backend", "auto")
    
    def set_default_backend(self, backend_name: str) -> bool:
        """Set the default OCR backend"""
        if "ocr_backends" not in self.config:
            self.config["ocr_backends"] = {}
        
        self.config["ocr_backends"]["default_backend"] = backend_name
        return self.save_config()
    
    def test_google_vision_config(self) -> Dict[str, Any]:
        """Test Google Vision API configuration"""
        try:
            from .google_vision_backend import GoogleVisionBackend
            
            config = self.get_google_vision_config()
            backend = GoogleVisionBackend(config)
            
            if not backend.is_available():
                return {
                    "success": False,
                    "error": "Google Vision API not available",
                    "details": "Check API credentials"
                }
            
            return backend.test_connection()
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "details": "Failed to test Google Vision API"
            }
    
    def get_all_backend_status(self) -> Dict[str, Any]:
        """Get status of all OCR backends"""
        status = {}
        
        # Test Tesseract
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            status["tesseract"] = {
                "available": True,
                "enabled": self.is_backend_enabled("tesseract"),
                "version": pytesseract.get_tesseract_version()
            }
        except:
            status["tesseract"] = {
                "available": False,
                "enabled": False,
                "error": "Tesseract not installed or not found"
            }
        
        # Test EasyOCR
        try:
            import easyocr
            status["easyocr"] = {
                "available": True,
                "enabled": self.is_backend_enabled("easyocr"),
                "version": "Available"
            }
        except:
            status["easyocr"] = {
                "available": False,
                "enabled": False,
                "error": "EasyOCR not installed"
            }
        
        # Test Google Vision
        google_test = self.test_google_vision_config()
        status["google_vision"] = {
            "available": google_test.get("success", False),
            "enabled": self.is_backend_enabled("google_vision"),
            "test_result": google_test
        }
        
        return status
    
    def export_config(self, export_path: Path, include_api_keys: bool = False) -> bool:
        """Export configuration to file"""
        try:
            export_config = self.config.copy()
            
            if not include_api_keys:
                # Remove sensitive information
                if "ocr_backends" in export_config:
                    for backend in export_config["ocr_backends"].values():
                        if isinstance(backend, dict):
                            backend.pop("key_file", None)
                            backend.pop("key_json", None)
            
            with open(export_path, 'w') as f:
                json.dump(export_config, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export config: {e}")
            return False
    
    def import_config(self, import_path: Path) -> bool:
        """Import configuration from file"""
        try:
            with open(import_path, 'r') as f:
                imported_config = json.load(f)
            
            # Merge with current config
            self._deep_update(self.config, imported_config)
            return self.save_config()
            
        except Exception as e:
            self.logger.error(f"Failed to import config: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults"""
        self.config = self.default_config.copy()
        return self.save_config()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of the current configuration"""
        return {
            "default_backend": self.get_default_backend(),
            "enabled_backends": [name for name in ["tesseract", "easyocr", "google_vision"] 
                               if self.is_backend_enabled(name)],
            "cache_enabled": self.config.get("processing", {}).get("use_cache", True),
            "encryption_enabled": self.config.get("security", {}).get("encrypt_api_keys", True),
            "config_file_exists": self.config_file.exists() or self.encrypted_config_file.exists()
        }