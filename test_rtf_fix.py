#!/usr/bin/env python3
"""Simple test to identify and fix RTF formatting issues"""

import re
import markdown
from bs4 import BeautifulSoup

# Simulate the MarkdownReader parsing
def parse_markdown_content(md_text):
    """Parse markdown content the same way MarkdownReader does"""
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

# Test markdown that shows the issue
test_md = """# Test Markdown
This is **bold text**"""

print("Original markdown:")
print(repr(test_md))
print("\nMarkdown content:")
print(test_md)

# Parse it
parsed = parse_markdown_content(test_md)
print(f"\nParsed content: {parsed}")

# Check what HTML was generated
html = markdown.markdown(test_md, extensions=['extra', 'toc'])
print(f"\nGenerated HTML: {html}")

# Parse HTML with BeautifulSoup to see elements
soup = BeautifulSoup(html, 'html.parser')
print(f"\nHTML elements found:")
for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']):
    print(f"  {element.name}: '{element.get_text().strip()}'")