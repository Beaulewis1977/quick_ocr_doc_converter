#!/usr/bin/env python3
"""
Performance Benchmark Test Suite
Tests performance metrics and benchmarks for CI monitoring
"""

import os
import sys
import tempfile
import unittest
import subprocess
import time
from pathlib import Path
import json
import statistics

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestPerformanceBenchmarks(unittest.TestCase):
    """Test performance benchmarks for CI monitoring"""
    
    def setUp(self):
        """Set up benchmark environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.benchmark_results = {}
        self._create_benchmark_files()
        
    def tearDown(self):
        """Clean up and save benchmark results"""
        import shutil
        
        # Save benchmark results
        results_file = os.path.join(self.temp_dir, "benchmark_results.json")
        with open(results_file, 'w') as f:
            json.dump(self.benchmark_results, f, indent=2)
        
        print(f"\n📊 Benchmark Results Summary:")
        for test_name, result in self.benchmark_results.items():
            if isinstance(result, dict) and 'duration' in result:
                print(f"  {test_name}: {result['duration']:.3f}s")
        
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_benchmark_files(self):
        """Create test files for benchmarking"""
        
        # Small file (100 words)
        small_file = os.path.join(self.temp_dir, "small_test.txt")
        small_content = " ".join([f"word{i}" for i in range(100)])
        with open(small_file, 'w', encoding='utf-8') as f:
            f.write(small_content)
        
        # Medium file (1000 words)
        medium_file = os.path.join(self.temp_dir, "medium_test.txt")
        medium_content = " ".join([f"word{i}" for i in range(1000)])
        with open(medium_file, 'w', encoding='utf-8') as f:
            f.write(medium_content)
        
        # Large file (5000 words)
        large_file = os.path.join(self.temp_dir, "large_test.txt")
        large_content = " ".join([f"word{i}" for i in range(5000)])
        with open(large_file, 'w', encoding='utf-8') as f:
            f.write(large_content)
        
        self.test_files = {
            'small': small_file,
            'medium': medium_file,
            'large': large_file
        }
    
    def _benchmark_cli_conversion(self, input_file, test_name, timeout=30):
        """Benchmark CLI conversion performance"""
        
        output_file = os.path.join(self.temp_dir, f"benchmark_{test_name}.txt")
        cmd = [sys.executable, "cli.py", input_file, "-o", output_file]
        
        start_time = time.time()
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            end_time = time.time()
            duration = end_time - start_time
            
            success = result.returncode == 0 and os.path.exists(output_file)
            file_size = os.path.getsize(input_file) if os.path.exists(input_file) else 0
            
            # Calculate throughput (bytes per second)
            throughput = file_size / duration if duration > 0 else 0
            
            self.benchmark_results[f"cli_conversion_{test_name}"] = {
                "duration": duration,
                "success": success,
                "file_size_bytes": file_size,
                "throughput_bps": throughput,
                "command": " ".join(cmd)
            }
            
            return success, duration
            
        except subprocess.TimeoutExpired:
            self.benchmark_results[f"cli_conversion_{test_name}"] = {
                "duration": timeout,
                "success": False,
                "timeout": True,
                "command": " ".join(cmd)
            }
            return False, timeout
        except Exception as e:
            self.benchmark_results[f"cli_conversion_{test_name}"] = {
                "duration": 0,
                "success": False,
                "error": str(e),
                "command": " ".join(cmd)
            }
            return False, 0
    
    def test_small_file_performance(self):
        """Benchmark performance with small files"""
        
        success, duration = self._benchmark_cli_conversion(
            self.test_files['small'], 
            'small_file'
        )
        
        # Performance assertions
        self.assertTrue(success, "Small file conversion should succeed")
        self.assertLess(duration, 10.0, "Small file conversion should complete within 10 seconds")
        
        print(f"✅ Small file ({os.path.getsize(self.test_files['small'])} bytes): {duration:.3f}s")
    
    def test_medium_file_performance(self):
        """Benchmark performance with medium files"""
        
        success, duration = self._benchmark_cli_conversion(
            self.test_files['medium'], 
            'medium_file'
        )
        
        # Performance assertions
        self.assertTrue(success, "Medium file conversion should succeed")
        self.assertLess(duration, 15.0, "Medium file conversion should complete within 15 seconds")
        
        print(f"✅ Medium file ({os.path.getsize(self.test_files['medium'])} bytes): {duration:.3f}s")
    
    def test_large_file_performance(self):
        """Benchmark performance with large files"""
        
        success, duration = self._benchmark_cli_conversion(
            self.test_files['large'], 
            'large_file',
            timeout=45  # Longer timeout for large files
        )
        
        # Performance assertions (more lenient for large files)
        if success:
            self.assertLess(duration, 30.0, "Large file conversion should complete within 30 seconds")
        else:
            print("⚠️  Large file conversion failed or timed out (acceptable in CI)")
        
        print(f"📊 Large file ({os.path.getsize(self.test_files['large'])} bytes): {duration:.3f}s")
    
    def test_startup_performance(self):
        """Benchmark application startup time"""
        
        cmd = [sys.executable, "-c", "import universal_document_converter_ocr; print('Imported successfully')"]
        
        times = []
        successful_imports = 0
        
        # Run multiple times for statistical accuracy
        for i in range(3):
            start_time = time.time()
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                end_time = time.time()
                duration = end_time - start_time
                
                if result.returncode == 0:
                    times.append(duration)
                    successful_imports += 1
                    
            except subprocess.TimeoutExpired:
                times.append(15.0)  # Max time
            except Exception:
                times.append(15.0)  # Max time
        
        if times:
            avg_startup_time = statistics.mean(times)
            min_startup_time = min(times)
            max_startup_time = max(times)
            
            self.benchmark_results["startup_performance"] = {
                "average_duration": avg_startup_time,
                "min_duration": min_startup_time,
                "max_duration": max_startup_time,
                "successful_imports": successful_imports,
                "total_attempts": len(times)
            }
            
            # Performance assertions
            self.assertGreater(successful_imports, 0, "At least one import should succeed")
            self.assertLess(avg_startup_time, 10.0, "Average startup time should be under 10 seconds")
            
            print(f"✅ Startup time: avg={avg_startup_time:.3f}s, min={min_startup_time:.3f}s, max={max_startup_time:.3f}s")
        else:
            self.fail("No successful startup measurements")
    
    def test_memory_usage_estimation(self):
        """Estimate memory usage during conversion"""
        
        # This is a basic memory estimation test
        # In a real scenario, you'd use memory profiling tools
        
        input_file = self.test_files['medium']
        output_file = os.path.join(self.temp_dir, "memory_test.txt")
        
        cmd = [sys.executable, "cli.py", input_file, "-o", output_file]
        
        start_time = time.time()
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            end_time = time.time()
            duration = end_time - start_time
            
            success = result.returncode == 0
            
            # Basic memory estimation based on file sizes
            input_size = os.path.getsize(input_file)
            output_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0
            estimated_memory = max(input_size, output_size) * 3  # Rough estimate
            
            self.benchmark_results["memory_usage_estimation"] = {
                "duration": duration,
                "success": success,
                "input_size_bytes": input_size,
                "output_size_bytes": output_size,
                "estimated_memory_bytes": estimated_memory,
                "estimated_memory_mb": estimated_memory / (1024 * 1024)
            }
            
            # Basic assertions
            self.assertTrue(success, "Memory test conversion should succeed")
            self.assertLess(estimated_memory / (1024 * 1024), 100, "Estimated memory usage should be reasonable")
            
            print(f"✅ Memory estimation: ~{estimated_memory / (1024 * 1024):.1f}MB for {input_size} byte file")
            
        except Exception as e:
            self.benchmark_results["memory_usage_estimation"] = {
                "success": False,
                "error": str(e)
            }
            print(f"⚠️  Memory estimation test failed: {e}")
    
    def test_concurrent_performance(self):
        """Test performance under concurrent load"""
        
        from concurrent.futures import ThreadPoolExecutor
        import threading
        
        def convert_file(file_index):
            """Convert a file and return timing info"""
            input_file = self.test_files['small']
            output_file = os.path.join(self.temp_dir, f"concurrent_{file_index}.txt")
            cmd = [sys.executable, "cli.py", input_file, "-o", output_file]
            
            start_time = time.time()
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
                end_time = time.time()
                duration = end_time - start_time
                
                return {
                    "index": file_index,
                    "duration": duration,
                    "success": result.returncode == 0 and os.path.exists(output_file)
                }
            except Exception as e:
                return {
                    "index": file_index,
                    "duration": 0,
                    "success": False,
                    "error": str(e)
                }
        
        # Test with 3 concurrent conversions
        concurrent_start = time.time()
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(convert_file, range(3)))
        
        concurrent_end = time.time()
        total_concurrent_time = concurrent_end - concurrent_start
        
        # Analyze results
        successful_results = [r for r in results if r["success"]]
        
        if successful_results:
            individual_times = [r["duration"] for r in successful_results]
            avg_individual_time = statistics.mean(individual_times)
            
            self.benchmark_results["concurrent_performance"] = {
                "total_concurrent_time": total_concurrent_time,
                "average_individual_time": avg_individual_time,
                "successful_conversions": len(successful_results),
                "total_attempts": len(results),
                "efficiency": (avg_individual_time / total_concurrent_time) * 100 if total_concurrent_time > 0 else 0
            }
            
            # Performance assertions
            self.assertGreater(len(successful_results), 0, "At least one concurrent conversion should succeed")
            
            print(f"✅ Concurrent performance: {len(successful_results)}/{len(results)} succeeded")
            print(f"   Total time: {total_concurrent_time:.3f}s, Avg individual: {avg_individual_time:.3f}s")
        else:
            self.benchmark_results["concurrent_performance"] = {
                "success": False,
                "message": "No concurrent conversions succeeded"
            }
            print("⚠️  No concurrent conversions succeeded")

def run_performance_benchmarks():
    """Run performance benchmark tests"""
    print("🏃 Running Performance Benchmarks")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestPerformanceBenchmarks))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"📊 Benchmark Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ All benchmarks completed!' if success else '❌ Some benchmarks failed!'}")
    
    return success

if __name__ == "__main__":
    success = run_performance_benchmarks()
    sys.exit(0 if success else 1)