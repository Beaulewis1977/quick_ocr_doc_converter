#!/usr/bin/env python3
"""
Test runner for Enhanced OCR System

Provides comprehensive test execution with different test suites,
coverage reporting, and performance analysis.

Author: Terry AI Agent for Terragon Labs
"""

import sys
import subprocess
import argparse
from pathlib import Path
import time


def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print('='*60)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        end_time = time.time()
        print(f"\n✅ {description} completed successfully in {end_time - start_time:.2f}s")
        return True
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        print(f"\n❌ {description} failed after {end_time - start_time:.2f}s")
        print(f"Exit code: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Command not found: {command[0]}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Enhanced OCR System Test Runner")
    parser.add_argument(
        "--suite", 
        choices=['all', 'unit', 'integration', 'security', 'performance', 'gui', 'cloud'],
        default='all',
        help="Test suite to run"
    )
    parser.add_argument(
        "--coverage", 
        action='store_true',
        help="Generate coverage report"
    )
    parser.add_argument(
        "--parallel", 
        action='store_true',
        help="Run tests in parallel"
    )
    parser.add_argument(
        "--verbose", 
        action='store_true',
        help="Verbose output"
    )
    parser.add_argument(
        "--quick", 
        action='store_true',
        help="Skip slow tests"
    )
    parser.add_argument(
        "--install-deps", 
        action='store_true',
        help="Install test dependencies first"
    )
    
    args = parser.parse_args()
    
    # Change to project directory
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    # Install dependencies if requested
    if args.install_deps:
        print("\n🔧 Installing test dependencies...")
        deps_command = [
            sys.executable, "-m", "pip", "install",
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "pytest-mock>=3.6",
            "pytest-timeout>=2.1",
            "pytest-xdist>=2.0",  # For parallel execution
            "coverage>=5.0",
            "Pillow>=8.0",  # For image testing
            "psutil>=5.8"   # For performance testing
        ]
        
        if not run_command(deps_command, "Installing test dependencies"):
            print("❌ Failed to install dependencies")
            return 1
    
    # Build base pytest command
    pytest_cmd = [sys.executable, "-m", "pytest"]
    
    # Add test directory
    pytest_cmd.extend(["tests/"])
    
    # Configure test selection based on suite
    if args.suite == 'unit':
        pytest_cmd.extend(["-m", "not integration and not performance and not cloud"])
    elif args.suite == 'integration':
        pytest_cmd.extend(["-m", "integration"])
    elif args.suite == 'security':
        pytest_cmd.extend(["-m", "security"])
    elif args.suite == 'performance':
        pytest_cmd.extend(["-m", "performance"])
    elif args.suite == 'gui':
        pytest_cmd.extend(["-m", "gui or not gui"])  # Run GUI tests if available
    elif args.suite == 'cloud':
        pytest_cmd.extend(["-m", "cloud"])
    
    # Add quick mode (skip slow tests)
    if args.quick:
        if "-m" in pytest_cmd:
            # Extend existing marker filter
            marker_idx = pytest_cmd.index("-m") + 1
            pytest_cmd[marker_idx] += " and not slow"
        else:
            pytest_cmd.extend(["-m", "not slow"])
    
    # Add parallel execution
    if args.parallel:
        pytest_cmd.extend(["-n", "auto"])
    
    # Add verbose output
    if args.verbose:
        pytest_cmd.extend(["-v", "-s"])
    
    # Add coverage if requested
    if args.coverage:
        pytest_cmd.extend([
            "--cov=security",
            "--cov=backends", 
            "--cov=monitoring",
            "--cov-report=html:htmlcov",
            "--cov-report=term-missing",
            "--cov-report=xml",
            "--cov-fail-under=75"
        ])
    
    # Add timeout
    pytest_cmd.extend(["--timeout=300"])
    
    # Run the tests
    success = run_command(pytest_cmd, f"Running {args.suite} tests")
    
    if success:
        print("\n🎉 All tests completed successfully!")
        
        if args.coverage:
            print("\n📊 Coverage report generated:")
            print("  - HTML: htmlcov/index.html")
            print("  - XML: coverage.xml")
            print("  - Terminal output above")
        
        print("\n📁 Test artifacts:")
        print("  - Test logs: pytest output above")
        if Path("htmlcov").exists():
            print("  - Coverage HTML: htmlcov/index.html")
        if Path("coverage.xml").exists():
            print("  - Coverage XML: coverage.xml")
        
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())