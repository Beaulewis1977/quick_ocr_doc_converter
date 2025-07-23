#!/usr/bin/env python3
"""Create comprehensive testing package for branch testing"""

import zipfile
import os
from pathlib import Path

def create_testing_package():
    """Create a comprehensive testing package"""
    
    print("Creating comprehensive testing package...")
    
    # Define output path
    output_path = Path("dist/Universal-Document-Converter-v3.1.1-Python3-Migration-TESTING.zip")
    
    # Files and directories to exclude
    exclude_patterns = {
        '.git', '__pycache__', '*.pyc', 'dist', 'test_env', 'lint_env',
        '.pytest_cache', '*.log', '.DS_Store', 'Thumbs.db'
    }
    
    exclude_dirs = {'.git', '__pycache__', 'dist', 'test_env', 'lint_env', '.pytest_cache'}
    
    def should_exclude(path_str):
        """Check if a path should be excluded"""
        path = Path(path_str)
        
        # Check if any parent directory is in exclude_dirs
        for part in path.parts:
            if part in exclude_dirs:
                return True
        
        # Check file patterns
        if path.name.startswith('.') and path.name not in {'.gitignore'}:
            return True
        if path.suffix in {'.pyc', '.log'}:
            return True
            
        return False
    
    # Create zip file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Add all files from current directory
        for root, dirs, files in os.walk('.'):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, '.')
                
                if not should_exclude(rel_path):
                    arcname = f"Universal-Document-Converter-v3.1.1-Python3-Migration/{rel_path}"
                    zipf.write(file_path, arcname)
                    print(f"  Added: {rel_path}")
    
    # Get file size
    size_bytes = output_path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)
    
    print(f"\n✅ Testing package created: {output_path}")
    print(f"📦 Size: {size_mb:.1f} MB ({size_bytes:,} bytes)")
    
    return output_path

if __name__ == "__main__":
    create_testing_package()