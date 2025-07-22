# Universal Document Converter - Settings & Configuration Guide

This guide covers all configuration options, settings files, and customization possibilities for Universal Document Converter v2.1.0.

## Table of Contents

1. [Configuration Files Overview](#configuration-files-overview)
2. [Application Settings](#application-settings)
3. [OCR Configuration](#ocr-configuration)
4. [VFP9/VB6 Configuration](#vfp9vb6-configuration)
5. [Environment Variables](#environment-variables)
6. [Command Line Configuration](#command-line-configuration)
7. [GUI Preferences](#gui-preferences)
8. [Performance Tuning](#performance-tuning)
9. [Security Settings](#security-settings)
10. [Advanced Configuration](#advanced-configuration)

## Configuration Files Overview

Universal Document Converter uses several configuration files:

| File | Purpose | Location |
|------|---------|----------|
| `settings.json` | Main application settings | App directory or `%APPDATA%\UniversalConverter\` |
| `vfp9_config.json` | VFP9/VB6 integration settings | App directory |
| `ocr_config.json` | OCR engine settings | App directory |
| `.env` | Environment variables | App directory |
| `user_preferences.json` | GUI user preferences | `%APPDATA%\UniversalConverter\` |

## Application Settings

### Main Settings File (`settings.json`)

```json
{
    "version": "2.1.0",
    "app_settings": {
        "default_input_format": "auto",
        "default_output_format": "pdf",
        "auto_detect_format": true,
        "preserve_metadata": true,
        "preserve_formatting": true,
        "overwrite_existing": false,
        "create_backup": false,
        "timestamp_output": false
    },
    "quality_settings": {
        "default_quality": "high",
        "pdf_compression": "standard",
        "image_dpi": 300,
        "jpeg_quality": 85,
        "png_compression": 6
    },
    "batch_settings": {
        "parallel_workers": 4,
        "max_concurrent_files": 10,
        "chunk_size_mb": 10,
        "recursive_scan": true,
        "follow_symlinks": false,
        "skip_hidden_files": true
    },
    "path_settings": {
        "temp_directory": "${TEMP}/UniversalConverter",
        "output_directory": "${DOCUMENTS}/Converted",
        "log_directory": "${APPDATA}/UniversalConverter/logs",
        "cache_directory": "${APPDATA}/UniversalConverter/cache"
    },
    "logging": {
        "enabled": true,
        "level": "INFO",
        "max_file_size_mb": 10,
        "max_files": 5,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    },
    "ui_settings": {
        "theme": "light",
        "language": "en",
        "show_tooltips": true,
        "confirm_exit": true,
        "remember_window_position": true,
        "auto_update_check": true
    }
}
```

### Setting Descriptions

#### App Settings
- **default_input_format**: Default format for input files ("auto" for automatic detection)
- **default_output_format**: Default output format (pdf, docx, rtf, html, txt, md)
- **auto_detect_format**: Automatically detect input file format
- **preserve_metadata**: Keep document metadata (author, creation date, etc.)
- **preserve_formatting**: Maintain original formatting when possible
- **overwrite_existing**: Overwrite existing output files without asking
- **create_backup**: Create backup of existing files before overwriting
- **timestamp_output**: Add timestamp to output filenames

#### Quality Settings
- **default_quality**: Default conversion quality (low, medium, high)
- **pdf_compression**: PDF compression level (none, low, standard, high)
- **image_dpi**: DPI for image outputs
- **jpeg_quality**: JPEG compression quality (1-100)
- **png_compression**: PNG compression level (0-9)

#### Batch Settings
- **parallel_workers**: Number of parallel conversion threads
- **max_concurrent_files**: Maximum files to process simultaneously
- **chunk_size_mb**: File chunk size for large file processing
- **recursive_scan**: Include subdirectories in batch operations
- **follow_symlinks**: Follow symbolic links
- **skip_hidden_files**: Skip hidden files and folders

## OCR Configuration

### OCR Settings File (`ocr_config.json`)

```json
{
    "ocr_settings": {
        "default_engine": "tesseract",
        "fallback_engine": "easyocr",
        "auto_engine_selection": true,
        "confidence_threshold": 0.6
    },
    "tesseract_settings": {
        "executable_path": "auto",
        "data_path": "auto",
        "default_language": "eng",
        "additional_languages": ["fra", "deu", "spa"],
        "page_segmentation_mode": 3,
        "ocr_engine_mode": 3,
        "custom_config": "--psm 3 --oem 3"
    },
    "easyocr_settings": {
        "default_languages": ["en"],
        "gpu_enabled": true,
        "model_storage_directory": "${APPDATA}/UniversalConverter/easyocr_models",
        "download_enabled": true,
        "detector": true,
        "recognizer": true
    },
    "preprocessing": {
        "enabled": true,
        "deskew": true,
        "denoise": true,
        "remove_background": false,
        "enhance_contrast": true,
        "binarize": false,
        "scale_factor": 2.0
    },
    "performance": {
        "max_image_dimension": 4096,
        "batch_size": 1,
        "worker_threads": 2,
        "gpu_memory_fraction": 0.7,
        "cache_results": true
    }
}
```

### OCR Language Codes

Common language codes for OCR:

| Language | Tesseract Code | EasyOCR Code |
|----------|----------------|--------------|
| English | eng | en |
| Spanish | spa | es |
| French | fra | fr |
| German | deu | de |
| Italian | ita | it |
| Portuguese | por | pt |
| Russian | rus | ru |
| Chinese (Simplified) | chi_sim | ch_sim |
| Chinese (Traditional) | chi_tra | ch_tra |
| Japanese | jpn | ja |
| Korean | kor | ko |
| Arabic | ara | ar |

### OCR Configuration Examples

#### High Accuracy Configuration
```json
{
    "ocr_settings": {
        "default_engine": "tesseract",
        "confidence_threshold": 0.8
    },
    "preprocessing": {
        "enabled": true,
        "deskew": true,
        "denoise": true,
        "enhance_contrast": true,
        "scale_factor": 3.0
    }
}
```

#### Fast Processing Configuration
```json
{
    "ocr_settings": {
        "default_engine": "easyocr",
        "confidence_threshold": 0.5
    },
    "preprocessing": {
        "enabled": false
    },
    "performance": {
        "batch_size": 4,
        "worker_threads": 4
    }
}
```

## VFP9/VB6 Configuration

### Integration Settings (`vfp9_config.json`)

```json
{
    "integration": {
        "default_method": "json_file",
        "timeout_seconds": 30,
        "retry_attempts": 3,
        "retry_delay_ms": 1000
    },
    "json_ipc": {
        "request_file": "C:\\temp\\uc_request.json",
        "response_file": "C:\\temp\\uc_response.json",
        "watch_interval_ms": 100,
        "auto_cleanup": true,
        "use_timestamps": true
    },
    "named_pipes": {
        "pipe_name": "\\\\.\\pipe\\UniversalConverter",
        "buffer_size": 4096,
        "timeout_ms": 5000,
        "max_instances": 10
    },
    "com_server": {
        "progid": "UniversalConverter.Application",
        "clsid": "{12345678-1234-1234-1234-123456789012}",
        "threading_model": "Apartment",
        "auto_register": false
    },
    "dll_wrapper": {
        "dll_path": "UniversalConverter32.dll",
        "calling_convention": "stdcall",
        "unicode_strings": false,
        "error_mode": "return_codes"
    },
    "paths": {
        "python_executable": "python",
        "converter_script": "universal_document_converter_ocr.py",
        "working_directory": "C:\\UniversalConverter"
    }
}
```

### Method-Specific Configurations

#### JSON IPC Optimized
```json
{
    "json_ipc": {
        "request_file": "${TEMP}\\uc_request_${PID}.json",
        "response_file": "${TEMP}\\uc_response_${PID}.json",
        "compression": true,
        "encryption": false
    }
}
```

#### Named Pipes High-Performance
```json
{
    "named_pipes": {
        "pipe_name": "\\\\.\\pipe\\UC_${COMPUTERNAME}",
        "buffer_size": 65536,
        "async_io": true,
        "message_mode": true
    }
}
```

## Environment Variables

### System Environment Variables

```bash
# Core paths
UC_HOME=C:\UniversalConverter
UC_PYTHON_PATH=C:\Python39\python.exe
UC_TEMP_DIR=C:\Temp\UniversalConverter

# OCR settings
UC_TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
UC_TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
UC_OCR_LANGUAGES=eng+fra+deu

# Performance
UC_MAX_WORKERS=8
UC_MEMORY_LIMIT=2048
UC_GPU_ENABLED=true

# Logging
UC_LOG_LEVEL=INFO
UC_LOG_FILE=converter.log
UC_DEBUG_MODE=false

# Network
UC_PROXY_SERVER=proxy.company.com:8080
UC_PROXY_BYPASS=localhost,127.0.0.1
```

### User Environment Variables (.env file)

```bash
# User preferences
DEFAULT_OUTPUT_FORMAT=pdf
DEFAULT_QUALITY=high
OCR_ENABLED=true
OCR_LANGUAGE=eng

# Paths
INPUT_DIRECTORY=/home/user/documents
OUTPUT_DIRECTORY=/home/user/converted
TEMP_DIRECTORY=/tmp/converter

# API Keys (if using cloud OCR)
GOOGLE_CLOUD_API_KEY=your-api-key-here
AZURE_CV_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_CV_KEY=your-key-here

# Feature flags
ENABLE_MARKDOWN=true
ENABLE_BATCH_PROCESSING=true
ENABLE_CLOUD_OCR=false
```

## Command Line Configuration

### Configuration via CLI Arguments

```bash
# Set configuration values
python universal_document_converter_ocr.py --config set default_output_format pdf
python universal_document_converter_ocr.py --config set ocr.default_engine tesseract
python universal_document_converter_ocr.py --config set batch.parallel_workers 8

# Get configuration values
python universal_document_converter_ocr.py --config get default_output_format
python universal_document_converter_ocr.py --config list

# Reset configuration
python universal_document_converter_ocr.py --config reset
python universal_document_converter_ocr.py --config reset ocr_settings
```

### Configuration Profiles

```bash
# Save current configuration as profile
python universal_document_converter_ocr.py --config save-profile high-quality

# Load configuration profile
python universal_document_converter_ocr.py --config load-profile high-quality

# List available profiles
python universal_document_converter_ocr.py --config list-profiles

# Delete profile
python universal_document_converter_ocr.py --config delete-profile old-profile
```

### Profile Examples

#### High Quality Profile
```json
{
    "name": "high-quality",
    "description": "Maximum quality settings for important documents",
    "settings": {
        "quality_settings.default_quality": "high",
        "quality_settings.image_dpi": 600,
        "quality_settings.jpeg_quality": 95,
        "ocr_settings.confidence_threshold": 0.9,
        "preprocessing.enabled": true,
        "preprocessing.scale_factor": 3.0
    }
}
```

#### Fast Processing Profile
```json
{
    "name": "fast-processing",
    "description": "Optimized for speed over quality",
    "settings": {
        "quality_settings.default_quality": "medium",
        "quality_settings.image_dpi": 150,
        "batch_settings.parallel_workers": 8,
        "preprocessing.enabled": false,
        "ocr_settings.confidence_threshold": 0.5
    }
}
```

## GUI Preferences

### User Preferences File (`user_preferences.json`)

```json
{
    "window": {
        "width": 1200,
        "height": 800,
        "x": 100,
        "y": 100,
        "maximized": false,
        "always_on_top": false
    },
    "appearance": {
        "theme": "light",
        "accent_color": "#0078D4",
        "font_family": "Segoe UI",
        "font_size": 10,
        "high_contrast": false
    },
    "behavior": {
        "auto_convert_on_drop": true,
        "show_preview": true,
        "play_sounds": true,
        "minimize_to_tray": true,
        "start_with_windows": false
    },
    "recent": {
        "files": [],
        "directories": [],
        "formats": ["pdf", "docx", "md"],
        "max_items": 10
    },
    "shortcuts": {
        "convert": "Ctrl+Enter",
        "open_file": "Ctrl+O",
        "save_as": "Ctrl+S",
        "preferences": "Ctrl+,",
        "quit": "Ctrl+Q"
    }
}
```

### Theme Configuration

#### Custom Theme Example
```json
{
    "theme": {
        "name": "custom-dark",
        "colors": {
            "background": "#1E1E1E",
            "foreground": "#FFFFFF",
            "accent": "#007ACC",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#F44336"
        },
        "fonts": {
            "ui": "Segoe UI",
            "monospace": "Consolas",
            "size_small": 9,
            "size_normal": 10,
            "size_large": 12
        }
    }
}
```

## Performance Tuning

### Performance Configuration

```json
{
    "performance": {
        "memory": {
            "max_memory_mb": 2048,
            "cache_size_mb": 512,
            "gc_threshold_mb": 1024,
            "low_memory_mode": false
        },
        "threading": {
            "thread_pool_size": 8,
            "io_threads": 4,
            "cpu_threads": 4,
            "gpu_threads": 2
        },
        "optimization": {
            "lazy_loading": true,
            "stream_processing": true,
            "batch_optimization": true,
            "pipeline_mode": true
        },
        "limits": {
            "max_file_size_mb": 500,
            "max_pages": 1000,
            "max_batch_size": 100,
            "timeout_seconds": 300
        }
    }
}
```

### Hardware-Specific Tuning

#### For High-End Systems
```json
{
    "performance": {
        "threading": {
            "thread_pool_size": 16,
            "cpu_threads": 12,
            "gpu_threads": 4
        },
        "memory": {
            "max_memory_mb": 8192,
            "cache_size_mb": 2048
        }
    }
}
```

#### For Low-End Systems
```json
{
    "performance": {
        "threading": {
            "thread_pool_size": 2,
            "cpu_threads": 2,
            "gpu_threads": 0
        },
        "memory": {
            "max_memory_mb": 512,
            "low_memory_mode": true
        }
    }
}
```

## Security Settings

### Security Configuration

```json
{
    "security": {
        "file_validation": {
            "check_file_signatures": true,
            "scan_for_malware": false,
            "max_file_size_mb": 100,
            "allowed_extensions": ["pdf", "docx", "txt", "rtf", "md"],
            "blocked_extensions": ["exe", "bat", "cmd", "ps1"]
        },
        "pdf_security": {
            "allow_encrypted_input": true,
            "preserve_encryption": false,
            "default_encryption_level": "128-bit",
            "default_permissions": {
                "print": true,
                "modify": false,
                "copy": true,
                "annotations": false
            }
        },
        "network": {
            "allow_network_paths": false,
            "allow_unc_paths": false,
            "verify_ssl_certificates": true,
            "proxy_authentication": false
        },
        "sandboxing": {
            "enabled": false,
            "temp_directory_isolation": true,
            "process_isolation": false,
            "memory_limits": true
        }
    }
}
```

### Encryption Settings

```json
{
    "encryption": {
        "pdf_encryption": {
            "algorithm": "AES",
            "key_length": 256,
            "compatibility": "PDF 2.0"
        },
        "file_encryption": {
            "enabled": false,
            "algorithm": "AES-256-GCM",
            "key_derivation": "PBKDF2"
        },
        "communication": {
            "encrypt_ipc": false,
            "tls_version": "1.3",
            "cipher_suites": ["TLS_AES_256_GCM_SHA384"]
        }
    }
}
```

## Advanced Configuration

### Plugin Configuration

```json
{
    "plugins": {
        "enabled": true,
        "directory": "${APP_DIR}/plugins",
        "auto_load": true,
        "whitelist": ["official_ocr_plugin", "markdown_extended"],
        "blacklist": [],
        "settings": {
            "official_ocr_plugin": {
                "priority": 1,
                "config": {
                    "engine": "advanced"
                }
            }
        }
    }
}
```

### API Configuration

```json
{
    "api": {
        "enabled": true,
        "host": "127.0.0.1",
        "port": 8080,
        "authentication": "token",
        "cors_enabled": true,
        "rate_limiting": {
            "enabled": true,
            "requests_per_minute": 60,
            "burst_size": 10
        },
        "endpoints": {
            "convert": "/api/v1/convert",
            "status": "/api/v1/status",
            "formats": "/api/v1/formats"
        }
    }
}
```

### Monitoring Configuration

```json
{
    "monitoring": {
        "metrics": {
            "enabled": true,
            "export_interval": 60,
            "exporters": ["prometheus", "json_file"]
        },
        "tracing": {
            "enabled": false,
            "sampling_rate": 0.1,
            "exporter": "jaeger"
        },
        "health_checks": {
            "enabled": true,
            "interval": 30,
            "endpoints": ["/health", "/ready"]
        }
    }
}
```

## Configuration Best Practices

### 1. Configuration Hierarchy

Configuration sources are loaded in this order (later overrides earlier):
1. Default settings (built-in)
2. System configuration file
3. User configuration file
4. Environment variables
5. Command line arguments

### 2. Configuration Validation

```bash
# Validate configuration files
python universal_document_converter_ocr.py --config validate

# Check specific configuration
python universal_document_converter_ocr.py --config check ocr_settings

# Test configuration
python universal_document_converter_ocr.py --config test
```

### 3. Backup and Restore

```bash
# Backup current configuration
python universal_document_converter_ocr.py --config backup config_backup.zip

# Restore configuration
python universal_document_converter_ocr.py --config restore config_backup.zip

# Export configuration
python universal_document_converter_ocr.py --config export > my_config.json

# Import configuration
python universal_document_converter_ocr.py --config import my_config.json
```

### 4. Configuration Templates

Create template configurations for different use cases:

#### Development Template
```json
{
    "template": "development",
    "logging.level": "DEBUG",
    "logging.enabled": true,
    "security.file_validation.check_file_signatures": false,
    "performance.optimization.pipeline_mode": false
}
```

#### Production Template
```json
{
    "template": "production",
    "logging.level": "WARNING",
    "security.file_validation.check_file_signatures": true,
    "performance.optimization.pipeline_mode": true,
    "monitoring.metrics.enabled": true
}
```

### 5. Troubleshooting Configuration Issues

#### Check Active Configuration
```bash
# Show all active settings
python universal_document_converter_ocr.py --config show

# Show configuration sources
python universal_document_converter_ocr.py --config sources

# Debug configuration loading
python universal_document_converter_ocr.py --config debug
```

#### Common Issues

1. **Settings not taking effect**
   - Check configuration hierarchy
   - Verify file permissions
   - Look for syntax errors in JSON

2. **Performance issues**
   - Review thread and memory settings
   - Check hardware limitations
   - Monitor resource usage

3. **OCR not working**
   - Verify OCR engine paths
   - Check language data files
   - Review preprocessing settings

---

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or visit [GitHub Issues](https://github.com/Beaulewis1977/quick_ocr_doc_converter/issues)