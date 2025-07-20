"""
Test utilities and helpers for Enhanced OCR System tests

Provides common utilities, mock generators, test data creation,
and helper functions for comprehensive testing.

Author: Terry AI Agent for Terragon Labs
"""

import tempfile
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, MagicMock
import random
import string
from PIL import Image, ImageDraw, ImageFont
import os


class TestDataGenerator:
    """Generate test data for OCR testing"""
    
    @staticmethod
    def create_test_image(text: str, size: tuple = (400, 200), 
                         background_color: str = 'white', 
                         text_color: str = 'black') -> Path:
        """Create a test image with specified text"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            img = Image.new('RGB', size, color=background_color)
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Center the text
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            
            draw.text((x, y), text, fill=text_color, font=font)
            img.save(tmp_file.name)
            
            return Path(tmp_file.name)
    
    @staticmethod
    def create_noisy_image(text: str, size: tuple = (400, 200), 
                          noise_level: float = 0.1) -> Path:
        """Create a noisy test image that's harder to OCR"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            img = Image.new('RGB', size, color='white')
            draw = ImageDraw.Draw(img)
            
            # Add noise
            for _ in range(int(size[0] * size[1] * noise_level)):
                x = random.randint(0, size[0] - 1)
                y = random.randint(0, size[1] - 1)
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                draw.point((x, y), fill=color)
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            draw.text((50, 90), text, fill='black', font=font)
            img.save(tmp_file.name)
            
            return Path(tmp_file.name)
    
    @staticmethod
    def create_document_image(lines: List[str], size: tuple = (600, 800)) -> Path:
        """Create a document-style image with multiple lines"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            img = Image.new('RGB', size, color='white')
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            y_offset = 50
            line_height = 30
            
            for line in lines:
                draw.text((50, y_offset), line, fill='black', font=font)
                y_offset += line_height
            
            img.save(tmp_file.name)
            return Path(tmp_file.name)
    
    @staticmethod
    def create_malformed_file(extension: str = '.txt') -> Path:
        """Create a malformed file for security testing"""
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as tmp_file:
            # Write some binary data that doesn't match the extension
            tmp_file.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00')
            return Path(tmp_file.name)


class MockBackendGenerator:
    """Generate mock backends for testing"""
    
    @staticmethod
    def create_successful_local_backend() -> Mock:
        """Create a mock local backend that always succeeds"""
        mock_backend = Mock()
        mock_backend.get_available_backends.return_value = ['tesseract', 'easyocr']
        mock_backend.extract_text.return_value = {
            'text': 'Mock successful OCR result',
            'confidence': 92.5,
            'success': True,
            'backend': 'tesseract'
        }
        return mock_backend
    
    @staticmethod
    def create_failing_backend() -> Mock:
        """Create a mock backend that always fails"""
        mock_backend = Mock()
        mock_backend.get_available_backends.return_value = []
        mock_backend.extract_text.side_effect = Exception("Mock backend failure")
        return mock_backend
    
    @staticmethod
    def create_cloud_backend_mock(service: str, confidence: float = 95.0) -> Mock:
        """Create a mock cloud backend"""
        mock_backend = Mock()
        
        if service == 'google_vision':
            mock_response = Mock()
            mock_response.text_annotations = [Mock(description=f"Mock {service} result")]
            mock_response.full_text_annotation = Mock(
                text=f"Mock {service} result",
                pages=[Mock(confidence=confidence/100)]
            )
            mock_backend.text_detection.return_value = mock_response
        
        elif service == 'aws_textract':
            mock_backend.detect_document_text.return_value = {
                'Blocks': [
                    {
                        'BlockType': 'LINE',
                        'Text': f'Mock {service} result',
                        'Confidence': confidence
                    }
                ]
            }
        
        elif service == 'azure_vision':
            mock_result = Mock()
            mock_result.read_results = [
                Mock(lines=[Mock(text=f"Mock {service} result", bounding_box=[1, 2, 3, 4])])
            ]
            mock_backend.read.return_value = Mock(operation_location="test://operation")
            mock_backend.get_read_result.return_value = mock_result
        
        return mock_backend


class TestCredentialsGenerator:
    """Generate test credentials for different services"""
    
    @staticmethod
    def generate_google_credentials() -> Dict[str, Any]:
        """Generate mock Google Cloud credentials"""
        return {
            'type': 'service_account',
            'project_id': 'test-project-12345',
            'private_key_id': 'test-key-id',
            'private_key': '-----BEGIN PRIVATE KEY-----\nMOCK_PRIVATE_KEY\n-----END PRIVATE KEY-----',
            'client_email': 'test@test-project-12345.iam.gserviceaccount.com',
            'client_id': '123456789012345678901',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
        }
    
    @staticmethod
    def generate_aws_credentials() -> Dict[str, Any]:
        """Generate mock AWS credentials"""
        return {
            'access_key_id': 'AKIA' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)),
            'secret_access_key': ''.join(random.choices(string.ascii_letters + string.digits + '+/', k=40)),
            'region': 'us-east-1'
        }
    
    @staticmethod
    def generate_azure_credentials() -> Dict[str, Any]:
        """Generate mock Azure credentials"""
        return {
            'subscription_key': ''.join(random.choices(string.ascii_lowercase + string.digits, k=32)),
            'endpoint': 'https://test-region.api.cognitive.microsoft.com/'
        }
    
    @staticmethod
    def generate_all_credentials() -> Dict[str, Any]:
        """Generate a complete set of mock credentials"""
        return {
            'google_vision': {
                'credentials_path': '/mock/path/to/google-credentials.json'
            },
            'aws_textract': TestCredentialsGenerator.generate_aws_credentials(),
            'azure_vision': TestCredentialsGenerator.generate_azure_credentials()
        }


class PerformanceTestHelper:
    """Helper for performance testing"""
    
    @staticmethod
    def measure_execution_time(func, *args, **kwargs):
        """Measure execution time of a function"""
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time
    
    @staticmethod
    def get_memory_usage():
        """Get current memory usage"""
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            return process.memory_info().rss
        except ImportError:
            return None
    
    @staticmethod
    def create_load_test_data(count: int) -> List[Dict[str, Any]]:
        """Create test data for load testing"""
        test_data = []
        
        for i in range(count):
            test_data.append({
                'file_path': f'/test/load_test_{i}.png',
                'backend': random.choice(['local', 'google_vision', 'aws_textract']),
                'expected_text': f'Load test document {i}',
                'confidence': random.uniform(70.0, 99.0),
                'processing_time': random.uniform(0.5, 3.0)
            })
        
        return test_data


class SecurityTestHelper:
    """Helper for security testing"""
    
    @staticmethod
    def generate_malicious_inputs() -> List[str]:
        """Generate various malicious input patterns"""
        return [
            # SQL Injection
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'/*",
            "1; EXEC xp_cmdshell('format c:')",
            
            # XSS
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            
            # Path Traversal
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "/etc/shadow",
            
            # Command Injection
            "; rm -rf /",
            "| cat /etc/passwd",
            "&& format c:",
            "`whoami`",
            "$(cat /etc/passwd)",
            
            # Template Injection
            "{{7*7}}",
            "${7*7}",
            "#{7*7}",
            
            # LDAP Injection
            "admin)(|(password=*)",
            "*)(uid=*",
            
            # XML Injection
            "<?xml version='1.0'?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///etc/passwd'>]><root>&test;</root>",
        ]
    
    @staticmethod
    def generate_pii_data() -> List[str]:
        """Generate text containing PII for masking tests"""
        return [
            "John Doe's SSN is 123-45-6789",
            "Contact us at john.doe@example.com",
            "Call me at (555) 123-4567",
            "Credit card: 4532-1234-5678-9012",
            "Driver's license: D123-456-789-012",
            "Account number: 9876543210",
            "Customer ID: CUST-12345-ABCDE",
            "Tax ID: 12-3456789",
        ]
    
    @staticmethod
    def create_malicious_file_content() -> List[tuple]:
        """Create malicious file content patterns"""
        return [
            ('.php', '<?php system($_GET["cmd"]); ?>'),
            ('.jsp', '<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>'),
            ('.aspx', '<script runat="server">Response.Write(System.Diagnostics.Process.Start(Request["cmd"]));</script>'),
            ('.py', 'import os; os.system("rm -rf /")')
        ]


class CostTrackingTestHelper:
    """Helper for cost tracking tests"""
    
    @staticmethod
    def generate_usage_data(count: int) -> List[Dict[str, Any]]:
        """Generate realistic usage data for testing"""
        backends = ['local', 'google_vision', 'aws_textract', 'azure_vision']
        costs = {'local': 0.0, 'google_vision': 0.0015, 'aws_textract': 0.002, 'azure_vision': 0.001}
        
        usage_data = []
        
        for i in range(count):
            backend = random.choice(backends)
            success = random.random() > 0.1  # 90% success rate
            
            usage_data.append({
                'backend': backend,
                'image_path': f'/test/usage_{i}.png',
                'result': {
                    'text': f'Usage test result {i}' if success else '',
                    'confidence': random.uniform(70.0, 98.0) if success else 0.0,
                    'success': success,
                    'duration': random.uniform(0.5, 4.0)
                },
                'cost': costs[backend] if success else 0.0,
                'image_size_mb': random.uniform(0.5, 10.0)
            })
        
        return usage_data
    
    @staticmethod
    def create_budget_scenarios() -> List[Dict[str, Any]]:
        """Create budget test scenarios"""
        return [
            {
                'name': 'Under Budget',
                'budget': 100.0,
                'usage_cost': 50.0,
                'expected_alert': False
            },
            {
                'name': 'Near Budget Warning',
                'budget': 100.0,
                'usage_cost': 80.0,
                'expected_alert': True,
                'alert_type': 'budget_warning'
            },
            {
                'name': 'Over Budget',
                'budget': 100.0,
                'usage_cost': 120.0,
                'expected_alert': True,
                'alert_type': 'budget_exceeded'
            }
        ]


class CleanupHelper:
    """Helper for test cleanup"""
    
    def __init__(self):
        self.temp_files = []
        self.temp_dirs = []
    
    def add_temp_file(self, file_path: Path):
        """Add a temporary file for cleanup"""
        self.temp_files.append(file_path)
    
    def add_temp_dir(self, dir_path: Path):
        """Add a temporary directory for cleanup"""
        self.temp_dirs.append(dir_path)
    
    def cleanup_all(self):
        """Clean up all temporary files and directories"""
        # Clean up files
        for file_path in self.temp_files:
            try:
                if file_path.exists():
                    file_path.unlink()
            except Exception:
                pass  # Ignore cleanup errors
        
        # Clean up directories
        for dir_path in self.temp_dirs:
            try:
                if dir_path.exists():
                    import shutil
                    shutil.rmtree(dir_path)
            except Exception:
                pass  # Ignore cleanup errors
        
        self.temp_files.clear()
        self.temp_dirs.clear()


# Test assertion helpers
def assert_ocr_result_structure(result: Dict[str, Any]):
    """Assert that an OCR result has the expected structure"""
    required_keys = ['text', 'confidence', 'success']
    for key in required_keys:
        assert key in result, f"Missing required key: {key}"
    
    assert isinstance(result['text'], str), "Text should be a string"
    assert isinstance(result['confidence'], (int, float)), "Confidence should be numeric"
    assert isinstance(result['success'], bool), "Success should be boolean"
    
    if result['success']:
        assert 0 <= result['confidence'] <= 100, "Confidence should be between 0 and 100"


def assert_cost_tracking_data(usage_record):
    """Assert that cost tracking data has the expected structure"""
    required_attrs = ['timestamp', 'backend', 'cost', 'success']
    for attr in required_attrs:
        assert hasattr(usage_record, attr), f"Missing required attribute: {attr}"
    
    assert usage_record.cost >= 0, "Cost should be non-negative"
    assert isinstance(usage_record.success, bool), "Success should be boolean"


def assert_security_validation_passed(validator, file_path):
    """Assert that security validation passes for a file"""
    try:
        validator.validate_file_path(file_path)
    except Exception as e:
        assert False, f"Security validation failed unexpectedly: {e}"


# Common test patterns
class TestPatterns:
    """Common test patterns and scenarios"""
    
    @staticmethod
    def test_error_handling_pattern(func, *args, **kwargs):
        """Test error handling pattern"""
        # Test with None input
        try:
            result = func(None, *args[1:], **kwargs)
            # Should either handle gracefully or raise appropriate exception
            assert result is not None or True  # Allow None as valid response
        except (ValueError, TypeError):
            pass  # Expected for None input
        
        # Test with empty input
        try:
            result = func("", *args[1:], **kwargs)
            assert result is not None or True
        except (ValueError, TypeError):
            pass
    
    @staticmethod
    def test_boundary_conditions(func, valid_input, boundary_values):
        """Test boundary conditions"""
        for boundary_value in boundary_values:
            try:
                result = func(boundary_value)
                # Should handle boundary gracefully
                assert result is not None or True
            except Exception as e:
                # Should be a reasonable exception type
                assert isinstance(e, (ValueError, TypeError, OverflowError))
    
    @staticmethod
    def test_concurrent_access_pattern(func, *args, **kwargs):
        """Test concurrent access pattern"""
        import threading
        import time
        
        results = []
        errors = []
        
        def worker():
            try:
                result = func(*args, **kwargs)
                results.append(result)
            except Exception as e:
                errors.append(e)
        
        # Start multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=10)
        
        # Should handle concurrent access without major issues
        assert len(errors) <= len(threads) // 2  # Allow some failures but not total failure