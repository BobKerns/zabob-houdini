"""
Type aliases for Zabob-Houdini core API.

This module defines the type aliases used throughout the codebase for clarity
and maintainability. These types document the various ways nodes, inputs, and
connections can be specified in the API.
"""

from __future__ import annotations
from typing import TypeAlias, TYPE_CHECKING
from collections.abc import Sequence

import hou

if TYPE_CHECKING:
    from zabob_houdini.core_node import NodeInstance, ForwardReference
    from zabob_houdini.core_chain import Chain

# Type aliases for clarity
NodeParent: TypeAlias = "str | NodeInstance | hou.Node"
"""A parent node, either as a path string (e.g., "/obj"), NodeInstance, or hou.Node object."""

NodeType: TypeAlias = str
"""A Houdini node type name (e.g., "geo", "box", "xform"). Will expand to NodeTypeInstance later."""

CreatableNode: TypeAlias = 'NodeInstance | Chain'
"""A node or chain that can be created via .create() method."""

ChainableNode: TypeAlias = 'NodeInstance | Chain'
"""A node or chain that can be used in a chain - includes existing hou.Node objects."""

LocalNodeName: TypeAlias = str
"""String name of a node within a context, used for forward references."""

ExistingNodeName: TypeAlias = 'str'
"""String path to an existing node in the Houdini scene, to connect to existing nodes."""

InputNodeSpec: TypeAlias = 'NodeInstance | Chain | ExistingNodeName | LocalNodeName | ForwardReference | hou.Node'
"""Values that can be used as input nodes - either NodeInstance, Chain, hou.Node, string path, or ForwardReference."""

InstanceNodeSpec: TypeAlias = 'tuple[InputNodeSpec, int] | InputNodeSpec'
"""A connection specification: either (<node>, <output_index>) tuple or just <node> (defaults to output 0)."""

InputNode: TypeAlias = 'InstanceNodeSpec | None'
"""A node that can be used as input - InputConnection or None for sparse connections."""

InputNodes: TypeAlias = 'Sequence[InputNode]'

ResolvedConnection: TypeAlias = 'tuple[NodeInstance | ForwardReference, int]'
"""A resolved connection: (node, output_index)."""

Inputs: TypeAlias = 'tuple[ResolvedConnection | None, ...]'
"""The inputs for a node or chain, as a tuple of ResolvedConnection objects or None for sparse connections."""

ChainCopyParam: TypeAlias = 'int | str | NodeInstance'
"""A parameter for Chain.copy() reordering: index, name, or NodeInstance to insert."""
