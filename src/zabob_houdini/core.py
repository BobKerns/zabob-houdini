"""
Core Zabob-Houdini API for creating Houdini node graphs.

This module assumes it's running in a Houdini environment (mediated by bridge or test fixture).
"""

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

import sys
from typing import TypeVar

if "hou" not in sys.modules:
    # Avoids SIGSEGV when importing hou in non-Houdini environments
    raise ImportError(
        "The 'hou' module is not available. This module requires Houdini's 'hou' module to run."
    )

import hou

# Bring together all the public API for __init__.py.

# Import ZChain and zchain() from core_chain (imported later to avoid circular dependency)
# Will be imported after ZChain class is defined

# Import type aliases from core_types module
from zabob_houdini.core_types import (
    UnresolvedConnection, UnresolvedConnections, ResolvedConnection, NativeNodeType,
    RawParent, ResolvedParent,
)
from zabob_houdini.core_utils import hou_node
from zabob_houdini.core_node import (
    ZNodeBase, ZNode, ROOT,
    ZNodeForwardRef, wrap_node, get_node_instance
)
from zabob_houdini.core_chain import ZChain, ZChainBuilder
from zabob_houdini.core_context import ZContext
from zabob_houdini.solo_fns import (
    znode, zchain, zcontext, zmerge,
)

T = TypeVar('T', bound=hou.Node)


# For the type checker's benefit. This must be in sync with the
# one in __init__.py.

__all__ = (
    "znode", "zchain", "zmerge", "zcontext", "ZNode", "ZChain", "ZContext",
    "NativeNodeType", "RawParent", "ResolvedParent",
    "ZNodeBase", "ZChainBuilder", "ZNodeForwardRef",
    "get_node_instance", "wrap_node", "hou_node", 'ROOT',
    "ResolvedConnection", "UnresolvedConnection", "UnresolvedConnections",
)
