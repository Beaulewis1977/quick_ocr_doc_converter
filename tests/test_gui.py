"""
GUI tests for the enhanced OCR system

Tests GUI functionality, user interactions, backend integration,
and error handling for the enhanced OCR GUI application.

Author: Terry AI Agent for Terragon Labs
"""

import pytest
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock
import threading
import time
from pathlib import Path

# GUI testing requires special handling since we can't actually display windows in CI
try:
    from enhanced_ocr_gui import EnhancedOCRGUI
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    EnhancedOCRGUI = None


@pytest.mark.skipif(not GUI_AVAILABLE, reason="GUI module not available")
class TestEnhancedOCRGUI:
    """Test suite for Enhanced OCR GUI"""
    
    @pytest.fixture
    def mock_gui_dependencies(self):
        """Mock all external dependencies for GUI testing"""
        with patch('enhanced_ocr_gui.SecurityValidator') as mock_sec, \
             patch('enhanced_ocr_gui.CredentialManager') as mock_cred, \
             patch('enhanced_ocr_gui.CostTracker') as mock_cost, \
             patch('enhanced_ocr_gui.OCRBackendManager') as mock_backend:
            
            # Setup mocks
            mock_sec.return_value = Mock()
            mock_cred.return_value = Mock()
            mock_cost.return_value = Mock()
            mock_backend.return_value = Mock()
            mock_backend.return_value.get_available_backends.return_value = ['local', 'google_vision']
            
            yield {
                'security': mock_sec.return_value,
                'credentials': mock_cred.return_value,
                'cost_tracker': mock_cost.return_value,
                'backend_manager': mock_backend.return_value
            }
    
    @pytest.fixture
    def gui_app(self, mock_gui_dependencies):
        """Create GUI app for testing"""
        # Don't actually start mainloop in tests
        with patch.object(tk.Tk, 'mainloop'):
            app = EnhancedOCRGUI()
            yield app
            # Cleanup
            if hasattr(app, 'root') and app.root:
                try:
                    app.root.destroy()
                except:
                    pass
    
    def test_gui_initialization(self, mock_gui_dependencies):
        """Test GUI initialization"""
        with patch.object(tk.Tk, 'mainloop'):
            app = EnhancedOCRGUI()
            
            # Check basic initialization
            assert app.root is not None
            assert app.security_validator is not None
            assert app.credential_manager is not None
            assert app.cost_tracker is not None
            
            # Check GUI state
            assert app.processing is False
            assert app.current_files == []
            assert app.results == []
            
            app.root.destroy()
    
    def test_backend_manager_initialization(self, gui_app, mock_gui_dependencies):
        """Test backend manager initialization in GUI"""
        backend_manager = mock_gui_dependencies['backend_manager']
        
        # Should have initialized backend manager
        assert gui_app.backend_manager is not None
        backend_manager.get_available_backends.assert_called()
    
    def test_file_selection(self, gui_app, temp_image):
        """Test file selection functionality"""
        # Mock file dialog
        with patch('tkinter.filedialog.askopenfilenames') as mock_dialog:
            mock_dialog.return_value = [str(temp_image)]
            
            # Simulate file selection
            gui_app.select_files()
            
            # Check that file was added
            assert str(temp_image) in gui_app.current_files
            assert gui_app.file_listbox.size() > 0
    
    def test_file_clearing(self, gui_app, temp_image):
        """Test clearing file list"""
        # Add a file first
        gui_app.current_files.append(str(temp_image))
        gui_app.file_listbox.insert(tk.END, Path(temp_image).name)
        
        # Clear files
        gui_app.clear_files()
        
        # Check that files were cleared
        assert len(gui_app.current_files) == 0
        assert gui_app.file_listbox.size() == 0
        assert len(gui_app.results) == 0
    
    def test_backend_selection_update(self, gui_app, mock_gui_dependencies):
        """Test backend selection combo box update"""
        backend_manager = mock_gui_dependencies['backend_manager']
        backend_manager.get_available_backends.return_value = ['local', 'google_vision', 'aws_textract']
        
        # Update backend list
        gui_app.update_backend_list()
        
        # Check that combo box was updated
        values = gui_app.backend_combo['values']
        assert 'auto' in values
        assert 'local' in values
        assert 'google_vision' in values
    
    def test_processing_start_no_files(self, gui_app):
        """Test starting processing with no files"""
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            gui_app.start_processing()
            
            # Should show warning about no files
            mock_warning.assert_called_once()
            assert "No Files" in mock_warning.call_args[0][0]
    
    def test_processing_start_with_files(self, gui_app, temp_image, mock_gui_dependencies):
        """Test starting processing with files"""
        # Add file to process
        gui_app.current_files = [str(temp_image)]
        
        # Mock successful processing
        backend_manager = mock_gui_dependencies['backend_manager']
        backend_manager.process_with_fallback.return_value = {
            'text': 'Test OCR result',
            'confidence': 90.0,
            'success': True,
            'backend_used': 'local',
            'duration': 1.0
        }
        
        with patch('threading.Thread') as mock_thread:
            gui_app.start_processing()
            
            # Should start processing thread
            mock_thread.assert_called_once()
            assert gui_app.processing is True
            assert gui_app.process_btn['state'] == 'disabled'
    
    def test_processing_workflow(self, gui_app, temp_image, mock_gui_dependencies):
        """Test complete processing workflow"""
        # Setup
        gui_app.current_files = [str(temp_image)]
        backend_manager = mock_gui_dependencies['backend_manager']
        cost_tracker = mock_gui_dependencies['cost_tracker']
        security_validator = mock_gui_dependencies['security_validator']
        
        # Mock successful processing
        backend_manager.process_with_fallback.return_value = {
            'text': 'Processed OCR text',
            'confidence': 95.0,
            'success': True,
            'backend_used': 'google_vision',
            'duration': 1.5,
            'cost': 0.0015
        }
        
        # Run processing (without thread)
        gui_app.process_files()
        
        # Verify processing occurred
        backend_manager.process_with_fallback.assert_called()
        cost_tracker.track_usage.assert_called()
        
        # Check results
        assert len(gui_app.results) > 0
        result = gui_app.results[0]
        assert result['success'] is True
        assert result['text'] == 'Processed OCR text'
    
    def test_processing_with_security_validation(self, gui_app, temp_image, mock_gui_dependencies):
        """Test processing with security validation enabled"""
        # Enable security validation
        gui_app.validate_files_var.set(True)
        gui_app.current_files = [str(temp_image)]
        
        security_validator = mock_gui_dependencies['security_validator']
        backend_manager = mock_gui_dependencies['backend_manager']
        
        # Mock successful validation and processing
        backend_manager.process_with_fallback.return_value = {
            'text': 'Secure OCR result',
            'confidence': 90.0,
            'success': True,
            'backend_used': 'local'
        }
        
        # Run processing
        gui_app.process_files()
        
        # Verify security validation was called
        security_validator.validate_file_path.assert_called_with(str(temp_image))
    
    def test_processing_with_pii_masking(self, gui_app, temp_image, mock_gui_dependencies):
        """Test processing with PII masking enabled"""
        # Enable PII masking
        gui_app.pii_masking_var.set(True)
        gui_app.current_files = [str(temp_image)]
        
        security_validator = mock_gui_dependencies['security_validator']
        backend_manager = mock_gui_dependencies['backend_manager']
        
        # Mock processing result with PII
        backend_manager.process_with_fallback.return_value = {
            'text': 'John Doe, SSN: 123-45-6789',
            'confidence': 90.0,
            'success': True,
            'backend_used': 'local'
        }
        
        security_validator.sanitize_ocr_output.return_value = 'John Doe, SSN: [MASKED]'
        
        # Run processing
        gui_app.process_files()
        
        # Verify PII masking was applied
        security_validator.sanitize_ocr_output.assert_called()
        result = gui_app.results[0]
        assert result['text'] == 'John Doe, SSN: [MASKED]'
    
    def test_processing_error_handling(self, gui_app, temp_image, mock_gui_dependencies):
        """Test error handling during processing"""
        gui_app.current_files = [str(temp_image)]
        
        backend_manager = mock_gui_dependencies['backend_manager']
        # Mock processing failure
        backend_manager.process_with_fallback.side_effect = Exception("Processing failed")
        
        # Run processing
        gui_app.process_files()
        
        # Should handle error gracefully
        assert len(gui_app.results) > 0
        result = gui_app.results[0]
        assert result['success'] is False
        assert 'error' in result
    
    def test_results_display_update(self, gui_app):
        """Test updating results display"""
        result = {
            'text': 'Display test result',
            'confidence': 85.0,
            'success': True,
            'backend_used': 'google_vision'
        }
        
        # Update display
        gui_app.update_results_display(result, '/test/file.png')
        
        # Check that text was added to results
        content = gui_app.results_text.get(1.0, tk.END)
        assert 'Display test result' in content
        assert 'google_vision' in content
        assert '85.0%' in content
    
    def test_results_display_error(self, gui_app):
        """Test displaying error results"""
        error_result = {
            'text': '',
            'success': False,
            'error': 'OCR processing failed',
            'file_path': '/test/error.png'
        }
        
        # Update display
        gui_app.update_results_display(error_result, '/test/error.png')
        
        # Check that error was displayed
        content = gui_app.results_text.get(1.0, tk.END)
        assert 'ERROR' in content
        assert 'OCR processing failed' in content
    
    def test_save_results_no_results(self, gui_app):
        """Test saving results when no results exist"""
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            gui_app.save_results()
            
            # Should show warning
            mock_warning.assert_called_once()
            assert "No Results" in mock_warning.call_args[0][0]
    
    def test_save_results_json_format(self, gui_app, temp_dir):
        """Test saving results in JSON format"""
        # Add some results
        gui_app.results = [
            {
                'text': 'Test result 1',
                'confidence': 90.0,
                'success': True,
                'backend_used': 'local'
            },
            {
                'text': 'Test result 2',
                'confidence': 85.0,
                'success': True,
                'backend_used': 'google_vision'
            }
        ]
        
        gui_app.output_format_var.set('json')
        
        save_path = temp_dir / "results.json"
        
        with patch('tkinter.filedialog.asksaveasfilename') as mock_dialog, \
             patch('tkinter.messagebox.showinfo') as mock_info:
            
            mock_dialog.return_value = str(save_path)
            
            gui_app.save_results()
            
            # Check that file was saved
            assert save_path.exists()
            
            # Verify content
            import json
            with open(save_path, 'r') as f:
                saved_data = json.load(f)
            
            assert len(saved_data) == 2
            assert saved_data[0]['text'] == 'Test result 1'
            
            mock_info.assert_called_once()
    
    def test_credential_storage(self, gui_app, mock_gui_dependencies):
        """Test storing credentials from GUI"""
        credential_manager = mock_gui_dependencies['credentials']
        
        # Set credential values
        gui_app.google_creds_var.set('/path/to/google/creds.json')
        gui_app.aws_key_var.set('AKIATEST123')
        gui_app.aws_secret_var.set('secret123')
        gui_app.azure_key_var.set('azure_key_123')
        gui_app.azure_endpoint_var.set('https://test.api.cognitive.microsoft.com/')
        
        with patch('tkinter.messagebox.showinfo') as mock_info:
            gui_app.save_configuration()
            
            # Verify credentials were stored
            assert credential_manager.store_credentials.call_count >= 3
            mock_info.assert_called_once()
    
    def test_credential_loading(self, gui_app, mock_gui_dependencies):
        """Test loading credentials in GUI"""
        credential_manager = mock_gui_dependencies['credentials']
        
        # Mock stored credentials
        credential_manager.get_credentials.side_effect = lambda service: {
            'google_vision': {'credentials_path': '/stored/google/creds.json'},
            'aws_textract': {'access_key_id': 'STORED_KEY', 'secret_access_key': 'STORED_SECRET'},
            'azure_vision': {'subscription_key': 'STORED_AZURE_KEY', 'endpoint': 'https://stored.endpoint/'}
        }.get(service)
        
        with patch('tkinter.messagebox.showinfo') as mock_info:
            gui_app.load_configuration()
            
            # Verify credentials were loaded into GUI
            assert gui_app.google_creds_var.get() == '/stored/google/creds.json'
            assert '*' in gui_app.aws_key_var.get()  # Should be masked
            assert gui_app.azure_endpoint_var.get() == 'https://stored.endpoint/'
            
            mock_info.assert_called_once()
    
    def test_backend_testing(self, gui_app, mock_gui_dependencies):
        """Test backend testing functionality"""
        backend_manager = mock_gui_dependencies['backend_manager']
        backend_manager.get_backend_status.return_value = {
            'local': {'available': True},
            'google_vision': {'available': False},
            'aws_textract': {'available': True}
        }
        
        with patch('tkinter.messagebox.showinfo') as mock_info:
            gui_app.test_backends()
            
            # Should show test results
            mock_info.assert_called_once()
            message = mock_info.call_args[0][1]
            assert 'local: Available' in message
            assert 'google_vision: Not Available' in message
    
    def test_cost_stats_refresh(self, gui_app, mock_gui_dependencies):
        """Test refreshing cost statistics"""
        cost_tracker = mock_gui_dependencies['cost_tracker']
        
        # Mock cost data
        cost_tracker.get_current_month_cost.return_value = 15.50
        cost_tracker.get_current_month_requests.return_value = 150
        cost_tracker.get_backend_costs.return_value = {
            'google_vision': 10.00,
            'aws_textract': 5.50
        }
        cost_tracker.get_usage_stats.return_value = {
            'backend_stats': {
                'google_vision': {'requests': 100, 'cost_per_request': 0.1},
                'aws_textract': {'requests': 50, 'cost_per_request': 0.11}
            }
        }
        cost_tracker.get_cost_optimization_recommendations.return_value = [
            {
                'title': 'Test Recommendation',
                'description': 'This is a test recommendation',
                'potential_savings': 5.0
            }
        ]
        
        # Refresh stats
        gui_app.refresh_cost_stats()
        
        # Check that UI was updated
        assert '$15.50' in gui_app.current_cost_label['text']
        assert '150' in gui_app.current_requests_label['text']
    
    def test_backend_status_refresh(self, gui_app, mock_gui_dependencies):
        """Test refreshing backend status"""
        backend_manager = mock_gui_dependencies['backend_manager']
        backend_manager.get_backend_status.return_value = {
            'local': {
                'available': True,
                'type': 'local',
                'priority': 1,
                'cost_per_request': 0.0,
                'performance_stats': {
                    'total_requests': 100,
                    'successful_requests': 95,
                    'failed_requests': 5,
                    'avg_duration': 1.2
                }
            }
        }
        
        # Refresh status
        gui_app.refresh_backend_status()
        
        # Check that tree view was updated
        # Note: In real tests, we'd need to check the tree view content
        # For now, just verify the method ran without error
        backend_manager.get_backend_status.assert_called()
    
    def test_processing_complete_callback(self, gui_app, mock_gui_dependencies):
        """Test processing completion callback"""
        # Simulate processing state
        gui_app.processing = True
        gui_app.process_btn.config(state='disabled', text='Processing...')
        
        # Call completion callback
        gui_app.processing_complete()
        
        # Check that state was reset
        assert gui_app.processing is False
        assert gui_app.process_btn['state'] == 'normal'
        assert gui_app.process_btn['text'] == 'Start OCR Processing'
        assert gui_app.status_label['text'] == 'Complete'


