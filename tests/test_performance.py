#!/usr/bin/env python3
"""
Performance benchmarking utilities for Universal Document Converter
"""

import time
import statistics
import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional, Tuple
from datetime import datetime
from functools import wraps
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from .test_base import BaseTestCase, TestFileFactory
from .test_fixtures import PerformanceData, DOCUMENT_TEMPLATES


class PerformanceBenchmark:
    """Performance benchmarking framework"""
    
    def __init__(self, name: str):
        self.name = name
        self.results = []
        self.metadata = {
            'name': name,
            'start_time': None,
            'end_time': None,
            'system_info': self._get_system_info()
        }
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Collect system information"""
        import platform
        import psutil
        
        return {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'cpu_count': multiprocessing.cpu_count(),
            'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2)
        }
    
    def measure(self, func: Callable, *args, **kwargs) -> Tuple[float, Any]:
        """Measure execution time of a function"""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        elapsed = end_time - start_time
        return elapsed, result
    
    def run_benchmark(self, func: Callable, iterations: int = 10, 
                     warmup: int = 2, *args, **kwargs) -> Dict[str, Any]:
        """Run a benchmark with multiple iterations"""
        self.metadata['start_time'] = datetime.now().isoformat()
        
        # Warmup runs
        for _ in range(warmup):
            func(*args, **kwargs)
        
        # Actual benchmark runs
        times = []
        for i in range(iterations):
            elapsed, _ = self.measure(func, *args, **kwargs)
            times.append(elapsed)
            
            self.results.append({
                'iteration': i,
                'time': elapsed,
                'timestamp': datetime.now().isoformat()
            })
        
        self.metadata['end_time'] = datetime.now().isoformat()
        
        # Calculate statistics
        stats = {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'iterations': iterations,
            'total_time': sum(times)
        }
        
        return stats
    
    def save_results(self, output_dir: Path):
        """Save benchmark results to files"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save detailed results as JSON
        json_path = output_dir / f"{self.name}_results.json"
        with open(json_path, 'w') as f:
            json.dump({
                'metadata': self.metadata,
                'results': self.results
            }, f, indent=2)
        
        # Save summary as CSV
        csv_path = output_dir / f"{self.name}_summary.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['iteration', 'time'])
            writer.writeheader()
            writer.writerows(self.results)
    
    def compare_with(self, other: 'PerformanceBenchmark') -> Dict[str, Any]:
        """Compare with another benchmark"""
        self_times = [r['time'] for r in self.results]
        other_times = [r['time'] for r in other.results]
        
        self_mean = statistics.mean(self_times)
        other_mean = statistics.mean(other_times)
        
        return {
            'speedup': other_mean / self_mean,
            'improvement_percent': ((other_mean - self_mean) / other_mean) * 100,
            'self_mean': self_mean,
            'other_mean': other_mean
        }


