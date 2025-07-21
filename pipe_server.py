#!/usr/bin/env python3
"""
Named Pipes Server for Universal Document Converter
Provides pipe-based communication for VFP9/VB6 integration

This creates a named pipe server that VFP9/VB6 can communicate with
using Windows named pipes or stdin/stdout redirection.

VFP9 Usage:
    lcCommand = 'python pipe_server.py'
    lnHandle = CreateFile("\\\\.\\pipe\\UniversalConverter", ...)
    WriteFile(lnHandle, '{"input":"test.md","output":"test.rtf","format":"rtf"}')
    ReadFile(lnHandle, lcResponse, ...)

VB6 Usage:
    Similar using CreateFile/WriteFile/ReadFile APIs
"""

import sys
import os
import json
import time
import threading
import traceback
from pathlib import Path
import select
import queue

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Platform-specific pipe implementations
WINDOWS_PIPES_AVAILABLE = False
try:
    if sys.platform == "win32":
        import win32pipe
        import win32file  
        import win32api
        import pywintypes
        WINDOWS_PIPES_AVAILABLE = True
except ImportError:
    pass

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


class PipeServer:
    """Named Pipes Server for document conversion"""
    
    def __init__(self, pipe_name="UniversalConverter"):
        self.pipe_name = pipe_name
        self.converter = None
        self.running = False
        self.request_queue = queue.Queue()
        
        if CONVERTER_AVAILABLE:
            try:
                self.converter = UniversalConverter("Pipe_Server")
            except Exception as e:
                print(f"Failed to initialize converter: {e}")
    
    def start_windows_pipe_server(self):
        """Start Windows named pipe server"""
        if not WINDOWS_PIPES_AVAILABLE:
            print("❌ Windows pipes not available (install pywin32)")
            return False
        
        pipe_path = f"\\\\.\\pipe\\{self.pipe_name}"
        print(f"🚀 Starting Windows named pipe server: {pipe_path}")
        
        self.running = True
        
        while self.running:
            try:
                # Create named pipe
                pipe_handle = win32pipe.CreateNamedPipe(
                    pipe_path,
                    win32pipe.PIPE_ACCESS_DUPLEX,
                    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                    1, 65536, 65536, 0, None
                )
                
                print("📞 Waiting for client connection...")
                
                # Wait for client to connect
                win32pipe.ConnectNamedPipe(pipe_handle, None)
                print("✅ Client connected")
                
                # Handle client communication
                self._handle_windows_pipe_client(pipe_handle)
                
            except pywintypes.error as e:
                if e.winerror == 232:  # Pipe is being closed
                    break
                print(f"Windows pipe error: {e}")
            except Exception as e:
                print(f"Pipe server error: {e}")
                traceback.print_exc()
            finally:
                try:
                    win32file.CloseHandle(pipe_handle)
                except:
                    pass
            
            time.sleep(0.1)
        
        print("🛑 Windows pipe server stopped")
        return True
    
    def _handle_windows_pipe_client(self, pipe_handle):
        """Handle Windows pipe client communication"""
        try:
            # Read request from client
            result, data = win32file.ReadFile(pipe_handle, 4096)
            request_text = data.decode('utf-8')
            
            print(f"📨 Received request: {request_text[:100]}...")
            
            # Process request
            response = self._process_request(request_text)
            
            # Send response back to client
            response_data = json.dumps(response).encode('utf-8')
            win32file.WriteFile(pipe_handle, response_data)
            
            print(f"📤 Sent response: {response.get('status', 'unknown')}")
            
        except Exception as e:
            print(f"Client handling error: {e}")
            # Send error response
            try:
                error_response = {
                    "status": "error",
                    "message": str(e)
                }
                response_data = json.dumps(error_response).encode('utf-8')
                win32file.WriteFile(pipe_handle, response_data)
            except:
                pass
    
    def start_stdio_server(self):
        """Start stdin/stdout pipe server (cross-platform)"""
        print("🚀 Starting stdin/stdout pipe server")
        print("💡 Send JSON requests to stdin, responses will be written to stdout")
        
        self.running = True
        
        while self.running:
            try:
                # Read from stdin
                if sys.stdin.readable():
                    line = sys.stdin.readline().strip()
                    
                    if line:
                        if line.lower() in ['quit', 'exit', 'stop']:
                            break
                        
                        print(f"📨 Processing request...", file=sys.stderr)
                        
                        # Process request
                        response = self._process_request(line)
                        
                        # Write response to stdout
                        print(json.dumps(response), flush=True)
                        print(f"📤 Response sent", file=sys.stderr)
                
                time.sleep(0.01)  # Small delay to prevent CPU spinning
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                error_response = {
                    "status": "error", 
                    "message": str(e)
                }
                print(json.dumps(error_response), flush=True)
                print(f"❌ Error: {e}", file=sys.stderr)
        
        print("🛑 Stdio pipe server stopped", file=sys.stderr)
        return True
    
    def _process_request(self, request_text):
        """Process a conversion request"""
        try:
            # Parse JSON request
            request = json.loads(request_text)
            
            # Extract parameters
            input_file = request.get('input', '')
            output_file = request.get('output', '')
            input_format = request.get('input_format', 'auto')
            output_format = request.get('output_format', 'markdown')
            
            # Validate parameters
            if not input_file or not output_file:
                return {
                    "status": "error",
                    "message": "Missing input or output file path"
                }
            
            if not self.converter:
                return {
                    "status": "error",
                    "message": "Document converter not available"
                }
            
            # Check input file exists
            if not os.path.exists(input_file):
                return {
                    "status": "error", 
                    "message": f"Input file not found: {input_file}"
                }
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Perform conversion
            start_time = time.time()
            self.converter.convert_file(input_file, output_file, input_format, output_format)
            end_time = time.time()
            
            # Check if conversion was successful
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                return {
                    "status": "success",
                    "message": "Conversion completed successfully",
                    "input_file": input_file,
                    "output_file": output_file,
                    "output_size": file_size,
                    "processing_time": round(end_time - start_time, 3)
                }
            else:
                return {
                    "status": "error",
                    "message": "Conversion failed - no output file created"
                }
                
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Invalid JSON request: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Conversion error: {str(e)}"
            }
    
    def stop(self):
        """Stop the pipe server"""
        self.running = False


