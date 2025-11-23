"""
Chain and ChainBuilder classes for Zabob-Houdini.

This module contains the Chain class for representing sequences of connected nodes,
and the ChainBuilder class for building chains within a context manager interface.
"""

from __future__ import annotations

import functools
from typing import Any, overload, TYPE_CHECKING
from collections.abc import Iterator, Sequence

import hou

from zabob_houdini.core_types import (
    NodeType,
    InputNode,
    Inputs,
    ChainableNode,
    ChainCopyParam,
    InputNodes,
)

# Import actual dependencies
from zabob_houdini.utils import HashableMapping
import zabob_houdini.core_node as cnode
if TYPE_CHECKING:
    from zabob_houdini.core_node import (
        NodeInstance,
        ForwardReference, DeferredChainPropertyReference,
    )
    from zabob_houdini.core_context import NodeContext

class Chain(cnode.NodeBase):
    """
    Represents a chain of Houdini nodes that can be created.

    Nodes in the chain are automatically connected in sequence.
    """
    nodes: tuple[NodeInstance, ...]

    def __init__(self, nodes: Sequence[NodeInstance]):
        '''
        We use an __init__ method rather than the dataclass-generated one,
        so we can store a private copy. This ensures we never hold a shared
        node.
        '''
        copied_nodes = []
        for i, node in enumerate(nodes):
            if i == 0:
                # First node keeps its original inputs
                copied_nodes.append(node._copy(_chain=self))
            else:
                # Subsequent nodes connect to the previous node
                prev_node = copied_nodes[i-1]
                copied_nodes.append(node._copy(_chain=self, _inputs=(prev_node,)))

        object.__setattr__(self, 'nodes', tuple(copied_nodes))

    @functools.cached_property
    def parent(self) -> NodeInstance:
        match self.nodes:
            case ():
                return cnode.ROOT
            case cnode.NodeInstance() as n, *_:
                return n.parent
            case _:
                raise RuntimeError(f"Invalid parent: {self.nodes[0]}")

    @functools.cached_property
    def first(self) -> NodeInstance:
        """Return the first node in this chain."""
        if not self.nodes:
            raise RuntimeError("Chain is empty.")
        return self.nodes[0]

    @functools.cached_property
    def last(self) -> NodeInstance:
        """Return the last node in this chain."""
        if not self.nodes:
            raise RuntimeError("Chain is empty.")
        return self.nodes[-1]

    @functools.cached_property
    def inputs(self) -> 'Inputs':
        """Return the input nodes for this chain, which are the inputs of the first node."""
        if not self.nodes:
            return tuple()
        return self.first.inputs

    @overload
    def __getitem__(self, key: int) -> NodeInstance: ...

    @overload
    def __getitem__(self, key: slice) -> 'Chain': ...

    @overload
    def __getitem__(self, key: str) -> NodeInstance: ...

    def __getitem__(self, key: int | slice | str) -> 'ChainableNode':
        """
        Access nodes in the chain by index, slice, or name.

        Args:
            key: Integer index, slice, or node name string

        Returns:
            NodeInstance for int/str keys, Chain for slice keys
        """
        nodes = self.nodes

        match key:
            case int() as index:
                return nodes[index]
            case slice() as slice_obj:
                # Return a new Chain with the subset of nodes
                subset = nodes[slice_obj]
                return Chain(
                    nodes=subset,
                )
            case str() as name:
                # Find node by name
                for node_instance in nodes:
                    if node_instance.name == name:
                        return node_instance
                raise KeyError(f"No node found with name '{name}'")
            case _:
                raise TypeError(f"Chain indices must be integers, slices, or strings, not {type(key).__name__}")

    def __len__(self) -> int:
        """Return the number of nodes in the chain."""
        return len(self.nodes)

    def __iter__(self) -> "Iterator[NodeInstance]":
        """Return an iterator over the flattened nodes in the chain."""
        return iter(self.nodes)

    def first_node(self) -> 'hou.Node':
        """
        Get the created hou.Node for the first node in the chain.

        Creates the chain if not already created.

        Returns:
            The first hou.Node in the created chain.

        Raises:
            ValueError: If the chain is empty.
        """
        created_instances = self.create()
        if not created_instances:
            raise ValueError("Cannot get first node of empty chain")

        first_instance = created_instances[0]
        return first_instance.create()

    def last_node(self) -> 'hou.Node':
        """
        Get the created hou.Node for the last node in the chain.

        Creates the chain if not already created.

        Returns:
            The last hou.Node in the created chain.

        Raises:
            ValueError: If the chain is empty.
        """
        created_instances = self.create()
        if not created_instances:
            raise ValueError("Cannot get last node of empty chain")

        last_instance = created_instances[-1]
        return last_instance.create()

    def nodes_iter(self) -> "Iterator[hou.Node]":
        """
        Return an iterator over the created hou.Node instances in the chain.

        Creates the chain if not already created.

        Yields:
            hou.Node objects for each node in the chain.
        """
        created_instances = self.create()
        for instance in created_instances:
            yield instance.create()

    def hou_nodes(self) -> tuple['hou.Node', ...]:
        """
        Get all created hou.Node instances in the chain as a tuple.

        Creates the chain if not already created.

        Returns:
            Tuple of hou.Node objects for all nodes in the chain.
        """
        return tuple(self.nodes_iter())

    @functools.cache
    def create(self) -> tuple[NodeInstance, ...]:
        """
        Create the actual chain of Houdini nodes.

        Chain connections are now handled through each node's _inputs,
        so we just need to create each node.

        Returns:
            Tuple of NodeInstance objects for created nodes. Same instances
            returned on subsequent calls (cached via @functools.cache).
        """
        nodes = self.nodes
        if not nodes:
            return tuple()

        # Create each node - connections are handled automatically via _inputs
        # Use _skip_chain=True to avoid recursion since we're already creating the chain
        created_node_instances = []
        for node_instance in nodes:
            # Create the node in Houdini (NodeInstance.create handles connections via _inputs)
            node_instance._create(_skip_chain=True)
            created_node_instances.append(node_instance)

        return tuple(created_node_instances)

    def copy(self, *copy_params: 'ChainCopyParam', _inputs: 'InputNodes'=()) -> 'Chain':  # type: ignore[override]
        """
        Return a copy of this Chain with nodes reordered, dropped, or inserted.

        Args:
            *copy_params: Parameters specifying nodes to copy:
                - int: Index of existing node to copy (can reorder/duplicate)
                - str: Name of existing node to copy
                - NodeInstance: New node to insert at this position
                If no arguments given, copies all nodes in original order
            _inputs: Input nodes for the first node in the new chain

        Returns:
            New Chain with specified nodes in specified order

        Examples:
            chain.copy(3, 2, 1, 0)      # Reverse 4-element chain
            chain.copy(0, 2)            # Copy only nodes 0 and 2
            chain.copy("box", "sphere") # Copy by name
            chain.copy(0, new_node, 1)  # Insert new_node between positions 0 and 1
        """
        # Build new node list using self[param] for uniform access
        new_nodes: Sequence[NodeInstance] = (
            self.nodes if not copy_params
            else [
                param if isinstance(param, cnode.NodeInstance) else self[param]
                for param in copy_params
                ]
        )

        if not new_nodes:
            raise ValueError("Chain copy must result in at least one node")

        # Handle inputs for first node
        inputs = cnode._wrap_inputs(_inputs)
        self_inputs: 'Inputs' = ()
        if self.nodes and new_nodes:
            if copy_params:
                # Get inputs from the original first node being copied
                first_param = copy_params[0]
                if not isinstance(first_param, cnode.NodeInstance):
                    # It's an int or str - get the original node's inputs
                    original_first = self[first_param]
                    self_inputs = original_first.inputs
            else:
                # Default copy: preserve first node's inputs
                self_inputs = self.nodes[0].inputs

        merged_inputs = cnode._merge_inputs(inputs, self_inputs)

        # Copy first node with merged inputs
        first_node = new_nodes[0].copy(_inputs=merged_inputs)

        # Copy remaining nodes
        remaining_nodes = [n.copy() for n in new_nodes[1:]]

        # Create new chain - __init__ will copy and set _chain references
        new_chain = Chain(
            nodes=(first_node, *remaining_nodes),
        )
        return new_chain


