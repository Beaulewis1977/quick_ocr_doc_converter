#!/usr/bin/env python3
"""Test Markdown to RTF conversion"""

import tempfile
import os

# Create test markdown content
test_markdown = """# Document Converter Test

This is a sample document to test **Markdown to RTF** conversion.

## Features Tested

1. Main headings (H1)
2. Sub headings (H2)
3. Regular paragraphs
4. Basic formatting

### Sub-section

This paragraph tests the conversion pipeline:
- Markdown parsing
- Internal format conversion  
- RTF output generation

## Conclusion

If you can read this in RTF format, the conversion worked!
"""

# Create temporary markdown file
with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
    f.write(test_markdown)
    input_path = f.name

output_path = input_path.replace('.md', '.rtf')

try:
    # Import the converter
    from universal_document_converter import UniversalConverter
    
    # Test the conversion
    converter = UniversalConverter()
    
    print(f"Converting {input_path} to {output_path}")
    
    converter.convert_file(
        input_path=input_path,
        output_path=output_path, 
        input_format='markdown',
        output_format='rtf'
    )
    
    # If we get here, conversion was successful (no exception was raised)
    print("✅ Conversion successful!")
    
    # Check if RTF file was created and has content
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            rtf_content = f.read()
        print(f"RTF file size: {len(rtf_content)} characters")
        
        # Show first few lines of RTF content
        lines = rtf_content.split('\n')[:10]
        print("\nFirst 10 lines of RTF content:")
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line[:80]}{'...' if len(line) > 80 else ''}")
    else:
        print("❌ Output file was not created")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Cleanup
    if os.path.exists(input_path):
        os.unlink(input_path)
    if os.path.exists(output_path):
        print(f"\nRTF file kept at: {output_path}")
        # os.unlink(output_path)  # Keep the RTF file to inspect