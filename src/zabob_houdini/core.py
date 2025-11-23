"""
Core Zabob-Houdini API for creating Houdini node graphs.

This module assumes it's running in a Houdini environment (mediated by bridge or test fixture).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any, TypeVar, cast, TYPE_CHECKING
from itertools import zip_longest
from collections.abc import Sequence

if "hou" not in sys.modules:
    # Avoids SIGSEGV when importing hou in non-Houdini environments
    raise ImportError(
        "The 'hou' module is not available. This module requires Houdini's 'hou' module to run."
    )

import hou

# Bring together all the public API for __init__.py.

# Import Chain and chain() from core_chain (imported later to avoid circular dependency)
# Will be imported after Chain class is defined

# Import type aliases from core_types module
from zabob_houdini.core_types import (
    NodeParent,
    NodeType,
    CreatableNode,
    ChainableNode,
    LocalNodeName,
    ExistingNodeName,
    InputNodeSpec,
    InstanceNodeSpec,
    InputNode,
    InputNodes,
    ResolvedConnection,
    Inputs,
    ChainCopyParam,
)
from zabob_houdini.core_utils import hou_node
from zabob_houdini.core_node import (
    NodeBase, NodeInstance, node, ROOT,
    ForwardReference, _node_registry, wrap_node
)
from zabob_houdini.core_chain import Chain, ChainBuilder, chain
from zabob_houdini.core_context import NodeContext, context

if TYPE_CHECKING:
    T = TypeVar('T', bound=hou.Node)
else:
    T = TypeVar('T')



def merge(*inputs: 'NodeInstance | Chain | ForwardReference', **attributes: Any) -> NodeInstance:
    """
    Create a merge node with multiple inputs.

    Args:
        *inputs: NodeInstance or Chain objects to merge (must have same parent)
        **attributes: Additional merge node parameters

    Returns:
        NodeInstance for the merge node

    Raises:
        ValueError: If no inputs provided or inputs have different parents

    Examples:
        # Merge two geometry nodes
        box = node(geo, "box")
        sphere = node(geo, "sphere")
        merged = merge(box, sphere)

        # Merge chains
        chain_a = chain(node(geo, "box"), node(geo, "xform"))
        chain_b = chain(node(geo, "sphere"), node(geo, "xform"))
        merged = merge(chain_a, chain_b)

        # Merge with parameters
        merged = merge(box, sphere, tol=0.01)
    """
    if not inputs:
        raise ValueError("merge() requires at least one input")

    # Convert Chain or ChainBuilder objects to their last NodeInstance
    node_inputs = []
    for inp in inputs:
        if isinstance(inp, ForwardReference):
            node_inputs.append(inp)  # Pass ForwardReference through unchanged
        elif hasattr(inp, 'last'):  # Chain or ChainBuilder object
            last_item = inp.last
            node_inputs.append(last_item)  # Could be NodeInstance or ForwardReference
        else:  # NodeInstance
            node_inputs.append(inp)

    # Get parent from first resolvable input and verify all have same parent
    # (ForwardReferences will be validated at create time)
    first_parent = None
    for inp in node_inputs:
        if not isinstance(inp, ForwardReference):
            first_parent = inp.parent
            break

    if first_parent is None:
        # All inputs are ForwardReferences - we can't validate parent until create time
        # Use a placeholder (this will be resolved later)
        first_parent = ROOT

    for i, inp in enumerate(node_inputs):
        if isinstance(inp, ForwardReference):
            continue  # Skip validation for ForwardReferences
        if inp.parent != first_parent:
            raise ValueError(
                f"All merge inputs must have same parent. "
                f"Input 0 has parent {first_parent}, input {i} has parent {inp.parent}"
            )

    return node(
        first_parent,
        "merge",
        _input=node_inputs,
        **attributes
    )




# For the type checker's benefit. This must be in sync with the
# one in __init__.py.

__all__ = (
    "node", "chain", "merge", "context", "NodeInstance", "Chain", "NodeContext", "NodeType", "NodeParent",
    "NodeBase", "CreatableNode", "ChainableNode", "InputNode", "ChainBuilder",
    "InputNodes", "Inputs", "ChainCopyParam",
    "get_node_instance", "wrap_node", "hou_node", 'ROOT',
)
