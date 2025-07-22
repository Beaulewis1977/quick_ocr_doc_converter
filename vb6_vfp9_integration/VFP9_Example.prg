* VFP9 Example - UniversalConverter32 Integration
* This example shows how to use the OCR Document Converter from Visual FoxPro 9

* Main form class for document conversion
DEFINE CLASS frmConverter AS FORM
    HEIGHT = 450
    WIDTH = 600
    AUTOCENTER = .T.
    CAPTION = "OCR Document Converter v3.1.0 - VFP9 Integration"
    SHOWWINDOW = 2
    MAXBUTTON = .F.
    
    * Form properties
    ADD OBJECT lblInput AS LABEL WITH ;
        TOP = 20, LEFT = 20, WIDTH = 120, HEIGHT = 20, ;
        CAPTION = "Input File:"
    
    ADD OBJECT txtInput AS TEXTBOX WITH ;
        TOP = 45, LEFT = 20, WIDTH = 400, HEIGHT = 25, ;
        VALUE = "C:\example\input.pdf"
    
    ADD OBJECT btnBrowseInput AS COMMANDBUTTON WITH ;
        TOP = 43, LEFT = 430, WIDTH = 80, HEIGHT = 30, ;
        CAPTION = "Browse..."
    
    ADD OBJECT lblOutput AS LABEL WITH ;
        TOP = 85, LEFT = 20, WIDTH = 120, HEIGHT = 20, ;
        CAPTION = "Output File:"
    
    ADD OBJECT txtOutput AS TEXTBOX WITH ;
        TOP = 110, LEFT = 20, WIDTH = 400, HEIGHT = 25, ;
        VALUE = "C:\example\output.txt"
    
    ADD OBJECT btnBrowseOutput AS COMMANDBUTTON WITH ;
        TOP = 108, LEFT = 430, WIDTH = 80, HEIGHT = 30, ;
        CAPTION = "Browse..."
    
    ADD OBJECT lblFormat AS LABEL WITH ;
        TOP = 150, LEFT = 20, WIDTH = 120, HEIGHT = 20, ;
        CAPTION = "Output Format:"
    
    ADD OBJECT cmbFormat AS COMBOBOX WITH ;
        TOP = 175, LEFT = 20, WIDTH = 150, HEIGHT = 25, ;
        STYLE = 2, ;
        ROWSOURCETYPE = 1, ;
        ROWSOURCE = "txt,docx,pdf,html,markdown", ;
        VALUE = "txt"
    
    ADD OBJECT btnConvert AS COMMANDBUTTON WITH ;
        TOP = 220, LEFT = 20, WIDTH = 120, HEIGHT = 35, ;
        CAPTION = "Convert"
    
    ADD OBJECT btnConvertOCR AS COMMANDBUTTON WITH ;
        TOP = 220, LEFT = 150, WIDTH = 120, HEIGHT = 35, ;
        CAPTION = "Convert with OCR"
    
    ADD OBJECT btnCheckOCR AS COMMANDBUTTON WITH ;
        TOP = 220, LEFT = 280, WIDTH = 100, HEIGHT = 35, ;
        CAPTION = "Check OCR"
    
    ADD OBJECT edtLog AS EDITBOX WITH ;
        TOP = 270, LEFT = 20, WIDTH = 560, HEIGHT = 150, ;
        SCROLLBARS = 2, ;
        READONLY = .T., ;
        VALUE = "Ready to convert documents..." + CHR(13)
    
    * Form initialization
    PROCEDURE INIT
        THIS.AddLog("OCR Document Converter v3.1.0 - VFP9 Integration Ready")
        THIS.AddLog("Python path: " + THIS.GetPythonPath())
        THIS.AddLog("")
    ENDPROC
    
    * Browse for input file
    PROCEDURE btnBrowseInput.CLICK
        LOCAL lcFile
        lcFile = GETFILE("PDF,JPG,PNG,TIFF,BMP", "Select Input File")
        IF !EMPTY(lcFile)
            THISFORM.txtInput.VALUE = lcFile
        ENDIF
    ENDPROC
    
    * Browse for output file
    PROCEDURE btnBrowseOutput.CLICK
        LOCAL lcFile
        lcFile = PUTFILE("Output File", THISFORM.txtOutput.VALUE)
        IF !EMPTY(lcFile)
            THISFORM.txtOutput.VALUE = lcFile
        ENDIF
    ENDPROC
    
    * Convert document without OCR
    PROCEDURE btnConvert.CLICK
        LOCAL lcInput, lcOutput, lcFormat, lnResult
        
        lcInput = ALLTRIM(THIS.txtInput.VALUE)
        lcOutput = ALLTRIM(THIS.txtOutput.VALUE)
        lcFormat = ALLTRIM(THIS.cmbFormat.VALUE)
        
        IF EMPTY(lcInput) OR EMPTY(lcOutput)
            MESSAGEBOX("Please specify both input and output files.", 48, "Error")
            RETURN
        ENDIF
        
        THIS.AddLog("Starting conversion...")
        THIS.AddLog("Input: " + lcInput)
        THIS.AddLog("Output: " + lcOutput)
        THIS.AddLog("Format: " + lcFormat)
        
        lnResult = THIS.CallUniversalConverter(lcInput, lcOutput, lcFormat, .F.)
        
        IF lnResult = 1
            THIS.AddLog("✅ Conversion successful!")
            MESSAGEBOX("Conversion completed successfully!", 64, "Success")
        ELSE
            THIS.AddLog("❌ Conversion failed!")
            MESSAGEBOX("Conversion failed. Check the log for details.", 16, "Error")
        ENDIF
        
        THIS.AddLog("")
    ENDPROC
    
    * Convert document with OCR
    PROCEDURE btnConvertOCR.CLICK
        LOCAL lcInput, lcOutput, lcFormat, lnResult
        
        lcInput = ALLTRIM(THIS.txtInput.VALUE)
        lcOutput = ALLTRIM(THIS.txtOutput.VALUE)
        lcFormat = ALLTRIM(THIS.cmbFormat.VALUE)
        
        IF EMPTY(lcInput) OR EMPTY(lcOutput)
            MESSAGEBOX("Please specify both input and output files.", 48, "Error")
            RETURN
        ENDIF
        
        THIS.AddLog("Starting OCR conversion...")
        THIS.AddLog("Input: " + lcInput)
        THIS.AddLog("Output: " + lcOutput)
        THIS.AddLog("Format: " + lcFormat)
        
        lnResult = THIS.CallUniversalConverter(lcInput, lcOutput, lcFormat, .T.)
        
        IF lnResult = 1
            THIS.AddLog("✅ OCR conversion successful!")
            MESSAGEBOX("OCR conversion completed successfully!", 64, "Success")
        ELSE
            THIS.AddLog("❌ OCR conversion failed!")
            MESSAGEBOX("OCR conversion failed. Check the log for details.", 16, "Error")
        ENDIF
        
        THIS.AddLog("")
    ENDPROC
    
    * Check OCR availability
    PROCEDURE btnCheckOCR.CLICK
        LOCAL lcCommand, lcResult
        
        THIS.AddLog("Checking OCR availability...")
        
        lcCommand = [python "vb6_vfp9_integration\UniversalConverter32.py"]
        lcResult = THIS.ExecuteCommand(lcCommand)
        
        THIS.AddLog("OCR Status: " + lcResult)
        THIS.AddLog("")
    ENDPROC
    
    * Call the Universal Converter
    FUNCTION CallUniversalConverter(tcInput, tcOutput, tcFormat, tlUseOCR)
        LOCAL lcCommand, lcParameters, lcResult, lnResult
        
        * Build the command
        lcCommand = [python "vb6_vfp9_integration\UniversalConverter32.py"]
        lcParameters = ["] + tcInput + [" "] + tcOutput + [" ] + tcFormat
        
        IF tlUseOCR
            lcParameters = lcParameters + [ --ocr --lang eng]
        ENDIF
        
        lcCommand = lcCommand + [ ] + lcParameters
        
        THIS.AddLog("Executing: " + lcCommand)
        
        * Execute the command
        lcResult = THIS.ExecuteCommand(lcCommand)
        
        * Check if output file exists (simple success check)
        IF FILE(tcOutput)
            lnResult = 1  && Success
        ELSE
            lnResult = 0  && Failure
        ENDIF
        
        RETURN lnResult
    ENDFUNC
    
    * Execute a shell command and capture output
    FUNCTION ExecuteCommand(tcCommand)
        LOCAL oWsh, oExec, lcResult
        
        TRY
            oWsh = CREATEOBJECT("WScript.Shell")
            oExec = oWsh.Exec(tcCommand)
            
            * Wait for completion (simple approach)
            DO WHILE oExec.Status = 0
                INKEY(0.1)
            ENDDO
            
            lcResult = oExec.StdOut.ReadAll()
            IF EMPTY(lcResult)
                lcResult = oExec.StdErr.ReadAll()
            ENDIF
            
        CATCH TO oError
            lcResult = "Error: " + oError.Message
        ENDTRY
        
        RETURN lcResult
    ENDFUNC
    
    * Get Python path
    FUNCTION GetPythonPath
        LOCAL lcPath
        lcPath = THIS.ExecuteCommand("where python")
        IF "python" $ LOWER(lcPath)
            RETURN STRTRAN(lcPath, CHR(13) + CHR(10), "")
        ELSE
            RETURN "Python not found in PATH"
        ENDIF
    ENDFUNC
    
    * Add message to log
    PROCEDURE AddLog(tcMessage)
        THIS.edtLog.VALUE = THIS.edtLog.VALUE + DTOC(DATE()) + " " + ;
                           TIME() + " - " + tcMessage + CHR(13)
        
        * Scroll to bottom
        THIS.edtLog.SELSTART = LEN(THIS.edtLog.VALUE)
    ENDPROC
    
