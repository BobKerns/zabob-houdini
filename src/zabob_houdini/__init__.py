"""
Zabob-Houdini: A simple API for creating Houdini node graphs.

Architecture Layers:
--------------------

1. **Core API Layer** (core.py):
   - znode() and zchain() functions for creating node graphs
   - ZNode and ZChain classes for deferred execution
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
   - Uses dynamic import system for core API (node, chain, ZNode, ZChain)
   - Only loads hou-dependent code when in Houdini environment
   - Safe to import in regular Python environments
   - Not safe to load into pytest, however.

Usage Patterns:
---------------
- In Houdini (shelf tools, HDAs): `from zabob_houdini import node, chain`
- In regular Python (CLI, tests): Uses bridge layer automatically
- Bridge routing is transparent to user code
"""

from __future__ import annotations  # , _dynamic_import  # noqa: F407 # type: ignore

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("zabob-houdini")
except PackageNotFoundError:
    # Package is not installed, fallback for development
    __version__ = "0.0.0-dev"

if 'hou' in globals():
    # In Houdini environment, import core API directly
    from zabob_houdini.core import (
        znode, zchain, zmerge, zcontext,
        ZNode, ZChain, ZContext,
        ZNodeBase, ZChainBuilder,
        get_node_instance, wrap_node, hou_node, ROOT,
    )

__all__ = [
    '__version__',
    "znode", "zchain", "zmerge", "zcontext",
    "ZNode", "ZChain", "ZContext",
    "ZNodeBase", "ZChainBuilder",
    "get_node_instance", "wrap_node", "hou_node", "ROOT",
]
