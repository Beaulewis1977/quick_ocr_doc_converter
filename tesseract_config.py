# Tesseract Configuration Fix
import os
import sys

def configure_tesseract():
    """Configure Tesseract OCR paths"""
    try:
        import pytesseract
        
        # Set Tesseract executable path for Windows (accessed from WSL)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        # Set tessdata directory environment variable
        os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"
        
        print("✅ Tesseract configured successfully")
        print(f"   Tesseract path: C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        print(f"   Tessdata path: C:\\Program Files\\Tesseract-OCR\\tessdata")
        
        return True
        
    except ImportError:
        print("❌ pytesseract not installed")
        return False
    except Exception as e:
        print(f"❌ Error configuring Tesseract: {e}")
        return False

# Auto-configure when imported
if __name__ == "__main__":
    configure_tesseract()
else:
    configure_tesseract()