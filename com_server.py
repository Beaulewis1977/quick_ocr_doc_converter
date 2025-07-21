#!/usr/bin/env python3
"""
COM Server for Universal Document Converter
Provides COM interface for VFP9/VB6 integration

Usage from VFP9:
  SET PROCEDURE TO com_server.py
  oConverter = CREATEOBJECT("UniversalConverter.Application")
  oConverter.ConvertFile("input.md", "output.rtf", "markdown", "rtf")

Usage from VB6:
  Set objConverter = CreateObject("UniversalConverter.Application")
  objConverter.ConvertFile "input.md", "output.rtf", "markdown", "rtf"
"""

import sys
import os
import traceback
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import win32com for Windows COM functionality
    import win32com.server.util
    import win32com.server.policy
    from win32com.server.exception import COMException
    import pythoncom
    WIN32COM_AVAILABLE = True
except ImportError:
    WIN32COM_AVAILABLE = False
    print("win32com not available - COM server functionality disabled")

# Import our converter (handle GUI dependencies gracefully)
try:
    # Mock tkinter to avoid GUI issues
    class MockTk:
        def __init__(self): pass
        def withdraw(self): pass
        def deiconify(self): pass
        
    class MockTtk:
        def __init__(self): pass
        
    if 'tkinter' not in sys.modules:
        sys.modules['tkinter'] = MockTk()
        sys.modules['tkinter.ttk'] = MockTtk()
        sys.modules['tkinter.messagebox'] = MockTk()
        sys.modules['tkinter.filedialog'] = MockTk()
        sys.modules['tkinterdnd2'] = MockTk()
    
    from universal_document_converter import UniversalConverter
    CONVERTER_AVAILABLE = True
except Exception as e:
    CONVERTER_AVAILABLE = False
    print(f"UniversalConverter not available: {e}")


class UniversalConverterCOM:
    """COM Server class for Universal Document Converter"""
    
    _reg_clsid_ = "{12345678-1234-5678-9012-123456789ABC}"
    _reg_desc_ = "Universal Document Converter COM Server"
    _reg_progid_ = "UniversalConverter.Application"
    _reg_verprogid_ = "UniversalConverter.Application.1"
    
    def __init__(self):
        """Initialize COM server"""
        self.converter = None
        if CONVERTER_AVAILABLE:
            try:
                self.converter = UniversalConverter("COM_Server")
            except Exception as e:
                print(f"Failed to initialize UniversalConverter: {e}")
    
    def ConvertFile(self, input_path, output_path, input_format="auto", output_format="markdown"):
        """
        Convert a document file
        
        Args:
            input_path (str): Path to input file
            output_path (str): Path to output file  
            input_format (str): Input format (auto, docx, pdf, txt, html, rtf, epub, markdown)
            output_format (str): Output format (markdown, txt, html, rtf, epub)
            
        Returns:
            int: 1 for success, 0 for failure
        """
        try:
            if not CONVERTER_AVAILABLE or not self.converter:
                raise Exception("UniversalConverter not available")
            
            # Validate input file exists
            if not os.path.exists(input_path):
                raise Exception(f"Input file not found: {input_path}")
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Perform conversion
            self.converter.convert_file(input_path, output_path, input_format, output_format)
            
            # Verify output was created
            if not os.path.exists(output_path):
                raise Exception(f"Output file was not created: {output_path}")
            
            return 1  # Success
            
        except Exception as e:
            print(f"COM Server ConvertFile error: {e}")
            traceback.print_exc()
            return 0  # Failure
    
    def ConvertString(self, input_text, output_format="markdown"):
        """
        Convert text content directly (for in-memory operations)
        
        Args:
            input_text (str): Input text content
            output_format (str): Output format
            
        Returns:
            str: Converted content or empty string on error
        """
        try:
            if not CONVERTER_AVAILABLE or not self.converter:
                raise Exception("UniversalConverter not available")
            
            # Write to temp file and convert
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_input:
                temp_input.write(input_text)
                temp_input_path = temp_input.name
            
            temp_output_path = temp_input_path.replace('.md', f'.{output_format}')
            
            try:
                self.converter.convert_file(temp_input_path, temp_output_path, 'markdown', output_format)
                
                if os.path.exists(temp_output_path):
                    with open(temp_output_path, 'r', encoding='utf-8') as f:
                        result = f.read()
                    return result
                else:
                    return ""
                    
            finally:
                # Cleanup temp files
                for temp_file in [temp_input_path, temp_output_path]:
                    try:
                        if os.path.exists(temp_file):
                            os.unlink(temp_file)
                    except:
                        pass
            
        except Exception as e:
            print(f"COM Server ConvertString error: {e}")
            return ""
    
    def GetSupportedFormats(self):
        """
        Get list of supported input and output formats
        
        Returns:
            str: JSON string with supported formats
        """
        try:
            import json
            formats = {
                "input_formats": ["auto", "docx", "pdf", "txt", "html", "rtf", "epub", "markdown"],
                "output_formats": ["markdown", "txt", "html", "rtf", "epub"]
            }
            return json.dumps(formats)
        except Exception as e:
            print(f"COM Server GetSupportedFormats error: {e}")
            return "{}"
    
    def GetVersion(self):
        """Get version information"""
        return "2.1.0"
    
    def TestConnection(self):
        """Test if COM server is working"""
        return "UniversalConverter COM Server v2.1.0 - Ready"


