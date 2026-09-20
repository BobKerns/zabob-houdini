'''
Functions to create nodes on a one-off basis, not part of a network.

For more complex cases use:

  with zcontext('/obj', 'geo', 'My Geo Node') as geo:
      with ctx.chain() as ctx:
          ctx.node('file', 'Input file', file="weird-object.glb")
          ctx.node('xform', scale=3.0)
          ctx.node('output')
'''

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from collections.abc import Iterator
from typing import Any, overload

import hou

from zabob_houdini.core_types import (
    T_Cat,
    T_Parent,
    T_Node,
    T_Child,
)
from zabob_houdini.core_node import ZImmediateNode, _merge_inputs
from zabob_houdini.utils import HashableMapping
from zabob_houdini.core_chain import ZChain
from zabob_houdini.core_types import RawChainNode, RawParent
from zabob_houdini.core_node import (
    ZNodeBase, ZNode, wrap_node, _wrap_inputs, ZNodeForwardRef,
    ROOT,
)
from zabob_houdini.core_utils import _generate_name
from zabob_houdini.core_context import ZContext


@overload
def zcontext(parent: T_Parent) -> ZContext[hou.NodeTypeCategory,
                                           T_Parent,
                                           hou.Node,
                                           hou.Node]: ...


@overload
def zcontext(parent: T_Parent,
             ) -> ZContext[hou.NodeTypeCategory,
                           T_Parent,
                           hou.Node,
                           hou.Node]: ...


@overload
def zcontext(parent: ZNode[T_Cat, T_Parent, T_Node, T_Child],
             ) -> ZContext[T_Cat,
                           T_Parent,
                           T_Node,
                           T_Child]: ...


@overload
def zcontext(parent: 'RawParent') -> ZContext: ...


def zcontext(parent: 'RawParent') -> ZContext:
    """
    Create a ZContext for organizing nodes under a specific parent.

    Args:
        parent: Parent node (path string, ZNode, or hou.Node)

    Returns:
        ZContext that can be used as a context manager

    Example:
        with zcontext(geo) as ctx:
            # Create nodes under the geo parent
            box = ctx.node("box")
            sphere = ctx.node("sphere")
    """
    # Wrap the parent as a ZNode for consistent interface
    parent_instance = wrap_node(parent)
    return ZContext(parent=parent_instance.resolved)


def znode(
    parent: 'RawParent',
    node_type: 'Any',  # NodeType
    /,
    name: str | None = None,
    *,
    _input: 'Any | None' = None,  # InputNode | Sequence[InputNode]
    _inputs: 'Any | None' = None,  # InputNode | Sequence[InputNode]
    _node: 'hou.Node | None' = None,
    _display: bool = False,
    _render: bool = False,
    _context: 'ZContext | None' = None,
    **attributes: Any
) -> ZNode:
    """
    Create a node definition.

    Args:
        parent: Parent node (path string or ZNode)
        node_type: Type of node to create (e.g., "box", "xform")
        name: Optional name for the node
        _input: Optional input znode(s) to connect
        _node: Optional existing hou.Node to return from create()
        _display: Set display flag on this node when created
        _render: Set render flag on this node when created
        **attributes: Node parameter values

    Returns:
        ZNode that can be created with .create()
    """

    inputs = _wrap_inputs(_input, _context)
    inputs2 = _wrap_inputs(_inputs, _context)
    inputs = _merge_inputs(inputs, inputs2)

    if name is None:
        match parent:
            case '/':
                parent_path = ''
            case str():
                parent_path = parent
            case ZNode():
                parent_path = parent.path
            case hou.Node():
                parent_path = parent.path()
            case _:
                raise TypeError(f"Invalid parent type: {type(parent).__name__}")

        if parent_path.endswith('/'):
            parent_path = parent_path[:-1]
        name = _generate_name(parent_path, node_type)

    resolved_parent = wrap_node(parent).resolve()
    if resolved_parent is None:
        raise RuntimeError(f"Failed to resolve parent node: {parent}")

    return ZImmediateNode(
        _parent=resolved_parent,
        node_type=node_type,
        name=name,
        attributes=HashableMapping(attributes) if attributes else HashableMapping(),
        _inputs=tuple(inputs),
        _node=_node,
        _display=_display,
        _render=_render
    )


