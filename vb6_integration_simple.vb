' VB6 Integration Example for Simple Document Converter
' Basic document conversion without OCR for legacy systems
' Compatible with 32-bit environments

Option Explicit

Private Declare Function ShellExecute Lib "shell32.dll" Alias "ShellExecuteA" _
    (ByVal hwnd As Long, ByVal lpOperation As String, ByVal lpFile As String, _
     ByVal lpParameters As String, ByVal lpDirectory As String, ByVal nShowCmd As Long) As Long

Private Declare Function CreateProcess Lib "kernel32" Alias "CreateProcessA" _
    (ByVal lpApplicationName As String, ByVal lpCommandLine As String, _
     ByVal lpProcessAttributes As Long, ByVal lpThreadAttributes As Long, _
     ByVal bInheritHandles As Long, ByVal dwCreationFlags As Long, _
     ByVal lpEnvironment As Long, ByVal lpCurrentDirectory As String, _
     lpStartupInfo As STARTUPINFO, lpProcessInformation As PROCESS_INFORMATION) As Long

Private Declare Function WaitForSingleObject Lib "kernel32" _
    (ByVal hHandle As Long, ByVal dwMilliseconds As Long) As Long

Private Declare Function CloseHandle Lib "kernel32" (ByVal hObject As Long) As Long

Private Type STARTUPINFO
    cb As Long
    lpReserved As String
    lpDesktop As String
    lpTitle As String
    dwX As Long
    dwY As Long
    dwXSize As Long
    dwYSize As Long
    dwXCountChars As Long
    dwYCountChars As Long
    dwFillAttribute As Long
    dwFlags As Long
    wShowWindow As Integer
    cbReserved2 As Integer
    lpReserved2 As Long
    hStdInput As Long
    hStdOutput As Long
    hStdError As Long
End Type

Private Type PROCESS_INFORMATION
    hProcess As Long
    hThread As Long
    dwProcessId As Long
    dwThreadId As Long
End Type

