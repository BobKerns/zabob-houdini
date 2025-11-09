"""
Zabob-Houdini: A simple API for creating Houdini node graphs.
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

# Core API will be available via __getattr__
__all__ = ["main", "call_houdini_function", "houdini_config"]
