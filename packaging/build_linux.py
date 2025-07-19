"""
Linux Package Building for Quick Document Convertor

This module provides functionality to create Linux packages including
.deb, .rpm, and AppImage formats.

Author: Beau Lewis
Project: Quick Document Convertor
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from . import get_app_info, get_supported_formats, get_mime_types, PackagingError


def create_deb_package(
    app_dir: Path,
    output_dir: Path,
    version: str = "2.0.0",
    architecture: str = "all"
) -> Path:
    """
    Create a .deb package for Debian/Ubuntu systems.
    
    Args:
        app_dir: Directory containing the application
        output_dir: Output directory for the package
        version: Package version
        architecture: Target architecture
    
    Returns:
        Path to created .deb package
    
    Raises:
        PackagingError: If package creation fails
    """
    app_info = get_app_info()
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create package structure
            pkg_dir = temp_path / "quick-document-convertor"
            pkg_dir.mkdir()
            
            # DEBIAN control directory
            debian_dir = pkg_dir / "DEBIAN"
            debian_dir.mkdir()
            
            # Application directory
            app_dest = pkg_dir / "opt" / "quick-document-convertor"
            app_dest.mkdir(parents=True)
            
            # Copy application files
            shutil.copytree(app_dir, app_dest, dirs_exist_ok=True)
            
            # Create control file
            control_content = f"""Package: quick-document-convertor
Version: {version}
Section: office
Priority: optional
Architecture: {architecture}
Depends: python3 (>= 3.8), python3-tk, python3-pip
Maintainer: {app_info['author']} <{app_info['email']}>
Description: {app_info['description']}
 Enterprise document conversion tool that supports multiple formats
 including PDF, DOCX, HTML, Markdown, and more. Features a modern
 GUI interface and batch processing capabilities.
Homepage: {app_info['url']}
"""
            
            with open(debian_dir / "control", 'w') as f:
                f.write(control_content)
            
            # Create postinst script
            postinst_content = """#!/bin/bash
set -e

# Create desktop entry
python3 /opt/quick-document-convertor/cross_platform/linux_integration.py

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database ~/.local/share/applications
fi

# Update MIME database
if command -v update-mime-database >/dev/null 2>&1; then
    update-mime-database ~/.local/share/mime
fi

exit 0
"""
            
            postinst_file = debian_dir / "postinst"
            with open(postinst_file, 'w') as f:
                f.write(postinst_content)
            postinst_file.chmod(0o755)
            
            # Create prerm script
            prerm_content = """#!/bin/bash
set -e

# Remove desktop entries
rm -f ~/.local/share/applications/quick-document-convertor.desktop
rm -f ~/Desktop/Quick\\ Document\\ Convertor.desktop

exit 0
"""
            
            prerm_file = debian_dir / "prerm"
            with open(prerm_file, 'w') as f:
                f.write(prerm_content)
            prerm_file.chmod(0o755)
            
            # Create launcher script
            launcher_dir = pkg_dir / "usr" / "local" / "bin"
            launcher_dir.mkdir(parents=True)
            
            launcher_content = f"""#!/bin/bash
