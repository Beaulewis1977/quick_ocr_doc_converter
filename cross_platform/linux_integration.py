"""
Linux Desktop Integration for Quick Document Convertor

This module provides Linux-specific functionality including .desktop file creation,
MIME type registration, and file manager integration following XDG standards.

Author: Beau Lewis
Project: Quick Document Convertor
"""

import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import get_platform, get_data_dir, get_config_dir


class LinuxIntegrationError(Exception):
    """Custom exception for Linux integration errors."""
    pass


def is_linux() -> bool:
    """
    Check if running on Linux.
    
    Returns:
        bool: True if on Linux
    """
    return get_platform() == 'linux'


def get_applications_dir() -> Path:
    """
    Get the XDG applications directory.
    
    Returns:
        Path to applications directory
    """
    return Path.home() / ".local" / "share" / "applications"


def get_mime_dir() -> Path:
    """
    Get the XDG MIME directory.
    
    Returns:
        Path to MIME directory
    """
    return Path.home() / ".local" / "share" / "mime"


def get_icons_dir() -> Path:
    """
    Get the XDG icons directory.
    
    Returns:
        Path to icons directory
    """
    return Path.home() / ".local" / "share" / "icons"


def create_desktop_file(
    app_name: str,
    app_path: Path,
    icon_path: Optional[Path] = None,
    categories: Optional[List[str]] = None,
    mime_types: Optional[List[str]] = None
) -> Path:
    """
    Create a .desktop file for the application.
    
    Args:
        app_name: Application name
        app_path: Path to application executable
        icon_path: Path to application icon
        categories: Desktop categories
        mime_types: Supported MIME types
    
    Returns:
        Path to created .desktop file
    
    Raises:
        LinuxIntegrationError: If creation fails
    """
    if not is_linux():
        raise LinuxIntegrationError("Not running on Linux")
    
    # Default values
    if categories is None:
        categories = ["Office", "Utility", "TextEditor"]
    
    if mime_types is None:
        mime_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
            "text/html",
            "application/rtf",
            "application/epub+zip",
            "application/vnd.oasis.opendocument.text",
            "text/csv"
        ]
    
    # Create applications directory
    apps_dir = get_applications_dir()
    apps_dir.mkdir(parents=True, exist_ok=True)
    
    # Desktop file content
    desktop_content = f"""[Desktop Entry]
Name={app_name}
Comment=Enterprise document conversion tool
Exec=python3 "{app_path}" %F
Path={app_path.parent}
Icon={icon_path if icon_path else 'text-x-generic'}
Terminal=false
Type=Application
Categories={';'.join(categories)};
MimeType={';'.join(mime_types)};
StartupNotify=true
StartupWMClass={app_name.replace(' ', '')}
Keywords=document;conversion;markdown;pdf;docx;
"""
    
    # Write desktop file
    desktop_file = apps_dir / f"quick-document-convertor.desktop"
    try:
        with open(desktop_file, 'w', encoding='utf-8') as f:
            f.write(desktop_content)
        
        # Make executable
        desktop_file.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        
        return desktop_file
    
    except Exception as e:
        raise LinuxIntegrationError(f"Failed to create desktop file: {e}")


def register_mime_types(mime_types: Optional[List[str]] = None) -> bool:
    """
    Register MIME types for the application.
    
    Args:
        mime_types: List of MIME types to register
    
    Returns:
        bool: True if successful
    
    Raises:
        LinuxIntegrationError: If registration fails
    """
    if not is_linux():
        raise LinuxIntegrationError("Not running on Linux")
    
    if mime_types is None:
        mime_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
            "text/html",
            "application/rtf",
            "application/epub+zip",
            "application/vnd.oasis.opendocument.text",
            "text/csv"
        ]
    
    try:
        # Create MIME directory
        mime_dir = get_mime_dir()
        mime_dir.mkdir(parents=True, exist_ok=True)
        
        # Create packages directory
        packages_dir = mime_dir / "packages"
        packages_dir.mkdir(parents=True, exist_ok=True)
        
        # Create MIME XML file
        mime_xml = packages_dir / "quick-document-convertor.xml"
        
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="application/x-quick-document-convertor">
        <comment>Quick Document Convertor Project</comment>
        <glob pattern="*.qdc"/>
    </mime-type>
