#!/usr/bin/env python3
"""
Secure Configuration Manager for OCR Document Converter
Handles encryption and secure storage of sensitive configuration data
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging
import base64
import secrets
import hashlib

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False

logger = logging.getLogger(__name__)

class SecureConfigurationError(Exception):
    """Exception raised for secure configuration errors"""
    pass

class SecureConfigManager:
    """Manages secure configuration with encryption for sensitive data"""
    
    def __init__(self, config_file: str = "config.json", encrypt_sensitive: bool = True):
        self.config_file = Path(config_file)
        self.encrypt_sensitive = encrypt_sensitive and HAS_CRYPTOGRAPHY
        self.sensitive_keys = {
            'api.google_vision.credentials_path',
            'api.google_vision.api_key',
            'database.password',
            'email.password',
            'ftp.password',
            'auth.secret_key'
        }
        
        if self.encrypt_sensitive and not HAS_CRYPTOGRAPHY:
            logger.warning("Cryptography library not available, sensitive data will not be encrypted")
            self.encrypt_sensitive = False
        
        self._encryption_key = None
        self._salt_file = self.config_file.with_suffix('.salt')
        
    def _get_encryption_key(self, password: Optional[str] = None) -> bytes:
        """
        Generate or retrieve encryption key for configuration
        
        Args:
            password: Optional password for key derivation
            
        Returns:
            Encryption key bytes
        """
        if self._encryption_key:
            return self._encryption_key
            
        if not self.encrypt_sensitive:
            return b''
            
        try:
            # Try to load existing salt
            if self._salt_file.exists():
                salt = self._salt_file.read_bytes()
            else:
                # Generate new salt
                salt = secrets.token_bytes(32)
                self._salt_file.write_bytes(salt)
                # Set restrictive permissions on salt file
                os.chmod(self._salt_file, 0o600)
            
            # Use environment variable or generate password
            if not password:
                password = os.environ.get('OCR_CONFIG_PASSWORD')
                if not password:
                    # For first-time setup, generate a random password
                    password = secrets.token_urlsafe(32)
                    logger.warning("Generated random password for config encryption. "
                                 "Set OCR_CONFIG_PASSWORD environment variable to persist.")
            
            # Derive key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            self._encryption_key = key
            return key
            
        except Exception as e:
            logger.error(f"Failed to generate encryption key: {e}")
            raise SecureConfigurationError(f"Encryption key generation failed: {e}")
    
    def _encrypt_value(self, value: str, password: Optional[str] = None) -> str:
        """
        Encrypt a sensitive configuration value
        
        Args:
            value: Value to encrypt
            password: Optional password for encryption
            
        Returns:
            Encrypted value as base64 string
        """
        if not self.encrypt_sensitive or not value:
            return value
            
        try:
            key = self._get_encryption_key(password)
            fernet = Fernet(key)
            encrypted = fernet.encrypt(value.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt value: {e}")
            raise SecureConfigurationError(f"Encryption failed: {e}")
    
    def _decrypt_value(self, encrypted_value: str, password: Optional[str] = None) -> str:
        """
        Decrypt a sensitive configuration value
        
        Args:
            encrypted_value: Encrypted value as base64 string
            password: Optional password for decryption
            
        Returns:
            Decrypted value
        """
        if not self.encrypt_sensitive or not encrypted_value:
            return encrypted_value
            
        try:
            key = self._get_encryption_key(password)
            fernet = Fernet(key)
            
            # Decode from base64 and decrypt
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_value.encode())
            decrypted = fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt value: {e}")
            # Return empty string rather than failing completely
            return ""
    
    def _is_sensitive_key(self, key_path: str) -> bool:
        """
        Check if a configuration key contains sensitive data
        
        Args:
            key_path: Dot-separated key path (e.g., 'api.google_vision.credentials_path')
            
        Returns:
            True if key is considered sensitive
        """
        return key_path in self.sensitive_keys or any(
            sensitive in key_path.lower() 
            for sensitive in ['password', 'key', 'secret', 'token', 'credential']
        )
    
    def _get_nested_value(self, config: Dict[str, Any], key_path: str) -> Any:
        """Get value from nested dictionary using dot notation"""
        keys = key_path.split('.')
        value = config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value
    
    def _set_nested_value(self, config: Dict[str, Any], key_path: str, value: Any) -> None:
        """Set value in nested dictionary using dot notation"""
        keys = key_path.split('.')
        current = config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
    
    def load_config(self, default_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Load configuration with automatic decryption of sensitive data
        
        Args:
            default_config: Default configuration to use if file doesn't exist
            
        Returns:
            Loaded configuration dictionary
        """
        try:
            if not self.config_file.exists():
                if default_config:
                    self.save_config(default_config)
                    return default_config
                else:
                    return {}
            
            # Load raw configuration
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Decrypt sensitive values
            if self.encrypt_sensitive:
                decrypted_config = self._decrypt_sensitive_values(config)
                return decrypted_config
            else:
                return config
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise SecureConfigurationError(f"Configuration file corrupted: {e}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise SecureConfigurationError(f"Configuration loading failed: {e}")
    
    def save_config(self, config: Dict[str, Any], password: Optional[str] = None) -> bool:
        """
        Save configuration with automatic encryption of sensitive data
        
        Args:
            config: Configuration dictionary to save
            password: Optional password for encryption
            
        Returns:
            True if successfully saved
        """
        try:
            # Create backup of existing config
            if self.config_file.exists():
                backup_file = self.config_file.with_suffix('.json.backup')
                backup_file.write_text(self.config_file.read_text())
            
            # Encrypt sensitive values
            if self.encrypt_sensitive:
                config_to_save = self._encrypt_sensitive_values(config, password)
            else:
                config_to_save = config.copy()
            
            # Save configuration
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            
            # Set restrictive permissions
            os.chmod(self.config_file, 0o600)
            
            logger.info(f"Configuration saved securely to: {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise SecureConfigurationError(f"Configuration saving failed: {e}")
    
    def _encrypt_sensitive_values(self, config: Dict[str, Any], password: Optional[str] = None) -> Dict[str, Any]:
        """Recursively encrypt sensitive values in configuration"""
        result = {}
        
        def encrypt_recursive(obj: Any, path: str = "") -> Any:
            if isinstance(obj, dict):
                return {
                    key: encrypt_recursive(value, f"{path}.{key}" if path else key)
                    for key, value in obj.items()
                }
            elif isinstance(obj, str) and self._is_sensitive_key(path) and obj:
                # Mark encrypted values with a prefix
                encrypted = self._encrypt_value(obj, password)
                return f"ENCRYPTED:{encrypted}"
            else:
                return obj
        
        return encrypt_recursive(config)
    
    def _decrypt_sensitive_values(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively decrypt sensitive values in configuration"""
        def decrypt_recursive(obj: Any, path: str = "") -> Any:
            if isinstance(obj, dict):
                return {
                    key: decrypt_recursive(value, f"{path}.{key}" if path else key)
                    for key, value in obj.items()
                }
            elif isinstance(obj, str) and obj.startswith("ENCRYPTED:"):
                # Remove prefix and decrypt
                encrypted_value = obj[10:]  # Remove "ENCRYPTED:" prefix
                return self._decrypt_value(encrypted_value)
            else:
                return obj
        
        return decrypt_recursive(config)
    
    def update_sensitive_value(self, key_path: str, value: str, password: Optional[str] = None) -> bool:
        """
        Update a sensitive configuration value
        
        Args:
            key_path: Dot-separated key path
            value: New value to set
            password: Optional password for encryption
            
        Returns:
            True if successfully updated
        """
        try:
            config = self.load_config()
            self._set_nested_value(config, key_path, value)
            return self.save_config(config, password)
        except Exception as e:
            logger.error(f"Failed to update sensitive value: {e}")
            return False
    
    def validate_credentials_file(self, file_path: str) -> bool:
        """
        Validate that a credentials file exists and has proper permissions
        
        Args:
            file_path: Path to credentials file
            
        Returns:
            True if file is valid and secure
        """
        try:
            if not file_path:
                return False
                
            path_obj = Path(file_path).expanduser().resolve()
            
            if not path_obj.exists():
                logger.warning(f"Credentials file not found: {path_obj}")
                return False
            
            if not path_obj.is_file():
                logger.warning(f"Credentials path is not a file: {path_obj}")
                return False
            
            # Check file permissions (should not be world-readable)
            file_stat = path_obj.stat()
            file_mode = file_stat.st_mode
            
            # Check if file is readable by others (dangerous)
            if file_mode & 0o044:  # Check group/other read permissions
                logger.warning(f"Credentials file has unsafe permissions: {path_obj}")
                return False
            
            # Try to read the file to ensure it's valid JSON
            try:
                with open(path_obj, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"Credentials file is not valid JSON: {path_obj}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating credentials file: {e}")
            return False

# Global secure config manager instance  
secure_config_manager = SecureConfigManager()