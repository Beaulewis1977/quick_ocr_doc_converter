// UniversalConverter32.cpp - 32-bit DLL for VB6/VFP9 Integration
// Universal Document Converter DLL
// Provides document conversion functionality for legacy systems

#include <windows.h>
#include <iostream>
#include <string>
#include <fstream>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <stdexcept>
#include <sstream>

// Export macros for VB6/VFP9 compatibility
#define EXPORT extern "C" __declspec(dllexport)

// Error codes
#define UC_SUCCESS 1
#define UC_FAILURE 0
#define UC_ERROR -1

// Global variables
static char g_lastError[512] = "";
static char g_version[] = "3.1.0";

// Helper function to execute Python CLI and capture output
std::string ExecutePythonCLI(const std::string& command) {
    char buffer[128];
    std::string result = "";
    
    // Create a unique pointer for FILE*
    std::unique_ptr<FILE, decltype(&_pclose)> pipe(_popen(command.c_str(), "r"), _pclose);
    
    if (!pipe) {
        strcpy_s(g_lastError, sizeof(g_lastError), "Failed to execute Python CLI");
        return "";
    }
    
    while (fgets(buffer, sizeof(buffer), pipe.get()) != nullptr) {
        result += buffer;
    }
    
    return result;
}

// Helper function to validate file exists
bool FileExists(const std::string& filename) {
    std::ifstream file(filename);
    return file.good();
}

// Helper function to build CLI command
std::string BuildCLICommand(const char* inputFile, const char* outputFile, 
                           const char* inputFormat, const char* outputFormat) {
    std::ostringstream cmd;
    
    // Get the directory of the DLL
    char dllPath[MAX_PATH];
    GetModuleFileNameA(NULL, dllPath, MAX_PATH);
    std::string dllDir = std::string(dllPath);
    size_t lastSlash = dllDir.find_last_of("\\/");
    if (lastSlash != std::string::npos) {
        dllDir = dllDir.substr(0, lastSlash);
    }
    
    // Build the Python CLI command
    cmd << "cd /d \"" << dllDir << "\" && python cli.py";
    cmd << " \"" << inputFile << "\"";
    cmd << " -o \"" << outputFile << "\"";
    
    if (outputFormat && strlen(outputFormat) > 0) {
        cmd << " -t " << outputFormat;
    }
    
    cmd << " --quiet 2>&1";
    
    return cmd.str();
}

// DLL Main Entry Point
BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH:
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
        case DLL_PROCESS_DETACH:
            break;
    }
    return TRUE;
}

// Main conversion function
EXPORT LONG ConvertDocument(const char* inputFile, const char* outputFile, 
                           const char* inputFormat, const char* outputFormat) {
    // Clear previous error
    g_lastError[0] = '\0';
    
    // Validate input parameters
    if (!inputFile || !outputFile) {
        strcpy_s(g_lastError, sizeof(g_lastError), "Invalid input parameters");
        return UC_ERROR;
    }
    
    // Check if input file exists
    if (!FileExists(inputFile)) {
        sprintf_s(g_lastError, sizeof(g_lastError), "Input file not found: %s", inputFile);
        return UC_ERROR;
    }
    
    try {
        // Build and execute CLI command
        std::string command = BuildCLICommand(inputFile, outputFile, inputFormat, outputFormat);
        std::string output = ExecutePythonCLI(command);
        
        // Check if output file was created
        if (FileExists(outputFile)) {
            return UC_SUCCESS;
        } else {
            if (strlen(g_lastError) == 0) {
                strcpy_s(g_lastError, sizeof(g_lastError), "Conversion failed - output file not created");
            }
            return UC_FAILURE;
        }
    } catch (const std::exception& e) {
        sprintf_s(g_lastError, sizeof(g_lastError), "Exception: %s", e.what());
        return UC_ERROR;
    } catch (...) {
        strcpy_s(g_lastError, sizeof(g_lastError), "Unknown error occurred");
        return UC_ERROR;
    }
}

