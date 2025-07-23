"""
Default configuration values for Universal Document Converter.
This module centralizes all hardcoded values and provides a single source of truth for configuration.
"""

import os
import platform
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import json
import logging

DEFAULT_CONFIG = {
    'cache': {
        'max_size_mb': int(os.getenv('UDC_CACHE_MAX_SIZE_MB', '100')),
        'eviction_policy': os.getenv('UDC_CACHE_EVICTION_POLICY', 'lru'),
        'directory': os.getenv('UDC_CACHE_DIR', None)  # Will use system default if None
    },
    'performance': {
        'max_workers': int(os.getenv('UDC_MAX_WORKERS', '4')),
        'memory_threshold_mb': int(os.getenv('UDC_MEMORY_THRESHOLD_MB', '500')),
        'timeout_seconds': int(os.getenv('UDC_TIMEOUT_SECONDS', '30')),
        'chunk_size': int(os.getenv('UDC_CHUNK_SIZE', '8192')),
        'max_file_size_mb': int(os.getenv('UDC_MAX_FILE_SIZE_MB', '100'))
    },
    'paths': {
        'tesseract_exe': os.getenv('UDC_TESSERACT_PATH', None),  # Auto-detect if None
        'temp_dir': os.getenv('UDC_TEMP_DIR', None),  # Use system temp if None
        'cache_dir': os.getenv('UDC_CACHE_DIR', None),  # Use user cache if None
        'config_dir': os.getenv('UDC_CONFIG_DIR', None)  # Use user config if None
    },
    'ocr': {
        'language': os.getenv('UDC_OCR_LANGUAGE', 'eng'),
        'page_seg_mode': int(os.getenv('UDC_OCR_PSM', '3')),
        'engine_mode': int(os.getenv('UDC_OCR_ENGINE_MODE', '3')),
        'dpi': int(os.getenv('UDC_OCR_DPI', '300')),
        'confidence_threshold': float(os.getenv('UDC_OCR_CONFIDENCE_THRESHOLD', '0.0'))
    },
    'api': {
        'google_vision_enabled': os.getenv('UDC_GOOGLE_VISION_ENABLED', 'false').lower() == 'true',
        'azure_enabled': os.getenv('UDC_AZURE_ENABLED', 'false').lower() == 'true',
        'aws_enabled': os.getenv('UDC_AWS_ENABLED', 'false').lower() == 'true'
    },
    'gui': {
        'theme': os.getenv('UDC_GUI_THEME', 'default'),
        'window_width': int(os.getenv('UDC_GUI_WIDTH', '800')),
        'window_height': int(os.getenv('UDC_GUI_HEIGHT', '600')),
        'auto_preview': os.getenv('UDC_GUI_AUTO_PREVIEW', 'true').lower() == 'true'
    },
    'logging': {
        'level': os.getenv('UDC_LOG_LEVEL', 'INFO'),
        'file_enabled': os.getenv('UDC_LOG_FILE_ENABLED', 'true').lower() == 'true',
        'max_file_size_mb': int(os.getenv('UDC_LOG_MAX_FILE_SIZE_MB', '10')),
        'backup_count': int(os.getenv('UDC_LOG_BACKUP_COUNT', '5'))
    }
}

# Platform-specific defaults
if platform.system() == 'Windows':
    PLATFORM_DEFAULTS = {
        'paths': {
            'tesseract_exe': r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        }
    }
elif platform.system() == 'Darwin':  # macOS
    PLATFORM_DEFAULTS = {
        'paths': {
            'tesseract_exe': '/usr/local/bin/tesseract'
        }
    }
else:  # Linux and others
    PLATFORM_DEFAULTS = {
        'paths': {
            'tesseract_exe': '/usr/bin/tesseract'
        }
    }

class ConfigManager:
    """Manages configuration loading, validation, and access."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.config_file = config_file or self._get_default_config_file()
        self._config = self._load_config()
        
    def _get_default_config_file(self) -> str:
        """Get the default configuration file path."""
        config_dir = Path.home() / ".universal_converter"
        try:
            config_dir.mkdir(exist_ok=True)
        except (OSError, PermissionError) as e:
            self.logger.warning(f"Failed to create config directory {config_dir}: {e}")
            config_dir = Path.home()  # Fallback to home directory
        return str(config_dir / "config.json")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file and merge with defaults."""
        config = DEFAULT_CONFIG.copy()
        
        # Apply platform-specific defaults
        self._deep_update(config, PLATFORM_DEFAULTS)
        
        # Load user configuration if it exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    self._deep_update(config, user_config)
                    self.logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                self.logger.warning(f"Failed to load configuration from {self.config_file}: {e}")
        
        # Resolve None values to actual paths
        self._resolve_paths(config)
        
        return config
    
    def _deep_update(self, base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
        """Deep update a dictionary."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def _resolve_paths(self, config: Dict[str, Any]) -> None:
        """Resolve None paths to actual system paths."""
        paths = config['paths']
        
        # Resolve temp directory
        if paths['temp_dir'] is None:
            paths['temp_dir'] = tempfile.gettempdir()
        
        # Resolve cache directory
        if paths['cache_dir'] is None:
            cache_dir = Path.home() / ".cache" / "universal_converter"
            cache_dir.mkdir(parents=True, exist_ok=True)
            paths['cache_dir'] = str(cache_dir)
        
        # Resolve config directory
        if paths['config_dir'] is None:
            config_dir = Path.home() / ".universal_converter"
            config_dir.mkdir(exist_ok=True)
            paths['config_dir'] = str(config_dir)
        
        # Auto-detect Tesseract if not specified
        if paths['tesseract_exe'] is None:
            paths['tesseract_exe'] = self._find_tesseract()
    
    def _find_tesseract(self) -> str:
        """Auto-detect Tesseract executable location."""
        possible_paths = [
            # Windows
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            # macOS
            '/usr/local/bin/tesseract',
            '/opt/homebrew/bin/tesseract',
            # Linux
            '/usr/bin/tesseract',
            '/usr/local/bin/tesseract'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Fallback to system PATH
        return 'tesseract'
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation (e.g., 'cache.max_size_mb')."""
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key_path.split('.')
        config = self._config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def save(self) -> None:
        """Save the current configuration to file."""
        try:
            config_dir = Path(self.config_file).parent
            config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
            
            self.logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration to {self.config_file}: {e}")
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the full configuration dictionary."""
        return self._config.copy()

# Global configuration instance
config_manager = ConfigManager()