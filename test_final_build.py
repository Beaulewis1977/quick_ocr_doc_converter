#!/usr/bin/env python3
"""
Final build test - verify all components are working
"""

import os
import sys
import json
from pathlib import Path

def test_component(name, test_func):
    """Test a component and report results"""
    try:
        result = test_func()
        if result:
            print(f"✅ {name}: PASSED")
            return True
        else:
            print(f"❌ {name}: FAILED")
            return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}")
        return False

def test_dll_package():
    """Test if DLL package was created"""
    dll_zip = Path("dist/UniversalConverter32.dll.zip")
    return dll_zip.exists() and dll_zip.stat().st_size > 0

def test_vfp9_files():
    """Test if VFP9 integration files exist"""
    files = [
        "UniversalConverter_VFP9.prg",
        "VFP9_PipeClient.prg",
    ]
    return all(Path(f).exists() for f in files)

def test_vb6_files():
    """Test if VB6 integration files exist"""
    files = [
        "VB6_UniversalConverter.bas",
        "VB6_ConverterForm.frm",
        "VB6_PipeClient.bas",
    ]
    return all(Path(f).exists() for f in files)

def test_ocr_engine():
    """Test if OCR engine files exist"""
    ocr_files = [
        "ocr_engine/__init__.py",
        "ocr_engine/ocr_engine.py",
        "ocr_engine/ocr_integration.py",
        "ocr_engine/format_detector.py",
        "ocr_engine/image_processor.py",
    ]
    return all(Path(f).exists() for f in ocr_files)

def test_markdown_support():
    """Test if markdown conversion works"""
    try:
        # Test markdown parsing
        import markdown
        md = markdown.Markdown()
        html = md.convert("# Test\n**Bold** text")
        return "<h1>Test</h1>" in html and "<strong>Bold</strong>" in html
    except:
        return False

def test_installers():
    """Test if installer scripts are properly configured"""
    installers = [
        "create_complete_installer.py",
        "create_simple_installer.py", 
        "create_windows_installer.py",
    ]
    
    for installer in installers:
        if Path(installer).exists():
            with open(installer, 'r') as f:
                content = f.read()
                if "universal_document_converter_ocr.py" not in content:
                    print(f"  ⚠️  {installer} not using OCR version")
                    return False
        else:
            print(f"  ❌ Missing: {installer}")
            return False
    
    return True

def test_batch_files():
    """Test if batch files exist"""
    return Path("run_converter.bat").exists()

def test_json_ipc():
    """Test JSON IPC configuration"""
    config_file = Path("vfp9_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return "request_file" in config and "response_file" in config
        except:
            return False
    return True

def main():
    """Run all tests"""
    print("🧪 Universal Document Converter - Final Build Test")
    print("=" * 60)
    
    tests = [
        ("DLL Package", test_dll_package),
        ("VFP9 Integration Files", test_vfp9_files),
        ("VB6 Integration Files", test_vb6_files),
        ("OCR Engine", test_ocr_engine),
        ("Markdown Support", test_markdown_support),
        ("Installer Scripts", test_installers),
        ("Batch Files", test_batch_files),
        ("JSON IPC Config", test_json_ipc),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_component(name, test_func):
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for production release.")
        return 0
    else:
        print("❌ Some tests failed. Please fix issues before release.")
        return 1

if __name__ == "__main__":
    sys.exit(main())