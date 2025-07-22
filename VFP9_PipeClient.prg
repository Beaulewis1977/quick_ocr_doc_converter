*!* Universal Document Converter - VFP9 Named Pipes Integration
*!* Communicates with Python pipe server for document conversion

*-- Constants for file access
#DEFINE GENERIC_READ          0x80000000
#DEFINE GENERIC_WRITE         0x40000000
#DEFINE OPEN_EXISTING         3
#DEFINE PIPE_WAIT             0

*-- API Declarations
DECLARE INTEGER CreateFile IN kernel32 ;
    STRING lpFileName, INTEGER dwDesiredAccess, INTEGER dwShareMode, ;
    INTEGER lpSecurityAttributes, INTEGER dwCreationDisposition, ;
    INTEGER dwFlagsAndAttributes, INTEGER hTemplateFile

DECLARE INTEGER WriteFile IN kernel32 ;
    INTEGER hFile, STRING lpBuffer, INTEGER nNumberOfBytesToWrite, ;
    INTEGER lpNumberOfBytesWritten, INTEGER lpOverlapped

DECLARE INTEGER ReadFile IN kernel32 ;
    INTEGER hFile, STRING @lpBuffer, INTEGER nNumberOfBytesToRead, ;
    INTEGER lpNumberOfBytesRead, INTEGER lpOverlapped

DECLARE INTEGER CloseHandle IN kernel32 INTEGER hObject

*!* Convert document using named pipe
FUNCTION ConvertDocumentPipe(tcInputFile, tcOutputFile, tcInputFormat, tcOutputFormat)
    LOCAL lnPipeHandle, lcRequest, lcResponse, llSuccess
    LOCAL lnBytesWritten, lnBytesRead, lnResult
    
    *-- Create pipe connection
    lnPipeHandle = CreateFile("\\.\pipe\UniversalConverter", ;
        GENERIC_READ + GENERIC_WRITE, 0, 0, OPEN_EXISTING, PIPE_WAIT, 0)
    
    IF lnPipeHandle = -1
        MESSAGEBOX("Failed to connect to converter pipe server")
        RETURN .F.
    ENDIF
    
    TRY
        *-- Create JSON request
        lcRequest = '{"input":"' + tcInputFile + '","output":"' + tcOutputFile + ;
                   '","input_format":"' + tcInputFormat + ;
                   '","output_format":"' + tcOutputFormat + '"}'
        
        *-- Send request
        lnBytesWritten = 0
        lnResult = WriteFile(lnPipeHandle, lcRequest, LEN(lcRequest), @lnBytesWritten, 0)
        
        IF lnResult = 0 OR lnBytesWritten = 0
            MESSAGEBOX("Failed to send request to pipe server")
            RETURN .F.
        ENDIF
        
        *-- Read response
        lcResponse = SPACE(4096)
        lnBytesRead = 0
        lnResult = ReadFile(lnPipeHandle, @lcResponse, LEN(lcResponse), @lnBytesRead, 0)
        
        IF lnResult = 0 OR lnBytesRead = 0
            MESSAGEBOX("Failed to read response from pipe server")
            RETURN .F.
        ENDIF
        
        *-- Trim response to actual length
        lcResponse = LEFT(lcResponse, lnBytesRead)
        
        *-- Parse response (simple check for success)
        llSuccess = ("success" $ LOWER(lcResponse))
        
        IF NOT llSuccess
            MESSAGEBOX("Conversion failed: " + lcResponse)
        ENDIF
        
        RETURN llSuccess
        
    CATCH TO loException
        MESSAGEBOX("Pipe communication error: " + loException.Message)
        RETURN .F.
    FINALLY
        *-- Always close the pipe handle
        CloseHandle(lnPipeHandle)
    ENDTRY
ENDFUNC

*!* Test pipe communication
PROCEDURE TestPipeConversion()
    LOCAL llResult
    
    *-- Test conversion
    llResult = ConvertDocumentPipe("C:\temp\test.md", "C:\temp\test.rtf", "markdown", "rtf")
    
    IF llResult
        MESSAGEBOX("Pipe conversion successful!")
    ELSE
        MESSAGEBOX("Pipe conversion failed!")
    ENDIF
ENDPROC

*!* Example usage with error handling
PROCEDURE PipeConversionExample()
    LOCAL lcInputFile, lcOutputFile
    
    *-- Set file paths
    lcInputFile = GETFILE("md", "Select Markdown file:", "Open")
    IF EMPTY(lcInputFile)
        RETURN
    ENDIF
    
    lcOutputFile = PUTFILE("RTF File", STRTRAN(lcInputFile, ".md", ".rtf"), "rtf")
    IF EMPTY(lcOutputFile)
        RETURN  
    ENDIF
    
    *-- Start pipe server if not running
    *-- (You would need to start pipe_server.py separately)
    
    *-- Convert using pipe
    IF ConvertDocumentPipe(lcInputFile, lcOutputFile, "markdown", "rtf")
        MESSAGEBOX("Document converted successfully!" + CHR(13) + ;
                  "Output: " + lcOutputFile)
    ELSE
        MESSAGEBOX("Document conversion failed!")
    ENDIF
ENDPROC
