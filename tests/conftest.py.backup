"""
Pytest fixtures for Houdini testing.
"""

import pytest
from zabob_houdini.houdini_bridge import call_houdini_function


def _is_in_houdini() -> bool:
    """Check if we're currently running in Houdini Python environment."""
    try:
        import hou
        return True
    except ImportError:
        return False


@pytest.fixture(scope="session")
def houdini_available():
    """Fixture that provides Houdini availability status."""
    return _is_in_houdini()


@pytest.fixture
def hython_test():
    """
    Fixture that provides a function to run test functions in hython.

    Returns a callable that takes a test function name and runs it in hython,
    returning the result.
    """
    def run_test(test_func_name: str, *args):
        return call_houdini_function(test_func_name, *args, module="houdini_test_functions")

    return run_test


@pytest.fixture
def skip_without_hython():
    """Fixture that skips tests if not running in hython and hython is not available."""
    if not _is_in_houdini():
        try:
            from zabob_houdini.houdini_bridge import _find_hython
            _find_hython()  # This will raise if hython not found
        except RuntimeError:
            pytest.skip("Hython not available - skipping Houdini integration test")


# Convenience fixture combining both
@pytest.fixture
def hython_required(skip_without_hython, hython_test):
    """Fixture that ensures hython is available and provides test runner."""
    return hython_test
