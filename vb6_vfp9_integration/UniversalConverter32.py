#!/usr/bin/env python3
"""
UniversalConverter32 - VB6/VFP9 Integration Module
Provides COM interface for legacy applications
"""

import sys
import os
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from cli import main as cli_main, parse_args
    from ocr_engine.ocr_integration import OCRIntegration
    from ocr_engine.config_manager import ConfigManager
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False


class UniversalConverter32:
    """
    Main converter class for VB6/VFP9 integration
    Provides simple interface for document conversion
    """
    
    def __init__(self):
        """Initialize the converter"""
        self.version = "3.1.0"
        self.last_error = ""
        
        # Initialize OCR integration if available
        if CLI_AVAILABLE:
            try:
                self.config_manager = ConfigManager()
                self.ocr_integration = OCRIntegration(config_manager=self.config_manager)
                self.initialized = True
            except Exception as e:
                self.last_error = f"Initialization failed: {e}"
                self.initialized = False
        else:
            self.initialized = False
            self.last_error = "CLI module not available"
    
    def ConvertDocument(self, input_path: str, output_path: str, output_format: str = "txt") -> int:
        """
        Convert document from input to output format
        
        Args:
            input_path: Path to input file
            output_path: Path to output file  
            output_format: Output format (txt, docx, pdf, html, etc.)
            
        Returns:
            1 for success, 0 for failure
        """
        try:
            if not self.initialized:
                self.last_error = "Converter not initialized"
                return 0
            
            # Validate input file exists
            if not Path(input_path).exists():
                self.last_error = f"Input file not found: {input_path}"
                return 0
            
            # Create output directory if needed
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Use CLI for conversion
            sys.argv = [
                'cli.py',
                input_path,
                '-o', output_path,
                '-t', output_format,
                '--quiet'
            ]
            
            # Capture CLI result
            result = cli_main()
            
            if result == 0:  # Success
                self.last_error = ""
                return 1
            else:
                self.last_error = "Conversion failed"
                return 0
                
        except Exception as e:
            self.last_error = str(e)
            return 0
    
    def ConvertDocumentWithOCR(self, input_path: str, output_path: str, 
                              output_format: str = "txt", ocr_language: str = "eng") -> int:
        """
        Convert document with OCR enabled
        
        Args:
            input_path: Path to input file
            output_path: Path to output file
            output_format: Output format
            ocr_language: OCR language (eng, fra, deu, etc.)
            
        Returns:
            1 for success, 0 for failure
        """
        try:
            if not self.initialized:
                self.last_error = "Converter not initialized"
                return 0
            
            # Validate input file exists
            if not Path(input_path).exists():
                self.last_error = f"Input file not found: {input_path}"
                return 0
            
            # Create output directory if needed
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Use CLI with OCR options
            sys.argv = [
                'cli.py',
                input_path,
                '-o', output_path,
                '-t', output_format,
                '--ocr',
                '--lang', ocr_language,
                '--quiet'
            ]
            
            # Capture CLI result
            result = cli_main()
            
            if result == 0:  # Success
                self.last_error = ""
                return 1
            else:
                self.last_error = "OCR conversion failed"
                return 0
                
        except Exception as e:
            self.last_error = str(e)
            return 0
    
    def GetLastError(self) -> str:
        """Get last error message"""
        return self.last_error
    
    def GetVersion(self) -> str:
        """Get version string"""
        return self.version
    
    def IsOCRAvailable(self) -> int:
        """Check if OCR is available (1=yes, 0=no)"""
        if not self.initialized:
            return 0
        
        try:
            status = self.ocr_integration.check_availability()
            return 1 if status.get('available', False) else 0
        except:
            return 0
    
    def GetSupportedFormats(self) -> str:
        """Get supported format list as comma-separated string"""
        formats = [
            # Input formats
            "jpg", "jpeg", "png", "tiff", "tif", "bmp", "gif", "webp", "pdf",
            "txt", "docx", "html", "rtf", "epub",
            # Output formats  
            "txt", "docx", "pdf", "html", "rtf", "epub", "json", "markdown"
        ]
        return ",".join(sorted(set(formats)))
    
    def BatchConvert(self, input_dir: str, output_dir: str, 
                    input_pattern: str = "*", output_format: str = "txt") -> str:
        """
        Batch convert files in directory
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            input_pattern: File pattern (*.pdf, *.jpg, etc.)
            output_format: Output format
            
        Returns:
            JSON string with results
        """
        try:
            if not self.initialized:
                return json.dumps({"error": "Converter not initialized"})
            
            input_path = Path(input_dir)
            output_path = Path(output_dir)
            
            if not input_path.exists():
                return json.dumps({"error": f"Input directory not found: {input_dir}"})
            
            # Create output directory
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Find matching files
            files = list(input_path.glob(input_pattern))
            results = {
                "total": len(files),
                "successful": 0,
                "failed": 0,
                "files": []
            }
            
            for file_path in files:
                output_file = output_path / f"{file_path.stem}.{output_format}"
                
                result = self.ConvertDocument(str(file_path), str(output_file), output_format)
                
                file_result = {
                    "input": str(file_path),
                    "output": str(output_file),
                    "success": result == 1,
                    "error": self.last_error if result == 0 else ""
                }
                
                results["files"].append(file_result)
                
                if result == 1:
                    results["successful"] += 1
                else:
                    results["failed"] += 1
            
            return json.dumps(results, indent=2)
            
        except Exception as e:
            return json.dumps({"error": str(e)})


# Global instance for procedural interface (VB6/VFP9 compatibility)
_converter_instance = None

def GetConverter():
    """Get global converter instance"""
    global _converter_instance
    if _converter_instance is None:
        _converter_instance = UniversalConverter32()
    return _converter_instance

# Procedural interface functions for VB6/VFP9
def ConvertDocument(input_path: str, output_path: str, output_format: str = "txt") -> int:
    """Convert document - procedural interface"""
    return GetConverter().ConvertDocument(input_path, output_path, output_format)

def ConvertDocumentWithOCR(input_path: str, output_path: str, 
                          output_format: str = "txt", ocr_language: str = "eng") -> int:
    """Convert document with OCR - procedural interface"""
    return GetConverter().ConvertDocumentWithOCR(input_path, output_path, output_format, ocr_language)

def GetLastError() -> str:
    """Get last error - procedural interface"""
    return GetConverter().GetLastError()

def GetVersion() -> str:
    """Get version - procedural interface"""
    return GetConverter().GetVersion()

def IsOCRAvailable() -> int:
    """Check OCR availability - procedural interface"""
    return GetConverter().IsOCRAvailable()

def GetSupportedFormats() -> str:
    """Get supported formats - procedural interface"""
    return GetConverter().GetSupportedFormats()


if __name__ == "__main__":
    # Test the converter
    converter = UniversalConverter32()
    print(f"UniversalConverter32 v{converter.GetVersion()}")
    print(f"Initialized: {converter.initialized}")
    print(f"OCR Available: {converter.IsOCRAvailable()}")
    print(f"Supported Formats: {converter.GetSupportedFormats()}")
    
    if len(sys.argv) > 3:
        # Command line usage
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        format_type = sys.argv[3] if len(sys.argv) > 3 else "txt"
        
        print(f"Converting {input_file} -> {output_file} ({format_type})")
        result = converter.ConvertDocument(input_file, output_file, format_type)
        
        if result == 1:
            print("✅ Conversion successful!")
        else:
            print(f"❌ Conversion failed: {converter.GetLastError()}")
        
        sys.exit(0 if result == 1 else 1)