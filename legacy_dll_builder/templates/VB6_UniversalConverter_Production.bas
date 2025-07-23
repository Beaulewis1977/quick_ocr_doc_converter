Attribute VB_Name = "UniversalConverterModule"
' Universal Document Converter VB6 Production Integration Module
' Version 3.1.0 - Production Ready
' 
' This module provides complete document conversion functionality
' for VB6 applications using the UniversalConverter32.dll
'
' Usage:
'   1. Add this module to your VB6 project
'   2. Ensure UniversalConverter32.dll is in your application directory or System32
'   3. Ensure cli.py and Python dependencies are available
'   4. Call conversion functions as needed

Option Explicit

' ============================================================================
' DLL FUNCTION DECLARATIONS
' ============================================================================

' Core conversion function
Private Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String, _
     ByVal inputFormat As String, ByVal outputFormat As String) As Long

' System functions
Private Declare Function TestConnection Lib "UniversalConverter32.dll" () As Long
Private Declare Function GetVersion Lib "UniversalConverter32.dll" () As String
Private Declare Function GetLastError Lib "UniversalConverter32.dll" () As String

' Format information functions
Private Declare Function GetSupportedInputFormats Lib "UniversalConverter32.dll" () As String
Private Declare Function GetSupportedOutputFormats Lib "UniversalConverter32.dll" () As String

' Specific conversion functions
Private Declare Function ConvertPDFToText Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String) As Long
Private Declare Function ConvertPDFToMarkdown Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String) As Long
Private Declare Function ConvertDOCXToText Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String) As Long
Private Declare Function ConvertDOCXToMarkdown Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String) As Long
Private Declare Function ConvertMarkdownToHTML Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String) As Long
Private Declare Function ConvertHTMLToMarkdown Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String) As Long
Private Declare Function ConvertRTFToText Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String) As Long
Private Declare Function ConvertRTFToMarkdown Lib "UniversalConverter32.dll" _
    (ByVal inputFile As String, ByVal outputFile As String) As Long

' File information function
Private Declare Function GetFileInfo Lib "UniversalConverter32.dll" _
    (ByVal filePath As String, ByVal infoBuffer As String, ByVal bufferSize As Long) As Long

' ============================================================================
' CONSTANTS
' ============================================================================

' Return codes
Public Const UC_SUCCESS As Long = 1
Public Const UC_FAILURE As Long = 0
Public Const UC_ERROR As Long = -1

' Input formats
Public Const UC_FORMAT_PDF As String = "pdf"
Public Const UC_FORMAT_DOCX As String = "docx"
Public Const UC_FORMAT_TXT As String = "txt"
Public Const UC_FORMAT_HTML As String = "html"
Public Const UC_FORMAT_RTF As String = "rtf"
Public Const UC_FORMAT_MARKDOWN As String = "md"

' Output formats
Public Const UC_OUTPUT_TXT As String = "txt"
Public Const UC_OUTPUT_MARKDOWN As String = "md"
Public Const UC_OUTPUT_HTML As String = "html"
Public Const UC_OUTPUT_JSON As String = "json"

' ============================================================================
' PUBLIC INTERFACE FUNCTIONS
' ============================================================================

' Initialize the converter system
Public Function InitializeConverter() As Boolean
    On Error GoTo ErrorHandler
    
    ' Test if the DLL and backend are available
    Dim result As Long
    result = TestConnection()
    
    If result = UC_SUCCESS Then
        InitializeConverter = True
    Else
        InitializeConverter = False
        ' Log error for debugging
        Debug.Print "Converter initialization failed: " & GetLastError()
    End If
    
    Exit Function
    
ErrorHandler:
    InitializeConverter = False
    Debug.Print "Error initializing converter: " & Err.Description
End Function

' Get converter version
Public Function GetConverterVersion() As String
    On Error GoTo ErrorHandler
    
    GetConverterVersion = GetVersion()
    Exit Function
    
ErrorHandler:
    GetConverterVersion = "Unknown"
End Function

' Get last error message
Public Function GetLastErrorMessage() As String
    On Error GoTo ErrorHandler
    
    GetLastErrorMessage = GetLastError()
    Exit Function
    
