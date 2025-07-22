"""
Windows Integration for Quick Document Convertor

This module provides enhanced Windows-specific functionality including
improved shortcuts, file associations, and MSI package creation.

Author: Beau Lewis
Project: Quick Document Convertor
"""

import os
import subprocess
import sys
import winreg
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import get_platform, get_data_dir, get_config_dir


class WindowsIntegrationError(Exception):
    """Custom exception for Windows integration errors."""
    pass


def is_windows() -> bool:
    """
    Check if running on Windows.
    
    Returns:
        bool: True if on Windows
    """
    return get_platform() == 'windows'


def get_start_menu_dir() -> Path:
    """
    Get the Start Menu programs directory.
    
    Returns:
        Path to Start Menu programs directory
    """
    return Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"


def get_desktop_dir() -> Path:
    """
    Get the Desktop directory.
    
    Returns:
        Path to Desktop directory
    """
    return Path.home() / "Desktop"


def create_enhanced_shortcuts(
    app_path: Path,
    app_name: str = "Quick Document Convertor",
    description: str = "Enterprise document conversion tool",
    icon_path: Optional[Path] = None
) -> Dict[str, bool]:
    """
    Create enhanced Windows shortcuts with proper file associations.
    
    Args:
        app_path: Path to application executable
        app_name: Application name
        description: Application description
        icon_path: Path to icon file
    
    Returns:
        Dict with creation status
    """
    if not is_windows():
        raise WindowsIntegrationError("Not running on Windows")
    
    results = {}
    
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        
        # Desktop shortcut
        desktop_shortcut = get_desktop_dir() / f"{app_name}.lnk"
        shortcut = shell.CreateShortCut(str(desktop_shortcut))
        shortcut.Targetpath = str(app_path)
        shortcut.WorkingDirectory = str(app_path.parent)
        shortcut.Description = description
        if icon_path and icon_path.exists():
            shortcut.IconLocation = str(icon_path)
        shortcut.save()
        results["desktop"] = desktop_shortcut.exists()
        
        # Start Menu shortcut
        start_menu_shortcut = get_start_menu_dir() / f"{app_name}.lnk"
        shortcut = shell.CreateShortCut(str(start_menu_shortcut))
        shortcut.Targetpath = str(app_path)
        shortcut.WorkingDirectory = str(app_path.parent)
        shortcut.Description = description
        if icon_path and icon_path.exists():
            shortcut.IconLocation = str(icon_path)
        shortcut.save()
        results["start_menu"] = start_menu_shortcut.exists()
        
        return results
    
    except ImportError:
        raise WindowsIntegrationError("pywin32 not available")
    except Exception as e:
        raise WindowsIntegrationError(f"Failed to create shortcuts: {e}")


def register_file_associations(
    app_path: Path,
    app_name: str = "Quick Document Convertor",
    extensions: Optional[List[str]] = None
) -> Dict[str, bool]:
    """
    Register file associations in Windows registry.
    
    Args:
        app_path: Path to application executable
        app_name: Application name
        extensions: List of file extensions to associate
    
    Returns:
        Dict with registration status for each extension
    """
    if not is_windows():
        raise WindowsIntegrationError("Not running on Windows")
    
    if extensions is None:
        extensions = ['.pdf', '.docx', '.txt', '.html', '.rtf', '.epub', '.odt', '.csv']
    
    results = {}
    
    try:
        for ext in extensions:
            try:
                # Create file type key
                file_type = f"QuickDocConvertor{ext[1:].upper()}"
                
                # Register file extension
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{ext}") as key:
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, file_type)
                
                # Register file type
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\{file_type}") as key:
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f"{ext.upper()} File")
                
                # Register open command
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                    f"Software\\Classes\\{file_type}\\shell\\open\\command") as key:
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{app_path}" "%1"')
                
                # Register "Convert with Quick Document Convertor" context menu
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                    f"Software\\Classes\\{file_type}\\shell\\convert") as key:
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f"Convert with {app_name}")
                
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                                    f"Software\\Classes\\{file_type}\\shell\\convert\\command") as key:
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'"{app_path}" "%1"')
                
                results[ext] = True
            
            except Exception as e:
                results[ext] = False
                results[f"{ext}_error"] = str(e)
        
        return results
    
    except Exception as e:
        raise WindowsIntegrationError(f"Failed to register file associations: {e}")


def create_uninstaller(
    app_dir: Path,
    app_name: str = "Quick Document Convertor",
    version: str = "3.1.0"
) -> Path:
    """
    Create an uninstaller script for Windows.
    
    Args:
        app_dir: Application directory
        app_name: Application name
        version: Application version
    
    Returns:
        Path to uninstaller script
    """
    if not is_windows():
        raise WindowsIntegrationError("Not running on Windows")
    
    uninstaller_content = f'''@echo off
echo Uninstalling {app_name}...

REM Remove shortcuts
del "%USERPROFILE%\\Desktop\\{app_name}.lnk" 2>nul
del "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{app_name}.lnk" 2>nul

REM Remove file associations
reg delete "HKCU\\Software\\Classes\\.pdf" /f 2>nul
reg delete "HKCU\\Software\\Classes\\.docx" /f 2>nul
reg delete "HKCU\\Software\\Classes\\.txt" /f 2>nul
reg delete "HKCU\\Software\\Classes\\.html" /f 2>nul
reg delete "HKCU\\Software\\Classes\\.rtf" /f 2>nul
reg delete "HKCU\\Software\\Classes\\.epub" /f 2>nul
reg delete "HKCU\\Software\\Classes\\.odt" /f 2>nul
reg delete "HKCU\\Software\\Classes\\.csv" /f 2>nul

REM Remove application files
echo Removing application files...
rmdir /s /q "{app_dir}" 2>nul

echo {app_name} has been uninstalled.
pause
'''
    
    uninstaller_path = app_dir / "uninstall.bat"
    with open(uninstaller_path, 'w', encoding='utf-8') as f:
        f.write(uninstaller_content)
    
    return uninstaller_path


