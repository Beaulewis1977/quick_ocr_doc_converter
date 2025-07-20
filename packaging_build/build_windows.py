"""
Windows Package Building for Quick Document Convertor

This module provides enhanced functionality to create Windows packages
including executables and MSI installers.

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


def create_pyinstaller_executable(
    script_path: Path,
    output_dir: Path,
    app_name: str = "Quick Document Convertor",
    icon_path: Optional[Path] = None,
    onefile: bool = False
) -> Path:
    """
    Create Windows executable using PyInstaller.
    
    Args:
        script_path: Path to main Python script
        output_dir: Output directory
        app_name: Application name
        icon_path: Path to icon file
        onefile: Create single file executable
    
    Returns:
        Path to created executable or directory
    
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
            '--windowed',
            '--name', app_name,
            '--distpath', str(output_dir),
            '--workpath', str(output_dir / 'build'),
            '--specpath', str(output_dir),
            '--clean',
            '--noconfirm'
        ]
        
        # Choose between onefile and onedir
        if onefile:
            cmd.append('--onefile')
        else:
            cmd.append('--onedir')
        
        # Add icon if provided
        if icon_path and icon_path.exists():
            cmd.extend(['--icon', str(icon_path)])
        
        # Add hidden imports for common modules
        hidden_imports = [
            'tkinter', 'tkinter.filedialog', 'tkinter.messagebox',
            'pathlib', 'threading', 'queue', 'logging', 'winreg'
        ]
        for module in hidden_imports:
            cmd.extend(['--hidden-import', module])
        
        # Add version info
        app_info = get_app_info()
        version_info = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 0, 0, 0),
    prodvers=(2, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{app_info["author"]}'),
        StringStruct(u'FileDescription', u'{app_info["description"]}'),
        StringStruct(u'FileVersion', u'{app_info["version"]}'),
        StringStruct(u'InternalName', u'{app_name}'),
        StringStruct(u'LegalCopyright', u'Copyright © 2024 {app_info["author"]}'),
        StringStruct(u'OriginalFilename', u'{app_name}.exe'),
        StringStruct(u'ProductName', u'{app_info["name"]}'),
        StringStruct(u'ProductVersion', u'{app_info["version"]}')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
        
        version_file = output_dir / 'version_info.txt'
        with open(version_file, 'w') as f:
            f.write(version_info)
        
        cmd.extend(['--version-file', str(version_file)])
        
        # Add the script
        cmd.append(str(script_path))
        
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=output_dir)
        
        if result.returncode != 0:
            raise PackagingError(f"PyInstaller failed: {result.stderr}")
        
        # Return path to executable or directory
        if onefile:
            executable = output_dir / 'dist' / f"{app_name}.exe"
        else:
            executable = output_dir / 'dist' / app_name
        
        if not executable.exists():
            raise PackagingError("Executable not created by PyInstaller")
        
        return executable
    
    except Exception as e:
        raise PackagingError(f"Failed to create executable: {e}")


