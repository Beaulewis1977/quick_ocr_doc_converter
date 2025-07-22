"""
OCR Integration Module - Integrates OCR functionality with the main application
"""

import threading
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .ocr_engine import OCREngine
from .format_detector import OCRFormatDetector

class OCRIntegration:
    """Integrates OCR functionality with the document converter"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.ocr_engine = OCREngine(logger)
        self.is_available = len(self.ocr_engine.get_available_backends()) > 0
        
    def check_availability(self) -> Dict[str, Any]:
        """Check if OCR functionality is available"""
        backends = self.ocr_engine.get_available_backends()
        tesseract_available = self.ocr_engine.is_tesseract_available()
        easyocr_available = self.ocr_engine.is_easyocr_available()
        
        if self.is_available:
            message = f"OCR functionality is ready. Available backends: {', '.join(backends)}"
        else:
            message = "No OCR backends available. Please install Tesseract OCR or EasyOCR dependencies."
        
        return {
            'available': self.is_available,
            'tesseract_available': tesseract_available,
            'easyocr_available': easyocr_available,
            'backends': backends,
            'message': message,
            'supported_formats': list(OCRFormatDetector.get_supported_extensions())
        }
    
    def process_files(self, file_paths: List[str], output_dir: str, 
                     output_format: str = 'txt', max_workers: int = 2,
                     progress_callback=None) -> Dict[str, Any]:
        """
        Process multiple image files with OCR
        
        Args:
            file_paths: List of image file paths
            output_dir: Output directory for results
            output_format: Output format (txt, json, markdown)
            max_workers: Maximum number of concurrent workers
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with processing results
        """
        if not self.is_available:
            raise RuntimeError("OCR functionality is not available")
        
        # Filter supported files
        supported_files = OCRFormatDetector.filter_supported_files(file_paths)
        unsupported_count = len(file_paths) - len(supported_files)
        
        if not supported_files:
            return {
                'successful': 0,
                'failed': len(file_paths),
                'skipped': 0,
                'results': [],
                'duration': 0,
                'message': "No supported image files found"
            }
        
        start_time = time.time()
        results = []
        successful = 0
        failed = 0
        
        # Process files with threading
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(self._process_single_file, file_path, output_dir, output_format): file_path
                for file_path in supported_files
            }
            
            # Process completed tasks
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result.get('success', False):
                        successful += 1
                    else:
                        failed += 1
                        
                    # Update progress
                    if progress_callback:
                        progress_callback(len(results), len(supported_files))
                        
                except Exception as e:
                    self.logger.error(f"Failed to process {file_path}: {str(e)}")
                    results.append({
                        'file': str(file_path),
                        'success': False,
                        'error': str(e)
                    })
                    failed += 1
        
        duration = time.time() - start_time
        
        return {
            'successful': successful,
            'failed': failed + unsupported_count,
            'skipped': 0,
            'results': results,
            'duration': duration,
            'message': f"Processed {successful} files successfully"
        }
    
    def _process_single_file(self, file_path: str, output_dir: str, output_format: str) -> Dict[str, Any]:
        """Process a single image file with OCR"""
        try:
            file_path = Path(file_path)
            output_dir = Path(output_dir)
            
            # Extract text
            result = self.ocr_engine.extract_text(str(file_path))
            
            # Generate output filename
            output_filename = file_path.stem + self._get_extension(output_format)
            output_path = output_dir / output_filename
            
            # Save result
            success = self.ocr_engine.save_result(result, str(output_path), output_format)
            
            return {
                'file': str(file_path),
                'output_file': str(output_path),
                'success': success,
                'word_count': result.get('word_count', 0),
                'character_count': result.get('character_count', 0)
            }
            
        except Exception as e:
            return {
                'file': str(file_path),
                'success': False,
                'error': str(e)
            }
    
    def _get_extension(self, format_type: str) -> str:
        """Get file extension for output format"""
        extensions = {
            'txt': '.txt',
            'json': '.json',
            'markdown': '.md'
        }
        return extensions.get(format_type, '.txt')
    
    def get_supported_formats_info(self) -> List[Dict[str, str]]:
        """Get information about supported formats"""
        return OCRFormatDetector.get_supported_formats()
