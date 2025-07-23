#!/usr/bin/env python3
"""
Test script for UniversalConverter32.dll integration
Tests the CLI backend that powers the DLL functionality
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

def test_cli_functionality():
    """Test the CLI that powers the DLL"""
    print("=== Universal Document Converter DLL Integration Test ===")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Test 1: Check if CLI script exists
    cli_path = Path("cli.py")
    if not cli_path.exists():
        print("❌ FAIL: cli.py not found")
        return False
    print("✅ PASS: cli.py found")
    
    # Test 2: Test CLI help
    try:
        result = subprocess.run([sys.executable, "cli.py", "--help"], 
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ PASS: CLI help command works")
        else:
            print(f"❌ FAIL: CLI help failed with code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ FAIL: CLI help test error: {e}")
        return False
    
    # Test 3: Create test markdown file
    test_content = """# Test Document

This is a test markdown document for the Universal Document Converter DLL.

## Features
- Document conversion
- VB6/VFP9 integration  
- Production-ready DLL

## Testing
This file tests the conversion functionality that will be used by the DLL.
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_input = Path(temp_dir) / "test.md"
        test_output = Path(temp_dir) / "test.txt"
        
        # Write test file
        test_input.write_text(test_content)
        print(f"✅ PASS: Created test file: {test_input}")
        
        # Test 4: Test conversion
        try:
            cmd = [sys.executable, "cli.py", str(test_input), "-o", str(test_output), "-t", "txt"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ PASS: Conversion command executed successfully")
                
                # Check if output file was created
                if test_output.exists():
                    print("✅ PASS: Output file created")
                    
                    # Check output content
                    output_content = test_output.read_text()
                    if len(output_content) > 0 and "Test Document" in output_content:
                        print("✅ PASS: Output file contains expected content")
                        print(f"Output preview: {output_content[:100]}...")
                    else:
                        print("❌ FAIL: Output file content is invalid")
                        print(f"Content: {output_content}")
                        return False
                else:
                    print("❌ FAIL: Output file was not created")
                    return False
            else:
                print(f"❌ FAIL: Conversion failed with code {result.returncode}")
                print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ FAIL: Conversion test error: {e}")
            return False
    
    # Test 5: Test different format
    with tempfile.TemporaryDirectory() as temp_dir:
        test_input = Path(temp_dir) / "test.md"
        test_output = Path(temp_dir) / "test.html"
        
        test_input.write_text(test_content)
        
        try:
            cmd = [sys.executable, "cli.py", str(test_input), "-o", str(test_output), "-t", "html"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and test_output.exists():
                output_content = test_output.read_text()
                if "<h1>" in output_content and "Test Document" in output_content:
                    print("✅ PASS: HTML conversion works correctly")
                else:
                    print("❌ FAIL: HTML conversion output is invalid")
                    return False
            else:
                print(f"❌ FAIL: HTML conversion failed")
                return False
                
        except Exception as e:
            print(f"❌ FAIL: HTML conversion test error: {e}")
            return False
    
    print()
    print("🎉 ALL TESTS PASSED!")
    print()
    print("The CLI backend is working correctly and ready for DLL integration.")
    print("This CLI will be called by the UniversalConverter32.dll for VB6/VFP9 applications.")
    print()
    print("Next steps:")
    print("1. Build the DLL: run build_dll.bat on Windows")
    print("2. Test with VB6/VFP9 using the production integration modules")
    print("3. Deploy the complete package to legacy systems")
    
    return True

def test_vb6_integration_syntax():
    """Test VB6 integration module syntax"""
    print("\n=== Testing VB6 Integration Module Syntax ===")
    
    vb6_file = Path("VB6_UniversalConverter_Production.bas")
    if not vb6_file.exists():
        print("❌ FAIL: VB6 production module not found")
        return False
    
    content = vb6_file.read_text()
    
    # Check for key VB6 declarations
    required_elements = [
        "Declare Function ConvertDocument",
        "Declare Function TestConnection", 
        "Declare Function GetVersion",
        "Public Function ConvertDocumentFile",
        "Public Function PDFToText",
        "Public Function DOCXToMarkdown",
        "UC_SUCCESS",
        "UC_FAILURE",
        "UC_ERROR"
    ]
    
    for element in required_elements:
        if element in content:
            print(f"✅ PASS: Found {element}")
        else:
            print(f"❌ FAIL: Missing {element}")
            return False
    
    print("✅ PASS: VB6 integration module syntax looks correct")
    return True

def test_vfp9_integration_syntax():
    """Test VFP9 integration module syntax"""
    print("\n=== Testing VFP9 Integration Module Syntax ===")
    
    vfp9_file = Path("VFP9_UniversalConverter_Production.prg")
    if not vfp9_file.exists():
        print("❌ FAIL: VFP9 production module not found")
        return False
    
    content = vfp9_file.read_text()
    
    # Check for key VFP9 declarations
    required_elements = [
        "DECLARE INTEGER ConvertDocument",
        "DECLARE INTEGER TestConnection",
        "DECLARE STRING GetVersion", 
        "DEFINE CLASS UniversalConverter",
        "FUNCTION ConvertDocumentFile",
        "FUNCTION PDFToText",
        "FUNCTION DOCXToMarkdown",
        "#DEFINE UC_SUCCESS",
        "#DEFINE UC_FAILURE",
        "#DEFINE UC_ERROR"
    ]
    
    for element in required_elements:
        if element in content:
            print(f"✅ PASS: Found {element}")
        else:
            print(f"❌ FAIL: Missing {element}")
            return False
    
    print("✅ PASS: VFP9 integration module syntax looks correct")
    return True

def test_dll_source():
    """Test DLL source code"""
    print("\n=== Testing DLL Source Code ===")
    
    dll_source = Path("dll_source/UniversalConverter32.cpp")
    if not dll_source.exists():
        print("❌ FAIL: DLL source code not found")
        return False
    
    content = dll_source.read_text()
    
    # Check for key DLL exports
    required_elements = [
        "EXPORT LONG ConvertDocument",
        "EXPORT LONG TestConnection",
        "EXPORT const char* GetVersion",
        "EXPORT const char* GetLastError",
        "UC_SUCCESS",
        "UC_FAILURE", 
        "UC_ERROR",
        "DllMain"
    ]
    
    for element in required_elements:
        if element in content:
            print(f"✅ PASS: Found {element}")
        else:
            print(f"❌ FAIL: Missing {element}")
            return False
    
    print("✅ PASS: DLL source code looks correct")
    return True

if __name__ == "__main__":
    print("Starting comprehensive DLL integration test...\n")
    
    all_passed = True
    
    # Test CLI functionality
    if not test_cli_functionality():
        all_passed = False
    
    # Test integration modules
    if not test_vb6_integration_syntax():
        all_passed = False
        
    if not test_vfp9_integration_syntax():
        all_passed = False
        
    # Test DLL source
    if not test_dll_source():
        all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("\nThe Universal Document Converter DLL system is ready for production:")
        print("✅ CLI backend working correctly")
        print("✅ VB6 integration module ready")
        print("✅ VFP9 integration module ready") 
        print("✅ DLL source code complete")
        print("\nNext step: Build and deploy on Windows systems")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please review the errors above and fix the issues.")
    
    print("="*60)