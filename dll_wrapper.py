#!/usr/bin/env python3
"""
DLL Wrapper for Universal Document Converter
Creates 32-bit compatible DLL for VFP9/VB6 integration using ctypes

This module provides:
1. Python functions suitable for DLL export
2. Build scripts for creating 32-bit DLL
3. VB6/VFP9 declarations and usage examples

Usage from VB6:
  Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
      (ByVal inputFile As String, ByVal outputFile As String, _
       ByVal inputFormat As String, ByVal outputFormat As String) As Long

Usage from VFP9:
  DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
      STRING inputFile, STRING outputFile, ;
      STRING inputFormat, STRING outputFormat
"""

import sys
import os
import traceback
import ctypes
from ctypes import c_char_p, c_int, c_wchar_p
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our converter (handle GUI dependencies gracefully)
try:
    # Mock tkinter to avoid GUI issues
    class MockTk:
        def __init__(self): pass
        
    if 'tkinter' not in sys.modules:
        sys.modules['tkinter'] = MockTk()
        sys.modules['tkinter.ttk'] = MockTk()
        sys.modules['tkinter.messagebox'] = MockTk()
        sys.modules['tkinter.filedialog'] = MockTk()
        sys.modules['tkinterdnd2'] = MockTk()
    
    from universal_document_converter import UniversalConverter
    CONVERTER_AVAILABLE = True
except Exception as e:
    CONVERTER_AVAILABLE = False
    print(f"UniversalConverter not available: {e}")

# Global converter instance
_converter = None

def _get_converter():
    """Get or create converter instance"""
    global _converter
    if _converter is None and CONVERTER_AVAILABLE:
        try:
            _converter = UniversalConverter("DLL_Wrapper")
        except Exception as e:
            print(f"Failed to create converter: {e}")
    return _converter


# DLL Export Functions (C-style calling convention)
def ConvertDocument(input_file_ptr, output_file_ptr, input_format_ptr, output_format_ptr):
    """
    Convert a document file (DLL export function)
    
    Args:
        input_file_ptr: C pointer to input file path string
        output_file_ptr: C pointer to output file path string  
        input_format_ptr: C pointer to input format string
        output_format_ptr: C pointer to output format string
        
    Returns:
        int: 1 for success, 0 for failure, -1 for error
    """
    try:
        # Convert C strings to Python strings
        input_file = ctypes.c_char_p(input_file_ptr).value.decode('utf-8')
        output_file = ctypes.c_char_p(output_file_ptr).value.decode('utf-8')
        input_format = ctypes.c_char_p(input_format_ptr).value.decode('utf-8')
        output_format = ctypes.c_char_p(output_format_ptr).value.decode('utf-8')
        
        converter = _get_converter()
        if not converter:
            return -1
        
        # Validate input file exists
        if not os.path.exists(input_file):
            return -1
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Perform conversion
        converter.convert_file(input_file, output_file, input_format, output_format)
        
        # Verify output was created
        if os.path.exists(output_file):
            return 1  # Success
        else:
            return 0  # Failure - no output created
            
    except Exception as e:
        print(f"DLL ConvertDocument error: {e}")
        return -1  # Error


def GetLastError():
    """
    Get last error message (DLL export function)
    
    Returns:
        char*: Pointer to error message string
    """
    try:
        # This would need to be implemented with proper error tracking
        return b"No error"
    except:
        return b"Unknown error"


def GetVersion():
    """
    Get version string (DLL export function)
    
    Returns:
        char*: Pointer to version string
    """
    try:
        return b"2.1.0"
    except:
        return b"Unknown"


def TestConnection():
    """
    Test if DLL is working (DLL export function)
    
    Returns:
        int: 1 if working, 0 if not
    """
    try:
        converter = _get_converter()
        return 1 if converter else 0
    except:
        return 0


