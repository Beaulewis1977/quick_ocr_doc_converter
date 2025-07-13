#!/usr/bin/env python3
"""
Create desktop shortcut for Quick Document Convertor
"""
import os
import sys
from pathlib import Path

def create_desktop_shortcut():
    """Create a desktop shortcut for the application"""
    try:
        # Get paths
        current_dir = Path(__file__).parent.absolute()
        desktop = Path.home() / "Desktop"
        
        if sys.platform == "win32":
            # Windows shortcut
            import winshell
            
            shortcut_path = desktop / "Quick Document Convertor.lnk"
            target = current_dir / "🚀 Launch Quick Document Convertor.bat"
            
            winshell.CreateShortcut(
                Path=str(shortcut_path),
                Target=str(target),
                Icon=(str(current_dir / "run_app.py"), 0),
                Description="Quick Document Convertor - Fast document conversion tool"
            )
            
            print(f"✅ Desktop shortcut created: {shortcut_path}")
            
        else:
            # Linux/macOS desktop file
            shortcut_content = f"""[Desktop Entry]
Name=Quick Document Convertor
Comment=Fast document conversion tool
Exec=python3 "{current_dir}/run_app.py"
Icon=document-properties
Terminal=false
Type=Application
Categories=Office;Utility;
"""
            
            shortcut_path = desktop / "Quick Document Convertor.desktop"
            with open(shortcut_path, 'w') as f:
                f.write(shortcut_content)
            
            # Make executable
            os.chmod(shortcut_path, 0o755)
            print(f"✅ Desktop shortcut created: {shortcut_path}")
            
    except ImportError:
        print("⚠️  Creating simple batch file instead...")
        # Fallback: create simple batch file
        if sys.platform == "win32":
            batch_content = f"""@echo off
cd /d "{current_dir}"
python run_app.py
pause
"""
            shortcut_path = desktop / "Quick Document Convertor.bat"
            with open(shortcut_path, 'w') as f:
                f.write(batch_content)
            print(f"✅ Desktop launcher created: {shortcut_path}")
        
    except Exception as e:
        print(f"❌ Failed to create desktop shortcut: {e}")
        print("💡 You can manually create a shortcut to '🚀 Launch Quick Document Convertor.bat'")

if __name__ == "__main__":
    create_desktop_shortcut() 