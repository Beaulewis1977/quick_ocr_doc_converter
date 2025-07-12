"""
Packaging Module for Quick Document Convertor

This module provides cross-platform packaging functionality for creating
distributable packages on Windows, Linux, and macOS.

Author: Beau Lewis
Project: Quick Document Convertor
"""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PackagingError(Exception):
    """Custom exception for packaging errors."""
    pass


def get_app_info() -> Dict[str, str]:
    """
    Get application information for packaging.
    
    Returns:
        Dict containing app metadata
    """
    return {
        'name': 'Quick Document Convertor',
        'version': '2.0.0',
        'description': 'Enterprise document conversion tool',
        'author': 'Beau Lewis',
        'email': 'blewisxx@gmail.com',
        'url': 'https://github.com/Beaulewis1977/quick_doc_convertor',
        'license': 'MIT',
        'keywords': ['document', 'conversion', 'markdown', 'pdf', 'docx'],
        'classifiers': [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Topic :: Office/Business',
            'Topic :: Text Processing',
            'Topic :: Utilities'
        ]
    }


def get_supported_formats() -> Dict[str, List[str]]:
    """
    Get supported file formats for packaging metadata.
    
    Returns:
        Dict with input and output formats
    """
    return {
        'input': ['pdf', 'docx', 'txt', 'html', 'rtf', 'epub', 'odt', 'csv'],
        'output': ['markdown', 'html', 'pdf', 'docx', 'txt']
    }


def get_mime_types() -> List[str]:
    """
    Get MIME types for file associations.
    
    Returns:
        List of MIME types
    """
    return [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'text/html',
        'application/rtf',
        'application/epub+zip',
        'application/vnd.oasis.opendocument.text',
        'text/csv'
    ]


def get_file_extensions() -> List[str]:
    """
    Get file extensions for file associations.
    
    Returns:
        List of file extensions
    """
    return [
        '.pdf', '.docx', '.txt', '.html', '.rtf', '.epub', '.odt', '.csv'
    ]


def check_dependencies() -> Dict[str, bool]:
    """
    Check if packaging dependencies are available.
    
    Returns:
        Dict with dependency availability status
    """
    dependencies = {
        'pyinstaller': False,
        'py2app': False,
        'python-dbus': False,
        'pillow': False
    }
    
    # Check PyInstaller
    try:
        import PyInstaller
        dependencies['pyinstaller'] = True
    except ImportError:
        pass
    
    # Check py2app (macOS only)
    if platform.system() == 'Darwin':
        try:
            import py2app
            dependencies['py2app'] = True
        except ImportError:
            pass
    
    # Check python-dbus (Linux only)
    if platform.system() == 'Linux':
        try:
            import dbus
            dependencies['python-dbus'] = True
        except ImportError:
            pass
    
    # Check Pillow
    try:
        import PIL
        dependencies['pillow'] = True
    except ImportError:
        pass
    
    return dependencies


def install_dependencies() -> bool:
    """
    Install required packaging dependencies.
    
    Returns:
        bool: True if successful
    """
    try:
        # Base dependencies
        base_deps = ['pyinstaller>=5.0', 'pillow>=9.0']
        
        # Platform-specific dependencies
        if platform.system() == 'Darwin':
            base_deps.append('py2app>=0.28')
        elif platform.system() == 'Linux':
            base_deps.append('python-dbus')
        
        for dep in base_deps:
            print(f"Installing {dep}...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', dep
            ])
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to project root
    """
    # Assume this file is in packaging/ subdirectory
    return Path(__file__).parent.parent


def get_main_script() -> Path:
    """
    Get the main application script.
    
    Returns:
        Path to main script
    """
    return get_project_root() / "universal_document_converter.py"


def get_icon_path() -> Optional[Path]:
    """
    Get the application icon path.
    
    Returns:
        Path to icon file or None
    """
    project_root = get_project_root()
    
    # Look for common icon files
    icon_files = [
        'icon.ico', 'icon.icns', 'icon.png',
        'app_icon.ico', 'app_icon.icns', 'app_icon.png'
    ]
    
    for icon_file in icon_files:
        icon_path = project_root / icon_file
        if icon_path.exists():
            return icon_path
    
    return None


def create_build_info() -> Dict[str, str]:
    """
    Create build information for packaging.
    
    Returns:
        Dict with build metadata
    """
    import datetime
    
    return {
        'build_date': datetime.datetime.now().isoformat(),
        'platform': platform.system(),
        'architecture': platform.machine(),
        'python_version': sys.version,
        'build_user': os.environ.get('USER', os.environ.get('USERNAME', 'unknown'))
    }


def get_package_builder():
    """
    Get the appropriate package builder for the current platform.
    
    Returns:
        Platform-specific package builder module or None
    """
    system = platform.system()
    
    try:
        if system == 'Linux':
            from . import build_linux
            return build_linux
        elif system == 'Darwin':
            from . import build_macos
            return build_macos
        elif system == 'Windows':
            from . import build_windows
            return build_windows
        else:
            return None
    except ImportError:
        return None


__all__ = [
    'PackagingError',
    'get_app_info',
    'get_supported_formats',
    'get_mime_types',
    'get_file_extensions',
    'check_dependencies',
    'install_dependencies',
    'get_project_root',
    'get_main_script',
    'get_icon_path',
    'create_build_info',
    'get_package_builder'
]
