"""
Cross-Platform Integration Module for Quick Document Convertor

This module provides platform-specific functionality for Linux, macOS, and Windows
to enable native desktop integration, file associations, and packaging.

Author: Beau Lewis
Project: Quick Document Convertor
"""

import platform
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple


def get_platform() -> str:
    """
    Get the current platform identifier.
    
    Returns:
        str: 'windows', 'linux', 'macos', or 'unknown'
    """
    system = platform.system().lower()
    if system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    elif system == 'darwin':
        return 'macos'
    else:
        return 'unknown'


def get_platform_info() -> Dict[str, str]:
    """
    Get detailed platform information.
    
    Returns:
        Dict containing platform details
    """
    return {
        'platform': get_platform(),
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': sys.version,
        'architecture': platform.architecture()[0]
    }


def get_config_dir() -> Path:
    """
    Get platform-specific configuration directory.
    
    Returns:
        Path to configuration directory
    """
    platform_name = get_platform()
    
    if platform_name == 'windows':
        # Windows: %APPDATA%\Quick Document Convertor
        return Path.home() / "AppData" / "Roaming" / "Quick Document Convertor"
    elif platform_name == 'macos':
        # macOS: ~/Library/Application Support/Quick Document Convertor
        return Path.home() / "Library" / "Application Support" / "Quick Document Convertor"
    elif platform_name == 'linux':
        # Linux: ~/.config/quick-document-convertor
        return Path.home() / ".config" / "quick-document-convertor"
    else:
        # Fallback
        return Path.home() / ".quick-document-convertor"


def get_data_dir() -> Path:
    """
    Get platform-specific data directory.
    
    Returns:
        Path to data directory
    """
    platform_name = get_platform()
    
    if platform_name == 'windows':
        # Windows: %LOCALAPPDATA%\Quick Document Convertor
        return Path.home() / "AppData" / "Local" / "Quick Document Convertor"
    elif platform_name == 'macos':
        # macOS: ~/Library/Application Support/Quick Document Convertor
        return Path.home() / "Library" / "Application Support" / "Quick Document Convertor"
    elif platform_name == 'linux':
        # Linux: ~/.local/share/quick-document-convertor
        return Path.home() / ".local" / "share" / "quick-document-convertor"
    else:
        # Fallback
        return Path.home() / ".quick-document-convertor"


def get_cache_dir() -> Path:
    """
    Get platform-specific cache directory.
    
    Returns:
        Path to cache directory
    """
    platform_name = get_platform()
    
    if platform_name == 'windows':
        # Windows: %LOCALAPPDATA%\Quick Document Convertor\Cache
        return get_data_dir() / "Cache"
    elif platform_name == 'macos':
        # macOS: ~/Library/Caches/Quick Document Convertor
        return Path.home() / "Library" / "Caches" / "Quick Document Convertor"
    elif platform_name == 'linux':
        # Linux: ~/.cache/quick-document-convertor
        return Path.home() / ".cache" / "quick-document-convertor"
    else:
        # Fallback
        return get_data_dir() / "cache"


def get_log_dir() -> Path:
    """
    Get platform-specific log directory.
    
    Returns:
        Path to log directory
    """
    platform_name = get_platform()
    
    if platform_name == 'windows':
        # Windows: %LOCALAPPDATA%\Quick Document Convertor\Logs
        return get_data_dir() / "Logs"
    elif platform_name == 'macos':
        # macOS: ~/Library/Logs/Quick Document Convertor
        return Path.home() / "Library" / "Logs" / "Quick Document Convertor"
    elif platform_name == 'linux':
        # Linux: ~/.local/share/quick-document-convertor/logs
        return get_data_dir() / "logs"
    else:
        # Fallback
        return get_data_dir() / "logs"


def is_supported_platform() -> bool:
    """
    Check if the current platform is supported.
    
    Returns:
        bool: True if platform is supported
    """
    return get_platform() in ['windows', 'linux', 'macos']


def get_executable_extension() -> str:
    """
    Get the executable file extension for the current platform.
    
    Returns:
        str: File extension including dot, or empty string
    """
    platform_name = get_platform()
    if platform_name == 'windows':
        return '.exe'
    else:
        return ''


def get_supported_file_formats() -> Dict[str, list]:
    """
    Get supported file formats for document conversion.
    
    Returns:
        Dict with input and output format lists
    """
    return {
        'input': [
            'pdf', 'docx', 'txt', 'html', 'rtf', 'epub', 'odt', 'csv'
        ],
        'output': [
            'markdown', 'html', 'pdf', 'docx', 'txt'
        ]
    }


def create_platform_directories() -> bool:
    """
    Create all necessary platform-specific directories.
    
    Returns:
        bool: True if successful
    """
    try:
        directories = [
            get_config_dir(),
            get_data_dir(),
            get_cache_dir(),
            get_log_dir()
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        return True
    except Exception as e:
        print(f"Error creating platform directories: {e}")
        return False


# Platform-specific integration modules
def get_platform_integration():
    """
    Get the appropriate platform integration module.
    
    Returns:
        Platform-specific integration module or None
    """
    platform_name = get_platform()
    
    try:
        if platform_name == 'linux':
            from . import linux_integration
            return linux_integration
        elif platform_name == 'macos':
            from . import macos_integration
            return macos_integration
        elif platform_name == 'windows':
            from . import windows_integration
            return windows_integration
        else:
            return None
    except ImportError:
        return None


__all__ = [
    'get_platform',
    'get_platform_info',
    'get_config_dir',
    'get_data_dir',
    'get_cache_dir',
    'get_log_dir',
    'is_supported_platform',
    'get_executable_extension',
    'get_supported_file_formats',
    'create_platform_directories',
    'get_platform_integration'
]
