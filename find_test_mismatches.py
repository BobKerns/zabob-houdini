#!/usr/bin/env python3
"""
Find mismatches between pytest function names and hython function names.
"""

import re
import os
from pathlib import Path
from typing import Dict, Set, List, Tuple

def extract_pytest_functions(file_path: str) -> List[Tuple[str, int]]:
    """Extract pytest function names and line numbers from a test file."""
    functions = []
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            # Match both class methods and standalone functions
            match = re.match(r'\s*def (test_\w+)\s*\(', line)
            if match:
                functions.append((match.group(1), line_num))
    return functions

def extract_hython_calls(file_path: str) -> List[Tuple[str, str, int]]:
    """Extract hython_test calls with pytest function context and line numbers."""
    calls = []
    current_test = None

    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            # Check for test function definition
            test_match = re.match(r'\s*def (test_\w+)\s*\(', line)
            if test_match:
                current_test = test_match.group(1)

            # Check for hython_test calls
            hython_match = re.search(r'hython_test\s*\(\s*["\']([^"\']+)["\']', line)
            if hython_match and current_test:
                hython_func = hython_match.group(1)
                calls.append((current_test, hython_func, line_num))

    return calls

def extract_houdini_functions(file_path: str) -> Set[str]:
    """Extract all function names from houdini_test_functions.py."""
    functions = set()
    with open(file_path, 'r') as f:
        for line in f:
            # Match function definitions, excluding private functions and __exit__
            match = re.match(r'^def ([a-zA-Z_]\w*)\s*\(', line)
            if match and not match.group(1).startswith('_'):
                functions.add(match.group(1))
    return functions

def find_mismatches():
    """Find all mismatches between pytest and hython function names."""
    tests_dir = Path("tests")
    houdini_test_file = Path("src/zabob_houdini/houdini_test_functions.py")

    # Get all houdini test functions
    houdini_functions = extract_houdini_functions(houdini_test_file)
    print(f"Found {len(houdini_functions)} houdini test functions")

    # Track all pytest functions and their hython calls
    all_pytest_functions = set()
    all_hython_calls = []
    mismatches = []

    # Process all test files
    test_files = list(tests_dir.glob("test_*.py"))
    print(f"Processing {len(test_files)} test files...")

    for test_file in test_files:
        pytest_functions = extract_pytest_functions(str(test_file))
        hython_calls = extract_hython_calls(str(test_file))

        # Add to global tracking
        all_pytest_functions.update(func for func, _ in pytest_functions)
        all_hython_calls.extend(hython_calls)

        # Check for mismatches in this file
        for pytest_func, hython_func, line_num in hython_calls:
            expected_hython = "_" + pytest_func
            if hython_func != expected_hython:
                mismatches.append({
                    'file': str(test_file),
                    'line': line_num,
                    'pytest_func': pytest_func,
                    'hython_func': hython_func,
                    'expected': expected_hython
                })

    # Print mismatches
    print(f"\n=== MISMATCHES FOUND ({len(mismatches)}) ===")
    for mismatch in mismatches:
        print(f"{mismatch['file']}:{mismatch['line']}")
        print(f"  pytest: {mismatch['pytest_func']}")
        print(f"  hython: {mismatch['hython_func']}")
        print(f"  expected: {mismatch['expected']}")
        print()

    # Find houdini functions without corresponding pytest tests
    hython_functions_called = set(call[1] for call in all_hython_calls)
    unused_houdini_functions = houdini_functions - hython_functions_called

    print(f"=== UNUSED HOUDINI FUNCTIONS ({len(unused_houdini_functions)}) ===")
    for func in sorted(unused_houdini_functions):
        print(f"  {func}")

    # Find pytest functions that don't call hython_test
    pytest_with_hython = set(call[0] for call in all_hython_calls)
    pytest_without_hython = all_pytest_functions - pytest_with_hython

    print(f"\n=== PYTEST FUNCTIONS WITHOUT HYTHON CALLS ({len(pytest_without_hython)}) ===")
    for func in sorted(pytest_without_hython):
        print(f"  {func}")

    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Total pytest functions: {len(all_pytest_functions)}")
    print(f"Total hython_test calls: {len(all_hython_calls)}")
    print(f"Total houdini functions: {len(houdini_functions)}")
    print(f"Mismatches: {len(mismatches)}")
    print(f"Unused houdini functions: {len(unused_houdini_functions)}")
    print(f"Pytest functions without hython calls: {len(pytest_without_hython)}")

if __name__ == "__main__":
    find_mismatches()