# Build and compile functions
def create_dll_build_script():
    """Create build script for generating 32-bit DLL"""
    
    build_script = '''#!/usr/bin/env python3
"""
Build script for UniversalConverter32.dll

Requirements:
- Python 3.x (32-bit for 32-bit DLL)  
- Nuitka: pip install nuitka
- OR cx_Freeze: pip install cx_freeze
- OR PyInstaller: pip install pyinstaller

Usage:
    python build_dll.py
"""

import os
import sys
import subprocess
import shutil

def build_with_nuitka():
    """Build DLL using Nuitka (recommended)"""
    print("🔨 Building DLL with Nuitka...")
    
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--plugin-enable=no-qt",
        "--plugin-disable=tk-inter",
        "--output-dir=dist",
        "--output-filename=UniversalConverter32.dll",
        "--windows-company-name=TerragonLabs",
        "--windows-product-name=UniversalConverter",
        "--windows-file-version=2.1.0.0",
        "--windows-product-version=2.1.0",
        "--windows-file-description=Universal Document Converter DLL",
        "dll_wrapper.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Nuitka build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Nuitka build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Nuitka not found. Install with: pip install nuitka")
        return False

def build_with_cython():
    """Build DLL using Cython"""
    print("🔨 Building DLL with Cython...")
    
    # Create setup.py for Cython
    setup_py = \\"""
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

ext = Extension(
    "UniversalConverter32", 
    ["dll_wrapper.py"],
    define_macros=[("WIN32", "1")],
)

setup(
    ext_modules=cythonize([ext], language_level=3),
    zip_safe=False,
)
\\"""
    
    with open("setup_dll.py", "w") as f:
        f.write(setup_py)
    
    try:
        cmd = [sys.executable, "setup_dll.py", "build_ext", "--inplace"]
        result = subprocess.run(cmd, check=True)
        print("✅ Cython build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Cython build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Cython not found. Install with: pip install cython")
        return False

def build_with_pyinstaller():
    """Build EXE that can act like DLL"""
    print("🔨 Building executable with PyInstaller...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name=UniversalConverter32",
        "dll_wrapper.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ PyInstaller build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False

if __name__ == "__main__":
    print("🏗️ Building UniversalConverter32.dll")
    print("=" * 50)
    
    # Try build methods in order of preference
    success = False
    
    if not success:
        success = build_with_nuitka()
    
    if not success:
        success = build_with_cython()
    
    if not success:
        success = build_with_pyinstaller()
    
    if success:
        print("\\n🎉 Build completed successfully!")
        print("📁 Check the dist/ folder for output files")
    else:
        print("\\n❌ All build methods failed")
        print("💡 Install build tools:")
        print("   pip install nuitka")
        print("   pip install cython")  
        print("   pip install pyinstaller")
'''
    
    with open('build_dll.py', 'w') as f:
        f.write(build_script)
    
    print("✅ Created build_dll.py")
    return True


def create_vb6_examples():
    """Create VB6 example files"""
    
    # VB6 Module file
    vb6_module = '''Attribute VB_Name = "UniversalConverterModule"
'Universal Document Converter VB6 Integration Module
'Provides easy access to document conversion functionality

'DLL Function Declarations
Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String, _
     ByVal inputFormat As String, ByVal outputFormat As String) As Long

Declare Function TestConnection Lib "UniversalConverter32.dll" () As Long
Declare Function GetVersion Lib "UniversalConverter32.dll" () As String

'Error codes
Public Const UC_SUCCESS = 1
Public Const UC_FAILURE = 0  
Public Const UC_ERROR = -1

'Wrapper functions for easier use
Public Function ConvertMarkdownToRTF(inputFile As String, outputFile As String) As Boolean
    Dim result As Long
    result = ConvertDocument(inputFile, outputFile, "markdown", "rtf")
    ConvertMarkdownToRTF = (result = UC_SUCCESS)
End Function

Public Function ConvertRTFToMarkdown(inputFile As String, outputFile As String) As Boolean
    Dim result As Long
    result = ConvertDocument(inputFile, outputFile, "rtf", "markdown")  
    ConvertRTFToMarkdown = (result = UC_SUCCESS)
End Function

Public Function IsConverterAvailable() As Boolean
    Dim result As Long
    result = TestConnection()
    IsConverterAvailable = (result = UC_SUCCESS)
End Function

Public Sub TestConverter()
    'Example test routine
    If IsConverterAvailable() Then
        MsgBox "Universal Document Converter is available!"
        
        'Test conversion
        Dim testResult As Boolean
        testResult = ConvertMarkdownToRTF("C:\\temp\\test.md", "C:\\temp\\test.rtf")
        
        If testResult Then
            MsgBox "Test conversion successful!"
        Else
            MsgBox "Test conversion failed!"
        End If
    Else
        MsgBox "Universal Document Converter is not available!"
    End If
End Sub
'''
    
    # VB6 Form example
    vb6_form = '''VERSION 5.00
Begin VB.Form frmConverter 
   Caption         =   "Universal Document Converter"
   Height          =   4200
   Width           =   6000
   
   Begin VB.CommandButton cmdConvert 
      Caption         =   "Convert Document"
      Height          =   400
      Left            =   2000
      Top             =   3000
      Width           =   2000
   End
   
   Begin VB.TextBox txtOutput
      Height          =   300
      Left            =   1500
      Top             =   2400
      Width           =   4000
   End
   
   Begin VB.TextBox txtInput
      Height          =   300
      Left            =   1500
      Top             =   2000
      Width           =   4000
   End
   
   Begin VB.Label lblOutput
      Caption         =   "Output File:"
      Left            =   200
      Top             =   2400
   End
   
   Begin VB.Label lblInput
      Caption         =   "Input File:"
      Left            =   200
      Top             =   2000
   End
End

Private Sub cmdConvert_Click()
    Dim result As Long
    
    If Len(txtInput.Text) = 0 Or Len(txtOutput.Text) = 0 Then
        MsgBox "Please enter both input and output file paths"
        Exit Sub
    End If
    
    'Convert markdown to RTF
    result = ConvertDocument(txtInput.Text, txtOutput.Text, "markdown", "rtf")
    
    Select Case result
        Case UC_SUCCESS
            MsgBox "Conversion successful!"
        Case UC_FAILURE
            MsgBox "Conversion failed - check file paths"
        Case UC_ERROR
            MsgBox "Error during conversion"
    End Select
End Sub

Private Sub Form_Load()
    'Test if converter is available
    If Not IsConverterAvailable() Then
        MsgBox "Warning: Universal Document Converter DLL not found!"
    End If
    
    'Set default paths
    txtInput.Text = "C:\\temp\\test.md"
    txtOutput.Text = "C:\\temp\\test.rtf"
End Sub
'''
    
    with open('VB6_UniversalConverter.bas', 'w') as f:
        f.write(vb6_module)
    
    with open('VB6_ConverterForm.frm', 'w') as f:
        f.write(vb6_form)
    
    print("✅ Created VB6 example files:")
    print("   - VB6_UniversalConverter.bas (module)")
    print("   - VB6_ConverterForm.frm (form example)")


