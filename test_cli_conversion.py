#!/usr/bin/env python3
"""Test CLI-style conversion of the sample.md file"""

from universal_document_converter import UniversalConverter

def main():
    print("🧪 Testing CLI-style Markdown → RTF Conversion")
    print("=" * 50)
    
    input_file = "sample.md"
    output_file = "sample.rtf"
    
    try:
        converter = UniversalConverter()
        
        print(f"Input:  {input_file}")
        print(f"Output: {output_file}")
        print()
        
        # Convert the file
        converter.convert_file(
            input_path=input_file,
            output_path=output_file,
            input_format='markdown',
            output_format='rtf'
        )
        
        print("✅ Conversion completed successfully!")
        
        # Show results
        with open(input_file, 'r') as f:
            md_content = f.read()
        
        with open(output_file, 'r') as f:
            rtf_content = f.read()
        
        print(f"\n📊 Results:")
        print(f"   Markdown: {len(md_content)} characters")
        print(f"   RTF:      {len(rtf_content)} characters")
        
        print(f"\n📄 RTF Preview:")
        # Show readable preview by extracting text between RTF codes
        import re
        text_parts = re.findall(r'([^\\{}]+)', rtf_content)
        readable_text = ' '.join(part.strip() for part in text_parts if part.strip() and not part.isdigit())[:200]
        print(f"   {readable_text}...")
        
        print(f"\n📁 Files:")
        print(f"   • {input_file} (Markdown input)")  
        print(f"   • {output_file} (RTF output)")
        
        print(f"\n🎉 Success! Markdown → RTF conversion is fully operational!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()