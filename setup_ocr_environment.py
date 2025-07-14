#!/usr/bin/env python3
"""
OCR Environment Setup Script
Automatically installs all required dependencies for the OCR-enhanced document converter
"""

import os
import sys
import subprocess
import platform
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCRSetup:
    """Automated setup for OCR environment"""
    
    def __init__(self):
        self.system = platform.system()
        self.python_executable = sys.executable
        self.pip_executable = f"{self.python_executable} -m pip"
        
    def run_command(self, command, shell=True):
        """Run system command with error handling"""
        try:
            logger.info(f"Running: {command}")
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Command completed successfully")
                return True
            else:
                logger.error(f"Command failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error running command: {e}")
            return False
    
    def install_python_packages(self):
        """Install required Python packages"""
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
            "weasyprint",
            "markdown",
            "beautifulsoup4"
        ]
        
        success_count = 0
        for package in packages:
            command = f"{self.pip_executable} install {package}"
            if self.run_command(command):
                success_count += 1
        
        logger.info(f"Installed {success_count}/{len(packages)} Python packages")
        return success_count == len(packages)
    
    def install_system_dependencies(self):
        """Install system-level dependencies"""
        if self.system == "Windows":
            return self.install_windows_dependencies()
        elif self.system == "Darwin":  # macOS
            return self.install_macos_dependencies()
        elif self.system == "Linux":
            return self.install_linux_dependencies()
        else:
            logger.error(f"Unsupported system: {self.system}")
            return False
    
    def install_windows_dependencies(self):
        """Install Windows-specific dependencies"""
        logger.info("Setting up Windows dependencies...")
        
        # Check if Tesseract is installed
        tesseract_paths = [
            "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
            "C:\\Users\\%USERNAME%\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
        ]
        
        tesseract_found = False
        for path in tesseract_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                tesseract_found = True
                logger.info(f"Tesseract found at: {expanded_path}")
                break
        
        if not tesseract_found:
            logger.warning("Tesseract not found. Please install from:")
            logger.warning("https://github.com/UB-Mannheim/tesseract/wiki")
            return False
        
        return True
    
    def install_macos_dependencies(self):
        """Install macOS-specific dependencies"""
        logger.info("Setting up macOS dependencies...")
        
        # Check if Homebrew is available
        if not self.run_command("which brew"):
            logger.error("Homebrew not found. Please install from https://brew.sh")
            return False
        
        # Install Tesseract
        commands = [
            "brew install tesseract",
            "brew install tesseract-lang"  # Language packs
        ]
        
        success = True
        for cmd in commands:
            if not self.run_command(cmd):
                success = False
        
        return success
    
    def install_linux_dependencies(self):
        """Install Linux-specific dependencies"""
        logger.info("Setting up Linux dependencies...")
        
        # Detect package manager
        package_managers = {
            'apt-get': 'sudo apt-get update && sudo apt-get install -y tesseract-ocr tesseract-ocr-eng libtesseract-dev',
            'yum': 'sudo yum install -y tesseract tesseract-langpack-eng',
            'dnf': 'sudo dnf install -y tesseract tesseract-langpack-eng'
        }
        
        for pm, cmd in package_managers.items():
            if self.run_command(f"which {pm}"):
                return self.run_command(cmd)
        
        logger.error("No supported package manager found")
        return False
    
    def verify_installation(self):
        """Verify all components are installed correctly"""
        checks = [
            ("Python packages", self.verify_python_packages),
            ("Tesseract", self.verify_tesseract),
            ("OCR Engine", self.verify_ocr_engine)
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            if check_func():
                logger.info(f"✅ {check_name}: OK")
            else:
                logger.error(f"❌ {check_name}: FAILED")
                all_passed = False
        
        return all_passed
    
    def verify_python_packages(self):
        """Verify Python packages are installed"""
        packages = [
            'pytesseract',
            'PIL',
            'numpy',
            'cv2',
            'easyocr'
        ]
        
        missing = []
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            logger.error(f"Missing Python packages: {missing}")
            return False
        
        return True
    
    def verify_tesseract(self):
        """Verify Tesseract is installed and accessible"""
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            return True
        except Exception as e:
            logger.error(f"Tesseract verification failed: {e}")
            return False
    
    def verify_ocr_engine(self):
        """Verify OCR engine is working"""
        try:
            from ocr_engine.ocr_engine import OCREngine
            
            engine = OCREngine()
            return hasattr(engine, 'extract_text')
        except Exception as e:
            logger.error(f"OCR engine verification failed: {e}")
            return False
    
    def create_environment_file(self):
        """Create environment configuration file"""
        env_config = {
            "system": platform.system(),
            "python_version": platform.python_version(),
            "tesseract_path": self.get_tesseract_path(),
            "setup_date": platform.uname()._asdict()
        }
        
        with open("ocr_environment.json", "w") as f:
            json.dump(env_config, f, indent=2)
        
        logger.info("Environment configuration saved to ocr_environment.json")
    
    def get_tesseract_path(self):
        """Get Tesseract executable path"""
        if self.system == "Windows":
            possible_paths = [
                "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
                "C:\\Users\\{}\\AppData\\Local\\Tesseract-OCR\\tesseract.exe".format(os.getenv('USERNAME'))
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return path
        
        elif self.system in ["Darwin", "Linux"]:
            try:
                result = subprocess.run(["which", "tesseract"], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
                pass
        
        return "tesseract"
    
    def run_setup(self):
        """Run complete setup process"""
        logger.info("=" * 60)
        logger.info("OCR Environment Setup")
        logger.info("=" * 60)
        logger.info(f"System: {self.system}")
        logger.info(f"Python: {self.python_executable}")
        
        steps = [
            ("System Dependencies", self.install_system_dependencies),
            ("Python Packages", self.install_python_packages),
            ("Verification", self.verify_installation),
            ("Environment Config", self.create_environment_file)
        ]
        
        success_count = 0
        for step_name, step_func in steps:
            logger.info(f"\n--- {step_name} ---")
            if step_func():
                success_count += 1
                logger.info(f"✅ {step_name} completed successfully")
            else:
                logger.error(f"❌ {step_name} failed")
        
        logger.info("\n" + "=" * 60)
        logger.info("SETUP SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Steps Completed: {success_count}/{len(steps)}")
        
        if success_count == len(steps):
            logger.info("🎉 OCR environment setup completed successfully!")
            logger.info("You can now run: python validate_ocr_integration.py")
            return True
        else:
            logger.error("❌ Some setup steps failed. Please check the logs.")
            return False

def main():
    """Main setup function"""
    setup = OCRSetup()
    return setup.run_setup()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)