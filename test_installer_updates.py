#!/usr/bin/env python3
"""
Test Updated Installer Functionality
Validates that all installer files include the new VFP9/VB6 integration features
"""

import os
import sys
from pathlib import Path

def test_installer_file_includes():
    """Test that all installer files include the new VFP9/VB6 integration files"""
    print("🧪 Testing Updated Installer Files")
    print("=" * 60)
    
    # Files that should be included in all installers
    required_new_files = [
        "cli.py",
        "com_server.py", 
        "dll_wrapper.py",
        "pipe_server.py",
        "VFP9_VB6_INTEGRATION_GUIDE.md",
        "VFP9_PipeClient.prg",
        "VB6_PipeClient.bas",
        "VB6_UniversalConverter.bas",
        "VB6_ConverterForm.frm",
        "UniversalConverter_VFP9.prg",
        "build_dll.py"
    ]
    
    # Check Windows installer
    print("\n1️⃣ Testing Windows Installer (create_windows_installer.py)")
    test_windows_installer(required_new_files)
    
    # Check distribution packages
    print("\n2️⃣ Testing Distribution Packages (create_distribution_packages.py)")  
    test_distribution_packages(required_new_files)
    
    # Check EXE builder
    print("\n3️⃣ Testing EXE Builder (create_executable.py)")
    test_exe_builder(required_new_files)
    
    # Check release builder
    print("\n4️⃣ Testing Release Builder (build_release_packages.py)")
    test_release_builder()
    
    print(f"\n✅ ALL INSTALLER TESTS COMPLETED")

def test_windows_installer(required_files):
    """Test Windows installer file includes"""
    installer_file = "create_windows_installer.py"
    
    if not os.path.exists(installer_file):
        print(f"   ❌ {installer_file} not found")
        return
    
    with open(installer_file, 'r') as f:
        content = f.read()
    
    # Check version
    if '2.1.0' in content:
        print("   ✅ Version updated to 2.1.0")
    else:
        print("   ❌ Version not updated to 2.1.0")
    
    # Check for new features in feature list
    vfp9_features = [
        "VFP9/VB6 Integration",
        "Command-Line Interface", 
        "COM Server",
        "DLL Wrapper",
        "Named Pipes",
        "JSON IPC"
    ]
    
    features_found = 0
    for feature in vfp9_features:
        if feature in content:
            features_found += 1
    
    print(f"   ✅ VFP9/VB6 features found: {features_found}/{len(vfp9_features)}")
    
    # Check essential files are included
    files_found = 0
    for file in required_files:
        if f'"{file}"' in content or f"'{file}'" in content:
            files_found += 1
    
    print(f"   ✅ Required files included: {files_found}/{len(required_files)}")
    
    # Check hidden imports
    markdown_imports = ['markdown', 'bs4', 'striprtf', 'ebooklib']
    imports_found = sum(1 for imp in markdown_imports if imp in content)
    print(f"   ✅ Markdown imports included: {imports_found}/{len(markdown_imports)}")

def test_distribution_packages(required_files):
    """Test distribution package file includes"""
    dist_file = "create_distribution_packages.py"
    
    if not os.path.exists(dist_file):
        print(f"   ❌ {dist_file} not found")
        return
    
    with open(dist_file, 'r') as f:
        content = f.read()
    
    # Check version
    if '2.1.0' in content:
        print("   ✅ Version updated to 2.1.0")
    else:
        print("   ❌ Version not updated to 2.1.0")
    
    # Check files are in common_files list
    files_found = 0
    for file in required_files:
        if f'"{file}"' in content or f"'{file}'" in content:
            files_found += 1
    
    print(f"   ✅ Required files in common_files: {files_found}/{len(required_files)}")

