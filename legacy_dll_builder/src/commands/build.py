#!/usr/bin/env python3
"""
Legacy DLL Builder - Build Commands
Extracted from universal_document_converter.py legacy functionality
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import logging

class DLLBuilder:
    """Handles DLL building and compilation"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.dll_paths = [
            Path("dist/UniversalConverter32.dll"),
            Path("dll_source/UniversalConverter32.dll"),
            Path("UniversalConverter32.dll")
        ]
        
    def check_dll_status(self) -> Dict[str, Any]:
        """Check the status of the DLL build and installation"""
        self.logger.info("Checking DLL status...")
        
        dll_found = False
        dll_path = None
        
        for path in self.dll_paths:
            if path.exists():
                dll_found = True
                dll_path = path
                break
        
        status = {
            'found': dll_found,
            'path': dll_path,
            'size_kb': 0,
            'modified': None
        }
        
        if dll_found:
            stat = dll_path.stat()
            status['size_kb'] = stat.st_size / 1024
            status['modified'] = stat.st_mtime
            self.logger.info(f"✅ DLL found at: {dll_path}")
            self.logger.info(f"   Size: {status['size_kb']:.1f} KB")
        else:
            self.logger.warning("⚠️ DLL not found - use 'build' command to create it")
        
        # Check for required source files
        required_files = [
            "dll_source/UniversalConverter32.cpp",
            "dll_source/UniversalConverter32.def",
            "build_dll.bat"
        ]
        
        for file in required_files:
            if Path(file).exists():
                self.logger.info(f"✅ Source: {file}")
            else:
                self.logger.warning(f"❌ Missing: {file}")
        
        return status
    
    def build_dll(self) -> bool:
        """Build the 32-bit DLL using the build script"""
        self.logger.info("Building UniversalConverter32.dll...")
        
        try:
            # Check if running on Windows
            if sys.platform != "win32":
                self.logger.error("❌ DLL building requires Windows")
                self.logger.error("   Transfer files to Windows system and run build_dll.bat")
                return False
            
            # Check for build script
            build_script = Path("build_dll.bat")
            if not build_script.exists():
                self.logger.error("❌ build_dll.bat not found")
                return False
            
            # Run build script
            def build_thread():
                try:
                    process = subprocess.Popen(
                        ["build_dll.bat"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        shell=True
                    )
                    
                    # Stream output
                    while True:
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                            break
                        if output:
                            self.logger.info(output.strip())
                    
                    # Check result
                    if process.returncode == 0:
                        self.logger.info("✅ DLL build completed successfully!")
                        return True
                    else:
                        self.logger.error(f"❌ DLL build failed with code {process.returncode}")
                        return False
                        
                except Exception as e:
                    self.logger.error(f"❌ Build error: {str(e)}")
                    return False
            
            return build_thread()
            
        except Exception as e:
            self.logger.error(f"❌ Error starting build: {str(e)}")
            return False
    
    def open_dll_source(self) -> bool:
        """Open the DLL source directory"""
        try:
            source_dir = Path("dll_source")
            if source_dir.exists():
                if sys.platform == "win32":
                    os.startfile(source_dir)
                elif sys.platform == "darwin":
                    subprocess.run(["open", source_dir])
                else:
                    subprocess.run(["xdg-open", source_dir])
                
                self.logger.info(f"📁 Opened source directory: {source_dir.absolute()}")
                return True
            else:
                self.logger.error("❌ DLL source directory not found")
                return False
        except Exception as e:
            self.logger.error(f"❌ Error opening directory: {str(e)}")
            return False
    
    def show_build_requirements(self) -> str:
        """Show DLL build requirements"""
        requirements = """
DLL Build Requirements:

Windows Requirements:
• Visual Studio Build Tools or Visual C++
• Windows SDK
• 32-bit compilation support

Build Process:
1. Ensure Visual Studio tools are in PATH
2. Open Command Prompt as Administrator
3. Run: build_dll.bat
4. Result: UniversalConverter32.dll

Verification:
• DLL should be ~50-200 KB in size
• Test with: test_dll_integration.py
• Import into VB6/VFP9 projects

Notes:
• Requires Python CLI (cli.py) in same directory
• cli.py must be in same directory as DLL
"""
        return requirements
    
    def create_dll_package(self) -> bool:
        """Create distribution package for DLL"""
        self.logger.info("📦 Creating DLL distribution package...")
        
        try:
            # Run packaging script
            result = subprocess.run(
                [sys.executable, "create_executable.py"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("✅ Distribution package created successfully!")
                self.logger.info(result.stdout)
                
                # Check package size
                package_path = Path("dist/UniversalConverter32.dll.zip")
                if package_path.exists():
                    size_kb = package_path.stat().st_size / 1024
                    self.logger.info(f"📦 Package: {package_path} ({size_kb:.1f} KB)")
                
                return True
            else:
                self.logger.error("❌ Package creation failed")
                self.logger.error(result.stderr)
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Package creation error: {str(e)}")
            return False
    
    def install_dll_system(self) -> bool:
        """Install DLL system-wide"""
        self.logger.info("⚙️ Installing DLL system-wide...")
        
        try:
            # Find DLL
            dll_path = None
            for path in [Path("dist/UniversalConverter32.dll"), Path("UniversalConverter32.dll")]:
                if path.exists():
                    dll_path = path
                    break
            
            if not dll_path:
                self.logger.error("❌ DLL not found - build it first")
                return False
            
            # Check if running on Windows
            if sys.platform != "win32":
                self.logger.error("❌ System-wide installation requires Windows")
                return False
            
            # Copy DLL to System32 (requires admin rights)
            system32 = Path(os.environ.get('SYSTEMROOT', 'C:\\Windows')) / "System32"
            target = system32 / "UniversalConverter32.dll"
            
            try:
                shutil.copy2(dll_path, target)
                self.logger.info(f"✅ DLL installed to: {target}")
                self.logger.info("   DLL is now available system-wide")
                return True
            except PermissionError:
                self.logger.error("❌ Installation failed - run as Administrator")
                return False
            except Exception as e:
                self.logger.error(f"❌ Installation error: {str(e)}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ System installation error: {str(e)}")
            return False