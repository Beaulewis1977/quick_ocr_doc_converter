VERSION 5.00
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
    txtInput.Text = "C:\temp\test.md"
    txtOutput.Text = "C:\temp\test.rtf"
End Sub