def add_to_programs_list(
    app_path: Path,
    app_name: str = "Quick Document Convertor",
    version: str = "3.1.0",
    publisher: str = "Beau Lewis",
    uninstaller_path: Optional[Path] = None
) -> bool:
    """
    Add application to Windows Programs and Features list.
    
    Args:
        app_path: Path to application executable
        app_name: Application name
        version: Application version
        publisher: Publisher name
        uninstaller_path: Path to uninstaller
    
    Returns:
        bool: True if successful
    """
    if not is_windows():
        return False
    
    try:
        # Register in Programs and Features
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                            f"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}") as key:
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, app_name)
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, version)
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, publisher)
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(app_path.parent))
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, str(app_path))
            
            if uninstaller_path:
                winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, str(uninstaller_path))
        
        return True
    
    except Exception:
        return False


def create_installer_script(
    app_dir: Path,
    app_name: str = "Quick Document Convertor",
    version: str = "3.1.0"
) -> Path:
    """
    Create a Windows installer script.
    
    Args:
        app_dir: Application directory
        app_name: Application name
        version: Application version
    
    Returns:
        Path to installer script
    """
    if not is_windows():
        raise WindowsIntegrationError("Not running on Windows")
    
    installer_content = f'''@echo off
echo Installing {app_name} {version}...

REM Create application directory
if not exist "{app_dir}" mkdir "{app_dir}"

REM Copy application files (this would be done by the actual installer)
echo Copying application files...

REM Create shortcuts
echo Creating shortcuts...
python "{app_dir}\\setup_shortcuts.py"

REM Register file associations
echo Registering file associations...
python -c "from cross_platform.windows_integration import register_file_associations; from pathlib import Path; register_file_associations(Path('{app_dir}\\universal_document_converter.py'))"

REM Add to Programs and Features
echo Adding to Programs and Features...
python -c "from cross_platform.windows_integration import add_to_programs_list; from pathlib import Path; add_to_programs_list(Path('{app_dir}\\universal_document_converter.py'))"

echo {app_name} has been installed successfully!
echo You can find it in the Start Menu or on your Desktop.
pause
'''
    
    installer_path = app_dir.parent / f"install_{app_name.replace(' ', '_')}.bat"
    with open(installer_path, 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    return installer_path


def setup_windows_integration(
    app_path: Path,
    icon_path: Optional[Path] = None
) -> Dict[str, any]:
    """
    Set up complete Windows integration.
    
    Args:
        app_path: Path to application executable
        icon_path: Path to icon file
    
    Returns:
        Dict with results of integration steps
    """
    if not is_windows():
        return {"error": "Not running on Windows"}
    
    results = {}
    
    try:
        # Create enhanced shortcuts
        shortcuts = create_enhanced_shortcuts(app_path, icon_path=icon_path)
        results["shortcuts"] = shortcuts
    except Exception as e:
        results["shortcuts"] = {"error": str(e)}
    
    try:
        # Register file associations
        associations = register_file_associations(app_path)
        results["file_associations"] = associations
    except Exception as e:
        results["file_associations"] = {"error": str(e)}
    
    try:
        # Create uninstaller
        uninstaller = create_uninstaller(app_path.parent)
        results["uninstaller"] = str(uninstaller)
        results["uninstaller_created"] = uninstaller.exists()
    except Exception as e:
        results["uninstaller_created"] = False
        results["uninstaller_error"] = str(e)
    
    try:
        # Add to Programs and Features
        programs_list = add_to_programs_list(app_path)
        results["programs_list"] = programs_list
    except Exception as e:
        results["programs_list"] = False
        results["programs_list_error"] = str(e)
    
    return results


def check_windows_dependencies() -> Dict[str, bool]:
    """
    Check if Windows integration dependencies are available.
    
    Returns:
        Dict with dependency availability
    """
    dependencies = {
        'pywin32': False,
        'winreg': True,  # Built-in module
        'registry_access': False
    }
    
    # Check pywin32
    try:
        import win32com.client
        dependencies['pywin32'] = True
    except ImportError:
        pass
    
    # Check registry access
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software") as key:
            dependencies['registry_access'] = True
    except Exception:
        pass
    
    return dependencies


__all__ = [
    'WindowsIntegrationError',
    'is_windows',
    'get_start_menu_dir',
    'get_desktop_dir',
    'create_enhanced_shortcuts',
    'register_file_associations',
    'create_uninstaller',
    'add_to_programs_list',
    'create_installer_script',
    'setup_windows_integration',
    'check_windows_dependencies'
]