// Test if the converter system is available
EXPORT LONG TestConnection() {
    // Clear previous error
    g_lastError[0] = '\0';
    
    try {
        // Test if Python and CLI are available
        std::string command = "python --version 2>&1";
        std::string output = ExecutePythonCLI(command);
        
        if (output.find("Python") != std::string::npos) {
            // Test if CLI script exists
            if (FileExists("cli.py")) {
                return UC_SUCCESS;
            } else {
                strcpy_s(g_lastError, sizeof(g_lastError), "CLI script not found");
                return UC_FAILURE;
            }
        } else {
            strcpy_s(g_lastError, sizeof(g_lastError), "Python not available");
            return UC_FAILURE;
        }
    } catch (...) {
        strcpy_s(g_lastError, sizeof(g_lastError), "Connection test failed");
        return UC_ERROR;
    }
}

// Get version information
EXPORT const char* GetVersion() {
    return g_version;
}

// Get last error message
EXPORT const char* GetLastError() {
    return g_lastError;
}

// Get supported input formats
EXPORT const char* GetSupportedInputFormats() {
    return "pdf,docx,txt,html,rtf,md,markdown";
}

// Get supported output formats
EXPORT const char* GetSupportedOutputFormats() {
    return "txt,md,html,json";
}

// Convert specific format pairs (convenience functions)
EXPORT LONG ConvertPDFToText(const char* inputFile, const char* outputFile) {
    return ConvertDocument(inputFile, outputFile, "pdf", "txt");
}

EXPORT LONG ConvertPDFToMarkdown(const char* inputFile, const char* outputFile) {
    return ConvertDocument(inputFile, outputFile, "pdf", "md");
}

EXPORT LONG ConvertDOCXToText(const char* inputFile, const char* outputFile) {
    return ConvertDocument(inputFile, outputFile, "docx", "txt");
}

EXPORT LONG ConvertDOCXToMarkdown(const char* inputFile, const char* outputFile) {
    return ConvertDocument(inputFile, outputFile, "docx", "md");
}

EXPORT LONG ConvertMarkdownToHTML(const char* inputFile, const char* outputFile) {
    return ConvertDocument(inputFile, outputFile, "md", "html");
}

EXPORT LONG ConvertHTMLToMarkdown(const char* inputFile, const char* outputFile) {
    return ConvertDocument(inputFile, outputFile, "html", "md");
}

EXPORT LONG ConvertRTFToText(const char* inputFile, const char* outputFile) {
    return ConvertDocument(inputFile, outputFile, "rtf", "txt");
}

EXPORT LONG ConvertRTFToMarkdown(const char* inputFile, const char* outputFile) {
    return ConvertDocument(inputFile, outputFile, "rtf", "md");
}

// Batch conversion function
EXPORT LONG ConvertBatch(const char* inputDir, const char* outputDir, 
                        const char* inputFormat, const char* outputFormat) {
    // This is a simplified version - full implementation would enumerate files
    strcpy_s(g_lastError, sizeof(g_lastError), "Batch conversion not yet implemented");
    return UC_ERROR;
}

// Get file info
EXPORT LONG GetFileInfo(const char* filePath, char* infoBuffer, int bufferSize) {
    if (!filePath || !infoBuffer || bufferSize <= 0) {
        strcpy_s(g_lastError, sizeof(g_lastError), "Invalid parameters for GetFileInfo");
        return UC_ERROR;
    }
    
    if (!FileExists(filePath)) {
        sprintf_s(g_lastError, sizeof(g_lastError), "File not found: %s", filePath);
        return UC_ERROR;
    }
    
    // Get file size
    std::ifstream file(filePath, std::ios::binary | std::ios::ate);
    if (file.is_open()) {
        std::streamsize size = file.tellg();
        sprintf_s(infoBuffer, bufferSize, "Size: %lld bytes", static_cast<long long>(size));
        return UC_SUCCESS;
    } else {
        strcpy_s(g_lastError, sizeof(g_lastError), "Could not open file for info");
        return UC_ERROR;
    }
}