def create_nsis_installer(
    app_dir: Path,
    output_path: Path,
    app_name: str = "Quick Document Convertor",
    version: str = "2.0.0",
    icon_path: Optional[Path] = None
) -> Path:
    """
    Create NSIS installer for Windows.
    
    Args:
        app_dir: Directory containing the application
        output_path: Output path for installer
        app_name: Application name
        version: Application version
        icon_path: Path to icon file
    
    Returns:
        Path to created installer
    
    Raises:
        PackagingError: If creation fails
    """
    app_info = get_app_info()
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create NSIS script
            nsis_script = f'''
!define APPNAME "{app_name}"
!define COMPANYNAME "{app_info['author']}"
!define DESCRIPTION "{app_info['description']}"
!define VERSIONMAJOR 2
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "{app_info['url']}"
!define UPDATEURL "{app_info['url']}"
!define ABOUTURL "{app_info['url']}"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\\${{COMPANYNAME}}\\${{APPNAME}}"

Name "${{APPNAME}}"
{"Icon " + str(icon_path) if icon_path and icon_path.exists() else ""}
outFile "{output_path}"

!include LogicLib.nsh

page components
page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${{If}} $0 != "admin"
    messageBox mb_iconstop "Administrator rights required!"
    setErrorLevel 740
    quit
${{EndIf}}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    setOutPath $INSTDIR
    file /r "{app_dir}\\*.*"
    
    writeUninstaller "$INSTDIR\\uninstall.exe"
    
    createDirectory "$SMPROGRAMS\\${{COMPANYNAME}}"
    createShortCut "$SMPROGRAMS\\${{COMPANYNAME}}\\${{APPNAME}}.lnk" "$INSTDIR\\{app_name}.exe"
    createShortCut "$DESKTOP\\${{APPNAME}}.lnk" "$INSTDIR\\{app_name}.exe"
    
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "DisplayName" "${{APPNAME}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "UninstallString" "$\\"$INSTDIR\\uninstall.exe$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "QuietUninstallString" "$\\"$INSTDIR\\uninstall.exe$\\" /S"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "InstallLocation" "$\\"$INSTDIR$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "DisplayIcon" "$\\"$INSTDIR\\{app_name}.exe$\\""
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "Publisher" "${{COMPANYNAME}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "HelpLink" "${{HELPURL}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "URLUpdateInfo" "${{UPDATEURL}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "URLInfoAbout" "${{ABOUTURL}}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "DisplayVersion" "${{VERSIONMAJOR}}.${{VERSIONMINOR}}.${{VERSIONBUILD}}"
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "VersionMajor" ${{VERSIONMAJOR}}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "VersionMinor" ${{VERSIONMINOR}}
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "NoModify" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "NoRepair" 1
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}" "EstimatedSize" ${{INSTALLSIZE}}
sectionEnd

section "uninstall"
    delete "$SMPROGRAMS\\${{COMPANYNAME}}\\${{APPNAME}}.lnk"
    rmDir "$SMPROGRAMS\\${{COMPANYNAME}}"
    delete "$DESKTOP\\${{APPNAME}}.lnk"
    
    rmDir /r "$INSTDIR"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{COMPANYNAME}} ${{APPNAME}}"
sectionEnd
'''
            
            nsis_file = temp_path / "installer.nsi"
            with open(nsis_file, 'w', encoding='utf-8') as f:
                f.write(nsis_script)
            
            # Try to compile with NSIS
            try:
                result = subprocess.run([
                    'makensis', str(nsis_file)
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise PackagingError(f"NSIS compilation failed: {result.stderr}")
                
                return output_path
            
            except FileNotFoundError:
                raise PackagingError("NSIS not found. Please install NSIS to create installers.")
    
    except Exception as e:
        raise PackagingError(f"Failed to create NSIS installer: {e}")


def create_msi_installer(
    app_dir: Path,
    output_path: Path,
    app_name: str = "Quick Document Convertor",
    version: str = "2.0.0"
) -> Path:
    """
    Create MSI installer using WiX Toolset.
    
    Args:
        app_dir: Directory containing the application
        output_path: Output path for MSI
        app_name: Application name
        version: Application version
    
    Returns:
        Path to created MSI
    
    Raises:
        PackagingError: If creation fails
    """
    app_info = get_app_info()
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create WiX source file
            wix_content = f'''<?xml version='1.0' encoding='windows-1252'?>
<Wix xmlns='http://schemas.microsoft.com/wix/2006/wi'>
  <Product Name='{app_name}' 
           Id='*' 
           UpgradeCode='12345678-1234-1234-1234-123456789012'
           Language='1033' 
           Codepage='1252' 
           Version='{version}' 
           Manufacturer='{app_info["author"]}'>

    <Package Id='*' 
             Keywords='Installer' 
             Description='{app_info["description"]}' 
             Comments='{app_info["description"]}' 
             Manufacturer='{app_info["author"]}' 
             InstallerVersion='100' 
             Languages='1033' 
             Compressed='yes' 
             SummaryCodepage='1252' />

    <Media Id='1' Cabinet='Sample.cab' EmbedCab='yes' DiskPrompt="CD-ROM #1" />
    <Property Id='DiskPrompt' Value='{app_name} Installation [1]' />

    <Directory Id='TARGETDIR' Name='SourceDir'>
      <Directory Id='ProgramFilesFolder' Name='PFiles'>
        <Directory Id='INSTALLDIR' Name='{app_name}'>
          <Component Id='MainExecutable' Guid='*'>
            <File Id='MainExe' Name='{app_name}.exe' DiskId='1' Source='{app_dir}\\{app_name}.exe' KeyPath='yes'>
              <Shortcut Id="startmenuShortcut" Directory="ProgramMenuDir" Name='{app_name}' WorkingDirectory='INSTALLDIR' Icon="icon.exe" IconIndex="0" Advertise="yes" />
              <Shortcut Id="desktopShortcut" Directory="DesktopFolder" Name='{app_name}' WorkingDirectory='INSTALLDIR' Icon="icon.exe" IconIndex="0" Advertise="yes" />
            </File>
          </Component>
        </Directory>
      </Directory>
      
      <Directory Id="ProgramMenuFolder" Name="Programs">
        <Directory Id="ProgramMenuDir" Name='{app_name}'>
          <Component Id="ProgramMenuDir" Guid="*">
            <RemoveFolder Id='ProgramMenuDir' On='uninstall' />
            <RegistryValue Root='HKCU' Key='Software\\[Manufacturer]\\[ProductName]' Type='string' Value='' KeyPath='yes' />
          </Component>
        </Directory>
      </Directory>
      
      <Directory Id="DesktopFolder" Name="Desktop" />
    </Directory>

    <Feature Id='Complete' Level='1'>
      <ComponentRef Id='MainExecutable' />
      <ComponentRef Id='ProgramMenuDir' />
    </Feature>

    <Icon Id="icon.exe" SourceFile="{app_dir}\\{app_name}.exe" />

  </Product>
</Wix>'''
            
            wix_file = temp_path / "installer.wxs"
            with open(wix_file, 'w', encoding='utf-8') as f:
                f.write(wix_content)
            
            # Try to compile with WiX
            try:
                # Compile to object file
                wixobj_file = temp_path / "installer.wixobj"
                result = subprocess.run([
                    'candle', '-out', str(wixobj_file), str(wix_file)
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise PackagingError(f"WiX candle failed: {result.stderr}")
                
                # Link to MSI
                result = subprocess.run([
                    'light', '-out', str(output_path), str(wixobj_file)
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    raise PackagingError(f"WiX light failed: {result.stderr}")
                
                return output_path
            
            except FileNotFoundError:
                raise PackagingError("WiX Toolset not found. Please install WiX to create MSI installers.")
    
    except Exception as e:
        raise PackagingError(f"Failed to create MSI installer: {e}")


def build_all_windows_packages(
    script_path: Path,
    output_dir: Path,
    version: str = "2.0.0",
    icon_path: Optional[Path] = None
) -> Dict[str, Path]:
    """
    Build all Windows package formats.
    
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
        # Create executable using PyInstaller
        executable = create_pyinstaller_executable(script_path, output_dir, icon_path=icon_path)
        results['executable'] = executable
    except Exception as e:
        results['executable_error'] = str(e)
        return results
    
    try:
        # Create NSIS installer
        nsis_path = output_dir / f"QuickDocumentConvertor-{version}-Setup.exe"
        nsis_result = create_nsis_installer(executable, nsis_path, version=version, icon_path=icon_path)
        results['nsis'] = nsis_result
    except Exception as e:
        results['nsis_error'] = str(e)
    
    try:
        # Create MSI installer
        msi_path = output_dir / f"QuickDocumentConvertor-{version}.msi"
        msi_result = create_msi_installer(executable, msi_path, version=version)
        results['msi'] = msi_result
    except Exception as e:
        results['msi_error'] = str(e)
    
    return results


__all__ = [
    'create_pyinstaller_executable',
    'create_nsis_installer',
    'create_msi_installer',
    'build_all_windows_packages'
]
