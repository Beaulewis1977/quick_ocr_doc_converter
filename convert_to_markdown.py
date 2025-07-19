#!/usr/bin/env python3
"""
Document to Markdown Converter
Converts DOCX, PDF, and TXT files to Markdown format
"""

import os
import sys
from pathlib import Path
import argparse

def install_requirements():
    """Install required packages"""
    required_packages = [
        'python-docx',
        'PyPDF2',
        'markdownify'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} already installed")
        except ImportError:
            print(f"Installing {package}...")
            os.system(f'pip install {package}')

def convert_docx_to_markdown(file_path):
    """Convert DOCX file to Markdown"""
    try:
        from docx import Document
        
        doc = Document(file_path)
        markdown_content = []
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                # Basic formatting detection
                if paragraph.style.name.startswith('Heading'):
                    level = paragraph.style.name.split()[-1]
                    if level.isdigit():
                        markdown_content.append(f"{'#' * int(level)} {text}")
                    else:
                        markdown_content.append(f"## {text}")
                else:
                    markdown_content.append(text)
                markdown_content.append("")  # Add blank line
        
        return "\n".join(markdown_content)
    
    except Exception as e:
        print(f"Error converting DOCX file {file_path}: {e}")
        return None

def convert_pdf_to_markdown(file_path):
    """Convert PDF file to Markdown"""
    try:
        import PyPDF2
        
        markdown_content = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():
                    if page_num == 0:
                        # Assume first page has title
                        lines = text.strip().split('\n')
                        if lines:
                            markdown_content.append(f"# {lines[0]}")
                            markdown_content.append("")
                            markdown_content.extend(lines[1:])
                    else:
                        markdown_content.append(text)
                    markdown_content.append("")  # Add blank line between pages
        
        return "\n".join(markdown_content)
    
    except Exception as e:
        print(f"Error converting PDF file {file_path}: {e}")
        return None

def convert_txt_to_markdown(file_path):
    """Convert TXT file to Markdown"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Basic markdown formatting for text files
        lines = content.split('\n')
        markdown_content = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line:
                # If it's the first non-empty line, make it a title
                if i == 0 or (not markdown_content and line):
                    markdown_content.append(f"# {line}")
                else:
                    markdown_content.append(line)
            markdown_content.append("")
        
        return "\n".join(markdown_content)
    
    except Exception as e:
        print(f"Error converting TXT file {file_path}: {e}")
        return None

def convert_file(file_path, output_dir):
    """Convert a single file to Markdown"""
    file_path = Path(file_path)
    output_dir = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine conversion method based on file extension
    extension = file_path.suffix.lower()
    
    print(f"Converting: {file_path.name}")
    
    if extension == '.docx':
        content = convert_docx_to_markdown(file_path)
    elif extension == '.pdf':
        content = convert_pdf_to_markdown(file_path)
    elif extension == '.txt':
        content = convert_txt_to_markdown(file_path)
    else:
        print(f"Unsupported file type: {extension}")
        return False
    
    if content:
        # Create output filename
        output_filename = file_path.stem + '.md'
        output_path = output_dir / output_filename
        
        # Write markdown content
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content)
        
        print(f"✓ Converted to: {output_path}")
        return True
    else:
        print(f"✗ Failed to convert: {file_path}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert documents to Markdown')
    parser.add_argument('input_dir', nargs='?', default='.', 
                       help='Input directory (default: current directory)')
    parser.add_argument('-o', '--output', default='markdown_output', 
                       help='Output directory (default: markdown_output)')
    parser.add_argument('--install', action='store_true', 
                       help='Install required packages')
    
    args = parser.parse_args()
    
    if args.install:
        install_requirements()
        return
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    # Find all supported files
    supported_extensions = ['.docx', '.pdf', '.txt']
    files_to_convert = []
    
    for ext in supported_extensions:
        files_to_convert.extend(input_dir.glob(f'*{ext}'))
    
    if not files_to_convert:
        print(f"No supported files found in '{input_dir}'")
        print(f"Supported formats: {', '.join(supported_extensions)}")
        return
    
    print(f"Found {len(files_to_convert)} files to convert:")
    for file in files_to_convert:
        print(f"  - {file.name}")
    
    print(f"\nOutput directory: {output_dir}")
    print("=" * 50)
    
    # Convert files
    successful = 0
    failed = 0
    
    for file_path in files_to_convert:
        if convert_file(file_path, output_dir):
            successful += 1
        else:
            failed += 1
    
    print("=" * 50)
    print(f"Conversion complete!")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    
    if successful > 0:
        print(f"\nMarkdown files saved to: {output_dir}")

if __name__ == '__main__':
    main() 
