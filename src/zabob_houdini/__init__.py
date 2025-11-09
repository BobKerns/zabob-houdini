"""
Zabob-Houdini: A simple API for creating Houdini node graphs.

Architecture Layers:
--------------------

1. **Core API Layer** (core.py):
   - node() and chain() functions for creating node graphs
   - NodeInstance and Chain classes for deferred execution
   - Only imported in Houdini context (requires hou module)

2. **Bridge Layer** (houdini_bridge.py):
   - Safe interface between regular Python and Houdini environments
   - Routes function calls to hython subprocess when not in Houdini
   - Returns TypedDict results for type safety

3. **CLI Layer** (cli.py):
   - Development utilities and testing commands
   - Never directly imports hou module (prevents segfaults)
   - Delegates all Houdini functionality to bridge layer

4. **Module Interface** (__init__.py):
   - Provides lazy imports for core API (node, chain, NodeInstance, Chain)
   - Only loads hou-dependent code when actually needed
   - Safe to import in regular Python environments

Usage Patterns:
---------------
- In Houdini (shelf tools, HDAs): `from zabob_houdini import node, chain`
- In regular Python (CLI, tests): Uses bridge layer automatically
- Bridge routing is transparent to user code
"""

from importlib.metadata import version, PackageNotFoundError

from zabob_houdini.cli import main
from zabob_houdini.houdini_bridge import call_houdini_function
import zabob_houdini.houdini_config as houdini_config

try:
    __version__ = version("zabob-houdini")
except PackageNotFoundError:
    # Package is not installed, fallback for development
    __version__ = "0.0.0-dev"

# Lazy imports to avoid importing hou when not needed
def __getattr__(name: str):
    """Lazy import core API components only when accessed."""
    if name in ("node", "chain", "NodeInstance", "Chain"):
        from zabob_houdini.core import node, chain, NodeInstance, Chain
        globals().update({
            "node": node,
            "chain": chain,
            "NodeInstance": NodeInstance,
            "Chain": Chain
        })
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Export public API
# Core components (node, chain, NodeInstance, Chain) are available via lazy loading through __getattr__
__all__ = ["main", "call_houdini_function", "houdini_config"]
