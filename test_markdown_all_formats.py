#!/usr/bin/env python3
"""Test Markdown to all supported output formats"""

import tempfile
import os

# Create comprehensive test markdown content
test_markdown = """# Universal Document Converter Test

This document tests **Markdown to all formats** conversion.

## Features

The converter supports:

1. **Headings** (H1 through H6)
2. **Paragraphs** with regular text
3. **Bold** and *italic* formatting
4. Lists and bullet points

### Technical Details

This tests the conversion pipeline:
- Markdown → Internal format
- Internal format → Target format

#### Performance

The system handles multiple formats efficiently.

##### Compatibility

Works with legacy systems including:
- 32-bit environments
- VFP9 and VB6

###### Conclusion

If this converts properly, the system is working!

## Final Notes

This is the last paragraph to test complete document conversion.
"""

formats = [
    ('rtf', 'Rich Text Format'),
    ('html', 'HTML Document'), 
    ('txt', 'Plain Text'),
    ('epub', 'EPUB eBook'),
    ('markdown', 'Markdown (round-trip test)')
]

# Create temporary markdown file
with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
    f.write(test_markdown)
    input_path = f.name

try:
    from universal_document_converter import UniversalConverter
    converter = UniversalConverter()
    
    print(f"Testing conversion from: {input_path}")
    print(f"Input file size: {len(test_markdown)} characters\n")
    
    results = {}
    
    for output_format, format_name in formats:
        output_path = input_path.replace('.md', f'.{output_format}')
        
        try:
            print(f"Converting to {format_name} ({output_format})...")
            
            converter.convert_file(
                input_path=input_path,
                output_path=output_path, 
                input_format='markdown',
                output_format=output_format
            )
            
            # Check output file
            if os.path.exists(output_path):
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                results[output_format] = {
                    'success': True,
                    'size': len(content),
                    'path': output_path,
                    'preview': content[:200].replace('\n', ' ')
                }
                print(f"  ✅ Success! Size: {len(content)} chars")
                
            else:
                results[output_format] = {'success': False, 'error': 'File not created'}
                print(f"  ❌ Failed: Output file not created")
                
        except Exception as e:
            results[output_format] = {'success': False, 'error': str(e)}
            print(f"  ❌ Failed: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print("CONVERSION SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for r in results.values() if r['success'])
    total = len(results)
    
    print(f"Successful conversions: {successful}/{total}")
    print()
    
    for output_format, format_name in formats:
        result = results.get(output_format, {'success': False})
        if result['success']:
            print(f"✅ {format_name:20} | {result['size']:6} chars | {result['path']}")
            print(f"   Preview: {result['preview'][:80]}...")
        else:
            print(f"❌ {format_name:20} | Error: {result.get('error', 'Unknown')}")
        print()
    
    if successful == total:
        print("🎉 ALL CONVERSIONS SUCCESSFUL!")
        print("Markdown → Other formats feature is fully working!")
    else:
        print(f"⚠️  {total - successful} conversion(s) failed")
        
except Exception as e:
    print(f"❌ Test Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Cleanup input file
    if os.path.exists(input_path):
        os.unlink(input_path)
        
    print(f"\nOutput files kept for inspection in: {os.path.dirname(input_path)}")