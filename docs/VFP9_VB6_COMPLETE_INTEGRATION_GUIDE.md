# Universal Document Converter v2.1.0 - Complete VFP9/VB6 Integration Guide

This comprehensive guide covers all aspects of integrating Universal Document Converter with Visual FoxPro 9 (VFP9) and Visual Basic 6 (VB6) applications.

## Table of Contents

1. [Overview](#overview)
2. [Installation for VFP9/VB6](#installation-for-vfp9vb6)
3. [Integration Methods](#integration-methods)
4. [Method 1: Command Line Interface](#method-1-command-line-interface)
5. [Method 2: JSON File IPC](#method-2-json-file-ipc)
6. [Method 3: Named Pipes](#method-3-named-pipes)
7. [Method 4: COM Server](#method-4-com-server)
8. [Method 5: DLL Wrapper](#method-5-dll-wrapper)
9. [Complete Code Examples](#complete-code-examples)
10. [Error Handling](#error-handling)
11. [Performance Optimization](#performance-optimization)
12. [Troubleshooting](#troubleshooting)

## Overview

Universal Document Converter v2.1.0 provides five different methods for VFP9/VB6 integration:

| Method | Complexity | Performance | Best For |
|--------|------------|-------------|----------|
| Command Line | Simple | Good | Quick integration |
| JSON File IPC | Medium | Good | Structured data exchange |
| Named Pipes | Medium | Better | Real-time communication |
| COM Server | Medium | Best | Native Windows integration |
| DLL Wrapper | Complex | Best | Direct function calls |

## Installation for VFP9/VB6

### Step 1: Download Required Files

1. **For Basic Integration (Methods 1-2)**:
   - Download [Universal-Document-Converter-v2.1.0-Windows-Complete.zip](https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/Universal-Document-Converter-v2.1.0-Windows-Complete.zip)
   - Extract to a known location (e.g., `C:\UniversalConverter`)

2. **For Advanced Integration (Methods 3-5)**:
   - Also download [UniversalConverter32.dll.zip](https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/latest/download/UniversalConverter32.dll.zip)
   - Extract DLL files to your application directory

### Step 2: Set Up Environment

#### For VFP9:
```foxpro
*!* Add to your application startup
SET PATH TO C:\UniversalConverter ADDITIVE
SET PROCEDURE TO UniversalConverter_VFP9.prg ADDITIVE
```

#### For VB6:
1. Add module to project: Project → Add Module → Existing
2. Browse to `VB6_UniversalConverter.bas`
3. For DLL method: Register DLL with `regsvr32 UniversalConverter32.dll`

### Step 3: Verify Installation

#### VFP9 Test:
```foxpro
*!* Test if converter is accessible
IF FILE("C:\UniversalConverter\universal_document_converter_ocr.py")
    MESSAGEBOX("Converter found and ready!")
ELSE
    MESSAGEBOX("Converter not found! Check installation path.")
ENDIF
```

#### VB6 Test:
```vb
' Test if converter is accessible
If Dir("C:\UniversalConverter\universal_document_converter_ocr.py") <> "" Then
    MsgBox "Converter found and ready!"
Else
    MsgBox "Converter not found! Check installation path."
End If
```

## Integration Methods

### Quick Comparison

- **Command Line**: Easiest, works everywhere, slightly slower
- **JSON IPC**: Good for complex data, structured communication
- **Named Pipes**: Real-time, bidirectional communication
- **COM Server**: Native Windows feel, good performance
- **DLL Wrapper**: Best performance, requires 32-bit compatibility

## Method 1: Command Line Interface

### Overview
The simplest method - execute the converter as an external process.

### VFP9 Implementation

#### Basic Conversion
```foxpro
*!* Simple conversion function
FUNCTION ConvertDocument(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    LOCAL lcCommand, lnResult
    
    TEXT TO lcCommand NOSHOW TEXTMERGE
python "C:\UniversalConverter\universal_document_converter_ocr.py" "<<tcInput>>" "<<tcOutput>>" -if <<tcInputFormat>> -of <<tcOutputFormat>>
    ENDTEXT
    
    RUN /N (lcCommand)
    
    *!* Wait for file to be created
    LOCAL lnSeconds
    lnSeconds = 0
    DO WHILE !FILE(tcOutput) AND lnSeconds < 30
        WAIT WINDOW "Converting..." TIMEOUT 1
        lnSeconds = lnSeconds + 1
    ENDDO
    
    RETURN FILE(tcOutput)
ENDFUNC
```

#### Advanced Implementation with Error Handling
```foxpro
*!* Advanced conversion with options
FUNCTION ConvertDocumentEx(tcInput, tcOutput, tcOptions)
    LOCAL lcCommand, lcTempFile, lcResult, llSuccess
    
    *!* Build command with options
    lcCommand = 'python "C:\UniversalConverter\universal_document_converter_ocr.py" '
    lcCommand = lcCommand + '"' + tcInput + '" "' + tcOutput + '"'
    
    *!* Add options if provided
    IF !EMPTY(tcOptions)
        lcCommand = lcCommand + ' ' + tcOptions
    ENDIF
    
    *!* Create temp file for output capture
    lcTempFile = SYS(2023) + '\' + SYS(2015) + '.txt'
    lcCommand = lcCommand + ' > "' + lcTempFile + '" 2>&1'
    
    *!* Execute
    RUN /N (lcCommand)
    
    *!* Wait and check result
    DO WHILE !FILE(lcTempFile)
        WAIT WINDOW "Processing..." TIMEOUT 0.5
    ENDDO
    
    *!* Read result
    lcResult = FILETOSTR(lcTempFile)
    DELETE FILE (lcTempFile)
    
    llSuccess = FILE(tcOutput) AND !("error" $ LOWER(lcResult))
    
    IF !llSuccess
        MESSAGEBOX("Conversion failed: " + lcResult, 16, "Error")
    ENDIF
    
    RETURN llSuccess
ENDFUNC
```

#### Batch Processing
```foxpro
*!* Convert multiple files
FUNCTION BatchConvert(taFiles, tcOutputFormat)
    LOCAL lnI, lcInput, lcOutput, lnConverted
    
    lnConverted = 0
    
    FOR lnI = 1 TO ALEN(taFiles)
        lcInput = taFiles[lnI]
        lcOutput = FORCEEXT(lcInput, tcOutputFormat)
        
        WAIT WINDOW "Converting " + JUSTFNAME(lcInput) + "..." NOWAIT
        
        IF ConvertDocument(lcInput, lcOutput, "", tcOutputFormat)
            lnConverted = lnConverted + 1
        ENDIF
    ENDFOR
    
    WAIT CLEAR
    MESSAGEBOX("Converted " + STR(lnConverted) + " of " + STR(ALEN(taFiles)) + " files")
    
    RETURN lnConverted
ENDFUNC
```

### VB6 Implementation

#### Basic Conversion
```vb
' Simple conversion function
Public Function ConvertDocument(inputFile As String, outputFile As String, _
                              inputFormat As String, outputFormat As String) As Boolean
    Dim cmd As String
    Dim wsh As Object
    Dim result As Integer
    
    ' Build command
    cmd = "python ""C:\UniversalConverter\universal_document_converter_ocr.py"" "
    cmd = cmd & """" & inputFile & """ """ & outputFile & """"
    
    If inputFormat <> "" Then cmd = cmd & " -if " & inputFormat
    If outputFormat <> "" Then cmd = cmd & " -of " & outputFormat
    
    ' Execute with wait
    Set wsh = CreateObject("WScript.Shell")
    result = wsh.Run(cmd, 0, True)
    
    ' Check if successful
    ConvertDocument = (result = 0) And (Dir(outputFile) <> "")
End Function
```

#### Advanced Implementation
```vb
' Advanced conversion with progress callback
Public Function ConvertDocumentEx(inputFile As String, outputFile As String, _
                                options As String, Optional progressCallback As Object) As Boolean
    Dim cmd As String
    Dim tempFile As String
    Dim fso As Object
    Dim ts As Object
    Dim output As String
    
    ' Build command
    cmd = "python ""C:\UniversalConverter\universal_document_converter_ocr.py"" "
    cmd = cmd & """" & inputFile & """ """ & outputFile & """ " & options
    
    ' Create temp file for output
    Set fso = CreateObject("Scripting.FileSystemObject")
    tempFile = Environ("TEMP") & "\" & fso.GetTempName
    cmd = cmd & " > """ & tempFile & """ 2>&1"
    
    ' Execute
    Shell cmd, vbHide
    
    ' Wait for completion with progress
    Dim elapsed As Integer
    elapsed = 0
    Do While Not fso.FileExists(outputFile) And elapsed < 30
        If Not progressCallback Is Nothing Then
            progressCallback.UpdateProgress elapsed, 30
        End If
        Sleep 1000
        elapsed = elapsed + 1
    Loop
    
    ' Read output
    If fso.FileExists(tempFile) Then
        Set ts = fso.OpenTextFile(tempFile, 1)
        output = ts.ReadAll
        ts.Close
        fso.DeleteFile tempFile
    End If
    
    ' Check result
    ConvertDocumentEx = fso.FileExists(outputFile)
    
    If Not ConvertDocumentEx And output <> "" Then
        MsgBox "Conversion failed: " & output, vbCritical
    End If
End Function
```

## Method 2: JSON File IPC

### Overview
Structured communication using JSON files for request/response.

### Configuration
Create `vfp9_config.json`:
```json
{
    "ipc_method": "json_file",
    "request_file": "C:\\temp\\uc_request.json",
    "response_file": "C:\\temp\\uc_response.json",
    "timeout": 30,
    "debug": false
}
```

### VFP9 Implementation

#### JSON Helper Functions
```foxpro
*!* JSON creation helper
FUNCTION CreateConversionRequest(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    LOCAL lcJSON
    
    TEXT TO lcJSON NOSHOW TEXTMERGE
{
    "action": "convert",
    "request_id": "<<SYS(2015)>>",
    "timestamp": "<<DATETIME()>>",
    "input_file": "<<tcInput>>",
    "output_file": "<<tcOutput>>",
    "input_format": "<<tcInputFormat>>",
    "output_format": "<<tcOutputFormat>>",
    "options": {
        "ocr_enabled": false,
        "quality": "high",
        "preserve_formatting": true
    }
}
    ENDTEXT
    
    RETURN lcJSON
ENDFUNC

*!* JSON response parser (simple)
FUNCTION ParseJSONResponse(tcJSON)
    LOCAL loResult
    
    *!* Create result object
    SCATTER NAME loResult MEMO BLANK
    
    *!* Parse basic fields
    loResult.success = '"success": true' $ tcJSON
    loResult.error = STREXTRACT(tcJSON, '"error": "', '"')
    loResult.message = STREXTRACT(tcJSON, '"message": "', '"')
    loResult.output_file = STREXTRACT(tcJSON, '"output_file": "', '"')
    
    RETURN loResult
ENDFUNC
```

#### Complete JSON IPC Implementation
```foxpro
*!* JSON IPC conversion
FUNCTION ConvertViaJSON(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    LOCAL lcRequest, lcResponse, loResult, llSuccess
    LOCAL lcRequestFile, lcResponseFile
    
    *!* File paths from config
    lcRequestFile = "C:\temp\uc_request.json"
    lcResponseFile = "C:\temp\uc_response.json"
    
    *!* Clean up old files
    DELETE FILE (lcRequestFile)
    DELETE FILE (lcResponseFile)
    
    *!* Create request
    lcRequest = CreateConversionRequest(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    STRTOFILE(lcRequest, lcRequestFile)
    
    *!* Execute converter with JSON IPC
    RUN /N python "C:\UniversalConverter\universal_document_converter_ocr.py" --json-ipc
    
    *!* Wait for response
    LOCAL lnWaitTime
    lnWaitTime = 0
    DO WHILE !FILE(lcResponseFile) AND lnWaitTime < 30
        WAIT WINDOW "Processing via JSON IPC..." TIMEOUT 1
        lnWaitTime = lnWaitTime + 1
    ENDDO
    
    *!* Process response
    IF FILE(lcResponseFile)
        lcResponse = FILETOSTR(lcResponseFile)
        loResult = ParseJSONResponse(lcResponse)
        llSuccess = loResult.success
        
        IF !llSuccess
            MESSAGEBOX("Conversion failed: " + loResult.error, 16)
        ENDIF
    ELSE
        llSuccess = .F.
        MESSAGEBOX("Timeout waiting for response", 16)
    ENDIF
    
    *!* Cleanup
    DELETE FILE (lcRequestFile)
    DELETE FILE (lcResponseFile)
    
    RETURN llSuccess
ENDFUNC
```

### VB6 Implementation

#### JSON Helper Class
```vb
' JsonHelper.cls
Option Explicit

Public Function CreateConversionRequest(inputFile As String, outputFile As String, _
                                      inputFormat As String, outputFormat As String) As String
    Dim json As String
    
    json = "{" & vbCrLf
    json = json & "  ""action"": ""convert""," & vbCrLf
    json = json & "  ""request_id"": """ & CreateGUID() & """," & vbCrLf
    json = json & "  ""timestamp"": """ & Now & """," & vbCrLf
    json = json & "  ""input_file"": """ & Replace(inputFile, "\", "\\") & """," & vbCrLf
    json = json & "  ""output_file"": """ & Replace(outputFile, "\", "\\") & """," & vbCrLf
    json = json & "  ""input_format"": """ & inputFormat & """," & vbCrLf
    json = json & "  ""output_format"": """ & outputFormat & """," & vbCrLf
    json = json & "  ""options"": {" & vbCrLf
    json = json & "    ""ocr_enabled"": false," & vbCrLf
    json = json & "    ""quality"": ""high""" & vbCrLf
    json = json & "  }" & vbCrLf
    json = json & "}"
    
    CreateConversionRequest = json
End Function

Public Function ParseJSONResponse(jsonText As String) As Object
    Dim result As Object
    Set result = CreateObject("Scripting.Dictionary")
    
    ' Simple parsing
    result("success") = InStr(jsonText, """success"": true") > 0
    result("error") = ExtractJSONValue(jsonText, "error")
    result("message") = ExtractJSONValue(jsonText, "message")
    result("output_file") = ExtractJSONValue(jsonText, "output_file")
    
    Set ParseJSONResponse = result
End Function

Private Function ExtractJSONValue(json As String, key As String) As String
    Dim startPos As Long, endPos As Long
    
    startPos = InStr(json, """" & key & """: """)
    If startPos > 0 Then
        startPos = startPos + Len("""" & key & """: """)
        endPos = InStr(startPos, json, """")
        If endPos > startPos Then
            ExtractJSONValue = Mid(json, startPos, endPos - startPos)
        End If
    End If
End Function
```

#### Complete JSON IPC Implementation
```vb
' JSON IPC conversion
Public Function ConvertViaJSON(inputFile As String, outputFile As String, _
                             inputFormat As String, outputFormat As String) As Boolean
    Dim fso As Object
    Dim ts As Object
    Dim requestFile As String
    Dim responseFile As String
    Dim requestJSON As String
    Dim responseJSON As String
    Dim result As Object
    Dim elapsed As Integer
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' File paths
    requestFile = "C:\temp\uc_request.json"
    responseFile = "C:\temp\uc_response.json"
    
    ' Clean up old files
    If fso.FileExists(requestFile) Then fso.DeleteFile requestFile
    If fso.FileExists(responseFile) Then fso.DeleteFile responseFile
    
    ' Create request
    Dim helper As New JsonHelper
    requestJSON = helper.CreateConversionRequest(inputFile, outputFile, inputFormat, outputFormat)
    
    ' Write request file
    Set ts = fso.CreateTextFile(requestFile, True)
    ts.Write requestJSON
    ts.Close
    
    ' Execute converter
    Shell "python ""C:\UniversalConverter\universal_document_converter_ocr.py"" --json-ipc", vbHide
    
    ' Wait for response
    elapsed = 0
    Do While Not fso.FileExists(responseFile) And elapsed < 30
        Sleep 1000
        elapsed = elapsed + 1
    Loop
    
    ' Process response
    If fso.FileExists(responseFile) Then
        Set ts = fso.OpenTextFile(responseFile, 1)
        responseJSON = ts.ReadAll
        ts.Close
        
        Set result = helper.ParseJSONResponse(responseJSON)
        ConvertViaJSON = result("success")
        
        If Not ConvertViaJSON Then
            MsgBox "Conversion failed: " & result("error"), vbCritical
        End If
    Else
        ConvertViaJSON = False
        MsgBox "Timeout waiting for response", vbCritical
    End If
    
    ' Cleanup
    If fso.FileExists(requestFile) Then fso.DeleteFile requestFile
    If fso.FileExists(responseFile) Then fso.DeleteFile responseFile
End Function
```

## Method 3: Named Pipes

### Overview
Real-time bidirectional communication using Windows named pipes.

### Server Setup
Start the pipe server:
```bash
python pipe_server.py
```

### VFP9 Implementation

```foxpro
*!* Named Pipe Client for VFP9
*!* Save as VFP9_PipeClient.prg

*!* Windows API declarations
DECLARE INTEGER CreateFile IN kernel32 ;
    STRING lpFileName, ;
    INTEGER dwDesiredAccess, ;
    INTEGER dwShareMode, ;
    INTEGER lpSecurityAttributes, ;
    INTEGER dwCreationDisposition, ;
    INTEGER dwFlagsAndAttributes, ;
    INTEGER hTemplateFile

DECLARE INTEGER WriteFile IN kernel32 ;
    INTEGER hFile, ;
    STRING lpBuffer, ;
    INTEGER nNumberOfBytesToWrite, ;
    INTEGER @lpNumberOfBytesWritten, ;
    INTEGER lpOverlapped

DECLARE INTEGER ReadFile IN kernel32 ;
    INTEGER hFile, ;
    STRING @lpBuffer, ;
    INTEGER nNumberOfBytesToRead, ;
    INTEGER @lpNumberOfBytesRead, ;
    INTEGER lpOverlapped

DECLARE INTEGER CloseHandle IN kernel32 ;
    INTEGER hObject

*!* Constants
#DEFINE GENERIC_READ    0x80000000
#DEFINE GENERIC_WRITE   0x40000000
#DEFINE OPEN_EXISTING   3
#DEFINE FILE_ATTRIBUTE_NORMAL 0x80

*!* Main pipe communication function
FUNCTION ConvertViaPipe(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    LOCAL lhPipe, lcPipeName, lcRequest, lcResponse
    LOCAL lnBytesWritten, lnBytesRead
    LOCAL llSuccess
    
    *!* Pipe name
    lcPipeName = "\\.\pipe\UniversalConverter"
    
    *!* Open pipe
    lhPipe = CreateFile(lcPipeName, ;
                       GENERIC_READ + GENERIC_WRITE, ;
                       0, 0, OPEN_EXISTING, ;
                       FILE_ATTRIBUTE_NORMAL, 0)
    
    IF lhPipe = -1
        MESSAGEBOX("Failed to connect to pipe server", 16)
        RETURN .F.
    ENDIF
    
    *!* Create request
    TEXT TO lcRequest NOSHOW TEXTMERGE
{
    "action": "convert",
    "input_file": "<<tcInput>>",
    "output_file": "<<tcOutput>>",
    "input_format": "<<tcInputFormat>>",
    "output_format": "<<tcOutputFormat>>"
}
    ENDTEXT
    
    *!* Send request
    lnBytesWritten = 0
    WriteFile(lhPipe, lcRequest, LEN(lcRequest), @lnBytesWritten, 0)
    
    *!* Read response
    lcResponse = SPACE(4096)
    lnBytesRead = 0
    ReadFile(lhPipe, @lcResponse, LEN(lcResponse), @lnBytesRead, 0)
    
    *!* Process response
    lcResponse = LEFT(lcResponse, lnBytesRead)
    llSuccess = '"success": true' $ lcResponse
    
    *!* Close pipe
    CloseHandle(lhPipe)
    
    IF !llSuccess
        MESSAGEBOX("Pipe conversion failed: " + lcResponse, 16)
    ENDIF
    
    RETURN llSuccess
ENDFUNC
```

### VB6 Implementation

```vb
' Named Pipe Client Module
Option Explicit

' Windows API declarations
Private Declare Function CreateFile Lib "kernel32" Alias "CreateFileA" _
    (ByVal lpFileName As String, ByVal dwDesiredAccess As Long, _
     ByVal dwShareMode As Long, lpSecurityAttributes As Any, _
     ByVal dwCreationDisposition As Long, ByVal dwFlagsAndAttributes As Long, _
     ByVal hTemplateFile As Long) As Long

Private Declare Function WriteFile Lib "kernel32" _
    (ByVal hFile As Long, lpBuffer As Any, ByVal nNumberOfBytesToWrite As Long, _
     lpNumberOfBytesWritten As Long, lpOverlapped As Any) As Long

Private Declare Function ReadFile Lib "kernel32" _
    (ByVal hFile As Long, lpBuffer As Any, ByVal nNumberOfBytesToRead As Long, _
     lpNumberOfBytesRead As Long, lpOverlapped As Any) As Long

Private Declare Function CloseHandle Lib "kernel32" _
    (ByVal hObject As Long) As Long

' Constants
Private Const GENERIC_READ = &H80000000
Private Const GENERIC_WRITE = &H40000000
Private Const OPEN_EXISTING = 3
Private Const FILE_ATTRIBUTE_NORMAL = &H80
Private Const INVALID_HANDLE_VALUE = -1

' Pipe communication function
Public Function ConvertViaPipe(inputFile As String, outputFile As String, _
                             inputFormat As String, outputFormat As String) As Boolean
    Dim hPipe As Long
    Dim pipeName As String
    Dim request As String
    Dim response As String * 4096
    Dim bytesWritten As Long
    Dim bytesRead As Long
    
    ' Connect to pipe
    pipeName = "\\.\pipe\UniversalConverter"
    hPipe = CreateFile(pipeName, GENERIC_READ Or GENERIC_WRITE, _
                      0, ByVal 0&, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0)
    
    If hPipe = INVALID_HANDLE_VALUE Then
        MsgBox "Failed to connect to pipe server", vbCritical
        ConvertViaPipe = False
        Exit Function
    End If
    
    ' Create request
    request = "{" & vbCrLf & _
              "  ""action"": ""convert""," & vbCrLf & _
              "  ""input_file"": """ & Replace(inputFile, "\", "\\") & """," & vbCrLf & _
              "  ""output_file"": """ & Replace(outputFile, "\", "\\") & """," & vbCrLf & _
              "  ""input_format"": """ & inputFormat & """," & vbCrLf & _
              "  ""output_format"": """ & outputFormat & """" & vbCrLf & _
              "}"
    
    ' Send request
    WriteFile hPipe, ByVal request, Len(request), bytesWritten, ByVal 0&
    
    ' Read response
    ReadFile hPipe, ByVal response, Len(response), bytesRead, ByVal 0&
    
    ' Process response
    Dim responseText As String
    responseText = Left(response, bytesRead)
    ConvertViaPipe = InStr(responseText, """success"": true") > 0
    
    ' Close pipe
    CloseHandle hPipe
    
    If Not ConvertViaPipe Then
        MsgBox "Pipe conversion failed: " & responseText, vbCritical
    End If
End Function
```

## Method 4: COM Server

### Overview
Native Windows COM integration for seamless VB6/VFP9 usage.

### COM Server Setup
Register the COM server:
```bash
python com_server.py --register
```

### VFP9 Implementation

```foxpro
*!* COM Server usage in VFP9
FUNCTION ConvertViaCOM(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    LOCAL loConverter, llSuccess
    
    TRY
        *!* Create COM object
        loConverter = CREATEOBJECT("UniversalConverter.Application")
        
        *!* Simple conversion
        llSuccess = loConverter.ConvertFile(tcInput, tcOutput)
        
        *!* Or with format specification
        * llSuccess = loConverter.ConvertFileEx(tcInput, tcOutput, ;
        *                                      tcInputFormat, tcOutputFormat, ;
        *                                      .F., "high")
        
    CATCH TO loError
        MESSAGEBOX("COM Error: " + loError.Message, 16)
        llSuccess = .F.
    ENDTRY
    
    *!* Release COM object
    loConverter = NULL
    
    RETURN llSuccess
ENDFUNC

*!* Batch conversion via COM
FUNCTION BatchConvertCOM(taFiles, tcOutputFormat)
    LOCAL loConverter, loSafeArray, lnI, llSuccess
    
    TRY
        *!* Create COM object
        loConverter = CREATEOBJECT("UniversalConverter.Application")
        
        *!* Create safe array for COM
        loSafeArray = CREATEOBJECT("Scripting.Dictionary")
        FOR lnI = 1 TO ALEN(taFiles)
            loSafeArray.Add(STR(lnI), taFiles[lnI])
        ENDFOR
        
        *!* Batch convert
        llSuccess = loConverter.BatchConvert(loSafeArray.Items(), ;
                                           tcOutputFormat, ;
                                           JUSTPATH(taFiles[1]))
        
    CATCH TO loError
        MESSAGEBOX("COM Error: " + loError.Message, 16)
        llSuccess = .F.
    ENDTRY
    
    RETURN llSuccess
ENDFUNC
```

### VB6 Implementation

```vb
' COM Server usage in VB6
Private converter As Object

Private Sub Form_Load()
    ' Create COM object on form load
    On Error GoTo ErrorHandler
    Set converter = CreateObject("UniversalConverter.Application")
    Exit Sub
    
ErrorHandler:
    MsgBox "Failed to create COM object: " & Err.Description, vbCritical
End Sub

Private Sub Form_Unload(Cancel As Integer)
    ' Release COM object
    Set converter = Nothing
End Sub

' Simple conversion
Public Function ConvertViaCOM(inputFile As String, outputFile As String) As Boolean
    On Error GoTo ErrorHandler
    
    ConvertViaCOM = converter.ConvertFile(inputFile, outputFile)
    Exit Function
    
ErrorHandler:
    MsgBox "COM conversion failed: " & Err.Description, vbCritical
    ConvertViaCOM = False
End Function

' Advanced conversion with options
Public Function ConvertViaCOMEx(inputFile As String, outputFile As String, _
                               inputFormat As String, outputFormat As String, _
                               enableOCR As Boolean, quality As String) As Boolean
    On Error GoTo ErrorHandler
    
    ConvertViaCOMEx = converter.ConvertFileEx(inputFile, outputFile, _
                                             inputFormat, outputFormat, _
                                             enableOCR, quality)
    Exit Function
    
ErrorHandler:
    MsgBox "COM conversion failed: " & Err.Description, vbCritical
    ConvertViaCOMEx = False
End Function

' Batch conversion
Public Function BatchConvertCOM(files() As String, outputFormat As String, _
                               outputDir As String) As Boolean
    On Error GoTo ErrorHandler
    
    BatchConvertCOM = converter.BatchConvert(files, outputFormat, outputDir)
    Exit Function
    
ErrorHandler:
    MsgBox "Batch conversion failed: " & Err.Description, vbCritical
    BatchConvertCOM = False
End Function
```

## Method 5: DLL Wrapper

### Overview
Direct DLL function calls for best performance and 32-bit compatibility.

### DLL Setup
1. Extract `UniversalConverter32.dll` to application directory
2. Optionally register: `regsvr32 UniversalConverter32.dll`

### VFP9 Implementation

```foxpro
*!* DLL declarations
DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, ;
    STRING inputFormat, STRING outputFormat

DECLARE INTEGER ConvertDocumentEx IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, ;
    STRING inputFormat, STRING outputFormat, ;
    INTEGER enableOCR, STRING quality

DECLARE INTEGER TestConnection IN UniversalConverter32.dll

DECLARE INTEGER GetLastError IN UniversalConverter32.dll ;
    STRING @errorBuffer, INTEGER bufferSize

DECLARE STRING GetVersion IN UniversalConverter32.dll

*!* Constants
#DEFINE UC_SUCCESS 1
#DEFINE UC_FAILURE 0
#DEFINE UC_ERROR -1

*!* Basic DLL conversion
FUNCTION ConvertViaDLL(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    LOCAL lnResult
    
    *!* Test connection first
    IF TestConnection() != UC_SUCCESS
        MESSAGEBOX("DLL not available", 16)
        RETURN .F.
    ENDIF
    
    *!* Perform conversion
    lnResult = ConvertDocument(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    
    *!* Check result
    DO CASE
        CASE lnResult = UC_SUCCESS
            RETURN .T.
            
        CASE lnResult = UC_FAILURE
            MESSAGEBOX("Conversion failed", 16)
            RETURN .F.
            
        CASE lnResult = UC_ERROR
            LOCAL lcError
            lcError = SPACE(256)
            GetLastError(@lcError, 256)
            MESSAGEBOX("Error: " + TRIM(lcError), 16)
            RETURN .F.
    ENDCASE
ENDFUNC

*!* Advanced DLL conversion with OCR
FUNCTION ConvertViaDLLEx(tcInput, tcOutput, tcInputFormat, tcOutputFormat, tlOCR)
    LOCAL lnResult, lnOCR
    
    lnOCR = IIF(tlOCR, 1, 0)
    lnResult = ConvertDocumentEx(tcInput, tcOutput, ;
                                tcInputFormat, tcOutputFormat, ;
                                lnOCR, "high")
    
    RETURN (lnResult = UC_SUCCESS)
ENDFUNC

*!* Get DLL version
FUNCTION GetDLLVersion()
    LOCAL lcVersion
    lcVersion = GetVersion()
    RETURN lcVersion
ENDFUNC
```

### VB6 Implementation

```vb
' DLL declarations module
Option Explicit

' DLL function declarations
Public Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String, _
     ByVal inputFormat As String, ByVal outputFormat As String) As Long

Public Declare Function ConvertDocumentEx Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String, _
     ByVal inputFormat As String, ByVal outputFormat As String, _
     ByVal enableOCR As Long, ByVal quality As String) As Long

Public Declare Function TestConnection Lib "UniversalConverter32.dll" () As Long

Public Declare Function GetLastError Lib "UniversalConverter32.dll" _
    (ByVal errorBuffer As String, ByVal bufferSize As Long) As Long

Public Declare Function GetVersion Lib "UniversalConverter32.dll" () As String

' Constants
Public Const UC_SUCCESS = 1
Public Const UC_FAILURE = 0
Public Const UC_ERROR = -1

' Basic DLL conversion
Public Function ConvertViaDLL(inputFile As String, outputFile As String, _
                            inputFormat As String, outputFormat As String) As Boolean
    Dim result As Long
    
    ' Test connection first
    If TestConnection() <> UC_SUCCESS Then
        MsgBox "DLL not available", vbCritical
        ConvertViaDLL = False
        Exit Function
    End If
    
    ' Perform conversion
    result = ConvertDocument(inputFile, outputFile, inputFormat, outputFormat)
    
    ' Check result
    Select Case result
        Case UC_SUCCESS
            ConvertViaDLL = True
            
        Case UC_FAILURE
            MsgBox "Conversion failed", vbCritical
            ConvertViaDLL = False
            
        Case UC_ERROR
            Dim errorMsg As String * 256
            GetLastError errorMsg, 256
            MsgBox "Error: " & Trim(errorMsg), vbCritical
            ConvertViaDLL = False
    End Select
End Function

' Advanced DLL conversion with OCR
Public Function ConvertViaDLLEx(inputFile As String, outputFile As String, _
                              inputFormat As String, outputFormat As String, _
                              enableOCR As Boolean) As Boolean
    Dim result As Long
    Dim ocrFlag As Long
    
    ocrFlag = IIf(enableOCR, 1, 0)
    result = ConvertDocumentEx(inputFile, outputFile, _
                              inputFormat, outputFormat, _
                              ocrFlag, "high")
    
    ConvertViaDLLEx = (result = UC_SUCCESS)
End Function

' Get DLL version
Public Function GetDLLVersion() As String
    GetDLLVersion = GetVersion()
End Function
```

## Complete Code Examples

### VFP9 Complete Application

```foxpro
*!* Complete VFP9 Document Converter Application
*!* Save as DocumentConverter.prg

*!* Initialize converter
PROCEDURE InitConverter
    PUBLIC gcConverterPath, gnMethod
    
    *!* Set converter path
    gcConverterPath = "C:\UniversalConverter\"
    
    *!* Select method (1-5)
    gnMethod = 1  && Default to command line
    
    *!* Load procedures
    DO CASE
        CASE gnMethod = 5  && DLL method
            *!* Declare DLL functions
            DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
                STRING inputFile, STRING outputFile, ;
                STRING inputFormat, STRING outputFormat
    ENDCASE
ENDPROC

*!* Main conversion function
FUNCTION ConvertFile(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    LOCAL llSuccess
    
    DO CASE
        CASE gnMethod = 1
            llSuccess = ConvertViaCommandLine(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
        CASE gnMethod = 2
            llSuccess = ConvertViaJSON(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
        CASE gnMethod = 3
            llSuccess = ConvertViaPipe(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
        CASE gnMethod = 4
            llSuccess = ConvertViaCOM(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
        CASE gnMethod = 5
            llSuccess = ConvertViaDLL(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    ENDCASE
    
    RETURN llSuccess
ENDFUNC

*!* Batch conversion with progress
FUNCTION BatchConvertFiles(tcSourceDir, tcDestDir, tcOutputFormat)
    LOCAL laFiles[1], lnFiles, lnI, lcSource, lcDest
    LOCAL lnConverted, lnFailed
    
    *!* Get files
    lnFiles = ADIR(laFiles, tcSourceDir + "\*.*")
    lnConverted = 0
    lnFailed = 0
    
    *!* Create progress form
    DO FORM ProgressForm NAME oProgress
    oProgress.Show()
    
    *!* Process files
    FOR lnI = 1 TO lnFiles
        lcSource = tcSourceDir + "\" + laFiles[lnI, 1]
        lcDest = tcDestDir + "\" + FORCEEXT(laFiles[lnI, 1], tcOutputFormat)
        
        *!* Update progress
        oProgress.UpdateProgress(lnI, lnFiles, laFiles[lnI, 1])
        
        *!* Convert
        IF ConvertFile(lcSource, lcDest, "", tcOutputFormat)
            lnConverted = lnConverted + 1
        ELSE
            lnFailed = lnFailed + 1
        ENDIF
        
        *!* Check for cancel
        IF oProgress.Cancelled
            EXIT
        ENDIF
    ENDFOR
    
    *!* Close progress
    oProgress.Release()
    
    *!* Show results
    MESSAGEBOX("Conversion complete!" + CHR(13) + ;
               "Converted: " + STR(lnConverted) + CHR(13) + ;
               "Failed: " + STR(lnFailed), 64, "Batch Conversion")
    
    RETURN lnConverted
ENDFUNC
```

### VB6 Complete Application

```vb
' Complete VB6 Document Converter Application
' Add to a form with appropriate controls

Option Explicit

Private converterPath As String
Private conversionMethod As Integer

Private Sub Form_Load()
    ' Initialize
    converterPath = "C:\UniversalConverter\"
    conversionMethod = 1  ' Default to command line
    
    ' Setup UI
    SetupUI
End Sub

Private Sub SetupUI()
    ' Add combo for method selection
    cboMethod.AddItem "Command Line"
    cboMethod.AddItem "JSON IPC"
    cboMethod.AddItem "Named Pipes"
    cboMethod.AddItem "COM Server"
    cboMethod.AddItem "DLL Wrapper"
    cboMethod.ListIndex = 0
    
    ' Add format combo
    cboFormat.AddItem "PDF"
    cboFormat.AddItem "DOCX"
    cboFormat.AddItem "RTF"
    cboFormat.AddItem "HTML"
    cboFormat.AddItem "TXT"
    cboFormat.AddItem "MD"
    cboFormat.ListIndex = 0
End Sub

' Main conversion function
Private Function ConvertFile(inputFile As String, outputFile As String, _
                           inputFormat As String, outputFormat As String) As Boolean
    Select Case conversionMethod
        Case 1
            ConvertFile = ConvertViaCommandLine(inputFile, outputFile, inputFormat, outputFormat)
        Case 2
            ConvertFile = ConvertViaJSON(inputFile, outputFile, inputFormat, outputFormat)
        Case 3
            ConvertFile = ConvertViaPipe(inputFile, outputFile, inputFormat, outputFormat)
        Case 4
            ConvertFile = ConvertViaCOM(inputFile, outputFile, inputFormat, outputFormat)
        Case 5
            ConvertFile = ConvertViaDLL(inputFile, outputFile, inputFormat, outputFormat)
    End Select
End Function

' Convert button click
Private Sub cmdConvert_Click()
    Dim inputFile As String
    Dim outputFile As String
    Dim outputFormat As String
    
    ' Get input file
    inputFile = txtInputFile.Text
    If inputFile = "" Then
        MsgBox "Please select an input file", vbExclamation
        Exit Sub
    End If
    
    ' Get output format
    outputFormat = LCase(cboFormat.Text)
    
    ' Generate output filename
    outputFile = Left(inputFile, InStrRev(inputFile, ".") - 1) & "." & outputFormat
    
    ' Show progress
    lblStatus.Caption = "Converting..."
    DoEvents
    
    ' Convert
    If ConvertFile(inputFile, outputFile, "", outputFormat) Then
        lblStatus.Caption = "Conversion successful!"
        MsgBox "File converted successfully!" & vbCrLf & vbCrLf & _
               "Output: " & outputFile, vbInformation
    Else
        lblStatus.Caption = "Conversion failed!"
        MsgBox "Conversion failed!", vbCritical
    End If
End Sub

' Batch conversion
Private Sub cmdBatchConvert_Click()
    Dim sourceDir As String
    Dim destDir As String
    Dim outputFormat As String
    Dim fso As Object
    Dim folder As Object
    Dim file As Object
    Dim converted As Integer
    Dim failed As Integer
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' Get directories
    sourceDir = txtSourceDir.Text
    destDir = txtDestDir.Text
    outputFormat = LCase(cboFormat.Text)
    
    If sourceDir = "" Or destDir = "" Then
        MsgBox "Please select source and destination directories", vbExclamation
        Exit Sub
    End If
    
    ' Process files
    Set folder = fso.GetFolder(sourceDir)
    converted = 0
    failed = 0
    
    ' Show progress form
    frmProgress.Show vbModeless
    
    For Each file In folder.Files
        ' Update progress
        frmProgress.UpdateProgress file.Name, converted + failed + 1, folder.Files.Count
        DoEvents
        
        ' Convert
        Dim outputFile As String
        outputFile = destDir & "\" & fso.GetBaseName(file.Name) & "." & outputFormat
        
        If ConvertFile(file.Path, outputFile, "", outputFormat) Then
            converted = converted + 1
        Else
            failed = failed + 1
        End If
        
        ' Check cancel
        If frmProgress.Cancelled Then Exit For
    Next
    
    ' Hide progress
    Unload frmProgress
    
    ' Show results
    MsgBox "Batch conversion complete!" & vbCrLf & vbCrLf & _
           "Converted: " & converted & vbCrLf & _
           "Failed: " & failed, vbInformation, "Batch Conversion"
End Sub
```

## Error Handling

### VFP9 Error Handling

```foxpro
*!* Comprehensive error handling
FUNCTION SafeConvert(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
    LOCAL llSuccess, lcError, loException
    
    llSuccess = .F.
    lcError = ""
    
    TRY
        *!* Validate inputs
        IF !FILE(tcInput)
            THROW "Input file not found: " + tcInput
        ENDIF
        
        IF EMPTY(JUSTPATH(tcOutput))
            THROW "Invalid output path: " + tcOutput
        ENDIF
        
        *!* Create output directory if needed
        LOCAL lcPath
        lcPath = JUSTPATH(tcOutput)
        IF !EMPTY(lcPath) AND !DIRECTORY(lcPath)
            MD (lcPath)
        ENDIF
        
        *!* Perform conversion
        llSuccess = ConvertFile(tcInput, tcOutput, tcInputFormat, tcOutputFormat)
        
        *!* Verify output
        IF llSuccess AND !FILE(tcOutput)
            THROW "Output file not created"
        ENDIF
        
    CATCH TO loException
        lcError = "Error: " + loException.Message
        IF !EMPTY(loException.Details)
            lcError = lcError + CHR(13) + "Details: " + loException.Details
        ENDIF
        
        *!* Log error
        LogError(lcError, tcInput, tcOutput)
        
        *!* Show error
        MESSAGEBOX(lcError, 16, "Conversion Error")
        
        llSuccess = .F.
    ENDTRY
    
    RETURN llSuccess
ENDFUNC

*!* Error logging
FUNCTION LogError(tcError, tcInput, tcOutput)
    LOCAL lcLogFile, lcLogEntry
    
    lcLogFile = "converter_errors.log"
    
    TEXT TO lcLogEntry NOSHOW TEXTMERGE
<<DATETIME()>> - ERROR
Input: <<tcInput>>
Output: <<tcOutput>>
Error: <<tcError>>
----------------------------------------
    ENDTEXT
    
    STRTOFILE(lcLogEntry, lcLogFile, 1)  && Append
ENDFUNC
```

### VB6 Error Handling

```vb
' Comprehensive error handling
Public Function SafeConvert(inputFile As String, outputFile As String, _
                          inputFormat As String, outputFormat As String) As Boolean
    On Error GoTo ErrorHandler
    
    Dim fso As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' Validate inputs
    If Not fso.FileExists(inputFile) Then
        Err.Raise vbObjectError + 1, , "Input file not found: " & inputFile
    End If
    
    ' Create output directory if needed
    Dim outputDir As String
    outputDir = fso.GetParentFolderName(outputFile)
    If outputDir <> "" And Not fso.FolderExists(outputDir) Then
        fso.CreateFolder outputDir
    End If
    
    ' Perform conversion
    SafeConvert = ConvertFile(inputFile, outputFile, inputFormat, outputFormat)
    
    ' Verify output
    If SafeConvert And Not fso.FileExists(outputFile) Then
        Err.Raise vbObjectError + 2, , "Output file not created"
    End If
    
    Exit Function
    
ErrorHandler:
    ' Log error
    LogError Err.Description, inputFile, outputFile
    
    ' Show error
    MsgBox "Conversion Error:" & vbCrLf & vbCrLf & _
           Err.Description, vbCritical, "Error"
    
    SafeConvert = False
End Function

' Error logging
Private Sub LogError(errorMsg As String, inputFile As String, outputFile As String)
    Dim fso As Object
    Dim ts As Object
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set ts = fso.OpenTextFile("converter_errors.log", 8, True)  ' Append mode
    
    ts.WriteLine Now & " - ERROR"
    ts.WriteLine "Input: " & inputFile
    ts.WriteLine "Output: " & outputFile
    ts.WriteLine "Error: " & errorMsg
    ts.WriteLine String(40, "-")
    
    ts.Close
End Sub
```

## Performance Optimization

### VFP9 Performance Tips

```foxpro
*!* Optimized batch conversion
FUNCTION FastBatchConvert(tcSourceDir, tcDestDir, tcOutputFormat)
    LOCAL laFiles[1], lnFiles, lnI
    LOCAL loPool, lnWorkers
    
    *!* Get file list
    lnFiles = ADIR(laFiles, tcSourceDir + "\*.*")
    
    *!* Determine optimal worker count
    lnWorkers = MIN(4, lnFiles)  && Max 4 parallel conversions
    
    *!* Process in parallel using multiple methods
    LOCAL lnMethod, lnFileIndex
    lnFileIndex = 1
    
    DO WHILE lnFileIndex <= lnFiles
        FOR lnMethod = 1 TO lnWorkers
            IF lnFileIndex <= lnFiles
                *!* Start async conversion
                StartAsyncConversion(;
                    tcSourceDir + "\" + laFiles[lnFileIndex, 1], ;
                    tcDestDir + "\" + FORCEEXT(laFiles[lnFileIndex, 1], tcOutputFormat), ;
                    "", tcOutputFormat, lnMethod)
                
                lnFileIndex = lnFileIndex + 1
            ENDIF
        ENDFOR
        
        *!* Wait for batch to complete
        WaitForConversions()
    ENDDO
    
    RETURN .T.
ENDFUNC

*!* Asynchronous conversion starter
FUNCTION StartAsyncConversion(tcInput, tcOutput, tcInputFormat, tcOutputFormat, tnMethod)
    LOCAL lcScript, lcScriptFile
    
    *!* Create conversion script
    TEXT TO lcScript NOSHOW TEXTMERGE
import sys
sys.path.append(r'<<gcConverterPath>>')
from universal_document_converter_ocr import UniversalConverter
converter = UniversalConverter("VFP9")
converter.convert_file(r'<<tcInput>>', r'<<tcOutput>>', '<<tcInputFormat>>', '<<tcOutputFormat>>')
    ENDTEXT
    
    *!* Save script
    lcScriptFile = SYS(2023) + "\" + SYS(2015) + ".py"
    STRTOFILE(lcScript, lcScriptFile)
    
    *!* Execute async
    RUN /N python (lcScriptFile)
    
    RETURN .T.
ENDFUNC
```

### VB6 Performance Tips

```vb
' Optimized batch conversion with threading
Private Type ConversionTask
    InputFile As String
    OutputFile As String
    Status As Integer  ' 0=Pending, 1=Running, 2=Complete, 3=Failed
End Type

Private tasks() As ConversionTask
Private taskCount As Integer

Public Sub FastBatchConvert(sourceDir As String, destDir As String, outputFormat As String)
    Dim fso As Object
    Dim folder As Object
    Dim file As Object
    Dim i As Integer
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set folder = fso.GetFolder(sourceDir)
    
    ' Build task list
    taskCount = folder.Files.Count
    ReDim tasks(1 To taskCount)
    
    i = 1
    For Each file In folder.Files
        tasks(i).InputFile = file.Path
        tasks(i).OutputFile = destDir & "\" & fso.GetBaseName(file.Name) & "." & outputFormat
        tasks(i).Status = 0
        i = i + 1
    Next
    
    ' Process with multiple workers
    Dim workers As Integer
    workers = 4  ' Optimal for most systems
    
    ' Start worker threads
    For i = 1 To workers
        StartWorker i
    Next
    
    ' Wait for completion
    WaitForAllTasks
    
    ' Show results
    ShowBatchResults
End Sub

Private Sub StartWorker(workerID As Integer)
    ' Create worker script
    Dim script As String
    Dim scriptFile As String
    
    script = "import sys" & vbCrLf & _
             "import json" & vbCrLf & _
             "sys.path.append(r'" & converterPath & "')" & vbCrLf & _
             "from universal_document_converter_ocr import UniversalConverter" & vbCrLf & _
             "converter = UniversalConverter('VB6')" & vbCrLf & _
             "# Process tasks for worker " & workerID & vbCrLf
    
    ' Add task processing logic
    Dim i As Integer
    For i = workerID To taskCount Step 4  ' Distribute tasks
        If tasks(i).Status = 0 Then
            script = script & "converter.convert_file(r'" & tasks(i).InputFile & _
                     "', r'" & tasks(i).OutputFile & "')" & vbCrLf
        End If
    Next
    
    ' Save and execute
    scriptFile = Environ("TEMP") & "\worker_" & workerID & ".py"
    SaveTextFile scriptFile, script
    
    Shell "python """ & scriptFile & """", vbHide
End Sub
```

## Troubleshooting

### Common Issues and Solutions

#### 1. DLL Not Found
**VFP9:**
```foxpro
*!* Check DLL availability
IF !FILE("UniversalConverter32.dll")
    MESSAGEBOX("DLL not found. Please ensure UniversalConverter32.dll is in the application directory.", 16)
    RETURN
ENDIF
```

**VB6:**
```vb
' Check DLL availability
If Dir(App.Path & "\UniversalConverter32.dll") = "" Then
    MsgBox "DLL not found. Please ensure UniversalConverter32.dll is in the application directory.", vbCritical
    Exit Sub
End If
```

#### 2. Python Not Found
**VFP9:**
```foxpro
*!* Check Python installation
FUNCTION CheckPython()
    LOCAL lcResult
    lcResult = ""
    
    RUN python --version > pythoncheck.txt 2>&1
    
    IF FILE("pythoncheck.txt")
        lcResult = FILETOSTR("pythoncheck.txt")
        DELETE FILE pythoncheck.txt
    ENDIF
    
    IF !"Python" $ lcResult
        MESSAGEBOX("Python not found. Please install Python 3.8 or later.", 16)
        RETURN .F.
    ENDIF
    
    RETURN .T.
ENDFUNC
```

**VB6:**
```vb
' Check Python installation
Function CheckPython() As Boolean
    Dim wsh As Object
    Dim result As Integer
    
    Set wsh = CreateObject("WScript.Shell")
    result = wsh.Run("python --version", 0, True)
    
    If result <> 0 Then
        MsgBox "Python not found. Please install Python 3.8 or later.", vbCritical
        CheckPython = False
    Else
        CheckPython = True
    End If
End Function
```

#### 3. Permission Errors
**VFP9:**
```foxpro
*!* Handle permission errors
FUNCTION CheckPermissions(tcPath)
    LOCAL llCanWrite
    
    TRY
        LOCAL lcTestFile
        lcTestFile = ADDBS(tcPath) + SYS(2015) + ".tmp"
        STRTOFILE("test", lcTestFile)
        DELETE FILE (lcTestFile)
        llCanWrite = .T.
    CATCH
        llCanWrite = .F.
        MESSAGEBOX("No write permission to: " + tcPath, 16)
    ENDTRY
    
    RETURN llCanWrite
ENDFUNC
```

**VB6:**
```vb
' Handle permission errors
Function CheckPermissions(path As String) As Boolean
    On Error GoTo NoPermission
    
    Dim testFile As String
    testFile = path & "\test_" & Timer & ".tmp"
    
    Open testFile For Output As #1
    Print #1, "test"
    Close #1
    Kill testFile
    
    CheckPermissions = True
    Exit Function
    
NoPermission:
    MsgBox "No write permission to: " & path, vbCritical
    CheckPermissions = False
End Function
```

### Debugging Tips

1. **Enable Verbose Logging**
   ```foxpro
   *!* VFP9
   lcCommand = lcCommand + " --verbose --log converter.log"
   ```
   
   ```vb
   ' VB6
   cmd = cmd & " --verbose --log converter.log"
   ```

2. **Check Process Exit Codes**
   ```foxpro
   *!* VFP9
   RUN /N7 (lcCommand) TO lnExitCode
   IF lnExitCode != 0
       MESSAGEBOX("Process failed with code: " + STR(lnExitCode))
   ENDIF
   ```

3. **Monitor File Creation**
   ```vb
   ' VB6
   Dim startTime As Single
   startTime = Timer
   
   Do While Not fso.FileExists(outputFile) And (Timer - startTime) < 30
       DoEvents
       Sleep 100
   Loop
   
   If Not fso.FileExists(outputFile) Then
       MsgBox "Timeout: Output file not created within 30 seconds"
   End If
   ```

## Best Practices

### For VFP9 Developers

1. **Always validate file paths**
2. **Use TRY-CATCH for error handling**
3. **Implement timeouts for long operations**
4. **Clean up temporary files**
5. **Log all operations for debugging**

### For VB6 Developers

1. **Use early binding when possible**
2. **Implement proper error handling**
3. **Release COM objects properly**
4. **Check for file locks before operations**
5. **Use asynchronous operations for UI responsiveness**

### General Tips

1. **Choose the right integration method**:
   - Simple needs: Command Line
   - Structured data: JSON IPC
   - Real-time: Named Pipes
   - Native feel: COM Server
   - Performance: DLL Wrapper

2. **Optimize for your use case**:
   - Single conversions: Any method
   - Batch processing: Parallel command line or DLL
   - UI integration: COM or DLL

3. **Handle edge cases**:
   - Large files
   - Network paths
   - Unicode filenames
   - Long path names

---

**Need more help?** 
- Check the main [USER_MANUAL.md](USER_MANUAL.md)
- Visit [GitHub Issues](https://github.com/Beaulewis1977/quick_ocr_doc_converter/issues)
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions