"""
Simplified DLL wrapper for UniversalConverter32
This creates a ctypes-compatible interface
"""

import ctypes
import json
import os
import sys
from pathlib import Path

# Simple file-based communication for 32-bit compatibility
COMM_DIR = Path(os.environ.get('TEMP', '/tmp')) / 'UniversalConverter'
COMM_DIR.mkdir(exist_ok=True)

def ConvertDocument(input_file, output_file, input_format, output_format):
    """Convert document via file-based IPC"""
    try:
        # Create request file
        request = {
            'action': 'convert',
            'input_file': input_file.decode('utf-8') if isinstance(input_file, bytes) else input_file,
            'output_file': output_file.decode('utf-8') if isinstance(output_file, bytes) else output_file,
            'input_format': input_format.decode('utf-8') if isinstance(input_format, bytes) else input_format,
            'output_format': output_format.decode('utf-8') if isinstance(output_format, bytes) else output_format,
        }
        
        request_file = COMM_DIR / 'request.json'
        with open(request_file, 'w') as f:
            json.dump(request, f)
        
        # Call the converter
        cmd = f'"{sys.executable}" -m universal_document_converter_ocr --json-request "{request_file}"'
        result = os.system(cmd)
        
        # Check result
        response_file = COMM_DIR / 'response.json'
        if response_file.exists():
            with open(response_file, 'r') as f:
                response = json.load(f)
            return 1 if response.get('success') else 0
        
        return 0 if result == 0 else -1
        
    except Exception as e:
        print(f"ConvertDocument error: {e}")
        return -1

def TestConnection():
    """Test if converter is available"""
    try:
        import universal_document_converter_ocr
        return 1
    except:
        return 0

def GetVersion():
    """Get version string"""
    return b"2.1.0"

# Export functions for ctypes
__all__ = ['ConvertDocument', 'TestConnection', 'GetVersion']
