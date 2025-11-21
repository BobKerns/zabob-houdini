"""Optional testing subpackage for zabob-houdini.

This subpackage contains hython test functions that mirror pytest test structure.
It's excluded from normal package distribution and only included when the
'testing' extra is installed.

To install with testing support:
    pip install zabob-houdini[testing]

Or for development:
    uv sync --extra testing
"""

# Only import if we're in a Houdini environment
try:
    import hou
    _HOUDINI_AVAILABLE = True
except ImportError:
    _HOUDINI_AVAILABLE = False

# Import registry for function lookup
from .registry import registry

def get_test_function(function_name: str):
    """Get a test function by name from the split modules."""
    return registry.get_function(function_name)

def list_test_functions() -> list[str]:
    """List all available test functions."""
    return registry.list_functions()

__all__ = ["_HOUDINI_AVAILABLE", "get_test_function", "list_test_functions", "registry"]
