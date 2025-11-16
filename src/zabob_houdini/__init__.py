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

lazy_imports = (
    "node", "chain", "NodeInstance", "Chain", "NodeType", "NodeParent",
    "NodeBase", "CreatableNode", "ChainableNode", "InputNode",
    "InputNodes", "Inputs", "ChainCopyParam",
    "get_node_instance", "wrap_node", "hou_node", "wrap_node", 'ROOT',
)
_imports_loaded = False

try:
    __version__ = version("zabob-houdini")
except PackageNotFoundError:
    # Package is not installed, fallback for development
    __version__ = "0.0.0-dev"

# Lazy imports to avoid importing hou when not needed
def __getattr__(name: str):
    """Lazy import core API components only when accessed."""
    import sys
    global _imports_loaded

    if name in lazy_imports:
        if "hou" not in sys.modules:
            raise ImportError(
                f"Cannot import '{name}' in regular Python environment. "
                f"Core API components (node, chain, NodeInstance, etc.) require Houdini's 'hou' module. "
                f"Use 'hython' instead of 'python', or run integration tests with the hython_test fixture."
            )
        if not _imports_loaded:
            import zabob_houdini.core as core
            globals().update({
                attr: getattr(core, attr) for attr in lazy_imports
            })
            _imports_loaded = True
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Note: Core API components (node, chain, NodeInstance, Chain, NodeType, NodeParent, etc) are available
# via lazy loading through __getattr__ but the linter can't check for us, so be careful to keep
# __all__ accurate.
# Although these appear to be undefined to static analysis, they are actually defined at runtime.
__all__ = ['__version__',
    "node", "chain", "NodeInstance", "Chain", "NodeType", "NodeParent", # type: ignore
    "NodeBase", "CreatableNode", "ChainableNode", "InputNode", # type: ignore
    "InputNodes", "Inputs", "ChainCopyParam", # type: ignore
    "get_node_instance", "wrap_node", "hou_node", "wrap_node", "ROOT", # type: ignore
    ]

# Validate __all__ consistency at import time
_expected_all = set(lazy_imports) | {'__version__'}
_actual_all = set(__all__)
if _expected_all != _actual_all:
    _missing = _expected_all - _actual_all
    _extra = _actual_all - _expected_all - {'__version__'}
    raise ImportError(
        f"__all__ inconsistency: "
        f"missing={list(_missing)}, unexpected_extra={list(_extra)}"
    )
