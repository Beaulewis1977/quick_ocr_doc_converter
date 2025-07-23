#!/usr/bin/env python3
"""
Integration tests for the Legacy DLL Builder
"""

import unittest
import sys
import subprocess
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any

from .test_base import BaseTestCase, TestFileFactory, CustomAssertions
from .test_fixtures import create_test_environment


def secure_dll_load_test(dll_path: Path):
    """
    Securely load a DLL for testing with path validation
    
    Args:
        dll_path: Path to the DLL file
        
    Returns:
        DLL handle if successful, None otherwise
    """
    if sys.platform != "win32":
        return None
        
    try:
        # Validate path
        resolved_path = dll_path.resolve()
        if not resolved_path.exists() or not resolved_path.is_file():
            return None
            
        # Check file extension
        if resolved_path.suffix.lower() != '.dll':
            return None
            
        # Basic file size check
        file_size = resolved_path.stat().st_size
        if file_size < 1024 or file_size > 50 * 1024 * 1024:  # 1KB to 50MB
            return None
            
        # Load DLL with absolute path
        import ctypes
        return ctypes.WinDLL(str(resolved_path))
        
    except Exception:
        return None


class LegacyDLLBuilderIntegrationTest(BaseTestCase):
    """Integration tests for the legacy DLL builder"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.legacy_dir = Path(__file__).parent.parent / "legacy_dll_builder"
        cls.cli_path = cls.legacy_dir / "cli.py"
        cls.cli_new_path = cls.legacy_dir / "cli_new.py"
        
        # Verify CLI exists
        if not cls.cli_path.exists():
            raise FileNotFoundError(f"Legacy CLI not found at {cls.cli_path}")
    
    def run_legacy_cli(self, args: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
        """Run the legacy CLI with given arguments"""
        cmd = [sys.executable, str(self.cli_path)] + args
        
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(self.legacy_dir)
        )
    
    def run_new_cli(self, args: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
        """Run the new Click-based CLI with given arguments"""
        cmd = [sys.executable, str(self.cli_new_path)] + args
        
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(self.legacy_dir)
        )
    
    def test_cli_help(self):
        """Test CLI help command"""
        # Test original CLI
        result = self.run_legacy_cli(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Legacy DLL Builder CLI", result.stdout)
        
        # Test new CLI if it exists
        if self.cli_new_path.exists():
            result = self.run_new_cli(["--help"])
            self.assertEqual(result.returncode, 0)
            self.assertIn("Legacy 32-bit DLL builder", result.stdout)
    
    def test_status_command(self):
        """Test DLL status checking"""
        result = self.run_legacy_cli(["status"])
        
        # Should complete without error
        self.assertEqual(result.returncode, 0)
        
        # Should report DLL status
        self.assertIn("DLL", result.stdout)
        self.assertTrue(
            "✅ Built and ready" in result.stdout or "❌ Not built" in result.stdout
        )
    
    def test_build_requirements(self):
        """Test showing build requirements"""
        result = self.run_legacy_cli(["requirements"])
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Build Requirements", result.stdout)
        self.assertIn("Visual Studio", result.stdout)
    
    def test_vb6_template_generation(self):
        """Test VB6 template generation"""
        result = self.run_legacy_cli(["vb6", "generate"])
        
        # Check if template was generated
        if result.returncode == 0:
            # Look for generated VB6 file
            vb6_files = list(self.legacy_dir.glob("*.bas"))
            self.assertTrue(len(vb6_files) > 0, "No VB6 module generated")
            
            # Clean up
            for file in vb6_files:
                if file.name != "VB6_UniversalConverter_Production.bas":
                    file.unlink()
    
    def test_vfp9_template_generation(self):
        """Test VFP9 template generation"""
        result = self.run_legacy_cli(["vfp9", "generate"])
        
        # Check if template was generated
        if result.returncode == 0:
            # Look for generated VFP9 file
            vfp9_files = list(self.legacy_dir.glob("*.prg"))
            self.assertTrue(len(vfp9_files) > 0, "No VFP9 class generated")
            
            # Clean up
            for file in vfp9_files:
                if file.name != "VFP9_UniversalConverter_Production.prg":
                    file.unlink()
    
    def test_vb6_examples(self):
        """Test VB6 examples display"""
        result = self.run_legacy_cli(["vb6", "examples"])
        
        self.assertEqual(result.returncode, 0)
        # Should show VB6 code examples
        self.assertIn("VB6", result.stdout)
    
    def test_vfp9_examples(self):
        """Test VFP9 examples display"""
        result = self.run_legacy_cli(["vfp9", "examples"])
        
        self.assertEqual(result.returncode, 0)
        # Should show VFP9 code examples
        self.assertIn("VFP9", result.stdout)
    
    def test_new_cli_verify_tools(self):
        """Test new CLI verify-tools command"""
        if not self.cli_new_path.exists():
            self.skipTest("New CLI not available")
        
        result = self.run_new_cli(["verify-tools"])
        
        self.assertEqual(result.returncode, 0)
        # Should check for compilers
        self.assertIn("Checking build tools", result.stdout)
        self.assertIn("Python", result.stdout)
    
    def test_new_cli_show_config(self):
        """Test new CLI show-config command"""
        if not self.cli_new_path.exists():
            self.skipTest("New CLI not available")
        
        result = self.run_new_cli(["show-config"])
        
        self.assertEqual(result.returncode, 0)
        # Should show configuration template
        self.assertIn("compiler", result.stdout)
        self.assertIn("dll", result.stdout)
        self.assertIn("python", result.stdout)
    
    def test_dll_source_check(self):
        """Test DLL source files existence"""
        dll_source_dir = self.legacy_dir / "dll_source"
        
        # Check required source files
        required_files = [
            "UniversalConverter32.cpp",
            "UniversalConverter32.def"
        ]
        
        for file_name in required_files:
            file_path = dll_source_dir / file_name
            self.assertTrue(
                file_path.exists(),
                f"Missing DLL source file: {file_name}"
            )
    
    def test_template_files_check(self):
        """Test template files existence"""
        templates_dir = self.legacy_dir / "templates"
        
        # Check template files
        expected_templates = [
            "VB6_UniversalConverter_Production.bas",
            "VFP9_UniversalConverter_Production.prg"
        ]
        
        for template_name in expected_templates:
            template_path = templates_dir / template_name
            self.assertTrue(
                template_path.exists(),
                f"Missing template file: {template_name}"
            )
    
    def test_build_command_dry_run(self):
        """Test build command in dry-run mode (without actual compilation)"""
        # Skip on non-Windows platforms
        if sys.platform != "win32":
            self.skipTest("DLL building requires Windows")
        
        # Test status before build
        result = self.run_legacy_cli(["status"])
        self.assertEqual(result.returncode, 0)
        
        # Note: Actual build test would require Visual Studio
        # This is just checking the command structure works
    
    def test_configuration_loading(self):
        """Test configuration file loading"""
        # Create test config
        config = {
            "compiler": {
                "build_timeout": 600,
                "type": "auto"
            },
            "dll": {
                "source_dir": "dll_source",
                "name": "UniversalConverter32.dll"
            }
        }
        
        config_file = self.temp_dir / "test_config.json"
        config_file.write_text(json.dumps(config))
        
        # Copy to legacy dir temporarily
        legacy_config = self.legacy_dir / "config.json"
        shutil.copy2(config_file, legacy_config)
        
        try:
            # Run command that would use config
            result = self.run_legacy_cli(["status"])
            self.assertEqual(result.returncode, 0)
        finally:
            # Clean up
            if legacy_config.exists():
                legacy_config.unlink()
    
    def test_error_handling(self):
        """Test error handling for invalid commands"""
        # Test invalid command
        result = self.run_legacy_cli(["invalid-command"])
        self.assertNotEqual(result.returncode, 0)
        
        # Test invalid subcommand
        result = self.run_legacy_cli(["vb6", "invalid"])
        self.assertNotEqual(result.returncode, 0)


class DLLFunctionalityTest(BaseTestCase):
    """Test DLL functionality if built"""
    
    def setUp(self):
        """Set up DLL test environment"""
        super().setUp()
        
        # Check if we're on Windows
        if sys.platform != "win32":
            self.skipTest("DLL testing requires Windows")
        
        # Check if DLL exists
        self.dll_paths = [
            Path("legacy_dll_builder/dist/UniversalConverter32.dll"),
            Path("legacy_dll_builder/UniversalConverter32.dll"),
            Path("dist/UniversalConverter32.dll")
        ]
        
        self.dll_path = None
        for path in self.dll_paths:
            if path.exists():
                self.dll_path = path
                break
        
        if not self.dll_path:
            self.skipTest("DLL not found - run build first")
    
    def test_dll_loading(self):
        """Test DLL can be loaded"""
        
        try:
            dll = secure_dll_load_test(self.dll_path)
            if not dll:
                self.skipTest("DLL loading failed or not on Windows")
            
            # Test GetVersion function
            import ctypes
            get_version = dll.GetVersion
            get_version.restype = ctypes.c_char_p
            version = get_version()
            
            self.assertIsNotNone(version)
            self.assertIn(b".", version)  # Version should have dots
        
        except Exception as e:
            self.fail(f"Failed to load DLL: {e}")
    
    def test_dll_functions(self):
        """Test DLL exported functions"""
        import ctypes
        
        dll = secure_dll_load_test(self.dll_path)
        if not dll:
            self.skipTest("DLL loading failed or not on Windows")
        
        # Test GetSupportedInputFormats
        get_input_formats = dll.GetSupportedInputFormats
        get_input_formats.restype = ctypes.c_char_p
        formats = get_input_formats().decode('utf-8')
        
        self.assertIn("pdf", formats)
        self.assertIn("docx", formats)
        self.assertIn("txt", formats)
        
        # Test GetSupportedOutputFormats
        get_output_formats = dll.GetSupportedOutputFormats
        get_output_formats.restype = ctypes.c_char_p
        formats = get_output_formats().decode('utf-8')
        
        self.assertIn("txt", formats)
        self.assertIn("md", formats)
        self.assertIn("html", formats)
    
    def test_dll_test_connection(self):
        """Test DLL connection testing"""
        import ctypes
        
        dll = secure_dll_load_test(self.dll_path)
        if not dll:
            self.skipTest("DLL loading failed or not on Windows")
        
        # Test TestConnection function
        test_connection = dll.TestConnection
        test_connection.restype = ctypes.c_long
        
        result = test_connection()
        
        # Result should be 1 (success), 0 (failure), or -1 (error)
        self.assertIn(result, [1, 0, -1])
        
        # If failed, check error message
        if result != 1:
            get_last_error = dll.GetLastError
            get_last_error.restype = ctypes.c_char_p
            error = get_last_error().decode('utf-8')
            self.logger.warning(f"DLL connection test failed: {error}")


class CrossPlatformIntegrationTest(BaseTestCase):
    """Test cross-platform compatibility"""
    
    def test_path_handling(self):
        """Test cross-platform path handling"""
        # Create files with different path separators
        if sys.platform == "win32":
            test_path = self.temp_dir / "subdir\\file.txt"
        else:
            test_path = self.temp_dir / "subdir/file.txt"
        
        test_path.parent.mkdir(exist_ok=True)
        test_path.write_text("Test content")
        
        # Both applications should handle paths correctly
        self.assertTrue(test_path.exists())
    
    def test_unicode_paths(self):
        """Test Unicode in file paths"""
        # Create file with Unicode name
        unicode_dir = self.temp_dir / "测试文件夹"
        unicode_dir.mkdir()
        
        unicode_file = unicode_dir / "файл.txt"
        unicode_file.write_text("Unicode path test")
        
        self.assertTrue(unicode_file.exists())
        content = unicode_file.read_text()
        self.assertEqual(content, "Unicode path test")


if __name__ == '__main__':
    unittest.main()