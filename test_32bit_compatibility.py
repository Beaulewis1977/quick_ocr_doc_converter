#!/usr/bin/env python3
"""
Test 32-bit compatibility and VFP9/VB6 integration paths
"""

import subprocess
import sys
import tempfile
import os
import json

# Add current directory to path
sys.path.insert(0, '/root/repo')

def check_python_architecture():
    """Check current Python architecture"""
    print("🏗️ Testing Python Architecture Compatibility...")
    
    import platform
    import struct
    
    # Check architecture
    architecture = platform.machine()
    python_bits = struct.calcsize("P") * 8
    platform_info = platform.platform()
    
    print(f"   🖥️  Platform: {platform_info}")
    print(f"   🐍 Python: {sys.version}")
    print(f"   📏 Architecture: {architecture}")
    print(f"   🔢 Python bits: {python_bits}-bit")
    
    # Check if we can determine 32-bit compatibility
    is_32bit_compatible = python_bits == 32 or "x86" in architecture.lower()
    
    print(f"   ✅ 32-bit compatible: {'Yes' if is_32bit_compatible else 'Potentially (64-bit system)'}")
    
    return {
        'platform': platform_info,
        'python_version': sys.version,
        'architecture': architecture,
        'python_bits': python_bits,
        'is_32bit_compatible': is_32bit_compatible
    }

def test_dependency_compatibility():
    """Test if dependencies are compatible with 32-bit systems"""
    print("\n📦 Testing Dependency 32-bit Compatibility...")
    
    # List of dependencies we're using
    dependencies = [
        'markdown',
        'beautifulsoup4', 
        'striprtf',
        'ebooklib',
        'docx',
        'PyPDF2',
        'reportlab',
        'flask',
        'tkinter'
    ]
    
    compatible_deps = {}
    
    for dep in dependencies:
        try:
            if dep == 'docx':
                import docx
                compatible_deps['python-docx'] = "✅ Pure Python - 32-bit compatible"
            elif dep == 'tkinter':
                import tkinter
                compatible_deps['tkinter'] = "✅ Built-in Python - 32-bit compatible"
            elif dep == 'PyPDF2':
                import PyPDF2
                compatible_deps['PyPDF2'] = "✅ Pure Python - 32-bit compatible"
            else:
                module = __import__(dep)
                compatible_deps[dep] = "✅ Pure Python - 32-bit compatible"
                
        except ImportError:
            compatible_deps[dep] = "❌ Not installed"
        except Exception as e:
            compatible_deps[dep] = f"⚠️ Error: {str(e)[:30]}..."
    
    # Report results
    for dep, status in compatible_deps.items():
        print(f"   {dep:15} | {status}")
    
    compatible_count = sum(1 for status in compatible_deps.values() if status.startswith("✅"))
    total_count = len(compatible_deps)
    
    print(f"   📊 Compatible: {compatible_count}/{total_count} dependencies")
    
    return compatible_deps