class ChainBuilder:
    """Context manager for building chains without registering intermediate nodes."""

    def __init__(self, context: 'NodeContext', _input: 'InputNode | Sequence[InputNode] | None' = None):
        self.context = context
        self._input = _input
        self._nodes: list[NodeInstance] = []

    def __enter__(self) -> 'ChainBuilder':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            # Exception occurred: discard any partially built chain, clean up temporary state
            self._created_chain = None
            self._nodes.clear()
            return
        if exc_type is None and self._nodes:
            # First, create the chain without inputs to mark it as complete
            self._created_chain = Chain(self._nodes)

            # Now process inputs - DeferredChainPropertyReferences can now resolve
            if self._input is not None:
                # Apply input to the first node (ForwardReferences should resolve now)
                first_node = self._nodes[0]._copy(_inputs=cnode._wrap_inputs(self._input))
                nodes_with_input = [first_node] + self._nodes[1:]
                # Recreate the chain with the connected input
                self._created_chain = Chain(nodes_with_input)

            # Register all chain nodes in the context
            for node_instance in self._created_chain.nodes:
                if node_instance not in self.context._dependency_registry:
                    self.context._dependency_registry[node_instance] = []

                # Register named nodes
                if (node_instance.name is not None and
                    node_instance.name not in self.context._nodes):
                    self.context._nodes[node_instance.name] = node_instance

            # Track chain dependencies (each node depends on the previous one)
            for i in range(1, len(self._created_chain.nodes)):
                prev_node = self._created_chain.nodes[i-1]
                current_node = self._created_chain.nodes[i]
                self.context._add_dependency(prev_node, current_node)

            # Track dependencies from all inputs to the first chain node
            # Use the constructed chain's first node inputs which have the correct merged list
            first_chain_node = self._created_chain.first
            for inp in first_chain_node.inputs:
                if inp is not None:
                    input_node, _ = inp
                    self.context._add_dependency(input_node, first_chain_node)

    @property
    def parent(self) -> NodeInstance:
        """Return the parent NodeInstance for this chain."""
        return self.context.parent

    def node(self, node_type: 'NodeType', /, name: str | None = None, **attributes: Any) -> NodeInstance:
        """Add a node to this chain (not registered with context until chain completes)."""
        # Create node without registering it with the context
        node_instance = cnode.NodeInstance(
            _parent=self.context.parent,  # Use the context's parent
            node_type=node_type,
            name=name,
            attributes=HashableMapping(attributes) if attributes else HashableMapping(),
        )
        self._nodes.append(node_instance)
        return node_instance

    @property
    def last(self) -> 'NodeInstance | ForwardReference':
        """Return the last node that will be in this chain."""
        if hasattr(self, '_created_chain') and self._created_chain:
            return self._created_chain.last
        elif self._nodes:
            # During chain construction - return a deferred forward reference
            return DeferredChainPropertyReference(
                resolution_type='deferred_chain_property',
                chain_builder=self,
                property_name='last'
            )
        else:
            raise RuntimeError("Chain is empty")

    @property
    def first(self) -> 'NodeInstance | ForwardReference':
        """Return the first node that will be in this chain."""
        if hasattr(self, '_created_chain') and self._created_chain:
            return self._created_chain.first
        elif self._nodes:
            # During chain construction - return a deferred forward reference
            return DeferredChainPropertyReference(
                resolution_type='deferred_chain_property',
                chain_builder=self,
                property_name='first'
            )
        else:
            raise RuntimeError("Chain is empty")

    def __getitem__(self, index: int) -> NodeInstance:
        """Access nodes in the chain by index."""
        if hasattr(self, '_created_chain') and self._created_chain:
            return self._created_chain[index]
        elif self._nodes:
            return self._nodes[index]
        else:
            raise IndexError("Chain is empty")

    def __len__(self) -> int:
        """Return the number of nodes in the chain."""
        if hasattr(self, '_created_chain') and self._created_chain:
            return len(self._created_chain)
        else:
            return len(self._nodes)

    @property
    def inputs(self) -> 'Inputs':
        """Return the inputs of the first node in the chain."""
        if hasattr(self, '_created_chain') and self._created_chain:
            return self._created_chain.inputs
        elif self._nodes:
            return self._nodes[0].inputs
        else:
            raise RuntimeError("Chain is empty")


def chain(
    *nodes: 'Any',  # ChainableNode
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
    from collections.abc import Iterator

    # Check for the old _input parameter and provide a helpful error message
    if '_input' in attributes:
        raise TypeError(
            "The '_input' parameter is no longer supported on chain(). "
            "Instead, pass the input to the first node: "
            "chain(node(parent, 'type', 'name', _input=your_input), ...)"
        )

    def _handle_entry(item: 'Any') -> Iterator[NodeInstance]:
        match item:
            case cnode.NodeInstance():
                yield item
            case Chain():
                yield from item.nodes

    flattened_nodes = tuple((
        node
        for item in nodes
        for node in _handle_entry(item)
    ))

    # Validate that all nodes have the same parent
    if flattened_nodes:
        first_parent = flattened_nodes[0].parent
        for i, node in enumerate(flattened_nodes[1:], 1):
            if node.parent != first_parent:
                raise ValueError(
                    f"All nodes in a context must have same parent. \n"
                    f"Node 0 has parent {first_parent}, node {i} has parent {node.parent}"
                )

    return Chain(
        nodes=flattened_nodes,  # Only NodeInstance objects now
    )