cd /opt/quick-document-convertor
python3 universal_document_converter.py "$@"
"""
            
            launcher_file = launcher_dir / "quick-document-convertor"
            with open(launcher_file, 'w') as f:
                f.write(launcher_content)
            launcher_file.chmod(0o755)
            
            # Build package
            output_file = output_dir / f"quick-document-convertor_{version}_{architecture}.deb"
            
            result = subprocess.run([
                'dpkg-deb', '--build', str(pkg_dir), str(output_file)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise PackagingError(f"dpkg-deb failed: {result.stderr}")
            
            return output_file
    
    except Exception as e:
        raise PackagingError(f"Failed to create .deb package: {e}")


def create_rpm_package(
    app_dir: Path,
    output_dir: Path,
    version: str = "2.0.0",
    architecture: str = "noarch"
) -> Path:
    """
    Create an .rpm package for Red Hat/CentOS/Fedora systems.
    
    Args:
        app_dir: Directory containing the application
        output_dir: Output directory for the package
        version: Package version
        architecture: Target architecture
    
    Returns:
        Path to created .rpm package
    
    Raises:
        PackagingError: If package creation fails
    """
    app_info = get_app_info()
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create RPM build structure
            rpm_build = temp_path / "rpmbuild"
            for subdir in ["BUILD", "RPMS", "SOURCES", "SPECS", "SRPMS"]:
                (rpm_build / subdir).mkdir(parents=True)
            
            # Create source tarball
            source_dir = temp_path / f"quick-document-convertor-{version}"
            shutil.copytree(app_dir, source_dir)
            
            tarball = rpm_build / "SOURCES" / f"quick-document-convertor-{version}.tar.gz"
            subprocess.run([
                'tar', '-czf', str(tarball), '-C', str(temp_path),
                f"quick-document-convertor-{version}"
            ], check=True)
            
            # Create spec file
            spec_content = f"""Name:           quick-document-convertor
Version:        {version}
Release:        1%{{?dist}}
Summary:        {app_info['description']}

License:        {app_info['license']}
URL:            {app_info['url']}
Source0:        %{{name}}-%{{version}}.tar.gz

BuildArch:      {architecture}
Requires:       python3 >= 3.8, python3-tkinter

%description
Enterprise document conversion tool that supports multiple formats
including PDF, DOCX, HTML, Markdown, and more. Features a modern
GUI interface and batch processing capabilities.

%prep
%setup -q

%build
# No build required for Python application

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/quick-document-convertor
cp -r * $RPM_BUILD_ROOT/opt/quick-document-convertor/

# Create launcher script
mkdir -p $RPM_BUILD_ROOT/usr/local/bin
cat > $RPM_BUILD_ROOT/usr/local/bin/quick-document-convertor << 'EOF'
#!/bin/bash
cd /opt/quick-document-convertor
python3 universal_document_converter.py "$@"
EOF
chmod +x $RPM_BUILD_ROOT/usr/local/bin/quick-document-convertor

%files
/opt/quick-document-convertor
/usr/local/bin/quick-document-convertor

%post
# Create desktop entry
if [ -x /opt/quick-document-convertor/cross_platform/linux_integration.py ]; then
    python3 /opt/quick-document-convertor/cross_platform/linux_integration.py
fi

%preun
# Remove desktop entries
rm -f ~/.local/share/applications/quick-document-convertor.desktop
rm -f ~/Desktop/Quick\\ Document\\ Convertor.desktop

%changelog
* Wed Jan 01 2025 {app_info['author']} <{app_info['email']}> - {version}-1
- Initial RPM package
"""
            
            spec_file = rpm_build / "SPECS" / "quick-document-convertor.spec"
            with open(spec_file, 'w') as f:
                f.write(spec_content)
            
            # Build RPM
            result = subprocess.run([
                'rpmbuild', '--define', f'_topdir {rpm_build}',
                '-ba', str(spec_file)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise PackagingError(f"rpmbuild failed: {result.stderr}")
            
            # Find and copy the built RPM
            rpm_files = list((rpm_build / "RPMS" / architecture).glob("*.rpm"))
            if not rpm_files:
                raise PackagingError("No RPM file was created")
            
            output_file = output_dir / rpm_files[0].name
            shutil.copy2(rpm_files[0], output_file)
            
            return output_file
    
    except Exception as e:
        raise PackagingError(f"Failed to create .rpm package: {e}")


def create_appimage(
    app_dir: Path,
    output_dir: Path,
    version: str = "2.0.0"
) -> Path:
    """
    Create an AppImage for universal Linux distribution.
    
    Args:
        app_dir: Directory containing the application
        output_dir: Output directory for the AppImage
        version: Application version
    
    Returns:
        Path to created AppImage
    
    Raises:
        PackagingError: If AppImage creation fails
    """
    app_info = get_app_info()
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create AppDir structure
            app_dir_name = "QuickDocumentConvertor.AppDir"
            appdir = temp_path / app_dir_name
            appdir.mkdir()
            
            # Copy application
            app_dest = appdir / "opt" / "quick-document-convertor"
            app_dest.mkdir(parents=True)
            shutil.copytree(app_dir, app_dest, dirs_exist_ok=True)
            
            # Create AppRun script
            apprun_content = f"""#!/bin/bash
