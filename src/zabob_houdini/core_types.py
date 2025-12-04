"""
Type aliases for Zabob-Houdini core API.

This module defines the type aliases used throughout the codebase for clarity
and maintainability. These types document the various ways nodes, inputs, and
connections can be specified in the API.
"""

from __future__ import annotations, _dynamic_import  # type: ignore # noqa: F401,F403,F407
from typing import Literal, TypeAlias, TypeVar
from collections.abc import Sequence

import hou

from zabob_houdini.core_node import NodeBase, NodeInstance
from zabob_houdini.core_chain import Chain

T_Cat = TypeVar('T_Cat', bound=hou.NodeTypeCategory)
T_Node = TypeVar('T_Node', bound=hou.Node)
T_Ctx = TypeVar('T_Ctx', bound=hou.Node)
T_Parent = TypeVar('T_Parent', bound=hou.Node)
T_Child = TypeVar('T_Child', bound=hou.Node)
T_Instance = TypeVar('T_Instance', bound=NodeInstance)

LocalNodeName: TypeAlias = str
"""String name of a node within a context, used for forward references."""

ExistingNodeName: TypeAlias = str
"""String path to an existing node in the Houdini scene, to connect to existing nodes."""

# Type aliases for clarity in function signatures and documentation
#
# Raw* types represent the various ways users can specify nodes and
# connections in the API, before they are resolved to an internal
# form such as actual NodeInstance or hou.Node objects.
#
# Unresolved* types represent forms that may contain
# ForwardReferences that need to be resolved before
# creating the actual nodes and connections.
#
# Resolved* types represent the final form of nodes and connections
# after all references have been resolved, ready for creation in Houdini.
#
# Native* types represent the actual hou.Node objects that have been
# created in Houdini, or other structures in Houdini native form.

RawParent: TypeAlias = 'ExistingNodeName | NodeBase | T_Node'
"""
Raw input: A parent node, either as a path string (e.g., "/obj"),
NodeInstance, ForwardReference, or hou.Node object."""

NativeNodeType: TypeAlias = str
"""
A Houdini node type name (e.g., "geo", "box", "xform").
TODO: expand to include NodeTypeInstance later.
"""

NativeParmData: TypeAlias = (
    None | int | float | str | bool
    | tuple['NativeParmData', ...]
    | dict[str, 'NativeParmData']
    | hou.Vector2 | hou.Vector3 | hou.Vector4
    | hou.Color
    | hou.Matrix4
)

RawCreatableNode: TypeAlias = 'NodeInstance | Chain'
"""
A node or chain that can be created via .create() method.
"""

_NodeSpec: TypeAlias = 'NodeBase | Chain | ExistingNodeName | LocalNodeName | T_Node'
"""A specification for a node, which can be a NodeBase, Chain, existing node name, local node name, or hou.Node."""

RawChainNode: TypeAlias = '_NodeSpec[T_Node]'
"""
A node or chain that can be used in a chain, or a name to resolve.
"""

_NoConnection: TypeAlias = tuple[None, Literal[0]]

_RawConnection: TypeAlias = tuple['_NodeSpec[T_Node]', int]

RawConnection: TypeAlias = '_NodeSpec[T_Node] | _RawConnection[T_Node] | _NoConnection | None'
"""
A specification for a connection, to the a specified output of a specified node.

The connection can be specified as:
- A node or chain (NodeBase, Chain, hou.Node, or name) to connect to the first output (index 0).
- A tuple of (node_spec, index), where:
  - node_spec specifies a node
  - index is the index of the output to connect to [default 0].
- A tuple of (None, 0) to represent no connection (i.e, a sparse connection).
- None to represent no connection (i.e., a sparse connection), only in Raw form.
"""

RawInput: TypeAlias = 'RawConnection[T_Node] | Sequence[RawConnection[T_Node]] | NodeInstance | ExistingNodeName | None'
"""One or more specifications for a connection, to the output of a specified node."""

RawInputs: TypeAlias = 'Sequence[RawConnection[T_Node]] | RawInput[T_Node] | None'
"""A sequence of specifications for connections, to the outputs of specified nodes."""

RawChainCopyNode: TypeAlias = 'int | str | NodeBase'
"""A parameter for Chain.copy() reordering: index, name, or NodeInstance to insert."""

RawParentNode: TypeAlias = 'ExistingNodeName | NodeBase | T_Node'
"""A parent node specification for creating a new node or chain."""

_UnresolvedConnection: TypeAlias = tuple['NodeBase', int]

UnresolvedConnection: TypeAlias = _UnresolvedConnection | _NoConnection
"""A connection that may contain unresolved ForwardReferences: (node, output_index)."""

UnresolvedConnections: TypeAlias = tuple[UnresolvedConnection, ...]
"""A tuple of unresolved connections for a node's inputs."""

UnresolvedNode: TypeAlias = 'NodeBase'
"""A node that may be unresolved."""

UnresolvedNodes: TypeAlias = 'tuple[UnresolvedNode, ...]'
"""A tuple of unresolved nodes."""

_Connection: TypeAlias = 'tuple[NodeInstance, int]'
"""A resolved connection: (node, output_index)."""

ResolvedConnection: TypeAlias = '_Connection | _NoConnection'
"""A resolved connection: (node, output_index).

Note: ResolvedConnection is a subset of UnresolvedConnection, with all forward
references resolved to concrete NodeInstance objects."""

ResolvedConnections: TypeAlias = tuple[ResolvedConnection, ...]
"""The inputs for a node or chain, as a tuple of ResolvedConnection objects or None for sparse connections."""

ResolvedNode: TypeAlias = 'NodeInstance'
"""A node that has been resolved to a NodeInstance."""

ResolvedNodes: TypeAlias = 'tuple[ResolvedNode, ...]'
"""A tuple of resolved nodes."""

ResolvedParent: TypeAlias = 'NodeInstance'
"""A parent node that has been resolved to a NodeInstance."""