ErrorHandler:
    GetLastErrorMessage = "Could not retrieve error message"
End Function

' ============================================================================
' GENERIC CONVERSION FUNCTION
' ============================================================================

' Convert any document to any supported format
Public Function ConvertDocumentFile(inputPath As String, outputPath As String, _
                                   Optional inputFormat As String = "", _
                                   Optional outputFormat As String = "") As Boolean
    On Error GoTo ErrorHandler
    
    ' Validate input parameters
    If Trim(inputPath) = "" Or Trim(outputPath) = "" Then
        Debug.Print "Invalid file paths provided"
        ConvertDocumentFile = False
        Exit Function
    End If
    
    ' Check if input file exists
    If Dir(inputPath) = "" Then
        Debug.Print "Input file not found: " & inputPath
        ConvertDocumentFile = False
        Exit Function
    End If
    
    ' Auto-detect formats if not specified
    If inputFormat = "" Then
        inputFormat = GetFileExtension(inputPath)
    End If
    
    If outputFormat = "" Then
        outputFormat = GetFileExtension(outputPath)
    End If
    
    ' Perform conversion
    Dim result As Long
    result = ConvertDocument(inputPath, outputPath, inputFormat, outputFormat)
    
    ConvertDocumentFile = (result = UC_SUCCESS)
    
    If Not ConvertDocumentFile Then
        Debug.Print "Conversion failed: " & GetLastError()
    End If
    
    Exit Function
    
ErrorHandler:
    ConvertDocumentFile = False
    Debug.Print "Error in ConvertDocumentFile: " & Err.Description
End Function

' ============================================================================
' SPECIFIC CONVERSION FUNCTIONS
' ============================================================================

' Convert PDF to text
Public Function PDFToText(pdfPath As String, txtPath As String) As Boolean
    On Error GoTo ErrorHandler
    
    If ValidateFiles(pdfPath, txtPath) Then
        PDFToText = (ConvertPDFToText(pdfPath, txtPath) = UC_SUCCESS)
    Else
        PDFToText = False
    End If
    
    Exit Function
    
ErrorHandler:
    PDFToText = False
    Debug.Print "Error in PDFToText: " & Err.Description
End Function

' Convert PDF to Markdown
Public Function PDFToMarkdown(pdfPath As String, mdPath As String) As Boolean
    On Error GoTo ErrorHandler
    
    If ValidateFiles(pdfPath, mdPath) Then
        PDFToMarkdown = (ConvertPDFToMarkdown(pdfPath, mdPath) = UC_SUCCESS)
    Else
        PDFToMarkdown = False
    End If
    
    Exit Function
    
ErrorHandler:
    PDFToMarkdown = False
    Debug.Print "Error in PDFToMarkdown: " & Err.Description
End Function

' Convert DOCX to text
Public Function DOCXToText(docxPath As String, txtPath As String) As Boolean
    On Error GoTo ErrorHandler
    
    If ValidateFiles(docxPath, txtPath) Then
        DOCXToText = (ConvertDOCXToText(docxPath, txtPath) = UC_SUCCESS)
    Else
        DOCXToText = False
    End If
    
    Exit Function
    
ErrorHandler:
    DOCXToText = False
    Debug.Print "Error in DOCXToText: " & Err.Description
End Function

' Convert DOCX to Markdown
Public Function DOCXToMarkdown(docxPath As String, mdPath As String) As Boolean
    On Error GoTo ErrorHandler
    
    If ValidateFiles(docxPath, mdPath) Then
        DOCXToMarkdown = (ConvertDOCXToMarkdown(docxPath, mdPath) = UC_SUCCESS)
    Else
        DOCXToMarkdown = False
    End If
    
    Exit Function
    
ErrorHandler:
    DOCXToMarkdown = False
    Debug.Print "Error in DOCXToMarkdown: " & Err.Description
End Function

' Convert Markdown to HTML
Public Function MarkdownToHTML(mdPath As String, htmlPath As String) As Boolean
    On Error GoTo ErrorHandler
    
    If ValidateFiles(mdPath, htmlPath) Then
        MarkdownToHTML = (ConvertMarkdownToHTML(mdPath, htmlPath) = UC_SUCCESS)
    Else
        MarkdownToHTML = False
    End If
    
    Exit Function
    
