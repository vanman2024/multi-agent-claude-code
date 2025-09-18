#!/usr/bin/env python3
"""
Test runner script for SignalHire Agent.
Provides convenient commands for running different test categories.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and print the description."""
    print(f"\n🧪 {description}")
    print("=" * 50)
    
    # Use the run.py wrapper for consistent environment
    full_cmd = ["python3", "run.py", "-m"] + cmd
    
    try:
        result = subprocess.run(full_cmd, check=False)
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
        return False


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Run SignalHire Agent tests")
    parser.add_argument(
        "category",
        nargs="?",
        choices=["smoke", "unit", "integration", "browser", "contract", "performance", "all", "quick"],
        default="quick",
        help="Test category to run (default: quick)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--no-creds", action="store_true", help="Skip tests requiring credentials")
    parser.add_argument("--fast", action="store_true", help="Skip slow tests")
    
    args = parser.parse_args()
    
    # Build pytest command
    pytest_args = ["pytest"]
    
    if args.verbose:
        pytest_args.append("-v")
    else:
        pytest_args.append("-q")
    
    # Add markers for filtering
    markers = []
    if args.no_creds:
        markers.append("not credentials")
    if args.fast:
        markers.append("not slow")
    
    if markers:
        pytest_args.extend(["-m", " and ".join(markers)])
    
    # Determine which tests to run
    success = True
    
    if args.category == "smoke":
        success &= run_command(pytest_args + ["tests/smoke/"], "Smoke Tests - Basic Functionality")
        
    elif args.category == "unit":
        success &= run_command(pytest_args + ["tests/unit/"], "Unit Tests - Component Testing")
        
    elif args.category == "integration":
        success &= run_command(pytest_args + ["tests/integration/"], "Integration Tests - External Services")
        
    elif args.category == "browser":
        success &= run_command(pytest_args + ["tests/browser/"], "Browser Tests - Automation Testing")
        
    elif args.category == "contract":
        success &= run_command(pytest_args + ["tests/contract/"], "Contract Tests - API/UI Validation")
        
    elif args.category == "performance":
        success &= run_command(pytest_args + ["tests/performance/"], "Performance Tests - Load Testing")
        
    elif args.category == "quick":
        # Quick test suite for development
        success &= run_command(
            pytest_args + ["tests/smoke/", "tests/unit/"],
            "Quick Tests - Smoke + Unit (Development)"
        )
        
    elif args.category == "all":
        # Full test suite
        categories = [
            ("tests/smoke/", "Smoke Tests"),
            ("tests/unit/", "Unit Tests"),
            ("tests/contract/", "Contract Tests"),
            ("tests/integration/", "Integration Tests"),
            ("tests/browser/", "Browser Tests"),
            ("tests/performance/", "Performance Tests"),
        ]
        
        for test_dir, description in categories:
            success &= run_command(pytest_args + [test_dir], description)
    
    # Final result
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n❌ Test run interrupted")
        sys.exit(1)