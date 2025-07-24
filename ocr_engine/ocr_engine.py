"""
OCR Engine for Quick Document Convertor

Provides comprehensive OCR functionality with support for multiple backends,
image preprocessing, and batch processing capabilities.

Author: Beau Lewis (blewisxx@gmail.com)
"""

import os
import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Callable, Generator
import json
import hashlib
import tempfile
from concurrent.futures import as_completed
import threading
import numpy as np
import sys
import weakref
import atexit
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from thread_pool_manager import thread_manager

try:
    import pytesseract
    import cv2
    from PIL import Image, ImageEnhance, ImageFilter
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

# Handle both relative and absolute imports
try:
    from .image_processor import ImageProcessor
    from .format_detector import OCRFormatDetector
except ImportError:
    # If relative imports fail, try absolute imports
    try:
        from image_processor import ImageProcessor
        from format_detector import OCRFormatDetector
    except ImportError:
        # If both fail, create simple fallback classes
        class ImageProcessor:
            def __init__(self, logger=None):
                self.logger = logger or logging.getLogger("ImageProcessor")
            def process_image(self, image_path, config=None):
                return image_path
        
        class OCRFormatDetector:
            def detect_format(self, file_path):
                return "image"

import tesseract_config  # Auto-configure Tesseract
class OCREngineError(Exception):
    """Base exception for OCR engine errors"""
    pass

class OCRBackendError(OCREngineError):
    """Raised when OCR backend is not available"""
    pass

class ImageProcessingError(OCREngineError):
    """Raised when image processing fails"""
    pass

