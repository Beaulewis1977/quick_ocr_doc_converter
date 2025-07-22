# UniversalConverter32 - VB6/VFP9 Integration Package

This package provides integration between the OCR Document Converter and legacy applications built with Visual Basic 6 (VB6) and Visual FoxPro 9 (VFP9).

## 📦 **Package Contents**

| File | Description |
|------|-------------|
| `UniversalConverter32.py` | Main Python integration module |
| `VB6_Example.vb` | Complete VB6 example application |
| `VFP9_Example.prg` | Complete VFP9 example application |
| `build_dll.bat` | Batch file to create Windows DLL |
| `README.md` | This documentation |

## 🚀 **Quick Start**

### **For VB6 Developers:**

1. **Copy the integration files** to your VB6 project directory
2. **Add the example code** from `VB6_Example.vb` to your project
3. **Call the converter functions** from your VB6 application:

```vb
' Simple document conversion
result = CallUniversalConverter("input.pdf", "output.txt", "txt", False)

' OCR conversion
result = CallUniversalConverter("image.jpg", "output.txt", "txt", True)
```

### **For VFP9 Developers:**

1. **Copy the integration files** to your VFP9 project directory  
2. **Include the example code** from `VFP9_Example.prg` in your project
3. **Use the converter functions** in your FoxPro application:

```foxpro
* Simple document conversion
lnResult = ConvertDocument("input.pdf", "output.txt", "txt")

* OCR conversion  
lnResult = ConvertDocumentWithOCR("image.jpg", "output.txt", "txt", "eng")
```

## 🔧 **Installation Requirements**

### **System Requirements:**
- Windows 10/11 (32-bit or 64-bit)
- Python 3.8+ installed and in system PATH
- OCR Document Converter v3.1.0 installed

### **Python Dependencies:**
The main OCR Document Converter must be installed with all dependencies:
```bash
pip install -r requirements.txt
```

### **Optional: Build Native DLL**
For better performance, you can build a native DLL:
```bash
cd vb6_vfp9_integration
build_dll.bat
```

## 📚 **API Reference**

### **Core Functions**

#### **ConvertDocument(input, output, format)**
Converts a document without OCR.

**Parameters:**
- `input` (String): Path to input file
- `output` (String): Path to output file  
- `format` (String): Output format (txt, docx, pdf, html, markdown)

**Returns:** 1 for success, 0 for failure

#### **ConvertDocumentWithOCR(input, output, format, language)**
Converts a document with OCR enabled.

**Parameters:**
- `input` (String): Path to input file
- `output` (String): Path to output file
- `format` (String): Output format
- `language` (String): OCR language code (eng, fra, deu, spa, etc.)

**Returns:** 1 for success, 0 for failure

#### **GetLastError()**
Gets the last error message.

**Returns:** String with error description

#### **GetVersion()**
Gets the converter version.

**Returns:** Version string (e.g., "3.1.0")

#### **IsOCRAvailable()**
Checks if OCR functionality is available.

**Returns:** 1 if available, 0 if not available

#### **GetSupportedFormats()**
Gets list of supported file formats.

**Returns:** Comma-separated string of formats

### **Advanced Functions**

#### **BatchConvert(input_dir, output_dir, pattern, format)**
Batch converts files in a directory.

**Parameters:**
- `input_dir` (String): Input directory path
- `output_dir` (String): Output directory path
- `pattern` (String): File pattern (*.pdf, *.jpg, etc.)
- `format` (String): Output format

**Returns:** JSON string with detailed results

## 💡 **Usage Examples**

### **VB6 Example - Simple Conversion:**

```vb
Private Sub btnConvert_Click()
    Dim result As Long
    result = CallUniversalConverter("C:\docs\input.pdf", "C:\docs\output.txt", "txt", False)
    
    If result = 1 Then
        MsgBox "Conversion successful!"
    Else
        MsgBox "Conversion failed!"
    End If
End Sub
```

### **VFP9 Example - OCR Conversion:**

```foxpro
PROCEDURE ConvertWithOCR
    LOCAL lnResult
    
    lnResult = ConvertDocumentWithOCR("C:\images\scan.jpg", "C:\text\output.txt", "txt", "eng")
    
    IF lnResult = 1
        MESSAGEBOX("OCR conversion successful!", 64)
    ELSE
        MESSAGEBOX("OCR conversion failed!", 16)
    ENDIF
ENDPROC
```

### **VFP9 Example - Batch Processing:**

```foxpro
PROCEDURE BatchConvertPDFs
    LOCAL lcResult, lcJSON
    
    lcResult = BatchConvert("C:\input_pdfs", "C:\output_txt", "*.pdf", "txt")
    
    * Parse JSON result (requires JSON parser)
    ? lcResult  && Display results
ENDPROC
```

## 🔍 **Supported File Formats**

### **Input Formats:**
- **Images**: JPG, PNG, TIFF, BMP, GIF, WebP
- **Documents**: PDF, TXT, DOCX, HTML, RTF, EPUB

### **Output Formats:**
- **Text**: TXT, Markdown
- **Documents**: DOCX, PDF, HTML, RTF, EPUB
- **Data**: JSON

## ⚙️ **Configuration**

The converter inherits settings from the main OCR Document Converter application. You can configure:

- **OCR Engine**: Tesseract, EasyOCR, or Google Vision API
- **Languages**: 80+ supported languages
- **Quality**: Fast, Balanced, or Accurate processing
- **Preprocessing**: Image enhancement options

Access settings through the main GUI application or programmatically via the Python API.

## 🚨 **Error Handling**

Always check return values and handle errors appropriately:

### **VB6 Error Handling:**
```vb
Dim result As Long
Dim errorMsg As String

result = CallUniversalConverter(inputFile, outputFile, "txt", False)

If result = 0 Then
    errorMsg = GetLastError()
    MsgBox "Error: " & errorMsg, vbCritical
End If
```

### **VFP9 Error Handling:**
```foxpro
LOCAL lnResult, lcError

lnResult = ConvertDocument(tcInput, tcOutput, "txt")

IF lnResult = 0
    lcError = GetLastError()
    MESSAGEBOX("Error: " + lcError, 16, "Conversion Failed")
ENDIF
```

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **"Python not found"**
   - Install Python 3.8+ from python.org
   - Add Python to system PATH
   - Test with `python --version` in Command Prompt

2. **"Module not found"**
   - Install requirements: `pip install -r requirements.txt`
   - Ensure OCR Document Converter is properly installed

3. **"OCR not available"**
   - Install Tesseract OCR
   - Check OCR settings in main application
   - Verify language packs are installed

4. **"Conversion failed"**
   - Check input file exists and is readable
   - Verify output directory exists
   - Check file permissions
   - Use GetLastError() for details

### **Debug Mode:**
Enable verbose logging by setting environment variable:
```
SET DEBUG_CONVERTER=1
```

## 📞 **Support**

- **Documentation**: Check the main README.md in parent directory
- **Issues**: Report bugs on GitHub repository
- **Examples**: See VB6_Example.vb and VFP9_Example.prg for complete implementations

---

**OCR Document Converter v3.1.0**  
**Enhanced by Terragon Labs**  
**VB6/VFP9 Integration Package**