class ConversionBenchmarks:
    """Specific benchmarks for document conversion"""
    
    def __init__(self, converter_func: Callable):
        self.converter_func = converter_func
        self.temp_dir = Path("benchmark_temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def benchmark_single_file(self, file_size_kb: int, 
                            file_format: str = 'txt') -> float:
        """Benchmark single file conversion"""
        # Create test file
        input_file = self.temp_dir / f"test_{file_size_kb}kb.{file_format}"
        output_file = self.temp_dir / f"output_{file_size_kb}kb.txt"
        
        # Generate content
        content = 'x' * (file_size_kb * 1024)
        
        if file_format == 'txt':
            TestFileFactory.create_text_file(input_file, content)
        elif file_format == 'html':
            TestFileFactory.create_html_file(input_file, f"<p>{content}</p>")
        elif file_format == 'md':
            TestFileFactory.create_markdown_file(input_file, content)
        
        # Measure conversion time
        benchmark = PerformanceBenchmark(f"single_file_{file_size_kb}kb")
        elapsed, _ = benchmark.measure(
            self.converter_func, 
            str(input_file), 
            str(output_file)
        )
        
        return elapsed
    
    def benchmark_batch_conversion(self, file_count: int, 
                                 file_size_kb: int = 10) -> Dict[str, Any]:
        """Benchmark batch file conversion"""
        # Create test files
        batch_dir = self.temp_dir / "batch"
        batch_dir.mkdir(exist_ok=True)
        
        files = PerformanceData.generate_test_files(file_count, batch_dir)
        
        # Sequential processing
        seq_benchmark = PerformanceBenchmark("batch_sequential")
        seq_time, _ = seq_benchmark.measure(
            self._convert_files_sequential, files
        )
        
        # Parallel processing
        par_benchmark = PerformanceBenchmark("batch_parallel")
        par_time, _ = par_benchmark.measure(
            self._convert_files_parallel, files
        )
        
        return {
            'sequential_time': seq_time,
            'parallel_time': par_time,
            'speedup': seq_time / par_time,
            'files_per_second_seq': file_count / seq_time,
            'files_per_second_par': file_count / par_time
        }
    
    def _convert_files_sequential(self, files: List[Path]):
        """Convert files sequentially"""
        for file in files:
            output = file.with_suffix('.converted.txt')
            self.converter_func(str(file), str(output))
    
    def _convert_files_parallel(self, files: List[Path], max_workers: int = 4):
        """Convert files in parallel"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for file in files:
                output = file.with_suffix('.converted.txt')
                future = executor.submit(self.converter_func, str(file), str(output))
                futures.append(future)
            
            # Wait for all to complete
            for future in futures:
                future.result()
    
    def benchmark_memory_usage(self, file_size_mb: int) -> Dict[str, Any]:
        """Benchmark memory usage during conversion"""
        import psutil
        import gc
        
        # Create large test file
        input_file = self.temp_dir / f"large_{file_size_mb}mb.txt"
        output_file = self.temp_dir / f"large_output_{file_size_mb}mb.txt"
        
        # Generate large content
        content = 'x' * (file_size_mb * 1024 * 1024)
        TestFileFactory.create_text_file(input_file, content)
        
        # Measure memory before
        gc.collect()
        process = psutil.Process()
        mem_before = process.memory_info().rss / (1024 * 1024)  # MB
        
        # Perform conversion
        start_time = time.perf_counter()
        self.converter_func(str(input_file), str(output_file))
        end_time = time.perf_counter()
        
        # Measure memory after
        mem_after = process.memory_info().rss / (1024 * 1024)  # MB
        
        return {
            'file_size_mb': file_size_mb,
            'memory_before_mb': mem_before,
            'memory_after_mb': mem_after,
            'memory_increase_mb': mem_after - mem_before,
            'conversion_time': end_time - start_time,
            'mb_per_second': file_size_mb / (end_time - start_time)
        }


class PerformanceTestCase(BaseTestCase):
    """Base class for performance tests"""
    
    def setUp(self):
        super().setUp()
        self.benchmarks = []
    
    def tearDown(self):
        # Save all benchmark results
        if self.benchmarks:
            results_dir = Path("benchmark_results") / datetime.now().strftime("%Y%m%d_%H%M%S")
            results_dir.mkdir(parents=True, exist_ok=True)
            
            for benchmark in self.benchmarks:
                benchmark.save_results(results_dir)
        
        super().tearDown()
    
    def assertPerformance(self, elapsed_time: float, max_time: float, 
                         operation: str = "Operation"):
        """Assert that performance meets requirements"""
        self.assertLessEqual(
            elapsed_time, max_time,
            f"{operation} took {elapsed_time:.2f}s, exceeding limit of {max_time}s"
        )
    
    def assertSpeedup(self, baseline_time: float, optimized_time: float,
                     min_speedup: float = 1.5):
        """Assert that optimization provides minimum speedup"""
        actual_speedup = baseline_time / optimized_time
        self.assertGreaterEqual(
            actual_speedup, min_speedup,
            f"Speedup of {actual_speedup:.2f}x is less than required {min_speedup}x"
        )


def performance_test(max_time: float = None, min_ops_per_sec: float = None):
    """Decorator for performance tests"""
    def decorator(test_func: Callable):
        @wraps(test_func)
        def wrapper(self, *args, **kwargs):
            start_time = time.perf_counter()
            result = test_func(self, *args, **kwargs)
            elapsed = time.perf_counter() - start_time
            
            # Check performance constraints
            if max_time is not None:
                self.assertLessEqual(
                    elapsed, max_time,
                    f"Test exceeded time limit: {elapsed:.2f}s > {max_time}s"
                )
            
            if min_ops_per_sec is not None:
                ops_per_sec = 1.0 / elapsed
                self.assertGreaterEqual(
                    ops_per_sec, min_ops_per_sec,
                    f"Performance below threshold: {ops_per_sec:.2f} ops/s < {min_ops_per_sec} ops/s"
                )
            
            return result
        return wrapper
    return decorator


class LoadTester:
    """Load testing utilities"""
    
    def __init__(self, target_func: Callable):
        self.target_func = target_func
        self.results = []
    
    def run_load_test(self, duration_seconds: int, 
                     concurrent_users: int,
                     ramp_up_seconds: int = 0) -> Dict[str, Any]:
        """Run load test with specified parameters"""
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        # Results storage
        response_times = []
        errors = []
        
        def user_session():
            """Simulate a single user session"""
            while time.time() < end_time:
                try:
                    session_start = time.perf_counter()
                    self.target_func()
                    session_end = time.perf_counter()
                    
                    response_times.append(session_end - session_start)
                except Exception as e:
                    errors.append({
                        'time': time.time() - start_time,
                        'error': str(e)
                    })
        
        # Start user threads with ramp-up
        threads = []
        for i in range(concurrent_users):
            if ramp_up_seconds > 0:
                time.sleep(ramp_up_seconds / concurrent_users)
            
            thread = threading.Thread(target=user_session)
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Calculate results
        return {
            'total_requests': len(response_times),
            'total_errors': len(errors),
            'error_rate': len(errors) / (len(response_times) + len(errors)) if response_times else 0,
            'avg_response_time': statistics.mean(response_times) if response_times else 0,
            'min_response_time': min(response_times) if response_times else 0,
            'max_response_time': max(response_times) if response_times else 0,
            'requests_per_second': len(response_times) / duration_seconds,
            'concurrent_users': concurrent_users
        }