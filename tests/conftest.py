"""
Safe pytest fixtures for Houdini testing.

This version avoids importing anything that could trigger hou imports.
"""

import pytest
from pathlib import Path
import sys


@pytest.fixture
def hython_test():
    """
    Fixture that provides a function to run test functions in hython.

    Skips tests if hython is not available.
    """
    def run_houdini_test(test_func_name: str, *args):
        """Run a test function in hython and validate the result."""
        # Import the bridge function only when needed
        from zabob_houdini.houdini_bridge import call_houdini_function, HoudiniResult

        # Call the test function via hython - returns HoudiniResult
        result: HoudiniResult = call_houdini_function(test_func_name, *args, module="houdini_test_functions")

        # Validate the result structure
        if not result['success']:
            error_msg = result.get("error", "Unknown error")
            traceback_info = result.get("traceback", "")
            pytest.fail(f"Houdini test failed: {error_msg}\n{traceback_info}")

        return result

    return run_houdini_test


@pytest.fixture
def houdini_available():
    """Check if we're running in hython environment."""
    executable = Path(sys.executable).name.lower()
    return 'hython' in executable or 'houdini' in executable
