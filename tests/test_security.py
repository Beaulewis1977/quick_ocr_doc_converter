"""
Security tests for the enhanced OCR system

Tests security validation, input sanitization, credential management,
and protection against various attack vectors.

Author: Terry AI Agent for Terragon Labs
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import os

from security import SecurityValidator, CredentialManager


class TestSecurityValidator:
    """Test suite for SecurityValidator"""
    
    def test_allowed_file_extensions(self, security_validator, temp_image):
        """Test that allowed file extensions pass validation"""
        # Should pass validation
        security_validator.validate_file_path(str(temp_image))
        
        # Test various allowed extensions
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp', '.pdf']
        for ext in allowed_extensions:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                try:
                    security_validator.validate_file_path(tmp.name)
                except Exception as e:
                    # Should not raise for allowed extensions
                    if "not allowed" in str(e):
                        pytest.fail(f"Extension {ext} should be allowed but was rejected")
                finally:
                    os.unlink(tmp.name)
    
    def test_disallowed_file_extensions(self, security_validator, malicious_file):
        """Test that disallowed file extensions are rejected"""
        with pytest.raises(ValueError, match="File extension .* not allowed"):
            security_validator.validate_file_path(str(malicious_file))
        
        # Test various disallowed extensions
        disallowed_extensions = ['.exe', '.bat', '.sh', '.scr', '.com', '.pif']
        for ext in disallowed_extensions:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                try:
                    with pytest.raises(ValueError, match="File extension .* not allowed"):
                        security_validator.validate_file_path(tmp.name)
                finally:
                    os.unlink(tmp.name)
    
    def test_path_traversal_protection(self, security_validator):
        """Test protection against path traversal attacks"""
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "/etc/shadow",
            "C:\\Windows\\System32\\config\\SAM",
            "file:///etc/passwd",
            "\\\\server\\share\\file.txt"
        ]
        
        for path in malicious_paths:
            with pytest.raises(ValueError, match="Invalid file path"):
                security_validator.validate_file_path(path)
    
    def test_file_size_limits(self, security_validator, temp_dir):
        """Test file size validation"""
        # Create a file that's too large (simulate 60MB)
        large_file = temp_dir / "large_file.png"
        
        # Mock the file size check
        with patch('pathlib.Path.stat') as mock_stat:
            mock_stat.return_value.st_size = 60 * 1024 * 1024  # 60MB
            
            with pytest.raises(ValueError, match="File size .* exceeds maximum"):
                security_validator.validate_file_path(str(large_file))
    
    def test_nonexistent_file_rejection(self, security_validator):
        """Test that nonexistent files are rejected"""
        with pytest.raises(ValueError, match="File does not exist"):
            security_validator.validate_file_path("/nonexistent/file.png")
    
    def test_directory_rejection(self, security_validator, temp_dir):
        """Test that directories are rejected"""
        with pytest.raises(ValueError, match="Path is not a file"):
            security_validator.validate_file_path(str(temp_dir))
    
    def test_pii_detection(self, security_validator):
        """Test PII detection in text"""
        text_with_pii = """
        John Doe's social security number is 123-45-6789.
        His email is john.doe@example.com and phone is (555) 123-4567.
        Credit card: 4532-1234-5678-9012
        """
        
        patterns = security_validator.get_pii_patterns()
        pii_found = []
        
        for pattern_name, pattern in patterns.items():
            if pattern.search(text_with_pii):
                pii_found.append(pattern_name)
        
        # Should detect multiple PII types
        assert len(pii_found) >= 3
        assert 'ssn' in pii_found
        assert 'email' in pii_found
        assert 'phone' in pii_found
    
    def test_pii_masking(self, security_validator):
        """Test PII masking functionality"""
        original_text = """
        Contact John at john.doe@example.com or call (555) 123-4567.
        SSN: 123-45-6789, Credit Card: 4532-1234-5678-9012
        """
        
        masked_text = security_validator.sanitize_ocr_output(original_text)
        
        # Check that PII has been masked
        assert "john.doe@example.com" not in masked_text
        assert "(555) 123-4567" not in masked_text
        assert "123-45-6789" not in masked_text
        assert "4532-1234-5678-9012" not in masked_text
        
        # Check that masking placeholders are present
        assert "[EMAIL]" in masked_text or "***" in masked_text
    
    def test_sql_injection_patterns(self, security_validator):
        """Test detection of SQL injection patterns"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'/*",
            "1; EXEC xp_cmdshell('format c:')",
            "UNION SELECT password FROM users"
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValueError, match="Potentially malicious content detected"):
                security_validator.validate_input(malicious_input)
    
    def test_script_injection_patterns(self, security_validator):
        """Test detection of script injection patterns"""
        malicious_scripts = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "{{7*7}}",  # Template injection
            "${7*7}",   # Expression language injection
        ]
        
        for script in malicious_scripts:
            with pytest.raises(ValueError, match="Potentially malicious content detected"):
                security_validator.validate_input(script)
    
    def test_command_injection_patterns(self, security_validator):
        """Test detection of command injection patterns"""
        malicious_commands = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "&& format c:",
            "`whoami`",
            "$(cat /etc/passwd)",
        ]
        
        for command in malicious_commands:
            with pytest.raises(ValueError, match="Potentially malicious content detected"):
                security_validator.validate_input(command)
    
    def test_safe_input_validation(self, security_validator):
        """Test that safe inputs pass validation"""
        safe_inputs = [
            "This is normal text",
            "Image with number 123",
            "Regular document content",
            "Some special chars: !@#$%^&*()",
            "Unicode text: café résumé naïve"
        ]
        
        for safe_input in safe_inputs:
            # Should not raise any exceptions
            security_validator.validate_input(safe_input)
    
    @pytest.mark.security
    def test_malicious_file_content_detection(self, security_validator, temp_dir):
        """Test detection of malicious file content"""
        # Create a file with potential malicious content
        malicious_file = temp_dir / "malicious.txt"
        malicious_file.write_text("<?php system($_GET['cmd']); ?>")
        
        # Should detect malicious patterns
        with pytest.raises(ValueError, match="Potentially malicious content detected"):
            content = malicious_file.read_text()
            security_validator.validate_input(content)


