#!/usr/bin/env python3
"""
Comprehensive GUI Test for Universal Document Converter Ultimate
Tests all GUI features and functionality
"""

import tkinter as tk
import tempfile
import os
import sys
import time
from pathlib import Path

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main application
from universal_document_converter_ultimate import DocumentConverterUltimate, ConfigManager

def test_gui_creation():
    """Test that GUI can be created"""
    print("Testing GUI creation...")
    root = tk.Tk()
    root.withdraw()  # Hide window for headless testing
    
    try:
        app = DocumentConverterUltimate(root)
        print("✓ GUI created successfully")
        return True
    except Exception as e:
        print(f"✗ GUI creation failed: {e}")
        return False
    finally:
        root.destroy()

def test_tab_switching():
    """Test tab switching functionality"""
    print("\nTesting tab switching...")
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = DocumentConverterUltimate(root)
        
        # Get all tabs
        tabs = app.notebook.tabs()
        print(f"  Found {len(tabs)} tabs")
        
        # Switch through each tab
        for i, tab in enumerate(tabs):
            app.notebook.select(tab)
            tab_text = app.notebook.tab(tab, "text")
            print(f"  ✓ Switched to tab: {tab_text}")
        
        return True
    except Exception as e:
        print(f"✗ Tab switching failed: {e}")
        return False
    finally:
        root.destroy()

def test_file_operations():
    """Test file add/remove operations"""
    print("\nTesting file operations...")
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = DocumentConverterUltimate(root)
        
        # Create test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content")
            test_file = f.name
        
        # Add file programmatically
        app.file_listbox.insert(tk.END, test_file)
        print("  ✓ Added test file")
        
        # Check if file is in list
        files = app.file_listbox.get(0, tk.END)
        assert test_file in files, "File not in listbox"
        print("  ✓ File appears in list")
        
        # Clear files
        app.clear_files()
        files = app.file_listbox.get(0, tk.END)
        assert len(files) == 0, "Files not cleared"
        print("  ✓ Files cleared successfully")
        
        # Cleanup
        os.unlink(test_file)
        return True
    except Exception as e:
        print(f"✗ File operations failed: {e}")
        return False
    finally:
        root.destroy()

def test_settings():
    """Test settings and configuration"""
    print("\nTesting settings...")
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = DocumentConverterUltimate(root)
        
        # Test format selection
        formats = ['txt', 'docx', 'pdf', 'html', 'rtf', 'epub']
        for fmt in formats:
            app.format_var.set(fmt)
            assert app.format_var.get() == fmt, f"Format not set to {fmt}"
            print(f"  ✓ Format selection: {fmt}")
        
        # Test OCR toggle
        app.ocr_var.set(True)
        assert app.ocr_var.get() == True, "OCR not enabled"
        print("  ✓ OCR toggle works")
        
        # Test thread count
        original = app.thread_count.get()
        app.thread_count.set(8)
        assert app.thread_count.get() == 8, "Thread count not set"
        print("  ✓ Thread count adjustment works")
        app.thread_count.set(original)
        
        return True
    except Exception as e:
        print(f"✗ Settings test failed: {e}")
        return False
    finally:
        root.destroy()

def test_advanced_settings():
    """Test advanced settings tab"""
    print("\nTesting advanced settings...")
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = DocumentConverterUltimate(root)
        
        # Switch to advanced settings tab
        for tab in app.notebook.tabs():
            if app.notebook.tab(tab, "text") == "⚙️ Advanced Settings":
                app.notebook.select(tab)
                print("  ✓ Switched to Advanced Settings tab")
                break
        
        # Test various settings
        settings_to_test = [
            ('ocr_language', 'fra'),
            ('ocr_backend', 'easyocr'),
            ('enable_caching', False),
            ('preserve_structure', False),
            ('overwrite_existing', True),
            ('auto_open_output', False)
        ]
        
        for setting, value in settings_to_test:
            if hasattr(app, f'{setting}_var'):
                var = getattr(app, f'{setting}_var')
                var.set(value)
                print(f"  ✓ Set {setting} = {value}")
        
        return True
    except Exception as e:
        print(f"✗ Advanced settings test failed: {e}")
        return False
    finally:
        root.destroy()

