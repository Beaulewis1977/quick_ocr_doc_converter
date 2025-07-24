#!/usr/bin/env python3
"""
Legacy DLL Builder CLI - Redirects to the correct CLI tools

This file exists for backward compatibility. The actual CLI tools are:
- dll_builder_advanced_cli.py: For building 32-bit DLLs
- document_converter_cli.py: For document conversion
"""

import sys
import os

print("=" * 60)
print("NOTICE: dll_builder_cli.py has been replaced")
print("=" * 60)
print()
print("Please use one of the following commands instead:")
print()
print("For document conversion:")
print("  python document_converter_cli.py [arguments]")
print()
print("For DLL building:")
print("  python dll_builder_advanced_cli.py [arguments]")
print()
print("Example usage:")
print("  python document_converter_cli.py input.pdf -o output.txt")
print("  python dll_builder_advanced_cli.py build")
print()
print("=" * 60)

# If arguments were provided, suggest the likely command
if len(sys.argv) > 1:
    if any(arg.endswith(('.pdf', '.docx', '.txt', '.html')) for arg in sys.argv[1:]):
        print("\nIt looks like you're trying to convert a document.")
        print("Try running:")
        print(f"  python document_converter_cli.py {' '.join(sys.argv[1:])}")
    elif any(arg in ['build', 'test', 'verify-tools'] for arg in sys.argv[1:]):
        print("\nIt looks like you're trying to build a DLL.")
        print("Try running:")
        print(f"  python dll_builder_advanced_cli.py {' '.join(sys.argv[1:])}")

sys.exit(1)