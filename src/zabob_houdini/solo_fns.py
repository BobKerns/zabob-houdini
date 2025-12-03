'''
Functions to create nodes on a one-off basis, not part of a network.

For more complex cases use:

  with context('/obj', 'geo', 'My Geo Node') as geo:
      with ctx.chain() as ctx:
          ctx.node('file', 'Input file', file="weird-object.glb")
          ctx.node('xform', scale=3.0)
          ctx.node('output')
'''

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, overload, TYPE_CHECKING

from zabob_houdini.core_node import ImmediateNode, _merge_inputs
from zabob_houdini.utils import HashableMapping

if TYPE_CHECKING:
    # This file should not have load-time dependencies on the
    # core modules.
    from zabob_houdini.core_chain import Chain
    from zabob_houdini.core_types import RawChainNode, RawParent
    from zabob_houdini.core_node import (
        NodeBase, NodeInstance, wrap_node, _wrap_inputs,
    )
    from zabob_houdini.core_utils import _generate_name
    from zabob_houdini.core_context import NodeContext
else:
    from zabob_houdini.core_chain import Chain
    from zabob_houdini.core_node import (
        _wrap_inputs, wrap_node, NodeInstance
    )
    from zabob_houdini.core_utils import _generate_name
    from zabob_houdini.core_context import NodeContext
import hou


def context(parent: 'RawParent') -> 'NodeContext':
    """
    Create a NodeContext for organizing nodes under a specific parent.

    Args:
        parent: Parent node (path string, NodeInstance, or hou.Node)

    Returns:
        NodeContext that can be used as a context manager

    Example:
        with context(geo) as ctx:
            # Create nodes under the geo parent
            box = node(ctx.parent, "box")
            sphere = node(ctx.parent, "sphere")
    """
    # Wrap the parent as a NodeInstance for consistent interface
    parent_instance = wrap_node(parent)
    return NodeContext(parent=parent_instance.resolved)


def node(
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
    _context: 'NodeContext | None' = None,
    **attributes: Any
) -> NodeInstance:
    """
    Create a node definition.

    Args:
        parent: Parent node (path string or NodeInstance)
        node_type: Type of node to create (e.g., "box", "xform")
        name: Optional name for the node
        _input: Optional input node(s) to connect
        _node: Optional existing hou.Node to return from create()
        _display: Set display flag on this node when created
        _render: Set render flag on this node when created
        **attributes: Node parameter values

    Returns:
        NodeInstance that can be created with .create()
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
            case NodeInstance():
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

    return ImmediateNode(
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
def chain(node1: 'RawChainNode',
          **attributes: Any
          ) -> Chain: ...


@overload
def chain(node1: 'RawChainNode', *nodes: 'RawChainNode',
          **attributes: Any
          ) -> Chain: ...


def chain(
    *nodes: RawChainNode,
    **attributes: Any
) -> Chain:
    """
    Create a chain of nodes definition.

    Args:
        *nodes: Sequence of NodeInstance objects, Chain objects, or Houdini nodes to chain together

    Returns:
        Chain that can be created with .create()

    Note:
        To connect inputs to the chain, pass them to the first node using the _input parameter:
        chain(node(parent, "xform", "first", _input=some_input), node(parent, "xform", "second"))
    """
    if not nodes:
        raise ValueError("At least one node must be provided to create a chain.")

    # Check for the old _input parameter and provide a helpful error message
    if '_input' in attributes:
        raise TypeError(
            "The '_input' parameter is no longer supported on chain(). "
            "Instead, pass the input to the first node: "
            "chain(node(parent, 'type', 'name', _input=your_input), ...)"
        )

    def _handle_entry(item: 'Any') -> Iterator[NodeBase]:
        match item:
            case NodeInstance():
                yield item
            case Chain():
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

    chain = Chain(
        nodes=copies,  # Only NodeInstance objects now
        context=NodeContext(first_parent),
    )
    for node in chain.nodes:
        node.resolved._connect_inputs()
    return chain
