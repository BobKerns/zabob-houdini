"""Unit tests for dynamic import system."""

import sys


def test_import_hook_installed():
    """Verify the dynamic import hook is installed in sys.meta_path."""
    for finder in sys.meta_path:
        if 'DynamicImportFinder' in type(finder).__name__:
            return  # Test passes

    raise AssertionError("Dynamic import hook is NOT installed")


def test_dynamic_imports_work():
    """Test that dynamic imports actually work by importing the test module."""
    from zabob_houdini import h_test_dynamic_imports

    assert h_test_dynamic_imports.DYNAMIC_IMPORTS_WORK, \
        "Dynamic import test module did not load correctly"
