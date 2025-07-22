"""
Cross-Platform Integration Tests for Quick Document Convertor

This module contains comprehensive test cases for Linux and macOS integration
using Test-Driven Development (TDD) approach.

Author: Beau Lewis
Project: Quick Document Convertor
"""

import os
import platform
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import the modules we're testing
import cross_platform
from packaging import get_app_info, check_dependencies


class TestPlatformDetection(unittest.TestCase):
    """Test platform detection functionality."""
    
    def test_get_platform_windows(self):
        """Test Windows platform detection."""
        with patch('platform.system', return_value='Windows'):
            self.assertEqual(cross_platform.get_platform(), 'windows')
    
    def test_get_platform_linux(self):
        """Test Linux platform detection."""
        with patch('platform.system', return_value='Linux'):
            self.assertEqual(cross_platform.get_platform(), 'linux')
    
    def test_get_platform_macos(self):
        """Test macOS platform detection."""
        with patch('platform.system', return_value='Darwin'):
            self.assertEqual(cross_platform.get_platform(), 'macos')
    
    def test_get_platform_unknown(self):
        """Test unknown platform detection."""
        with patch('platform.system', return_value='FreeBSD'):
            self.assertEqual(cross_platform.get_platform(), 'unknown')
    
    def test_is_supported_platform(self):
        """Test supported platform check."""
        with patch('cross_platform.get_platform', return_value='windows'):
            self.assertTrue(cross_platform.is_supported_platform())
        
        with patch('cross_platform.get_platform', return_value='linux'):
            self.assertTrue(cross_platform.is_supported_platform())
        
        with patch('cross_platform.get_platform', return_value='macos'):
            self.assertTrue(cross_platform.is_supported_platform())
        
        with patch('cross_platform.get_platform', return_value='unknown'):
            self.assertFalse(cross_platform.is_supported_platform())
    
    def test_get_platform_info(self):
        """Test platform info gathering."""
        info = cross_platform.get_platform_info()
        
        self.assertIn('platform', info)
        self.assertIn('system', info)
        self.assertIn('release', info)
        self.assertIn('version', info)
        self.assertIn('machine', info)
        self.assertIn('processor', info)
        self.assertIn('python_version', info)
        self.assertIn('architecture', info)


class TestPlatformDirectories(unittest.TestCase):
    """Test platform-specific directory handling."""
    
    def test_get_config_dir_windows(self):
        """Test Windows config directory."""
        with patch('cross_platform.get_platform', return_value='windows'):
            with patch('pathlib.Path.home', return_value=Path('/home/user')):
                config_dir = cross_platform.get_config_dir()
                expected = Path('/home/user/AppData/Roaming/Quick Document Convertor')
                self.assertEqual(config_dir, expected)
    
    def test_get_config_dir_linux(self):
        """Test Linux config directory."""
        with patch('cross_platform.get_platform', return_value='linux'):
            with patch('pathlib.Path.home', return_value=Path('/home/user')):
                config_dir = cross_platform.get_config_dir()
                expected = Path('/home/user/.config/quick-document-convertor')
                self.assertEqual(config_dir, expected)
    
    def test_get_config_dir_macos(self):
        """Test macOS config directory."""
        with patch('cross_platform.get_platform', return_value='macos'):
            with patch('pathlib.Path.home', return_value=Path('/Users/user')):
                config_dir = cross_platform.get_config_dir()
                expected = Path('/Users/user/Library/Application Support/Quick Document Convertor')
                self.assertEqual(config_dir, expected)
    
    def test_get_data_dir_linux(self):
        """Test Linux data directory."""
        with patch('cross_platform.get_platform', return_value='linux'):
            with patch('pathlib.Path.home', return_value=Path('/home/user')):
                data_dir = cross_platform.get_data_dir()
                expected = Path('/home/user/.local/share/quick-document-convertor')
                self.assertEqual(data_dir, expected)
    
    def test_get_cache_dir_linux(self):
        """Test Linux cache directory."""
        with patch('cross_platform.get_platform', return_value='linux'):
            with patch('pathlib.Path.home', return_value=Path('/home/user')):
                cache_dir = cross_platform.get_cache_dir()
                expected = Path('/home/user/.cache/quick-document-convertor')
                self.assertEqual(cache_dir, expected)
    
    def test_get_log_dir_macos(self):
        """Test macOS log directory."""
        with patch('cross_platform.get_platform', return_value='macos'):
            with patch('pathlib.Path.home', return_value=Path('/Users/user')):
                log_dir = cross_platform.get_log_dir()
                expected = Path('/Users/user/Library/Logs/Quick Document Convertor')
                self.assertEqual(log_dir, expected)