@overload
def zchain(node1: 'RawChainNode',
           **attributes: Any
           ) -> ZChain: ...


@overload
def zchain(node1: 'RawChainNode', *nodes: 'RawChainNode',
           **attributes: Any
           ) -> ZChain: ...


def zchain(
    *nodes: RawChainNode,
    **attributes: Any
) -> ZChain:
    """
    Create a chain of nodes definition.

    Args:
        *nodes: Sequence of ZNode objects, ZChain objects, or Houdini nodes to chain together

    Returns:
        ZChain that can be created with .create()

    Note:
        To connect inputs to the chain, pass them to the first node using the _input parameter:
        zchain(znode(parent, "xform", "first", _input=some_input), znode(parent, "xform", "second"))
    """
    if not nodes:
        raise ValueError("At least one node must be provided to create a chain.")

    # Check for the old _input parameter and provide a helpful error message
    if '_input' in attributes:
        raise TypeError(
            "The '_input' parameter is no longer supported on zchain(). "
            "Instead, pass the input to the first node: "
            "zchain(znode(parent, 'type', 'name', _input=your_input), ...)"
        )

    def _handle_entry(item: 'Any') -> Iterator[ZNodeBase]:
        match item:
            case ZNode():
                yield item
            case ZChain():
                yield from item.nodes

    flattened_nodes = tuple((
        node
        for item in nodes
        for node in _handle_entry(item)
    ))

    # Validate that all nodes have the same parent
    first_parent = flattened_nodes[0].parent
    for i, node in enumerate(flattened_nodes[1:], 1):
        if node.parent != first_parent:
            raise ValueError(
                f"All nodes in a context must have same parent. \n"
                f"Node 0 has parent {first_parent}, node {i} has parent {node.parent}"
            )

    copies = tuple(node.copy() for node in flattened_nodes)

    chain = ZChain(
        nodes=copies,  # Only ZNode objects now
        context=ZContext(first_parent),
    )
    for node in chain.nodes:
        node.resolved._connect_inputs()
    return chain


def zmerge(*inputs: ZNode | ZChain | ZNodeForwardRef, **attributes: Any) -> ZNode:
    """
    Create a merge node with multiple inputs.

    Args:
        *inputs: ZNode or ZChain objects to merge (must have same parent)
        **attributes: Additional merge node parameters

    Returns:
        ZNode for the merge node

    Raises:
        ValueError: If no inputs provided or inputs have different parents

    Examples:
        # Merge two geometry nodes
        box = znode(geo, "box")
        sphere = znode(geo, "sphere")
        merged = zmerge(box, sphere)

        # Merge chains
        chain_a = zchain(znode(geo, "box"), znode(geo, "xform"))
        chain_b = zchain(znode(geo, "sphere"), znode(geo, "xform"))
        merged = zmerge(chain_a, chain_b)

        # Merge with parameters
        merged = zmerge(box, sphere, tol=0.01)
    """
    if not inputs:
        raise ValueError("zmerge() requires at least one input")

    # Convert ZChain or ZChainBuilder objects to their last ZNode
    node_inputs = []
    for inp in inputs:
        if isinstance(inp, ZNodeForwardRef):
            node_inputs.append(inp)  # Pass ZNodeForwardRef through unchanged
        elif hasattr(inp, 'last'):  # ZChain or ZChainBuilder object
            last_item = inp.last
            node_inputs.append(last_item)  # Could be ZNode or ZNodeForwardRef
        else:  # ZNode
            node_inputs.append(inp)

    # Get parent from first resolvable input and verify all have same parent
    # (ForwardReferences will be validated at create time)
    first_parent = None
    for inp in node_inputs:
        if not isinstance(inp, ZNodeForwardRef):
            first_parent = inp.parent
            break

    if first_parent is None:
        # All inputs are ForwardReferences - we can't validate parent until create time
        # Use a placeholder (this will be resolved later)
        first_parent = ROOT

    for i, inp in enumerate(node_inputs):
        if isinstance(inp, ZNodeForwardRef):
            continue  # Skip validation for ForwardReferences
        if inp.parent != first_parent:
            raise ValueError(
                f"All merge inputs must have same parent. "
                f"Input 0 has parent {first_parent}, input {i} has parent {inp.parent}"
            )

    return znode(
        first_parent,
        "merge",
        _input=node_inputs,
        **attributes
    )