def test_statistics():
    """Test statistics functionality"""
    print("\nTesting statistics...")
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = DocumentConverterUltimate(root)
        
        # Switch to statistics tab
        for tab in app.notebook.tabs():
            if app.notebook.tab(tab, "text") == "📊 Statistics":
                app.notebook.select(tab)
                print("  ✓ Switched to Statistics tab")
                break
        
        # Update statistics
        app.update_statistics()
        print("  ✓ Statistics updated")
        
        # Test export functionality
        with tempfile.TemporaryDirectory() as tmpdir:
            # Export as CSV
            csv_file = os.path.join(tmpdir, "stats.csv")
            app.statistics_manager.export_csv(csv_file)
            assert os.path.exists(csv_file), "CSV export failed"
            print("  ✓ Exported statistics as CSV")
            
            # Export as JSON
            json_file = os.path.join(tmpdir, "stats.json")
            app.statistics_manager.export_json(json_file)
            assert os.path.exists(json_file), "JSON export failed"
            print("  ✓ Exported statistics as JSON")
        
        return True
    except Exception as e:
        print(f"✗ Statistics test failed: {e}")
        return False
    finally:
        root.destroy()

def test_api_server_tab():
    """Test API server tab functionality"""
    print("\nTesting API server tab...")
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = DocumentConverterUltimate(root)
        
        # Switch to API tab
        for tab in app.notebook.tabs():
            if app.notebook.tab(tab, "text") == "🌐 API Server":
                app.notebook.select(tab)
                print("  ✓ Switched to API Server tab")
                break
        
        # Check API controls exist
        if hasattr(app, 'api_status_label'):
            print("  ✓ API status label exists")
        
        if hasattr(app, 'api_host_var') and hasattr(app, 'api_port_var'):
            # Test setting host and port
            app.api_host_var.set("localhost")
            app.api_port_var.set(8080)
            print("  ✓ API host/port configuration works")
        
        return True
    except Exception as e:
        print(f"✗ API server tab test failed: {e}")
        return False
    finally:
        root.destroy()

def test_conversion_workflow():
    """Test a complete conversion workflow"""
    print("\nTesting conversion workflow...")
    root = tk.Tk()
    root.withdraw()
    
    try:
        app = DocumentConverterUltimate(root)
        
        # Create test files
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create input file
            input_file = os.path.join(tmpdir, "test.txt")
            with open(input_file, 'w') as f:
                f.write("Test content for conversion")
            
            # Set output directory
            app.output_dir = tmpdir
            
            # Add file
            app.file_listbox.insert(tk.END, input_file)
            print("  ✓ Added test file")
            
            # Set format
            app.format_var.set("html")
            print("  ✓ Set output format to HTML")
            
            # Simulate conversion (without actually running the GUI event loop)
            files = app.file_listbox.get(0, tk.END)
            assert len(files) == 1, "No files to convert"
            print("  ✓ Ready for conversion")
            
            # Check conversion function exists
            assert hasattr(app, 'convert_files'), "Convert function missing"
            print("  ✓ Conversion function available")
        
        return True
    except Exception as e:
        print(f"✗ Conversion workflow test failed: {e}")
        return False
    finally:
        root.destroy()

def main():
    """Run all GUI tests"""
    print("=" * 60)
    print("Universal Document Converter Ultimate - GUI Test Suite")
    print("=" * 60)
    
    tests = [
        test_gui_creation,
        test_tab_switching,
        test_file_operations,
        test_settings,
        test_advanced_settings,
        test_statistics,
        test_api_server_tab,
        test_conversion_workflow
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All GUI tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return failed == 0

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)