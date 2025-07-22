#!/usr/bin/env python3
"""
Simple Windows Installer Creator
Creates a portable ZIP package with all necessary files
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_portable_package():
    """Create a portable ZIP package for easy distribution"""
    print("📦 Creating Portable Package...")
    
    # Create dist directory
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # Files to include in package
    files_to_include = [
        "universal_document_converter_ocr.py",
        "run_converter.bat",
        "run_converter.ps1",
        "install_converter.py",
        "icon.ico",
        "README.md",
        "QUICK_START.md",
        "TROUBLESHOOTING.md",
        "requirements.txt",
        "requirements_installer.txt",
        "UniversalConverter_VFP9.prg",
        "VB6_UniversalConverter.bas",
        "VB6_ConverterForm.frm",
        "VFP9_PipeClient.prg",
        "VB6_PipeClient.bas",
        "VFP9_VB6_INTEGRATION_GUIDE.md",
        "dist/UniversalConverter32.dll.zip",
        "DOCUMENTATION_COMPLETE.md"
    ]
    
    # Create package directory
    package_name = "QuickDocumentConvertor_Portable"
    package_dir = dist_dir / package_name
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy files
    missing_files = []
    for file_path in files_to_include:
        if Path(file_path).exists():
            shutil.copy2(file_path, package_dir)
            print(f"✅ Added: {file_path}")
        else:
            missing_files.append(file_path)
            print(f"⚠️ Missing: {file_path}")
    
    # Add ocr_engine directory
    ocr_engine_dir = Path("ocr_engine")
    if ocr_engine_dir.exists():
        package_ocr_dir = package_dir / "ocr_engine"
        package_ocr_dir.mkdir(exist_ok=True)
        for ocr_file in ocr_engine_dir.glob("*.py"):
            shutil.copy2(ocr_file, package_ocr_dir / ocr_file.name)
            print(f"✅ Added: ocr_engine/{ocr_file.name}")
    else:
        print("⚠️ Missing: ocr_engine directory")
        missing_files.append("ocr_engine")
    
    # Add documentation directory
    docs_dir = Path("docs")
    if docs_dir.exists():
        package_docs_dir = package_dir / "docs"
        package_docs_dir.mkdir(exist_ok=True)
        for doc_file in docs_dir.glob("*.md"):
            shutil.copy2(doc_file, package_docs_dir / doc_file.name)
            print(f"✅ Added: docs/{doc_file.name}")
    else:
        print("⚠️ Missing: docs directory")
    
    # Create ZIP file
    zip_path = dist_dir / f"{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_path)
    
    print(f"\n📦 Portable package created: {zip_path}")
    print(f"📁 Extract and run: run_converter.bat")
    
    if missing_files:
        print(f"\n⚠️ Missing files: {', '.join(missing_files)}")
    
    return zip_path

if __name__ == "__main__":
    print("🚀 Quick Document Convertor - Portable Package Creator")
    print("=" * 60)
    
    zip_path = create_portable_package()
    
    print("\n" + "=" * 60)
    print("✅ Package ready for distribution!")
    print(f"📁 Location: {zip_path}")
    print("\n📋 Distribution Instructions:")
    print("1. Share the ZIP file with users")
    print("2. Users extract and run run_converter.bat")
    print("3. First-time users run install_converter.py")
    
    input("\nPress Enter to exit...")
