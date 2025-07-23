*!* Universal Document Converter VFP9 Production Integration
*!* Version 3.1.0 - Production Ready
*!* 
*!* This program provides complete document conversion functionality
*!* for VFP9 applications using the UniversalConverter32.dll
*!*
*!* Usage:
*!*   1. Include this program in your VFP9 project
*!*   2. Ensure UniversalConverter32.dll is in your application directory or System32
*!*   3. Ensure cli.py and Python dependencies are available
*!*   4. Call conversion functions as needed

*!* ============================================================================
*!* DLL FUNCTION DECLARATIONS
*!* ============================================================================

*-- Core conversion function
DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, ;
    STRING inputFormat, STRING outputFormat

*-- System functions  
DECLARE INTEGER TestConnection IN UniversalConverter32.dll
DECLARE STRING GetVersion IN UniversalConverter32.dll
DECLARE STRING GetLastError IN UniversalConverter32.dll

*-- Format information functions
DECLARE STRING GetSupportedInputFormats IN UniversalConverter32.dll
DECLARE STRING GetSupportedOutputFormats IN UniversalConverter32.dll

*-- Specific conversion functions
DECLARE INTEGER ConvertPDFToText IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile
DECLARE INTEGER ConvertPDFToMarkdown IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile
DECLARE INTEGER ConvertDOCXToText IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile
DECLARE INTEGER ConvertDOCXToMarkdown IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile
DECLARE INTEGER ConvertMarkdownToHTML IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile
DECLARE INTEGER ConvertHTMLToMarkdown IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile
DECLARE INTEGER ConvertRTFToText IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile
DECLARE INTEGER ConvertRTFToMarkdown IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile

*-- File information function
DECLARE INTEGER GetFileInfo IN UniversalConverter32.dll ;
    STRING filePath, STRING @infoBuffer, INTEGER bufferSize

*!* ============================================================================
*!* CONSTANTS
*!* ============================================================================

*-- Return codes
#DEFINE UC_SUCCESS 1
#DEFINE UC_FAILURE 0
#DEFINE UC_ERROR -1

*-- Input formats
#DEFINE UC_FORMAT_PDF "pdf"
#DEFINE UC_FORMAT_DOCX "docx"
#DEFINE UC_FORMAT_TXT "txt"
#DEFINE UC_FORMAT_HTML "html"
#DEFINE UC_FORMAT_RTF "rtf"
#DEFINE UC_FORMAT_MARKDOWN "md"

*-- Output formats
#DEFINE UC_OUTPUT_TXT "txt"
#DEFINE UC_OUTPUT_MARKDOWN "md"
#DEFINE UC_OUTPUT_HTML "html"
#DEFINE UC_OUTPUT_JSON "json"

*!* ============================================================================
*!* MAIN CONVERTER CLASS
*!* ============================================================================