HERE="$(dirname "$(readlink -f "${{0}}")")"
export APPDIR="$HERE"
export PATH="$HERE/usr/bin:$PATH"
export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"
export PYTHONPATH="$HERE/opt/quick-document-convertor:$PYTHONPATH"

cd "$HERE/opt/quick-document-convertor"
python3 universal_document_converter.py "$@"
"""
            
            apprun_file = appdir / "AppRun"
            with open(apprun_file, 'w') as f:
                f.write(apprun_content)
            apprun_file.chmod(0o755)
            
            # Create desktop file
            desktop_content = f"""[Desktop Entry]
Name={app_info['name']}
Comment={app_info['description']}
Exec=AppRun %F
Icon=quick-document-convertor
Terminal=false
Type=Application
Categories=Office;Utility;
MimeType=application/pdf;application/vnd.openxmlformats-officedocument.wordprocessingml.document;text/plain;text/html;
StartupNotify=true
"""
            
            with open(appdir / "quick-document-convertor.desktop", 'w') as f:
                f.write(desktop_content)
            
            # Create icon (placeholder)
            icon_content = """# Placeholder icon file
# In a real implementation, this would be a proper icon
"""
            with open(appdir / "quick-document-convertor.png", 'w') as f:
                f.write(icon_content)
            
            # Download and use appimagetool
            appimagetool_url = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
            appimagetool = temp_path / "appimagetool"
            
            try:
                # Try to download appimagetool
                subprocess.run([
                    'wget', '-O', str(appimagetool), appimagetool_url
                ], check=True, capture_output=True)
                appimagetool.chmod(0o755)
                
                # Create AppImage
                output_file = output_dir / f"QuickDocumentConvertor-{version}-x86_64.AppImage"
                
                result = subprocess.run([
                    str(appimagetool), str(appdir), str(output_file)
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise PackagingError(f"appimagetool failed: {result.stderr}")
                
                return output_file
            
            except subprocess.CalledProcessError:
                # If appimagetool download fails, create a simple archive
                output_file = output_dir / f"QuickDocumentConvertor-{version}.tar.gz"
                subprocess.run([
                    'tar', '-czf', str(output_file), '-C', str(temp_path), app_dir_name
                ], check=True)
                
                return output_file
    
    except Exception as e:
        raise PackagingError(f"Failed to create AppImage: {e}")


def build_all_linux_packages(
    app_dir: Path,
    output_dir: Path,
    version: str = "2.0.0"
) -> Dict[str, Path]:
    """
    Build all Linux package formats.
    
    Args:
        app_dir: Directory containing the application
        output_dir: Output directory for packages
        version: Application version
    
    Returns:
        Dict mapping package type to file path
    """
    results = {}
    
    try:
        results['deb'] = create_deb_package(app_dir, output_dir, version)
    except Exception as e:
        results['deb_error'] = str(e)
    
    try:
        results['rpm'] = create_rpm_package(app_dir, output_dir, version)
    except Exception as e:
        results['rpm_error'] = str(e)
    
    try:
        results['appimage'] = create_appimage(app_dir, output_dir, version)
    except Exception as e:
        results['appimage_error'] = str(e)
    
    return results


__all__ = [
    'create_deb_package',
    'create_rpm_package',
    'create_appimage',
    'build_all_linux_packages'
]