class TestFileFormats(unittest.TestCase):
    """Test file format handling."""
    
    def test_get_supported_file_formats(self):
        """Test supported file formats."""
        formats = cross_platform.get_supported_file_formats()
        
        self.assertIn('input', formats)
        self.assertIn('output', formats)
        
        # Check input formats
        expected_input = ['pdf', 'docx', 'txt', 'html', 'rtf', 'epub', 'odt', 'csv']
        for fmt in expected_input:
            self.assertIn(fmt, formats['input'])
        
        # Check output formats
        expected_output = ['markdown', 'html', 'pdf', 'docx', 'txt']
        for fmt in expected_output:
            self.assertIn(fmt, formats['output'])
    
    def test_get_executable_extension(self):
        """Test executable extension detection."""
        with patch('cross_platform.get_platform', return_value='windows'):
            self.assertEqual(cross_platform.get_executable_extension(), '.exe')
        
        with patch('cross_platform.get_platform', return_value='linux'):
            self.assertEqual(cross_platform.get_executable_extension(), '')
        
        with patch('cross_platform.get_platform', return_value='macos'):
            self.assertEqual(cross_platform.get_executable_extension(), '')


class TestLinuxDesktopIntegration(unittest.TestCase):
    """Test Linux desktop integration functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.temp_dir, ignore_errors=True))
    
    def test_desktop_file_creation(self):
        """Test .desktop file creation for Linux."""
        with patch('cross_platform.get_platform', return_value='linux'):
            # This test will be implemented when we create linux_integration.py
            pass

    def test_mime_type_registration(self):
        """Test MIME type registration for Linux."""
        with patch('cross_platform.get_platform', return_value='linux'):
            # This test will be implemented when we create linux_integration.py
            pass

    def test_file_associations(self):
        """Test file associations for Linux."""
        with patch('cross_platform.get_platform', return_value='linux'):
            # This test will be implemented when we create linux_integration.py
            pass


class TestMacOSIntegration(unittest.TestCase):
    """Test macOS integration functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.temp_dir, ignore_errors=True))

    def test_app_bundle_creation(self):
        """Test .app bundle creation for macOS."""
        with patch('cross_platform.get_platform', return_value='macos'):
            # This test will be implemented when we create macos_integration.py
            pass

    def test_info_plist_configuration(self):
        """Test Info.plist configuration for macOS."""
        with patch('cross_platform.get_platform', return_value='macos'):
            # This test will be implemented when we create macos_integration.py
            pass

    def test_uti_registration(self):
        """Test UTI registration for macOS."""
        with patch('cross_platform.get_platform', return_value='macos'):
            # This test will be implemented when we create macos_integration.py
            pass


class TestPackaging(unittest.TestCase):
    """Test packaging functionality."""
    
    def test_get_app_info(self):
        """Test application info retrieval."""
        app_info = get_app_info()
        
        self.assertIn('name', app_info)
        self.assertIn('version', app_info)
        self.assertIn('description', app_info)
        self.assertIn('author', app_info)
        self.assertEqual(app_info['name'], 'Quick Document Convertor')
        self.assertEqual(app_info['author'], 'Beau Lewis')
    
    def test_check_dependencies(self):
        """Test dependency checking."""
        deps = check_dependencies()
        
        self.assertIn('pyinstaller', deps)
        self.assertIn('pillow', deps)
        self.assertIsInstance(deps['pyinstaller'], bool)
        self.assertIsInstance(deps['pillow'], bool)
        
        # Platform-specific dependencies
        if platform.system() == 'Darwin':
            self.assertIn('py2app', deps)
        elif platform.system() == 'Linux':
            self.assertIn('python-dbus', deps)


class TestDirectoryCreation(unittest.TestCase):
    """Test directory creation functionality."""
    
    def test_create_platform_directories(self):
        """Test platform directory creation."""
        with patch('cross_platform.get_config_dir') as mock_config:
            with patch('cross_platform.get_data_dir') as mock_data:
                with patch('cross_platform.get_cache_dir') as mock_cache:
                    with patch('cross_platform.get_log_dir') as mock_log:
                        # Mock directory paths
                        temp_base = Path(tempfile.mkdtemp())
                        mock_config.return_value = temp_base / 'config'
                        mock_data.return_value = temp_base / 'data'
                        mock_cache.return_value = temp_base / 'cache'
                        mock_log.return_value = temp_base / 'logs'
                        
                        # Test directory creation
                        result = cross_platform.create_platform_directories()
                        self.assertTrue(result)
                        
                        # Verify directories were created
                        self.assertTrue((temp_base / 'config').exists())
                        self.assertTrue((temp_base / 'data').exists())
                        self.assertTrue((temp_base / 'cache').exists())
                        self.assertTrue((temp_base / 'logs').exists())
                        
                        # Cleanup
                        shutil.rmtree(temp_base, ignore_errors=True)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
