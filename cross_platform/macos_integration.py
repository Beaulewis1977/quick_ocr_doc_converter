"""
macOS Integration for Quick Document Convertor

This module provides macOS-specific functionality including .app bundle creation,
Info.plist configuration, and native file associations using UTI.

Author: Beau Lewis
Project: Quick Document Convertor
"""

import os
import plistlib
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import get_platform, get_data_dir, get_config_dir


class MacOSIntegrationError(Exception):
    """Custom exception for macOS integration errors."""
    pass


def is_macos() -> bool:
    """
    Check if running on macOS.
    
    Returns:
        bool: True if on macOS
    """
    return get_platform() == 'macos'


def get_applications_dir() -> Path:
    """
    Get the Applications directory.
    
    Returns:
        Path to Applications directory
    """
    return Path("/Applications")


def get_user_applications_dir() -> Path:
    """
    Get the user Applications directory.
    
    Returns:
        Path to user Applications directory
    """
    return Path.home() / "Applications"


def create_info_plist(
    app_name: str,
    bundle_id: str,
    version: str = "3.1.0",
    executable_name: str = "main",
    icon_file: Optional[str] = None
) -> Dict:
    """
    Create Info.plist dictionary for macOS app bundle.
    
    Args:
        app_name: Application name
        bundle_id: Bundle identifier (reverse domain)
        version: Application version
        executable_name: Name of executable in MacOS folder
        icon_file: Icon file name (without extension)
    
    Returns:
        Dict containing Info.plist data
    """
    if not is_macos():
        raise MacOSIntegrationError("Not running on macOS")
    
    # Document types for file associations
    document_types = [
        {
            'CFBundleTypeName': 'PDF Document',
            'CFBundleTypeExtensions': ['pdf'],
            'CFBundleTypeIconFile': icon_file or 'document.icns',
            'CFBundleTypeRole': 'Viewer',
            'LSItemContentTypes': ['com.adobe.pdf'],
            'LSHandlerRank': 'Alternate'
        },
        {
            'CFBundleTypeName': 'Microsoft Word Document',
            'CFBundleTypeExtensions': ['docx', 'doc'],
            'CFBundleTypeIconFile': icon_file or 'document.icns',
            'CFBundleTypeRole': 'Viewer',
            'LSItemContentTypes': [
                'org.openxmlformats.wordprocessingml.document',
                'com.microsoft.word.doc'
            ],
            'LSHandlerRank': 'Alternate'
        },
        {
            'CFBundleTypeName': 'Plain Text Document',
            'CFBundleTypeExtensions': ['txt'],
            'CFBundleTypeIconFile': icon_file or 'document.icns',
            'CFBundleTypeRole': 'Editor',
            'LSItemContentTypes': ['public.plain-text'],
            'LSHandlerRank': 'Alternate'
        },
        {
            'CFBundleTypeName': 'HTML Document',
            'CFBundleTypeExtensions': ['html', 'htm'],
            'CFBundleTypeIconFile': icon_file or 'document.icns',
            'CFBundleTypeRole': 'Viewer',
            'LSItemContentTypes': ['public.html'],
            'LSHandlerRank': 'Alternate'
        },
        {
            'CFBundleTypeName': 'Rich Text Format',
            'CFBundleTypeExtensions': ['rtf'],
            'CFBundleTypeIconFile': icon_file or 'document.icns',
            'CFBundleTypeRole': 'Viewer',
            'LSItemContentTypes': ['public.rtf'],
            'LSHandlerRank': 'Alternate'
        },
        {
            'CFBundleTypeName': 'EPUB Document',
            'CFBundleTypeExtensions': ['epub'],
            'CFBundleTypeIconFile': icon_file or 'document.icns',
            'CFBundleTypeRole': 'Viewer',
            'LSItemContentTypes': ['org.idpf.epub-container'],
            'LSHandlerRank': 'Alternate'
        },
        {
            'CFBundleTypeName': 'OpenDocument Text',
            'CFBundleTypeExtensions': ['odt'],
            'CFBundleTypeIconFile': icon_file or 'document.icns',
            'CFBundleTypeRole': 'Viewer',
            'LSItemContentTypes': ['org.oasis-open.opendocument.text'],
            'LSHandlerRank': 'Alternate'
        },
        {
            'CFBundleTypeName': 'CSV Document',
            'CFBundleTypeExtensions': ['csv'],
            'CFBundleTypeIconFile': icon_file or 'document.icns',
            'CFBundleTypeRole': 'Viewer',
            'LSItemContentTypes': ['public.comma-separated-values-text'],
            'LSHandlerRank': 'Alternate'
        }
    ]
    
    # URL types for custom protocols
    url_types = [
        {
            'CFBundleURLName': 'Quick Document Convertor Protocol',
            'CFBundleURLSchemes': ['quick-doc-convertor'],
            'CFBundleTypeRole': 'Viewer'
        }
    ]
    
    info_plist = {
        'CFBundleName': app_name,
        'CFBundleDisplayName': app_name,
        'CFBundleIdentifier': bundle_id,
        'CFBundleVersion': version,
        'CFBundleShortVersionString': version,
        'CFBundleExecutable': executable_name,
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': 'QDCV',
        'CFBundleInfoDictionaryVersion': '6.0',
        'LSMinimumSystemVersion': '10.13.0',
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,  # Support Dark Mode
        'CFBundleDocumentTypes': document_types,
        'CFBundleURLTypes': url_types,
        'LSApplicationCategoryType': 'public.app-category.productivity',
        'NSHumanReadableCopyright': f'Copyright © 2024 Beau Lewis. All rights reserved.',
        'CFBundleGetInfoString': f'{app_name} {version}, Copyright © 2024 Beau Lewis',
        'NSSupportsAutomaticGraphicsSwitching': True,
        'LSMultipleInstancesProhibited': False
    }
    
    # Add icon if specified
    if icon_file:
        info_plist['CFBundleIconFile'] = icon_file
    
    return info_plist


