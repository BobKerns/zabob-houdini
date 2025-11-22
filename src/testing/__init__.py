"""Testing module for zabob-houdini.

This module contains hython test functions that mirror pytest test structure.
It's not included in the distributed package - only available in the source tree.

Functions are automatically discovered and called by the dynamic module detection
in conftest.py based on the calling pytest module name.

For development, add src/ to PYTHONPATH:
    PYTHONPATH=src pytest tests/
"""

# Only import if we're in a Houdini environment
try:
    import hou
    _HOUDINI_AVAILABLE = True
except ImportError:
    _HOUDINI_AVAILABLE = False

__all__ = ["_HOUDINI_AVAILABLE"]
