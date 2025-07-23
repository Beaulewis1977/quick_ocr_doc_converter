#!/usr/bin/env python3
"""
Legacy 32-bit DLL builder for VB6/VFP9
Clean CLI interface with proper command structure and error handling
"""

import click
import sys
import os
import subprocess
import shutil
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def secure_dll_load(dll_path: Path) -> Optional[object]:
    """
    Securely load a DLL with path validation and basic verification
    
    Args:
        dll_path: Path to the DLL file
        
    Returns:
        DLL handle if successful, None otherwise
    """
    if sys.platform != "win32":
        logger.warning("DLL loading only supported on Windows")
        return None
        
    try:
        # Validate path
        resolved_path = dll_path.resolve()
        if not resolved_path.exists():
            logger.error(f"DLL file not found: {resolved_path}")
            return None
            
        if not resolved_path.is_file():
            logger.error(f"Path is not a file: {resolved_path}")
            return None
            
        # Check file extension
        if resolved_path.suffix.lower() != '.dll':
            logger.error(f"File is not a DLL: {resolved_path}")
            return None
            
        # Basic file size check (reasonable bounds)
        file_size = resolved_path.stat().st_size
        if file_size < 1024 or file_size > 50 * 1024 * 1024:  # 1KB to 50MB
            logger.error(f"DLL file size suspicious: {file_size} bytes")
            return None
            
        # Ensure we're loading from absolute path
        import ctypes
        dll_handle = ctypes.WinDLL(str(resolved_path))
        logger.info(f"Successfully loaded DLL: {resolved_path}")
        return dll_handle
        
    except Exception as e:
        logger.error(f"Failed to load DLL {dll_path}: {e}")
        return None


