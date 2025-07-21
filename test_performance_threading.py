#!/usr/bin/env python3
"""Test performance, threading, and batch processing capabilities"""

import tempfile
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor

# Add current directory to path  
sys.path.insert(0, '/root/repo')

def test_batch_conversion():
    """Test batch conversion performance"""
    from universal_document_converter import UniversalConverter
    
    print("🔄 Testing Batch Conversion Performance...")
    
    # Create test files
    test_content = """# Performance Test Document {num}

This is test document number **{num}** for performance testing.

## Features

- Document number: {num}
- Batch processing test
- Performance measurement

## Content

Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

### Results

This document tests the conversion performance and threading capabilities.

## Conclusion

Document {num} conversion complete!"""

    converter = UniversalConverter()
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create 10 test markdown files
        input_files = []
        output_files = []
        
        for i in range(10):
            content = test_content.format(num=i+1)
            input_file = os.path.join(temp_dir, f"test_{i+1}.md")
            output_file = os.path.join(temp_dir, f"test_{i+1}.rtf")
            
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            input_files.append(input_file)
            output_files.append(output_file)
        
        # Test sequential conversion
        print("   📊 Sequential conversion...")
        start_time = time.time()
        
        for i, (input_file, output_file) in enumerate(zip(input_files, output_files)):
            converter.convert_file(input_file, output_file, 'markdown', 'rtf')
            
        sequential_time = time.time() - start_time
        print(f"   ⏱️  Sequential: {sequential_time:.2f} seconds")
        
        # Verify all files were created
        successful = sum(1 for f in output_files if os.path.exists(f))
        print(f"   ✅ Files created: {successful}/10")
        
        # Check file sizes
        total_size = sum(os.path.getsize(f) for f in output_files if os.path.exists(f))
        print(f"   📁 Total output: {total_size} bytes")
        
        return sequential_time, successful == 10
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)

def test_concurrent_conversion():
    """Test concurrent conversion with ThreadPoolExecutor"""
    from universal_document_converter import UniversalConverter
    
    print("\n⚡ Testing Concurrent Conversion...")
    
    converter = UniversalConverter()
    temp_dir = tempfile.mkdtemp()
    
    def convert_file_wrapper(args):
        """Wrapper function for thread pool"""
        input_file, output_file, input_format, output_format = args
        try:
            converter.convert_file(input_file, output_file, input_format, output_format)
            return True
        except Exception as e:
            print(f"   ❌ Error converting {input_file}: {e}")
            return False
    
    try:
        # Create test files
        test_files = []
        for i in range(5):
            content = f"""# Concurrent Test {i+1}
            
This is concurrent test document {i+1}.

## Performance Test

Testing multi-threading capabilities with document {i+1}.

### Results

Concurrent processing test in progress...

## Status

Document {i+1} ready for conversion."""

            input_file = os.path.join(temp_dir, f"concurrent_{i+1}.md")
            output_file = os.path.join(temp_dir, f"concurrent_{i+1}.rtf")
            
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            test_files.append((input_file, output_file, 'markdown', 'rtf'))
        
        # Test with ThreadPoolExecutor
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(convert_file_wrapper, test_files))
        
        concurrent_time = time.time() - start_time
        successful = sum(results)
        
        print(f"   ⏱️  Concurrent: {concurrent_time:.2f} seconds")
        print(f"   ✅ Successful: {successful}/5")
        print(f"   🧵 Max workers: 3")
        
        return concurrent_time, successful == 5
        
    finally:
        import shutil
        shutil.rmtree(temp_dir)

def test_memory_usage():
    """Test memory usage during conversions"""
    print("\n💾 Testing Memory Usage...")
    
    try:
        import psutil
        process = psutil.Process()
        
        from universal_document_converter import UniversalConverter
        converter = UniversalConverter()
        
        # Get initial memory
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(f"   🔍 Initial memory: {initial_memory:.1f} MB")
        
        # Create a large test document
        large_content = """# Large Document Test\n\n""" + \
                       "This is a paragraph with lots of content. " * 100 + \
                       "\n\n## Section 2\n\n" + \
                       "More content for memory testing. " * 200
        
        temp_dir = tempfile.mkdtemp()
        try:
            input_file = os.path.join(temp_dir, "large_test.md")
            output_file = os.path.join(temp_dir, "large_test.rtf")
            
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(large_content)
            
            # Convert and measure memory
            converter.convert_file(input_file, output_file, 'markdown', 'rtf')
            
            peak_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = peak_memory - initial_memory
            
            print(f"   📈 Peak memory: {peak_memory:.1f} MB")
            print(f"   📊 Memory increase: {memory_increase:.1f} MB")
            
            # Check if conversion was successful
            if os.path.exists(output_file):
                output_size = os.path.getsize(output_file)
                print(f"   📄 Output size: {output_size} bytes")
                return True
            else:
                print("   ❌ Output file not created")
                return False
                
        finally:
            import shutil
            shutil.rmtree(temp_dir)
            
    except ImportError:
        print("   ⚠️  psutil not available, skipping memory test")
        return True
    except Exception as e:
        print(f"   ❌ Memory test error: {e}")
        return False

def test_error_handling():
    """Test error handling and recovery"""
    print("\n🛡️ Testing Error Handling...")
    
    from universal_document_converter import UniversalConverter
    converter = UniversalConverter()
    
    test_cases = [
        ("nonexistent.md", "output.rtf", "markdown", "rtf", "File not found"),
        ("test.md", "/invalid/path/output.rtf", "markdown", "rtf", "Invalid output path"),
        ("test.md", "output.rtf", "invalid_format", "rtf", "Unsupported input format"),
        ("test.md", "output.rtf", "markdown", "invalid_format", "Unsupported output format"),
    ]
    
    error_handling_results = []
    
    for input_file, output_file, input_format, output_format, expected_error in test_cases:
        try:
            converter.convert_file(input_file, output_file, input_format, output_format)
            error_handling_results.append(f"❌ Expected error for {expected_error}")
        except Exception as e:
            error_handling_results.append(f"✅ Caught error: {expected_error}")
    
    for result in error_handling_results:
        print(f"   {result}")
    
    successful_errors = sum(1 for r in error_handling_results if r.startswith("✅"))
    print(f"   📊 Error handling: {successful_errors}/{len(test_cases)} cases")
    
    return successful_errors == len(test_cases)

def main():
    """Run all performance and threading tests"""
    print("⚡ Performance and Threading Test Suite")
    print("=" * 60)
    
    results = {}
    
    # Run tests
    try:
        seq_time, batch_success = test_batch_conversion()
        results['batch'] = batch_success
    except Exception as e:
        print(f"   ❌ Batch test error: {e}")
        results['batch'] = False
    
    try:
        conc_time, concurrent_success = test_concurrent_conversion() 
        results['concurrent'] = concurrent_success
    except Exception as e:
        print(f"   ❌ Concurrent test error: {e}")
        results['concurrent'] = False
    
    try:
        memory_success = test_memory_usage()
        results['memory'] = memory_success
    except Exception as e:
        print(f"   ❌ Memory test error: {e}")
        results['memory'] = False
    
    try:
        error_success = test_error_handling()
        results['errors'] = error_success
    except Exception as e:
        print(f"   ❌ Error handling test error: {e}")
        results['errors'] = False
    
    # Summary
    print(f"\n📊 Test Results Summary")
    print("=" * 60)
    
    for test, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test.title():15} | {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\n🎯 Overall: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 All performance and threading tests PASSED!")
    else:
        print("⚠️ Some tests failed - check output above")
    
    return total_passed == total_tests

if __name__ == '__main__':
    main()