@pytest.mark.skipif(not GUI_AVAILABLE, reason="GUI module not available")
class TestGUIIntegration:
    """Integration tests for GUI components"""
    
    def test_full_ocr_workflow_simulation(self, temp_image, mock_gui_dependencies):
        """Test complete OCR workflow through GUI"""
        with patch.object(tk.Tk, 'mainloop'), \
             patch('tkinter.filedialog.askopenfilenames') as mock_dialog:
            
            # Setup
            mock_dialog.return_value = [str(temp_image)]
            backend_manager = mock_gui_dependencies['backend_manager']
            backend_manager.process_with_fallback.return_value = {
                'text': 'Full workflow test result',
                'confidence': 92.0,
                'success': True,
                'backend_used': 'local',
                'duration': 1.0,
                'cost': 0.0
            }
            
            # Create app
            app = EnhancedOCRGUI()
            
            # Simulate user workflow
            # 1. Select files
            app.select_files()
            assert len(app.current_files) > 0
            
            # 2. Configure settings
            app.backend_var.set('local')
            app.language_var.set('en')
            app.high_accuracy_var.set(True)
            
            # 3. Process files
            app.process_files()
            
            # 4. Verify results
            assert len(app.results) > 0
            assert app.results[0]['success'] is True
            
            app.root.destroy()
    
    def test_error_recovery_workflow(self, temp_image, mock_gui_dependencies):
        """Test error recovery in GUI workflow"""
        with patch.object(tk.Tk, 'mainloop'), \
             patch('tkinter.filedialog.askopenfilenames') as mock_dialog:
            
            # Setup with failing backend
            mock_dialog.return_value = [str(temp_image)]
            backend_manager = mock_gui_dependencies['backend_manager']
            backend_manager.process_with_fallback.side_effect = Exception("Backend error")
            
            app = EnhancedOCRGUI()
            
            # Select file
            app.select_files()
            
            # Process (should handle error gracefully)
            app.process_files()
            
            # Should have error result
            assert len(app.results) > 0
            assert app.results[0]['success'] is False
            
            app.root.destroy()