Public Class SimpleDocConverter
    Private PythonPath As String
    Private CliPath As String
    
    Public Sub Initialize()
        ' Set paths for Python and CLI script
        PythonPath = "python.exe"  ' Assumes Python is in PATH
        CliPath = App.Path & "\cli.py"  ' CLI script in same directory
    End Sub
    
    Public Function ConvertDocument(InputFile As String, OutputFile As String, _
                                  Optional OutputFormat As String = "txt", _
                                  Optional Encoding As String = "utf-8", _
                                  Optional LineEndings As String = "windows") As Boolean
        ' Convert a single document using the simple CLI
        
        Dim CommandLine As String
        Dim Result As Long
        
        ' Build command line
        CommandLine = """" & PythonPath & """ """ & CliPath & """ """ & _
                     InputFile & """ """ & OutputFile & """ --format " & OutputFormat & _
                     " --encoding " & Encoding & " --line-endings " & LineEndings
        
        ' Execute conversion
        Result = ExecuteCommand(CommandLine)
        
        ' Check if output file was created
        ConvertDocument = (Result = 0) And (Dir(OutputFile) <> "")
    End Function
    
    Public Function ConvertDirectory(InputDir As String, OutputDir As String, _
                                   Optional OutputFormat As String = "txt", _
                                   Optional Recursive As Boolean = False, _
                                   Optional Overwrite As Boolean = False) As Boolean
        ' Convert all documents in a directory
        
        Dim CommandLine As String
        Dim Result As Long
        Dim RecursiveFlag As String
        Dim OverwriteFlag As String
        
        ' Build flags
        If Recursive Then RecursiveFlag = " --recursive"
        If Overwrite Then OverwriteFlag = " --overwrite"
        
        ' Build command line
        CommandLine = """" & PythonPath & """ """ & CliPath & """ """ & _
                     InputDir & """ """ & OutputDir & """ --format " & OutputFormat & _
                     RecursiveFlag & OverwriteFlag
        
        ' Execute conversion
        Result = ExecuteCommand(CommandLine)
        
        ConvertDirectory = (Result = 0)
    End Function
    
    Public Function GetSupportedFormats() As String
        ' Get list of supported input/output formats
        
        Dim CommandLine As String
        Dim TempFile As String
        Dim FileNum As Integer
        Dim Content As String
        
        ' Create temp file for output
        TempFile = Environ("TEMP") & "\formats_" & Timer & ".txt"
        
        ' Build command line to get formats
        CommandLine = """" & PythonPath & """ """ & CliPath & """ --formats > """ & TempFile & """"
        
        ' Execute command
        ExecuteCommand CommandLine
        
        ' Read result from temp file
        If Dir(TempFile) <> "" Then
            FileNum = FreeFile
            Open TempFile For Input As FileNum
            Content = Input$(LOF(FileNum), FileNum)
            Close FileNum
            Kill TempFile  ' Delete temp file
        End If
        
        GetSupportedFormats = Content
    End Function
    
    Public Function ConvertPdfToText(PdfFile As String, TextFile As String) As Boolean
        ' Convert PDF to plain text (no OCR)
        ConvertPdfToText = ConvertDocument(PdfFile, TextFile, "txt")
    End Function
    
    Public Function ConvertDocxToMarkdown(DocxFile As String, MarkdownFile As String) As Boolean
        ' Convert DOCX to Markdown
        ConvertDocxToMarkdown = ConvertDocument(DocxFile, MarkdownFile, "md")
    End Function
    
    Public Function ConvertHtmlToText(HtmlFile As String, TextFile As String) As Boolean
        ' Convert HTML to plain text
        ConvertHtmlToText = ConvertDocument(HtmlFile, TextFile, "txt")
    End Function
    
    Public Function BatchConvertToJson(InputDir As String, OutputDir As String) As Boolean
        ' Batch convert all documents to JSON format
        BatchConvertToJson = ConvertDirectory(InputDir, OutputDir, "json", True, False)
    End Function
    
    Private Function ExecuteCommand(CommandLine As String) As Long
        ' Execute command and wait for completion
        
        Dim si As STARTUPINFO
        Dim pi As PROCESS_INFORMATION
        Dim Result As Long
        
        ' Initialize structures
        si.cb = Len(si)
        si.wShowWindow = 0  ' Hide window
        si.dwFlags = 1      ' Use wShowWindow
        
        ' Create process
        Result = CreateProcess(vbNullString, CommandLine, 0, 0, 0, 0, 0, vbNullString, si, pi)
        
        If Result <> 0 Then
            ' Wait for process to complete (30 second timeout)
            WaitForSingleObject pi.hProcess, 30000
            
            ' Close handles
            CloseHandle pi.hProcess
            CloseHandle pi.hThread
            
            ExecuteCommand = 0  ' Success
        Else
            ExecuteCommand = 1  ' Failed to start
        End If
    End Function
    
    Public Function TestConnection() As Boolean
        ' Test if CLI is accessible
        
        Dim CommandLine As String
        Dim Result As Long
        
        CommandLine = """" & PythonPath & """ """ & CliPath & """ --version"
        Result = ExecuteCommand(CommandLine)
        
        TestConnection = (Result = 0)
    End Function
End Class

' Example usage in a form or module
Sub ExampleUsage()
    Dim Converter As New SimpleDocConverter
    Dim Success As Boolean
    
    ' Initialize the converter
    Converter.Initialize
    
    ' Test connection
    If Not Converter.TestConnection() Then
        MsgBox "Error: Cannot connect to document converter CLI"
        Exit Sub
    End If
    
    ' Convert a single PDF to text
    Success = Converter.ConvertPdfToText("C:\Documents\sample.pdf", "C:\Output\sample.txt")
    If Success Then
        MsgBox "PDF converted successfully!"
    Else
        MsgBox "PDF conversion failed"
    End If
    
    ' Convert DOCX to Markdown
    Success = Converter.ConvertDocxToMarkdown("C:\Documents\report.docx", "C:\Output\report.md")
    
    ' Batch convert directory
    Success = Converter.ConvertDirectory("C:\Input\", "C:\Output\", "txt", True, True)
    If Success Then
        MsgBox "Directory conversion completed!"
    End If
    
    ' Get supported formats
    Dim Formats As String
    Formats = Converter.GetSupportedFormats()
    MsgBox "Supported formats:" & vbCrLf & Formats
End Sub