def create_vfp9_pipe_example():
    """Create VFP9 example for pipe communication"""
    
    vfp9_pipe = '''*!* Universal Document Converter - VFP9 Named Pipes Integration
*!* Communicates with Python pipe server for document conversion

*-- Constants for file access
#DEFINE GENERIC_READ          0x80000000
#DEFINE GENERIC_WRITE         0x40000000
#DEFINE OPEN_EXISTING         3
#DEFINE PIPE_WAIT             0

*-- API Declarations
DECLARE INTEGER CreateFile IN kernel32 ;
    STRING lpFileName, INTEGER dwDesiredAccess, INTEGER dwShareMode, ;
    INTEGER lpSecurityAttributes, INTEGER dwCreationDisposition, ;
    INTEGER dwFlagsAndAttributes, INTEGER hTemplateFile

DECLARE INTEGER WriteFile IN kernel32 ;
    INTEGER hFile, STRING lpBuffer, INTEGER nNumberOfBytesToWrite, ;
    INTEGER lpNumberOfBytesWritten, INTEGER lpOverlapped

DECLARE INTEGER ReadFile IN kernel32 ;
    INTEGER hFile, STRING @lpBuffer, INTEGER nNumberOfBytesToRead, ;
    INTEGER lpNumberOfBytesRead, INTEGER lpOverlapped

DECLARE INTEGER CloseHandle IN kernel32 INTEGER hObject

*!* Convert document using named pipe
FUNCTION ConvertDocumentPipe(tcInputFile, tcOutputFile, tcInputFormat, tcOutputFormat)
    LOCAL lnPipeHandle, lcRequest, lcResponse, llSuccess
    LOCAL lnBytesWritten, lnBytesRead, lnResult
    
    *-- Create pipe connection
    lnPipeHandle = CreateFile("\\\\.\\pipe\\UniversalConverter", ;
        GENERIC_READ + GENERIC_WRITE, 0, 0, OPEN_EXISTING, PIPE_WAIT, 0)
    
    IF lnPipeHandle = -1
        MESSAGEBOX("Failed to connect to converter pipe server")
        RETURN .F.
    ENDIF
    
    TRY
        *-- Create JSON request
        lcRequest = '{"input":"' + tcInputFile + '","output":"' + tcOutputFile + ;
                   '","input_format":"' + tcInputFormat + ;
                   '","output_format":"' + tcOutputFormat + '"}'
        
        *-- Send request
        lnBytesWritten = 0
        lnResult = WriteFile(lnPipeHandle, lcRequest, LEN(lcRequest), @lnBytesWritten, 0)
        
        IF lnResult = 0 OR lnBytesWritten = 0
            MESSAGEBOX("Failed to send request to pipe server")
            RETURN .F.
        ENDIF
        
        *-- Read response
        lcResponse = SPACE(4096)
        lnBytesRead = 0
        lnResult = ReadFile(lnPipeHandle, @lcResponse, LEN(lcResponse), @lnBytesRead, 0)
        
        IF lnResult = 0 OR lnBytesRead = 0
            MESSAGEBOX("Failed to read response from pipe server")
            RETURN .F.
        ENDIF
        
        *-- Trim response to actual length
        lcResponse = LEFT(lcResponse, lnBytesRead)
        
        *-- Parse response (simple check for success)
        llSuccess = ("success" $ LOWER(lcResponse))
        
        IF NOT llSuccess
            MESSAGEBOX("Conversion failed: " + lcResponse)
        ENDIF
        
        RETURN llSuccess
        
    CATCH TO loException
        MESSAGEBOX("Pipe communication error: " + loException.Message)
        RETURN .F.
    FINALLY
        *-- Always close the pipe handle
        CloseHandle(lnPipeHandle)
    ENDTRY
ENDFUNC

*!* Test pipe communication
PROCEDURE TestPipeConversion()
    LOCAL llResult
    
    *-- Test conversion
    llResult = ConvertDocumentPipe("C:\\temp\\test.md", "C:\\temp\\test.rtf", "markdown", "rtf")
    
    IF llResult
        MESSAGEBOX("Pipe conversion successful!")
    ELSE
        MESSAGEBOX("Pipe conversion failed!")
    ENDIF
ENDPROC

*!* Example usage with error handling
PROCEDURE PipeConversionExample()
    LOCAL lcInputFile, lcOutputFile
    
    *-- Set file paths
    lcInputFile = GETFILE("md", "Select Markdown file:", "Open")
    IF EMPTY(lcInputFile)
        RETURN
    ENDIF
    
    lcOutputFile = PUTFILE("RTF File", STRTRAN(lcInputFile, ".md", ".rtf"), "rtf")
    IF EMPTY(lcOutputFile)
        RETURN  
    ENDIF
    
    *-- Start pipe server if not running
    *-- (You would need to start pipe_server.py separately)
    
    *-- Convert using pipe
    IF ConvertDocumentPipe(lcInputFile, lcOutputFile, "markdown", "rtf")
        MESSAGEBOX("Document converted successfully!" + CHR(13) + ;
                  "Output: " + lcOutputFile)
    ELSE
        MESSAGEBOX("Document conversion failed!")
    ENDIF
ENDPROC
'''
    
    with open('VFP9_PipeClient.prg', 'w') as f:
        f.write(vfp9_pipe)
    
    print("✅ Created VFP9 pipe client example: VFP9_PipeClient.prg")