@pytest.mark.skipif(not GUI_AVAILABLE, reason="GUI module not available")
@pytest.mark.performance
class TestGUIPerformance:
    """Performance tests for GUI components"""
    
    def test_large_file_list_performance(self, mock_gui_dependencies):
        """Test GUI performance with large file lists"""
        with patch.object(tk.Tk, 'mainloop'):
            app = EnhancedOCRGUI()
            
            # Add many files
            large_file_list = [f'/test/file_{i}.png' for i in range(100)]
            
            start_time = time.time()
            for file_path in large_file_list:
                app.current_files.append(file_path)
                app.file_listbox.insert(tk.END, Path(file_path).name)
            
            end_time = time.time()
            
            # Should complete quickly
            assert (end_time - start_time) < 1.0  # Less than 1 second
            assert len(app.current_files) == 100
            
            app.root.destroy()
    
    def test_results_display_performance(self, mock_gui_dependencies):
        """Test performance of results display with many results"""
        with patch.object(tk.Tk, 'mainloop'):
            app = EnhancedOCRGUI()
            
            # Add many results
            start_time = time.time()
            
            for i in range(50):
                result = {
                    'text': f'Performance test result {i}' * 10,  # Long text
                    'confidence': 85.0 + i % 15,
                    'success': True,
                    'backend_used': 'local'
                }
                app.update_results_display(result, f'/test/file_{i}.png')
            
            end_time = time.time()
            
            # Should complete within reasonable time
            assert (end_time - start_time) < 5.0  # Less than 5 seconds
            
            app.root.destroy()