#!/usr/bin/env python3
"""Reproduce the exact issue mentioned by the user"""

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

# Let me try to reproduce their exact issue by creating test.md
test_md_content = """# Test Markdown\\nThis is bold text"""

print("User's exact example:")
print(f"Input: {repr(test_md_content)}")

parsed = parse_markdown_content(test_md_content)
print(f"Parsed result: {parsed}")

# Let's also try with what they might have written in test.md
# Create a test.md file
with open('test.md', 'w') as f:
    f.write("# Test Markdown\nThis is **bold text**")

print("\nTesting with actual file:")
with open('test.md', 'r') as f:
    file_content = f.read()

print(f"File content: {repr(file_content)}")
parsed_file = parse_markdown_content(file_content)
print(f"Parsed file result: {parsed_file}")

# Check if there are any issues with the HTML output
html = markdown.markdown(file_content, extensions=['extra', 'toc'])
print(f"\nHTML output: {html}")