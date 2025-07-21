#!/usr/bin/env python3
"""Simple test to verify MarkdownReader implementation"""

import tempfile

# Create a simple test markdown file
test_content = """# Main Title

This is a paragraph.

## Subtitle

Another paragraph.
"""

# Create temp file
with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
    f.write(test_content)
    temp_path = f.name

try:
    # Try to import and use the MarkdownReader
    from universal_document_converter import MarkdownReader, FormatDetector
    
    # Test format detection
    detected = FormatDetector.detect_format(temp_path)
    print(f"Format detection: {detected}")
    
    # Test reader
    reader = MarkdownReader()
    result = reader.read(temp_path)
    
    print(f"MarkdownReader result:")
    for item in result:
        print(f"  {item}")
        
    print("\nSuccess! MarkdownReader is working.")
    
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Clean up
    import os
    os.unlink(temp_path)