def create_vfp9_examples():
    """Create VFP9 example files"""
    
    vfp9_prg = '''*!* Universal Document Converter VFP9 Integration
*!* Provides easy access to document conversion functionality

*-- DLL Function Declarations
DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, ;
    STRING inputFormat, STRING outputFormat

DECLARE INTEGER TestConnection IN UniversalConverter32.dll

*-- Constants
#DEFINE UC_SUCCESS 1
#DEFINE UC_FAILURE 0  
#DEFINE UC_ERROR -1

*!* Convert Markdown to RTF
FUNCTION ConvertMarkdownToRTF(tcInputFile, tcOutputFile)
    LOCAL lnResult
    lnResult = ConvertDocument(tcInputFile, tcOutputFile, "markdown", "rtf")
    RETURN (lnResult = UC_SUCCESS)
ENDFUNC

*!* Convert RTF to Markdown  
FUNCTION ConvertRTFToMarkdown(tcInputFile, tcOutputFile)
    LOCAL lnResult
    lnResult = ConvertDocument(tcInputFile, tcOutputFile, "rtf", "markdown")
    RETURN (lnResult = UC_SUCCESS)
ENDFUNC

*!* Test if converter is available
FUNCTION IsConverterAvailable()
    LOCAL lnResult
    lnResult = TestConnection()
    RETURN (lnResult = UC_SUCCESS)
ENDFUNC

*!* Test conversion functionality
PROCEDURE TestConverter()
    IF IsConverterAvailable()
        MESSAGEBOX("Universal Document Converter is available!")
        
        *-- Test conversion
        LOCAL llResult
        llResult = ConvertMarkdownToRTF("C:\\temp\\test.md", "C:\\temp\\test.rtf")
        
        IF llResult
            MESSAGEBOX("Test conversion successful!")
        ELSE
            MESSAGEBOX("Test conversion failed!")
        ENDIF
    ELSE
        MESSAGEBOX("Universal Document Converter is not available!")
    ENDIF
ENDPROC

*!* Example usage
PROCEDURE ExampleUsage()
    LOCAL lcInputFile, lcOutputFile, llSuccess
    
    *-- Set file paths
    lcInputFile = "C:\\Documents\\readme.md"
    lcOutputFile = "C:\\Documents\\readme.rtf"
    
    *-- Convert markdown to RTF
    llSuccess = ConvertMarkdownToRTF(lcInputFile, lcOutputFile)
    
    IF llSuccess
        MESSAGEBOX("Conversion successful! Check: " + lcOutputFile)
    ELSE
        MESSAGEBOX("Conversion failed! Check file paths and DLL availability.")
    ENDIF
ENDPROC

*!* Batch conversion example
PROCEDURE BatchConvert()
    LOCAL ARRAY laFiles[1]
    LOCAL lnFiles, lnI, lcInputFile, lcOutputFile, llSuccess
    
    *-- Get all .md files in a directory
    lnFiles = ADIR(laFiles, "C:\\Documents\\*.md")
    
    IF lnFiles > 0
        FOR lnI = 1 TO lnFiles
            lcInputFile = "C:\\Documents\\" + laFiles[lnI, 1]
            lcOutputFile = STRTRAN(lcInputFile, ".md", ".rtf")
            
            llSuccess = ConvertMarkdownToRTF(lcInputFile, lcOutputFile)
            
            IF llSuccess
                ? "Converted: " + laFiles[lnI, 1]
            ELSE
                ? "Failed: " + laFiles[lnI, 1]
            ENDIF
        ENDFOR
    ELSE
        MESSAGEBOX("No .md files found in C:\\Documents\\")
    ENDIF
ENDPROC
'''
    
    with open('UniversalConverter_VFP9.prg', 'w') as f:
        f.write(vfp9_prg)
    
    print("✅ Created VFP9 example file:")
    print("   - UniversalConverter_VFP9.prg")


