#!/usr/bin/env python3
"""
Demo System Tray Application for Quick Document Convertor
Test the system tray functionality without full installation
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def check_dependencies():
    """Check if system tray dependencies are available"""
    missing = []
    
    try:
        import pystray
    except ImportError:
        missing.append("pystray")
    
    try:
        import PIL
    except ImportError:
        missing.append("pillow")
    
    return missing

def install_dependencies():
    """Install missing dependencies"""
    missing = check_dependencies()
    
    if not missing:
        print("✅ All dependencies are available!")
        return True
    
    print(f"📦 Missing dependencies: {', '.join(missing)}")
    
    try:
        import subprocess
        for dep in missing:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def demo_tray():
    """Demo the system tray functionality"""
    print("🚀 Starting System Tray Demo...")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        response = input("Install missing dependencies? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            if not install_dependencies():
                return
        else:
            print("Cannot run demo without dependencies")
            return
    
    # Import and run tray application
    try:
        from enhanced_system_tray import QuickConverterTray
        
        print("✅ Starting system tray application...")
        print("💡 Look for the Quick Document Convertor icon in your system tray")
        print("💡 Right-click the icon to see the menu")
        print("💡 Close this window or press Ctrl+C to exit")
        
        app = QuickConverterTray()
        app.run()
        
    except ImportError as e:
        print(f"❌ Failed to import tray application: {e}")
        print("Make sure enhanced_system_tray.py exists in the current directory")
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error running tray demo: {e}")

def main():
    """Main function"""
    print("🎯 Quick Document Convertor - System Tray Demo")
    print("=" * 50)
    
    # Show current directory
    print(f"📁 Current directory: {Path.cwd()}")
    
    # Check if main application exists
    main_app = Path("universal_document_converter.py")
    if main_app.exists():
        print("✅ Main application found")
    else:
        print("⚠️  Main application not found (some features may not work)")
    
    # Check if CLI exists
    cli_app = Path("cli.py")
    if cli_app.exists():
        print("✅ CLI application found")
    else:
        print("⚠️  CLI application not found (quick convert may not work)")
    
    print("\n" + "=" * 50)
    
    # Run demo
    demo_tray()
    
    print("\n👋 Demo completed!")

if __name__ == "__main__":
    main() 