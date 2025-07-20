"""
macOS Package Building for Quick Document Convertor

This module provides functionality to create macOS packages including
.app bundles and .dmg installers.

Author: Beau Lewis
Project: Quick Document Convertor
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from . import get_app_info, PackagingError
from ..cross_platform.macos_integration import (
    build_app_bundle, create_dmg_installer, setup_macos_integration
)


def create_pyinstaller_bundle(
    script_path: Path,
    output_dir: Path,
    app_name: str = "Quick Document Convertor",
    icon_path: Optional[Path] = None
) -> Path:
    """
    Create macOS app bundle using PyInstaller.
    
    Args:
        script_path: Path to main Python script
        output_dir: Output directory
        app_name: Application name
        icon_path: Path to icon file
    
    Returns:
        Path to created app bundle
    
    Raises:
        PackagingError: If creation fails
    """
    try:
        # Check if PyInstaller is available
        try:
            import PyInstaller
        except ImportError:
            raise PackagingError("PyInstaller not installed. Install with: pip install pyinstaller")
        
        # PyInstaller command
        cmd = [
            'pyinstaller',
            '--onedir',
            '--windowed',
            '--name', app_name,
            '--distpath', str(output_dir),
            '--workpath', str(output_dir / 'build'),
            '--specpath', str(output_dir),
            '--clean',
            '--noconfirm'
        ]
        
        # Add icon if provided
        if icon_path and icon_path.exists():
            cmd.extend(['--icon', str(icon_path)])
        
        # Add hidden imports for common modules
        hidden_imports = [
            'tkinter', 'tkinter.filedialog', 'tkinter.messagebox',
            'pathlib', 'threading', 'queue', 'logging'
        ]
        for module in hidden_imports:
            cmd.extend(['--hidden-import', module])
        
        # Add the script
        cmd.append(str(script_path))
        
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=output_dir)
        
        if result.returncode != 0:
            raise PackagingError(f"PyInstaller failed: {result.stderr}")
        
        # Return path to app bundle
        app_bundle = output_dir / 'dist' / f"{app_name}.app"
        if not app_bundle.exists():
            raise PackagingError("App bundle not created by PyInstaller")
        
        return app_bundle
    
    except Exception as e:
        raise PackagingError(f"Failed to create PyInstaller bundle: {e}")


def create_standalone_dmg(
    app_bundle: Path,
    output_path: Path,
    volume_name: str = "Quick Document Convertor",
    background_image: Optional[Path] = None
) -> Path:
    """
    Create a professional DMG installer with custom layout.
    
    Args:
        app_bundle: Path to .app bundle
        output_path: Output path for DMG
        volume_name: Volume name for DMG
        background_image: Optional background image
    
    Returns:
        Path to created DMG
    
    Raises:
        PackagingError: If creation fails
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create DMG contents directory
            dmg_contents = temp_path / "dmg_contents"
            dmg_contents.mkdir()
            
            # Copy app bundle
            app_dest = dmg_contents / app_bundle.name
            shutil.copytree(app_bundle, app_dest)
            
            # Create Applications symlink
            apps_link = dmg_contents / "Applications"
            apps_link.symlink_to("/Applications")
            
            # Create README file
            readme_content = f"""Quick Document Convertor

Installation Instructions:
1. Drag "{app_bundle.name}" to the Applications folder
2. Launch the application from Applications or Spotlight
3. The application will be available in your Dock and Launchpad

Features:
- Convert documents between multiple formats
- Batch processing support
- Modern GUI interface
- Cross-platform compatibility

For support, visit: https://github.com/Beaulewis1977/quick_doc_convertor

© 2024 Beau Lewis. All rights reserved.
"""
            
            readme_file = dmg_contents / "README.txt"
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # Create temporary DMG
            temp_dmg = temp_path / "temp.dmg"
            
            # Calculate size needed (rough estimate)
            size_mb = 200  # Base size
            try:
                # Get actual size of contents
                result = subprocess.run(['du', '-sm', str(dmg_contents)], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    actual_size = int(result.stdout.split()[0])
                    size_mb = max(size_mb, actual_size + 50)  # Add 50MB buffer
            except (subprocess.SubprocessError, ValueError):
                pass
            
            # Create temporary DMG
            result = subprocess.run([
                'hdiutil', 'create',
                '-srcfolder', str(dmg_contents),
                '-volname', volume_name,
                '-fs', 'HFS+',
                '-fsargs', '-c c=64,a=16,e=16',
                '-format', 'UDRW',
                '-size', f'{size_mb}m',
                str(temp_dmg)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise PackagingError(f"Failed to create temporary DMG: {result.stderr}")
            
            # Mount the DMG
            result = subprocess.run([
                'hdiutil', 'attach', str(temp_dmg), '-readwrite', '-noverify', '-noautoopen'
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise PackagingError(f"Failed to mount DMG: {result.stderr}")
            
            # Extract mount point
            mount_point = None
            for line in result.stdout.split('\n'):
                if '/Volumes/' in line:
                    mount_point = line.split()[-1]
                    break
            
            if not mount_point:
                raise PackagingError("Could not determine mount point")
            
            try:
                # Set up DMG appearance using AppleScript
                applescript = f'''
tell application "Finder"
    tell disk "{volume_name}"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {{100, 100, 600, 400}}
        set theViewOptions to the icon view options of container window
        set arrangement of theViewOptions to not arranged
        set icon size of theViewOptions to 128
        set position of item "{app_bundle.name}" of container window to {{150, 200}}
        set position of item "Applications" of container window to {{350, 200}}
        close
        open
        update without registering applications
        delay 2
    end tell
end tell
'''
                
                # Run AppleScript
                subprocess.run(['osascript', '-e', applescript], 
                             capture_output=True, text=True)
                
                # Sync and unmount
                subprocess.run(['sync'], check=True)
                subprocess.run(['hdiutil', 'detach', mount_point], 
                             capture_output=True)
                
                # Convert to compressed DMG
                result = subprocess.run([
                    'hdiutil', 'convert', str(temp_dmg),
                    '-format', 'UDZO',
                    '-imagekey', 'zlib-level=9',
                    '-o', str(output_path)
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise PackagingError(f"Failed to compress DMG: {result.stderr}")
                
            except Exception as e:
                # Try to unmount in case of error
                try:
                    subprocess.run(['hdiutil', 'detach', mount_point], 
                                 capture_output=True)
                except subprocess.SubprocessError:
                    pass
                raise e
        
        return output_path
    
    except Exception as e:
        raise PackagingError(f"Failed to create DMG: {e}")


def create_pkg_installer(
    app_bundle: Path,
    output_path: Path,
    identifier: str = "com.beaulewis.quickdocumentconvertor",
    version: str = "2.0.0"
) -> Path:
    """
    Create a .pkg installer for macOS.
    
    Args:
        app_bundle: Path to .app bundle
        output_path: Output path for .pkg
        identifier: Package identifier
        version: Package version
    
    Returns:
        Path to created .pkg
    
    Raises:
        PackagingError: If creation fails
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create package root
            pkg_root = temp_path / "pkg_root"
            pkg_root.mkdir()
            
            # Create Applications directory in package
            apps_dir = pkg_root / "Applications"
            apps_dir.mkdir()
            
            # Copy app bundle
            app_dest = apps_dir / app_bundle.name
            shutil.copytree(app_bundle, app_dest)
            
            # Create component property list
            component_plist = temp_path / "component.plist"
            plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>BundleHasStrictIdentifier</key>
    <true/>
    <key>BundleIsRelocatable</key>
    <false/>
    <key>BundleIsVersionChecked</key>
    <true/>
    <key>BundleOverwriteAction</key>
    <string>upgrade</string>
    <key>RootRelativeBundlePath</key>
    <string>Applications/{app_bundle.name}</string>
</dict>
</plist>'''
            
            with open(component_plist, 'w') as f:
                f.write(plist_content)
            
            # Build package
            result = subprocess.run([
                'pkgbuild',
                '--root', str(pkg_root),
                '--component-plist', str(component_plist),
                '--identifier', identifier,
                '--version', version,
                '--install-location', '/',
                str(output_path)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise PackagingError(f"pkgbuild failed: {result.stderr}")
        
        return output_path
    
    except Exception as e:
        raise PackagingError(f"Failed to create .pkg installer: {e}")


def build_all_macos_packages(
    script_path: Path,
    output_dir: Path,
    version: str = "2.0.0",
    icon_path: Optional[Path] = None
) -> Dict[str, Path]:
    """
    Build all macOS package formats.
    
    Args:
        script_path: Path to main Python script
        output_dir: Output directory for packages
        version: Application version
        icon_path: Path to icon file
    
    Returns:
        Dict mapping package type to file path
    """
    results = {}
    
    try:
        # Create app bundle using PyInstaller
        app_bundle = create_pyinstaller_bundle(script_path, output_dir, icon_path=icon_path)
        results['app_bundle'] = app_bundle
    except Exception as e:
        results['app_bundle_error'] = str(e)
        return results
    
    try:
        # Create DMG installer
        dmg_path = output_dir / f"QuickDocumentConvertor-{version}.dmg"
        dmg_result = create_standalone_dmg(app_bundle, dmg_path)
        results['dmg'] = dmg_result
    except Exception as e:
        results['dmg_error'] = str(e)
    
    try:
        # Create PKG installer
        pkg_path = output_dir / f"QuickDocumentConvertor-{version}.pkg"
        pkg_result = create_pkg_installer(app_bundle, pkg_path, version=version)
        results['pkg'] = pkg_result
    except Exception as e:
        results['pkg_error'] = str(e)
    
    return results


__all__ = [
    'create_pyinstaller_bundle',
    'create_standalone_dmg',
    'create_pkg_installer',
    'build_all_macos_packages'
]
