#!/usr/bin/env python3
"""
Install requirements for OCR Document Converter
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {cmd}")
            return True
        else:
            print(f"❌ {cmd}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {cmd}")
        print(f"Exception: {e}")
        return False

def install_requirements():
    """Install requirements from requirements.txt"""
    print("Installing requirements...")
    
    # Try different Python commands
    python_commands = ['python', 'python3', 'py']
    
    for python_cmd in python_commands:
        if run_command(f"{python_cmd} --version"):
            print(f"Using Python command: {python_cmd}")
            
            # Install requirements
            if run_command(f"{python_cmd} -m pip install -r requirements.txt"):
                print("✅ Requirements installed successfully")
                return True
            else:
                print("❌ Failed to install requirements")
                return False
    
    print("❌ No Python command found")
    return False

def install_tkinterdnd2():
    """Install tkinterdnd2 specifically"""
    print("Installing tkinterdnd2...")
    
    # Try different Python commands
    python_commands = ['python', 'python3', 'py']
    
    for python_cmd in python_commands:
        if run_command(f"{python_cmd} --version"):
            print(f"Using Python command: {python_cmd}")
            
            # Install tkinterdnd2
            if run_command(f"{python_cmd} -m pip install tkinterdnd2"):
                print("✅ tkinterdnd2 installed successfully")
                return True
            else:
                print("❌ Failed to install tkinterdnd2")
                return False
    
    print("❌ No Python command found")
    return False

def main():
    """Main function"""
    print("="*60)
    print("OCR DOCUMENT CONVERTER - REQUIREMENTS INSTALLER")
    print("="*60)
    
    success = True
    
    # Install tkinterdnd2 first
    if not install_tkinterdnd2():
        success = False
    
    # Install other requirements
    if not install_requirements():
        success = False
    
    print("="*60)
    if success:
        print("✅ All requirements installed successfully!")
        print("You can now run the OCR applications.")
    else:
        print("❌ Some requirements failed to install.")
        print("Please check the error messages above.")
    print("="*60)

if __name__ == "__main__":
    main()