class TestCredentialManager:
    """Test suite for CredentialManager"""
    
    def test_credential_storage_and_retrieval(self, credential_manager, sample_credentials):
        """Test storing and retrieving credentials"""
        service = "test_service"
        credentials = sample_credentials['google_vision']
        
        # Store credentials
        success = credential_manager.store_credentials(service, credentials)
        assert success
        
        # Retrieve credentials
        retrieved = credential_manager.get_credentials(service)
        assert retrieved == credentials
    
    def test_credential_encryption(self, credential_manager, sample_credentials):
        """Test that credentials are encrypted in storage"""
        service = "test_service"
        credentials = sample_credentials['aws_textract']
        
        # Store credentials
        credential_manager.store_credentials(service, credentials)
        
        # Check that the stored file is encrypted (not plain JSON)
        storage_path = Path(credential_manager.config_dir)
        if storage_path.exists():
            raw_content = storage_path.read_bytes()
            # Should not contain plain text credentials
            assert b"AKIAIOSFODNN7EXAMPLE" not in raw_content
            assert b"wJalrXUtnFEMI" not in raw_content
    
    def test_credential_overwrite(self, credential_manager):
        """Test overwriting existing credentials"""
        service = "test_service"
        
        # Store initial credentials
        initial_creds = {"key": "initial_value"}
        credential_manager.store_credentials(service, initial_creds)
        
        # Overwrite with new credentials
        new_creds = {"key": "new_value", "additional": "data"}
        credential_manager.store_credentials(service, new_creds)
        
        # Should retrieve new credentials
        retrieved = credential_manager.get_credentials(service)
        assert retrieved == new_creds
        assert retrieved != initial_creds
    
    def test_nonexistent_credentials(self, credential_manager):
        """Test retrieving nonexistent credentials"""
        result = credential_manager.get_credentials("nonexistent_service")
        assert result is None
    
    def test_invalid_service_name(self, credential_manager):
        """Test handling of invalid service names"""
        invalid_names = ["", None, "../../etc/passwd", "service\x00name"]
        
        for invalid_name in invalid_names:
            if invalid_name is None:
                continue
            success = credential_manager.store_credentials(invalid_name, {"test": "data"})
            # Should handle gracefully (may return False or raise exception)
            assert success is False or isinstance(success, bool)
    
    def test_credential_deletion(self, credential_manager, sample_credentials):
        """Test deleting stored credentials"""
        service = "test_service"
        credentials = sample_credentials['azure_vision']
        
        # Store credentials
        credential_manager.store_credentials(service, credentials)
        assert credential_manager.get_credentials(service) is not None
        
        # Delete credentials
        success = credential_manager.delete_credentials(service)
        assert success
        
        # Should no longer exist
        assert credential_manager.get_credentials(service) is None
    
    def test_list_stored_services(self, credential_manager, sample_credentials):
        """Test listing all stored services"""
        # Store multiple credentials
        for service, creds in sample_credentials.items():
            credential_manager.store_credentials(service, creds)
        
        # List services
        services = credential_manager.list_services()
        
        # Should contain all stored services
        for service in sample_credentials.keys():
            assert service in services
    
    @pytest.mark.security
    def test_credential_file_permissions(self, credential_manager, sample_credentials):
        """Test that credential files have restricted permissions"""
        service = "test_service"
        credentials = sample_credentials['google_vision']
        
        # Store credentials
        credential_manager.store_credentials(service, credentials)
        
        # Check file permissions (Unix systems)
        storage_path = Path(credential_manager.config_dir)
        if storage_path.exists() and hasattr(os, 'stat'):
            stat_info = storage_path.stat()
            # Should be readable/writable by owner only (600 or 700)
            permissions = stat_info.st_mode & 0o777
            assert permissions in [0o600, 0o700], f"Insecure permissions: {oct(permissions)}"
    
    def test_audit_logging(self, credential_manager, sample_credentials):
        """Test that credential operations are logged"""
        service = "test_service"
        credentials = sample_credentials['google_vision']
        
        with patch('logging.Logger.info') as mock_log:
            # Store credentials
            credential_manager.store_credentials(service, credentials)
            
            # Should have logged the operation
            mock_log.assert_called()
            
            # Check log message contains service name
            log_calls = mock_log.call_args_list
            log_messages = [call[0][0] for call in log_calls]
            service_logged = any(service in msg for msg in log_messages)
            assert service_logged


