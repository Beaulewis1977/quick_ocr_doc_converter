"""
Secure credential management for OCR cloud API services

Provides encrypted storage and retrieval of API credentials with
audit logging and key rotation support.

Author: Terry AI Agent for Terragon Labs
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import base64

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

class CredentialError(Exception):
    """Raised when credential operations fail"""
    pass

class CredentialManager:
    """
    Secure credential management system
    
    Features:
    - Encrypted credential storage using Fernet
    - Key derivation from master password
    - Audit logging for all operations
    - Credential rotation support
    - Environment variable fallback
    """
    
    def __init__(self, config_dir: Optional[str] = None, master_password: Optional[str] = None):
        """
        Initialize credential manager
        
        Args:
            config_dir: Custom configuration directory
            master_password: Master password for encryption (uses env var if not provided)
        """
        if not CRYPTOGRAPHY_AVAILABLE:
            raise CredentialError("cryptography package is required for credential management")
        
        # Set up configuration directory
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".ocr_secure"
        
        self.config_dir.mkdir(mode=0o700, exist_ok=True)
        
        # Set up logging
        self.logger = logging.getLogger("CredentialManager")
        self.audit_log = self.config_dir / "audit.log"
        
        # Initialize encryption
        self.master_password = master_password or os.getenv('OCR_MASTER_PASSWORD')
        if not self.master_password:
            # Generate a default password from system info (not recommended for production)
            import getpass
            import platform
            system_info = f"{getpass.getuser()}_{platform.node()}_{platform.system()}"
            self.master_password = system_info[:32].ljust(32, '0')
            self.logger.warning("Using default master password. Set OCR_MASTER_PASSWORD environment variable for better security.")
        
        self._init_encryption()
        
    def _init_encryption(self):
        """Initialize encryption system"""
        # Derive key from master password
        password_bytes = self.master_password.encode('utf-8')
        salt = b'ocr_salt_2024'  # In production, use random salt stored securely
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        self.cipher = Fernet(key)
        
    def _log_audit(self, action: str, service: str, success: bool, details: str = ""):
        """Log audit event"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'action': action,
            'service': service,
            'success': success,
            'details': details,
            'user': os.getenv('USER', 'unknown')
        }
        
        try:
            with open(self.audit_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write audit log: {e}")
    
    def store_credentials(self, service: str, credentials: Dict[str, Any]) -> bool:
        """
        Store encrypted credentials for a service
        
        Args:
            service: Service name (e.g., 'google_vision', 'aws_textract')
            credentials: Dictionary containing credentials
            
        Returns:
            True if successful
        """
        try:
            # Validate service name
            if not service or not isinstance(service, str):
                raise CredentialError("Invalid service name")
            
            # Validate credentials
            if not credentials or not isinstance(credentials, dict):
                raise CredentialError("Invalid credentials format")
            
            # Add metadata
            credential_data = {
                'credentials': credentials,
                'created_at': datetime.now().isoformat(),
                'service': service,
                'version': 1
            }
            
            # Encrypt credentials
            credential_json = json.dumps(credential_data)
            encrypted_data = self.cipher.encrypt(credential_json.encode('utf-8'))
            
            # Store in secure file
            cred_file = self.config_dir / f"{service}.cred"
            with open(cred_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Set secure permissions
            os.chmod(cred_file, 0o600)
            
            self._log_audit("store_credentials", service, True)
            return True
            
        except Exception as e:
            self._log_audit("store_credentials", service, False, str(e))
            self.logger.error(f"Failed to store credentials for {service}: {e}")
            return False
    
    def get_credentials(self, service: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve and decrypt credentials for a service
        
        Args:
            service: Service name
            
        Returns:
            Credentials dictionary or None if not found
        """
        try:
            # Check environment variables first
            env_creds = self._get_credentials_from_env(service)
            if env_creds:
                self._log_audit("get_credentials", service, True, "from_environment")
                return env_creds
            
            # Try encrypted file
            cred_file = self.config_dir / f"{service}.cred"
            if not cred_file.exists():
                self._log_audit("get_credentials", service, False, "file_not_found")
                return None
            
            # Read and decrypt
            with open(cred_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            credential_data = json.loads(decrypted_data.decode('utf-8'))
            
            self._log_audit("get_credentials", service, True, "from_file")
            return credential_data.get('credentials')
            
        except Exception as e:
            self._log_audit("get_credentials", service, False, str(e))
            self.logger.error(f"Failed to get credentials for {service}: {e}")
            return None
    
    def _get_credentials_from_env(self, service: str) -> Optional[Dict[str, Any]]:
        """
        Get credentials from environment variables
        
        Args:
            service: Service name
            
        Returns:
            Credentials from environment or None
        """
        env_mappings = {
            'google_vision': {
                'credentials_path': 'GOOGLE_APPLICATION_CREDENTIALS',
                'project_id': 'GOOGLE_CLOUD_PROJECT'
            },
            'aws_textract': {
                'access_key_id': 'AWS_ACCESS_KEY_ID',
                'secret_access_key': 'AWS_SECRET_ACCESS_KEY',
                'region': 'AWS_DEFAULT_REGION'
            },
            'azure_vision': {
                'subscription_key': 'AZURE_COGNITIVE_SERVICES_KEY',
                'endpoint': 'AZURE_COGNITIVE_SERVICES_ENDPOINT'
            }
        }
        
        if service not in env_mappings:
            return None
        
        credentials = {}
        for key, env_var in env_mappings[service].items():
            value = os.getenv(env_var)
            if value:
                credentials[key] = value
        
        return credentials if credentials else None
    
    def delete_credentials(self, service: str) -> bool:
        """
        Delete stored credentials for a service
        
        Args:
            service: Service name
            
        Returns:
            True if successful
        """
        try:
            cred_file = self.config_dir / f"{service}.cred"
            if cred_file.exists():
                cred_file.unlink()
                self._log_audit("delete_credentials", service, True)
                return True
            else:
                self._log_audit("delete_credentials", service, False, "file_not_found")
                return False
                
        except Exception as e:
            self._log_audit("delete_credentials", service, False, str(e))
            self.logger.error(f"Failed to delete credentials for {service}: {e}")
            return False
    
    def list_services(self) -> list[str]:
        """
        List services with stored credentials
        
        Returns:
            List of service names
        """
        try:
            services = []
            for cred_file in self.config_dir.glob("*.cred"):
                service_name = cred_file.stem
                services.append(service_name)
            
            self._log_audit("list_services", "all", True, f"found_{len(services)}")
            return services
            
        except Exception as e:
            self._log_audit("list_services", "all", False, str(e))
            return []
    
    def rotate_credentials(self, service: str, new_credentials: Dict[str, Any]) -> bool:
        """
        Rotate credentials for a service (backup old, store new)
        
        Args:
            service: Service name
            new_credentials: New credentials to store
            
        Returns:
            True if successful
        """
        try:
            # Backup existing credentials
            old_creds = self.get_credentials(service)
            if old_creds:
                backup_file = self.config_dir / f"{service}.cred.backup"
                cred_file = self.config_dir / f"{service}.cred"
                if cred_file.exists():
                    import shutil
                    shutil.copy2(cred_file, backup_file)
                    os.chmod(backup_file, 0o600)
            
            # Store new credentials
            success = self.store_credentials(service, new_credentials)
            
            if success:
                self._log_audit("rotate_credentials", service, True)
            else:
                self._log_audit("rotate_credentials", service, False, "store_failed")
            
            return success
            
        except Exception as e:
            self._log_audit("rotate_credentials", service, False, str(e))
            self.logger.error(f"Failed to rotate credentials for {service}: {e}")
            return False
    
    def validate_credentials(self, service: str) -> bool:
        """
        Validate that credentials exist and are properly formatted
        
        Args:
            service: Service name
            
        Returns:
            True if credentials are valid
        """
        credentials = self.get_credentials(service)
        if not credentials:
            return False
        
        # Service-specific validation
        required_keys = {
            'google_vision': ['credentials_path'],
            'aws_textract': ['access_key_id', 'secret_access_key'],
            'azure_vision': ['subscription_key', 'endpoint']
        }
        
        if service in required_keys:
            return all(key in credentials for key in required_keys[service])
        
        return True
    
    def get_audit_log(self, days: int = 7) -> list[Dict[str, Any]]:
        """
        Get audit log entries from the last N days
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of audit log entries
        """
        try:
            if not self.audit_log.exists():
                return []
            
            cutoff_date = datetime.now() - timedelta(days=days)
            entries = []
            
            with open(self.audit_log, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        entry_date = datetime.fromisoformat(entry['timestamp'])
                        if entry_date >= cutoff_date:
                            entries.append(entry)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
            
            return sorted(entries, key=lambda x: x['timestamp'], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Failed to get audit log: {e}")
            return []
    
    def cleanup_old_backups(self, days: int = 30) -> int:
        """
        Clean up old credential backups
        
        Args:
            days: Age threshold in days
            
        Returns:
            Number of files cleaned up
        """
        try:
            cutoff_time = datetime.now().timestamp() - (days * 24 * 3600)
            cleaned = 0
            
            for backup_file in self.config_dir.glob("*.backup"):
                if backup_file.stat().st_mtime < cutoff_time:
                    backup_file.unlink()
                    cleaned += 1
            
            self._log_audit("cleanup_backups", "all", True, f"cleaned_{cleaned}")
            return cleaned
            
        except Exception as e:
            self._log_audit("cleanup_backups", "all", False, str(e))
            return 0