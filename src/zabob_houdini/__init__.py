"""
Zabob-Houdini: A simple API for creating Houdini node graphs.
"""

from importlib.metadata import version, PackageNotFoundError

from zabob_houdini.cli import main
from zabob_houdini.core import node, chain, NodeInstance, Chain
from zabob_houdini.houdini_bridge import call_houdini_function
import zabob_houdini.houdini_config as houdini_config

try:
    __version__ = version("zabob-houdini")
except PackageNotFoundError:
    # Package is not installed, fallback for development
    __version__ = "0.0.0-dev"

__all__ = ["main", "node", "chain", "NodeInstance", "Chain", "call_houdini_function", "houdini_config"]
