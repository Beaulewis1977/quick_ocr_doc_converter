#!/usr/bin/env python3
"""
Setup script for OCR Document Converter
Handles system dependencies and Python packages
"""

import os
import sys
import subprocess
import platform
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCRSetup:
    """Setup class for OCR Document Converter"""
    
    def __init__(self):
        self.system = platform.system()
        self.is_admin = self._check_admin()
        
    def _check_admin(self):
        """Check if running as administrator"""
        try:
            if self.system == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except (AttributeError, OSError, PermissionError):
            return False
    
    def install_python_packages(self):
        """Install required Python packages"""
        logger.info("Installing Python packages...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements_updated.txt"
            ], check=True)
            logger.info("Python packages installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install Python packages: {e}")
            return False
    
    def install_tesseract_windows(self):
        """Install Tesseract on Windows"""
        logger.info("Installing Tesseract OCR on Windows...")
        
        try:
            # Try winget first
            result = subprocess.run([
                "winget", "install", "--id", "tesseract-ocr.tesseract-ocr", "-e"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Tesseract installed successfully via winget")
                return True
            else:
                logger.warning("winget installation failed, trying chocolatey...")
                
                # Try chocolatey
                result = subprocess.run([
                    "choco", "install", "tesseract", "-y"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info("Tesseract installed successfully via chocolatey")
                    return True
                else:
                    logger.error("Tesseract installation failed")
                    return False
                    
        except Exception as e:
            logger.error(f"Windows Tesseract installation error: {e}")
            return False
    
    def install_tesseract_macos(self):
        """Install Tesseract on macOS"""
        logger.info("Installing Tesseract OCR on macOS...")
        
        try:
            subprocess.run([
                "brew", "install", "tesseract"
            ], check=True)
            logger.info("Tesseract installed successfully via homebrew")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"macOS Tesseract installation failed: {e}")
            return False
    
    def install_tesseract_linux(self):
        """Install Tesseract on Linux"""
        logger.info("Installing Tesseract OCR on Linux...")
        
        try:
            if self.is_admin:
                subprocess.run([
                    "apt-get", "update"], check=True)
                subprocess.run([
                    "apt-get", "install", "-y", "tesseract-ocr"
                ], check=True)
            else:
                subprocess.run([
                    "sudo", "apt-get", "update"], check=True)
                subprocess.run([
                    "sudo", "apt-get", "install", "-y", "tesseract-ocr"
                ], check=True)
            logger.info("Tesseract installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Linux Tesseract installation failed: {e}")
            return False
    
    def verify_tesseract_installation(self):
        """Verify Tesseract is properly installed"""
        try:
            # Try to run tesseract --version
            result = subprocess.run([
                "tesseract", "--version"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                logger.info(f"Tesseract verified: {version_line}")
                return True
            else:
                logger.warning("Tesseract not found in PATH")
                return False
        except FileNotFoundError:
            logger.warning("Tesseract not found")
            return False
    
    def setup_tesseract_path(self):
        """Setup Tesseract path for pytesseract"""
        possible_paths = {
            "Windows": [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', '')),
            ],
            "Darwin": [
                "/usr/local/bin/tesseract",
                "/opt/homebrew/bin/tesseract",
            ],
            "Linux": [
                "/usr/bin/tesseract",
                "/usr/local/bin/tesseract",
            ]
        }
        
        system_paths = possible_paths.get(self.system, [])
        
        for path in system_paths:
            if os.path.isfile(path):
                # Create config file
                config_path = Path("tesseract_config.py")
                config_content = f'''# Tesseract configuration
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"{path}"
'''
                config_path.write_text(config_content)
                logger.info(f"Tesseract path configured: {path}")
                return True
        
        logger.warning("Could not find Tesseract installation")
        return False
    
    def run_setup(self):
        """Run complete setup"""
        logger.info(f"Starting setup for {self.system}")
        
        # Install Python packages
        if not self.install_python_packages():
            logger.error("Python package installation failed")
            return False
        
        # Install system dependencies
        tesseract_installed = False
        
        if self.system == "Windows":
            tesseract_installed = self.install_tesseract_windows()
        elif self.system == "Darwin":
            tesseract_installed = self.install_tesseract_macos()
        elif self.system == "Linux":
            tesseract_installed = self.install_tesseract_linux()
        
        # Verify installation
        if not self.verify_tesseract_installation():
            logger.warning("Tesseract verification failed, checking paths...")
            self.setup_tesseract_path()
        
        # Test OCR functionality
        try:
            from ocr_engine import OCREngine
            ocr = OCREngine()
            if ocr.is_available():
                logger.info("✅ OCR setup completed successfully!")
                return True
            else:
                logger.warning("⚠️  OCR engine setup incomplete")
                logger.info("You can still use basic document conversion without OCR")
                return True
        except Exception as e:
            logger.error(f"OCR engine test failed: {e}")
            return False
    
    def print_instructions(self):
        """Print manual installation instructions"""
        print("\n" + "="*60)
        print("OCR DOCUMENT CONVERTER - SETUP INSTRUCTIONS")
        print("="*60)
        
        if self.system == "Windows":
            print("""
Windows Setup:
1. Install Tesseract OCR:
   - Via winget: winget install tesseract-ocr.tesseract-ocr
   - Via chocolatey: choco install tesseract -y
   - Manual: Download from https://github.com/tesseract-ocr/tesseract/releases

2. Verify installation:
   - Open Command Prompt
   - Run: tesseract --version
   - Should show version 5.x

3. Python packages:
   - Run: python -m pip install -r requirements_updated.txt
            """)
        
        elif self.system == "Darwin":
            print("""
macOS Setup:
1. Install Tesseract OCR:
   - Via homebrew: brew install tesseract

2. Verify installation:
   - Open Terminal
   - Run: tesseract --version
   - Should show version 5.x

3. Python packages:
   - Run: python3 -m pip install -r requirements_updated.txt
            """)
        
        elif self.system == "Linux":
            print("""
Linux Setup:
1. Install Tesseract OCR:
   - Ubuntu/Debian: sudo apt-get install tesseract-ocr
   - CentOS/RHEL: sudo yum install tesseract
   - Arch: sudo pacman -S tesseract

2. Verify installation:
   - Open Terminal
   - Run: tesseract --version
   - Should show version 5.x

3. Python packages:
   - Run: python3 -m pip install -r requirements_updated.txt
            """)
        
        print("\n" + "="*60)
        print("USAGE")
        print("="*60)
        print("Command Line:")
        print("  python convert_to_markdown.py input.pdf")
        print("  python convert_recursive.py /path/to/folder")
        print()
        print("GUI:")
        print("  python universal_document_converter.py")
        print()
        print("For help:")
        print("  python cli.py --help")

if __name__ == "__main__":
    setup = OCRSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        setup.print_instructions()
    else:
        print("Starting OCR Document Converter setup...")
        setup.run()
        setup.print_instructions()