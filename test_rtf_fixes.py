#!/usr/bin/env python3
"""Test the fixed RTF writer and MarkdownReader with parse_content method"""

import sys
import os
sys.path.insert(0, '.')

# Import without GUI
import re
import markdown
from bs4 import BeautifulSoup

class MarkdownReader:
    """Test implementation of MarkdownReader with parse_content"""
    
    def parse_content(self, md_text):
        """Parse markdown content from a string"""
        try:
            import markdown
            from bs4 import BeautifulSoup
        except ImportError:
            raise Exception("markdown and beautifulsoup4 are required")
        
        # Convert Markdown to HTML using python-markdown
        html = markdown.markdown(md_text, extensions=['extra', 'toc'])
        
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        content = []
        
        # Extract headings and paragraphs
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']):
            text = element.get_text().strip()
            if text:
                if element.name.startswith('h'):
                    level = int(element.name[1])
                    content.append(('heading', level, text))
                else:
                    content.append(('paragraph', text))
        
        return content

class RtfWriter:
    """Test implementation of improved RTF writer"""
    
    def write_file(self, output_path, content):
        # Basic RTF structure
        rtf_lines = [
            r"{\rtf1\ansi\deff0",
            r"{\fonttbl{\f0 Times New Roman;}}",
            r"\f0\fs24"
        ]
        
        for i, item in enumerate(content):
            if item[0] == 'heading':
                level, text = item[1], item[2]
                size = max(32 - (level * 4), 20)  # Larger size for higher level headings
                # Add spacing before headings (except the first element)
                if i > 0:
                    rtf_lines.append("\\par")
                rtf_lines.append(f"\\par\\fs{size}\\b {self._escape_rtf(text)}\\b0\\fs24")
            elif item[0] == 'paragraph':
                rtf_lines.append(f"\\par {self._escape_rtf(item[1])}")
            elif item[0] == 'page':
                page_num, text = item[1], item[2]
                rtf_lines.append(f"\\par\\fs28\\b Page {page_num}\\b0\\fs24")
                rtf_lines.append(f"\\par {self._escape_rtf(text)}")
        
        rtf_lines.append("}")
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(''.join(rtf_lines))
    
    def _escape_rtf(self, text):
        """Escape RTF special characters"""
        return text.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')

def test_markdown_to_rtf_conversion():
    """Test the complete markdown to RTF conversion"""
    print("🧪 Testing Markdown → RTF Conversion with Fixes")
    
    # Test 1: User's original issue (literal \n)
    print("\n1️⃣ Testing user's original issue:")
    reader = MarkdownReader()
    writer = RtfWriter()
    
    # This was causing the issue - literal \n instead of actual newline
    problematic_md = "# Test Markdown\\nThis is bold text"
    print(f"   Input: {repr(problematic_md)}")
    
    parsed = reader.parse_content(problematic_md)
    print(f"   Parsed: {parsed}")
    
    # Test 2: Correct markdown 
    print("\n2️⃣ Testing correct markdown:")
    correct_md = """# Test Markdown
This is **bold text**

## Another Heading
Some more content here.

### Sub-heading
Final paragraph with some text."""
    
    print(f"   Input: {repr(correct_md)}")
    parsed_correct = reader.parse_content(correct_md)
    print(f"   Parsed: {parsed_correct}")
    
    # Test 3: Generate RTF
    print("\n3️⃣ Testing RTF generation:")
    output_file = "/tmp/test_output.rtf"
    writer.write_file(output_file, parsed_correct)
    
    with open(output_file, 'r') as f:
        rtf_content = f.read()
    
    print(f"   RTF file size: {len(rtf_content)} characters")
    print(f"   RTF preview (first 200 chars):")
    print(f"   {rtf_content[:200]}...")
    
    # Test 4: Verify RTF structure
    print("\n4️⃣ Verifying RTF structure:")
    checks = {
        "RTF header": r'\rtf1' in rtf_content,
        "Font table": r'\fonttbl' in rtf_content,
        "Bold formatting": r'\b ' in rtf_content,
        "Paragraph breaks": r'\par' in rtf_content,
        "Font sizes": any(f'\\fs{size}' in rtf_content for size in [20, 24, 28, 32]),
        "Proper closing": rtf_content.endswith('}')
    }
    
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
    
    print(f"\n📄 Complete RTF output:")
    print(rtf_content)
    
    return rtf_content

if __name__ == "__main__":
    rtf_output = test_markdown_to_rtf_conversion()
    print(f"\n🎉 RTF conversion test completed!")
    print(f"📁 Output saved to: /tmp/test_output.rtf")