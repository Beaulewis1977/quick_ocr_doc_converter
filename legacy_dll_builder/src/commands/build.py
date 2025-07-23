#!/usr/bin/env python3
"""
Legacy DLL Builder - Build Commands
Extracted from universal_document_converter.py legacy functionality
"""

import os
import sys
import subprocess
import shutil
import platform
import json
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List
import logging
import time

class DLLBuilder:
    """Handles DLL building and compilation with improved subprocess management"""
    
    def __init__(self, logger: Optional[logging.Logger] = None, config: Optional[Dict[str, Any]] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.config = config or {}
        self.timeout = self.config.get('build_timeout', 300)  # 5 minutes default
        self.dll_paths = [
            Path("dist") / "UniversalConverter32.dll",
            Path("dll_source") / "UniversalConverter32.dll",
            Path("UniversalConverter32.dll")
        ]
        self.compiler_info = None
        
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
            
            # Detect compiler if not already done
            if not self.compiler_info:
                compiler_found, message = self._detect_compiler()
                if not compiler_found:
                    self.logger.error(f"❌ {message}")
                    self._show_compiler_help()
                    return False
                self.logger.info(f"✅ {message}")
            
            # Build based on detected compiler
            if self.compiler_info.get('type') == 'visual_studio':
                return self._build_with_visual_studio()
            elif self.compiler_info.get('type') == 'build_script':
                return self._build_with_script()
            else:
                self.logger.error("❌ No supported build method found")
                return False
            
        except Exception as e:
            self.logger.error(f"❌ Error starting build: {str(e)}")
            return False
    
    def open_dll_source(self) -> bool:
        """Open the DLL source directory"""
        try:
            source_dir = Path("dll_source")
            if source_dir.exists():
                if sys.platform == "win32":
                    subprocess.run(["explorer", str(source_dir)], check=False)
                elif sys.platform == "darwin":
                    subprocess.run(["open", str(source_dir)], check=False)
                else:
                    subprocess.run(["xdg-open", str(source_dir)], check=False)
                
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
• Requires Python CLI (document_converter_cli.py) in same directory
• document_converter_cli.py must be in same directory as DLL
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
    
    def _detect_compiler(self) -> Tuple[bool, str]:
        """Detect available compiler with improved checks"""
        # Check for Visual Studio
        vs_info = self._find_visual_studio()
        if vs_info:
            self.compiler_info = {'type': 'visual_studio', **vs_info}
            return True, f"Found Visual Studio {vs_info['version']}"
        
        # Check for build script
        if Path("build_dll.bat").exists():
            self.compiler_info = {'type': 'build_script'}
            return True, "Found build_dll.bat script"
        
        # Check for MinGW
        if self._check_mingw():
            self.compiler_info = {'type': 'mingw'}
            return True, "Found MinGW compiler"
        
        return False, "No compatible compiler found"
    
    def _find_visual_studio(self) -> Optional[Dict[str, str]]:
        """Find Visual Studio installation"""
        vs_paths = [
            Path(r"C:\Program Files (x86)\Microsoft Visual Studio"),
            Path(r"C:\Program Files\Microsoft Visual Studio")
        ]
        
        for base_path in vs_paths:
            if not base_path.exists():
                continue
            
            for year in ["2022", "2019", "2017"]:
                vs_path = base_path / year
                if vs_path.exists():
                    # Find vcvarsall.bat
                    for edition in ["Community", "Professional", "Enterprise"]:
                        vcvars = vs_path / edition / "VC" / "Auxiliary" / "Build" / "vcvarsall.bat"
                        if vcvars.exists():
                            return {
                                "version": year,
                                "edition": edition,
                                "path": str(vs_path),
                                "vcvarsall": str(vcvars)
                            }
        return None
    
    def _check_mingw(self) -> bool:
        """Check if MinGW is available"""
        try:
            result = subprocess.run(
                ["gcc", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _build_with_visual_studio(self) -> bool:
        """Build using Visual Studio with proper error handling"""
        self.logger.info("Building with Visual Studio...")
        
        vcvarsall = self.compiler_info['vcvarsall']
        source_dir = Path("dll_source")
        
        # Build command with proper escaping
        build_cmd = [
            "cmd", "/c",
            f'"{vcvarsall}" x86 && cl /LD /Fe"UniversalConverter32.dll" "UniversalConverter32.cpp" /DEF:"UniversalConverter32.def"'
        ]
        
        try:
            # Run build with timeout
            start_time = time.time()
            process = subprocess.run(
                build_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=source_dir
            )
            
            elapsed = time.time() - start_time
            
            if process.returncode == 0:
                self.logger.info(f"✅ Build completed in {elapsed:.1f}s")
                
                # Copy DLL to expected locations
                dll_source = source_dir / "UniversalConverter32.dll"
                if dll_source.exists():
                    for dest in [Path("."), Path("dist")]:
                        dest.mkdir(exist_ok=True)
                        shutil.copy2(dll_source, dest / "UniversalConverter32.dll")
                return True
            else:
                self.logger.error("❌ Build failed")
                if process.stdout:
                    self.logger.error(f"Output: {process.stdout}")
                if process.stderr:
                    self.logger.error(f"Error: {process.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"❌ Build timeout exceeded ({self.timeout}s)")
            return False
        except Exception as e:
            self.logger.error(f"❌ Build error: {str(e)}")
            return False
    
    def _build_with_script(self) -> bool:
        """Build using build_dll.bat script with improved handling"""
        self.logger.info("Building with build_dll.bat script...")
        
        try:
            # Run build script with proper subprocess handling
            process = subprocess.run(
                ["cmd", "/c", "build_dll.bat"],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            # Log output
            if process.stdout:
                for line in process.stdout.splitlines():
                    self.logger.info(line)
            
            if process.returncode == 0:
                self.logger.info("✅ Build completed successfully")
                return True
            else:
                self.logger.error(f"❌ Build failed with code {process.returncode}")
                if process.stderr:
                    self.logger.error(f"Error: {process.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"❌ Build timeout exceeded ({self.timeout}s)")
            return False
        except Exception as e:
            self.logger.error(f"❌ Build error: {str(e)}")
            return False
    
    def _show_compiler_help(self):
        """Show helpful compiler installation instructions"""
        self.logger.info("\n📋 Compiler Installation Help:")
        self.logger.info("\nOption 1: Visual Studio Build Tools")
        self.logger.info("  1. Download from: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022")
        self.logger.info("  2. Install with 'Desktop development with C++' workload")
        self.logger.info("  3. Include 'MSVC v143 - VS 2022 C++ x64/x86 build tools'")
        self.logger.info("\nOption 2: MinGW-w64")
        self.logger.info("  1. Download from: https://www.mingw-w64.org/downloads/")
        self.logger.info("  2. Install with i686 (32-bit) support")
        self.logger.info("  3. Add to PATH")
        self.logger.info("\nOption 3: Use existing build_dll.bat")
        self.logger.info("  Ensure build_dll.bat is in the current directory")