class CompilerDetector:
    """Detect and validate compiler tools"""
    
    @staticmethod
    def find_visual_studio() -> Optional[Dict[str, str]]:
        """Find Visual Studio installation"""
        # Check common VS paths
        vs_paths = [
            r"C:\Program Files (x86)\Microsoft Visual Studio",
            r"C:\Program Files\Microsoft Visual Studio"
        ]
        
        for base_path in vs_paths:
            if not os.path.exists(base_path):
                continue
                
            # Look for VS versions (2019, 2022, etc)
            for year in ["2022", "2019", "2017"]:
                vs_path = os.path.join(base_path, year)
                if os.path.exists(vs_path):
                    # Find vcvarsall.bat
                    vcvars_paths = [
                        os.path.join(vs_path, "Community", "VC", "Auxiliary", "Build", "vcvarsall.bat"),
                        os.path.join(vs_path, "Professional", "VC", "Auxiliary", "Build", "vcvarsall.bat"),
                        os.path.join(vs_path, "Enterprise", "VC", "Auxiliary", "Build", "vcvarsall.bat")
                    ]
                    
                    for vcvars in vcvars_paths:
                        if os.path.exists(vcvars):
                            return {
                                "version": year,
                                "path": vs_path,
                                "vcvarsall": vcvars
                            }
        
        return None
    
    @staticmethod
    def check_mingw() -> bool:
        """Check if MinGW is available"""
        try:
            result = subprocess.run(["gcc", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError, OSError):
            return False


class DLLBuilder:
    """Handles DLL building with proper subprocess management"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.compiler_info = None
        self.timeout = self.config.get('timeout', 300)  # 5 minutes default
        
    def detect_compiler(self) -> Tuple[bool, str]:
        """Detect available compiler"""
        # Check for Visual Studio
        vs_info = CompilerDetector.find_visual_studio()
        if vs_info:
            self.compiler_info = vs_info
            return True, f"Visual Studio {vs_info['version']} found"
        
        # Check for MinGW
        if CompilerDetector.check_mingw():
            self.compiler_info = {"type": "mingw"}
            return True, "MinGW compiler found"
        
        return False, "No compatible compiler found"
    
    def build_with_vs(self, source_dir: Path, output_file: Path) -> Tuple[bool, str]:
        """Build DLL using Visual Studio"""
        if not self.compiler_info:
            return False, "Visual Studio not detected"
        
        vcvarsall = self.compiler_info['vcvarsall']
        
        # Validate and escape file paths for security
        import shlex
        try:
            vcvarsall_escaped = shlex.quote(str(vcvarsall))
            output_file_escaped = shlex.quote(str(output_file))
            cpp_file_escaped = shlex.quote(str(source_dir / "UniversalConverter32.cpp"))
            def_file_escaped = shlex.quote(str(source_dir / "UniversalConverter32.def"))
        except Exception as e:
            return False, f"Path validation failed: {e}"
        
        # Create build command with escaped paths
        build_cmd = f'{vcvarsall_escaped} x86 && cl /LD /Fe:{output_file_escaped} {cpp_file_escaped} /DEF:{def_file_escaped}'
        
        try:
            # Run build with timeout - need shell=True for vcvarsall to work
            process = subprocess.run(
                ["cmd", "/c", build_cmd],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=source_dir
            )
            
            if process.returncode == 0:
                return True, "Build successful"
            else:
                return False, f"Build failed: {process.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, f"Build timeout exceeded ({self.timeout}s)"
        except Exception as e:
            return False, f"Build error: {str(e)}"
    
    def build_with_mingw(self, source_dir: Path, output_file: Path) -> Tuple[bool, str]:
        """Build DLL using MinGW"""
        build_cmd = [
            "g++",
            "-shared",
            "-m32",  # 32-bit
            "-o", str(output_file),
            str(source_dir / "UniversalConverter32.cpp"),
            f"-Wl,--def,{source_dir / 'UniversalConverter32.def'}"
        ]
        
        try:
            process = subprocess.run(
                build_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=source_dir
            )
            
            if process.returncode == 0:
                return True, "Build successful"
            else:
                return False, f"Build failed: {process.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, f"Build timeout exceeded ({self.timeout}s)"
        except Exception as e:
            return False, f"Build error: {str(e)}"


class ErrorReporter:
    """Provide helpful error messages and fixes"""
    
    ERROR_FIXES = {
        "compiler not found": {
            "message": "No C++ compiler detected",
            "fixes": [
                "Install Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022",
                "Or install MinGW: https://www.mingw-w64.org/downloads/",
                "Ensure compiler is in PATH"
            ]
        },
        "32-bit support": {
            "message": "32-bit compilation support missing",
            "fixes": [
                "For Visual Studio: Install 'MSVC v143 - VS 2022 C++ x64/x86 build tools' in Visual Studio Installer",
                "For MinGW: Install mingw-w64 with i686 support"
            ]
        },
        "dll not found": {
            "message": "DLL source files missing",
            "fixes": [
                "Ensure dll_source/UniversalConverter32.cpp exists",
                "Ensure dll_source/UniversalConverter32.def exists",
                "Run from the legacy_dll_builder directory"
            ]
        },
        "python not found": {
            "message": "Python CLI not accessible from DLL",
            "fixes": [
                "Ensure Python is in system PATH",
                "Copy document_converter_cli.py to the same directory as the DLL",
                "Use absolute paths in DLL configuration"
            ]
        }
    }
    
    @classmethod
    def get_error_help(cls, error_type: str) -> Dict[str, Any]:
        """Get helpful error information"""
        return cls.ERROR_FIXES.get(error_type, {
            "message": "Unknown error",
            "fixes": ["Check the error message above", "Consult documentation"]
        })


@click.group()
@click.option('--config', type=click.Path(exists=True), help='Path to configuration file')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """Legacy 32-bit DLL builder for VB6/VFP9"""
    ctx.ensure_object(dict)
    
    # Load configuration
    if config:
        with open(config, 'r') as f:
            ctx.obj['config'] = json.load(f)
    else:
        ctx.obj['config'] = {}
    
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    ctx.obj['builder'] = DLLBuilder(ctx.obj['config'])


@cli.command()
@click.option('--source', type=click.Path(exists=True), default='dll_source', help='Source directory path')
@click.option('--output', type=click.Path(), default='UniversalConverter32.dll', help='Output DLL path')
@click.option('--compiler', type=click.Choice(['auto', 'vs', 'mingw']), default='auto', help='Compiler type')
@click.option('--timeout', type=int, default=300, help='Build timeout in seconds')
@click.pass_context
def build(ctx, source, output, compiler, timeout):
    """Build 32-bit DLL from source"""
    builder = ctx.obj['builder']
    builder.timeout = timeout
    
    source_path = Path(source)
    output_path = Path(output)
    
    # Check source files
    if not (source_path / "UniversalConverter32.cpp").exists():
        click.echo(click.style("Error: Source file not found", fg='red'))
        error_info = ErrorReporter.get_error_help("dll not found")
        click.echo(f"\n{error_info['message']}")
        for fix in error_info['fixes']:
            click.echo(f"  • {fix}")
        ctx.exit(1)
    
    # Detect compiler
    if compiler == 'auto':
        found, message = builder.detect_compiler()
        if not found:
            click.echo(click.style("Error: No compiler found", fg='red'))
            error_info = ErrorReporter.get_error_help("compiler not found")
            click.echo(f"\n{error_info['message']}")
            for fix in error_info['fixes']:
                click.echo(f"  • {fix}")
            ctx.exit(1)
        click.echo(f"Detected: {message}")
    
    # Build based on compiler type
    click.echo(f"Building DLL from {source_path}...")
    
    if builder.compiler_info and builder.compiler_info.get('version'):
        success, message = builder.build_with_vs(source_path, output_path)
    else:
        success, message = builder.build_with_mingw(source_path, output_path)
    
    if success:
        click.echo(click.style(f"✅ Build successful: {output_path}", fg='green'))
        # Verify file size
        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            click.echo(f"   Size: {size_kb:.1f} KB")
    else:
        click.echo(click.style(f"❌ Build failed: {message}", fg='red'))
        ctx.exit(1)


@cli.command()
@click.option('--dll-path', type=click.Path(), help='Path to DLL to verify')
def verify_tools(dll_path):
    """Verify compiler tools are available"""
    click.echo("Checking build tools...")
    
    # Check Visual Studio
    vs_info = CompilerDetector.find_visual_studio()
    if vs_info:
        click.echo(click.style(f"✅ Visual Studio {vs_info['version']} found", fg='green'))
        click.echo(f"   Path: {vs_info['path']}")
    else:
        click.echo(click.style("❌ Visual Studio not found", fg='yellow'))
    
    # Check MinGW
    if CompilerDetector.check_mingw():
        click.echo(click.style("✅ MinGW compiler found", fg='green'))
        try:
            result = subprocess.run(["gcc", "--version"], capture_output=True, text=True)
            version_line = result.stdout.split('\n')[0]
            click.echo(f"   Version: {version_line}")
        except (IndexError, AttributeError, subprocess.SubprocessError):
            pass
    else:
        click.echo(click.style("❌ MinGW not found", fg='yellow'))
    
    # Check Python
    click.echo("\nChecking Python environment...")
    click.echo(f"✅ Python {sys.version.split()[0]} ({sys.executable})")
    
    # Check DLL if provided
    if dll_path:
        dll_file = Path(dll_path)
        if dll_file.exists():
            click.echo(click.style(f"\n✅ DLL found: {dll_file}", fg='green'))
            size_kb = dll_file.stat().st_size / 1024
            click.echo(f"   Size: {size_kb:.1f} KB")
            mtime = datetime.fromtimestamp(dll_file.stat().st_mtime)
            click.echo(f"   Modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            click.echo(click.style(f"\n❌ DLL not found: {dll_file}", fg='red'))


@cli.command()
@click.argument('language', type=click.Choice(['vb6', 'vfp9']))
@click.option('--output', type=click.Path(), help='Output file path')
def generate_template(language, output):
    """Generate VB6/VFP9 integration templates"""
    template_dir = Path(__file__).parent / "templates"
    
    if language == 'vb6':
        template_file = template_dir / "VB6_UniversalConverter_Production.bas"
        default_output = "UniversalConverter.bas"
    else:
        template_file = template_dir / "VFP9_UniversalConverter_Production.prg"
        default_output = "UniversalConverter.prg"
    
    if not template_file.exists():
        click.echo(click.style(f"Error: Template not found: {template_file}", fg='red'))
        return
    
    output_path = Path(output) if output else Path(default_output)
    
    try:
        shutil.copy2(template_file, output_path)
        click.echo(click.style(f"✅ Generated {language.upper()} template: {output_path}", fg='green'))
        click.echo(f"   Template includes:")
        click.echo(f"   • Error handling")
        click.echo(f"   • All conversion functions")
        click.echo(f"   • Usage examples")
        click.echo(f"   • Production-ready code")
    except Exception as e:
        click.echo(click.style(f"Error: Failed to generate template: {e}", fg='red'))


@cli.command()
def show_config():
    """Show build configuration options"""
    config_template = {
        "compiler": {
            "type": "auto",
            "timeout": 300,
            "paths": {
                "vs_path": "C:\\Program Files\\Microsoft Visual Studio\\2022",
                "mingw_path": "C:\\mingw64\\bin"
            }
        },
        "dll": {
            "source_dir": "dll_source",
            "output_dir": "dist",
            "name": "UniversalConverter32.dll"
        },
        "python": {
            "executable": "python",
            "cli_path": "document_converter_cli.py"
        }
    }
    
    click.echo("Build Configuration Template:")
    click.echo(json.dumps(config_template, indent=2))
    click.echo("\nSave this to a JSON file and use with --config option")


@cli.command()
@click.option('--dll', type=click.Path(exists=True), help='DLL to test')
@click.option('--test-file', type=click.Path(exists=True), help='Test document')
def test(dll, test_file):
    """Test DLL functionality"""
    if not dll:
        dll = "UniversalConverter32.dll"
    
    dll_path = Path(dll)
    if not dll_path.exists():
        click.echo(click.style(f"Error: DLL not found: {dll}", fg='red'))
        return
    
    click.echo(f"Testing DLL: {dll_path}")
    
    # Basic DLL load test (Windows only)
    if sys.platform == "win32":
        dll_handle = secure_dll_load(dll_path)
        if dll_handle:
            click.echo(click.style("✅ DLL loads successfully", fg='green'))
            
            # Test GetVersion
            try:
                get_version = dll_handle.GetVersion
                get_version.restype = ctypes.c_char_p
                version = get_version().decode('utf-8')
                click.echo(f"   Version: {version}")
            except (AttributeError, OSError, UnicodeDecodeError, Exception):
                click.echo(click.style("⚠️  Could not get version", fg='yellow'))
            
            # Test GetSupportedInputFormats
            try:
                get_formats = dll_handle.GetSupportedInputFormats
                get_formats.restype = ctypes.c_char_p
                formats = get_formats().decode('utf-8')
                click.echo(f"   Input formats: {formats}")
            except (AttributeError, OSError, UnicodeDecodeError, Exception):
                click.echo(click.style("⚠️  Could not get formats", fg='yellow'))
                
        except Exception as e:
            click.echo(click.style(f"❌ DLL load failed: {e}", fg='red'))
    else:
        click.echo(click.style("⚠️  DLL testing requires Windows", fg='yellow'))
    
    # Test file conversion if provided
    if test_file and sys.platform == "win32":
        test_path = Path(test_file)
        output_path = test_path.with_suffix('.txt')
        
        click.echo(f"\nTesting conversion: {test_path} -> {output_path}")
        # Would implement actual conversion test here


if __name__ == '__main__':
    cli()