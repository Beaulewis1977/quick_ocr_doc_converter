#!/usr/bin/env python3
"""
Universal Build Script for Quick Document Convertor

This script builds packages for all supported platforms (Windows, Linux, macOS)
using the cross-platform packaging system.

Author: Beau Lewis
Project: Quick Document Convertor
"""

import argparse
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import cross_platform
from packaging import get_app_info, check_dependencies, install_dependencies


def main():
    """Main build function."""
    parser = argparse.ArgumentParser(
        description="Build Quick Document Convertor packages for all platforms"
    )
    parser.add_argument(
        "--platform", 
        choices=["windows", "linux", "macos", "all"],
        default="all",
        help="Platform to build for (default: all)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("dist"),
        help="Output directory for packages (default: dist)"
    )
    parser.add_argument(
        "--version",
        default="2.0.0",
        help="Package version (default: 2.0.0)"
    )
    parser.add_argument(
        "--icon",
        type=Path,
        help="Path to application icon"
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install missing dependencies"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Print header
    app_info = get_app_info()
    print(f"🚀 Building {app_info['name']} v{args.version}")
    print("=" * 60)
    
    # Check platform support
    current_platform = cross_platform.get_platform()
    if not cross_platform.is_supported_platform():
        print(f"❌ Unsupported platform: {current_platform}")
        return 1
    
    print(f"📍 Current platform: {current_platform}")
    print(f"🎯 Target platform(s): {args.platform}")
    print(f"📁 Output directory: {args.output_dir}")
    
    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    deps = check_dependencies()
    missing_deps = [dep for dep, available in deps.items() if not available]
    
    if missing_deps:
        print(f"⚠️  Missing dependencies: {', '.join(missing_deps)}")
        if args.install_deps:
            print("📦 Installing missing dependencies...")
            if install_dependencies():
                print("✅ Dependencies installed successfully")
            else:
                print("❌ Failed to install dependencies")
                return 1
        else:
            print("💡 Use --install-deps to install missing dependencies")
            return 1
    else:
        print("✅ All dependencies available")
    
    # Get main script path
    main_script = project_root / "universal_document_converter.py"
    if not main_script.exists():
        print(f"❌ Main script not found: {main_script}")
        return 1
    
    # Build for specified platforms
    platforms_to_build = []
    if args.platform == "all":
        platforms_to_build = ["windows", "linux", "macos"]
    else:
        platforms_to_build = [args.platform]
    
    results = {}
    
    for platform in platforms_to_build:
        print(f"\n🔨 Building for {platform}...")
        
        try:
            if platform == "windows":
                results[platform] = build_windows_packages(
                    main_script, args.output_dir, args.version, args.icon, args.verbose
                )
            elif platform == "linux":
                results[platform] = build_linux_packages(
                    main_script, args.output_dir, args.version, args.icon, args.verbose
                )
            elif platform == "macos":
                results[platform] = build_macos_packages(
                    main_script, args.output_dir, args.version, args.icon, args.verbose
                )
            
            print(f"✅ {platform} build completed")
            
        except Exception as e:
            print(f"❌ {platform} build failed: {e}")
            results[platform] = {"error": str(e)}
    
    # Print summary
    print("\n📊 Build Summary")
    print("=" * 60)
    
    for platform, result in results.items():
        print(f"\n{platform.upper()}:")
        if "error" in result:
            print(f"  ❌ Failed: {result['error']}")
        else:
            for package_type, path in result.items():
                if isinstance(path, Path) and path.exists():
                    print(f"  ✅ {package_type}: {path}")
                elif "error" in package_type:
                    print(f"  ⚠️  {package_type}: {path}")
    
    print(f"\n🎉 Build process completed!")
    print(f"📁 Output directory: {args.output_dir.absolute()}")
    
    return 0


def build_windows_packages(script_path, output_dir, version, icon_path, verbose):
    """Build Windows packages."""
    if cross_platform.get_platform() != "windows":
        print("⚠️  Cross-platform Windows building not supported yet")
        return {"note": "Cross-platform building not supported"}
    
    from packaging.build_windows import build_all_windows_packages
    return build_all_windows_packages(script_path, output_dir, version, icon_path)


def build_linux_packages(script_path, output_dir, version, icon_path, verbose):
    """Build Linux packages."""
    if cross_platform.get_platform() != "linux":
        print("⚠️  Cross-platform Linux building not supported yet")
        return {"note": "Cross-platform building not supported"}
    
    from packaging.build_linux import build_all_linux_packages
    
    # For Linux, we need the application directory, not just the script
    app_dir = script_path.parent
    return build_all_linux_packages(app_dir, output_dir, version)


def build_macos_packages(script_path, output_dir, version, icon_path, verbose):
    """Build macOS packages."""
    if cross_platform.get_platform() != "macos":
        print("⚠️  Cross-platform macOS building not supported yet")
        return {"note": "Cross-platform building not supported"}
    
    from packaging.build_macos import build_all_macos_packages
    return build_all_macos_packages(script_path, output_dir, version, icon_path)


if __name__ == "__main__":
    sys.exit(main())
