"""
Monitoring module for OCR system

Provides cost tracking, performance monitoring, and usage analytics
for OCR operations across multiple backends.
"""

from .cost_tracker import CostTracker, UsageRecord

__all__ = ['CostTracker', 'UsageRecord']