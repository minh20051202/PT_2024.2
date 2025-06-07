#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test runner script for the invoice management system.

This script provides a convenient way to run tests with various options
including test categories, coverage reports, and different test runners.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def run_pytest_tests(test_path=None, verbose=False, coverage=False):
    """Run tests using pytest."""
    cmd = ['python3', '-m', 'pytest']
    
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append('tests/')
    
    if verbose:
        cmd.append('-v')
    
    if coverage:
        cmd.extend(['--cov=src', '--cov-report=html', '--cov-report=term'])
    
    # Add other useful pytest options
    cmd.extend([
        '--tb=short',  # Shorter traceback format
        '--strict-markers',  # Strict marker checking
        '-ra',  # Show all test results
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=Path(__file__).parent.parent)


def run_unittest_tests(test_path=None, verbose=False):
    """Run tests using unittest (fallback)."""
    if test_path:
        # Run specific test file
        cmd = ['python3', '-m', 'unittest', test_path]
    else:
        # Discover and run all tests
        cmd = ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py']
    
    if verbose:
        cmd.append('-v')
    
    print(f"Running command: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=Path(__file__).parent.parent)


def check_test_dependencies():
    """Check if required test dependencies are installed."""
    required_packages = ['pytest', 'pytest-cov']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing test dependencies: {', '.join(missing_packages)}")
        print("Install them with: pip install " + ' '.join(missing_packages))
        return False
    
    return True


def run_specific_test_categories():
    """Run specific categories of tests."""
    categories = {
        'unit': 'tests/unit/',
        'integration': 'tests/integration/',
        'validation': 'tests/unit/test_validation.py',
        'models': ['tests/unit/test_product_model.py', 'tests/unit/test_invoice_model.py'],
        'managers': ['tests/unit/test_product_manager.py', 'tests/unit/test_invoice_manager.py'],
        'database': 'tests/unit/test_db_utils.py',
        'formatting': 'tests/unit/test_formatting.py'
    }
    
    print("Available test categories:")
    for category, path in categories.items():
        print(f"  {category}: {path}")
    
    return categories


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description='Run tests for the invoice management system')
    parser.add_argument('--category', '-c', help='Test category to run (unit, integration, etc.)')
    parser.add_argument('--file', '-f', help='Specific test file to run')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--coverage', action='store_true', help='Run with coverage report')
    parser.add_argument('--unittest', action='store_true', help='Use unittest instead of pytest')
    parser.add_argument('--list-categories', action='store_true', help='List available test categories')
    
    args = parser.parse_args()
    
    if args.list_categories:
        run_specific_test_categories()
        return 0
    
    # Determine test path
    test_path = None
    if args.file:
        test_path = args.file
    elif args.category:
        categories = run_specific_test_categories()
        if args.category in categories:
            test_path = categories[args.category]
            if isinstance(test_path, list):
                test_path = ' '.join(test_path)
        else:
            print(f"Unknown category: {args.category}")
            return 1
    
    # Choose test runner
    if args.unittest or not check_test_dependencies():
        print("Using unittest runner...")
        result = run_unittest_tests(test_path, args.verbose)
    else:
        print("Using pytest runner...")
        result = run_pytest_tests(test_path, args.verbose, args.coverage)
    
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
