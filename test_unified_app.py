#!/usr/bin/env python3
"""
Test script for the unified application components
Tests the core functionality without GUI dependencies
"""

import sys
import os
from pathlib import Path
import json
import logging
from typing import Optional, List, Dict, Any, Union
import time
import threading
import queue

# Import our core modules
try:
    from ocr_engine import OCREngine
    print("✅ OCR Engine imported successfully")
except ImportError as e:
    print(f"❌ OCR Engine import failed: {e}")
    OCREngine = None

try:
    from universal_document_converter import UniversalDocumentConverter
    print("✅ Universal Document Converter imported successfully")
except ImportError as e:
    print(f"❌ Universal Document Converter import failed: {e}")
    UniversalDocumentConverter = None

class ThreadSafeManager:
    """Thread-safe update manager for testing"""
    
    def __init__(self):
        self.update_queue = queue.Queue()
        self.running = True
        self.process_thread = threading.Thread(target=self.process_updates, daemon=True)
        self.process_thread.start()
    
    def process_updates(self):
        """Process queued updates"""
        while self.running:
            try:
                func, args, kwargs = self.update_queue.get(timeout=0.1)
                func(*args, **kwargs)
                self.update_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing update: {e}")
    
    def schedule_update(self, func, *args, **kwargs):
        """Schedule an update from any thread"""
        self.update_queue.put((func, args, kwargs))
    
    def stop(self):
        """Stop the update processor"""
        self.running = False
        if self.process_thread.is_alive():
            self.process_thread.join(timeout=1)

class TestUnifiedApp:
    """Test version of the unified application without GUI dependencies"""
    
    def __init__(self):
        # Initialize thread-safe manager
        self.manager = ThreadSafeManager()
        
        # Initialize core components
        self.ocr_engine = OCREngine() if OCREngine else None
        self.document_converter = UniversalDocumentConverter() if UniversalDocumentConverter else None
        
        # Configuration
        self.config = self.load_config()
        self.setup_logging()
        
        # State variables
        self.current_files = []
        self.processing_thread = None
        self.is_processing = False
        self.cancel_requested = False
        self.processed_count = 0
        self.total_files = 0
        
        # Log successful initialization
        self.logger.info("Test application initialized successfully")
    
    def load_config(self) -> Dict[str, Any]:
        """Load application configuration"""
        config_path = Path("config.json")
        default_config = {
            "output_format": "txt",
            "ocr_enabled": True,
            "ocr_language": "eng",
            "batch_size": 5,
            "max_workers": 4,
            "output_directory": str(Path.home() / "Documents" / "OCR_Converted"),
            "theme": "default",
            "window_size": "1200x800",
            "auto_detect_format": True,
            "preserve_structure": True,
            "enable_cloud_ocr": False
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")
                
        return default_config
    
    def setup_logging(self):
        """Setup logging system"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"test_app_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Test application logging initialized")
    
    def test_threading(self):
        """Test the threading functionality"""
        print("Testing threading functionality...")
        
        def test_function(message):
            print(f"Thread-safe update: {message}")
        
        # Schedule updates from different threads
        def worker(worker_id):
            for i in range(3):
                self.manager.schedule_update(test_function, f"Worker {worker_id} - Message {i}")
                time.sleep(0.1)
        
        # Start multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Give time for all updates to process
        time.sleep(1)
        print("✅ Threading test completed")
    
    def test_ocr_engine(self):
        """Test OCR engine functionality"""
        print("Testing OCR engine...")
        
        if self.ocr_engine:
            print(f"OCR Engine available: {self.ocr_engine.is_available()}")
            if self.ocr_engine.is_available():
                print(f"Supported languages: {self.ocr_engine.get_supported_languages()}")
            print("✅ OCR engine test completed")
        else:
            print("❌ OCR engine not available")
    
    def test_file_processing(self):
        """Test file processing simulation"""
        print("Testing file processing simulation...")
        
        # Simulate file processing
        test_files = ["test1.txt", "test2.pdf", "test3.jpg"]
        
        def process_files_thread():
            """Simulate file processing in background thread"""
            try:
                for i, file_path in enumerate(test_files):
                    if self.cancel_requested:
                        break
                    
                    # Simulate processing
                    self.manager.schedule_update(self.update_status, f"Processing {file_path}...")
                    progress = (i / len(test_files)) * 100
                    self.manager.schedule_update(self.update_progress, progress)
                    
                    # Simulate work
                    time.sleep(0.5)
                    
                    self.processed_count += 1
                    self.logger.info(f"Processed: {file_path}")
                
                self.manager.schedule_update(self.processing_complete)
                
            except Exception as e:
                self.logger.error(f"Processing error: {e}")
                self.manager.schedule_update(self.processing_complete)
        
        # Start processing
        self.is_processing = True
        self.processed_count = 0
        self.total_files = len(test_files)
        self.cancel_requested = False
        
        self.processing_thread = threading.Thread(target=process_files_thread, daemon=True)
        self.processing_thread.start()
        
        # Wait for processing to complete
        self.processing_thread.join()
        
        print("✅ File processing test completed")
    
    def update_status(self, message: str):
        """Update status (thread-safe)"""
        print(f"Status: {message}")
    
    def update_progress(self, value: float):
        """Update progress (thread-safe)"""
        print(f"Progress: {value:.1f}%")
    
    def processing_complete(self):
        """Handle processing completion (called from main thread)"""
        self.is_processing = False
        
        if self.cancel_requested:
            status_msg = f"Cancelled: {self.processed_count}/{self.total_files} files processed"
        else:
            status_msg = f"Completed: {self.processed_count}/{self.total_files} files processed"
        
        print(f"Final status: {status_msg}")
    
    def cleanup(self):
        """Cleanup resources"""
        self.manager.stop()
        print("✅ Cleanup completed")

def main():
    """Main test function"""
    print("OCR Document Converter - Unified Application Test")
    print("=" * 60)
    
    # Initialize test application
    app = TestUnifiedApp()
    
    try:
        # Run tests
        app.test_threading()
        print()
        
        app.test_ocr_engine()
        print()
        
        app.test_file_processing()
        print()
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        app.cleanup()

if __name__ == "__main__":
    main()