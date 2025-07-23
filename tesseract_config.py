# Cross-Platform Tesseract Configuration
import os
import sys
import platform
import shutil
import logging
from pathlib import Path
from typing import Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_tesseract_executable() -> Optional[str]:
    """Find Tesseract executable across different platforms"""
    system = platform.system().lower()
    
    # Check if tesseract is in PATH first
    tesseract_path = shutil.which('tesseract')
    if tesseract_path:
        return tesseract_path
    
    # Platform-specific default paths
    common_paths = []
    
    if system == 'windows':
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\%USERNAME%\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        ]
    elif system == 'darwin':  # macOS
        common_paths = [
            '/usr/local/bin/tesseract',
            '/opt/homebrew/bin/tesseract',
            '/usr/bin/tesseract'
        ]
    elif system == 'linux':
        common_paths = [
            '/usr/bin/tesseract',
            '/usr/local/bin/tesseract',
            '/snap/bin/tesseract'
        ]
    
    # Check each path
    for path in common_paths:
        expanded_path = os.path.expandvars(path)
        if os.path.isfile(expanded_path) and os.access(expanded_path, os.X_OK):
            return expanded_path
    
    return None

def find_tessdata_directory(tesseract_path: str) -> Optional[str]:
    """Find tessdata directory based on tesseract executable location"""
    if not tesseract_path:
        return None
    
    tesseract_dir = Path(tesseract_path).parent
    
    # Common tessdata locations relative to tesseract executable
    possible_tessdata_dirs = [
        tesseract_dir / "tessdata",
        tesseract_dir.parent / "tessdata", 
        tesseract_dir.parent / "share" / "tessdata",
        tesseract_dir.parent / "share" / "tesseract-ocr" / "4.00" / "tessdata",
        tesseract_dir.parent / "share" / "tesseract-ocr" / "5.00" / "tessdata"
    ]
    
    # System-wide locations
    system_tessdata_dirs = [
        Path("/usr/share/tessdata"),
        Path("/usr/share/tesseract-ocr/tessdata"),
        Path("/usr/share/tesseract-ocr/4.00/tessdata"),
        Path("/usr/share/tesseract-ocr/5.00/tessdata"),
        Path("/opt/homebrew/share/tessdata")
    ]
    
    possible_tessdata_dirs.extend(system_tessdata_dirs)
    
    for tessdata_dir in possible_tessdata_dirs:
        if tessdata_dir.exists() and tessdata_dir.is_dir():
            # Check if it contains expected tessdata files
            if list(tessdata_dir.glob("*.traineddata")) or (tessdata_dir / "eng.traineddata").exists():
                return str(tessdata_dir)
    
    return None

def configure_tesseract():
    """Configure Tesseract OCR paths with cross-platform support"""
    try:
        import pytesseract
        
        # Find tesseract executable
        tesseract_path = find_tesseract_executable()
        if not tesseract_path:
            logger.warning("⚠️ Tesseract executable not found in common locations")
            logger.warning("   Please ensure Tesseract is installed and in PATH")
            return False
        
        # Configure pytesseract
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Find and set tessdata directory
        tessdata_path = find_tessdata_directory(tesseract_path)
        if tessdata_path:
            os.environ["TESSDATA_PREFIX"] = tessdata_path
            logger.info("✅ Tesseract configured successfully")
            logger.info(f"   Tesseract executable: {tesseract_path}")
            logger.info(f"   Tessdata directory: {tessdata_path}")
        else:
            logger.warning("⚠️ Tessdata directory not found, using system default")
            logger.info("✅ Tesseract executable configured")
            logger.info(f"   Tesseract executable: {tesseract_path}")
        
        # Test configuration
        try:
            version = pytesseract.get_tesseract_version()
            logger.info(f"   Tesseract version: {version}")
        except Exception as e:
            logger.warning(f"   Could not get Tesseract version: {e}")
        
        return True
        
    except ImportError:
        logger.error("❌ pytesseract not installed")
        logger.error("   Install with: pip install pytesseract")
        return False
    except Exception as e:
        logger.error(f"❌ Error configuring Tesseract: {e}")
        return False

# Auto-configure when imported
if __name__ == "__main__":
    configure_tesseract()
else:
    configure_tesseract()