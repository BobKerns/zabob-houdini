"""
Safe pytest fixtures for Houdini testing.

This version avoids importing anything that could trigger hou imports.
"""

import pytest
import json
import subprocess
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
        try:
            # Import the bridge function only when needed
            from zabob_houdini.houdini_bridge import call_houdini_function

            # Call the test function via hython
            result = call_houdini_function(test_func_name, *args, module="houdini_test_functions")

            # If result is a string, try to parse as JSON
            if isinstance(result, str):
                try:
                    parsed_result = json.loads(result)
                    if isinstance(parsed_result, dict):
                        result = parsed_result
                except json.JSONDecodeError:
                    # If not JSON, wrap in a result structure
                    result = {"raw_output": result}

            # Validate the result structure
            if isinstance(result, dict):
                if "success" in result:
                    if not result["success"]:
                        error_msg = result.get("error", "Unknown error")
                        traceback_info = result.get("traceback", "")
                        pytest.fail(f"Houdini test failed: {error_msg}\n{traceback_info}")
                    return result
                else:
                    # No success field, assume it's a valid result
                    return result
            else:
                # Non-dict result, assume success
                return result

        except ImportError as e:
            pytest.skip(f"Cannot import bridge functions: {e}")
        except RuntimeError as e:
            if "hython not found" in str(e):
                pytest.skip("Hython not available - skipping Houdini integration test")
            else:
                pytest.fail(f"Runtime error: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error running Houdini test: {e}")

    return run_houdini_test


@pytest.fixture
def houdini_available():
    """Check if we're running in hython environment."""
    executable = Path(sys.executable).name.lower()
    return 'hython' in executable or 'houdini' in executable
