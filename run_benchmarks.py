#!/usr/bin/env python3
"""
Performance benchmark runner for Universal Document Converter
Run various performance tests and generate reports
"""

import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add tests directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tests.test_performance import (
    PerformanceBenchmark, 
    ConversionBenchmarks,
    LoadTester
)
from tests.test_base import TestFileFactory
from tests.test_fixtures import PerformanceData, DOCUMENT_TEMPLATES


class BenchmarkRunner:
    """Run and coordinate performance benchmarks"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("benchmark_results")
        self.output_dir.mkdir(exist_ok=True)
        self.results = {}
        
    def setup_test_environment(self):
        """Set up test files and environment"""
        self.test_dir = Path("benchmark_temp")
        self.test_dir.mkdir(exist_ok=True)
        
        print("Setting up test environment...")
        
        # Create various test files
        self.test_files = {
            'small_text': TestFileFactory.create_text_file(
                self.test_dir / "small.txt",
                "Small test file content"
            ),
            'medium_text': TestFileFactory.create_text_file(
                self.test_dir / "medium.txt",
                DOCUMENT_TEMPLATES['technical']['content']
            ),
            'large_text': TestFileFactory.create_text_file(
                self.test_dir / "large.txt",
                "x" * (1024 * 1024)  # 1MB
            ),
            'html': TestFileFactory.create_html_file(
                self.test_dir / "test.html"
            ),
            'markdown': TestFileFactory.create_markdown_file(
                self.test_dir / "test.md"
            )
        }
        
        # Create batch test files
        self.batch_files = PerformanceData.generate_test_files(
            50, self.test_dir / "batch"
        )
        
    def cleanup(self):
        """Clean up test environment"""
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def run_file_size_benchmarks(self):
        """Benchmark conversion performance for different file sizes"""
        print("\n=== File Size Benchmarks ===")
        
        # Import converter
        try:
            from universal_document_converter import DocumentConverter
            converter = DocumentConverter()
        except ImportError:
            print("Error: Could not import DocumentConverter")
            return
        
        sizes_kb = [1, 10, 100, 1000, 5000]
        results = []
        
        for size_kb in sizes_kb:
            print(f"Testing {size_kb}KB file...")
            
            # Create test file
            content = "x" * (size_kb * 1024)
            input_file = self.test_dir / f"size_test_{size_kb}kb.txt"
            input_file.write_text(content)
            output_file = self.test_dir / f"size_output_{size_kb}kb.txt"
            
            # Benchmark conversion
            benchmark = PerformanceBenchmark(f"file_size_{size_kb}kb")
            
            def convert():
                converter.convert_file(str(input_file), str(output_file))
            
            stats = benchmark.run_benchmark(convert, iterations=5)
            
            results.append({
                'size_kb': size_kb,
                'mean_time': stats['mean'],
                'min_time': stats['min'],
                'max_time': stats['max'],
                'throughput_mb_per_sec': (size_kb / 1024) / stats['mean']
            })
            
            print(f"  Mean time: {stats['mean']:.3f}s")
            print(f"  Throughput: {results[-1]['throughput_mb_per_sec']:.2f} MB/s")
        
        self.results['file_size_benchmarks'] = results
    
    def run_format_benchmarks(self):
        """Benchmark conversion performance for different formats"""
        print("\n=== Format Conversion Benchmarks ===")
        
        try:
            from universal_document_converter import DocumentConverter
            converter = DocumentConverter()
        except ImportError:
            print("Error: Could not import DocumentConverter")
            return
        
        format_tests = [
            ('txt', 'txt', self.test_files['medium_text']),
            ('txt', 'md', self.test_files['medium_text']),
            ('txt', 'html', self.test_files['medium_text']),
            ('html', 'txt', self.test_files['html']),
            ('html', 'md', self.test_files['html']),
            ('md', 'html', self.test_files['markdown']),
            ('md', 'txt', self.test_files['markdown'])
        ]
        
        results = []
        
        for in_fmt, out_fmt, test_file in format_tests:
            print(f"Testing {in_fmt} -> {out_fmt}...")
            
            output_file = self.test_dir / f"format_test.{out_fmt}"
            
            benchmark = PerformanceBenchmark(f"format_{in_fmt}_to_{out_fmt}")
            
            def convert():
                converter.convert_file(
                    str(test_file), 
                    str(output_file),
                    output_format=out_fmt
                )
            
            stats = benchmark.run_benchmark(convert, iterations=10)
            
            results.append({
                'input_format': in_fmt,
                'output_format': out_fmt,
                'mean_time': stats['mean'],
                'min_time': stats['min'],
                'max_time': stats['max']
            })
            
            print(f"  Mean time: {stats['mean']:.3f}s")
        
        self.results['format_benchmarks'] = results
    
    def run_batch_processing_benchmarks(self):
        """Benchmark batch processing performance"""
        print("\n=== Batch Processing Benchmarks ===")
        
        try:
            from universal_document_converter import DocumentConverter
            converter = DocumentConverter()
        except ImportError:
            print("Error: Could not import DocumentConverter")
            return
        
        # Test different batch sizes
        batch_sizes = [1, 5, 10, 25, 50]
        results = []
        
        for batch_size in batch_sizes:
            print(f"Testing batch size {batch_size}...")
            
            files = self.batch_files[:batch_size]
            
            # Sequential processing
            seq_benchmark = PerformanceBenchmark(f"batch_seq_{batch_size}")
            
            def process_sequential():
                for file in files:
                    output = file.with_suffix('.out.txt')
                    converter.convert_file(str(file), str(output))
            
            seq_stats = seq_benchmark.run_benchmark(
                process_sequential, 
                iterations=3
            )
            
            # Parallel processing (if supported)
            par_benchmark = PerformanceBenchmark(f"batch_par_{batch_size}")
            
            def process_parallel():
                # Simulate parallel processing
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=4) as executor:
                    futures = []
                    for file in files:
                        output = file.with_suffix('.out2.txt')
                        future = executor.submit(
                            converter.convert_file, 
                            str(file), 
                            str(output)
                        )
                        futures.append(future)
                    
                    for future in futures:
                        future.result()
            
            par_stats = par_benchmark.run_benchmark(
                process_parallel,
                iterations=3
            )
            
            results.append({
                'batch_size': batch_size,
                'sequential_time': seq_stats['mean'],
                'parallel_time': par_stats['mean'],
                'speedup': seq_stats['mean'] / par_stats['mean'],
                'files_per_sec_seq': batch_size / seq_stats['mean'],
                'files_per_sec_par': batch_size / par_stats['mean']
            })
            
            print(f"  Sequential: {seq_stats['mean']:.3f}s "
                  f"({results[-1]['files_per_sec_seq']:.1f} files/s)")
            print(f"  Parallel: {par_stats['mean']:.3f}s "
                  f"({results[-1]['files_per_sec_par']:.1f} files/s)")
            print(f"  Speedup: {results[-1]['speedup']:.2f}x")
        
        self.results['batch_benchmarks'] = results
    
    def run_memory_benchmarks(self):
        """Benchmark memory usage"""
        print("\n=== Memory Usage Benchmarks ===")
        
        try:
            import psutil
            from universal_document_converter import DocumentConverter
            converter = DocumentConverter()
        except ImportError as e:
            print(f"Error: Could not import required modules: {e}")
            return
        
        file_sizes_mb = [1, 5, 10, 25]
        results = []
        
        for size_mb in file_sizes_mb:
            print(f"Testing {size_mb}MB file...")
            
            # Create large file
            content = "x" * (size_mb * 1024 * 1024)
            input_file = self.test_dir / f"memory_test_{size_mb}mb.txt"
            input_file.write_text(content)
            output_file = self.test_dir / f"memory_output_{size_mb}mb.txt"
            
            # Measure memory before
            import gc
            gc.collect()
            process = psutil.Process()
            mem_before = process.memory_info().rss / (1024 * 1024)
            
            # Perform conversion
            start_time = time.time()
            converter.convert_file(str(input_file), str(output_file))
            end_time = time.time()
            
            # Measure memory after
            mem_after = process.memory_info().rss / (1024 * 1024)
            
            results.append({
                'file_size_mb': size_mb,
                'memory_before_mb': mem_before,
                'memory_after_mb': mem_after,
                'memory_increase_mb': mem_after - mem_before,
                'time_seconds': end_time - start_time,
                'mb_per_second': size_mb / (end_time - start_time)
            })
            
            print(f"  Memory increase: {results[-1]['memory_increase_mb']:.1f}MB")
            print(f"  Processing speed: {results[-1]['mb_per_second']:.1f}MB/s")
            
            # Clean up large file
            input_file.unlink()
            output_file.unlink(missing_ok=True)
        
        self.results['memory_benchmarks'] = results
    
    def generate_report(self):
        """Generate benchmark report"""
        print("\n=== Generating Report ===")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = self.output_dir / timestamp
        report_dir.mkdir(exist_ok=True)
        
        # Save raw results
        results_file = report_dir / "benchmark_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Generate summary report
        summary_file = report_dir / "benchmark_summary.txt"
        with open(summary_file, 'w') as f:
            f.write("Universal Document Converter - Performance Benchmark Report\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("=" * 60 + "\n\n")
            
            # File size summary
            if 'file_size_benchmarks' in self.results:
                f.write("File Size Performance:\n")
                for result in self.results['file_size_benchmarks']:
                    f.write(f"  {result['size_kb']}KB: "
                           f"{result['mean_time']:.3f}s "
                           f"({result['throughput_mb_per_sec']:.2f} MB/s)\n")
                f.write("\n")
            
            # Format conversion summary
            if 'format_benchmarks' in self.results:
                f.write("Format Conversion Performance:\n")
                for result in self.results['format_benchmarks']:
                    f.write(f"  {result['input_format']} -> "
                           f"{result['output_format']}: "
                           f"{result['mean_time']:.3f}s\n")
                f.write("\n")
            
            # Batch processing summary
            if 'batch_benchmarks' in self.results:
                f.write("Batch Processing Performance:\n")
                for result in self.results['batch_benchmarks']:
                    f.write(f"  {result['batch_size']} files: "
                           f"Sequential {result['sequential_time']:.3f}s, "
                           f"Parallel {result['parallel_time']:.3f}s "
                           f"(Speedup: {result['speedup']:.2f}x)\n")
                f.write("\n")
            
            # Memory usage summary
            if 'memory_benchmarks' in self.results:
                f.write("Memory Usage:\n")
                for result in self.results['memory_benchmarks']:
                    f.write(f"  {result['file_size_mb']}MB file: "
                           f"+{result['memory_increase_mb']:.1f}MB memory\n")
        
        print(f"Report saved to: {report_dir}")
        return report_dir


def main():
    """Main benchmark runner"""
    parser = argparse.ArgumentParser(
        description="Run performance benchmarks for Universal Document Converter"
    )
    parser.add_argument(
        '--output-dir', 
        type=str,
        help='Output directory for results'
    )
    parser.add_argument(
        '--benchmarks',
        nargs='+',
        choices=['file-size', 'format', 'batch', 'memory', 'all'],
        default=['all'],
        help='Which benchmarks to run'
    )
    
    args = parser.parse_args()
    
    # Create benchmark runner
    runner = BenchmarkRunner(
        Path(args.output_dir) if args.output_dir else None
    )
    
    try:
        # Set up test environment
        runner.setup_test_environment()
        
        # Run selected benchmarks
        benchmarks_to_run = set(args.benchmarks)
        
        if 'all' in benchmarks_to_run or 'file-size' in benchmarks_to_run:
            runner.run_file_size_benchmarks()
        
        if 'all' in benchmarks_to_run or 'format' in benchmarks_to_run:
            runner.run_format_benchmarks()
        
        if 'all' in benchmarks_to_run or 'batch' in benchmarks_to_run:
            runner.run_batch_processing_benchmarks()
        
        if 'all' in benchmarks_to_run or 'memory' in benchmarks_to_run:
            runner.run_memory_benchmarks()
        
        # Generate report
        report_dir = runner.generate_report()
        
        print("\nBenchmarks completed successfully!")
        
    finally:
        # Clean up
        runner.cleanup()


if __name__ == '__main__':
    main()