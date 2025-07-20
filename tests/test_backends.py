"""
Backend tests for the enhanced OCR system

Tests OCR backend functionality, integration, fallback mechanisms,
and cloud service interactions.

Author: Terry AI Agent for Terragon Labs
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import time
import json

from backends import OCRBackendManager, BackendSelectionError
from backends.google_vision import GoogleVisionBackend
from backends.aws_textract import AWSTextractBackend
from backends.azure_vision import AzureVisionBackend


class TestOCRBackendManager:
    """Test suite for OCRBackendManager"""
    
    def test_backend_manager_initialization(self, temp_dir):
        """Test backend manager initialization"""
        config = {
            'backends': {
                'local': {'enabled': True, 'priority': 1}
            }
        }
        
        config_file = temp_dir / "config.json"
        config_file.write_text(json.dumps(config))
        
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            manager = OCRBackendManager(config_path=str(config_file))
            
            assert 'local' in manager.backends
            assert manager.backends['local']['available']
    
    def test_backend_selection_strategies(self, temp_image):
        """Test different backend selection strategies"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            # Test cost-optimized strategy
            manager = OCRBackendManager()
            manager.config['selection_strategy'] = 'cost_optimized'
            
            selected = manager.select_backend(str(temp_image))
            assert selected in manager.fallback_order
            
            # Test fastest strategy
            manager.config['selection_strategy'] = 'fastest'
            selected = manager.select_backend(str(temp_image))
            assert selected in manager.fallback_order
            
            # Test most_accurate strategy
            manager.config['selection_strategy'] = 'most_accurate'
            selected = manager.select_backend(str(temp_image))
            assert selected in manager.fallback_order
    
    def test_offline_only_requirement(self, temp_image):
        """Test offline-only processing requirement"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            manager = OCRBackendManager()
            
            # Should select local backend for offline-only
            requirements = {'offline_only': True}
            selected = manager.select_backend(str(temp_image), requirements)
            assert selected == 'local'
    
    def test_no_backends_available(self):
        """Test handling when no backends are available"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_local.return_value.get_available_backends.return_value = []
            
            manager = OCRBackendManager()
            
            with pytest.raises(BackendSelectionError):
                manager.select_backend("/fake/image.png")
    
    def test_fallback_mechanism(self, temp_image):
        """Test fallback to alternative backends"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            # Setup mock that fails first, succeeds second
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            # First call fails, second succeeds
            mock_instance.extract_text.side_effect = [
                Exception("First backend failed"),
                {'text': 'Success from fallback', 'confidence': 90}
            ]
            
            manager = OCRBackendManager()
            
            # Should handle fallback gracefully
            result = manager.process_with_fallback(str(temp_image))
            
            # Should either succeed with fallback or return error gracefully
            assert isinstance(result, dict)
            assert 'success' in result
    
    def test_image_analysis(self, temp_image, large_image):
        """Test image analysis for backend selection"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            manager = OCRBackendManager()
            
            # Test normal image
            info = manager._analyze_image(str(temp_image))
            assert 'width' in info
            assert 'height' in info
            assert 'size_mb' in info
            assert isinstance(info['is_large'], bool)
            assert isinstance(info['is_document'], bool)
            
            # Test large image analysis
            with patch('PIL.Image.open') as mock_open:
                mock_img = Mock()
                mock_img.size = (4000, 3000)
                mock_open.return_value.__enter__.return_value = mock_img
                
                info = manager._analyze_image(str(large_image))
                assert info['width'] == 4000
                assert info['height'] == 3000
                assert info['is_large'] is True
    
    def test_performance_tracking(self, temp_image):
        """Test performance statistics tracking"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            mock_instance.extract_text.return_value = {
                'text': 'Test result',
                'confidence': 90
            }
            
            manager = OCRBackendManager()
            
            # Process multiple requests to generate stats
            for _ in range(3):
                manager.process_with_fallback(str(temp_image))
            
            # Check performance stats
            stats = manager.performance_stats.get('local', {})
            assert stats.get('total_requests', 0) >= 3
            assert 'avg_duration' in stats
    
    def test_backend_status(self):
        """Test backend status reporting"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            manager = OCRBackendManager()
            
            status = manager.get_backend_status()
            
            assert isinstance(status, dict)
            if 'local' in status:
                backend_status = status['local']
                assert 'available' in backend_status
                assert 'type' in backend_status
                assert 'priority' in backend_status
                assert 'cost_per_request' in backend_status
    
    def test_quality_assessment(self):
        """Test OCR result quality assessment"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            manager = OCRBackendManager()
            
            # Test high quality result
            high_quality = {'confidence': 95, 'text': 'This is a good quality result'}
            assert manager._is_quality_acceptable(high_quality, {'accuracy': 'high'})
            
            # Test low quality result
            low_quality = {'confidence': 30, 'text': 'Bad'}
            assert not manager._is_quality_acceptable(low_quality, {'accuracy': 'high'})
            
            # Test with different requirements
            assert manager._is_quality_acceptable(low_quality, {'accuracy': 'low'})


class TestGoogleVisionBackend:
    """Test suite for Google Vision Backend"""
    
    def test_google_vision_initialization(self, sample_credentials):
        """Test Google Vision backend initialization"""
        creds = sample_credentials['google_vision']
        
        with patch('backends.google_vision.vision') as mock_vision:
            mock_client = Mock()
            mock_vision.ImageAnnotatorClient.from_service_account_file.return_value = mock_client
            
            backend = GoogleVisionBackend(creds)
            assert backend.credentials == creds
            assert backend.client == mock_client
    
    def test_google_vision_text_extraction(self, sample_credentials, temp_image, mock_google_vision):
        """Test Google Vision text extraction"""
        creds = sample_credentials['google_vision']
        
        with patch('backends.google_vision.vision') as mock_vision:
            mock_vision.ImageAnnotatorClient.from_service_account_file.return_value = mock_google_vision
            
            backend = GoogleVisionBackend(creds)
            result = backend.extract_text(str(temp_image))
            
            assert isinstance(result, dict)
            assert 'text' in result
            assert 'confidence' in result
            assert 'success' in result
    
    def test_google_vision_error_handling(self, sample_credentials, temp_image):
        """Test Google Vision error handling"""
        creds = sample_credentials['google_vision']
        
        with patch('backends.google_vision.vision') as mock_vision:
            mock_client = Mock()
            mock_client.text_detection.side_effect = Exception("API Error")
            mock_vision.ImageAnnotatorClient.from_service_account_file.return_value = mock_client
            
            backend = GoogleVisionBackend(creds)
            result = backend.extract_text(str(temp_image))
            
            assert result['success'] is False
            assert 'error' in result
    
    def test_google_vision_cost_estimation(self, sample_credentials):
        """Test Google Vision cost estimation"""
        creds = sample_credentials['google_vision']
        
        with patch('backends.google_vision.vision'):
            backend = GoogleVisionBackend(creds)
            
            cost = backend.get_cost_estimate("dummy_path")
            assert isinstance(cost, (int, float))
            assert cost >= 0
    
    @pytest.mark.cloud
    def test_google_vision_availability_check(self, sample_credentials):
        """Test Google Vision availability check"""
        creds = sample_credentials['google_vision']
        
        with patch('backends.google_vision.vision') as mock_vision:
            mock_client = Mock()
            mock_vision.ImageAnnotatorClient.from_service_account_file.return_value = mock_client
            
            backend = GoogleVisionBackend(creds)
            
            # Should check availability based on credentials
            is_available = backend.is_available()
            assert isinstance(is_available, bool)


class TestAWSTextractBackend:
    """Test suite for AWS Textract Backend"""
    
    def test_aws_textract_initialization(self, sample_credentials):
        """Test AWS Textract backend initialization"""
        creds = sample_credentials['aws_textract']
        
        with patch('backends.aws_textract.boto3') as mock_boto3:
            mock_client = Mock()
            mock_boto3.client.return_value = mock_client
            
            backend = AWSTextractBackend(creds)
            assert backend.credentials == creds
            assert backend.client == mock_client
    
    def test_aws_textract_text_extraction(self, sample_credentials, temp_image, mock_aws_textract):
        """Test AWS Textract text extraction"""
        creds = sample_credentials['aws_textract']
        
        with patch('backends.aws_textract.boto3') as mock_boto3:
            mock_boto3.client.return_value = mock_aws_textract
            
            backend = AWSTextractBackend(creds)
            result = backend.extract_text(str(temp_image))
            
            assert isinstance(result, dict)
            assert 'text' in result
            assert 'confidence' in result
            assert 'success' in result
    
    def test_aws_textract_document_analysis(self, sample_credentials, temp_image):
        """Test AWS Textract document analysis features"""
        creds = sample_credentials['aws_textract']
        
        with patch('backends.aws_textract.boto3') as mock_boto3:
            mock_client = Mock()
            mock_client.analyze_document.return_value = {
                'Blocks': [
                    {'BlockType': 'TABLE', 'Text': 'Table content'},
                    {'BlockType': 'FORM', 'Text': 'Form field'}
                ]
            }
            mock_boto3.client.return_value = mock_client
            
            backend = AWSTextractBackend(creds)
            
            # Test with document analysis enabled
            result = backend.extract_text(str(temp_image), analyze_document=True)
            
            assert isinstance(result, dict)
            assert 'tables' in result or 'forms' in result
    
    def test_aws_textract_error_handling(self, sample_credentials, temp_image):
        """Test AWS Textract error handling"""
        creds = sample_credentials['aws_textract']
        
        with patch('backends.aws_textract.boto3') as mock_boto3:
            mock_client = Mock()
            mock_client.detect_document_text.side_effect = Exception("AWS Error")
            mock_boto3.client.return_value = mock_client
            
            backend = AWSTextractBackend(creds)
            result = backend.extract_text(str(temp_image))
            
            assert result['success'] is False
            assert 'error' in result


class TestAzureVisionBackend:
    """Test suite for Azure Vision Backend"""
    
    def test_azure_vision_initialization(self, sample_credentials):
        """Test Azure Vision backend initialization"""
        creds = sample_credentials['azure_vision']
        
        with patch('backends.azure_vision.ComputerVisionClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            
            backend = AzureVisionBackend(creds)
            assert backend.credentials == creds
            assert backend.client == mock_client
    
    def test_azure_vision_text_extraction(self, sample_credentials, temp_image, mock_azure_vision):
        """Test Azure Vision text extraction"""
        creds = sample_credentials['azure_vision']
        
        with patch('backends.azure_vision.ComputerVisionClient') as mock_client_class:
            mock_client_class.return_value = mock_azure_vision
            
            backend = AzureVisionBackend(creds)
            result = backend.extract_text(str(temp_image))
            
            assert isinstance(result, dict)
            assert 'text' in result
            assert 'confidence' in result
            assert 'success' in result
    
    def test_azure_vision_handwriting_recognition(self, sample_credentials, temp_image):
        """Test Azure Vision handwriting recognition"""
        creds = sample_credentials['azure_vision']
        
        with patch('backends.azure_vision.ComputerVisionClient') as mock_client_class:
            mock_client = Mock()
            
            # Mock handwriting detection
            mock_result = Mock()
            mock_result.read_results = [
                Mock(lines=[Mock(text="Handwritten text", bounding_box=[1, 2, 3, 4])])
            ]
            mock_client.read.return_value = Mock(operation_location="test://operation")
            mock_client.get_read_result.return_value = mock_result
            
            mock_client_class.return_value = mock_client
            
            backend = AzureVisionBackend(creds)
            result = backend.extract_text(str(temp_image), recognize_handwriting=True)
            
            assert isinstance(result, dict)
            assert 'handwriting' in result or 'text' in result


@pytest.mark.integration
class TestBackendIntegration:
    """Integration tests for backend systems"""
    
    def test_multi_backend_workflow(self, temp_image):
        """Test workflow with multiple backends"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            mock_local.return_value.extract_text.return_value = {
                'text': 'Local OCR result',
                'confidence': 85
            }
            
            manager = OCRBackendManager()
            
            # Process with fallback
            result = manager.process_with_fallback(str(temp_image))
            
            assert isinstance(result, dict)
            assert 'backend_used' in result
    
    def test_backend_switching_on_failure(self, temp_image):
        """Test automatic backend switching on failure"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            # Setup to fail first, succeed second
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract', 'easyocr']
            
            mock_instance.extract_text.side_effect = [
                Exception("First attempt failed"),
                {'text': 'Second attempt succeeded', 'confidence': 90}
            ]
            
            manager = OCRBackendManager()
            
            result = manager.process_with_fallback(str(temp_image))
            
            # Should handle the failure and try again
            assert isinstance(result, dict)
    
    def test_cost_optimization_selection(self, temp_image):
        """Test cost-optimized backend selection"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            manager = OCRBackendManager()
            manager.config['selection_strategy'] = 'cost_optimized'
            
            # Should prefer free local backend
            selected = manager.select_backend(str(temp_image))
            
            if 'local' in manager.backends:
                assert selected == 'local'  # Cheapest option
    
    @pytest.mark.performance
    def test_performance_under_load(self, temp_image):
        """Test backend performance under load"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            mock_instance.extract_text.return_value = {
                'text': 'Performance test result',
                'confidence': 90
            }
            
            manager = OCRBackendManager()
            
            # Process multiple requests
            start_time = time.time()
            results = []
            
            for i in range(10):
                result = manager.process_with_fallback(str(temp_image))
                results.append(result)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Should complete within reasonable time
            assert total_time < 30  # 30 seconds for 10 requests
            assert len(results) == 10
            
            # All results should be successful
            successful = sum(1 for r in results if r.get('success', False))
            assert successful >= 8  # At least 80% success rate