ENDDEFINE

* Helper functions for procedural programming style

* Convert document function (procedural interface)
FUNCTION ConvertDocument(tcInput, tcOutput, tcFormat)
    LOCAL oConverter, lnResult
    
    oConverter = CREATEOBJECT("UniversalConverter32")
    lnResult = oConverter.ConvertDocument(tcInput, tcOutput, tcFormat)
    
    RETURN lnResult
ENDFUNC

* Convert document with OCR function (procedural interface)
FUNCTION ConvertDocumentWithOCR(tcInput, tcOutput, tcFormat, tcLanguage)
    LOCAL oConverter, lnResult
    
    oConverter = CREATEOBJECT("UniversalConverter32")
    lnResult = oConverter.ConvertDocumentWithOCR(tcInput, tcOutput, tcFormat, tcLanguage)
    
    RETURN lnResult
ENDFUNC

* Check OCR availability function
FUNCTION IsOCRAvailable()
    LOCAL oConverter, lnResult
    
    oConverter = CREATEOBJECT("UniversalConverter32")
    lnResult = oConverter.IsOCRAvailable()
    
    RETURN lnResult
ENDFUNC

* Main program entry point
IF PROGRAM() = "VFP9_EXAMPLE"
    * Create and show the form
    PUBLIC oConverterForm
    oConverterForm = CREATEOBJECT("frmConverter")
    oConverterForm.SHOW(1)  && Modal
ENDIF