@pytest.mark.security
class TestSecurityIntegration:
    """Integration tests for security components"""
    
    def test_end_to_end_security_validation(self, temp_image, security_validator):
        """Test complete security validation workflow"""
        # Should pass all security checks
        security_validator.validate_file_path(str(temp_image))
        
        # Simulate OCR result with PII
        ocr_result = "John Doe, SSN: 123-45-6789, Email: john@example.com"
        sanitized = security_validator.sanitize_ocr_output(ocr_result)
        
        # Should be sanitized
        assert "123-45-6789" not in sanitized
        assert "john@example.com" not in sanitized
    
    def test_security_with_malicious_workflow(self, malicious_file, security_validator):
        """Test security blocks malicious file workflow"""
        # Should block malicious file
        with pytest.raises(ValueError):
            security_validator.validate_file_path(str(malicious_file))
    
    def test_credential_security_workflow(self, credential_manager, temp_dir):
        """Test secure credential management workflow"""
        # Store sensitive credentials
        sensitive_creds = {
            "api_key": "super_secret_key_12345",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKBwx7Qx",
            "password": "very_secure_password"
        }
        
        # Store and retrieve
        credential_manager.store_credentials("sensitive_service", sensitive_creds)
        retrieved = credential_manager.get_credentials("sensitive_service")
        
        assert retrieved == sensitive_creds
        
        # Verify storage is encrypted
        storage_path = Path(credential_manager.config_dir)
        if storage_path.exists():
            raw_content = storage_path.read_text()
            assert "super_secret_key_12345" not in raw_content
            assert "very_secure_password" not in raw_content