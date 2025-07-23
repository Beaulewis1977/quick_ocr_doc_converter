#!/usr/bin/env python3
"""
Legacy DLL Builder - Testing Commands
Extracted from universal_document_converter.py legacy functionality
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Optional, List
import logging

class DLLTester:
    """Handles DLL testing functionality"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.test_file = None
    
    def set_test_file(self, file_path: str) -> bool:
        """Set the test file for conversion testing"""
        test_file = Path(file_path)
        if not test_file.exists():
            self.logger.error(f"❌ Test file does not exist: {file_path}")
            return False
        
        self.test_file = test_file
        self.logger.info(f"📁 Selected test file: {file_path}")
        return True
    
    def test_dll_conversion(self) -> bool:
        """Test DLL conversion functionality"""
        if not self.test_file:
            self.logger.error("❌ No test file selected")
            return False
        
        if not self.test_file.exists():
            self.logger.error("❌ Test file does not exist")
            return False
        
        self.logger.info(f"🧪 Testing DLL conversion: {self.test_file}")
        
        try:
            # Test CLI backend (which the DLL uses)
            output_file = self.test_file.with_suffix('.converted.txt')
            
            # Run conversion through CLI
            result = subprocess.run([
                sys.executable, "cli.py",
                str(self.test_file),
                str(output_file),
                "--format", "txt"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                if output_file.exists():
                    # Check output content
                    content = output_file.read_text()[:200]  # First 200 chars
                    if content.strip():
                        self.logger.info("✅ Conversion successful!")
                        self.logger.info(f"   Output preview: {content}...")
                        
                        # Clean up test file
                        output_file.unlink()
                        return True
                    else:
                        self.logger.error("❌ Conversion completed but no output file")
                        return False
                else:
                    self.logger.error("❌ Conversion completed but no output file")
                    return False
            else:
                self.logger.error(f"❌ Conversion failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Test error: {str(e)}")
            return False
    
    def test_dll_functions(self) -> bool:
        """Test individual DLL functions"""
        self.logger.info("🔍 Testing DLL functions...")
        
        try:
            # Test the CLI backend that powers the DLL
            
            # Test help function
            result = subprocess.run([
                sys.executable, "cli.py", "--help"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.logger.info("✅ CLI help function working")
            else:
                self.logger.error("❌ CLI help function failed")
                return False
            
            # Test format detection
            result = subprocess.run([
                sys.executable, "cli.py", "--list-formats"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.logger.info("✅ Format detection working")
                self.logger.info(f"   Supported formats: {result.stdout.strip()}")
            else:
                self.logger.error("❌ Format detection failed")
                return False
            
            # Test version function
            result = subprocess.run([
                sys.executable, "cli.py", "--version"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.logger.info("✅ Version function working")
                self.logger.info(f"   Version: {result.stdout.strip()}")
            else:
                self.logger.error("❌ Version function failed")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Function test error: {str(e)}")
            return False
    
    def performance_test_dll(self, num_tests: int = 5) -> bool:
        """Run performance test on DLL"""
        self.logger.info("📊 Running performance test...")
        
        if not self.test_file:
            self.logger.error("❌ Need a valid test file for performance testing")
            return False
        
        try:
            times = []
            
            for i in range(num_tests):
                output_file = self.test_file.with_suffix(f'.perf_test_{i}.txt')
                
                start_time = time.time()
                result = subprocess.run([
                    sys.executable, "cli.py",
                    str(self.test_file),
                    str(output_file),
                    "--format", "txt"
                ], capture_output=True, text=True, timeout=60)
                end_time = time.time()
                
                duration = end_time - start_time
                
                if result.returncode == 0 and output_file.exists():
                    times.append(duration)
                    self.logger.info(f"✅ Test {i+1}: {duration:.2f} seconds")
                    output_file.unlink()  # Clean up
                else:
                    self.logger.error(f"❌ Test {i+1}: Failed")
            
            if times:
                avg_time = sum(times) / len(times)
                self.logger.info(f"📊 Average conversion time: {avg_time:.2f} seconds")
                self.logger.info(f"📊 Fastest: {min(times):.2f}s, Slowest: {max(times):.2f}s")
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Performance test error: {str(e)}")
            return False
    
    def run_comprehensive_test(self) -> bool:
        """Run comprehensive DLL test suite"""
        self.logger.info("🧪 Running comprehensive DLL test suite...")
        
        tests = [
            ("Function Tests", self.test_dll_functions),
            ("Conversion Test", self.test_dll_conversion),
            ("Performance Test", lambda: self.performance_test_dll(3))
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            self.logger.info(f"\n--- {test_name} ---")
            try:
                if test_func():
                    self.logger.info(f"✅ {test_name}: PASSED")
                    passed += 1
                else:
                    self.logger.error(f"❌ {test_name}: FAILED")
                    failed += 1
            except Exception as e:
                self.logger.error(f"❌ {test_name}: ERROR - {str(e)}")
                failed += 1
        
        self.logger.info(f"\n📊 Test Results: {passed} passed, {failed} failed")
        return failed == 0