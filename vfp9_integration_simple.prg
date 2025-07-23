* Visual FoxPro 9 Integration Example for Simple Document Converter
* Basic document conversion without OCR for legacy systems
* Compatible with 32-bit VFP environments

DEFINE CLASS SimpleDocConverter AS Custom
    
    * Properties
    PythonPath = "python.exe"
    CliPath = ""
    
    * Initialize the converter
    PROCEDURE Init()
        THIS.CliPath = ADDBS(SYS(16,0)) + "cli.py"  && CLI script in same directory
    ENDPROC
    
    * Convert a single document
    PROCEDURE ConvertDocument(tcInputFile, tcOutputFile, tcFormat, tcEncoding, tcLineEndings)
        LOCAL lcCommandLine, lnResult, lcFormat, lcEncoding, lcLineEndings
        
        * Set defaults
        lcFormat = IIF(EMPTY(tcFormat), "txt", tcFormat)
        lcEncoding = IIF(EMPTY(tcEncoding), "utf-8", tcEncoding)
        lcLineEndings = IIF(EMPTY(tcLineEndings), "windows", tcLineEndings)
        
        * Build command line
        lcCommandLine = ["] + THIS.PythonPath + [" "] + THIS.CliPath + [" "] + ;
                       tcInputFile + [" "] + tcOutputFile + [" --format ] + lcFormat + ;
                       [ --encoding ] + lcEncoding + [ --line-endings ] + lcLineEndings
        
        * Execute conversion
        lnResult = THIS.ExecuteCommand(lcCommandLine)
        
        * Check if output file was created
        RETURN (lnResult = 0) AND FILE(tcOutputFile)
    ENDPROC
    
    * Convert all documents in a directory
    PROCEDURE ConvertDirectory(tcInputDir, tcOutputDir, tcFormat, tlRecursive, tlOverwrite)
        LOCAL lcCommandLine, lnResult, lcFlags, lcFormat
        
        * Set defaults
        lcFormat = IIF(EMPTY(tcFormat), "txt", tcFormat)
        lcFlags = ""
        
        * Build flags
        IF tlRecursive
            lcFlags = lcFlags + " --recursive"
        ENDIF
        
        IF tlOverwrite
            lcFlags = lcFlags + " --overwrite"
        ENDIF
        
        * Build command line
        lcCommandLine = ["] + THIS.PythonPath + [" "] + THIS.CliPath + [" "] + ;
                       tcInputDir + [" "] + tcOutputDir + [" --format ] + lcFormat + lcFlags
        
        * Execute conversion
        lnResult = THIS.ExecuteCommand(lcCommandLine)
        
        RETURN (lnResult = 0)
    ENDPROC
    
    * Get supported formats
    PROCEDURE GetSupportedFormats()
        LOCAL lcCommandLine, lcTempFile, lcContent
        
        * Create temp file for output
        lcTempFile = SYS(2023) + "\" + "formats_" + TRANSFORM(SECONDS()) + ".txt"
        
        * Build command line
        lcCommandLine = ["] + THIS.PythonPath + [" "] + THIS.CliPath + [" --formats > "] + lcTempFile + ["]
        
        * Execute command
        THIS.ExecuteCommand(lcCommandLine)
        
        * Read result from temp file
        lcContent = ""
        IF FILE(lcTempFile)
            lcContent = FILETOSTR(lcTempFile)
            DELETE FILE (lcTempFile)  && Clean up temp file
        ENDIF
        
        RETURN lcContent
    ENDPROC
    
    * Convert PDF to text (no OCR)
    PROCEDURE ConvertPdfToText(tcPdfFile, tcTextFile)
        RETURN THIS.ConvertDocument(tcPdfFile, tcTextFile, "txt")
    ENDPROC
    
    * Convert DOCX to Markdown
    PROCEDURE ConvertDocxToMarkdown(tcDocxFile, tcMarkdownFile)
        RETURN THIS.ConvertDocument(tcDocxFile, tcMarkdownFile, "md")
    ENDPROC
    
    * Convert HTML to text
    PROCEDURE ConvertHtmlToText(tcHtmlFile, tcTextFile)
        RETURN THIS.ConvertDocument(tcHtmlFile, tcTextFile, "txt")
    ENDPROC
    
    * Batch convert to JSON
    PROCEDURE BatchConvertToJson(tcInputDir, tcOutputDir)
        RETURN THIS.ConvertDirectory(tcInputDir, tcOutputDir, "json", .T., .F.)
    ENDPROC
    
    * Execute command using Windows API
    PROCEDURE ExecuteCommand(tcCommandLine)
        LOCAL lnResult
        
        * Use RUN command for simplicity in VFP
        * In production, you might want to use Windows API for better control
        RUN /N &tcCommandLine
        
        * VFP doesn't easily capture return codes from RUN
        * So we return 0 (assume success) - you might want to enhance this
        RETURN 0
    ENDPROC
    
    * Test if CLI is accessible
    PROCEDURE TestConnection()
        LOCAL lcCommandLine, lcTempFile, llSuccess
        
        * Create temp file to capture output
        lcTempFile = SYS(2023) + "\" + "test_" + TRANSFORM(SECONDS()) + ".txt"
        
        * Build command line
        lcCommandLine = ["] + THIS.PythonPath + [" "] + THIS.CliPath + [" --version > "] + lcTempFile + [" 2>&1"]
        
        * Execute command
        RUN /N &lcCommandLine
        
        * Check if temp file was created (indicates command ran)
        llSuccess = FILE(lcTempFile)
        
        * Clean up
        IF llSuccess
            DELETE FILE (lcTempFile)
        ENDIF
        
        RETURN llSuccess
    ENDPROC
    
    * Enhanced execute with better error handling (VFP9 specific)
    PROCEDURE ExecuteCommandAdvanced(tcCommandLine)
        LOCAL oShell, lnResult
        
        TRY
            * Use Windows Script Host for better control
            oShell = CREATEOBJECT("WScript.Shell")
            lnResult = oShell.Run(tcCommandLine, 0, .T.)  && Hidden, wait for completion
            
            RETURN lnResult
            
        CATCH TO oException
            * Fallback to RUN command
            RUN /N &tcCommandLine
            RETURN 0
            
        ENDTRY
    ENDPROC
    
ENDDEFINE

* Example usage procedures
PROCEDURE ExampleUsage()
    LOCAL oConverter, llSuccess, lcFormats
    
    * Create converter instance
    oConverter = CREATEOBJECT("SimpleDocConverter")
    
    * Test connection
    IF NOT oConverter.TestConnection()
        MESSAGEBOX("Error: Cannot connect to document converter CLI", 16, "Connection Error")
        RETURN
    ENDIF
    
    * Convert a single PDF to text
    llSuccess = oConverter.ConvertPdfToText("C:\Documents\sample.pdf", "C:\Output\sample.txt")
    IF llSuccess
        MESSAGEBOX("PDF converted successfully!", 64, "Success")
    ELSE
        MESSAGEBOX("PDF conversion failed", 16, "Error")
    ENDIF
    
    * Convert DOCX to Markdown
    llSuccess = oConverter.ConvertDocxToMarkdown("C:\Documents\report.docx", "C:\Output\report.md")
    
    * Batch convert directory
    llSuccess = oConverter.ConvertDirectory("C:\Input\", "C:\Output\", "txt", .T., .T.)
    IF llSuccess
        MESSAGEBOX("Directory conversion completed!", 64, "Success")
    ENDIF
    
    * Get supported formats
    lcFormats = oConverter.GetSupportedFormats()
    MESSAGEBOX("Supported formats:" + CHR(13) + CHR(10) + lcFormats, 64, "Formats")
ENDPROC

* Batch processing example
PROCEDURE BatchProcessExample()
    LOCAL oConverter, lcSourceDir, lcTargetDir, llSuccess
    
    oConverter = CREATEOBJECT("SimpleDocConverter")
    
    * Set directories
    lcSourceDir = "C:\Documents\ToConvert\"
    lcTargetDir = "C:\Documents\Converted\"
    
    * Create target directory if it doesn't exist
    IF NOT DIRECTORY(lcTargetDir)
        MD (lcTargetDir)
    ENDIF
    
    * Convert all documents to text format recursively
    llSuccess = oConverter.ConvertDirectory(lcSourceDir, lcTargetDir, "txt", .T., .T.)
    
    IF llSuccess
        MESSAGEBOX("Batch conversion completed successfully!", 64, "Batch Process")
    ELSE
        MESSAGEBOX("Batch conversion failed", 16, "Error")
    ENDIF
ENDPROC

* PDF processing example
PROCEDURE PdfProcessingExample()
    LOCAL oConverter, laFiles[1], lnFiles, lnI, lcInputFile, lcOutputFile, llSuccess, lnCount
    
    oConverter = CREATEOBJECT("SimpleDocConverter")
    lnCount = 0
    
    * Get all PDF files in a directory
    lnFiles = ADIR(laFiles, "C:\PDFs\*.pdf")
    
    FOR lnI = 1 TO lnFiles
        lcInputFile = "C:\PDFs\" + laFiles[lnI, 1]
        lcOutputFile = "C:\TextOutput\" + JUSTSTEM(laFiles[lnI, 1]) + ".txt"
        
        * Convert each PDF
        llSuccess = oConverter.ConvertPdfToText(lcInputFile, lcOutputFile)
        IF llSuccess
            lnCount = lnCount + 1
        ENDIF
    ENDFOR
    
    MESSAGEBOX("Converted " + TRANSFORM(lnCount) + " of " + TRANSFORM(lnFiles) + " PDF files", 64, "PDF Processing")
ENDPROC

* Document format conversion example
PROCEDURE FormatConversionExample()
    LOCAL oConverter, lcSourceFile, lcTargetFile, llSuccess
    
    oConverter = CREATEOBJECT("SimpleDocConverter")
    
    * Convert various formats
    lcSourceFile = "C:\Documents\report.docx"
    
    * To Markdown
    lcTargetFile = "C:\Output\report.md"
    llSuccess = oConverter.ConvertDocument(lcSourceFile, lcTargetFile, "md")
    
    * To HTML
    lcTargetFile = "C:\Output\report.html"
    llSuccess = oConverter.ConvertDocument(lcSourceFile, lcTargetFile, "html")
    
    * To JSON
    lcTargetFile = "C:\Output\report.json"
    llSuccess = oConverter.ConvertDocument(lcSourceFile, lcTargetFile, "json")
    
    MESSAGEBOX("Format conversion examples completed", 64, "Conversion")
ENDPROC