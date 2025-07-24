# OCR Troubleshooting Guide

## Common Issues and Solutions

### 1. Blank OCR Output / "OCR processing failed: File content validation failed"

**Symptoms:**
- OCR saves txt files but they are blank
- Error: "Tesseract OCR failed: (1, 'Error opening data file...'"
- Message: "# OCR Result: image" with "Confidence: 0"

**Solutions:**

1. **Verify Tesseract Installation:**
   ```bash
   # Check if Tesseract is installed
   tesseract --version
   
   # Should show something like:
   # tesseract 5.5.0
   # leptonica-1.82.0
   ```

2. **Install Language Data Files:**
   
   **Windows:**
   - During Tesseract installation, make sure to select "Additional language data" 
   - Or download manually from: https://github.com/tesseract-ocr/tessdata
   - Place in: `C:\Program Files\Tesseract-OCR\tessdata\`
   
   **macOS:**
   ```bash
   brew install tesseract
   brew install tesseract-lang  # Installs all language packs
   ```
   
   **Linux:**
   ```bash
   sudo apt-get install tesseract-ocr
   sudo apt-get install tesseract-ocr-eng  # English
   sudo apt-get install tesseract-ocr-all  # All languages
   ```

3. **Set TESSDATA_PREFIX Environment Variable:**
   
   **Windows:**
   ```cmd
   setx TESSDATA_PREFIX "C:\Program Files\Tesseract-OCR\tessdata"
   ```
   
   **macOS/Linux:**
   ```bash
   export TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/
   # Add to ~/.bashrc or ~/.zshrc to make permanent
   ```

4. **Verify Language Files Exist:**
   ```bash
   # Check if eng.traineddata exists
   ls $TESSDATA_PREFIX/eng.traineddata
   
   # Or on Windows:
   dir "C:\Program Files\Tesseract-OCR\tessdata\eng.traineddata"
   ```

### 2. "All OCR engines failed" Error

**Solutions:**

1. **Use EasyOCR as Fallback:**
   - In the OCR tab, change engine from "Tesseract" to "EasyOCR" or "Auto"
   - EasyOCR doesn't require external files

2. **Enable Google Vision API:**
   - Go to API Management tab
   - Add Google Vision API credentials
   - Enable the API
   - Select "Google Vision" as OCR engine

### 3. OCR Accuracy Issues

**Solutions:**

1. **Improve Image Quality:**
   - Use high-resolution images (300 DPI or higher)
   - Ensure good contrast between text and background
   - Avoid blurry or skewed images

2. **Select Appropriate Engine:**
   - **Tesseract**: Best for printed text
   - **EasyOCR**: Better for handwritten text or mixed content
   - **Google Vision**: Highest accuracy for all types

3. **Adjust OCR Settings:**
   - Change Quality from "Fast" to "Accurate"
   - Select correct language
   - Enable preprocessing for poor quality images

### 4. Performance Issues

**Solutions:**

1. **Reduce Batch Size:**
   - Process fewer files at once
   - Lower thread count in settings

2. **Enable GPU Acceleration (EasyOCR):**
   ```bash
   pip install torch torchvision  # For CUDA support
   ```

3. **Use Caching:**
   - Keep "Use cache" enabled
   - Cached results load instantly

### 5. Language-Specific Issues

**Problem:** Wrong language detected or poor accuracy

**Solutions:**

1. **Specify Language Explicitly:**
   - Don't use "Auto-detect"
   - Select specific language in dropdown

2. **Install Language Packs:**
   
   **Tesseract Languages:**
   ```bash
   # Example for German
   sudo apt-get install tesseract-ocr-deu
   
   # Example for Japanese
   sudo apt-get install tesseract-ocr-jpn
   ```
   
   **Common Language Codes:**
   - eng - English
   - fra - French  
   - deu - German
   - spa - Spanish
   - chi_sim - Chinese Simplified
   - jpn - Japanese
   - ara - Arabic

### 6. File Format Issues

**Problem:** "Unsupported file type" or validation errors

**Solutions:**

1. **Supported Formats:**
   - Images: PNG, JPG, JPEG, TIFF, BMP, GIF, WebP
   - Documents: PDF (as images)

2. **Convert Unsupported Formats:**
   ```bash
   # Convert HEIC to JPG
   convert input.heic output.jpg
   
   # Convert PDF to images
   pdftoppm -jpeg input.pdf output
   ```

### 7. Installation Dependencies

**If OCR isn't working at all:**

1. **Reinstall Dependencies:**
   ```bash
   pip install --upgrade pytesseract pillow opencv-python
   pip install --upgrade easyocr
   ```

2. **Check Python Version:**
   - Requires Python 3.8 or higher
   - Some features need Python 3.9+

### 8. Debug Mode

**Enable detailed logging:**

1. Go to Settings → Logging
2. Set level to "DEBUG"
3. Check logs at: `~/.universal_converter/logs/`

**Manual Test:**
```python
import pytesseract
from PIL import Image

# Test Tesseract
try:
    img = Image.open("test_image.png")
    text = pytesseract.image_to_string(img)
    print("Success:", text)
except Exception as e:
    print("Error:", e)
```

### Getting Help

If issues persist:

1. Check the log files
2. Run the test commands above
3. Contact: blewisxx@gmail.com

Include:
- Error messages
- Log files
- System info (OS, Python version)
- Tesseract version
- Steps to reproduce