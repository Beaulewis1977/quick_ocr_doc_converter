"""
Integration tests for the enhanced OCR system

Tests end-to-end workflows, component integration, real-world scenarios,
and system-level functionality.

Author: Terry AI Agent for Terragon Labs
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json
from pathlib import Path
import time
import threading

from security import SecurityValidator, CredentialManager
from backends import OCRBackendManager
from monitoring import CostTracker


@pytest.mark.integration
class TestSecurityIntegration:
    """Integration tests for security components"""
    
    def test_end_to_end_security_workflow(self, temp_image, temp_dir):
        """Test complete security validation workflow"""
        # Initialize security components
        validator = SecurityValidator()
        cred_manager = CredentialManager(config_dir=str(temp_dir))
        
        # Store credentials securely
        test_credentials = {
            'api_key': 'test_key_12345',
            'secret': 'very_secret_data'
        }
        
        success = cred_manager.store_credentials('test_service', test_credentials)
        assert success
        
        # Validate file security
        validator.validate_file_path(str(temp_image))
        
        # Simulate OCR result with PII
        ocr_result = "John Doe lives at 123 Main St. His SSN is 123-45-6789."
        sanitized = validator.sanitize_ocr_output(ocr_result)
        
        # Verify PII was masked
        assert "123-45-6789" not in sanitized
        
        # Retrieve credentials
        retrieved = cred_manager.get_credentials('test_service')
        assert retrieved == test_credentials
    
    def test_security_with_malicious_input(self, temp_dir):
        """Test security handling of malicious inputs"""
        validator = SecurityValidator()
        
        # Test various malicious patterns
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "<script>alert('xss')</script>",
            "../../../etc/passwd",
            "; rm -rf /",
            "{{7*7}}"
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValueError, match="Potentially malicious content detected"):
                validator.validate_input(malicious_input)
    
    def test_credential_security_audit(self, temp_dir):
        """Test credential security audit trail"""
        cred_manager = CredentialManager(config_dir=str(temp_dir))
        
        # Perform various operations
        operations = [
            ('store', 'service1', {'key': 'value1'}),
            ('store', 'service2', {'key': 'value2'}),
            ('get', 'service1', None),
            ('delete', 'service1', None),
        ]
        
        with patch('logging.Logger.info') as mock_log:
            for op, service, data in operations:
                if op == 'store':
                    cred_manager.store_credentials(service, data)
                elif op == 'get':
                    cred_manager.get_credentials(service)
                elif op == 'delete':
                    cred_manager.delete_credentials(service)
            
            # Verify audit logging occurred
            assert mock_log.call_count >= len(operations)


@pytest.mark.integration
class TestBackendIntegration:
    """Integration tests for OCR backend systems"""
    
    def test_local_backend_integration(self, temp_image):
        """Test integration with local OCR backends"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            # Mock successful local OCR
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract', 'easyocr']
            mock_instance.extract_text.return_value = {
                'text': 'Local OCR integration test',
                'confidence': 88.5
            }
            
            # Initialize manager
            manager = OCRBackendManager()
            
            # Process image
            result = manager.process_with_fallback(str(temp_image))
            
            assert result.get('success', False)
            assert 'Local OCR integration test' in result.get('text', '')
            assert result.get('backend_used') == 'local'
    
    def test_cloud_backend_integration(self, temp_image, sample_credentials):
        """Test integration with cloud OCR backends"""
        with patch('backends.manager.LocalOCREngine') as mock_local, \
             patch('backends.google_vision.vision') as mock_vision, \
             patch('backends.manager.CredentialManager') as mock_cred_manager:
            
            # Setup mocks
            mock_local.return_value.get_available_backends.return_value = []
            
            # Mock credentials
            mock_cred_manager.return_value.get_credentials.return_value = sample_credentials['google_vision']
            
            # Mock Google Vision
            mock_client = Mock()
            mock_response = Mock()
            mock_response.text_annotations = [Mock(description="Cloud OCR result")]
            mock_response.full_text_annotation = Mock(text="Cloud OCR result", pages=[Mock(confidence=0.95)])
            mock_client.text_detection.return_value = mock_response
            mock_vision.ImageAnnotatorClient.from_service_account_file.return_value = mock_client
            
            # Initialize manager with cloud backends enabled
            config = {
                'backends': {
                    'local': {'enabled': False},
                    'google_vision': {'enabled': True, 'priority': 1}
                }
            }
            
            with patch('backends.manager.OCRBackendManager._load_config') as mock_config:
                mock_config.return_value = config
                manager = OCRBackendManager()
                
                # Process image
                result = manager.process_with_fallback(str(temp_image))
                
                if result.get('success'):
                    assert 'Cloud OCR result' in result.get('text', '')
                    assert result.get('backend_used') == 'google_vision'
    
    def test_fallback_mechanism_integration(self, temp_image):
        """Test complete fallback mechanism"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            # Setup multiple backends with different behaviors
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract', 'easyocr']
            
            # First call fails, second succeeds
            mock_instance.extract_text.side_effect = [
                Exception("Primary backend failed"),
                {'text': 'Fallback success', 'confidence': 85}
            ]
            
            manager = OCRBackendManager()
            
            # Process with fallback
            result = manager.process_with_fallback(str(temp_image))
            
            # Should succeed with fallback
            if result.get('success'):
                assert result.get('used_fallback') is True
                assert 'Fallback success' in result.get('text', '')
    
    def test_backend_performance_tracking(self, temp_image):
        """Test performance tracking across backends"""
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            # Mock varying performance
            mock_instance.extract_text.side_effect = [
                {'text': 'Result 1', 'confidence': 90},
                {'text': 'Result 2', 'confidence': 85},
                Exception("Failed request"),
                {'text': 'Result 3', 'confidence': 95}
            ]
            
            manager = OCRBackendManager()
            
            # Process multiple requests
            results = []
            for i in range(4):
                result = manager.process_with_fallback(str(temp_image))
                results.append(result)
            
            # Check performance stats
            stats = manager.performance_stats.get('local', {})
            assert stats.get('total_requests', 0) >= 4
            assert stats.get('successful_requests', 0) >= 3
            assert stats.get('failed_requests', 0) >= 1


@pytest.mark.integration
class TestCostTrackingIntegration:
    """Integration tests for cost tracking system"""
    
    def test_complete_cost_tracking_workflow(self, temp_db, temp_image):
        """Test complete cost tracking workflow"""
        cost_tracker = CostTracker(db_path=str(temp_db))
        
        # Simulate various OCR operations
        operations = [
            ('local', 0.0, True, 90.0),
            ('google_vision', 0.0015, True, 95.0),
            ('google_vision', 0.0015, False, 0.0),  # Failed
            ('aws_textract', 0.002, True, 88.0),
            ('azure_vision', 0.001, True, 92.0),
            ('local', 0.0, True, 85.0),
        ]
        
        for backend, cost, success, confidence in operations:
            result = {
                'text': 'Integration test result' if success else '',
                'confidence': confidence,
                'success': success,
                'duration': 1.5
            }
            
            cost_tracker.track_usage(
                backend=backend,
                image_path=str(temp_image),
                result=result,
                cost=cost,
                image_size_mb=2.0
            )
        
        # Verify tracking
        current_cost = cost_tracker.get_current_month_cost()
        current_requests = cost_tracker.get_current_month_requests()
        
        assert current_cost >= 0.0045  # Sum of successful cloud operations
        assert current_requests >= 6
        
        # Get comprehensive stats
        stats = cost_tracker.get_usage_stats(30)
        assert stats['total_stats']['total_requests'] >= 6
        assert stats['total_stats']['successful_requests'] >= 5
        
        # Test recommendations
        recommendations = cost_tracker.get_cost_optimization_recommendations()
        assert isinstance(recommendations, list)
    
    def test_cost_tracking_with_budgets(self, temp_db):
        """Test cost tracking with budget management"""
        cost_tracker = CostTracker(db_path=str(temp_db))
        
        # Set budgets
        cost_tracker.set_monthly_budget('google_vision', 10.0)
        cost_tracker.set_monthly_budget('aws_textract', 15.0)
        
        # Simulate usage approaching budgets
        for i in range(8):  # $0.012 for Google Vision
            result = {'text': 'Budget test', 'confidence': 90, 'success': True, 'duration': 1.0}
            cost_tracker.track_usage('google_vision', f'/test/budget_{i}.png', result, 0.0015)
        
        for i in range(6):  # $0.012 for AWS Textract
            result = {'text': 'Budget test', 'confidence': 88, 'success': True, 'duration': 1.5}
            cost_tracker.track_usage('aws_textract', f'/test/budget_{i}.pdf', result, 0.002)
        
        # Check budget alerts
        alerts = cost_tracker.check_budget_alerts()
        
        # Should not have alerts yet (usage is low)
        budget_exceeded = [alert for alert in alerts if alert.get('type') == 'budget_exceeded']
        assert len(budget_exceeded) == 0
    
    def test_cost_optimization_recommendations_integration(self, temp_db):
        """Test cost optimization recommendations generation"""
        cost_tracker = CostTracker(db_path=str(temp_db))
        
        # Simulate expensive, low-accuracy usage
        for i in range(15):
            result = {
                'text': 'Expensive low quality',
                'confidence': 65.0,  # Low confidence
                'success': True,
                'duration': 3.0  # Slow processing
            }
            cost_tracker.track_usage('aws_textract', f'/test/expensive_{i}.png', result, 0.005)
        
        # Simulate good local usage
        for i in range(20):
            result = {
                'text': 'Good local result',
                'confidence': 88.0,
                'success': True,
                'duration': 1.0
            }
            cost_tracker.track_usage('local', f'/test/local_{i}.png', result, 0.0)
        
        # Get recommendations
        recommendations = cost_tracker.get_cost_optimization_recommendations()
        
        # Should recommend cost reduction and accuracy improvement
        rec_types = [rec.get('type') for rec in recommendations]
        assert 'cost_reduction' in rec_types or 'accuracy_vs_cost' in rec_types


@pytest.mark.integration
class TestFullSystemIntegration:
    """End-to-end system integration tests"""
    
    def test_complete_ocr_pipeline(self, temp_image, temp_dir):
        """Test complete OCR processing pipeline"""
        # Initialize all components
        security_validator = SecurityValidator()
        cred_manager = CredentialManager(config_dir=str(temp_dir))
        cost_tracker = CostTracker(db_path=str(temp_dir / "pipeline_costs.db"))
        
        with patch('backends.manager.LocalOCREngine') as mock_local:
            # Setup local backend
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            mock_instance.extract_text.return_value = {
                'text': 'Complete pipeline test result',
                'confidence': 92.5
            }
            
            # Initialize backend manager
            manager = OCRBackendManager()
            
            # Step 1: Security validation
            security_validator.validate_file_path(str(temp_image))
            
            # Step 2: OCR processing
            result = manager.process_with_fallback(str(temp_image))
            
            # Step 3: Cost tracking
            cost = 0.0  # Local backend is free
            cost_tracker.track_usage(
                backend=result.get('backend_used', 'unknown'),
                image_path=str(temp_image),
                result=result,
                cost=cost,
                image_size_mb=1.0
            )
            
            # Step 4: Output sanitization
            if result.get('success'):
                sanitized_text = security_validator.sanitize_ocr_output(result['text'])
                result['sanitized_text'] = sanitized_text
            
            # Verify pipeline results
            assert result.get('success', False)
            assert 'Complete pipeline test result' in result.get('text', '')
            assert 'sanitized_text' in result
            
            # Verify cost tracking
            tracked_cost = cost_tracker.get_current_month_cost()
            assert tracked_cost >= 0  # Should be 0 for local backend
    
    def test_multi_backend_workflow_with_fallback(self, temp_image, temp_dir, sample_credentials):
        """Test workflow with multiple backends and fallback"""
        # Initialize components
        cost_tracker = CostTracker(db_path=str(temp_dir / "multibackend_costs.db"))
        
        with patch('backends.manager.LocalOCREngine') as mock_local, \
             patch('backends.google_vision.vision') as mock_vision, \
             patch('backends.manager.CredentialManager') as mock_cred_manager:
            
            # Setup local backend to fail
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            mock_local.return_value.extract_text.side_effect = Exception("Local backend failed")
            
            # Setup Google Vision as fallback
            mock_cred_manager.return_value.get_credentials.return_value = sample_credentials['google_vision']
            mock_client = Mock()
            mock_response = Mock()
            mock_response.text_annotations = [Mock(description="Fallback OCR success")]
            mock_response.full_text_annotation = Mock(text="Fallback OCR success", pages=[Mock(confidence=0.93)])
            mock_client.text_detection.return_value = mock_response
            mock_vision.ImageAnnotatorClient.from_service_account_file.return_value = mock_client
            
            # Configure for fallback
            config = {
                'backends': {
                    'local': {'enabled': True, 'priority': 1},
                    'google_vision': {'enabled': True, 'priority': 2}
                },
                'fallback_enabled': True
            }
            
            with patch('backends.manager.OCRBackendManager._load_config') as mock_config:
                mock_config.return_value = config
                manager = OCRBackendManager()
                
                # Process with fallback
                result = manager.process_with_fallback(str(temp_image))
                
                if result.get('success'):
                    # Should have used fallback
                    assert result.get('used_fallback') is True
                    assert result.get('backend_used') == 'google_vision'
                    
                    # Track the cost
                    cost = 0.0015  # Google Vision cost
                    cost_tracker.track_usage(
                        backend=result['backend_used'],
                        image_path=str(temp_image),
                        result=result,
                        cost=cost
                    )
                    
                    # Verify cost was tracked
                    tracked_cost = cost_tracker.get_current_month_cost()
                    assert tracked_cost >= cost
    
    def test_high_volume_processing_simulation(self, temp_image, temp_dir):
        """Test system behavior under high volume processing"""
        cost_tracker = CostTracker(db_path=str(temp_dir / "highvolume_costs.db"))
        
        with patch('backends.manager.LocalOCREngine') as mock_local:
            # Setup local backend for high volume
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            # Mock varying results
            results = []
            for i in range(50):
                if i % 10 == 0:  # 10% failure rate
                    results.append(Exception(f"Processing failed for request {i}"))
                else:
                    results.append({
                        'text': f'High volume result {i}',
                        'confidence': 80.0 + (i % 20)  # Varying confidence
                    })
            
            mock_instance.extract_text.side_effect = results
            
            manager = OCRBackendManager()
            
            # Process many requests
            start_time = time.time()
            processed_results = []
            
            for i in range(50):
                result = manager.process_with_fallback(str(temp_image))
                processed_results.append(result)
                
                # Track each result
                cost = 0.0  # Local backend
                cost_tracker.track_usage(
                    backend=result.get('backend_used', 'local'),
                    image_path=str(temp_image),
                    result=result,
                    cost=cost
                )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Verify performance
            assert processing_time < 30.0  # Should complete within 30 seconds
            
            # Verify results
            successful_results = [r for r in processed_results if r.get('success')]
            assert len(successful_results) >= 40  # At least 80% success rate
            
            # Verify cost tracking
            stats = cost_tracker.get_usage_stats(30)
            assert stats['total_stats']['total_requests'] >= 50
    
    def test_concurrent_processing_safety(self, temp_image, temp_dir):
        """Test system safety under concurrent processing"""
        cost_tracker = CostTracker(db_path=str(temp_dir / "concurrent_costs.db"))
        
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            mock_instance.extract_text.return_value = {
                'text': 'Concurrent processing result',
                'confidence': 87.5
            }
            
            manager = OCRBackendManager()
            
            results = []
            errors = []
            
            def process_file(file_id):
                try:
                    result = manager.process_with_fallback(str(temp_image))
                    results.append(result)
                    
                    # Track cost
                    cost_tracker.track_usage(
                        backend=result.get('backend_used', 'local'),
                        image_path=str(temp_image),
                        result=result,
                        cost=0.0
                    )
                except Exception as e:
                    errors.append(e)
            
            # Start multiple threads
            threads = []
            for i in range(10):
                thread = threading.Thread(target=process_file, args=(i,))
                threads.append(thread)
                thread.start()
            
            # Wait for completion
            for thread in threads:
                thread.join(timeout=10)
            
            # Verify concurrent processing
            assert len(errors) == 0  # No errors should occur
            assert len(results) == 10  # All threads should complete
            
            # Verify cost tracking integrity
            tracked_requests = cost_tracker.get_current_month_requests()
            assert tracked_requests >= 10
    
    def test_error_recovery_and_resilience(self, temp_image, temp_dir):
        """Test system error recovery and resilience"""
        security_validator = SecurityValidator()
        cost_tracker = CostTracker(db_path=str(temp_dir / "resilience_costs.db"))
        
        with patch('backends.manager.LocalOCREngine') as mock_local:
            # Setup backend that fails intermittently
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            
            # Alternate between success and failure
            mock_instance.extract_text.side_effect = [
                Exception("Temporary failure 1"),
                {'text': 'Recovery success 1', 'confidence': 90},
                Exception("Temporary failure 2"),
                {'text': 'Recovery success 2', 'confidence': 85},
                Exception("Temporary failure 3"),
                {'text': 'Recovery success 3', 'confidence': 88}
            ]
            
            manager = OCRBackendManager()
            
            # Process with error recovery
            successful_recoveries = 0
            total_attempts = 6
            
            for i in range(total_attempts):
                try:
                    # Security validation (should always pass for valid file)
                    security_validator.validate_file_path(str(temp_image))
                    
                    # OCR processing (may fail)
                    result = manager.process_with_fallback(str(temp_image))
                    
                    if result.get('success'):
                        successful_recoveries += 1
                        
                        # Track successful operations
                        cost_tracker.track_usage(
                            backend=result.get('backend_used', 'local'),
                            image_path=str(temp_image),
                            result=result,
                            cost=0.0
                        )
                    
                except Exception as e:
                    # System should handle errors gracefully
                    assert False, f"Unhandled system error: {e}"
            
            # Verify resilience
            assert successful_recoveries >= 3  # Should recover from failures
            
            # Verify cost tracking continued during errors
            stats = cost_tracker.get_usage_stats(30)
            assert stats['total_stats']['total_requests'] >= successful_recoveries


@pytest.mark.integration
@pytest.mark.performance
class TestPerformanceIntegration:
    """Performance integration tests"""
    
    def test_memory_usage_under_load(self, temp_image, temp_dir):
        """Test memory usage during heavy processing"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        cost_tracker = CostTracker(db_path=str(temp_dir / "memory_costs.db"))
        
        with patch('backends.manager.LocalOCREngine') as mock_local:
            mock_instance = Mock()
            mock_local.return_value = mock_instance
            mock_local.return_value.get_available_backends.return_value = ['tesseract']
            mock_instance.extract_text.return_value = {
                'text': 'Memory test result' * 100,  # Large text
                'confidence': 90.0
            }
            
            manager = OCRBackendManager()
            
            # Process many files
            for i in range(100):
                result = manager.process_with_fallback(str(temp_image))
                cost_tracker.track_usage(
                    backend=result.get('backend_used', 'local'),
                    image_path=str(temp_image),
                    result=result,
                    cost=0.0
                )
            
            final_memory = process.memory_info().rss
            memory_increase = final_memory - initial_memory
            
            # Memory increase should be reasonable (less than 100MB)
            assert memory_increase < 100 * 1024 * 1024  # 100MB
    
    def test_database_performance_under_load(self, temp_dir):
        """Test database performance with many cost tracking operations"""
        cost_tracker = CostTracker(db_path=str(temp_dir / "db_performance.db"))
        
        start_time = time.time()
        
        # Perform many database operations
        for i in range(1000):
            result = {
                'text': f'DB performance test {i}',
                'confidence': 85.0 + (i % 15),
                'success': True,
                'duration': 1.0 + (i % 3)
            }
            
            cost_tracker.track_usage(
                backend='local',
                image_path=f'/test/db_perf_{i}.png',
                result=result,
                cost=0.0
            )
        
        # Get statistics (database query)
        stats = cost_tracker.get_usage_stats(30)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should complete within reasonable time
        assert total_time < 10.0  # 10 seconds for 1000 operations
        assert stats['total_stats']['total_requests'] >= 1000