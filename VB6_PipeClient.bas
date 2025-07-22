Attribute VB_Name = "PipeClientModule"
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
