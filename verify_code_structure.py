#!/usr/bin/env python3
"""
Code Structure Verification Script
Verifies the application structure without requiring external dependencies
"""

import os
import sys
import ast
import json
from pathlib import Path

class CodeVerifier:
    def __init__(self):
        self.results = {}
        self.errors = []
        
    def log_result(self, category, test, success, message=""):
        if category not in self.results:
            self.results[category] = {}
        self.results[category][test] = {
            'success': success,
            'message': message
        }
        print(f"{'✅' if success else '❌'} {category} - {test}: {message}")
        
    def verify_file_structure(self):
        """Verify essential files exist"""
        print("\n=== Verifying File Structure ===")
        
        essential_files = [
            'universal_document_converter.py',
            'ocr_engine/__init__.py',
            'ocr_engine/ocr_engine.py',
            'ocr_engine/ocr_integration.py',
            'ocr_engine/format_detector.py',
            'ocr_engine/image_processor.py',
            'requirements.txt',
            'README.md',
            'LICENSE'
        ]
        
        for file in essential_files:
            exists = os.path.exists(file)
            self.log_result('File Structure', file, exists, 
                           'Found' if exists else 'Missing')
                           
    def verify_python_syntax(self):
        """Verify Python files compile without syntax errors"""
        print("\n=== Verifying Python Syntax ===")
        
        python_files = []
        for root, dirs, files in os.walk('.'):
            # Skip hidden directories and build directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['build', 'dist', '__pycache__', 'test_env', 'dev_docs_backup']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        syntax_errors = 0
        for file in python_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                ast.parse(content)
                self.log_result('Python Syntax', file, True, 'Valid')
            except SyntaxError as e:
                syntax_errors += 1
                self.log_result('Python Syntax', file, False, str(e))
                
        return syntax_errors == 0
        
    def verify_imports(self):
        """Verify internal imports are correct"""
        print("\n=== Verifying Internal Imports ===")
        
        # Check main application imports
        main_app = 'universal_document_converter.py'
        if os.path.exists(main_app):
            with open(main_app, 'r') as f:
                content = f.read()
                
            required_imports = [
                'from ocr_engine.ocr_integration import OCRIntegration',
                'from ocr_engine.format_detector import OCRFormatDetector'
            ]
            
            for imp in required_imports:
                if imp in content:
                    self.log_result('Imports', imp, True, 'Found')
                else:
                    self.log_result('Imports', imp, False, 'Missing')
                    
    def verify_class_structure(self):
        """Verify main classes exist"""
        print("\n=== Verifying Class Structure ===")
        
        class_checks = {
            'universal_document_converter.py': ['UniversalDocumentConverter'],
            'ocr_engine/ocr_engine.py': ['OCREngine'],
            'ocr_engine/ocr_integration.py': ['OCRIntegration'],
            'ocr_engine/format_detector.py': ['OCRFormatDetector'],
            'ocr_engine/image_processor.py': ['ImageProcessor']
        }
        
        for file, classes in class_checks.items():
            if os.path.exists(file):
                with open(file, 'r') as f:
                    content = f.read()
                    
                for class_name in classes:
                    if f'class {class_name}' in content:
                        self.log_result('Classes', f'{file}::{class_name}', True, 'Found')
                    else:
                        self.log_result('Classes', f'{file}::{class_name}', False, 'Missing')
            else:
                for class_name in classes:
                    self.log_result('Classes', f'{file}::{class_name}', False, 'File missing')
                    
    def verify_test_structure(self):
        """Verify test files exist and are properly structured"""
        print("\n=== Verifying Test Structure ===")
        
        test_files = [
            'test_ocr_integration.py',
            'test_converter.py',
            'validate_ocr_integration.py'
        ]
        
        for test_file in test_files:
            if os.path.exists(test_file):
                with open(test_file, 'r') as f:
                    content = f.read()
                    
                # Count test functions
                test_count = content.count('def test_')
                if test_count > 0:
                    self.log_result('Tests', test_file, True, f'{test_count} tests found')
                else:
                    self.log_result('Tests', test_file, False, 'No tests found')
            else:
                self.log_result('Tests', test_file, False, 'File missing')
                
    def generate_report(self):
        """Generate final report"""
        print("\n=== VERIFICATION SUMMARY ===")
        
        total_tests = 0
        passed_tests = 0
        
        for category, tests in self.results.items():
            category_passed = sum(1 for t in tests.values() if t['success'])
            category_total = len(tests)
            total_tests += category_total
            passed_tests += category_passed
            
            print(f"\n{category}: {category_passed}/{category_total} passed")
            
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"\nOverall: {passed_tests}/{total_tests} ({success_rate:.1f}%) passed")
        
        # Save detailed results
        with open('verification_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
            
        print("\nDetailed results saved to: verification_results.json")
        
        return success_rate >= 80  # Consider 80% as passing

def main():
    verifier = CodeVerifier()
    
    # Run all verifications
    verifier.verify_file_structure()
    verifier.verify_python_syntax()
    verifier.verify_imports()
    verifier.verify_class_structure()
    verifier.verify_test_structure()
    
    # Generate report
    success = verifier.generate_report()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())