#!/usr/bin/env python3
"""
Secure Dependency Update Script for OCR Document Converter
Updates dependencies while checking for security issues
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import List, Dict, Any
import logging
from utils.safe_input import safe_input, safe_yes_no

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecureDependencyUpdater:
    """Handles secure dependency updates"""
    
    def __init__(self):
        self.backup_requirements = None
        
    def backup_current_requirements(self) -> bool:
        """Backup current requirements.txt"""
        try:
            req_file = Path("requirements.txt")
            if req_file.exists():
                backup_file = Path("requirements.txt.backup")
                backup_file.write_text(req_file.read_text())
                self.backup_requirements = backup_file
                logger.info(f"Backed up requirements to: {backup_file}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to backup requirements: {e}")
            return False
    
    def restore_requirements(self) -> bool:
        """Restore requirements from backup"""
        try:
            if self.backup_requirements and self.backup_requirements.exists():
                req_file = Path("requirements.txt")
                req_file.write_text(self.backup_requirements.read_text())
                logger.info("Restored requirements from backup")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to restore requirements: {e}")
            return False
    
    def check_outdated_packages(self) -> List[Dict[str, str]]:
        """Check for outdated packages"""
        try:
            logger.info("Checking for outdated packages...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "list", "--outdated", "--format=json"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                outdated = json.loads(result.stdout)
                return outdated
            else:
                logger.error(f"Failed to check outdated packages: {result.stderr}")
                return []
                
        except Exception as e:
            logger.error(f"Error checking outdated packages: {e}")
            return []
    
    def update_package_safely(self, package: str, version: str = None) -> bool:
        """Update a single package safely"""
        try:
            if version:
                package_spec = f"{package}=={version}"
            else:
                package_spec = package
                
            logger.info(f"Updating {package_spec}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", package_spec
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logger.info(f"✅ Successfully updated {package}")
                return True
            else:
                logger.error(f"❌ Failed to update {package}: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating {package}: {e}")
            return False
    
    def generate_pinned_requirements(self) -> bool:
        """Generate pinned requirements file from current environment"""
        try:
            logger.info("Generating pinned requirements...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "freeze"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                pinned_file = Path("requirements-generated.txt")
                pinned_file.write_text(result.stdout)
                logger.info(f"Generated pinned requirements: {pinned_file}")
                return True
            else:
                logger.error(f"Failed to generate requirements: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error generating requirements: {e}")
            return False
    
    def run_security_scan_after_update(self) -> bool:
        """Run security scan after updating dependencies"""
        try:
            scanner_path = Path("security_scan_dependencies.py")
            if scanner_path.exists():
                logger.info("Running security scan after update...")
                result = subprocess.run([
                    sys.executable, str(scanner_path)
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    logger.info("✅ Security scan passed")
                    return True
                else:
                    logger.warning("⚠️ Security scan found issues")
                    print(result.stdout)
                    return False
            else:
                logger.warning("Security scanner not found, skipping scan")
                return True
                
        except Exception as e:
            logger.error(f"Error running security scan: {e}")
            return False
    
    def update_dependencies_interactive(self) -> bool:
        """Interactively update dependencies with security checks"""
        logger.info("Starting interactive dependency update...")
        
        # Backup current requirements
        if not self.backup_current_requirements():
            logger.error("Failed to backup requirements")
            return False
        
        try:
            # Check for outdated packages
            outdated = self.check_outdated_packages()
            
            if not outdated:
                logger.info("All packages are up to date")
                return True
            
            logger.info(f"Found {len(outdated)} outdated packages")
            
            # Update packages one by one
            updated_packages = []
            failed_packages = []
            
            for package_info in outdated:
                package = package_info["name"]
                current = package_info["version"]
                latest = package_info["latest_version"]
                
                # Skip development packages
                if package in ["pip", "setuptools", "wheel"]:
                    continue
                
                print(f"\\n📦 {package}: {current} → {latest}")
                
                # For security-critical packages, be more cautious
                security_critical = ["cryptography", "requests", "urllib3", "pillow"]
                
                if package.lower() in security_critical:
                    response = safe_input(f"Update security-critical package {package}?", 
                                        valid_options=["y", "n", "s", "yes", "no", "skip"],
                                        max_length=10)
                    if response.lower() in ['s', 'skip']:
                        continue
                    elif response.lower() not in ['y', 'yes']:
                        continue
                
                # Update the package
                if self.update_package_safely(package):
                    updated_packages.append(package)
                else:
                    failed_packages.append(package)
            
            # Generate new pinned requirements
            self.generate_pinned_requirements()
            
            # Run security scan
            if not self.run_security_scan_after_update():
                logger.warning("Security scan failed, consider reviewing updates")
                if not safe_yes_no("Continue despite security warnings?"):
                    logger.info("Restoring previous requirements...")
                    self.restore_requirements()
                    return False
            
            logger.info(f"✅ Successfully updated {len(updated_packages)} packages")
            if failed_packages:
                logger.warning(f"⚠️ Failed to update: {', '.join(failed_packages)}")
            
            return True
            
        except KeyboardInterrupt:
            logger.info("Update cancelled by user")
            self.restore_requirements()
            return False
        except Exception as e:
            logger.error(f"Update failed: {e}")
            self.restore_requirements()
            return False

def main():
    """Main function"""
    updater = SecureDependencyUpdater()
    
    print("🔄 OCR Document Converter - Secure Dependency Updater")
    print("=" * 60)
    print("This script will help you safely update dependencies")
    print("with security scanning and backup/restore functionality.")
    print()
    
    if not safe_yes_no("Start interactive dependency update?"):
        print("Update cancelled.")
        sys.exit(0)
    
    success = updater.update_dependencies_interactive()
    
    if success:
        print("\\n✅ Dependency update completed successfully!")
        print("Remember to test your application after updating dependencies.")
    else:
        print("\\n❌ Dependency update failed or was cancelled.")
        print("Check the logs above for details.")

if __name__ == "__main__":
    main()