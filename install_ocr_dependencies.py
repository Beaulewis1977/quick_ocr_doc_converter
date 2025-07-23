#!/usr/bin/env python3
"""
OCR Dependencies Installation Script
Installs required Python packages and configures Tesseract OCR
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and handle errors"""
    print(f"Running: {command}")
    if description:
        print(f"  {description}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            return True
        else:
            print(f"❌ Failed: {description}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("=" * 60)
    print("INSTALLING PYTHON DEPENDENCIES")
    print("=" * 60)
    
    # Try different python commands
    python_commands = ['python3', 'python', 'py']
    pip_commands = ['pip3', 'pip']
    
    python_cmd = None
    pip_cmd = None
    
    # Find working python command
    for cmd in python_commands:
        if run_command(f"{cmd} --version", f"Testing {cmd}"):
            python_cmd = cmd
            break
    
    if not python_cmd:
        print("❌ No working Python installation found")
        return False
    
    # Find working pip command
    for cmd in pip_commands:
        if run_command(f"{cmd} --version", f"Testing {cmd}"):
            pip_cmd = cmd
            break
    
    if not pip_cmd:
        print("❌ No working pip installation found")
        return False
    
    print(f"Using Python: {python_cmd}")
    print(f"Using pip: {pip_cmd}")
    
    # Install dependencies
    dependencies = [
        "pytesseract>=0.3.10",
        "Pillow>=9.0.0", 
        "numpy>=1.21.0",
        "opencv-python>=4.5.0",
        "easyocr>=1.6.0",
        "tkinterdnd2>=0.3.0",
        "python-docx>=0.8.11",
        "psutil>=5.9.0"
    ]
    
    success_count = 0
    for dep in dependencies:
        if run_command(f"{pip_cmd} install {dep}", f"Installing {dep}"):
            success_count += 1
        else:
            print(f"⚠️  Failed to install {dep}, trying to continue...")
    
    print(f"\nInstalled {success_count}/{len(dependencies)} dependencies")
    return success_count > 0

def check_tesseract_installation():
    """Check if Tesseract is installed"""
    print("=" * 60)
    print("CHECKING TESSERACT INSTALLATION")
    print("=" * 60)
    
    system = platform.system().lower()
    
    if system == "windows":
        # Common Tesseract installation paths on Windows
        common_paths = [
            "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
            "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
            "C:\\Tools\\tesseract\\tesseract.exe",
            "C:\\tesseract\\tesseract.exe"
        ]
        
        tesseract_path = None
        for path in common_paths:
            if os.path.exists(path):
                tesseract_path = path
                break
        
        if tesseract_path:
            print(f"✅ Tesseract found at: {tesseract_path}")
            return tesseract_path
        else:
            print("❌ Tesseract not found in common locations")
            print("Please install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
            return None
            
    else:
        # Linux/macOS
        if run_command("tesseract --version", "Testing Tesseract"):
            return "tesseract"
        else:
            print("❌ Tesseract not found")
            print("Please install Tesseract:")
            print("  Ubuntu/Debian: sudo apt-get install tesseract-ocr")
            print("  macOS: brew install tesseract")
            return None

def configure_tesseract():
    """Configure Tesseract OCR settings"""
    print("=" * 60)
    print("CONFIGURING TESSERACT OCR")
    print("=" * 60)
    
    tesseract_path = check_tesseract_installation()
    if not tesseract_path:
        return False
    
    system = platform.system().lower()
    
    if system == "windows":
        # Set up Windows-specific configuration
        tesseract_dir = os.path.dirname(tesseract_path)
        tessdata_dir = os.path.join(tesseract_dir, "tessdata")
        
        print(f"Tesseract directory: {tesseract_dir}")
        print(f"Tessdata directory: {tessdata_dir}")
        
        if os.path.exists(tessdata_dir):
            print("✅ Tessdata directory found")
            
            # Create configuration file
            config_content = f'''# Tesseract OCR Configuration
import pytesseract
import os

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"{tesseract_path}"

# Set tessdata path
os.environ["TESSDATA_PREFIX"] = r"{tessdata_dir}"

print("Tesseract configured successfully")
print(f"Tesseract path: {tesseract_path}")
print(f"Tessdata path: {tessdata_dir}")
'''
            
            with open("tesseract_config.py", "w") as f:
                f.write(config_content)
            
            print("✅ Created tesseract_config.py")
            
            # Create a simple test script
            test_script = '''import sys
sys.path.insert(0, ".")
import tesseract_config

try:
    import pytesseract
    from PIL import Image
    import numpy as np
    
    # Test Tesseract version
    version = pytesseract.get_tesseract_version()
    print(f"Tesseract version: {version}")
    
    # Test language data
    languages = pytesseract.get_languages()
    print(f"Available languages: {languages}")
    
    print("✅ Tesseract configuration test passed")
except Exception as e:
    print(f"❌ Tesseract configuration test failed: {e}")
'''
            
            with open("test_tesseract_config.py", "w") as f:
                f.write(test_script)
            
            print("✅ Created test_tesseract_config.py")
            return True
        else:
            print(f"❌ Tessdata directory not found: {tessdata_dir}")
            return False
    else:
        print("✅ Tesseract configured for Linux/macOS")
        return True

def create_ocr_engine_fix():
    """Create a fixed version of OCR engine that handles Tesseract configuration"""
    print("=" * 60)
    print("CREATING OCR ENGINE FIX")
    print("=" * 60)
    
    system = platform.system().lower()
    
    if system == "windows":
        # Create a Windows-specific OCR engine fix
        fix_content = '''#!/usr/bin/env python3
"""
OCR Engine Fix for Windows Tesseract Configuration
"""

import os
import sys
from pathlib import Path

def configure_tesseract_windows():
    """Configure Tesseract for Windows"""
    # Common Tesseract paths
    tesseract_paths = [
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Tools\\tesseract\\tesseract.exe",
        r"C:\\tesseract\\tesseract.exe"
    ]
    
    tesseract_path = None
    tessdata_path = None
    
    for path in tesseract_paths:
        if os.path.exists(path):
            tesseract_path = path
            tessdata_path = os.path.join(os.path.dirname(path), "tessdata")
            break
    
    if tesseract_path and os.path.exists(tessdata_path):
        try:
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            os.environ["TESSDATA_PREFIX"] = tessdata_path
            print(f"✅ Tesseract configured: {tesseract_path}")
            print(f"✅ Tessdata path set: {tessdata_path}")
            return True
        except ImportError:
            print("❌ pytesseract not installed")
            return False
    else:
        print("❌ Tesseract not found or tessdata missing")
        return False

# Apply configuration automatically when imported
if __name__ == "__main__":
    configure_tesseract_windows()
else:
    # Auto-configure when imported
    import platform
    if platform.system().lower() == "windows":
        configure_tesseract_windows()
'''
        
        with open("ocr_engine_fix.py", "w") as f:
            f.write(fix_content)
        
        print("✅ Created ocr_engine_fix.py for Windows")
        return True
    else:
        print("✅ No OCR engine fix needed for Linux/macOS")
        return True

def main():
    """Main installation process"""
    print("=" * 60)
    print("OCR DEPENDENCIES INSTALLATION")
    print("=" * 60)
    
    success_count = 0
    total_steps = 4
    
    # Step 1: Install Python dependencies
    if install_python_dependencies():
        success_count += 1
    
    # Step 2: Check Tesseract installation
    if check_tesseract_installation():
        success_count += 1
    
    # Step 3: Configure Tesseract
    if configure_tesseract():
        success_count += 1
    
    # Step 4: Create OCR engine fix
    if create_ocr_engine_fix():
        success_count += 1
    
    print("\n" + "=" * 60)
    print(f"INSTALLATION COMPLETE: {success_count}/{total_steps} steps successful")
    print("=" * 60)
    
    if success_count == total_steps:
        print("✅ OCR system should now be ready!")
        print("\nNext steps:")
        print("1. Test the installation: python3 test_all_fixes.py")
        print("2. Run Complete GUI: python3 universal_document_converter.py")
        print("3. Run Universal Converter: python3 universal_document_converter_ocr.py")
    else:
        print(f"❌ {total_steps - success_count} steps failed")
        print("Please check the errors above and resolve them manually.")
    
    return success_count == total_steps

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)