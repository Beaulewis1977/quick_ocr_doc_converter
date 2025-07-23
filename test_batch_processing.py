#!/usr/bin/env python3
"""
Batch Processing Test Suite
Tests batch processing capabilities and performance
"""

import os
import sys
import tempfile
import unittest
import subprocess
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestBatchProcessing(unittest.TestCase):
    """Test batch processing functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.temp_dir, "input")
        self.output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        self._create_test_files()
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_test_files(self):
        """Create test files for batch processing"""
        
        test_files = [
            ("document1.txt", "This is the first test document.\nIt has multiple lines.\nEnd of document 1."),
            ("document2.md", "# Document 2\n\nThis is a **markdown** document.\n\n- Item 1\n- Item 2"),
            ("document3.html", "<html><body><h1>Document 3</h1><p>HTML test content.</p></body></html>"),
            ("document4.txt", "Short document for testing batch processing."),
            ("document5.md", "# Another Test\n\nMore content for batch testing.\n\n> Quote block\n\nEnd."),
        ]
        
        for filename, content in test_files:
            file_path = os.path.join(self.input_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"Created {len(test_files)} test files for batch processing")
    
    def test_batch_processing_basic(self):
        """Test basic batch processing functionality"""
        
        # Get all input files
        input_files = list(Path(self.input_dir).glob("*.txt"))
        
        if not input_files:
            self.skipTest("No test files created")
        
        successful_conversions = 0
        
        # Process each file individually (simulating batch)
        for input_file in input_files:
            output_file = os.path.join(self.output_dir, f"batch_{input_file.stem}.txt")
            cmd = [sys.executable, "cli.py", str(input_file), "-o", output_file]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and os.path.exists(output_file):
                    successful_conversions += 1
                    print(f"  ✅ Converted: {input_file.name}")
                else:
                    print(f"  ❌ Failed: {input_file.name} - {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"  ⏰ Timeout: {input_file.name}")
            except Exception as e:
                print(f"  💥 Error: {input_file.name} - {e}")
        
        # At least half should succeed
        self.assertGreater(successful_conversions, len(input_files) // 2, 
                          f"Too few successful conversions: {successful_conversions}/{len(input_files)}")
        
        print(f"✅ Batch processing: {successful_conversions}/{len(input_files)} files processed successfully")
    
    def test_batch_processing_mixed_formats(self):
        """Test batch processing with mixed input formats"""
        
        # Get all input files (mixed formats)
        input_files = list(Path(self.input_dir).glob("*"))
        
        if not input_files:
            self.skipTest("No test files created")
        
        successful_conversions = 0
        format_results = {}
        
        # Process mixed format files
        for input_file in input_files:
            if input_file.is_file():
                output_file = os.path.join(self.output_dir, f"mixed_{input_file.stem}.txt")
                cmd = [sys.executable, "cli.py", str(input_file), "-o", output_file, "-f", "txt"]
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    
                    file_ext = input_file.suffix
                    if file_ext not in format_results:
                        format_results[file_ext] = {"success": 0, "total": 0}
                    
                    format_results[file_ext]["total"] += 1
                    
                    if result.returncode == 0 and os.path.exists(output_file):
                        successful_conversions += 1
                        format_results[file_ext]["success"] += 1
                        print(f"  ✅ Converted {file_ext}: {input_file.name}")
                    else:
                        print(f"  ❌ Failed {file_ext}: {input_file.name}")
                        
                except Exception as e:
                    format_results[input_file.suffix]["total"] += 1
                    print(f"  💥 Error {input_file.suffix}: {input_file.name} - {e}")
        
        # Print format-specific results
        print("\n📊 Format-specific results:")
        for ext, results in format_results.items():
            success_rate = (results["success"] / results["total"]) * 100 if results["total"] > 0 else 0
            print(f"  {ext}: {results['success']}/{results['total']} ({success_rate:.1f}%)")
        
        self.assertGreater(successful_conversions, 0, "No files were processed successfully")
        print(f"✅ Mixed format batch processing: {successful_conversions} files processed")
    
    def test_batch_processing_output_formats(self):
        """Test batch processing with different output formats"""
        
        input_file = os.path.join(self.input_dir, "document1.txt")
        if not os.path.exists(input_file):
            self.skipTest("Test input file not available")
        
        output_formats = ["txt", "html", "rtf"]
        successful_formats = 0
        
        for fmt in output_formats:
            output_file = os.path.join(self.output_dir, f"format_test.{fmt}")
            cmd = [sys.executable, "cli.py", input_file, "-o", output_file, "-f", fmt]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0 and os.path.exists(output_file):
                    successful_formats += 1
                    
                    # Check file has content
                    file_size = os.path.getsize(output_file)
                    print(f"  ✅ Format {fmt}: {file_size} bytes")
                else:
                    print(f"  ❌ Format {fmt} failed: {result.stderr}")
                    
            except Exception as e:
                print(f"  💥 Format {fmt} error: {e}")
        
        self.assertGreater(successful_formats, 0, "No output formats worked")
        print(f"✅ Output format testing: {successful_formats}/{len(output_formats)} formats succeeded")
    
    def test_batch_processing_performance(self):
        """Test batch processing performance and timing"""
        
        # Create additional test files for performance testing
        perf_dir = os.path.join(self.temp_dir, "performance")
        os.makedirs(perf_dir, exist_ok=True)
        
        # Create files of different sizes
        file_sizes = [100, 500, 1000, 2000]  # Number of words
        created_files = []
        
        for i, size in enumerate(file_sizes):
            filename = os.path.join(perf_dir, f"perf_test_{i}.txt")
            content = " ".join([f"word{j}" for j in range(size)])
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            created_files.append(filename)
        
        # Time the batch processing
        start_time = time.time()
        successful_conversions = 0
        processing_times = []
        
        for input_file in created_files:
            file_start = time.time()
            output_file = os.path.join(self.output_dir, f"perf_{os.path.basename(input_file)}")
            cmd = [sys.executable, "cli.py", input_file, "-o", output_file]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                file_end = time.time()
                processing_time = file_end - file_start
                processing_times.append(processing_time)
                
                if result.returncode == 0:
                    successful_conversions += 1
                    print(f"  ✅ Processed {os.path.basename(input_file)} in {processing_time:.2f}s")
                else:
                    print(f"  ❌ Failed {os.path.basename(input_file)}")
                    
            except Exception as e:
                print(f"  💥 Error processing {os.path.basename(input_file)}: {e}")
        
        total_time = time.time() - start_time
        
        # Performance metrics
        if processing_times:
            avg_time = sum(processing_times) / len(processing_times)
            max_time = max(processing_times)
            min_time = min(processing_times)
            
            print(f"\n📊 Performance Metrics:")
            print(f"  Total time: {total_time:.2f}s")
            print(f"  Average per file: {avg_time:.2f}s")
            print(f"  Fastest file: {min_time:.2f}s")
            print(f"  Slowest file: {max_time:.2f}s")
            print(f"  Files per second: {successful_conversions / total_time:.2f}")
            
            # Performance assertions
            self.assertLess(avg_time, 10.0, "Average processing time too slow")
            self.assertGreater(successful_conversions / total_time, 0.1, "Processing rate too slow")
        
        self.assertGreater(successful_conversions, 0, "No files processed successfully")
        print(f"✅ Performance test: {successful_conversions} files processed")
    
    def test_concurrent_batch_processing(self):
        """Test concurrent processing simulation"""
        
        input_files = list(Path(self.input_dir).glob("*.txt"))
        if len(input_files) < 2:
            self.skipTest("Need at least 2 test files for concurrent testing")
        
        def process_file(input_file):
            """Process a single file"""
            output_file = os.path.join(self.output_dir, f"concurrent_{input_file.stem}.txt")
            cmd = [sys.executable, "cli.py", str(input_file), "-o", output_file]
            
            try:
                start_time = time.time()
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                end_time = time.time()
                
                return {
                    "file": input_file.name,
                    "success": result.returncode == 0 and os.path.exists(output_file),
                    "time": end_time - start_time,
                    "error": result.stderr if result.returncode != 0 else None
                }
            except Exception as e:
                return {
                    "file": input_file.name,
                    "success": False,
                    "time": 0,
                    "error": str(e)
                }
        
        # Test concurrent processing
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(process_file, input_files[:2]))
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_results = [r for r in results if r["success"]]
        
        print(f"\n📊 Concurrent Processing Results:")
        for result in results:
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {result['file']}: {result['time']:.2f}s")
            if result["error"]:
                print(f"    Error: {result['error']}")
        
        print(f"  Total concurrent time: {total_time:.2f}s")
        print(f"  Successful files: {len(successful_results)}/{len(results)}")
        
        # Should complete faster than sequential processing
        sequential_time_estimate = sum(r["time"] for r in successful_results)
        if len(successful_results) > 1:
            efficiency = (sequential_time_estimate / total_time) * 100
            print(f"  Efficiency: {efficiency:.1f}%")
        
        self.assertGreater(len(successful_results), 0, "No concurrent processing succeeded")
        print("✅ Concurrent processing test completed")
    
    def test_error_handling_in_batch(self):
        """Test error handling during batch processing"""
        
        # Create a mix of valid and invalid files
        error_test_dir = os.path.join(self.temp_dir, "error_test")
        os.makedirs(error_test_dir, exist_ok=True)
        
        # Valid file
        valid_file = os.path.join(error_test_dir, "valid.txt")
        with open(valid_file, 'w', encoding='utf-8') as f:
            f.write("Valid test content")
        
        # Invalid/corrupted file
        invalid_file = os.path.join(error_test_dir, "invalid.txt")
        with open(invalid_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04\x05')  # Binary data
        
        # Non-existent file
        non_existent_file = os.path.join(error_test_dir, "non_existent.txt")
        
        test_files = [valid_file, invalid_file, non_existent_file]
        results = {"success": 0, "errors": 0, "total": len(test_files)}
        
        for input_file in test_files:
            output_file = os.path.join(self.output_dir, f"error_test_{os.path.basename(input_file)}")
            cmd = [sys.executable, "cli.py", input_file, "-o", output_file]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and os.path.exists(output_file):
                    results["success"] += 1
                    print(f"  ✅ Processed: {os.path.basename(input_file)}")
                else:
                    results["errors"] += 1
                    print(f"  ❌ Error (expected): {os.path.basename(input_file)}")
                    
            except Exception as e:
                results["errors"] += 1
                print(f"  💥 Exception (expected): {os.path.basename(input_file)} - {e}")
        
        print(f"\n📊 Error Handling Results:")
        print(f"  Successful: {results['success']}")
        print(f"  Errors: {results['errors']}")
        print(f"  Total: {results['total']}")
        
        # Should handle errors gracefully (at least valid file should work)
        self.assertGreater(results["success"], 0, "No files processed successfully")
        self.assertGreater(results["errors"], 0, "No errors detected (test may be invalid)")
        
        print("✅ Error handling in batch processing validated")

def run_batch_processing_tests():
    """Run batch processing tests"""
    print("🧪 Running Batch Processing Tests")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestBatchProcessing))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed!'}")
    
    return success

if __name__ == "__main__":
    success = run_batch_processing_tests()
    sys.exit(0 if success else 1)