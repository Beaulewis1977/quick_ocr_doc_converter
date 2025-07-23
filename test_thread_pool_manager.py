#!/usr/bin/env python3
"""
Test script for Thread Pool Manager
Verifies resource validation and backpressure handling
"""

import time
import threading
from thread_pool_manager import thread_manager

def test_task(task_id, duration=0.1):
    """Simple test task"""
    print(f"Task {task_id} starting on thread {threading.current_thread().name}")
    time.sleep(duration)
    return f"Task {task_id} completed"

def test_resource_validation():
    """Test resource validation"""
    print("\n=== Testing Resource Validation ===")
    
    # Get system info
    stats = thread_manager.get_stats()
    print(f"System: {stats['system']['cpu_count']} CPUs, "
          f"{stats['system']['memory_gb']:.1f}GB RAM, "
          f"max {stats['system']['max_threads']} threads")
    
    # Test worker count validation
    requested = 100
    validated = thread_manager.validate_worker_count(requested, "test_pool")
    print(f"Requested {requested} workers, validated to {validated}")
    
    # Create pool with excessive workers
    pool = thread_manager.get_pool("test_high", max_workers=50)
    print(f"Created pool with {pool._max_workers} workers")

def test_backpressure():
    """Test backpressure handling"""
    print("\n=== Testing Backpressure ===")
    
    # Submit many tasks quickly
    futures = []
    for i in range(20):
        future = thread_manager.submit_with_backpressure(
            "test_backpressure",
            test_task,
            i,
            0.5  # Longer tasks to trigger backpressure
        )
        futures.append(future)
        print(f"Submitted task {i}")
    
    # Wait for completion
    for i, future in enumerate(futures):
        result = future.result()
        print(f"Got result: {result}")

def test_multiple_pools():
    """Test multiple concurrent pools"""
    print("\n=== Testing Multiple Pools ===")
    
    # Create multiple pools
    pools = {
        "ocr": thread_manager.get_pool("ocr", max_workers=4),
        "conversion": thread_manager.get_pool("conversion", max_workers=6),
        "batch": thread_manager.get_pool("batch", max_workers=2)
    }
    
    # Show pool stats
    stats = thread_manager.get_stats()
    print("Active pools:")
    for name, pool_stats in stats['pools'].items():
        print(f"  {name}: {pool_stats['workers']} workers")

def test_managed_pool():
    """Test managed pool context manager"""
    print("\n=== Testing Managed Pool ===")
    
    with thread_manager.managed_pool("test_managed", max_workers=3) as pool:
        futures = [pool.submit(test_task, i) for i in range(5)]
        results = [f.result() for f in futures]
        print(f"Results: {results}")
    
    print("Pool auto-cleaned after context exit")

def test_cleanup():
    """Test cleanup"""
    print("\n=== Testing Cleanup ===")
    
    # Get current stats
    stats = thread_manager.get_stats()
    print(f"Active pools before cleanup: {len(stats['pools'])}")
    
    # Shutdown all pools
    thread_manager.shutdown_all(wait=True, timeout=5)
    
    # Check after cleanup
    stats = thread_manager.get_stats()
    print(f"Active pools after cleanup: {len(stats['pools'])}")

if __name__ == "__main__":
    print("Thread Pool Manager Test Suite")
    print("=" * 50)
    
    try:
        test_resource_validation()
        test_multiple_pools()
        test_managed_pool()
        test_backpressure()
        test_cleanup()
        
        print("\n✓ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()