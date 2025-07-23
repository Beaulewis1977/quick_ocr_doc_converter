#!/usr/bin/env python3
"""
Thread Pool Manager for Universal Document Converter (Simplified version without psutil)
Provides centralized thread pool management with resource validation and backpressure handling

Author: Beau Lewis (blewisxx@gmail.com)
"""

import os
import sys
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Optional, Dict, Any, Callable, List
from functools import wraps
import time
import queue
from contextlib import contextmanager

class ThreadPoolManager:
    """
    Centralized thread pool manager with resource validation
    """
    
    # Singleton instance
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'ThreadPoolManager':
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if hasattr(self, '_initialized'):
            return
            
        self._initialized = True
        self.logger = logging.getLogger("ThreadPoolManager")
        
        # System resource limits (simplified without psutil)
        self.cpu_count = os.cpu_count() or 2
        
        # Calculate safe thread limits based on system resources
        self.max_system_threads = self._calculate_max_threads()
        self.default_workers = min(4, self.max_system_threads // 2)
        
        # Thread pool tracking
        self._pools: Dict[str, ThreadPoolExecutor] = {}
        self._pool_stats: Dict[str, Dict[str, Any]] = {}
        self._pools_lock = threading.RLock()
        
        # Backpressure handling
        self._active_tasks = 0
        self._max_active_tasks = self.max_system_threads * 2
        self._task_queue = queue.Queue(maxsize=self._max_active_tasks)
        self._backpressure_event = threading.Event()
        self._backpressure_event.set()
        
        self.logger.info(f"ThreadPoolManager initialized: CPUs={self.cpu_count}, "
                        f"Max threads={self.max_system_threads}")
    
    def _calculate_max_threads(self) -> int:
        """Calculate maximum safe thread count based on system resources"""
        # Base calculation: 2 threads per CPU core
        cpu_based_limit = self.cpu_count * 2
        
        # System-specific adjustments
        if sys.platform == "win32":
            # Windows has lower thread limits
            system_limit = 64
        elif sys.platform == "darwin":
            # macOS has reasonable thread limits
            system_limit = 128
        else:
            # Linux typically handles more threads
            system_limit = 256
        
        # Take the minimum of all limits
        max_threads = min(cpu_based_limit, system_limit)
        
        # Ensure reasonable minimum
        return max(4, max_threads)
    
    def validate_worker_count(self, requested_workers: int, pool_name: str = "default") -> int:
        """
        Validate and adjust requested worker count based on system resources
        
        Args:
            requested_workers: Number of workers requested
            pool_name: Name of the thread pool
            
        Returns:
            Safe number of workers to use
        """
        with self._pools_lock:
            # Count existing threads across all pools
            existing_threads = sum(
                pool._max_workers for pool in self._pools.values()
                if pool and not pool._shutdown
            )
            
            # Calculate available thread budget
            available_threads = max(1, self.max_system_threads - existing_threads)
            
            # Limit to available threads
            safe_workers = min(requested_workers, available_threads)
            
            # Apply minimum for functionality
            safe_workers = max(1, safe_workers)
            
            if safe_workers < requested_workers:
                self.logger.warning(
                    f"Reducing worker count for '{pool_name}' from {requested_workers} to {safe_workers} "
                    f"(system limit: {self.max_system_threads}, existing: {existing_threads})"
                )
            
            return safe_workers
    
    def get_pool(self, pool_name: str = "default", max_workers: Optional[int] = None) -> ThreadPoolExecutor:
        """
        Get or create a named thread pool with resource validation
        
        Args:
            pool_name: Name of the thread pool
            max_workers: Maximum number of workers (will be validated)
            
        Returns:
            ThreadPoolExecutor instance
        """
        with self._pools_lock:
            # Check if pool exists and is healthy
            if pool_name in self._pools:
                pool = self._pools[pool_name]
                if pool and not pool._shutdown:
                    return pool
                else:
                    # Clean up dead pool
                    del self._pools[pool_name]
            
            # Validate worker count
            requested_workers = max_workers or self.default_workers
            safe_workers = self.validate_worker_count(requested_workers, pool_name)
            
            # Create new pool
            pool = ThreadPoolExecutor(
                max_workers=safe_workers,
                thread_name_prefix=f"TPM-{pool_name}"
            )
            
            self._pools[pool_name] = pool
            self._pool_stats[pool_name] = {
                'created': time.time(),
                'max_workers': safe_workers,
                'tasks_submitted': 0,
                'tasks_completed': 0
            }
            
            self.logger.info(f"Created thread pool '{pool_name}' with {safe_workers} workers")
            return pool
    
    @contextmanager
    def managed_pool(self, pool_name: str = "default", max_workers: Optional[int] = None) -> ThreadPoolExecutor:
        """
        Context manager for automatic pool cleanup
        
        Usage:
            with thread_manager.managed_pool("ocr", max_workers=4) as pool:
                futures = [pool.submit(task, arg) for arg in args]
        """
        pool = self.get_pool(pool_name, max_workers)
        try:
            yield pool
        finally:
            # Don't shutdown the pool here as it might be reused
            # Pools are cleaned up in shutdown_all()
            pass
    
    def submit_with_backpressure(self, pool_name: str, fn: Callable, *args, **kwargs) -> Future:
        """
        Submit task with backpressure handling
        
        Args:
            pool_name: Name of the thread pool
            fn: Function to execute
            args: Positional arguments for function
            kwargs: Keyword arguments for function
            
        Returns:
            Future object
        """
        # Wait if system is under pressure
        self._backpressure_event.wait()
        
        # Check task queue size
        if self._active_tasks >= self._max_active_tasks:
            self.logger.warning(f"Task queue full ({self._active_tasks} tasks), applying backpressure")
            # Wait for some tasks to complete
            time.sleep(0.1)
        
        pool = self.get_pool(pool_name)
        
        # Wrap function to track active tasks
        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            try:
                self._active_tasks += 1
                return fn(*args, **kwargs)
            finally:
                self._active_tasks -= 1
                if pool_name in self._pool_stats:
                    self._pool_stats[pool_name]['tasks_completed'] += 1
        
        # Submit task
        if pool_name in self._pool_stats:
            self._pool_stats[pool_name]['tasks_submitted'] += 1
        
        return pool.submit(wrapped_fn, *args, **kwargs)
    
    def shutdown_pool(self, pool_name: str, wait: bool = True, timeout: Optional[float] = None) -> None:
        """
        Shutdown a specific thread pool
        
        Args:
            pool_name: Name of the thread pool
            wait: Whether to wait for tasks to complete
            timeout: Maximum time to wait for shutdown
        """
        with self._pools_lock:
            if pool_name in self._pools:
                pool = self._pools[pool_name]
                if pool and not pool._shutdown:
                    self.logger.info(f"Shutting down thread pool '{pool_name}' (wait={wait})")
                    pool.shutdown(wait=wait)
                del self._pools[pool_name]
                
                if pool_name in self._pool_stats:
                    stats = self._pool_stats[pool_name]
                    self.logger.info(
                        f"Pool '{pool_name}' stats: "
                        f"submitted={stats['tasks_submitted']}, "
                        f"completed={stats['tasks_completed']}"
                    )
                    del self._pool_stats[pool_name]
    
    def shutdown_all(self, wait: bool = True, timeout: float = 30) -> None:
        """
        Shutdown all thread pools
        
        Args:
            wait: Whether to wait for tasks to complete
            timeout: Maximum time to wait for shutdown
        """
        self.logger.info("Shutting down all thread pools")
        
        # Shutdown all pools
        with self._pools_lock:
            pool_names = list(self._pools.keys())
            for pool_name in pool_names:
                self.shutdown_pool(pool_name, wait=wait)
        
        self.logger.info("All thread pools shut down")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current thread pool statistics"""
        with self._pools_lock:
            active_pools = {
                name: {
                    'active': not pool._shutdown,
                    'workers': pool._max_workers,
                    **self._pool_stats.get(name, {})
                }
                for name, pool in self._pools.items()
            }
            
            return {
                'system': {
                    'cpu_count': self.cpu_count,
                    'max_threads': self.max_system_threads
                },
                'pools': active_pools,
                'active_tasks': self._active_tasks,
                'backpressure': not self._backpressure_event.is_set()
            }

# Global instance
thread_manager = ThreadPoolManager()