def register_com_server():
    """Register the COM server"""
    if not WIN32COM_AVAILABLE:
        print("❌ win32com not available - Cannot register COM server")
        print("   Install with: pip install pywin32")
        return False
    
    try:
        import win32com.server.register
        win32com.server.register.UseCommandLine(UniversalConverterCOM)
        print("✅ COM Server registered successfully")
        print(f"   ProgID: {UniversalConverterCOM._reg_progid_}")
        print(f"   Class ID: {UniversalConverterCOM._reg_clsid_}")
        return True
    except Exception as e:
        print(f"❌ Failed to register COM server: {e}")
        return False


def unregister_com_server():
    """Unregister the COM server"""
    if not WIN32COM_AVAILABLE:
        print("❌ win32com not available")
        return False
    
    try:
        import win32com.server.register
        win32com.server.register.UnregisterServer(UniversalConverterCOM._reg_clsid_)
        print("✅ COM Server unregistered successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to unregister COM server: {e}")
        return False


def test_com_server():
    """Test COM server functionality"""
    print("🧪 Testing COM Server Functionality")
    print("=" * 50)
    
    if not WIN32COM_AVAILABLE:
        print("❌ win32com not available for testing")
        return False
    
    try:
        # Create COM server instance directly
        server = UniversalConverterCOM()
        
        # Test basic methods
        version = server.GetVersion()
        print(f"✅ Version: {version}")
        
        connection_test = server.TestConnection()
        print(f"✅ Connection: {connection_test}")
        
        formats = server.GetSupportedFormats()
        print(f"✅ Formats available: {len(formats)} characters")
        
        # Test file conversion if possible
        test_md = "# Test Document\nThis is a **test** for COM server."
        
        # Create test file
        with open('com_test_input.md', 'w', encoding='utf-8') as f:
            f.write(test_md)
        
        result = server.ConvertFile('com_test_input.md', 'com_test_output.rtf', 'markdown', 'rtf')
        
        if result == 1 and os.path.exists('com_test_output.rtf'):
            print("✅ File conversion test successful")
            
            # Test string conversion
            string_result = server.ConvertString(test_md, 'rtf')
            if string_result:
                print("✅ String conversion test successful")
            else:
                print("⚠️ String conversion test failed")
        else:
            print("❌ File conversion test failed")
        
        # Cleanup
        for file in ['com_test_input.md', 'com_test_output.rtf']:
            try:
                if os.path.exists(file):
                    os.unlink(file)
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"❌ COM server test failed: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Document Converter COM Server")
    parser.add_argument("--register", action="store_true", help="Register COM server")
    parser.add_argument("--unregister", action="store_true", help="Unregister COM server")  
    parser.add_argument("--test", action="store_true", help="Test COM server functionality")
    
    args = parser.parse_args()
    
    if args.register:
        register_com_server()
    elif args.unregister:
        unregister_com_server()
    elif args.test:
        test_com_server()
    else:
        print("Universal Document Converter COM Server v2.1.0")
        print("\nOptions:")
        print("  --register    Register COM server for VFP9/VB6 use")
        print("  --unregister  Unregister COM server")
        print("  --test        Test COM server functionality")
        print("\nVFP9 Usage:")
        print('  oConverter = CREATEOBJECT("UniversalConverter.Application")')
        print('  lnResult = oConverter.ConvertFile("input.md", "output.rtf", "markdown", "rtf")')
        print("\nVB6 Usage:")
        print('  Set objConverter = CreateObject("UniversalConverter.Application")')
        print('  result = objConverter.ConvertFile("input.md", "output.rtf", "markdown", "rtf")')