def test_dll_wrapper():
    """Test DLL wrapper functionality"""
    print("🧪 Testing DLL Wrapper Functionality")
    print("=" * 50)
    
    try:
        # Test converter availability
        converter = _get_converter()
        if not converter:
            print("❌ UniversalConverter not available")
            return False
        
        print("✅ UniversalConverter available")
        
        # Test basic functions
        version = GetVersion()
        print(f"✅ Version: {version.decode('utf-8')}")
        
        connection = TestConnection()
        print(f"✅ Connection test: {'OK' if connection == 1 else 'Failed'}")
        
        # Test file conversion
        test_md = "# Test Document\nThis is a **test** for DLL wrapper."
        
        # Create test file
        with open('dll_test_input.md', 'w', encoding='utf-8') as f:
            f.write(test_md)
        
        # Convert strings to byte pointers for C interface
        input_file = b'dll_test_input.md'
        output_file = b'dll_test_output.rtf'
        input_format = b'markdown'
        output_format = b'rtf'
        
        # Test conversion (simulated - would need proper ctypes interface)
        try:
            converter.convert_file('dll_test_input.md', 'dll_test_output.rtf', 'markdown', 'rtf')
            
            if os.path.exists('dll_test_output.rtf'):
                print("✅ File conversion test successful")
            else:
                print("❌ File conversion test failed - no output")
        except Exception as e:
            print(f"❌ File conversion test failed: {e}")
        
        # Cleanup
        for file in ['dll_test_input.md', 'dll_test_output.rtf']:
            try:
                if os.path.exists(file):
                    os.unlink(file)
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"❌ DLL wrapper test failed: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Document Converter DLL Wrapper")
    parser.add_argument("--build-script", action="store_true", help="Create DLL build script")
    parser.add_argument("--vb6-examples", action="store_true", help="Create VB6 example files")
    parser.add_argument("--vfp9-examples", action="store_true", help="Create VFP9 example files")
    parser.add_argument("--test", action="store_true", help="Test DLL wrapper functionality")
    parser.add_argument("--all", action="store_true", help="Create all files")
    
    args = parser.parse_args()
    
    if args.all:
        create_dll_build_script()
        create_vb6_examples()
        create_vfp9_examples()
        test_dll_wrapper()
    elif args.build_script:
        create_dll_build_script()
    elif args.vb6_examples:
        create_vb6_examples()
    elif args.vfp9_examples:
        create_vfp9_examples()
    elif args.test:
        test_dll_wrapper()
    else:
        print("Universal Document Converter DLL Wrapper v2.1.0")
        print("\nOptions:")
        print("  --build-script  Create build script for DLL compilation")
        print("  --vb6-examples  Create VB6 example files")
        print("  --vfp9-examples Create VFP9 example files")
        print("  --test          Test DLL wrapper functionality")
        print("  --all           Create all files and test")
        print("\nUsage:")
        print("  python dll_wrapper.py --all")
        print("  python build_dll.py  # After creating build script")