def create_vb6_pipe_example():
    """Create VB6 example for pipe communication"""
    
    vb6_pipe = r'''Attribute VB_Name = "PipeClientModule"
'Universal Document Converter - VB6 Named Pipes Integration
'Communicates with Python pipe server for document conversion

'API Declarations for Named Pipes
Private Declare Function CreateFile Lib "kernel32" Alias "CreateFileA" _
    (ByVal lpFileName As String, ByVal dwDesiredAccess As Long, _
     ByVal dwShareMode As Long, ByVal lpSecurityAttributes As Long, _
     ByVal dwCreationDisposition As Long, ByVal dwFlagsAndAttributes As Long, _
     ByVal hTemplateFile As Long) As Long

Private Declare Function WriteFile Lib "kernel32" _
    (ByVal hFile As Long, lpBuffer As Any, ByVal nNumberOfBytesToWrite As Long, _
     lpNumberOfBytesWritten As Long, ByVal lpOverlapped As Long) As Long

Private Declare Function ReadFile Lib "kernel32" _
    (ByVal hFile As Long, lpBuffer As Any, ByVal nNumberOfBytesToRead As Long, _
     lpNumberOfBytesRead As Long, ByVal lpOverlapped As Long) As Long

Private Declare Function CloseHandle Lib "kernel32" _
    (ByVal hObject As Long) As Long

'Constants
Private Const GENERIC_READ = &H80000000
Private Const GENERIC_WRITE = &H40000000
Private Const OPEN_EXISTING = 3
Private Const PIPE_WAIT = 0

'Convert document using named pipe
Public Function ConvertDocumentPipe(inputFile As String, outputFile As String, _
                                   inputFormat As String, outputFormat As String) As Boolean
    Dim pipeHandle As Long
    Dim request As String
    Dim response As String
    Dim bytesWritten As Long
    Dim bytesRead As Long
    Dim result As Long
    Dim buffer() As Byte
    
    'Create pipe connection
    pipeHandle = CreateFile("\\.\pipe\UniversalConverter", _
                           GENERIC_READ Or GENERIC_WRITE, 0, 0, OPEN_EXISTING, PIPE_WAIT, 0)
    
    If pipeHandle = -1 Then
        MsgBox "Failed to connect to converter pipe server"
        ConvertDocumentPipe = False
        Exit Function
    End If
    
    On Error GoTo ErrorHandler
    
    'Create JSON request
    request = "{""input"":""" & inputFile & """,""output"":""" & outputFile & _
              """,""input_format"":""" & inputFormat & """,""output_format"":""" & outputFormat & """}"
    
    'Send request
    buffer = StrConv(request, vbFromUnicode)
    result = WriteFile(pipeHandle, buffer(0), UBound(buffer) + 1, bytesWritten, 0)
    
    If result = 0 Or bytesWritten = 0 Then
        MsgBox "Failed to send request to pipe server"
        ConvertDocumentPipe = False
        GoTo Cleanup
    End If
    
    'Read response
    ReDim buffer(4095)
    result = ReadFile(pipeHandle, buffer(0), 4096, bytesRead, 0)
    
    If result = 0 Or bytesRead = 0 Then
        MsgBox "Failed to read response from pipe server"
        ConvertDocumentPipe = False
        GoTo Cleanup
    End If
    
    'Convert response to string
    ReDim Preserve buffer(bytesRead - 1)
    response = StrConv(buffer, vbUnicode)
    
    'Parse response (simple check for success)
    ConvertDocumentPipe = InStr(LCase(response), "success") > 0
    
    If Not ConvertDocumentPipe Then
        MsgBox "Conversion failed: " & response
    End If
    
Cleanup:
    CloseHandle pipeHandle
    Exit Function
    
ErrorHandler:
    MsgBox "Pipe communication error: " & Err.Description
    ConvertDocumentPipe = False
    GoTo Cleanup
End Function

'Test pipe communication
Public Sub TestPipeConversion()
    Dim result As Boolean
    
    'Test conversion
    result = ConvertDocumentPipe("C:\temp\test.md", "C:\temp\test.rtf", "markdown", "rtf")
    
    If result Then
        MsgBox "Pipe conversion successful!"
    Else
        MsgBox "Pipe conversion failed!"
    End If
End Sub

'Example with file dialogs
Public Sub PipeConversionExample()
    Dim inputFile As String
    Dim outputFile As String
    
    'Get input file
    inputFile = InputBox("Enter path to Markdown file:", "Input File", "C:\temp\test.md")
    If inputFile = "" Then Exit Sub
    
    'Get output file  
    outputFile = InputBox("Enter path for RTF output:", "Output File", "C:\temp\test.rtf")
    If outputFile = "" Then Exit Sub
    
    'Convert using pipe
    If ConvertDocumentPipe(inputFile, outputFile, "markdown", "rtf") Then
        MsgBox "Document converted successfully!" & vbCrLf & "Output: " & outputFile
    Else
        MsgBox "Document conversion failed!"
    End If
End Sub
'''
    
    with open('VB6_PipeClient.bas', 'w') as f:
        f.write(vb6_pipe)
    
    print("✅ Created VB6 pipe client example: VB6_PipeClient.bas")


