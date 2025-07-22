' VB6 Example - UniversalConverter32 Integration
' This example shows how to use the OCR Document Converter from VB6

Option Explicit

' API declarations for calling Python DLL
Private Declare Function ShellExecute Lib "shell32.dll" Alias "ShellExecuteA" _
    (ByVal hwnd As Long, ByVal lpOperation As String, ByVal lpFile As String, _
     ByVal lpParameters As String, ByVal lpDirectory As String, ByVal nShowCmd As Long) As Long

' Constants
Private Const SW_HIDE = 0
Private Const SW_SHOW = 1

' Form with conversion functionality
Private Sub Form_Load()
    Me.Caption = "OCR Document Converter v3.1.0 - VB6 Integration"
    
    ' Create UI elements
    Dim lblInput As Label
    Set lblInput = Controls.Add("VB.Label", "lblInput")
    lblInput.Caption = "Input File:"
    lblInput.Move 120, 120, 1500, 240
    lblInput.Visible = True
    
    Dim txtInput As TextBox
    Set txtInput = Controls.Add("VB.TextBox", "txtInput")
    txtInput.Move 120, 360, 4000, 300
    txtInput.Text = "C:\example\input.pdf"
    txtInput.Visible = True
    
    Dim lblOutput As Label
    Set lblOutput = Controls.Add("VB.Label", "lblOutput")
    lblOutput.Caption = "Output File:"
    lblOutput.Move 120, 800, 1500, 240
    lblOutput.Visible = True
    
    Dim txtOutput As TextBox
    Set txtOutput = Controls.Add("VB.TextBox", "txtOutput")
    txtOutput.Move 120, 1040, 4000, 300
    txtOutput.Text = "C:\example\output.txt"
    txtOutput.Visible = True
    
    Dim lblFormat As Label
    Set lblFormat = Controls.Add("VB.Label", "lblFormat")
    lblFormat.Caption = "Output Format:"
    lblFormat.Move 120, 1480, 1500, 240
    lblFormat.Visible = True
    
    Dim cmbFormat As ComboBox
    Set cmbFormat = Controls.Add("VB.ComboBox", "cmbFormat")
    cmbFormat.Move 120, 1720, 2000, 300
    cmbFormat.AddItem "txt"
    cmbFormat.AddItem "docx"
    cmbFormat.AddItem "pdf"
    cmbFormat.AddItem "html"
    cmbFormat.AddItem "markdown"
    cmbFormat.ListIndex = 0
    cmbFormat.Visible = True
    
    Dim btnConvert As CommandButton
    Set btnConvert = Controls.Add("VB.CommandButton", "btnConvert")
    btnConvert.Caption = "Convert Document"
    btnConvert.Move 120, 2160, 2000, 400
    btnConvert.Visible = True
    
    Dim btnConvertOCR As CommandButton
    Set btnConvertOCR = Controls.Add("VB.CommandButton", "btnConvertOCR")
    btnConvertOCR.Caption = "Convert with OCR"
    btnConvertOCR.Move 2240, 2160, 2000, 400
    btnConvertOCR.Visible = True
    
    Dim txtLog As TextBox
    Set txtLog = Controls.Add("VB.TextBox", "txtLog")
    txtLog.Move 120, 2680, 6000, 1500
    txtLog.MultiLine = True
    txtLog.ScrollBars = vbVertical
    txtLog.Text = "Ready to convert documents..." & vbCrLf
    txtLog.Visible = True
    
    ' Resize form
    Me.Width = 6500
    Me.Height = 4800
End Sub

' Event handler for Convert button
Private Sub btnConvert_Click()
    Dim inputFile As String
    Dim outputFile As String
    Dim outputFormat As String
    
    inputFile = Me.Controls("txtInput").Text
    outputFile = Me.Controls("txtOutput").Text
    outputFormat = Me.Controls("cmbFormat").Text
    
    ' Log the operation
    Me.Controls("txtLog").Text = Me.Controls("txtLog").Text & _
        "Starting conversion..." & vbCrLf & _
        "Input: " & inputFile & vbCrLf & _
        "Output: " & outputFile & vbCrLf & _
        "Format: " & outputFormat & vbCrLf
    
    ' Call the converter
    Dim result As Long
    result = CallUniversalConverter(inputFile, outputFile, outputFormat, False)
    
    If result = 1 Then
        Me.Controls("txtLog").Text = Me.Controls("txtLog").Text & _
            "✅ Conversion successful!" & vbCrLf & vbCrLf
    Else
        Me.Controls("txtLog").Text = Me.Controls("txtLog").Text & _
            "❌ Conversion failed!" & vbCrLf & vbCrLf
    End If
End Sub

' Event handler for Convert with OCR button
Private Sub btnConvertOCR_Click()
    Dim inputFile As String
    Dim outputFile As String
    Dim outputFormat As String
    
    inputFile = Me.Controls("txtInput").Text
    outputFile = Me.Controls("txtOutput").Text
    outputFormat = Me.Controls("cmbFormat").Text
    
    ' Log the operation
    Me.Controls("txtLog").Text = Me.Controls("txtLog").Text & _
        "Starting OCR conversion..." & vbCrLf & _
        "Input: " & inputFile & vbCrLf & _
        "Output: " & outputFile & vbCrLf & _
        "Format: " & outputFormat & vbCrLf
    
    ' Call the converter with OCR
    Dim result As Long
    result = CallUniversalConverter(inputFile, outputFile, outputFormat, True)
    
    If result = 1 Then
        Me.Controls("txtLog").Text = Me.Controls("txtLog").Text & _
            "✅ OCR conversion successful!" & vbCrLf & vbCrLf
    Else
        Me.Controls("txtLog").Text = Me.Controls("txtLog").Text & _
            "❌ OCR conversion failed!" & vbCrLf & vbCrLf
    End If
End Sub

' Function to call the UniversalConverter32
Private Function CallUniversalConverter(inputPath As String, outputPath As String, _
                                       outputFormat As String, useOCR As Boolean) As Long
    Dim pythonPath As String
    Dim scriptPath As String
    Dim parameters As String
    Dim result As Long
    
    ' Get the path to the Python script
    scriptPath = App.Path & "\vb6_vfp9_integration\UniversalConverter32.py"
    pythonPath = "python"
    
    ' Build parameters
    parameters = """" & inputPath & """ """ & outputPath & """ " & outputFormat
    
    If useOCR Then
        parameters = parameters & " --ocr --lang eng"
    End If
    
    ' Execute the Python script
    result = ShellExecute(0, "open", pythonPath, scriptPath & " " & parameters, App.Path, SW_HIDE)
    
    ' Wait a moment for execution
    Dim startTime As Single
    startTime = Timer
    Do While Timer < startTime + 2  ' Wait 2 seconds
        DoEvents
    Loop
    
    ' Check if output file was created (simple success check)
    If Dir(outputPath) <> "" Then
        CallUniversalConverter = 1  ' Success
    Else
        CallUniversalConverter = 0  ' Failure
    End If
End Function

' Helper function to get file version info
Private Function GetConverterVersion() As String
    ' This would call the Python script to get version
    GetConverterVersion = "3.1.0"
End Function

' Helper function to check if OCR is available
Private Function IsOCRAvailable() As Boolean
    ' This would call the Python script to check OCR availability
    IsOCRAvailable = True  ' Assume available for this example
End Function