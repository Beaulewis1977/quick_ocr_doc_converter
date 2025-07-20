"""
pytest configuration and fixtures for OCR testing

Provides test fixtures, configuration, and utilities for
comprehensive testing of the enhanced OCR system.

Author: Terry AI Agent for Terragon Labs
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Generator
import sqlite3
import json
from unittest.mock import Mock, MagicMock
from PIL import Image, ImageDraw, ImageFont
import io
import os

# Import modules under test
from security import SecurityValidator, CredentialManager
from backends import OCRBackendManager
from monitoring import CostTracker


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Fixture providing test data directory"""
    return Path(__file__).parent / "test_data"


@pytest.fixture(scope="function")
def temp_dir() -> Generator[Path, None, None]:
    """Fixture providing temporary directory for each test"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture(scope="function")
def temp_image() -> Generator[Path, None, None]:
    """Fixture providing a temporary test image with text"""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        # Create a test image with text
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a simple font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 80), "Test OCR Text", fill='black', font=font)
        img.save(tmp_file.name)
        
        yield Path(tmp_file.name)
        
        # Cleanup
        try:
            os.unlink(tmp_file.name)
        except:
            pass


@pytest.fixture(scope="function")
def temp_pdf() -> Generator[Path, None, None]:
    """Fixture providing a temporary test PDF"""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        # Create a simple PDF with text (mock)
        tmp_file.write(b"%PDF-1.4\n%Test PDF content\nendobj\n")
        
        yield Path(tmp_file.name)
        
        # Cleanup
        try:
            os.unlink(tmp_file.name)
        except:
            pass


@pytest.fixture(scope="function")
def malicious_file() -> Generator[Path, None, None]:
    """Fixture providing a potentially malicious test file"""
    with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as tmp_file:
        tmp_file.write(b"MZ\x90\x00\x03\x00\x00\x00")  # PE header
        
        yield Path(tmp_file.name)
        
        # Cleanup
        try:
            os.unlink(tmp_file.name)
        except:
            pass


@pytest.fixture(scope="function")
def large_image() -> Generator[Path, None, None]:
    """Fixture providing a large test image"""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        # Create a large image (>50MB simulated)
        img = Image.new('RGB', (4000, 3000), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((200, 1500), "Large Image Test", fill='black')
        img.save(tmp_file.name)
        
        yield Path(tmp_file.name)
        
        # Cleanup
        try:
            os.unlink(tmp_file.name)
        except:
            pass


@pytest.fixture(scope="function")
def temp_db() -> Generator[Path, None, None]:
    """Fixture providing temporary SQLite database"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        yield Path(tmp_file.name)
        
        # Cleanup
        try:
            os.unlink(tmp_file.name)
        except:
            pass


@pytest.fixture(scope="function")
def security_validator(temp_dir: Path) -> SecurityValidator:
    """Fixture providing SecurityValidator instance"""
    return SecurityValidator()


@pytest.fixture(scope="function")
def credential_manager(temp_dir: Path) -> CredentialManager:
    """Fixture providing CredentialManager instance with temp storage"""
    return CredentialManager(storage_path=str(temp_dir / "credentials.enc"))


@pytest.fixture(scope="function")
def cost_tracker(temp_db: Path) -> CostTracker:
    """Fixture providing CostTracker instance with temp database"""
    return CostTracker(db_path=str(temp_db))


@pytest.fixture(scope="function")
def mock_google_vision():
    """Mock Google Vision API client"""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.text_annotations = [
        Mock(description="Test OCR Text", locale="en")
    ]
    mock_response.full_text_annotation = Mock()
    mock_response.full_text_annotation.text = "Test OCR Text"
    mock_response.full_text_annotation.pages = [
        Mock(confidence=0.95)
    ]
    mock_client.text_detection.return_value = mock_response
    return mock_client


@pytest.fixture(scope="function")
def mock_aws_textract():
    """Mock AWS Textract client"""
    mock_client = Mock()
    mock_response = {
        'Blocks': [
            {
                'BlockType': 'LINE',
                'Text': 'Test OCR Text',
                'Confidence': 95.0
            }
        ]
    }
    mock_client.detect_document_text.return_value = mock_response
    return mock_client


@pytest.fixture(scope="function")
def mock_azure_vision():
    """Mock Azure Computer Vision client"""
    mock_client = Mock()
    mock_result = Mock()
    mock_result.read_results = [
        Mock(lines=[
            Mock(text="Test OCR Text", bounding_box=[1, 2, 3, 4])
        ])
    ]
    mock_client.read.return_value = Mock(operation_location="test://operation")
    mock_client.get_read_result.return_value = mock_result
    return mock_client


@pytest.fixture(scope="function")
def sample_credentials() -> Dict[str, Any]:
    """Sample credentials for testing"""
    return {
        'google_vision': {
            'credentials_path': '/fake/path/to/credentials.json'
        },
        'aws_textract': {
            'access_key_id': 'AKIAIOSFODNN7EXAMPLE',
            'secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            'region': 'us-east-1'
        },
        'azure_vision': {
            'subscription_key': 'fake-azure-key-12345',
            'endpoint': 'https://fake-region.api.cognitive.microsoft.com/'
        }
    }


@pytest.fixture(scope="function")
def sample_ocr_result() -> Dict[str, Any]:
    """Sample OCR result for testing"""
    return {
        'text': 'Sample extracted text from image',
        'confidence': 95.5,
        'success': True,
        'duration': 1.23,
        'backend': 'test_backend',
        'language': 'en',
        'word_count': 5,
        'line_count': 1
    }


@pytest.fixture(scope="function")
def mock_backend_manager(temp_dir: Path):
    """Mock OCR Backend Manager for testing"""
    manager = Mock(spec=OCRBackendManager)
    manager.get_available_backends.return_value = ['local', 'google_vision']
    manager.select_backend.return_value = 'local'
    manager.process_with_fallback.return_value = {
        'text': 'Test OCR Result',
        'confidence': 90.0,
        'success': True,
        'backend_used': 'local',
        'duration': 1.0
    }
    manager.get_backend_status.return_value = {
        'local': {
            'available': True,
            'type': 'local',
            'priority': 1,
            'cost_per_request': 0.0,
            'performance_stats': {}
        }
    }
    return manager


@pytest.fixture(autouse=True)
def setup_test_logging():
    """Setup logging for tests"""
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@pytest.fixture(scope="function")
def clean_environment():
    """Clean environment variables that might affect tests"""
    original_env = os.environ.copy()
    
    # Remove any OCR-related environment variables
    env_vars_to_remove = [
        'GOOGLE_APPLICATION_CREDENTIALS',
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AZURE_COGNITIVE_SERVICES_KEY'
    ]
    
    for var in env_vars_to_remove:
        if var in os.environ:
            del os.environ[var]
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


# Performance test markers
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "security: marks tests as security tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "cloud: marks tests that require cloud APIs"
    )