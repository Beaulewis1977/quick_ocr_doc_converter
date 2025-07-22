Attribute VB_Name = "UniversalConverterModule"
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
        testResult = ConvertMarkdownToRTF("C:\temp\test.md", "C:\temp\test.rtf")
        
        If testResult Then
            MsgBox "Test conversion successful!"
        Else
            MsgBox "Test conversion failed!"
        End If
    Else
        MsgBox "Universal Document Converter is not available!"
    End If
End Sub
