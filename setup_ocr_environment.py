#!/usr/bin/env python3
"""
OCR Environment Setup Script - Windows Optimized
Automatically installs all required dependencies for the OCR-enhanced document converter
"""

import os
import sys
import subprocess
import platform
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCRSetup:
    """Automated setup for OCR environment"""
    
    def __init__(self):
        self.system = platform.system()
        self.is_windows = self.system == "Windows"
        self.is_mac = self.system == "Darwin"
        self.is_linux = self.system == "Linux"
        
    def check_python_version(self):
        """Verify Python version compatibility"""
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            logger.info(f"Python {version.major}.{version.minor}.{version.micro} - Compatible")
            return True
        else:
            logger.error(f"Python {version.major}.{version.minor}.{version.micro} - Incompatible (requires 3.8+)")
            return False
    
    def check_tesseract(self):
        """Check Tesseract installation using cross-platform detection"""
        try:
            # Try to use our hardened tesseract_config module
            try:
                import tesseract_config
                if tesseract_config.configure_tesseract():
                    logger.info("Tesseract configured successfully using cross-platform detection")
                    return True
            except ImportError:
                logger.warning("tesseract_config module not available, using fallback detection")
            
            # Fallback: Try system PATH first (works on all platforms)
            import shutil
            tesseract_path = shutil.which('tesseract')
            if tesseract_path:
                logger.info(f"Tesseract found in PATH: {tesseract_path}")
                return True
            
            # Platform-specific fallback paths
            if self.is_windows:
                tesseract_paths = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Users\%USERNAME%\AppData\Local\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
                ]
                
                for path in tesseract_paths:
                    expanded_path = os.path.expandvars(path)
                    if os.path.isfile(expanded_path):
                        os.environ["TESSERACT_CMD"] = expanded_path
                        logger.info(f"Tesseract found at: {expanded_path}")
                        return True
                        
            else:
                # Unix-like systems fallback
                result = subprocess.run(["which", "tesseract"], capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info(f"Tesseract found at: {result.stdout.strip()}")
                    return True
                    
            logger.error("Tesseract not found. Please install Tesseract OCR:")
            if self.is_windows:
                logger.error("- Install from: https://github.com/UB-Mannheim/tesseract/wiki")
                logger.error("- Or run: choco install tesseract")
            elif self.is_mac:
                logger.error("- Run: brew install tesseract")
            elif self.is_linux:
                logger.error("- Run: sudo apt-get install tesseract-ocr")
                
            return False
            
        except Exception as e:
            logger.error(f"Error checking Tesseract: {e}")
            return False
    
    def install_python_packages(self):
        """Install required Python packages"""
        # Skip weasyprint on Windows due to GTK+ dependencies
        packages = [
            "pytesseract",
            "pillow",
            "numpy",
            "opencv-python",
            "easyocr",
            "psutil",
            "python-docx",
            "docx2txt",
            "reportlab",
            # "weasyprint",  # Skip on Windows
            "markdown",
            "beautifulsoup4"
        ]
        
        failed_packages = []
        
        for package in packages:
            try:
                logger.info(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                logger.info(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install {package}: {e}")
                failed_packages.append(package)
        
        if failed_packages:
            logger.error(f"Failed packages: {failed_packages}")
            return False
        
        return True
    
    def verify_installation(self):
        """Verify all components are properly installed"""
        logger.info("Verifying installation...")
        
        # Check Python packages
        packages = [
            "pytesseract",
            "PIL", 
            "cv2", 
            "easyocr", 
            "psutil", 
            "docx", 
            "docx2txt", 
            "reportlab", 
            # "weasyprint",  # Skip verification on Windows
            "markdown", 
            "bs4"
        ]
        
        missing_packages = []
        
        for package in packages:
            try:
                __import__(package)
                logger.info(f"✅ {package} - Available")
            except ImportError as e:
                logger.error(f"❌ {package} - Missing: {e}")
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Missing packages: {missing_packages}")
            return False
        
        # Check Tesseract
        try:
            import pytesseract
            if self.is_windows and "TESSERACT_CMD" in os.environ:
                pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_CMD"]
            
            version = pytesseract.get_tesseract_version()
            logger.info(f"✅ Tesseract version: {version}")
        except Exception as e:
            logger.error(f"❌ Tesseract verification failed: {e}")
            return False
        
        # Check EasyOCR
        try:
            import easyocr
            reader = easyocr.Reader(['en'], gpu=False)  # Initialize without GPU
            logger.info("✅ EasyOCR - Available")
        except Exception as e:
            logger.error(f"❌ EasyOCR verification failed: {e}")
            return False
        
        return True
    
    def create_environment_file(self):
        """Create environment configuration file"""
        try:
            env_config = {
                "system": self.system,
                "python_version": sys.version,
                "tesseract_path": os.environ.get("TESSERACT_CMD", "system"),
                "packages_installed": True,
                "setup_date": "Windows - Setup Complete"
            }
            
            with open("environment.json", "w") as f:
                json.dump(env_config, f, indent=2)
            
            logger.info("✅ Environment configuration saved")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create environment file: {e}")
            return False
    
    def run_setup(self):
        """Run complete setup process"""
        logger.info("=" * 60)
        logger.info("OCR Environment Setup")
        logger.info("=" * 60)
        
        steps = [
            ("Python Version", self.check_python_version),
            ("System Dependencies", self.check_tesseract),
            ("Python Packages", self.install_python_packages),
            ("Verification", self.verify_installation),
            ("Environment Config", self.create_environment_file)
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n--- {step_name} ---")
            if not step_func():
                logger.error(f"❌ Setup failed at: {step_name}")
                return False
        
        logger.info("\n" + "=" * 60)
        logger.info("✅ Setup completed successfully!")
        logger.info("=" * 60)
        logger.info("You can now run: python universal_document_converter_ocr.py")
        
        return True

if __name__ == "__main__":
    setup = OCRSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)