def create_py2app_setup(
    script_path: Path,
    app_name: str = "Quick Document Convertor",
    bundle_id: str = "com.beaulewis.quickdocumentconvertor",
    version: str = "3.1.0",
    icon_path: Optional[Path] = None
) -> str:
    """
    Create py2app setup.py content.
    
    Args:
        script_path: Path to main Python script
        app_name: Application name
        bundle_id: Bundle identifier
        version: Application version
        icon_path: Path to icon file
    
    Returns:
        String content for setup.py
    """
    if not is_macos():
        raise MacOSIntegrationError("Not running on macOS")
    
    # Create Info.plist
    plist_data = create_info_plist(
        app_name, bundle_id, version,
        icon_file=icon_path.stem if icon_path else None
    )
    
    setup_content = f'''"""
py2app setup script for {app_name}

Usage:
    python setup_macos.py py2app
"""

from setuptools import setup
import sys

# Application metadata
APP = ['{script_path}']
DATA_FILES = []
OPTIONS = {{
    'py2app': {{
        'iconfile': '{icon_path}' if icon_path else None,
        'plist': {repr(plist_data)},
        'packages': ['tkinter', 'pathlib', 'threading'],
        'includes': ['tkinter.filedialog', 'tkinter.messagebox'],
        'excludes': ['PyQt4', 'PyQt5', 'PyQt6', 'PySide', 'PySide2', 'PySide6'],
        'resources': [],
        'optimize': 2,
        'compressed': True,
        'semi_standalone': False,
        'site_packages': False,
        'strip': True,
        'prefer_ppc': False,
        'debug_modulegraph': False,
        'debug_skip_macholib': False,
        'arch': 'universal2',  # Support both Intel and Apple Silicon
        'codesign_identity': None,  # Set to signing identity for distribution
        'entitlements_file': None,  # Set for sandboxing
    }}
}}

setup(
    name='{app_name}',
    app=APP,
    data_files=DATA_FILES,
    options=OPTIONS,
    setup_requires=['py2app'],
    version='{version}',
    description='Enterprise document conversion tool',
    author='Beau Lewis',
    author_email='blewisxx@gmail.com',
    url='https://github.com/Beaulewis1977/quick_doc_convertor',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ]
)
'''
    
    return setup_content