ErrorHandler:
    MarkdownToHTML = False
    Debug.Print "Error in MarkdownToHTML: " & Err.Description
End Function

' Convert HTML to Markdown
Public Function HTMLToMarkdown(htmlPath As String, mdPath As String) As Boolean
    On Error GoTo ErrorHandler
    
    If ValidateFiles(htmlPath, mdPath) Then
        HTMLToMarkdown = (ConvertHTMLToMarkdown(htmlPath, mdPath) = UC_SUCCESS)
    Else
        HTMLToMarkdown = False
    End If
    
    Exit Function
    
ErrorHandler:
    HTMLToMarkdown = False
    Debug.Print "Error in HTMLToMarkdown: " & Err.Description
End Function

' Convert RTF to text
Public Function RTFToText(rtfPath As String, txtPath As String) As Boolean
    On Error GoTo ErrorHandler
    
    If ValidateFiles(rtfPath, txtPath) Then
        RTFToText = (ConvertRTFToText(rtfPath, txtPath) = UC_SUCCESS)
    Else
        RTFToText = False
    End If
    
    Exit Function
    
ErrorHandler:
    RTFToText = False
    Debug.Print "Error in RTFToText: " & Err.Description
End Function

' Convert RTF to Markdown
Public Function RTFToMarkdown(rtfPath As String, mdPath As String) As Boolean
    On Error GoTo ErrorHandler
    
    If ValidateFiles(rtfPath, mdPath) Then
        RTFToMarkdown = (ConvertRTFToMarkdown(rtfPath, mdPath) = UC_SUCCESS)
    Else
        RTFToMarkdown = False
    End If
    
    Exit Function
    
ErrorHandler:
    RTFToMarkdown = False
    Debug.Print "Error in RTFToMarkdown: " & Err.Description
End Function

' ============================================================================
' BATCH CONVERSION FUNCTIONS
' ============================================================================

' Convert all files in a directory
Public Function ConvertDirectory(inputDir As String, outputDir As String, _
                                inputFormat As String, outputFormat As String) As Long
    On Error GoTo ErrorHandler
    
    Dim fileCount As Long
    Dim successCount As Long
    Dim fileName As String
    Dim inputPath As String
    Dim outputPath As String
    Dim baseName As String
    
    fileCount = 0
    successCount = 0
    
    ' Ensure directories exist
    If Dir(inputDir, vbDirectory) = "" Then
        Debug.Print "Input directory not found: " & inputDir
        ConvertDirectory = 0
        Exit Function
    End If
    
    ' Create output directory if it doesn't exist
    If Dir(outputDir, vbDirectory) = "" Then
        MkDir outputDir
    End If
    
    ' Process all files with the specified input format
    fileName = Dir(inputDir & "\*." & inputFormat)
    
    Do While fileName <> ""
        inputPath = inputDir & "\" & fileName
        baseName = Left(fileName, InStrRev(fileName, ".") - 1)
        outputPath = outputDir & "\" & baseName & "." & outputFormat
        
        fileCount = fileCount + 1
        
        If ConvertDocumentFile(inputPath, outputPath, inputFormat, outputFormat) Then
            successCount = successCount + 1
            Debug.Print "Converted: " & fileName
        Else
            Debug.Print "Failed: " & fileName & " - " & GetLastError()
        End If
        
        fileName = Dir  ' Get next file
    Loop
    
    Debug.Print "Batch conversion complete: " & successCount & " of " & fileCount & " files converted"
    ConvertDirectory = successCount
    
    Exit Function
    
ErrorHandler:
    Debug.Print "Error in ConvertDirectory: " & Err.Description
    ConvertDirectory = successCount
End Function

' ============================================================================
' UTILITY FUNCTIONS
' ============================================================================