DEFINE CLASS UniversalConverter AS Custom

    *-- Properties
    cVersion = ""
    lInitialized = .F.
    cLastError = ""
    
    *-- Initialize the converter
    FUNCTION Init()
        THIS.lInitialized = THIS.InitializeConverter()
        RETURN THIS.lInitialized
    ENDFUNC
    
    *-- Initialize converter system
    FUNCTION InitializeConverter()
        LOCAL lnResult
        
        TRY
            lnResult = TestConnection()
            
            IF lnResult = UC_SUCCESS
                THIS.cVersion = THIS.GetConverterVersion()
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error initializing converter: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *-- Get converter version
    FUNCTION GetConverterVersion()
        LOCAL lcVersion
        
        TRY
            lcVersion = GetVersion()
            RETURN lcVersion
        CATCH TO loError
            RETURN "Unknown"
        ENDTRY
    ENDFUNC
    
    *-- Get last error message
    FUNCTION GetLastErrorMessage()
        LOCAL lcError
        
        TRY
            lcError = GetLastError()
            RETURN lcError
        CATCH TO loError
            RETURN "Could not retrieve error message"
        ENDTRY
    ENDFUNC
    
    *!* ========================================================================
    *!* GENERIC CONVERSION FUNCTION
    *!* ========================================================================
    
    *-- Convert any document to any supported format
    FUNCTION ConvertDocumentFile(tcInputPath, tcOutputPath, tcInputFormat, tcOutputFormat)
        LOCAL lnResult, lcInputFormat, lcOutputFormat
        
        *-- Validate parameters
        IF EMPTY(tcInputPath) OR EMPTY(tcOutputPath)
            THIS.cLastError = "Invalid file paths provided"
            RETURN .F.
        ENDIF
        
        *-- Check if input file exists
        IF NOT FILE(tcInputPath)
            THIS.cLastError = "Input file not found: " + tcInputPath
            RETURN .F.
        ENDIF
        
        *-- Auto-detect formats if not specified
        lcInputFormat = IIF(EMPTY(tcInputFormat), THIS.GetFileExtension(tcInputPath), tcInputFormat)
        lcOutputFormat = IIF(EMPTY(tcOutputFormat), THIS.GetFileExtension(tcOutputPath), tcOutputFormat)
        
        TRY
            lnResult = ConvertDocument(tcInputPath, tcOutputPath, lcInputFormat, lcOutputFormat)
            
            IF lnResult = UC_SUCCESS
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error in ConvertDocumentFile: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *!* ========================================================================
    *!* SPECIFIC CONVERSION FUNCTIONS
    *!* ========================================================================
    
    *-- Convert PDF to text
    FUNCTION PDFToText(tcPDFPath, tcTxtPath)
        LOCAL lnResult
        
        IF NOT THIS.ValidateFiles(tcPDFPath, tcTxtPath)
            RETURN .F.
        ENDIF
        
        TRY
            lnResult = ConvertPDFToText(tcPDFPath, tcTxtPath)
            
            IF lnResult = UC_SUCCESS
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error in PDFToText: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *-- Convert PDF to Markdown
    FUNCTION PDFToMarkdown(tcPDFPath, tcMDPath)
        LOCAL lnResult
        
        IF NOT THIS.ValidateFiles(tcPDFPath, tcMDPath)
            RETURN .F.
        ENDIF
        
        TRY
            lnResult = ConvertPDFToMarkdown(tcPDFPath, tcMDPath)
            
            IF lnResult = UC_SUCCESS
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error in PDFToMarkdown: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *-- Convert DOCX to text
    FUNCTION DOCXToText(tcDOCXPath, tcTxtPath)
        LOCAL lnResult
        
        IF NOT THIS.ValidateFiles(tcDOCXPath, tcTxtPath)
            RETURN .F.
        ENDIF
        
        TRY
            lnResult = ConvertDOCXToText(tcDOCXPath, tcTxtPath)
            
            IF lnResult = UC_SUCCESS
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error in DOCXToText: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *-- Convert DOCX to Markdown
    FUNCTION DOCXToMarkdown(tcDOCXPath, tcMDPath)
        LOCAL lnResult
        
        IF NOT THIS.ValidateFiles(tcDOCXPath, tcMDPath)
            RETURN .F.
        ENDIF
        
        TRY
            lnResult = ConvertDOCXToMarkdown(tcDOCXPath, tcMDPath)
            
            IF lnResult = UC_SUCCESS
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error in DOCXToMarkdown: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *-- Convert Markdown to HTML
    FUNCTION MarkdownToHTML(tcMDPath, tcHTMLPath)
        LOCAL lnResult
        
        IF NOT THIS.ValidateFiles(tcMDPath, tcHTMLPath)
            RETURN .F.
        ENDIF
        
        TRY
            lnResult = ConvertMarkdownToHTML(tcMDPath, tcHTMLPath)
            
            IF lnResult = UC_SUCCESS
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error in MarkdownToHTML: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *-- Convert HTML to Markdown
    FUNCTION HTMLToMarkdown(tcHTMLPath, tcMDPath)
        LOCAL lnResult
        
        IF NOT THIS.ValidateFiles(tcHTMLPath, tcMDPath)
            RETURN .F.
        ENDIF
        
        TRY
            lnResult = ConvertHTMLToMarkdown(tcHTMLPath, tcMDPath)
            
            IF lnResult = UC_SUCCESS
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error in HTMLToMarkdown: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *-- Convert RTF to text
    FUNCTION RTFToText(tcRTFPath, tcTxtPath)
        LOCAL lnResult
        
        IF NOT THIS.ValidateFiles(tcRTFPath, tcTxtPath)
            RETURN .F.
        ENDIF
        
        TRY
            lnResult = ConvertRTFToText(tcRTFPath, tcTxtPath)
            
            IF lnResult = UC_SUCCESS
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error in RTFToText: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *-- Convert RTF to Markdown
    FUNCTION RTFToMarkdown(tcRTFPath, tcMDPath)
        LOCAL lnResult
        
        IF NOT THIS.ValidateFiles(tcRTFPath, tcMDPath)
            RETURN .F.
        ENDIF
        
        TRY
            lnResult = ConvertRTFToMarkdown(tcRTFPath, tcMDPath)
            
            IF lnResult = UC_SUCCESS
                THIS.cLastError = ""
                RETURN .T.
            ELSE
                THIS.cLastError = THIS.GetLastErrorMessage()
                RETURN .F.
            ENDIF
            
        CATCH TO loError
            THIS.cLastError = "Error in RTFToMarkdown: " + loError.Message
            RETURN .F.
        ENDTRY
    ENDFUNC
    
    *!* ========================================================================
    *!* BATCH CONVERSION FUNCTIONS
    *!* ========================================================================
    
    *-- Convert all files in a directory
    FUNCTION ConvertDirectory(tcInputDir, tcOutputDir, tcInputFormat, tcOutputFormat)
        LOCAL ARRAY laFiles[1]
        LOCAL lnFiles, lnI, lcInputPath, lcOutputPath, lcBaseName
        LOCAL lnSuccessCount, lnFileCount
        
        lnSuccessCount = 0
        lnFileCount = 0
        
        *-- Validate directories
        IF NOT DIRECTORY(tcInputDir)
            THIS.cLastError = "Input directory not found: " + tcInputDir
            RETURN 0
        ENDIF
        
        *-- Create output directory if it doesn't exist
        IF NOT DIRECTORY(tcOutputDir)
            MD (tcOutputDir)
        ENDIF
        
        *-- Get all files with the specified input format
        lnFiles = ADIR(laFiles, tcInputDir + "\*." + tcInputFormat)
        
        IF lnFiles > 0
            FOR lnI = 1 TO lnFiles
                lcInputPath = tcInputDir + "\" + laFiles[lnI, 1]
                lcBaseName = LEFT(laFiles[lnI, 1], RAT(".", laFiles[lnI, 1]) - 1)
                lcOutputPath = tcOutputDir + "\" + lcBaseName + "." + tcOutputFormat
                
                lnFileCount = lnFileCount + 1
                
                IF THIS.ConvertDocumentFile(lcInputPath, lcOutputPath, tcInputFormat, tcOutputFormat)
                    lnSuccessCount = lnSuccessCount + 1
                    ? "Converted: " + laFiles[lnI, 1]
                ELSE
                    ? "Failed: " + laFiles[lnI, 1] + " - " + THIS.cLastError
                ENDIF
            ENDFOR
        ELSE
            THIS.cLastError = "No files found with format: " + tcInputFormat
        ENDIF
        
        ? "Batch conversion complete: " + TRANSFORM(lnSuccessCount) + " of " + TRANSFORM(lnFileCount) + " files converted"
        
        RETURN lnSuccessCount
    ENDFUNC
    
    *!* ========================================================================
    *!* UTILITY FUNCTIONS
    *!* ========================================================================
    
    *-- Validate input and output file paths
    FUNCTION ValidateFiles(tcInputPath, tcOutputPath)
        *-- Check input path
        IF EMPTY(tcInputPath)
            THIS.cLastError = "Empty input path"
            RETURN .F.
        ENDIF
        
        *-- Check output path
        IF EMPTY(tcOutputPath)
            THIS.cLastError = "Empty output path"
            RETURN .F.
        ENDIF
        
        *-- Check if input file exists
        IF NOT FILE(tcInputPath)
            THIS.cLastError = "Input file not found: " + tcInputPath
            RETURN .F.
        ENDIF
        
        RETURN .T.
    ENDFUNC
    
    *-- Extract file extension from path
    FUNCTION GetFileExtension(tcFilePath)
        LOCAL lnLastDot
        
        lnLastDot = RAT(".", tcFilePath)
        
        IF lnLastDot > 0
            RETURN LOWER(SUBSTR(tcFilePath, lnLastDot + 1))
        ELSE
            RETURN ""
        ENDIF
    ENDFUNC
    
    *-- Get file size information
    FUNCTION GetDocumentFileInfo(tcFilePath)
        LOCAL lcBuffer, lnResult
        
        lcBuffer = SPACE(512)
        lnResult = GetFileInfo(tcFilePath, @lcBuffer, 512)
        
        IF lnResult = UC_SUCCESS
            RETURN TRIM(lcBuffer)
        ELSE
            RETURN "File information not available"
        ENDIF
    ENDFUNC
    
    *-- Get supported formats
    FUNCTION GetInputFormats()
        TRY
            RETURN GetSupportedInputFormats()
        CATCH TO loError
            RETURN "pdf,docx,txt,html,rtf,md"
        ENDTRY
    ENDFUNC
    
    FUNCTION GetOutputFormats()
        TRY
            RETURN GetSupportedOutputFormats()
        CATCH TO loError
            RETURN "txt,md,html,json"
        ENDTRY
    ENDFUNC
    
    *-- Run comprehensive test
    FUNCTION TestConverter()
        LOCAL lcTestFile, lcOutputFile, llSuccess
        
        ? "=== Universal Document Converter Test ==="
        ? "Version: " + THIS.GetConverterVersion()
        ? ""
        
        IF NOT THIS.lInitialized
            ? "✗ Converter not initialized"
            ? "Error: " + THIS.cLastError
            RETURN .F.
        ENDIF
        
        ? "✓ Converter initialized successfully"
        ? "Supported input formats: " + THIS.GetInputFormats()
        ? "Supported output formats: " + THIS.GetOutputFormats()
        ? ""
        
        *-- Test conversions (modify paths as needed)
        
        *-- Test 1: PDF to Text
        lcTestFile = "C:\temp\test.pdf"
        lcOutputFile = "C:\temp\test.txt"
        
        IF FILE(lcTestFile)
            llSuccess = THIS.PDFToText(lcTestFile, lcOutputFile)
            IF llSuccess
                ? "✓ PDF to Text conversion successful"
            ELSE
                ? "✗ PDF to Text conversion failed: " + THIS.cLastError
            ENDIF
        ELSE
            ? "Test PDF file not found: " + lcTestFile
        ENDIF
        
        *-- Test 2: Generic conversion
        lcTestFile = "C:\temp\document.docx"
        lcOutputFile = "C:\temp\document.md"
        
        IF FILE(lcTestFile)
            llSuccess = THIS.ConvertDocumentFile(lcTestFile, lcOutputFile)
            IF llSuccess
                ? "✓ Generic conversion successful"
            ELSE
                ? "✗ Generic conversion failed: " + THIS.cLastError
            ENDIF
        ELSE
            ? "Test DOCX file not found: " + lcTestFile
        ENDIF
        
        ? ""
        ? "=== Test Complete ==="
        
        RETURN .T.
    ENDFUNC
    