def build_app_bundle(
    script_path: Path,
    output_dir: Path,
    app_name: str = "Quick Document Convertor",
    icon_path: Optional[Path] = None
) -> Path:
    """
    Build macOS app bundle using py2app.
    
    Args:
        script_path: Path to main Python script
        output_dir: Output directory for app bundle
        app_name: Application name
        icon_path: Path to icon file
    
    Returns:
        Path to created app bundle
    
    Raises:
        MacOSIntegrationError: If build fails
    """
    if not is_macos():
        raise MacOSIntegrationError("Not running on macOS")
    
    try:
        # Check if py2app is available
        try:
            import py2app
        except ImportError:
            raise MacOSIntegrationError("py2app not installed. Install with: pip install py2app")
        
        # Create setup.py content
        setup_content = create_py2app_setup(script_path, app_name, icon_path=icon_path)
        
        # Write setup.py
        setup_file = output_dir / "setup_macos.py"
        with open(setup_file, 'w', encoding='utf-8') as f:
            f.write(setup_content)
        
        # Run py2app
        result = subprocess.run([
            sys.executable, str(setup_file), 'py2app'
        ], cwd=output_dir, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise MacOSIntegrationError(f"py2app build failed: {result.stderr}")
        
        # Return path to app bundle
        app_bundle = output_dir / "dist" / f"{app_name}.app"
        if not app_bundle.exists():
            raise MacOSIntegrationError("App bundle not created")
        
        return app_bundle
    
    except Exception as e:
        raise MacOSIntegrationError(f"Failed to build app bundle: {e}")


def register_file_associations(app_bundle: Path) -> bool:
    """
    Register file associations for the app bundle.
    
    Args:
        app_bundle: Path to .app bundle
    
    Returns:
        bool: True if successful
    """
    if not is_macos() or not app_bundle.exists():
        return False
    
    try:
        # Use Launch Services to register the app
        subprocess.run([
            '/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister',
            '-f', str(app_bundle)
        ], check=True, capture_output=True)
        
        return True
    
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_dmg_installer(
    app_bundle: Path,
    output_path: Path,
    volume_name: str = "Quick Document Convertor"
) -> Path:
    """
    Create DMG installer for the app bundle.
    
    Args:
        app_bundle: Path to .app bundle
        output_path: Output path for DMG
        volume_name: Volume name for DMG
    
    Returns:
        Path to created DMG
    
    Raises:
        MacOSIntegrationError: If creation fails
    """
    if not is_macos():
        raise MacOSIntegrationError("Not running on macOS")
    
    try:
        # Create temporary directory for DMG contents
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Copy app bundle to temp directory
            import shutil
            app_dest = temp_path / app_bundle.name
            shutil.copytree(app_bundle, app_dest)
            
            # Create Applications symlink
            apps_link = temp_path / "Applications"
            apps_link.symlink_to("/Applications")
            
            # Create DMG
            result = subprocess.run([
                'hdiutil', 'create',
                '-volname', volume_name,
                '-srcfolder', str(temp_path),
                '-ov', '-format', 'UDZO',
                str(output_path)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise MacOSIntegrationError(f"DMG creation failed: {result.stderr}")
        
        return output_path
    
    except Exception as e:
        raise MacOSIntegrationError(f"Failed to create DMG: {e}")


def setup_macos_integration(
    script_path: Path,
    output_dir: Path,
    icon_path: Optional[Path] = None
) -> Dict[str, any]:
    """
    Set up complete macOS integration.
    
    Args:
        script_path: Path to main Python script
        output_dir: Output directory
        icon_path: Path to icon file
    
    Returns:
        Dict with results of integration steps
    """
    if not is_macos():
        return {"error": "Not running on macOS"}
    
    results = {}
    
    try:
        # Build app bundle
        app_bundle = build_app_bundle(script_path, output_dir, icon_path=icon_path)
        results["app_bundle"] = str(app_bundle)
        results["app_bundle_created"] = app_bundle.exists()
    except Exception as e:
        results["app_bundle_created"] = False
        results["app_bundle_error"] = str(e)
        return results
    
    # Register file associations
    results["file_associations"] = register_file_associations(app_bundle)
    
    try:
        # Create DMG installer
        dmg_path = output_dir / "Quick Document Convertor.dmg"
        dmg_result = create_dmg_installer(app_bundle, dmg_path)
        results["dmg_installer"] = str(dmg_result)
        results["dmg_created"] = dmg_result.exists()
    except Exception as e:
        results["dmg_created"] = False
        results["dmg_error"] = str(e)
    
    return results


def check_macos_dependencies() -> Dict[str, bool]:
    """
    Check if macOS integration dependencies are available.
    
    Returns:
        Dict with dependency availability
    """
    dependencies = {
        'py2app': False,
        'hdiutil': False,
        'lsregister': False,
        'codesign': False
    }
    
    # Check py2app
    try:
        import py2app
        dependencies['py2app'] = True
    except ImportError:
        pass
    
    # Check command line tools
    commands = {
        'hdiutil': 'hdiutil',
        'lsregister': '/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister',
        'codesign': 'codesign'
    }
    
    for name, cmd in commands.items():
        try:
            subprocess.run([cmd], capture_output=True)
            dependencies[name] = True
        except FileNotFoundError:
            pass
    
    return dependencies


__all__ = [
    'MacOSIntegrationError',
    'is_macos',
    'get_applications_dir',
    'get_user_applications_dir',
    'create_info_plist',
    'create_py2app_setup',
    'build_app_bundle',
    'register_file_associations',
    'create_dmg_installer',
    'setup_macos_integration',
    'check_macos_dependencies'
]
