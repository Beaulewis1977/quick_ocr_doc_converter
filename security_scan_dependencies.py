#!/usr/bin/env python3
"""
Dependency Security Scanner for OCR Document Converter
Scans dependencies for known vulnerabilities and security issues
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DependencySecurityScanner:
    """Scans dependencies for security vulnerabilities"""
    
    def __init__(self):
        self.vulnerabilities_found = []
        self.scan_results = {}
        
    def check_tool_availability(self, tool: str) -> bool:
        """Check if a security scanning tool is available"""
        try:
            result = subprocess.run([tool, "--version"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            return False
    
    def install_security_tools(self) -> bool:
        """Install security scanning tools if not available"""
        tools_to_install = []
        
        if not self.check_tool_availability("safety"):
            tools_to_install.append("safety")
        if not self.check_tool_availability("bandit"):
            tools_to_install.append("bandit")
        if not self.check_tool_availability("pip-audit"):
            tools_to_install.append("pip-audit")
            
        if not tools_to_install:
            logger.info("All security tools already available")
            return True
            
        logger.info(f"Installing security tools: {', '.join(tools_to_install)}")
        
        try:
            for tool in tools_to_install:
                logger.info(f"Installing {tool}...")
                result = subprocess.run([sys.executable, "-m", "pip", "install", tool],
                                      capture_output=True, text=True, timeout=120)
                if result.returncode != 0:
                    logger.error(f"Failed to install {tool}: {result.stderr}")
                    return False
                logger.info(f"✅ {tool} installed successfully")
            return True
        except subprocess.TimeoutExpired:
            logger.error("Tool installation timed out")
            return False
        except Exception as e:
            logger.error(f"Error installing security tools: {e}")
            return False
    
    def run_safety_scan(self) -> Dict[str, Any]:
        """Run Safety vulnerability scan"""
        logger.info("Running Safety vulnerability scan...")
        
        try:
            # Check if requirements file exists
            req_file = Path("requirements.txt")
            if not req_file.exists():
                return {"status": "error", "message": "requirements.txt not found"}
                
            # Run safety check
            result = subprocess.run([
                "safety", "check", "-r", "requirements.txt", "--json"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # No vulnerabilities found
                return {
                    "status": "clean", 
                    "vulnerabilities": [],
                    "message": "No known vulnerabilities found"
                }
            else:
                # Parse JSON output if available
                try:
                    vulnerabilities = json.loads(result.stdout)
                    return {
                        "status": "vulnerabilities_found",
                        "vulnerabilities": vulnerabilities,
                        "count": len(vulnerabilities)
                    }
                except json.JSONDecodeError:
                    return {
                        "status": "error",
                        "message": f"Safety scan failed: {result.stderr}"
                    }
                    
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Safety scan timed out"}
        except Exception as e:
            return {"status": "error", "message": f"Safety scan error: {e}"}
    
    def run_pip_audit_scan(self) -> Dict[str, Any]:
        """Run pip-audit vulnerability scan"""
        logger.info("Running pip-audit vulnerability scan...")
        
        try:
            # Run pip-audit
            result = subprocess.run([
                "pip-audit", "--format=json", "--progress-spinner=off"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                try:
                    audit_results = json.loads(result.stdout)
                    vulnerabilities = audit_results.get("vulnerabilities", [])
                    
                    if not vulnerabilities:
                        return {
                            "status": "clean",
                            "vulnerabilities": [],
                            "message": "No vulnerabilities found by pip-audit"
                        }
                    else:
                        return {
                            "status": "vulnerabilities_found",
                            "vulnerabilities": vulnerabilities,
                            "count": len(vulnerabilities)
                        }
                except json.JSONDecodeError:
                    return {"status": "error", "message": "Failed to parse pip-audit output"}
            else:
                return {"status": "error", "message": f"pip-audit failed: {result.stderr}"}
                
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "pip-audit scan timed out"}
        except Exception as e:
            return {"status": "error", "message": f"pip-audit error: {e}"}
    
    def run_bandit_scan(self) -> Dict[str, Any]:
        """Run Bandit security scan on Python code"""
        logger.info("Running Bandit security scan on Python code...")
        
        try:
            # Run bandit on Python files
            result = subprocess.run([
                "bandit", "-r", ".", "-f", "json", "--skip", "B101,B601"
            ], capture_output=True, text=True, timeout=120)
            
            try:
                bandit_results = json.loads(result.stdout)
                issues = bandit_results.get("results", [])
                
                # Filter out low-severity issues for this report
                high_issues = [issue for issue in issues 
                             if issue.get("issue_severity") in ["HIGH", "MEDIUM"]]
                
                return {
                    "status": "completed",
                    "total_issues": len(issues),
                    "high_severity_issues": len(high_issues),
                    "issues": high_issues[:5],  # Limit to first 5 for report
                    "message": f"Found {len(issues)} total issues, {len(high_issues)} high/medium severity"
                }
            except json.JSONDecodeError:
                return {"status": "error", "message": "Failed to parse Bandit output"}
                
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Bandit scan timed out"}
        except Exception as e:
            return {"status": "error", "message": f"Bandit scan error: {e}"}
    
    def generate_security_report(self) -> str:
        """Generate comprehensive security report"""
        report = []
        report.append("=" * 80)
        report.append("DEPENDENCY SECURITY SCAN REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Safety scan results
        safety_results = self.scan_results.get("safety", {})
        report.append("🔍 SAFETY VULNERABILITY SCAN")
        report.append("-" * 40)
        if safety_results.get("status") == "clean":
            report.append("✅ No known vulnerabilities found")
        elif safety_results.get("status") == "vulnerabilities_found":
            count = safety_results.get("count", 0)
            report.append(f"❌ {count} vulnerabilities found!")
            for vuln in safety_results.get("vulnerabilities", [])[:3]:
                pkg = vuln.get("package", "unknown")
                vuln_id = vuln.get("vulnerability_id", "unknown")
                report.append(f"   - {pkg}: {vuln_id}")
        else:
            report.append(f"⚠️ {safety_results.get('message', 'Scan failed')}")
        report.append("")
        
        # pip-audit results
        audit_results = self.scan_results.get("pip_audit", {})
        report.append("🔍 PIP-AUDIT VULNERABILITY SCAN")
        report.append("-" * 40)
        if audit_results.get("status") == "clean":
            report.append("✅ No vulnerabilities found")
        elif audit_results.get("status") == "vulnerabilities_found":
            count = audit_results.get("count", 0)
            report.append(f"❌ {count} vulnerabilities found!")
            for vuln in audit_results.get("vulnerabilities", [])[:3]:
                pkg = vuln.get("package", "unknown")
                vuln_id = vuln.get("id", "unknown")
                report.append(f"   - {pkg}: {vuln_id}")
        else:
            report.append(f"⚠️ {audit_results.get('message', 'Scan failed')}")
        report.append("")
        
        # Bandit results
        bandit_results = self.scan_results.get("bandit", {})
        report.append("🔍 BANDIT CODE SECURITY SCAN")
        report.append("-" * 40)
        if bandit_results.get("status") == "completed":
            total = bandit_results.get("total_issues", 0)
            high = bandit_results.get("high_severity_issues", 0)
            if total == 0:
                report.append("✅ No security issues found")
            else:
                report.append(f"⚠️ {total} total issues, {high} high/medium severity")
                for issue in bandit_results.get("issues", [])[:3]:
                    test_id = issue.get("test_id", "unknown")
                    filename = Path(issue.get("filename", "")).name
                    report.append(f"   - {test_id} in {filename}")
        else:
            report.append(f"⚠️ {bandit_results.get('message', 'Scan failed')}")
        report.append("")
        
        # Summary and recommendations
        report.append("📋 SECURITY RECOMMENDATIONS")
        report.append("-" * 40)
        report.append("1. Use requirements-pinned.txt for production deployments")
        report.append("2. Regularly update dependencies to latest secure versions")
        report.append("3. Run security scans in CI/CD pipeline")
        report.append("4. Monitor security advisories for used packages")
        report.append("5. Consider using virtual environments for isolation")
        report.append("")
        
        return "\\n".join(report)
    
    def run_full_scan(self) -> bool:
        """Run complete security scan"""
        logger.info("Starting comprehensive dependency security scan...")
        
        # Install tools if needed
        if not self.install_security_tools():
            logger.error("Failed to install required security tools")
            return False
        
        # Run all scans
        self.scan_results["safety"] = self.run_safety_scan()
        self.scan_results["pip_audit"] = self.run_pip_audit_scan()
        self.scan_results["bandit"] = self.run_bandit_scan()
        
        # Generate and save report
        report = self.generate_security_report()
        
        # Save report to file
        report_file = Path("security_scan_report.txt")
        report_file.write_text(report)
        logger.info(f"Security report saved to: {report_file}")
        
        # Print summary
        print("\\n" + report)
        
        # Check if any critical vulnerabilities were found
        safety_vulns = self.scan_results["safety"].get("count", 0)
        audit_vulns = self.scan_results["pip_audit"].get("count", 0)
        
        if safety_vulns > 0 or audit_vulns > 0:
            logger.warning(f"Found {safety_vulns + audit_vulns} total vulnerabilities")
            return False
        else:
            logger.info("✅ No critical vulnerabilities found")
            return True

def main():
    """Main function"""
    scanner = DependencySecurityScanner()
    
    print("🔐 OCR Document Converter - Dependency Security Scanner")
    print("=" * 60)
    
    success = scanner.run_full_scan()
    
    if success:
        print("\\n✅ Security scan completed successfully!")
        sys.exit(0)
    else:
        print("\\n❌ Security issues found! Please review the report.")
        sys.exit(1)

if __name__ == "__main__":
    main()