</mime-info>
"""
        
        with open(mime_xml, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        # Update MIME database
        try:
            subprocess.run(['update-mime-database', str(mime_dir)], 
                         check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # update-mime-database might not be available or might fail
            # This is not critical for basic functionality
            pass
        
        return True
    
    except Exception as e:
        raise LinuxIntegrationError(f"Failed to register MIME types: {e}")


def update_desktop_database() -> bool:
    """
    Update the desktop database to register the application.
    
    Returns:
        bool: True if successful
    """
    if not is_linux():
        return False
    
    try:
        apps_dir = get_applications_dir()
        subprocess.run(['update-desktop-database', str(apps_dir)], 
                      check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # update-desktop-database might not be available
        # This is not critical for basic functionality
        return False


def install_icon(icon_source: Path, icon_name: str = "quick-document-convertor") -> bool:
    """
    Install application icon to the system.
    
    Args:
        icon_source: Source icon file
        icon_name: Icon name
    
    Returns:
        bool: True if successful
    """
    if not is_linux() or not icon_source.exists():
        return False
    
    try:
        icons_dir = get_icons_dir()
        
        # Determine icon size and format
        if icon_source.suffix.lower() == '.png':
            # Try to determine size from filename or use default
            if '48' in icon_source.name:
                size_dir = icons_dir / "hicolor" / "48x48" / "apps"
            elif '64' in icon_source.name:
                size_dir = icons_dir / "hicolor" / "64x64" / "apps"
            else:
                size_dir = icons_dir / "hicolor" / "48x48" / "apps"
        else:
            # For other formats, use scalable
            size_dir = icons_dir / "hicolor" / "scalable" / "apps"
        
        size_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy icon
        icon_dest = size_dir / f"{icon_name}{icon_source.suffix}"
        import shutil
        shutil.copy2(icon_source, icon_dest)
        
        # Update icon cache
        try:
            subprocess.run(['gtk-update-icon-cache', str(icons_dir / "hicolor")], 
                          check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # gtk-update-icon-cache might not be available
            pass
        
        return True
    
    except Exception:
        return False


def create_file_associations(app_path: Path) -> bool:
    """
    Create file associations for supported formats.
    
    Args:
        app_path: Path to application executable
    
    Returns:
        bool: True if successful
    """
    if not is_linux():
        return False
    
    try:
        # File extensions to associate
        extensions = ['.pdf', '.docx', '.txt', '.html', '.rtf', '.epub', '.odt', '.csv']
        
        for ext in extensions:
            try:
                # Use xdg-mime to set default application
                subprocess.run([
                    'xdg-mime', 'default', 
                    'quick-document-convertor.desktop',
                    f'application/x-{ext[1:]}'
                ], check=False, capture_output=True)
            except FileNotFoundError:
                # xdg-mime might not be available
                pass
        
        return True
    
    except Exception:
        return False


def setup_linux_integration(app_path: Path, icon_path: Optional[Path] = None) -> Dict[str, bool]:
    """
    Set up complete Linux desktop integration.
    
    Args:
        app_path: Path to application executable
        icon_path: Path to application icon
    
    Returns:
        Dict with status of each integration step
    """
    if not is_linux():
        return {"error": "Not running on Linux"}
    
    results = {}
    
    try:
        # Create desktop file
        desktop_file = create_desktop_file(
            "Quick Document Convertor",
            app_path,
            icon_path
        )
        results["desktop_file"] = desktop_file.exists()
    except Exception as e:
        results["desktop_file"] = False
        results["desktop_file_error"] = str(e)
    
    try:
        # Register MIME types
        results["mime_types"] = register_mime_types()
    except Exception as e:
        results["mime_types"] = False
        results["mime_types_error"] = str(e)
    
    # Update desktop database
    results["desktop_database"] = update_desktop_database()
    
    # Install icon
    if icon_path and icon_path.exists():
        results["icon"] = install_icon(icon_path)
    else:
        results["icon"] = False
    
    # Create file associations
    results["file_associations"] = create_file_associations(app_path)
    
    return results


def check_linux_dependencies() -> Dict[str, bool]:
    """
    Check if Linux desktop integration dependencies are available.
    
    Returns:
        Dict with dependency availability
    """
    dependencies = {
        'update-desktop-database': False,
        'update-mime-database': False,
        'xdg-mime': False,
        'gtk-update-icon-cache': False
    }
    
    for cmd in dependencies.keys():
        try:
            subprocess.run([cmd, '--help'], 
                          check=True, capture_output=True)
            dependencies[cmd] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    return dependencies


__all__ = [
    'LinuxIntegrationError',
    'is_linux',
    'get_applications_dir',
    'get_mime_dir',
    'get_icons_dir',
    'create_desktop_file',
    'register_mime_types',
    'update_desktop_database',
    'install_icon',
    'create_file_associations',
    'setup_linux_integration',
    'check_linux_dependencies'
]
