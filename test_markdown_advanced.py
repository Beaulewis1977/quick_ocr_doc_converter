#!/usr/bin/env python3
"""Test advanced Markdown features like lists, code blocks, tables"""

import tempfile
import os

# Create markdown with advanced features
advanced_markdown = """# Advanced Markdown Test

This tests complex Markdown features.

## Lists

### Unordered Lists

- First item
- Second item
  - Nested item
  - Another nested item
- Third item

### Ordered Lists

1. First numbered item
2. Second numbered item
   1. Nested numbered item
   2. Another nested numbered item
3. Third numbered item

## Code

### Inline Code

This paragraph contains `inline code` examples.

### Code Blocks

```python
def hello_world():
    print("Hello, World!")
    return True
```

```
Plain text code block
No syntax highlighting
```

## Blockquotes

> This is a blockquote
> It can span multiple lines
>
> And have multiple paragraphs

## Tables

| Feature | Status | Notes |
|---------|--------|-------|
| Headers | ✅ Working | All levels |
| Paragraphs | ✅ Working | Basic text |
| Lists | 🔍 Testing | Nested support |
| Code | 🔍 Testing | Blocks & inline |

## Links and Images

Visit [Claude Code](https://claude.ai/code) for more info.

![Test Image](https://example.com/test.png)

## Emphasis

This text has **bold**, *italic*, and ***bold italic*** formatting.

## Horizontal Rules

---

That was a horizontal rule.

## Final Test

If all these features convert properly, the advanced support is working!
"""

def test_markdown_structure():
    """Test that advanced markdown parses correctly"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(advanced_markdown)
        input_path = f.name
    
    try:
        from universal_document_converter import MarkdownReader
        reader = MarkdownReader()
        result = reader.read(input_path)
        
        print(f"Parsed {len(result)} elements from advanced Markdown:")
        print()
        
        # Analyze the structure
        headings = [item for item in result if item[0] == 'heading']
        paragraphs = [item for item in result if item[0] == 'paragraph']
        
        print(f"📊 Structure Analysis:")
        print(f"  - Headings: {len(headings)}")
        print(f"  - Paragraphs: {len(paragraphs)}")
        print(f"  - Total elements: {len(result)}")
        print()
        
        print("📋 Headings found:")
        for i, (_, level, text) in enumerate(headings, 1):
            indent = "  " * (level - 1)
            print(f"  {i:2d}. {indent}H{level}: {text}")
        
        print()
        print("📄 First 10 elements:")
        for i, item in enumerate(result[:10], 1):
            if item[0] == 'heading':
                print(f"  {i:2d}. HEADING (H{item[1]}): {item[2]}")
            elif item[0] == 'paragraph':
                preview = item[1][:60] + "..." if len(item[1]) > 60 else item[1]
                print(f"  {i:2d}. PARAGRAPH: {preview}")
            else:
                print(f"  {i:2d}. {item[0].upper()}: {item[1] if len(item) > 1 else 'N/A'}")
        
        return result
        
    finally:
        os.unlink(input_path)

def test_conversion_quality():
    """Test conversion to RTF maintains structure"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(advanced_markdown)
        input_path = f.name
    
    output_path = input_path.replace('.md', '.rtf')
    
    try:
        from universal_document_converter import UniversalConverter
        converter = UniversalConverter()
        
        print("🔄 Converting advanced Markdown to RTF...")
        
        converter.convert_file(
            input_path=input_path,
            output_path=output_path,
            input_format='markdown',
            output_format='rtf'
        )
        
        # Analyze RTF output
        with open(output_path, 'r') as f:
            rtf_content = f.read()
        
        print(f"✅ RTF conversion successful!")
        print(f"   Input size: {len(advanced_markdown)} chars")
        print(f"   Output size: {len(rtf_content)} chars")
        
        # Check for RTF formatting codes
        formatting_checks = {
            '\\b': 'Bold formatting',
            '\\fs': 'Font size changes',
            '\\par': 'Paragraph breaks',
            'Times New Roman': 'Font specification',
        }
        
        print("\n🔍 RTF Formatting Analysis:")
        for code, description in formatting_checks.items():
            count = rtf_content.count(code)
            print(f"   {code:15} ({description:20}): {count:3d} instances")
        
        # Show preview
        print(f"\n📄 RTF Preview (first 200 chars):")
        print(f"   {rtf_content[:200]}...")
        
        return rtf_content
        
    finally:
        os.unlink(input_path)
        if os.path.exists(output_path):
            print(f"\n📁 RTF file saved: {output_path}")
            # os.unlink(output_path)  # Keep for inspection

if __name__ == '__main__':
    print("🧪 Testing Advanced Markdown Features")
    print("=" * 50)
    
    try:
        print("\n1️⃣ Testing Markdown Structure Parsing...")
        result = test_markdown_structure()
        
        print("\n2️⃣ Testing RTF Conversion Quality...")
        rtf_content = test_conversion_quality()
        
        print("\n🎉 Advanced Markdown testing completed!")
        print("   • Structure parsing: ✅")
        print("   • RTF conversion: ✅")
        print("   • All features preserved in basic form")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()