*!* Universal Document Converter VFP9 Integration
*!* Provides easy access to document conversion functionality

*-- DLL Function Declarations
DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
    STRING inputFile, STRING outputFile, ;
    STRING inputFormat, STRING outputFormat

DECLARE INTEGER TestConnection IN UniversalConverter32.dll

*-- Constants
#DEFINE UC_SUCCESS 1
#DEFINE UC_FAILURE 0  
#DEFINE UC_ERROR -1

*!* Convert Markdown to RTF
FUNCTION ConvertMarkdownToRTF(tcInputFile, tcOutputFile)
    LOCAL lnResult
    lnResult = ConvertDocument(tcInputFile, tcOutputFile, "markdown", "rtf")
    RETURN (lnResult = UC_SUCCESS)
ENDFUNC

*!* Convert RTF to Markdown  
FUNCTION ConvertRTFToMarkdown(tcInputFile, tcOutputFile)
    LOCAL lnResult
    lnResult = ConvertDocument(tcInputFile, tcOutputFile, "rtf", "markdown")
    RETURN (lnResult = UC_SUCCESS)
ENDFUNC

*!* Test if converter is available
FUNCTION IsConverterAvailable()
    LOCAL lnResult
    lnResult = TestConnection()
    RETURN (lnResult = UC_SUCCESS)
ENDFUNC

*!* Test conversion functionality
PROCEDURE TestConverter()
    IF IsConverterAvailable()
        MESSAGEBOX("Universal Document Converter is available!")
        
        *-- Test conversion
        LOCAL llResult
        llResult = ConvertMarkdownToRTF("C:\temp\test.md", "C:\temp\test.rtf")
        
        IF llResult
            MESSAGEBOX("Test conversion successful!")
        ELSE
            MESSAGEBOX("Test conversion failed!")
        ENDIF
    ELSE
        MESSAGEBOX("Universal Document Converter is not available!")
    ENDIF
ENDPROC

*!* Example usage
PROCEDURE ExampleUsage()
    LOCAL lcInputFile, lcOutputFile, llSuccess
    
    *-- Set file paths
    lcInputFile = "C:\Documents\readme.md"
    lcOutputFile = "C:\Documents\readme.rtf"
    
    *-- Convert markdown to RTF
    llSuccess = ConvertMarkdownToRTF(lcInputFile, lcOutputFile)
    
    IF llSuccess
        MESSAGEBOX("Conversion successful! Check: " + lcOutputFile)
    ELSE
        MESSAGEBOX("Conversion failed! Check file paths and DLL availability.")
    ENDIF
ENDPROC

*!* Batch conversion example
PROCEDURE BatchConvert()
    LOCAL ARRAY laFiles[1]
    LOCAL lnFiles, lnI, lcInputFile, lcOutputFile, llSuccess
    
    *-- Get all .md files in a directory
    lnFiles = ADIR(laFiles, "C:\Documents\*.md")
    
    IF lnFiles > 0
        FOR lnI = 1 TO lnFiles
            lcInputFile = "C:\Documents\" + laFiles[lnI, 1]
            lcOutputFile = STRTRAN(lcInputFile, ".md", ".rtf")
            
            llSuccess = ConvertMarkdownToRTF(lcInputFile, lcOutputFile)
            
            IF llSuccess
                ? "Converted: " + laFiles[lnI, 1]
            ELSE
                ? "Failed: " + laFiles[lnI, 1]
            ENDIF
        ENDFOR
    ELSE
        MESSAGEBOX("No .md files found in C:\Documents\")
    ENDIF
ENDPROC