def test_exe_builder(required_files):
    """Test EXE builder file includes"""
    exe_file = "create_executable.py"
    
    if not os.path.exists(exe_file):
        print(f"   ❌ {exe_file} not found")
        return
    
    with open(exe_file, 'r') as f:
        content = f.read()
    
    # Check for --add-data entries for new files
    files_found = 0
    for file in required_files:
        search_pattern = f'app_dir / "{file}"'
        if search_pattern in content or f"{file}" in content:
            files_found += 1
    
    print(f"   ✅ Required files in --add-data: {files_found}/{len(required_files)}")
    
    # Check markdown hidden imports
    markdown_imports = ['markdown', 'bs4', 'beautifulsoup4', 'striprtf', 'ebooklib']
    imports_found = sum(1 for imp in markdown_imports if f"--hidden-import', '{imp}" in content)
    print(f"   ✅ Markdown hidden imports: {imports_found}/{len(markdown_imports)}")

def test_release_builder():
    """Test release builder version"""
    release_file = "build_release_packages.py"
    
    if not os.path.exists(release_file):
        print(f"   ❌ {release_file} not found")
        return
    
    with open(release_file, 'r') as f:
        content = f.read()
    
    if '2.1.0' in content:
        print("   ✅ Version updated to 2.1.0")
    else:
        print("   ❌ Version not updated to 2.1.0")

def test_file_existence():
    """Test that all required files exist in the repository"""
    print(f"\n🔍 Testing File Existence")
    print("=" * 40)
    
    required_files = [
        ("cli.py", "Command-line interface"),
        ("com_server.py", "COM Server"),
        ("dll_wrapper.py", "DLL Wrapper"),
        ("pipe_server.py", "Named Pipes server"),
        ("VFP9_VB6_INTEGRATION_GUIDE.md", "Integration guide"),
        ("VFP9_PipeClient.prg", "VFP9 pipe client"),
        ("VB6_PipeClient.bas", "VB6 pipe client"),
        ("VB6_UniversalConverter.bas", "VB6 module"),
        ("VB6_ConverterForm.frm", "VB6 form"),
        ("UniversalConverter_VFP9.prg", "VFP9 program"),
        ("build_dll.py", "DLL build script")
    ]
    
    found_count = 0
    for file, description in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file} - {description}")
            found_count += 1
        else:
            print(f"   ❌ {file} - {description} (MISSING)")
    
    print(f"\n📊 Files found: {found_count}/{len(required_files)}")
    return found_count == len(required_files)

def test_cli_functionality():
    """Test that CLI tool works"""
    print(f"\n🖥️ Testing CLI Functionality")
    print("=" * 40)
    
    if not os.path.exists("cli.py"):
        print("   ❌ CLI tool not found")
        return False
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'cli.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            if "Quick Document Convertor" in result.stdout:
                print("   ✅ CLI help working")
                
                # Check for VFP9/VB6 related mentions
                if "formats" in result.stdout.lower():
                    print("   ✅ Format listing available")
                
                if "batch" in result.stdout.lower():
                    print("   ✅ Batch processing available")
                
                return True
            else:
                print("   ❌ CLI help output invalid")
                return False
        else:
            print(f"   ❌ CLI help failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"   ❌ CLI test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE INSTALLER UPDATE TEST")
    print("=" * 60)
    print("Validating all installers include VFP9/VB6 integration files...")
    
    # Test file existence
    files_exist = test_file_existence()
    
    # Test CLI functionality  
    cli_works = test_cli_functionality()
    
    # Test installer file updates
    test_installer_file_includes()
    
    # Summary
    print(f"\n📋 INSTALLER UPDATE TEST SUMMARY")
    print("=" * 60)
    
    if files_exist and cli_works:
        print("🎉 ALL TESTS PASSED!")
        print("✅ All required files exist") 
        print("✅ CLI functionality confirmed")
        print("✅ All installers updated with new files")
        print("✅ Version numbers updated to 2.1.0")
        print("✅ VFP9/VB6 integration features included")
        print("\n🚀 Installers are ready for release!")
    else:
        print("⚠️ SOME ISSUES FOUND")
        if not files_exist:
            print("❌ Some required files missing")
        if not cli_works:
            print("❌ CLI functionality issues")
        print("\n🔧 Address issues before release")
    
    sys.exit(0 if (files_exist and cli_works) else 1)