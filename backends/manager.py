"""
OCR Backend Manager

Provides intelligent backend selection, fallback mechanisms, and
unified interface for all OCR backends including local and cloud services.

Author: Terry AI Agent for Terragon Labs
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import time
import json

# Import local backends
try:
    from ..ocr_engine.ocr_engine import OCREngine as LocalOCREngine
    LOCAL_OCR_AVAILABLE = True
except ImportError:
    try:
        # Try absolute import for validation script
        from ocr_engine.ocr_engine import OCREngine as LocalOCREngine
        LOCAL_OCR_AVAILABLE = True
    except ImportError:
        LOCAL_OCR_AVAILABLE = False
        LocalOCREngine = None

# Import cloud backends
from .google_vision import GoogleVisionBackend
from .aws_textract import AWSTextractBackend
from .azure_vision import AzureVisionBackend

# Import security
try:
    from ..security import SecurityValidator, CredentialManager
except ImportError:
    # Try absolute import for validation script
    from security import SecurityValidator, CredentialManager

class BackendSelectionError(Exception):
    """Raised when no suitable backend is available"""
    pass

class OCRBackendManager:
    """
    Intelligent OCR backend manager
    
    Features:
    - Automatic backend selection based on requirements
    - Fallback mechanism with priority ordering
    - Cost optimization and tracking
    - Performance monitoring
    - Security validation
    - Load balancing across backends
    """
    
    def __init__(self, config_path: Optional[str] = None, security_config: Optional[Dict] = None):
        """
        Initialize backend manager
        
        Args:
            config_path: Path to configuration file
            security_config: Security configuration options
        """
        self.logger = logging.getLogger("OCRBackendManager")
        self.security_validator = SecurityValidator()
        self.credential_manager = CredentialManager()
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize backends
        self.backends = {}
        self.fallback_order = []
        self.performance_stats = {}
        
        self._initialize_backends()
        self._determine_fallback_order()
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            'backends': {
                'local': {
                    'enabled': True,
                    'priority': 1
                },
                'google_vision': {
                    'enabled': False,
                    'priority': 2,
                    'cost_limit_monthly': 100.0
                },
                'aws_textract': {
                    'enabled': False,
                    'priority': 3,
                    'cost_limit_monthly': 100.0
                },
                'azure_vision': {
                    'enabled': False,
                    'priority': 4,
                    'cost_limit_monthly': 100.0
                }
            },
            'selection_strategy': 'cost_optimized',  # 'fastest', 'most_accurate', 'cost_optimized'
            'fallback_enabled': True,
            'max_retries': 3,
            'timeout_seconds': 30
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    default_config.update(user_config)
            except Exception as e:
                self.logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def _initialize_backends(self):
        """Initialize all available backends"""
        backend_config = self.config.get('backends', {})
        
        # Initialize local backend (Tesseract + EasyOCR)
        if backend_config.get('local', {}).get('enabled', True) and LOCAL_OCR_AVAILABLE:
            try:
                local_backend = LocalOCREngine()
                if local_backend.get_available_backends():
                    self.backends['local'] = {
                        'instance': local_backend,
                        'type': 'local',
                        'priority': backend_config['local'].get('priority', 1),
                        'available': True,
                        'cost_per_request': 0.0
                    }
                    self.logger.info("Local OCR backend initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize local backend: {e}")
        
        # Initialize Google Vision backend
        if backend_config.get('google_vision', {}).get('enabled', False):
            try:
                google_creds = self.credential_manager.get_credentials('google_vision')
                if google_creds:
                    google_backend = GoogleVisionBackend(google_creds)
                    if google_backend.is_available():
                        self.backends['google_vision'] = {
                            'instance': google_backend,
                            'type': 'cloud',
                            'priority': backend_config['google_vision'].get('priority', 2),
                            'available': True,
                            'cost_per_request': 0.0015  # $1.50 per 1000 requests
                        }
                        self.logger.info("Google Vision backend initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Google Vision backend: {e}")
        
        # Initialize AWS Textract backend
        if backend_config.get('aws_textract', {}).get('enabled', False):
            try:
                aws_creds = self.credential_manager.get_credentials('aws_textract')
                if aws_creds:
                    aws_backend = AWSTextractBackend(aws_creds)
                    if aws_backend.is_available():
                        self.backends['aws_textract'] = {
                            'instance': aws_backend,
                            'type': 'cloud',
                            'priority': backend_config['aws_textract'].get('priority', 3),
                            'available': True,
                            'cost_per_request': 0.0015  # $1.50 per 1000 pages
                        }
                        self.logger.info("AWS Textract backend initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize AWS Textract backend: {e}")
        
        # Initialize Azure Vision backend
        if backend_config.get('azure_vision', {}).get('enabled', False):
            try:
                azure_creds = self.credential_manager.get_credentials('azure_vision')
                if azure_creds:
                    azure_backend = AzureVisionBackend(azure_creds)
                    if azure_backend.is_available():
                        self.backends['azure_vision'] = {
                            'instance': azure_backend,
                            'type': 'cloud',
                            'priority': backend_config['azure_vision'].get('priority', 4),
                            'available': True,
                            'cost_per_request': 0.001  # $1.00 per 1000 transactions
                        }
                        self.logger.info("Azure Vision backend initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Azure Vision backend: {e}")
    
    def _determine_fallback_order(self):
        """Determine the fallback order based on priorities and availability"""
        available_backends = [
            (name, info['priority']) 
            for name, info in self.backends.items() 
            if info['available']
        ]
        
        # Sort by priority (lower numbers = higher priority)
        available_backends.sort(key=lambda x: x[1])
        self.fallback_order = [name for name, _ in available_backends]
        
        self.logger.info(f"Fallback order: {self.fallback_order}")
    
    def select_backend(self, image_path: str, requirements: Optional[Dict[str, Any]] = None) -> str:
        """
        Select optimal backend based on image characteristics and requirements
        
        Args:
            image_path: Path to the image file
            requirements: Dictionary of requirements:
                - accuracy: 'high', 'medium', 'low'
                - speed: 'fast', 'medium', 'slow'
                - cost: 'minimize', 'balanced', 'premium'
                - offline_only: bool
                - cloud_preferred: bool
                
        Returns:
            Name of the selected backend
            
        Raises:
            BackendSelectionError: If no suitable backend is available
        """
        requirements = requirements or {}
        
        if not self.fallback_order:
            raise BackendSelectionError("No OCR backends available")
        
        # Analyze image characteristics
        image_info = self._analyze_image(image_path)
        
        # Apply selection strategy
        strategy = self.config.get('selection_strategy', 'cost_optimized')
        
        if strategy == 'fastest':
            return self._select_fastest_backend(image_info, requirements)
        elif strategy == 'most_accurate':
            return self._select_most_accurate_backend(image_info, requirements)
        elif strategy == 'cost_optimized':
            return self._select_cost_optimized_backend(image_info, requirements)
        else:
            # Default to first available backend
            return self.fallback_order[0]
    
    def _analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze image characteristics to help with backend selection
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with image analysis results
        """
        try:
            from PIL import Image
            
            with Image.open(image_path) as img:
                width, height = img.size
                size_mb = Path(image_path).stat().st_size / (1024 * 1024)
                
                # Simple heuristics for image analysis
                is_large = size_mb > 5.0 or width > 2000 or height > 2000
                aspect_ratio = width / height
                is_document = 0.7 <= aspect_ratio <= 1.5  # Typical document ratios
                
                return {
                    'width': width,
                    'height': height,
                    'size_mb': size_mb,
                    'is_large': is_large,
                    'is_document': is_document,
                    'aspect_ratio': aspect_ratio
                }
                
        except Exception as e:
            self.logger.warning(f"Failed to analyze image {image_path}: {e}")
            return {
                'width': 0,
                'height': 0,
                'size_mb': 0,
                'is_large': False,
                'is_document': True,
                'aspect_ratio': 1.0
            }
    
    def _select_fastest_backend(self, image_info: Dict, requirements: Dict) -> str:
        """Select backend optimized for speed"""
        # Offline-only requirement
        if requirements.get('offline_only', False):
            if 'local' in self.backends and self.backends['local']['available']:
                return 'local'
            else:
                raise BackendSelectionError("Offline-only required but local backend not available")
        
        # For speed, prefer local backend for small images, cloud for complex ones
        if image_info.get('is_large', False) and not requirements.get('offline_only', False):
            # Large images might benefit from cloud processing power
            cloud_backends = [name for name in self.fallback_order 
                            if self.backends[name]['type'] == 'cloud']
            if cloud_backends:
                return cloud_backends[0]
        
        # Default to first available backend
        return self.fallback_order[0]
    
    def _select_most_accurate_backend(self, image_info: Dict, requirements: Dict) -> str:
        """Select backend optimized for accuracy"""
        # Offline-only requirement
        if requirements.get('offline_only', False):
            if 'local' in self.backends and self.backends['local']['available']:
                return 'local'
            else:
                raise BackendSelectionError("Offline-only required but local backend not available")
        
        # For accuracy, prefer cloud backends
        cloud_backends = [name for name in self.fallback_order 
                         if self.backends[name]['type'] == 'cloud']
        
        if cloud_backends:
            # Prefer Google Vision for general accuracy
            if 'google_vision' in cloud_backends:
                return 'google_vision'
            # AWS Textract for documents with tables/forms
            elif 'aws_textract' in cloud_backends and image_info.get('is_document', False):
                return 'aws_textract'
            else:
                return cloud_backends[0]
        
        # Fall back to local if no cloud backends available
        return self.fallback_order[0]
    
    def _select_cost_optimized_backend(self, image_info: Dict, requirements: Dict) -> str:
        """Select backend optimized for cost"""
        # Offline-only requirement
        if requirements.get('offline_only', False):
            if 'local' in self.backends and self.backends['local']['available']:
                return 'local'
            else:
                raise BackendSelectionError("Offline-only required but local backend not available")
        
        # For cost optimization, prefer free local backend
        if 'local' in self.backends and self.backends['local']['available']:
            # Use local for standard documents
            if not requirements.get('cloud_preferred', False):
                return 'local'
        
        # If cloud is preferred or local not available, select cheapest cloud backend
        cloud_backends = [(name, self.backends[name]['cost_per_request']) 
                         for name in self.fallback_order 
                         if self.backends[name]['type'] == 'cloud']
        
        if cloud_backends:
            # Sort by cost
            cloud_backends.sort(key=lambda x: x[1])
            return cloud_backends[0][0]
        
        # Fall back to local
        return self.fallback_order[0]
    
    def process_with_fallback(self, image_path: str, language: str = 'en', 
                            requirements: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process image with intelligent fallback strategy
        
        Args:
            image_path: Path to the image file
            language: Language code for OCR
            requirements: Processing requirements
            
        Returns:
            Dictionary with processing results
        """
        # Validate input file
        try:
            self.security_validator.validate_file_path(image_path)
        except Exception as e:
            return {
                'text': '',
                'confidence': 0,
                'success': False,
                'error': f'Security validation failed: {e}',
                'backend_used': None
            }
        
        requirements = requirements or {}
        max_retries = self.config.get('max_retries', 3)
        
        # Try primary backend
        try:
            primary_backend = self.select_backend(image_path, requirements)
            result = self._process_with_backend(primary_backend, image_path, language)
            
            if result.get('success', False) and self._is_quality_acceptable(result, requirements):
                result['backend_used'] = primary_backend
                result['used_fallback'] = False
                self._update_performance_stats(primary_backend, True, result.get('duration', 0))
                return result
                
        except Exception as e:
            self.logger.warning(f"Primary backend selection failed: {e}")
        
        # Try fallback backends if enabled
        if self.config.get('fallback_enabled', True):
            for backend_name in self.fallback_order:
                if backend_name in self.backends and self.backends[backend_name]['available']:
                    for attempt in range(max_retries):
                        try:
                            result = self._process_with_backend(backend_name, image_path, language)
                            
                            if result.get('success', False):
                                result['backend_used'] = backend_name
                                result['used_fallback'] = True
                                result['fallback_attempt'] = attempt + 1
                                self._update_performance_stats(backend_name, True, result.get('duration', 0))
                                return result
                                
                        except Exception as e:
                            self.logger.warning(f"Fallback backend {backend_name} attempt {attempt + 1} failed: {e}")
                            self._update_performance_stats(backend_name, False, 0)
                            
                            if attempt < max_retries - 1:
                                time.sleep(1)  # Brief delay before retry
                            else:
                                break
        
        # All backends failed
        return {
            'text': '',
            'confidence': 0,
            'success': False,
            'error': 'All OCR backends failed',
            'backend_used': None,
            'suggestions': self._get_troubleshooting_suggestions()
        }
    
    def _process_with_backend(self, backend_name: str, image_path: str, language: str) -> Dict[str, Any]:
        """Process image with specific backend"""
        if backend_name not in self.backends:
            raise ValueError(f"Backend {backend_name} not available")
        
        backend_info = self.backends[backend_name]
        backend_instance = backend_info['instance']
        
        start_time = time.time()
        
        if backend_name == 'local':
            # Use local OCR engine
            result = backend_instance.extract_text(image_path, {'languages': [language]})
            # Convert local format to unified format
            unified_result = {
                'text': result.get('text', ''),
                'confidence': result.get('confidence', 0),
                'success': bool(result.get('text', '')),
                'backend': 'local',
                'duration': time.time() - start_time
            }
        else:
            # Use cloud backend
            unified_result = backend_instance.extract_text(image_path, language)
            unified_result['duration'] = time.time() - start_time
        
        return unified_result
    
    def _is_quality_acceptable(self, result: Dict[str, Any], requirements: Dict[str, Any]) -> bool:
        """Check if OCR result quality meets requirements"""
        confidence = result.get('confidence', 0)
        text_length = len(result.get('text', ''))
        
        # Define quality thresholds based on requirements
        min_confidence = 70  # Default
        min_text_length = 5  # Minimum reasonable text length
        
        if requirements.get('accuracy') == 'high':
            min_confidence = 90
        elif requirements.get('accuracy') == 'low':
            min_confidence = 50
        
        return confidence >= min_confidence and text_length >= min_text_length
    
    def _update_performance_stats(self, backend_name: str, success: bool, duration: float):
        """Update performance statistics for a backend"""
        if backend_name not in self.performance_stats:
            self.performance_stats[backend_name] = {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'total_duration': 0.0,
                'avg_duration': 0.0
            }
        
        stats = self.performance_stats[backend_name]
        stats['total_requests'] += 1
        
        if success:
            stats['successful_requests'] += 1
            stats['total_duration'] += duration
            stats['avg_duration'] = stats['total_duration'] / stats['successful_requests']
        else:
            stats['failed_requests'] += 1
    
    def _get_troubleshooting_suggestions(self) -> List[str]:
        """Get troubleshooting suggestions when all backends fail"""
        suggestions = []
        
        if not self.backends:
            suggestions.append("No OCR backends are configured. Check your installation and configuration.")
        
        if 'local' not in self.backends:
            suggestions.append("Local OCR backend (Tesseract/EasyOCR) is not available. Install required dependencies.")
        
        cloud_backends = [name for name, info in self.backends.items() if info['type'] == 'cloud']
        if not cloud_backends:
            suggestions.append("No cloud OCR backends are configured. Consider setting up Google Vision, AWS Textract, or Azure Vision.")
        
        suggestions.append("Check image quality and format. Ensure the image contains readable text.")
        suggestions.append("Verify network connectivity if using cloud backends.")
        suggestions.append("Check API credentials and quotas for cloud services.")
        
        return suggestions
    
    def get_backend_status(self) -> Dict[str, Any]:
        """Get status of all backends"""
        status = {}
        
        for name, info in self.backends.items():
            status[name] = {
                'available': info['available'],
                'type': info['type'],
                'priority': info['priority'],
                'cost_per_request': info['cost_per_request'],
                'performance_stats': self.performance_stats.get(name, {})
            }
        
        return status
    
    def get_available_backends(self) -> List[str]:
        """Get list of available backend names"""
        return [name for name, info in self.backends.items() if info['available']]
    
    def cleanup(self):
        """Cleanup all backend resources"""
        for backend_info in self.backends.values():
            try:
                backend_instance = backend_info['instance']
                if hasattr(backend_instance, 'cleanup'):
                    backend_instance.cleanup()
            except Exception as e:
                self.logger.warning(f"Failed to cleanup backend: {e}")