' Validate input and output file paths
Private Function ValidateFiles(inputPath As String, outputPath As String) As Boolean
    On Error GoTo ErrorHandler
    
    ' Check input path
    If Trim(inputPath) = "" Then
        Debug.Print "Empty input path"
        ValidateFiles = False
        Exit Function
    End If
    
    ' Check output path
    If Trim(outputPath) = "" Then
        Debug.Print "Empty output path"
        ValidateFiles = False
        Exit Function
    End If
    
    ' Check if input file exists
    If Dir(inputPath) = "" Then
        Debug.Print "Input file not found: " & inputPath
        ValidateFiles = False
        Exit Function
    End If
    
    ValidateFiles = True
    Exit Function
    
ErrorHandler:
    ValidateFiles = False
    Debug.Print "Error validating files: " & Err.Description
End Function

' Extract file extension from path
Private Function GetFileExtension(filePath As String) As String
    On Error GoTo ErrorHandler
    
    Dim lastDot As Long
    lastDot = InStrRev(filePath, ".")
    
    If lastDot > 0 Then
        GetFileExtension = LCase(Mid(filePath, lastDot + 1))
    Else
        GetFileExtension = ""
    End If
    
    Exit Function
    
ErrorHandler:
    GetFileExtension = ""
End Function

' Get file size information
Public Function GetDocumentFileInfo(filePath As String) As String
    On Error GoTo ErrorHandler
    
    Dim buffer As String
    Dim result As Long
    
    buffer = Space(512)  ' Allocate buffer
    result = GetFileInfo(filePath, buffer, 512)
    
    If result = UC_SUCCESS Then
        GetDocumentFileInfo = Trim(buffer)
    Else
        GetDocumentFileInfo = "File information not available"
    End If
    
    Exit Function
    
ErrorHandler:
    GetDocumentFileInfo = "Error getting file info: " & Err.Description
End Function

' Get supported formats
Public Function GetInputFormats() As String
    On Error GoTo ErrorHandler
    
    GetInputFormats = GetSupportedInputFormats()
    Exit Function
    
ErrorHandler:
    GetInputFormats = "pdf,docx,txt,html,rtf,md"
End Function

Public Function GetOutputFormats() As String
    On Error GoTo ErrorHandler
    
    GetOutputFormats = GetSupportedOutputFormats()
    Exit Function
    
ErrorHandler:
    GetOutputFormats = "txt,md,html,json"
End Function

' ============================================================================
' EXAMPLE USAGE FUNCTION
' ============================================================================

' Demonstration of how to use the converter
Public Sub TestConverter()
    On Error GoTo ErrorHandler
    
    Debug.Print "=== Universal Document Converter Test ==="
    Debug.Print "Version: " & GetConverterVersion()
    Debug.Print ""
    
    ' Initialize converter
    If Not InitializeConverter() Then
        MsgBox "Failed to initialize converter: " & GetLastErrorMessage(), vbCritical
        Exit Sub
    End If
    
    Debug.Print "✓ Converter initialized successfully"
    Debug.Print "Supported input formats: " & GetInputFormats()
    Debug.Print "Supported output formats: " & GetOutputFormats()
    Debug.Print ""
    
    ' Example conversions (modify paths as needed)
    Dim testFile As String
    Dim outputFile As String
    
    ' Test 1: PDF to Text
    testFile = "C:\temp\test.pdf"
    outputFile = "C:\temp\test.txt"
    
    If Dir(testFile) <> "" Then
        If PDFToText(testFile, outputFile) Then
            Debug.Print "✓ PDF to Text conversion successful"
        Else
            Debug.Print "✗ PDF to Text conversion failed: " & GetLastErrorMessage()
        End If
    Else
        Debug.Print "Test PDF file not found: " & testFile
    End If
    
    ' Test 2: Generic conversion
    testFile = "C:\temp\document.docx"
    outputFile = "C:\temp\document.md"
    
    If Dir(testFile) <> "" Then
        If ConvertDocumentFile(testFile, outputFile) Then
            Debug.Print "✓ Generic conversion successful"
        Else
            Debug.Print "✗ Generic conversion failed: " & GetLastErrorMessage()
        End If
    Else
        Debug.Print "Test DOCX file not found: " & testFile
    End If
    
    Debug.Print ""
    Debug.Print "=== Test Complete ==="
    
    Exit Sub
    
ErrorHandler:
    Debug.Print "Error in TestConverter: " & Err.Description
End Sub