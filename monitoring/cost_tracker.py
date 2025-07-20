"""
Cost tracking and optimization for OCR cloud services

Provides comprehensive cost tracking, usage monitoring, and
optimization recommendations for cloud OCR APIs.

Author: Terry AI Agent for Terragon Labs
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import json
import sqlite3
from dataclasses import dataclass, asdict

@dataclass
class UsageRecord:
    """Record of OCR usage"""
    timestamp: datetime
    backend: str
    image_path: str
    image_size_mb: float
    processing_time: float
    cost: float
    success: bool
    confidence: float
    character_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

class CostTracker:
    """
    Comprehensive cost tracking and optimization system
    
    Features:
    - Real-time cost tracking per backend
    - Usage analytics and reporting
    - Cost optimization recommendations
    - Budget alerts and limits
    - Monthly/yearly cost projections
    """
    
    # Current pricing (as of 2024, in USD)
    PRICING = {
        'google_vision': {
            'per_1000_requests': 1.50,
            'free_tier_monthly': 1000
        },
        'aws_textract': {
            'detect_text_per_1000_pages': 1.50,
            'analyze_document_per_1000_pages': 50.00,
            'free_tier_monthly': 1000
        },
        'azure_vision': {
            'per_1000_transactions': 1.00,
            'free_tier_monthly': 5000
        },
        'local': {
            'per_request': 0.0  # Free
        }
    }
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize cost tracker
        
        Args:
            db_path: Path to SQLite database for usage storage
        """
        self.logger = logging.getLogger("CostTracker")
        
        # Set up database
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = Path.home() / ".ocr_secure" / "usage.db"
        
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        # In-memory cache for current session
        self.session_usage = []
        self.monthly_totals = {}
        
        # Load monthly totals
        self._load_monthly_totals()
    
    def _init_database(self):
        """Initialize SQLite database for usage tracking"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS usage_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    backend TEXT NOT NULL,
                    image_path TEXT,
                    image_size_mb REAL,
                    processing_time REAL,
                    cost REAL NOT NULL,
                    success BOOLEAN NOT NULL,
                    confidence REAL,
                    character_count INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp ON usage_records(timestamp)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_backend ON usage_records(backend)
            ''')
    
    def track_usage(self, backend: str, image_path: str, result: Dict[str, Any], 
                   cost: float, image_size_mb: float = 0.0) -> None:
        """
        Track OCR usage for cost calculation
        
        Args:
            backend: Backend name used
            image_path: Path to processed image
            result: OCR result dictionary
            cost: Cost of the operation
            image_size_mb: Size of image in MB
        """
        try:
            record = UsageRecord(
                timestamp=datetime.now(),
                backend=backend,
                image_path=image_path,
                image_size_mb=image_size_mb,
                processing_time=result.get('duration', 0.0),
                cost=cost,
                success=result.get('success', False),
                confidence=result.get('confidence', 0.0),
                character_count=len(result.get('text', ''))
            )
            
            # Add to session cache
            self.session_usage.append(record)
            
            # Update monthly totals
            month_key = record.timestamp.strftime('%Y-%m')
            if month_key not in self.monthly_totals:
                self.monthly_totals[month_key] = {'cost': 0.0, 'requests': 0}
            
            self.monthly_totals[month_key]['cost'] += cost
            self.monthly_totals[month_key]['requests'] += 1
            
            # Store in database
            self._save_to_database(record)
            
            self.logger.debug(f"Tracked usage: {backend} - ${cost:.4f}")
            
        except Exception as e:
            self.logger.error(f"Failed to track usage: {e}")
    
    def _save_to_database(self, record: UsageRecord) -> None:
        """Save usage record to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO usage_records 
                    (timestamp, backend, image_path, image_size_mb, processing_time, 
                     cost, success, confidence, character_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record.timestamp.isoformat(),
                    record.backend,
                    record.image_path,
                    record.image_size_mb,
                    record.processing_time,
                    record.cost,
                    record.success,
                    record.confidence,
                    record.character_count
                ))
        except Exception as e:
            self.logger.error(f"Failed to save usage record to database: {e}")
    
    def _load_monthly_totals(self) -> None:
        """Load monthly totals from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT 
                        strftime('%Y-%m', timestamp) as month,
                        SUM(cost) as total_cost,
                        COUNT(*) as total_requests
                    FROM usage_records 
                    GROUP BY strftime('%Y-%m', timestamp)
                    ORDER BY month DESC
                    LIMIT 12
                ''')
                
                for month, total_cost, total_requests in cursor.fetchall():
                    self.monthly_totals[month] = {
                        'cost': total_cost,
                        'requests': total_requests
                    }
                    
        except Exception as e:
            self.logger.error(f"Failed to load monthly totals: {e}")
    
    def get_current_month_cost(self) -> float:
        """Get total cost for current month"""
        current_month = datetime.now().strftime('%Y-%m')
        return self.monthly_totals.get(current_month, {}).get('cost', 0.0)
    
    def get_current_month_requests(self) -> int:
        """Get total requests for current month"""
        current_month = datetime.now().strftime('%Y-%m')
        return self.monthly_totals.get(current_month, {}).get('requests', 0)
    
    def get_backend_costs(self, days: int = 30) -> Dict[str, float]:
        """
        Get cost breakdown by backend for the last N days
        
        Args:
            days: Number of days to look back
            
        Returns:
            Dictionary mapping backend names to costs
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT backend, SUM(cost) as total_cost
                    FROM usage_records 
                    WHERE timestamp >= ?
                    GROUP BY backend
                ''', (cutoff_date.isoformat(),))
                
                return dict(cursor.fetchall())
                
        except Exception as e:
            self.logger.error(f"Failed to get backend costs: {e}")
            return {}
    
    def get_usage_stats(self, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive usage statistics
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with usage statistics
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                # Total stats
                cursor = conn.execute('''
                    SELECT 
                        COUNT(*) as total_requests,
                        SUM(cost) as total_cost,
                        AVG(cost) as avg_cost_per_request,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_requests,
                        AVG(processing_time) as avg_processing_time,
                        AVG(confidence) as avg_confidence,
                        SUM(character_count) as total_characters
                    FROM usage_records 
                    WHERE timestamp >= ?
                ''', (cutoff_date.isoformat(),))
                
                row = cursor.fetchone()
                total_stats = {
                    'total_requests': row[0] or 0,
                    'total_cost': row[1] or 0.0,
                    'avg_cost_per_request': row[2] or 0.0,
                    'successful_requests': row[3] or 0,
                    'success_rate': (row[3] or 0) / max(1, row[0] or 0),
                    'avg_processing_time': row[4] or 0.0,
                    'avg_confidence': row[5] or 0.0,
                    'total_characters': row[6] or 0
                }
                
                # Backend breakdown
                cursor = conn.execute('''
                    SELECT 
                        backend,
                        COUNT(*) as requests,
                        SUM(cost) as cost,
                        AVG(processing_time) as avg_time,
                        AVG(confidence) as avg_confidence
                    FROM usage_records 
                    WHERE timestamp >= ?
                    GROUP BY backend
                ''', (cutoff_date.isoformat(),))
                
                backend_stats = {}
                for backend, requests, cost, avg_time, avg_conf in cursor.fetchall():
                    backend_stats[backend] = {
                        'requests': requests,
                        'cost': cost,
                        'avg_processing_time': avg_time,
                        'avg_confidence': avg_conf,
                        'cost_per_request': cost / max(1, requests)
                    }
                
                return {
                    'period_days': days,
                    'total_stats': total_stats,
                    'backend_stats': backend_stats,
                    'monthly_totals': self.monthly_totals
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get usage stats: {e}")
            return {}
    
    def get_cost_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get cost optimization recommendations based on usage patterns
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        try:
            stats = self.get_usage_stats(30)
            backend_stats = stats.get('backend_stats', {})
            total_cost = stats.get('total_stats', {}).get('total_cost', 0)
            
            # Check if local backend could handle most requests
            local_stats = backend_stats.get('local', {})
            cloud_total_cost = sum(
                info['cost'] for name, info in backend_stats.items() 
                if name != 'local'
            )
            
            if cloud_total_cost > 10.0:  # More than $10/month on cloud
                recommendations.append({
                    'type': 'cost_reduction',
                    'title': 'Consider Local Processing',
                    'description': f'You spent ${cloud_total_cost:.2f} on cloud OCR this month. '
                                 f'Local processing could reduce costs for standard documents.',
                    'potential_savings': cloud_total_cost * 0.7,
                    'action': 'Configure local OCR as primary backend for standard documents'
                })
            
            # Check for expensive backends with low accuracy
            for backend, info in backend_stats.items():
                if backend != 'local' and info['cost'] > 5.0:
                    if info['avg_confidence'] < 80.0:
                        recommendations.append({
                            'type': 'accuracy_vs_cost',
                            'title': f'Low Accuracy on {backend}',
                            'description': f'{backend} has low average confidence ({info["avg_confidence"]:.1f}%) '
                                         f'but costs ${info["cost"]:.2f}. Consider switching backends.',
                            'potential_savings': info['cost'] * 0.5,
                            'action': f'Test alternative backends for better accuracy'
                        })
            
            # Check for free tier optimization
            current_month_requests = self.get_current_month_requests()
            for backend, pricing in self.PRICING.items():
                if backend in backend_stats and 'free_tier_monthly' in pricing:
                    backend_requests = backend_stats[backend]['requests']
                    free_tier = pricing['free_tier_monthly']
                    
                    if backend_requests < free_tier * 0.8:  # Using less than 80% of free tier
                        recommendations.append({
                            'type': 'free_tier_optimization',
                            'title': f'Underutilizing {backend} Free Tier',
                            'description': f'You used {backend_requests} requests out of {free_tier} free '
                                         f'monthly requests for {backend}.',
                            'potential_savings': 0,
                            'action': f'Consider using {backend} more to maximize free tier value'
                        })
            
            # Check for batch processing opportunities
            total_requests = stats.get('total_stats', {}).get('total_requests', 0)
            if total_requests > 100:
                avg_processing_time = stats.get('total_stats', {}).get('avg_processing_time', 0)
                if avg_processing_time > 3.0:  # Slow processing
                    recommendations.append({
                        'type': 'performance_optimization',
                        'title': 'Batch Processing Opportunity',
                        'description': f'Average processing time is {avg_processing_time:.1f}s. '
                                     f'Batch processing could reduce costs and improve speed.',
                        'potential_savings': total_cost * 0.2,
                        'action': 'Implement batch processing for multiple documents'
                    })
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
        
        return recommendations
    
    def set_monthly_budget(self, backend: str, budget: float) -> None:
        """
        Set monthly budget for a backend
        
        Args:
            backend: Backend name
            budget: Monthly budget in USD
        """
        # This would be stored in a configuration file or database
        # For now, we'll store in a simple JSON file
        try:
            budget_file = self.db_path.parent / "budgets.json"
            budgets = {}
            
            if budget_file.exists():
                with open(budget_file, 'r') as f:
                    budgets = json.load(f)
            
            budgets[backend] = budget
            
            with open(budget_file, 'w') as f:
                json.dump(budgets, f, indent=2)
                
            self.logger.info(f"Set monthly budget for {backend}: ${budget:.2f}")
            
        except Exception as e:
            self.logger.error(f"Failed to set budget: {e}")
    
    def check_budget_alerts(self) -> List[Dict[str, Any]]:
        """
        Check for budget alerts
        
        Returns:
            List of budget alert dictionaries
        """
        alerts = []
        
        try:
            budget_file = self.db_path.parent / "budgets.json"
            if not budget_file.exists():
                return alerts
            
            with open(budget_file, 'r') as f:
                budgets = json.load(f)
            
            current_costs = self.get_backend_costs(30)  # Current month approximation
            
            for backend, budget in budgets.items():
                current_cost = current_costs.get(backend, 0.0)
                usage_percent = (current_cost / budget) * 100 if budget > 0 else 0
                
                if usage_percent >= 90:
                    alerts.append({
                        'type': 'budget_exceeded',
                        'backend': backend,
                        'budget': budget,
                        'current_cost': current_cost,
                        'usage_percent': usage_percent,
                        'message': f'{backend} is at {usage_percent:.1f}% of monthly budget'
                    })
                elif usage_percent >= 75:
                    alerts.append({
                        'type': 'budget_warning',
                        'backend': backend,
                        'budget': budget,
                        'current_cost': current_cost,
                        'usage_percent': usage_percent,
                        'message': f'{backend} is at {usage_percent:.1f}% of monthly budget'
                    })
                    
        except Exception as e:
            self.logger.error(f"Failed to check budget alerts: {e}")
        
        return alerts
    
    def export_usage_report(self, output_path: str, days: int = 30) -> bool:
        """
        Export detailed usage report to file
        
        Args:
            output_path: Path to save the report
            days: Number of days to include in report
            
        Returns:
            True if export successful
        """
        try:
            stats = self.get_usage_stats(days)
            recommendations = self.get_cost_optimization_recommendations()
            alerts = self.check_budget_alerts()
            
            report = {
                'report_generated': datetime.now().isoformat(),
                'period_days': days,
                'usage_statistics': stats,
                'cost_optimization_recommendations': recommendations,
                'budget_alerts': alerts,
                'total_savings_potential': sum(
                    rec.get('potential_savings', 0) for rec in recommendations
                )
            }
            
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            self.logger.info(f"Usage report exported to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export usage report: {e}")
            return False
    
    def cleanup_old_records(self, days: int = 365) -> int:
        """
        Clean up old usage records
        
        Args:
            days: Keep records newer than this many days
            
        Returns:
            Number of records deleted
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    DELETE FROM usage_records 
                    WHERE timestamp < ?
                ''', (cutoff_date.isoformat(),))
                
                deleted_count = cursor.rowcount
                self.logger.info(f"Cleaned up {deleted_count} old usage records")
                return deleted_count
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup old records: {e}")
            return 0