class OCREngine:
    """
    Main OCR engine for image-to-text conversion
    
    Features:
    - Multiple OCR backend support (Tesseract, EasyOCR)
    - Image preprocessing and enhancement
    - Batch processing with progress tracking
    - Caching for improved performance
    - Configurable quality settings
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, logger: Optional[logging.Logger] = None):
        """
        Initialize OCR engine
        
        Args:
            config: Configuration dictionary for OCR settings
            logger: Optional logger instance
        """
        self.config = config or {}
        self.logger = logger or logging.getLogger("OCREngine")
        
        # Initialize thread safety locks FIRST
        self._active_readers = weakref.WeakValueDictionary()  # thread_id -> reader mapping with weak refs
        self._readers_lock = threading.Lock()  # Lock for reader tracking
        self._cache_lock = threading.RLock()  # Reentrant lock for cache operations
        self._config_lock = threading.RLock()  # Lock for configuration changes
        self._backend_lock = threading.Lock()  # Lock for backend initialization
        
        # Thread-local storage for OCR readers
        self._thread_local = threading.local()
        
        # Register cleanup on exit
        atexit.register(self._cleanup_all_readers)
        
        # Cache directory for OCR results
        self.cache_dir = Path.home() / ".quick_document_convertor" / "ocr_cache"
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            self.logger.warning(f"Failed to create OCR cache directory {self.cache_dir}: {e}")
            # Fallback to temporary directory
            import tempfile
            self.cache_dir = Path(tempfile.gettempdir()) / "ocr_cache"
            try:
                self.cache_dir.mkdir(parents=True, exist_ok=True)
            except (OSError, PermissionError):
                self.logger.error("Failed to create fallback cache directory, disabling cache")
                self.cache_dir = None
        
        # Configuration defaults
        self.default_config = {
            'backend': 'auto',
            'languages': ['en'],
            'use_cache': True,
            'cache_ttl': 86400,  # 24 hours
            'max_file_size': 50 * 1024 * 1024,  # 50MB
            'max_workers': 2,  # Default thread pool size
            'batch_size': 10,  # Default batch processing size
            'preprocessing': {
                'enhance_contrast': True,
                'denoise': True,
                'resize_max': 2048,
                'threshold_method': 'adaptive'
            },
            'tesseract_config': '--oem 3 --psm 6',
            'confidence_threshold': 30
        }
        
        # Merge user config with defaults
        self.config = {**self.default_config, **self.config}
        
        # Initialize image processor and format detector (after locks are ready)
        self.image_processor = ImageProcessor(self.logger)
        self.format_detector = OCRFormatDetector()
        
        # Initialize OCR backends (after everything else is set up)
        self._initialize_backends()

    def _initialize_backends(self):
        """Initialize available OCR backends"""
        with self._backend_lock:
            self.backends = {}
        
        # Tesseract OCR
        if TESSERACT_AVAILABLE:
            try:
                # Test if tesseract is available
                pytesseract.get_tesseract_version()
                self.backends['tesseract'] = {
                    'name': 'Tesseract OCR',
                    'priority': 1,
                    'available': True
                }
                self.logger.info("Tesseract OCR backend initialized")
            except Exception as e:
                self.logger.warning(f"Tesseract not available: {e}")
                self.backends['tesseract'] = {
                    'name': 'Tesseract OCR',
                    'priority': 1,
                    'available': False
                }
        
        # EasyOCR
        if EASYOCR_AVAILABLE:
            try:
                self.backends['easyocr'] = {
                    'name': 'EasyOCR',
                    'priority': 2,
                    'available': True,
                    'reader': None  # Lazy initialization
                }
                self.logger.info("EasyOCR backend available")
            except Exception as e:
                self.logger.warning(f"EasyOCR initialization failed: {e}")
                self.backends['easyocr'] = {
                    'name': 'EasyOCR',
                    'priority': 2,
                    'available': False
                }

    def is_tesseract_available(self) -> bool:
        """Check if Tesseract OCR is available"""
        return 'tesseract' in self.backends and self.backends['tesseract']['available']

    def is_easyocr_available(self) -> bool:
        """Check if EasyOCR is available"""
        return 'easyocr' in self.backends and self.backends['easyocr']['available']

    def is_available(self) -> bool:
        """Check if any OCR backend is available"""
        return len(self.get_available_backends()) > 0

    def get_available_backends(self) -> List[str]:
        """Get list of available OCR backends"""
        return [name for name, info in self.backends.items() if info['available']]

    def get_preferred_backend(self) -> str:
        """Get the preferred OCR backend based on availability and priority"""
        available = [(name, info['priority']) for name, info in self.backends.items() 
                    if info['available']]
        if not available:
            raise OCRBackendError("No OCR backends available")
        
        # Sort by priority (lower is better)
        available.sort(key=lambda x: x[1])
        return available[0][0]

    def _get_easyocr_reader(self, languages: List[str] = None):
        """Get thread-local EasyOCR reader with global tracking"""
        # Clean up dead threads periodically
        self._cleanup_dead_thread_readers()
        
        if not hasattr(self._thread_local, 'easyocr_reader'):
            if languages is None:
                languages = self.config['languages']
            reader = easyocr.Reader(
                languages, 
                gpu=False,  # Disable GPU for compatibility
                verbose=False
            )
            self._thread_local.easyocr_reader = reader
            
            # Track reader globally for cleanup with weak reference
            thread_id = threading.get_ident()
            with self._readers_lock:
                self._active_readers[thread_id] = reader
                
        return self._thread_local.easyocr_reader
    
    def _cleanup_dead_thread_readers(self):
        """Clean up readers from threads that no longer exist"""
        import threading
        active_threads = {t.ident for t in threading.enumerate() if t.ident}
        
        with self._readers_lock:
            dead_threads = [tid for tid in self._active_readers.keys() if tid not in active_threads]
            for tid in dead_threads:
                try:
                    # WeakValueDictionary will automatically remove dead references
                    if tid in self._active_readers:
                        del self._active_readers[tid]
                        self.logger.debug(f"Cleaned up reader for dead thread {tid}")
                except Exception as e:
                    self.logger.warning(f"Error cleaning up reader for thread {tid}: {e}")

    def _get_cache_key(self, image_path: Path, options: Dict[str, Any]) -> str:
        """Generate cache key for OCR result"""
        # Create hash from file content and options
        hasher = hashlib.md5()
        
        # Add file content hash
        if image_path.exists():
            with open(image_path, 'rb') as f:
                hasher.update(f.read(1024))  # First 1KB for speed
        
        # Add options hash
        options_str = json.dumps(options, sort_keys=True)
        hasher.update(options_str.encode())
        
        return hasher.hexdigest()

    def _is_cache_valid(self, cache_file: Path) -> bool:
        """Check if cache file is still valid based on TTL"""
        try:
            cache_age = time.time() - cache_file.stat().st_mtime
            cache_ttl = self.config.get('cache_ttl', 86400)  # Default 24 hours
            return cache_age < cache_ttl
        except (OSError, AttributeError):
            return False

    def _load_from_cache(self, cache_key: str) -> Optional[str]:
        """Load OCR result from cache"""
        with self._cache_lock:
            cache_file = self.cache_dir / f"{cache_key}.txt"
            if cache_file.exists():
                try:
                    # Check if cache is still valid
                    if not self._is_cache_valid(cache_file):
                        cache_file.unlink()  # Remove expired cache
                        return None
                    
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        return f.read()
                except (IOError, OSError, UnicodeDecodeError) as e:
                    self.logger.warning(f"Failed to load from cache: {e}")
            return None

    def _save_to_cache(self, cache_key: str, text: str) -> None:
        """Save OCR result to cache"""
        with self._cache_lock:
            cache_file = self.cache_dir / f"{cache_key}.txt"
            try:
                # Ensure cache directory exists
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                
                # Write to temporary file first, then move to avoid corruption
                temp_file = cache_file.with_suffix('.txt.tmp')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                temp_file.replace(cache_file)  # Atomic operation on most systems
                
            except (IOError, OSError, UnicodeEncodeError) as e:
                self.logger.warning(f"Failed to save to cache: {e}")
                # Clean up temp file if it exists
                temp_file = cache_file.with_suffix('.txt.tmp')
                if temp_file.exists():
                    try:
                        temp_file.unlink()
                    except OSError:
                        pass

    def extract_text(self, image_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract text from an image using OCR
        
        Args:
            image_path: Path to the image file
            options: OCR options (backend, languages, etc.)
            
        Returns:
            Dictionary with extracted text and metadata
        """
        # Validate and prepare the image path
        validated_path = self._validate_image_path(image_path)
        
        # Merge options with config
        ocr_options = {**self.config, **(options or {})}
        
        # Try to get from cache first
        cached_result = self._try_get_cached_result(validated_path, ocr_options)
        if cached_result:
            return cached_result
        
        # Process the image
        processed_image = self._preprocess_image_for_ocr(validated_path, ocr_options)
        
        # Extract text using selected backend
        result = self._perform_ocr_extraction(processed_image, ocr_options)
        
        # Add metadata and cache the result
        final_result = self._finalize_ocr_result(result, validated_path, ocr_options)
        
        return final_result
    
    def _validate_image_path(self, image_path: str) -> Path:
        """Validate and secure the image path"""
        if not isinstance(image_path, (str, Path)):
            raise TypeError("image_path must be a string or Path object")
            
        path = Path(image_path)
        
        # Security check: ensure path is safe (no directory traversal)
        try:
            path.resolve()
        except (OSError, RuntimeError) as e:
            raise ValueError(f"Invalid or unsafe path: {e}")
            
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")
        
        # Check if it's actually a file (not a directory)
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        
        # Check file size (prevent processing of extremely large files)
        file_size = path.stat().st_size
        max_file_size = self.config.get('max_file_size', 50 * 1024 * 1024)  # 50MB default
        if file_size > max_file_size:
            raise ValueError(f"File too large: {file_size / 1024 / 1024:.1f}MB exceeds limit of {max_file_size / 1024 / 1024:.1f}MB")
        
        if not self.format_detector.is_ocr_supported(str(path)):
            raise ValueError(f"Unsupported image format: {path.suffix}")
            
        return path
    
    def _try_get_cached_result(self, image_path: Path, options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Try to get OCR result from cache"""
        if not options.get('use_cache', True):
            return None
            
        cache_key = self._get_cache_key(image_path, options)
        cached_text = self._load_from_cache(cache_key)
        
        if cached_text:
            return {
                'text': cached_text,
                'source': 'cache',
                'confidence': None,
                'word_count': len(cached_text.split()),
                'character_count': len(cached_text)
            }
        return None
    
    def _preprocess_image_for_ocr(self, image_path: Path, options: Dict[str, Any]) -> np.ndarray:
        """Preprocess image for OCR extraction"""
        try:
            processed_image = self.image_processor.preprocess_image(
                str(image_path), 
                options.get('preprocessing', {})
            )
            return processed_image
        except Exception as e:
            raise ImageProcessingError(f"Image preprocessing failed: {e}")
    
    def _perform_ocr_extraction(self, processed_image: np.ndarray, options: Dict[str, Any]) -> Dict[str, Any]:
        """Perform the actual OCR extraction"""
        backend = options.get('backend', 'auto')
        if backend == 'auto':
            backend = self.get_preferred_backend()
        
        start_time = time.time()
        
        if backend == 'tesseract' and self.is_tesseract_available():
            result = self._extract_with_tesseract(processed_image, options)
        elif backend == 'easyocr' and self.is_easyocr_available():
            result = self._extract_with_easyocr(processed_image, options)
        else:
            raise OCRBackendError(f"Selected backend '{backend}' is not available")
        
        result['backend'] = backend
        result['duration'] = time.time() - start_time
        
        return result
    
    def _finalize_ocr_result(self, result: Dict[str, Any], image_path: Path, options: Dict[str, Any]) -> Dict[str, Any]:
        """Add metadata and cache the OCR result"""
        # Add metadata
        result.update({
            'image_path': str(image_path),
            'word_count': len(result['text'].split()),
            'character_count': len(result['text'])
        })
        
        # Cache result
        if options.get('use_cache', True):
            cache_key = self._get_cache_key(image_path, options)
            self._save_to_cache(cache_key, result['text'])
        
        return result

    def _extract_with_tesseract(self, image: np.ndarray, options: Dict[str, Any]) -> Dict[str, Any]:
        """Extract text using Tesseract OCR"""
        try:
            # Convert numpy array to PIL Image
            if len(image.shape) == 3:
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                pil_image = Image.fromarray(image)
            
            # Configure Tesseract before use
            import tesseract_config
            tesseract_config.configure_tesseract()
            
            # Extract text - use 'eng' as language code, not 'en'
            lang_codes = options.get('languages', ['eng'])
            # Map common language codes to Tesseract codes
            lang_map = {'en': 'eng', 'english': 'eng', 'fr': 'fra', 'de': 'deu', 'es': 'spa'}
            mapped_langs = [lang_map.get(lang, lang) for lang in lang_codes]
            
            text = pytesseract.image_to_string(
                pil_image,
                lang='+'.join(mapped_langs),
                config=options.get('tesseract_config', '--oem 3 --psm 6')
            )
            
            # Get confidence data
            try:
                data = pytesseract.image_to_data(
                    pil_image,
                    lang='+'.join(mapped_langs),
                    output_type=pytesseract.Output.DICT
                )
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            except (ValueError, ZeroDivisionError, KeyError) as e:
                self.logger.warning(f"Could not calculate confidence score: {e}")
                avg_confidence = None
            
            return {
                'text': text.strip(),
                'confidence': avg_confidence,
                'source': 'tesseract'
            }
            
        except Exception as e:
            raise OCRBackendError(f"Tesseract OCR failed: {e}")

    def _extract_with_easyocr(self, image: np.ndarray, options: Dict[str, Any]) -> Dict[str, Any]:
        """Extract text using EasyOCR"""
        try:
            reader = self._get_easyocr_reader(options.get('languages', ['en']))
            
            # Convert BGR to RGB if needed
            if len(image.shape) == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            # Extract text
            results = reader.readtext(image_rgb)
            
            # Combine text and calculate confidence
            text_parts = []
            confidences = []
            
            for (bbox, text, confidence) in results:
                if confidence >= options.get('confidence_threshold', 30):
                    text_parts.append(text)
                    confidences.append(confidence)
            
            combined_text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'text': combined_text.strip(),
                'confidence': avg_confidence,
                'source': 'easyocr'
            }
            
        except Exception as e:
            raise OCRBackendError(f"EasyOCR failed: {e}")

    def extract_text_from_multiple_images(
        self, 
        image_paths: List[str], 
        options: Optional[Dict[str, Any]] = None,
        max_workers: int = 2,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract text from multiple images using parallel processing
        
        Args:
            image_paths: List of image file paths
            options: OCR options
            max_workers: Maximum number of concurrent workers
            progress_callback: Optional callback for progress updates
            
        Returns:
            List of extraction results
        """
        results = []
        
        # Use thread pool manager with resource validation
        with thread_manager.managed_pool("ocr_batch_process", max_workers=max_workers) as pool:
            # Submit all tasks with backpressure handling
            future_to_path = {}
            for path in image_paths:
                future = thread_manager.submit_with_backpressure(
                    "ocr_batch_process",
                    self.extract_text,
                    path,
                    options
                )
                future_to_path[future] = path
            
            # Process completed tasks
            for i, future in enumerate(as_completed(future_to_path)):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Update progress
                    if progress_callback:
                        progress_callback(i + 1, len(image_paths))
                        
                except Exception as e:
                    self.logger.error(f"Failed to process {path}: {e}")
                    results.append({
                        'image_path': path,
                        'text': '',
                        'error': str(e),
                        'success': False
                    })
        
        return results

    def extract_text_from_multiple_images_streaming(
        self, 
        image_paths: List[str], 
        options: Optional[Dict[str, Any]] = None,
        max_workers: int = 2,
        batch_size: int = 10
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Stream OCR results from multiple images as they complete.
        Memory efficient for large batches.
        
        Args:
            image_paths: List of image file paths
            options: OCR options
            max_workers: Maximum number of concurrent workers
            batch_size: Number of images to process in each batch
            
        Yields:
            Individual extraction results as they complete
        """
        # Process images in batches to manage memory
        for i in range(0, len(image_paths), batch_size):
            batch = image_paths[i:i + batch_size]
            
            # Use thread pool manager with adaptive worker count
            batch_workers = min(max_workers, len(batch))
            with thread_manager.managed_pool("ocr_streaming", max_workers=batch_workers) as pool:
                # Submit batch tasks with backpressure
                future_to_path = {}
                for path in batch:
                    future = thread_manager.submit_with_backpressure(
                        "ocr_streaming",
                        self.extract_text,
                        path,
                        options
                    )
                    future_to_path[future] = path
                
                # Yield results as they complete
                for future in as_completed(future_to_path):
                    path = future_to_path[future]
                    try:
                        result = future.result()
                        yield result
                    except Exception as e:
                        self.logger.error(f"Failed to process {path}: {e}")
                        yield {
                            'image_path': path,
                            'text': '',
                            'error': str(e),
                            'success': False
                        }

    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """Get information about an image file"""
        try:
            return self.image_processor.get_image_info(image_path)
        except Exception as e:
            return {'error': str(e)}

    def clear_cache(self) -> bool:
        """Clear the OCR cache"""
        with self._cache_lock:
            try:
                cache_files = list(self.cache_dir.glob("*.txt"))
                temp_files = list(self.cache_dir.glob("*.txt.tmp"))
                all_files = cache_files + temp_files
                
                for cache_file in all_files:
                    try:
                        cache_file.unlink()
                    except OSError as e:
                        self.logger.warning(f"Could not delete {cache_file}: {e}")
                
                self.logger.info(f"Cleared {len(cache_files)} cache files")
                return True
            except Exception as e:
                self.logger.error(f"Failed to clear cache: {e}")
                return False

    def get_cache_size(self) -> int:
        """Get the total size of the cache in bytes"""
        with self._cache_lock:
            try:
                return sum(f.stat().st_size for f in self.cache_dir.glob("*.txt") if f.is_file())
            except (OSError, PermissionError) as e:
                self.logger.warning(f"Could not calculate cache size: {e}")
                return 0

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            cache_files = list(self.cache_dir.glob("*.txt"))
            total_size = sum(f.stat().st_size for f in cache_files)
            
            return {
                'file_count': len(cache_files),
                'total_size': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2)
            }
        except Exception as e:
            return {'error': str(e)}

    def save_result(self, result: Dict[str, Any], output_path: str, output_format: str = 'txt') -> bool:
        """
        Save OCR result to file
        
        Args:
            result: OCR result dictionary
            output_path: Output file path
            output_format: Output format (txt, json, markdown)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            text = result.get('text', '')
            
            if output_format.lower() == 'json':
                # Save as JSON with metadata
                output_data = {
                    'text': text,
                    'confidence': result.get('confidence'),
                    'backend': result.get('backend'),
                    'duration': result.get('duration'),
                    'word_count': result.get('word_count', 0),
                    'character_count': result.get('character_count', 0),
                    'image_path': result.get('image_path')
                }
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                    
            elif output_format.lower() == 'markdown':
                # Save as markdown with metadata
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# OCR Result\n\n")
                    f.write(f"**Source:** {result.get('image_path', 'Unknown')}\n\n")
                    if result.get('confidence'):
                        f.write(f"**Confidence:** {result.get('confidence'):.1f}%\n\n")
                    if result.get('backend'):
                        f.write(f"**Backend:** {result.get('backend')}\n\n")
                    f.write(f"**Word Count:** {result.get('word_count', 0)}\n\n")
                    f.write(f"**Character Count:** {result.get('character_count', 0)}\n\n")
                    f.write("---\n\n")
                    f.write(text)
                    
            else:  # txt
                # Save as plain text
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save result: {e}")
            return False

    def extract_text_from_pdf(self, pdf_path: str, language: str = 'eng') -> str:
        """
        Extract text from PDF using OCR
        
        Args:
            pdf_path: Path to PDF file
            language: Language for OCR (default: eng)
            
        Returns:
            Extracted text string
        """
        try:
            # Import PDF processing libraries
            try:
                import fitz  # PyMuPDF
            except ImportError:
                self.logger.error("PyMuPDF not available for PDF processing")
                return ""
            
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                self.logger.error(f"PDF file not found: {pdf_path}")
                return ""
            
            # Open PDF and extract text using context manager
            text = ""
            with fitz.open(str(pdf_path)) as doc:
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    page_text = page.get_text()
                    
                    # If page has no text or very little text, use OCR
                    if not page_text.strip() or len(page_text.strip()) < 50:
                        temp_image = None
                        try:
                            # Convert page to image and OCR
                            pix = page.get_pixmap()
                            try:
                                img_data = pix.tobytes("png")
                                
                                # Save temporary image
                                temp_image = pdf_path.parent / f"temp_page_{page_num}_{os.getpid()}.png"
                                with open(temp_image, 'wb') as f:
                                    f.write(img_data)
                                
                                # OCR the image
                                ocr_result = self.extract_text(str(temp_image), {'language': language})
                                ocr_text = ocr_result.get('text', '')
                                text += f"\n--- Page {page_num + 1} ---\n{ocr_text}\n"
                                
                            finally:
                                # Clean up pixmap memory
                                pix = None
                                
                        finally:
                            # Ensure temp file is always cleaned up
                            if temp_image and temp_image.exists():
                                try:
                                    temp_image.unlink()
                                except OSError as e:
                                    self.logger.warning(f"Could not delete temp file {temp_image}: {e}")
                    else:
                        text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"PDF OCR extraction failed: {e}")
            return ""
    
    def _cleanup_all_readers(self):
        """Clean up all EasyOCR readers on exit"""
        try:
            self.cleanup()
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def cleanup(self):
        """Clean up OCR engine resources"""
        # Clean up all tracked EasyOCR readers
        with self._readers_lock:
            for thread_id, reader in self._active_readers.items():
                try:
                    # EasyOCR readers don't have explicit close method, 
                    # but we can delete the reference to free memory
                    del reader
                    self.logger.debug(f"Cleaned up EasyOCR reader for thread {thread_id}")
                except Exception as e:
                    self.logger.warning(f"Error cleaning up EasyOCR reader for thread {thread_id}: {e}")
            self._active_readers.clear()
        
        # Clean up current thread's reader from thread local storage
        if hasattr(self, '_thread_local'):
            if hasattr(self._thread_local, 'easyocr_reader'):
                try:
                    del self._thread_local.easyocr_reader
                except Exception as e:
                    self.logger.warning(f"Error cleaning up thread-local EasyOCR reader: {e}")
        
        # Clear the cache
        try:
            self.clear_cache()
        except Exception as e:
            self.logger.warning(f"Error clearing cache: {e}")
        
        # Force garbage collection to free memory
        import gc
        gc.collect()
        
        self.logger.info("OCR engine cleanup completed")
    
    def __del__(self):
        """Destructor to ensure cleanup on object deletion"""
        try:
            self.cleanup()
        except Exception as e:
            # Use print since logger might not be available during destruction
            self.logger.warning(f"Error during OCR engine destruction: {e}")