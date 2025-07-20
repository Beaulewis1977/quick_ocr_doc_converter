"""
Azure Cognitive Services Computer Vision backend for OCR

Provides OCR capabilities using Azure's Computer Vision API with
support for printed and handwritten text recognition.

Author: Terry AI Agent for Terragon Labs
"""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import time

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from azure.cognitiveservices.vision.computervision import ComputerVisionClient
    from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
    from msrest.authentication import CognitiveServicesCredentials
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

from .base import CloudOCRBackend

class AzureVisionBackend(CloudOCRBackend):
    """
    Azure Cognitive Services Computer Vision OCR backend
    
    Features:
    - Print and handwriting text recognition
    - Multi-language support
    - Enterprise-grade security and compliance
    - Batch processing support
    - Cost tracking and optimization
    - GDPR compliance for European operations
    """
    
    # Azure Computer Vision pricing (as of 2024)
    COST_PER_1000_TRANSACTIONS = 1.00  # USD for OCR operations
    
    # Supported languages
    SUPPORTED_LANGUAGES = [
        'en', 'es', 'fr', 'de', 'it', 'pt', 'nl', 'ru', 'zh', 'ja', 'ko',
        'ar', 'hi', 'th', 'vi', 'sv', 'da', 'no', 'fi', 'pl', 'cs', 'hu'
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Azure Vision backend
        
        Args:
            config: Configuration dictionary containing:
                - subscription_key: Azure Cognitive Services subscription key
                - endpoint: Azure Cognitive Services endpoint URL
                - region: Azure region (optional)
        """
        super().__init__(config)
        self.logger = logging.getLogger("AzureVisionBackend")
        self.client = None
        self.endpoint = config.get('endpoint', '')
        self.subscription_key = config.get('subscription_key', '')
        
        if not AZURE_AVAILABLE:
            self.logger.error("Azure Cognitive Services library not available")
            return
        
        # Initialize client
        self._init_client()
    
    def _init_client(self):
        """Initialize the Azure Computer Vision client"""
        try:
            if not self.subscription_key or not self.endpoint:
                self.logger.error("Azure subscription key and endpoint are required")
                return
            
            credentials = CognitiveServicesCredentials(self.subscription_key)
            self.client = ComputerVisionClient(self.endpoint, credentials)
            
            self.logger.info("Azure Computer Vision client initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure Computer Vision client: {e}")
            self.client = None
    
    def authenticate(self) -> bool:
        """
        Test authentication with Azure Computer Vision
        
        Returns:
            True if authentication is successful
        """
        if not self.client:
            return False
        
        try:
            # Test with a minimal request to validate credentials
            # We'll use the list models endpoint which doesn't consume quota
            response = requests.get(
                f"{self.endpoint}/vision/v3.2/models",
                headers={'Ocp-Apim-Subscription-Key': self.subscription_key}
            )
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Azure Computer Vision authentication failed: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Azure Vision backend is available"""
        return AZURE_AVAILABLE and self.client is not None
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def get_cost_estimate(self, image_path: str) -> Optional[float]:
        """
        Estimate cost for processing an image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Estimated cost in USD
        """
        return self.COST_PER_1000_TRANSACTIONS / 1000  # Cost per single transaction
    
    def extract_text(self, image_path: str, language: str = 'en') -> Dict[str, Any]:
        """
        Extract text from image using Azure Computer Vision
        
        Args:
            image_path: Path to the image file
            language: Language code for OCR
            
        Returns:
            Dictionary with extraction results
        """
        if not self.is_available():
            return {
                'text': '',
                'confidence': 0,
                'backend': 'azure_vision',
                'language': language,
                'success': False,
                'error': 'Azure Vision backend not available'
            }
        
        try:
            # Read image file
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Start the read operation
            read_response = self.client.read_in_stream(
                image_data,
                language=language,
                raw=True
            )
            
            # Get operation ID from response headers
            operation_location = read_response.headers['Operation-Location']
            operation_id = operation_location.split('/')[-1]
            
            # Poll for completion
            result = self._poll_for_result(operation_id)
            
            if result['success']:
                # Track usage and cost
                cost = self.get_cost_estimate(image_path)
                self.track_usage(cost)
                result['cost'] = cost
            
            return result
            
        except Exception as e:
            self.logger.error(f"Azure Vision OCR failed for {image_path}: {e}")
            return {
                'text': '',
                'confidence': 0,
                'backend': 'azure_vision',
                'language': language,
                'success': False,
                'error': str(e)
            }
    
    def _poll_for_result(self, operation_id: str, max_wait_time: int = 60) -> Dict[str, Any]:
        """
        Poll for read operation result
        
        Args:
            operation_id: Operation ID from read operation
            max_wait_time: Maximum time to wait in seconds
            
        Returns:
            Dictionary with extraction results
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                result = self.client.get_read_result(operation_id)
                
                if result.status == OperationStatusCodes.succeeded:
                    return self._process_read_result(result)
                elif result.status == OperationStatusCodes.failed:
                    return {
                        'text': '',
                        'confidence': 0,
                        'backend': 'azure_vision',
                        'success': False,
                        'error': 'Azure read operation failed'
                    }
                elif result.status in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                    time.sleep(1)  # Wait 1 second before polling again
                else:
                    return {
                        'text': '',
                        'confidence': 0,
                        'backend': 'azure_vision',
                        'success': False,
                        'error': f'Unknown operation status: {result.status}'
                    }
                    
            except Exception as e:
                return {
                    'text': '',
                    'confidence': 0,
                    'backend': 'azure_vision',
                    'success': False,
                    'error': f'Polling failed: {e}'
                }
        
        # Timeout
        return {
            'text': '',
            'confidence': 0,
            'backend': 'azure_vision',
            'success': False,
            'error': f'Operation timed out after {max_wait_time} seconds'
        }
    
    def _process_read_result(self, result) -> Dict[str, Any]:
        """
        Process the read operation result
        
        Args:
            result: Azure read operation result
            
        Returns:
            Dictionary with processed results
        """
        text_blocks = []
        lines = []
        words = []
        confidences = []
        
        # Extract text from all pages
        for page in result.analyze_result.read_results:
            page_info = {
                'page_number': page.page,
                'width': page.width,
                'height': page.height,
                'unit': page.unit,
                'angle': page.angle
            }
            
            for line in page.lines:
                line_text = line.text
                text_blocks.append(line_text)
                
                # Extract bounding box
                bbox = {
                    'x': min(point.x for point in line.bounding_box),
                    'y': min(point.y for point in line.bounding_box),
                    'width': max(point.x for point in line.bounding_box) - min(point.x for point in line.bounding_box),
                    'height': max(point.y for point in line.bounding_box) - min(point.y for point in line.bounding_box)
                }
                
                line_info = {
                    'text': line_text,
                    'bounding_box': bbox,
                    'page': page.page
                }
                lines.append(line_info)
                
                # Process words in the line
                for word in line.words:
                    word_bbox = {
                        'x': min(point.x for point in word.bounding_box),
                        'y': min(point.y for point in word.bounding_box),
                        'width': max(point.x for point in word.bounding_box) - min(point.x for point in word.bounding_box),
                        'height': max(point.y for point in word.bounding_box) - min(point.y for point in word.bounding_box)
                    }
                    
                    word_info = {
                        'text': word.text,
                        'confidence': word.confidence,
                        'bounding_box': word_bbox,
                        'page': page.page
                    }
                    words.append(word_info)
                    confidences.append(word.confidence)
        
        # Combine all text
        full_text = '\n'.join(text_blocks)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        metadata = {
            'page_count': len(result.analyze_result.read_results),
            'line_count': len(lines),
            'word_count': len(words),
            'lines': lines,
            'words': words
        }
        
        return {
            'text': full_text,
            'confidence': avg_confidence * 100,  # Convert to percentage
            'backend': 'azure_vision',
            'success': True,
            'metadata': metadata
        }
    
    def extract_handwriting(self, image_path: str, language: str = 'en') -> Dict[str, Any]:
        """
        Extract handwritten text using Azure Computer Vision
        
        Args:
            image_path: Path to the image file
            language: Language code
            
        Returns:
            Dictionary with extraction results optimized for handwriting
        """
        # Azure's Read API handles both printed and handwritten text automatically
        result = self.extract_text(image_path, language)
        
        if result['success']:
            result['metadata']['optimized_for'] = 'handwriting'
        
        return result
    
    def batch_extract_text(self, image_paths: List[str], language: str = 'en', 
                          max_concurrent: int = 5) -> List[Dict[str, Any]]:
        """
        Extract text from multiple images with controlled concurrency
        
        Args:
            image_paths: List of image file paths
            language: Language code
            max_concurrent: Maximum number of concurrent operations
            
        Returns:
            List of extraction results
        """
        results = []
        
        # Process in batches to respect rate limits
        for i in range(0, len(image_paths), max_concurrent):
            batch = image_paths[i:i + max_concurrent]
            batch_results = []
            
            # Start all operations in the batch
            operation_ids = []
            for image_path in batch:
                try:
                    with open(image_path, 'rb') as image_file:
                        image_data = image_file.read()
                    
                    read_response = self.client.read_in_stream(
                        image_data,
                        language=language,
                        raw=True
                    )
                    
                    operation_location = read_response.headers['Operation-Location']
                    operation_id = operation_location.split('/')[-1]
                    operation_ids.append((operation_id, image_path))
                    
                except Exception as e:
                    batch_results.append({
                        'text': '',
                        'confidence': 0,
                        'backend': 'azure_vision',
                        'language': language,
                        'success': False,
                        'error': str(e),
                        'image_path': image_path
                    })
            
            # Poll for all results in the batch
            for operation_id, image_path in operation_ids:
                result = self._poll_for_result(operation_id)
                result['image_path'] = image_path
                result['language'] = language
                
                if result['success']:
                    cost = self.get_cost_estimate(image_path)
                    self.track_usage(cost)
                    result['cost'] = cost
                
                batch_results.append(result)
            
            results.extend(batch_results)
            
            # Small delay between batches to respect rate limits
            if i + max_concurrent < len(image_paths):
                time.sleep(1)
        
        return results
    
    def get_supported_regions(self) -> List[str]:
        """
        Get list of supported Azure regions for Computer Vision
        
        Returns:
            List of region names
        """
        return [
            'eastus', 'eastus2', 'westus', 'westus2', 'westcentralus',
            'southcentralus', 'northcentralus', 'centralus',
            'westeurope', 'northeurope', 'uksouth', 'ukwest',
            'francecentral', 'germanywestcentral', 'switzerlandnorth',
            'brazilsouth', 'canadacentral', 'canadaeast',
            'australiaeast', 'australiasoutheast', 'centralindia',
            'southindia', 'japaneast', 'japanwest',
            'koreacentral', 'koreasouth', 'southeastasia', 'eastasia'
        ]
    
    def cleanup(self):
        """Cleanup Azure Computer Vision client resources"""
        if self.client:
            # Azure clients don't require explicit cleanup
            pass