#!/usr/bin/env python3
"""
Legacy DLL Builder - VB6/VFP9 Integration Commands
Extracted from universal_document_converter.py legacy functionality
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import logging

class VB6VFP9Integration:
    """Handles VB6 and VFP9 integration functionality"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def generate_vb6_module(self) -> bool:
        """Generate customized VB6 integration module"""
        self.logger.info("Generating VB6 integration module...")
        
        try:
            # Read the production VB6 module
            vb6_source = Path("VB6_UniversalConverter_Production.bas")
            if not vb6_source.exists():
                self.logger.error("❌ VB6 production module not found")
                return False
            
            content = vb6_source.read_text()
            
            # Save to desktop if available, otherwise current directory
            try:
                desktop = Path.home() / "Desktop"
                output_path = desktop / "UniversalConverter_VB6.bas"
            except (OSError, AttributeError):
                output_path = Path("UniversalConverter_VB6.bas")
            
            output_path.write_text(content)
            self.logger.info(f"✅ VB6 module generated: {output_path}")
            self.logger.info("   Add this .bas file to your VB6 project")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error generating VB6 module: {str(e)}")
            return False
    
    def generate_vfp9_class(self) -> bool:
        """Generate customized VFP9 integration class"""
        self.logger.info("Generating VFP9 integration class...")
        
        try:
            # Read the production VFP9 class
            vfp9_source = Path("VFP9_UniversalConverter_Production.prg")
            if not vfp9_source.exists():
                self.logger.error("❌ VFP9 production class not found")
                return False
            
            content = vfp9_source.read_text()
            
            # Save to desktop if available, otherwise current directory
            try:
                desktop = Path.home() / "Desktop"
                output_path = desktop / "UniversalConverter_VFP9.prg"
            except (OSError, AttributeError):
                output_path = Path("UniversalConverter_VFP9.prg")
            
            output_path.write_text(content)
            self.logger.info(f"✅ VFP9 class generated: {output_path}")
            self.logger.info("   Include this .prg file in your VFP9 project")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error generating VFP9 class: {str(e)}")
            return False
    
    def show_vb6_examples(self) -> str:
        """Show real VB6 DLL integration examples"""
        examples = '''
REAL VB6 DLL INTEGRATION EXAMPLES:

1. BASIC DLL USAGE:
' Declare the DLL functions
Private Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    (ByVal inputPath As String, ByVal outputPath As String, _
     ByVal inputFormat As String, ByVal outputFormat As String) As Long

Private Declare Function TestConnection Lib "UniversalConverter32.dll" () As Long

' Test if DLL is available
Private Sub TestDLL()
    If TestConnection() = 1 Then
        MsgBox "DLL is working!"
    Else
        MsgBox "DLL not available"
    End If
End Sub

2. DOCUMENT CONVERSION:
Private Sub ConvertFile()
    Dim result As Long
    result = ConvertDocument("C:\\docs\\file.pdf", "C:\\docs\\file.txt", "pdf", "txt")
    If result = 1 Then
        MsgBox "Conversion successful!"
    Else
        MsgBox "Conversion failed"
    End If
End Sub

3. PRODUCTION USAGE:
' Add VB6_UniversalConverter_Production.bas to your project
' Then use the ConvertDocument class:
Dim converter As New ConvertDocument
converter.ConvertFile("input.pdf", "output.txt")
'''
        return examples
    
    def show_vfp9_examples(self) -> str:
        """Show real VFP9 DLL integration examples"""
        examples = '''
REAL VFP9 DLL INTEGRATION EXAMPLES:

1. BASIC DLL USAGE:
*-- Declare the DLL functions
DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
    STRING inputPath, STRING outputPath, ;
    STRING inputFormat, STRING outputFormat

DECLARE INTEGER TestConnection IN UniversalConverter32.dll

*-- Test if DLL is available
PROCEDURE TestDLL()
    IF TestConnection() = 1
        MESSAGEBOX("DLL is working!")
    ELSE
        MESSAGEBOX("DLL not available")
    ENDIF
ENDPROC

2. DOCUMENT CONVERSION:
PROCEDURE ConvertFile()
    LOCAL lnResult
    lnResult = ConvertDocument("C:\\docs\\file.pdf", "C:\\docs\\file.txt", "pdf", "txt")
    IF lnResult = 1
        MESSAGEBOX("Conversion successful!")
    ELSE
        MESSAGEBOX("Conversion failed")
    ENDIF
ENDPROC

3. PRODUCTION USAGE:
*-- Include VFP9_UniversalConverter_Production.prg in your project
*-- Then use the ConvertDocument class:
LOCAL oConverter
oConverter = CREATEOBJECT("ConvertDocument")
oConverter.ConvertFile("input.pdf", "output.txt")
'''
        return examples
    
    def test_vb6_integration(self) -> str:
        """Test VB6 DLL integration - returns test code"""
        self.logger.info("Testing VB6 DLL integration...")
        
        vb6_test = '''
' VB6 Test Code for UniversalConverter32.dll
Private Declare Function ConvertDocument Lib "UniversalConverter32.dll" _
    (ByVal inputPath As String, ByVal outputPath As String, _
     ByVal inputFormat As String, ByVal outputFormat As String) As Long

Private Declare Function TestConnection Lib "UniversalConverter32.dll" () As Long

Sub TestDLL()
    Dim result As Long
    
    ' Test if DLL is available
    result = TestConnection()
    If result = 1 Then
        MsgBox "✅ DLL is available and working!"
    Else
        MsgBox "❌ DLL test failed"
    End If
    
    ' Test conversion
    result = ConvertDocument("C:\\temp\\test.txt", "C:\\temp\\test.md", "txt", "md")
    If result = 1 Then
        MsgBox "✅ Conversion test successful!"
    Else
        MsgBox "❌ Conversion test failed"
    End If
End Sub
'''
        
        self.logger.info("VB6 Test Code:")
        self.logger.info(vb6_test)
        self.logger.info("Copy this code to a VB6 form and run TestDLL()")
        return vb6_test
    
    def test_vfp9_integration(self) -> str:
        """Test VFP9 DLL integration - returns test code"""
        self.logger.info("Testing VFP9 DLL integration...")
        
        vfp9_test = '''
*!* VFP9 Test Code for UniversalConverter32.dll
DECLARE INTEGER ConvertDocument IN UniversalConverter32.dll ;
    STRING inputPath, STRING outputPath, ;
    STRING inputFormat, STRING outputFormat

DECLARE INTEGER TestConnection IN UniversalConverter32.dll

PROCEDURE TestDLL()
    LOCAL lnResult
    
    *-- Test if DLL is available
    lnResult = TestConnection()
    IF lnResult = 1
        MESSAGEBOX("✅ DLL is available and working!")
    ELSE
        MESSAGEBOX("❌ DLL test failed")
    ENDIF
    
    *-- Test conversion
    lnResult = ConvertDocument("C:\\temp\\test.txt", "C:\\temp\\test.md", "txt", "md")
    IF lnResult = 1
        MESSAGEBOX("✅ Conversion test successful!")
    ELSE
        MESSAGEBOX("❌ Conversion test failed")
    ENDIF
ENDPROC
'''
        
        self.logger.info("VFP9 Test Code:")
        self.logger.info(vfp9_test)
        self.logger.info("Copy this code to a VFP9 program and run TestDLL")
        return vfp9_test
    
    def copy_integration_files(self) -> bool:
        """Copy integration files to desktop"""
        self.logger.info("📋 Copying integration files...")
        
        try:
            desktop = Path.home() / "Desktop"
            if not desktop.exists():
                desktop = Path(".")
            
            files_to_copy = [
                ("VB6_UniversalConverter_Production.bas", "VB6 Integration Module"),
                ("VFP9_UniversalConverter_Production.prg", "VFP9 Integration Class"),
                ("cli.py", "Python CLI Backend"),
                ("requirements.txt", "Python Dependencies"),
                ("README_DLL_Production.md", "Documentation")
            ]
            
            copied = 0
            for filename, description in files_to_copy:
                source = Path(filename)
                if source.exists():
                    target = desktop / filename
                    target.write_text(source.read_text())
                    self.logger.info(f"✅ {description}: {target}")
                    copied += 1
                else:
                    self.logger.warning(f"❌ Missing: {filename}")
            
            self.logger.info(f"📋 Copied {copied} files to {desktop}")
            return copied > 0
            
        except Exception as e:
            self.logger.error(f"❌ Copy error: {str(e)}")
            return False