def test_pipe_server():
    """Test pipe server functionality"""
    print("🧪 Testing Pipe Server Functionality")
    print("=" * 50)
    
    server = PipeServer()
    
    if not server.converter:
        print("❌ UniversalConverter not available")
        return False
    
    print("✅ PipeServer created successfully")
    
    # Test request processing
    test_request = {
        "input": "test.md",
        "output": "test.rtf", 
        "input_format": "markdown",
        "output_format": "rtf"
    }
    
    # Create test input file
    with open('test.md', 'w', encoding='utf-8') as f:
        f.write("# Test Document\nThis is a **test** for pipe server.")
    
    # Test request processing
    request_json = json.dumps(test_request)
    response = server._process_request(request_json)
    
    print(f"✅ Request processing test: {response.get('status')}")
    
    if response.get('status') == 'success':
        print(f"   Output file: {response.get('output_file')}")
        print(f"   File size: {response.get('output_size')} bytes")
        print(f"   Processing time: {response.get('processing_time')} seconds")
    
    # Cleanup
    for file in ['test.md', 'test.rtf']:
        try:
            if os.path.exists(file):
                os.unlink(file)
        except:
            pass
    
    return response.get('status') == 'success'


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Document Converter Pipe Server")
    parser.add_argument("--windows", action="store_true", help="Start Windows named pipe server")
    parser.add_argument("--stdio", action="store_true", help="Start stdin/stdout pipe server")
    parser.add_argument("--vfp9-example", action="store_true", help="Create VFP9 pipe client example")
    parser.add_argument("--vb6-example", action="store_true", help="Create VB6 pipe client example")
    parser.add_argument("--test", action="store_true", help="Test pipe server functionality")
    parser.add_argument("--examples", action="store_true", help="Create all client examples")
    
    args = parser.parse_args()
    
    if args.windows:
        server = PipeServer()
        try:
            server.start_windows_pipe_server()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
    elif args.stdio:
        server = PipeServer()
        try:
            server.start_stdio_server()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user", file=sys.stderr)
    elif args.vfp9_example:
        create_vfp9_pipe_example()
    elif args.vb6_example:
        create_vb6_pipe_example()
    elif args.examples:
        create_vfp9_pipe_example()
        create_vb6_pipe_example()
    elif args.test:
        test_pipe_server()
    else:
        print("Universal Document Converter Pipe Server v2.1.0")
        print("\nOptions:")
        print("  --windows       Start Windows named pipe server")
        print("  --stdio         Start stdin/stdout pipe server (cross-platform)")
        print("  --vfp9-example  Create VFP9 client example")
        print("  --vb6-example   Create VB6 client example")
        print("  --examples      Create all client examples")
        print("  --test          Test pipe server functionality")
        print("\nUsage:")
        print("  python pipe_server.py --stdio")
        print("  python pipe_server.py --windows  # Windows only")
        print("  python pipe_server.py --examples  # Create client examples")