ENDDEFINE

*!* ============================================================================
*!* STANDALONE FUNCTIONS (Alternative to class-based approach)
*!* ============================================================================

*-- Initialize converter system
FUNCTION InitializeConverter()
    LOCAL lnResult
    
    TRY
        lnResult = TestConnection()
        RETURN (lnResult = UC_SUCCESS)
    CATCH TO loError
        RETURN .F.
    ENDTRY
ENDFUNC

*-- Simple conversion function
FUNCTION ConvertFile(tcInputFile, tcOutputFile, tcInputFormat, tcOutputFormat)
    LOCAL lnResult
    
    IF EMPTY(tcInputFile) OR EMPTY(tcOutputFile)
        RETURN .F.
    ENDIF
    
    IF NOT FILE(tcInputFile)
        RETURN .F.
    ENDIF
    
    TRY
        lnResult = ConvertDocument(tcInputFile, tcOutputFile, tcInputFormat, tcOutputFormat)
        RETURN (lnResult = UC_SUCCESS)
    CATCH TO loError
        RETURN .F.
    ENDTRY
ENDFUNC

*!* ============================================================================
*!* EXAMPLE USAGE
*!* ============================================================================

*-- Example 1: Using the class approach
PROCEDURE ExampleClassUsage()
    LOCAL loConverter, llSuccess
    
    *-- Create converter instance
    loConverter = CREATEOBJECT("UniversalConverter")
    
    IF loConverter.lInitialized
        MESSAGEBOX("Converter initialized successfully!")
        
        *-- Convert a document
        llSuccess = loConverter.ConvertDocumentFile("C:\temp\test.pdf", "C:\temp\test.txt")
        
        IF llSuccess
            MESSAGEBOX("Conversion successful!")
        ELSE
            MESSAGEBOX("Conversion failed: " + loConverter.cLastError)
        ENDIF
    ELSE
        MESSAGEBOX("Failed to initialize converter: " + loConverter.cLastError)
    ENDIF
ENDPROC

*-- Example 2: Using standalone functions
PROCEDURE ExampleStandaloneUsage()
    LOCAL llSuccess
    
    IF InitializeConverter()
        MESSAGEBOX("Converter available!")
        
        llSuccess = ConvertFile("C:\temp\document.docx", "C:\temp\document.txt", "docx", "txt")
        
        IF llSuccess
            MESSAGEBOX("Conversion successful!")
        ELSE
            MESSAGEBOX("Conversion failed!")
        ENDIF
    ELSE
        MESSAGEBOX("Converter not available!")
    ENDIF
ENDPROC

*-- Example 3: Batch conversion
PROCEDURE ExampleBatchConversion()
    LOCAL loConverter, lnConverted
    
    loConverter = CREATEOBJECT("UniversalConverter")
    
    IF loConverter.lInitialized
        *-- Convert all PDF files to text
        lnConverted = loConverter.ConvertDirectory("C:\Documents\PDFs", "C:\Documents\Text", "pdf", "txt")
        MESSAGEBOX(TRANSFORM(lnConverted) + " files converted successfully!")
    ELSE
        MESSAGEBOX("Converter not available!")
    ENDIF
ENDPROC