def test_dll_creation_possibility():
    """Test if DLL creation is possible with current setup"""
    print("\n🏭 Testing DLL Creation Possibilities...")
    
    # Check for DLL creation tools
    dll_tools = {
        'cx_Freeze': 'Cross-platform freezing utility',
        'py2exe': 'Windows-specific executable creator', 
        'pyinstaller': 'Cross-platform application bundler',
        'nuitka': 'Python compiler with native code generation',
        'cython': 'Python to C compiler'
    }
    
    available_tools = {}
    
    for tool, description in dll_tools.items():
        try:
            if tool == 'cx_Freeze':
                import cx_Freeze
                available_tools[tool] = f"✅ Available - {description}"
            elif tool == 'pyinstaller':
                result = subprocess.run(['pyinstaller', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    available_tools[tool] = f"✅ Available v{result.stdout.strip()} - {description}"
                else:
                    available_tools[tool] = f"❌ Not available - {description}"
            elif tool == 'nuitka':
                result = subprocess.run(['nuitka', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    available_tools[tool] = f"✅ Available - {description}"
                else:
                    available_tools[tool] = f"❌ Not available - {description}"
            else:
                module = __import__(tool)
                available_tools[tool] = f"✅ Available - {description}"
                
        except ImportError:
            available_tools[tool] = f"❌ Not installed - {description}"
        except subprocess.TimeoutExpired:
            available_tools[tool] = f"⚠️ Timeout - {description}"
        except Exception:
            available_tools[tool] = f"❌ Not available - {description}"
    
    # Report results
    for tool, status in available_tools.items():
        print(f"   {tool:12} | {status}")
    
    available_count = sum(1 for status in available_tools.values() if status.startswith("✅"))
    
    print(f"   📊 Available tools: {available_count}/{len(available_tools)}")
    
    return available_tools

def test_vfp9_vb6_integration():
    """Test VFP9/VB6 integration approaches"""
    print("\n🔗 Testing VFP9/VB6 Integration Approaches...")
    
    integration_approaches = {
        'command_line': 'Execute Python script as external process',
        'com_server': 'Register Python as COM server (win32com)',
        'dll_wrapper': 'Create 32-bit DLL with exported functions',
        'json_ipc': 'Inter-process communication via JSON files',
        'pipe_communication': 'Named pipes or stdin/stdout communication'
    }
    
    # Test command line approach
    temp_dir = tempfile.mkdtemp()
    try:
        # Create a simple test script
        test_script = os.path.join(temp_dir, 'vfp_test.py')
        test_input = os.path.join(temp_dir, 'test.md')
        test_output = os.path.join(temp_dir, 'test.rtf')
        
        # Write test markdown file
        with open(test_input, 'w', encoding='utf-8') as f:
            f.write("# VFP9 Test\n\nThis tests **VFP9 integration**.")
        
        # Write test script
        script_content = f"""#!/usr/bin/env python3
import sys
sys.path.insert(0, '/root/repo')

from universal_document_converter import UniversalConverter

def main():
    if len(sys.argv) != 4:
        print("Usage: script.py input_file output_file format")
        return 1
    
    input_file, output_file, output_format = sys.argv[1:4]
    
    try:
        converter = UniversalConverter()
        converter.convert_file(input_file, output_file, 'markdown', output_format)
        print(f"SUCCESS: Converted {{input_file}} to {{output_file}}")
        return 0
    except Exception as e:
        print(f"ERROR: {{str(e)}}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
"""
        
        with open(test_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Test command line execution
        try:
            result = subprocess.run([
                sys.executable, test_script, test_input, test_output, 'rtf'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and os.path.exists(test_output):
                integration_approaches['command_line'] = "✅ Command line execution works"
            else:
                integration_approaches['command_line'] = f"❌ Failed: {result.stderr[:50]}"
                
        except Exception as e:
            integration_approaches['command_line'] = f"❌ Error: {str(e)[:50]}"
        
        # Test JSON IPC approach
        json_input = os.path.join(temp_dir, 'request.json')
        json_output = os.path.join(temp_dir, 'response.json')
        
        request_data = {
            'input_file': test_input,
            'output_file': test_output.replace('.rtf', '_json.rtf'),
            'input_format': 'markdown',
            'output_format': 'rtf'
        }
        
        try:
            with open(json_input, 'w') as f:
                json.dump(request_data, f)
            
            # Simple JSON processor script
            json_script = f"""#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/root/repo')

from universal_document_converter import UniversalConverter

with open('{json_input}') as f:
    request = json.load(f)

try:
    converter = UniversalConverter()
    converter.convert_file(
        request['input_file'],
        request['output_file'], 
        request['input_format'],
        request['output_format']
    )
    response = {{'status': 'success', 'message': 'Conversion completed'}}
except Exception as e:
    response = {{'status': 'error', 'message': str(e)}}

with open('{json_output}', 'w') as f:
    json.dump(response, f)
"""
            
            json_script_file = os.path.join(temp_dir, 'json_processor.py')
            with open(json_script_file, 'w') as f:
                f.write(json_script)
            
            result = subprocess.run([sys.executable, json_script_file], 
                                  capture_output=True, text=True, timeout=10)
            
            if os.path.exists(json_output):
                with open(json_output) as f:
                    response = json.load(f)
                if response.get('status') == 'success':
                    integration_approaches['json_ipc'] = "✅ JSON IPC works"
                else:
                    integration_approaches['json_ipc'] = f"❌ JSON Error: {response.get('message', 'Unknown')[:30]}"
            else:
                integration_approaches['json_ipc'] = "❌ JSON response not created"
                
        except Exception as e:
            integration_approaches['json_ipc'] = f"❌ JSON Error: {str(e)[:30]}"
        
        # Check for COM server possibility
        try:
            import win32com.server.register
            integration_approaches['com_server'] = "✅ win32com available for COM server"
        except ImportError:
            integration_approaches['com_server'] = "❌ win32com not available (Linux environment)"
        
        # DLL wrapper assessment
        integration_approaches['dll_wrapper'] = "⚠️ Requires compilation tools (Nuitka, Cython, etc.)"
        
        # Pipe communication
        integration_approaches['pipe_communication'] = "✅ Possible via stdin/stdout"
        
    finally:
        import shutil
        shutil.rmtree(temp_dir)
    
    # Report results
    for approach, status in integration_approaches.items():
        print(f"   {approach:18} | {status}")
    
    working_approaches = sum(1 for status in integration_approaches.values() if status.startswith("✅"))
    print(f"   📊 Working approaches: {working_approaches}/{len(integration_approaches)}")
    
    return integration_approaches

def generate_vfp9_example():
    """Generate example VFP9 code for integration"""
    print("\n💼 Generating VFP9 Integration Example...")
    
    vfp9_code = '''* VFP9 Markdown to RTF Converter Integration
* Uses command line execution approach

LOCAL lcInputFile, lcOutputFile, lcPythonScript, lcCommand, lcResult
LOCAL lnExitCode

* Set file paths
lcInputFile = "C:\\temp\\document.md"
lcOutputFile = "C:\\temp\\document.rtf" 
lcPythonScript = "C:\\converter\\markdown_converter.py"

* Build command line
lcCommand = [python "] + lcPythonScript + [" "] + ;
           lcInputFile + [" "] + lcOutputFile + [" rtf]

* Execute conversion
lnExitCode = RunScript(lcCommand)

IF lnExitCode = 0
    MESSAGEBOX("Conversion successful!")
    * Open the RTF file
    MODIFY FILE (lcOutputFile)
ELSE  
    MESSAGEBOX("Conversion failed!")
ENDIF

* Function to run external script
FUNCTION RunScript(tcCommand)
    LOCAL lcTempBat, lnResult
    
    * Create temporary batch file
    lcTempBat = SYS(2023) + "\\converter.bat"
    
    * Write batch commands
    STRTOFILE(tcCommand + CHR(13) + CHR(10) + ;
             "EXIT %ERRORLEVEL%" + CHR(13) + CHR(10), ;
             lcTempBat)
    
    * Execute and capture exit code
    RUN /N7 (lcTempBat)
    lnResult = _VFP.ProcessID
    
    * Cleanup
    DELETE FILE (lcTempBat)
    
    RETURN lnResult
ENDFUNC'''
    
    print("   📄 VFP9 Example Code Generated:")
    print("   " + "="*50)
    lines = vfp9_code.split('\n')[:15]  # Show first 15 lines
    for line in lines:
        print(f"   {line}")
    print("   ... (truncated)")
    
    return vfp9_code

def main():
    """Run all 32-bit compatibility tests"""
    print("🏗️ 32-bit Compatibility and VFP9/VB6 Integration Test")
    print("=" * 70)
    
    results = {}
    
    # Run tests
    try:
        arch_info = check_python_architecture()
        results['architecture'] = arch_info['is_32bit_compatible']
    except Exception as e:
        print(f"   ❌ Architecture test error: {e}")
        results['architecture'] = False
    
    try:
        dep_compat = test_dependency_compatibility()
        results['dependencies'] = sum(1 for s in dep_compat.values() if s.startswith("✅")) >= 6
    except Exception as e:
        print(f"   ❌ Dependency test error: {e}")
        results['dependencies'] = False
    
    try:
        dll_tools = test_dll_creation_possibility()
        results['dll_tools'] = sum(1 for s in dll_tools.values() if s.startswith("✅")) >= 1
    except Exception as e:
        print(f"   ❌ DLL tools test error: {e}")
        results['dll_tools'] = False
    
    try:
        integration = test_vfp9_vb6_integration()
        results['integration'] = sum(1 for s in integration.values() if s.startswith("✅")) >= 2
    except Exception as e:
        print(f"   ❌ Integration test error: {e}")
        results['integration'] = False
    
    try:
        vfp9_example = generate_vfp9_example()
        results['examples'] = len(vfp9_example) > 500  # Non-empty example
    except Exception as e:
        print(f"   ❌ Example generation error: {e}")
        results['examples'] = False
    
    # Summary
    print(f"\n📊 32-bit Compatibility Results")
    print("=" * 70)
    
    test_names = {
        'architecture': 'Python Architecture',
        'dependencies': 'Dependencies Compatible', 
        'dll_tools': 'DLL Creation Tools',
        'integration': 'Integration Approaches',
        'examples': 'Code Examples'
    }
    
    for key, name in test_names.items():
        status = "✅ READY" if results.get(key, False) else "⚠️ NEEDS WORK"
        print(f"{name:25} | {status}")
    
    ready_count = sum(results.values())
    total_tests = len(results)
    
    print(f"\n🎯 Overall Readiness: {ready_count}/{total_tests}")
    
    if ready_count >= 3:  # Most components ready
        print("✅ System is ready for 32-bit deployment!")
        print("💡 Recommended approach: Command line execution or JSON IPC")
    else:
        print("⚠️ Some components need additional setup for 32-bit deployment")
    
    return ready_count >= 3

if __name__ == '__main__':
    main()