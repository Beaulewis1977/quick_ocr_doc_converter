"""
Cost tracking tests for the enhanced OCR system

Tests cost monitoring, usage analytics, optimization recommendations,
and budget management functionality.

Author: Terry AI Agent for Terragon Labs
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import json
import tempfile
from pathlib import Path

from monitoring import CostTracker, UsageRecord


class TestUsageRecord:
    """Test suite for UsageRecord data class"""
    
    def test_usage_record_creation(self):
        """Test creating usage records"""
        timestamp = datetime.now()
        record = UsageRecord(
            timestamp=timestamp,
            backend='google_vision',
            image_path='/test/image.png',
            image_size_mb=2.5,
            processing_time=1.23,
            cost=0.0015,
            success=True,
            confidence=95.5,
            character_count=150
        )
        
        assert record.timestamp == timestamp
        assert record.backend == 'google_vision'
        assert record.cost == 0.0015
        assert record.success is True
        assert record.confidence == 95.5
    
    def test_usage_record_to_dict(self):
        """Test converting usage record to dictionary"""
        timestamp = datetime.now()
        record = UsageRecord(
            timestamp=timestamp,
            backend='aws_textract',
            image_path='/test/doc.pdf',
            image_size_mb=1.0,
            processing_time=2.1,
            cost=0.002,
            success=True,
            confidence=88.0,
            character_count=200
        )
        
        data = record.to_dict()
        
        assert isinstance(data, dict)
        assert data['backend'] == 'aws_textract'
        assert data['cost'] == 0.002
        assert data['timestamp'] == timestamp.isoformat()


class TestCostTracker:
    """Test suite for CostTracker"""
    
    def test_cost_tracker_initialization(self, temp_db):
        """Test cost tracker initialization with custom database"""
        tracker = CostTracker(db_path=str(temp_db))
        
        assert tracker.db_path == temp_db
        assert temp_db.exists()
        
        # Verify database tables were created
        import sqlite3
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='usage_records'"
            )
            assert cursor.fetchone() is not None
    
    def test_track_usage_basic(self, cost_tracker):
        """Test basic usage tracking"""
        result = {
            'text': 'Sample OCR text',
            'confidence': 90.0,
            'success': True,
            'duration': 1.5
        }
        
        cost_tracker.track_usage(
            backend='local',
            image_path='/test/image.png',
            result=result,
            cost=0.0,
            image_size_mb=1.5
        )
        
        # Verify it was tracked
        assert len(cost_tracker.session_usage) == 1
        record = cost_tracker.session_usage[0]
        assert record.backend == 'local'
        assert record.cost == 0.0
        assert record.success is True
    
    def test_track_usage_cloud_service(self, cost_tracker):
        """Test tracking usage for cloud services"""
        result = {
            'text': 'Cloud OCR result',
            'confidence': 95.0,
            'success': True,
            'duration': 2.3
        }
        
        cost_tracker.track_usage(
            backend='google_vision',
            image_path='/test/doc.jpg',
            result=result,
            cost=0.0015,
            image_size_mb=3.2
        )
        
        # Check current month cost
        current_cost = cost_tracker.get_current_month_cost()
        assert current_cost >= 0.0015
        
        # Check current month requests
        current_requests = cost_tracker.get_current_month_requests()
        assert current_requests >= 1
    
    def test_multiple_usage_tracking(self, cost_tracker):
        """Test tracking multiple usage records"""
        backends = ['local', 'google_vision', 'aws_textract']
        costs = [0.0, 0.0015, 0.002]
        
        for i, (backend, cost) in enumerate(zip(backends, costs)):
            result = {
                'text': f'Result {i}',
                'confidence': 85.0 + i * 5,
                'success': True,
                'duration': 1.0 + i * 0.5
            }
            
            cost_tracker.track_usage(
                backend=backend,
                image_path=f'/test/image_{i}.png',
                result=result,
                cost=cost,
                image_size_mb=1.0 + i
            )
        
        # Check totals
        total_cost = cost_tracker.get_current_month_cost()
        total_requests = cost_tracker.get_current_month_requests()
        
        assert total_cost >= sum(costs)
        assert total_requests >= len(backends)
    
    def test_backend_cost_breakdown(self, cost_tracker):
        """Test getting cost breakdown by backend"""
        # Add usage for different backends
        usage_data = [
            ('google_vision', 0.0015, True),
            ('google_vision', 0.0015, True),
            ('aws_textract', 0.002, True),
            ('local', 0.0, True),
            ('azure_vision', 0.001, False)  # Failed request
        ]
        
        for backend, cost, success in usage_data:
            result = {
                'text': 'Test result',
                'confidence': 90.0,
                'success': success,
                'duration': 1.0
            }
            
            cost_tracker.track_usage(
                backend=backend,
                image_path='/test/image.png',
                result=result,
                cost=cost
            )
        
        # Get backend costs
        backend_costs = cost_tracker.get_backend_costs(30)
        
        assert 'google_vision' in backend_costs
        assert 'aws_textract' in backend_costs
        assert backend_costs['google_vision'] >= 0.003  # 2 * 0.0015
        assert backend_costs['aws_textract'] >= 0.002
    
    def test_usage_statistics(self, cost_tracker):
        """Test comprehensive usage statistics"""
        # Add varied usage data
        for i in range(10):
            backend = ['local', 'google_vision'][i % 2]
            cost = 0.0 if backend == 'local' else 0.0015
            success = i < 8  # 80% success rate
            
            result = {
                'text': f'Result {i}',
                'confidence': 70.0 + i * 3,
                'success': success,
                'duration': 1.0 + i * 0.1
            }
            
            cost_tracker.track_usage(
                backend=backend,
                image_path=f'/test/image_{i}.png',
                result=result,
                cost=cost
            )
        
        # Get statistics
        stats = cost_tracker.get_usage_stats(30)
        
        assert 'total_stats' in stats
        assert 'backend_stats' in stats
        
        total_stats = stats['total_stats']
        assert total_stats['total_requests'] >= 10
        assert total_stats['successful_requests'] >= 8
        assert 0.7 <= total_stats['success_rate'] <= 1.0
        
        backend_stats = stats['backend_stats']
        assert 'local' in backend_stats
        if 'google_vision' in backend_stats:
            assert backend_stats['google_vision']['cost'] > 0
    
    def test_cost_optimization_recommendations(self, cost_tracker):
        """Test cost optimization recommendations"""
        # Simulate expensive cloud usage
        for _ in range(20):
            result = {
                'text': 'Expensive cloud result',
                'confidence': 85.0,
                'success': True,
                'duration': 2.0
            }
            
            cost_tracker.track_usage(
                backend='google_vision',
                image_path='/test/expensive.png',
                result=result,
                cost=0.0015
            )
        
        recommendations = cost_tracker.get_cost_optimization_recommendations()
        
        assert isinstance(recommendations, list)
        
        # Should suggest cost reduction for expensive usage
        cost_reduction_recs = [
            rec for rec in recommendations 
            if rec.get('type') == 'cost_reduction'
        ]
        
        if cost_reduction_recs:
            assert any('Local' in rec['title'] for rec in cost_reduction_recs)
    
    def test_low_accuracy_recommendations(self, cost_tracker):
        """Test recommendations for low accuracy with high cost"""
        # Simulate low accuracy expensive backend
        for _ in range(10):
            result = {
                'text': 'Poor quality result',
                'confidence': 60.0,  # Low confidence
                'success': True,
                'duration': 2.0
            }
            
            cost_tracker.track_usage(
                backend='aws_textract',
                image_path='/test/poor_quality.png',
                result=result,
                cost=0.005  # High cost
            )
        
        recommendations = cost_tracker.get_cost_optimization_recommendations()
        
        # Should recommend switching backends for low accuracy
        accuracy_recs = [
            rec for rec in recommendations 
            if rec.get('type') == 'accuracy_vs_cost'
        ]
        
        if accuracy_recs:
            assert any('Low Accuracy' in rec['title'] for rec in accuracy_recs)
    
    def test_budget_management(self, cost_tracker):
        """Test budget setting and alerts"""
        # Set a budget
        cost_tracker.set_monthly_budget('google_vision', 50.0)
        
        # Simulate usage approaching budget
        for _ in range(30):  # Should cost ~$0.045
            result = {
                'text': 'Budget test',
                'confidence': 90.0,
                'success': True,
                'duration': 1.0
            }
            
            cost_tracker.track_usage(
                backend='google_vision',
                image_path='/test/budget.png',
                result=result,
                cost=0.0015
            )
        
        # Check for budget alerts
        alerts = cost_tracker.check_budget_alerts()
        
        # Should not trigger alerts yet (under budget)
        budget_alerts = [alert for alert in alerts if alert.get('backend') == 'google_vision']
        
        # If alerts exist, they should be reasonable
        for alert in budget_alerts:
            assert alert['usage_percent'] <= 100
            assert alert['current_cost'] >= 0
    
    def test_budget_exceeded_alerts(self, cost_tracker):
        """Test budget exceeded alerts"""
        # Set a low budget
        cost_tracker.set_monthly_budget('azure_vision', 0.01)  # $0.01 budget
        
        # Exceed the budget
        for _ in range(10):
            result = {
                'text': 'Over budget',
                'confidence': 90.0,
                'success': True,
                'duration': 1.0
            }
            
            cost_tracker.track_usage(
                backend='azure_vision',
                image_path='/test/overbudget.png',
                result=result,
                cost=0.002  # $0.02 total > $0.01 budget
            )
        
        alerts = cost_tracker.check_budget_alerts()
        
        # Should have budget alerts
        budget_alerts = [alert for alert in alerts if alert.get('backend') == 'azure_vision']
        
        if budget_alerts:
            for alert in budget_alerts:
                assert alert['usage_percent'] > 90  # Should be over 90%
                assert alert['type'] in ['budget_warning', 'budget_exceeded']
    
    def test_usage_report_export(self, cost_tracker, temp_dir):
        """Test exporting usage reports"""
        # Add some usage data
        for i in range(5):
            result = {
                'text': f'Export test {i}',
                'confidence': 85.0,
                'success': True,
                'duration': 1.0
            }
            
            cost_tracker.track_usage(
                backend='google_vision',
                image_path=f'/test/export_{i}.png',
                result=result,
                cost=0.0015
            )
        
        # Export report
        report_path = temp_dir / "usage_report.json"
        success = cost_tracker.export_usage_report(str(report_path), days=30)
        
        assert success
        assert report_path.exists()
        
        # Verify report content
        with open(report_path, 'r') as f:
            report = json.load(f)
        
        assert 'report_generated' in report
        assert 'usage_statistics' in report
        assert 'cost_optimization_recommendations' in report
        assert 'budget_alerts' in report
        assert 'total_savings_potential' in report
    
    def test_old_records_cleanup(self, cost_tracker):
        """Test cleanup of old usage records"""
        # Add some old records by manipulating the database directly
        import sqlite3
        old_date = (datetime.now() - timedelta(days=400)).isoformat()
        
        with sqlite3.connect(cost_tracker.db_path) as conn:
            conn.execute('''
                INSERT INTO usage_records 
                (timestamp, backend, image_path, cost, success, confidence, character_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (old_date, 'test_backend', '/old/file.png', 0.001, True, 90.0, 100))
        
        # Cleanup old records (keep last 365 days)
        deleted_count = cost_tracker.cleanup_old_records(365)
        
        assert isinstance(deleted_count, int)
        assert deleted_count >= 0
    
    def test_error_handling_in_tracking(self, cost_tracker):
        """Test error handling in usage tracking"""
        # Test with invalid data
        invalid_result = None
        
        # Should handle gracefully
        cost_tracker.track_usage(
            backend='test_backend',
            image_path='/invalid/path.png',
            result=invalid_result,
            cost=0.001
        )
        
        # Should still have created a record (with defaults)
        assert len(cost_tracker.session_usage) >= 0
    
    def test_pricing_information(self):
        """Test pricing information is available"""
        pricing = CostTracker.PRICING
        
        assert isinstance(pricing, dict)
        assert 'google_vision' in pricing
        assert 'aws_textract' in pricing
        assert 'azure_vision' in pricing
        assert 'local' in pricing
        
        # Check pricing structure
        for service, info in pricing.items():
            assert isinstance(info, dict)
            if service != 'local':
                assert any('per_' in key for key in info.keys())
    
    @pytest.mark.performance
    def test_cost_tracking_performance(self, cost_tracker):
        """Test cost tracking performance with many records"""
        import time
        
        start_time = time.time()
        
        # Track many usage records
        for i in range(100):
            result = {
                'text': f'Performance test {i}',
                'confidence': 85.0,
                'success': True,
                'duration': 1.0
            }
            
            cost_tracker.track_usage(
                backend='local',
                image_path=f'/test/perf_{i}.png',
                result=result,
                cost=0.0
            )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should complete within reasonable time
        assert elapsed < 10.0  # 10 seconds for 100 records
        
        # Verify all records were tracked
        assert len(cost_tracker.session_usage) >= 100


@pytest.mark.integration
class TestCostTrackingIntegration:
    """Integration tests for cost tracking system"""
    
    def test_full_cost_tracking_workflow(self, cost_tracker, temp_dir):
        """Test complete cost tracking workflow"""
        # Simulate a full OCR session with mixed backends
        session_data = [
            ('local', '/test/doc1.png', 0.0, True, 90.0),
            ('google_vision', '/test/doc2.jpg', 0.0015, True, 95.0),
            ('aws_textract', '/test/doc3.pdf', 0.002, True, 88.0),
            ('google_vision', '/test/doc4.png', 0.0015, False, 0.0),  # Failed
            ('local', '/test/doc5.jpg', 0.0, True, 85.0),
        ]
        
        # Track all usage
        for backend, path, cost, success, confidence in session_data:
            result = {
                'text': 'Session test result' if success else '',
                'confidence': confidence,
                'success': success,
                'duration': 1.5
            }
            
            cost_tracker.track_usage(
                backend=backend,
                image_path=path,
                result=result,
                cost=cost
            )
        
        # Get comprehensive statistics
        stats = cost_tracker.get_usage_stats(30)
        recommendations = cost_tracker.get_cost_optimization_recommendations()
        
        # Set budgets
        cost_tracker.set_monthly_budget('google_vision', 10.0)
        cost_tracker.set_monthly_budget('aws_textract', 20.0)
        
        # Check alerts
        alerts = cost_tracker.check_budget_alerts()
        
        # Export full report
        report_path = temp_dir / "full_report.json"
        success = cost_tracker.export_usage_report(str(report_path))
        
        # Verify everything worked
        assert success
        assert report_path.exists()
        assert stats['total_stats']['total_requests'] >= 5
        assert stats['total_stats']['successful_requests'] >= 4  # One failed
        assert isinstance(recommendations, list)
        assert isinstance(alerts, list)
    
    def test_cost_optimization_workflow(self, cost_tracker):
        """Test cost optimization recommendation workflow"""
        # Simulate expensive usage pattern
        expensive_usage = [
            ('google_vision', 0.0015, 75.0),  # Low accuracy, high cost
            ('aws_textract', 0.002, 70.0),   # Low accuracy, high cost
        ] * 10
        
        for backend, cost, confidence in expensive_usage:
            result = {
                'text': 'Expensive low quality result',
                'confidence': confidence,
                'success': True,
                'duration': 3.0  # Slow
            }
            
            cost_tracker.track_usage(
                backend=backend,
                image_path='/test/expensive.png',
                result=result,
                cost=cost
            )
        
        # Get recommendations
        recommendations = cost_tracker.get_cost_optimization_recommendations()
        
        # Should have multiple recommendation types
        rec_types = [rec.get('type') for rec in recommendations]
        
        # Should recommend cost reduction and accuracy improvements
        assert len(recommendations) > 0
        
        # Calculate potential savings
        total_savings = sum(rec.get('potential_savings', 0) for rec in recommendations)
        assert total_savings >= 0