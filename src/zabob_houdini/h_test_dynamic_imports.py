"""
Test module for verifying dynamic imports work correctly.

This module exists solely to test the dynamic import mechanism.
"""
from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from zabob_houdini.core_node import NodeInstance  # noqa: F401
from zabob_houdini.core_chain import Chain  # noqa: F401


def test_dynamic_imports_enabled() -> bool:
    """
    Verify that dynamic imports are working.

    Returns:
        True if dynamic imports are enabled and working
    """
    # If we can import this module at all, dynamic imports are working
    # because the __future__ import would cause a SyntaxError otherwise
    return True


# Module-level test
DYNAMIC_IMPORTS_WORK = test_dynamic_imports_enabled()
