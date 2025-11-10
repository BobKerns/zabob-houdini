"""
Core Zabob-Houdini API for creating Houdini node graphs.

This module assumes it's running in a Houdini environment (mediated by bridge or test fixture).
"""

from __future__ import annotations

import copy
import functools
from abc import ABC, abstractmethod
import dataclasses
from dataclasses import dataclass, field
from typing import Any, Union
from types import MappingProxyType
import weakref



from typing import Any, TypeAlias, overload, Iterator
from dataclasses import dataclass
from abc import ABC, abstractmethod
import functools
import hou

# Global registry to map hou.Node objects back to their originating NodeInstance
# Uses WeakKeyDictionary so that when hou.Node objects are deleted, the mapping is automatically cleaned up
_node_registry: weakref.WeakKeyDictionary[hou.Node, 'NodeInstance'] = weakref.WeakKeyDictionary()


def _wrap_hou_node(hou_node: hou.Node) -> 'NodeInstance':
    """
    Wrap a hou.Node in a NodeInstance, checking the global registry first.

    If the hou.Node was originally created by a NodeInstance, returns that original.
    Otherwise, creates a new NodeInstance wrapper.

    Args:
        hou_node: The Houdini node to wrap

    Returns:
        NodeInstance object (either original or newly created wrapper)
    """
    # Check if we already have this node in our registry
    if hou_node in _node_registry:
        return _node_registry[hou_node]

    # Create a new wrapper NodeInstance
    node_path = hou_node.path()
    parent_path = '/'.join(node_path.split('/')[:-1]) or '/'
    node_name = node_path.split('/')[-1]

    wrapped = NodeInstance(
        parent=parent_path,
        node_type=hou_node.type().name(),
        name=node_name,
        _node=hou_node  # Pass the existing node so create() returns it
    )

    # Register this wrapper in case it gets referenced again
    _node_registry[hou_node] = wrapped

    return wrapped


class HashableMapping:
    """
    A hashable immutable mapping for use in frozen dataclasses.

    Wraps a MappingProxyType and provides hash functionality.
    """

    def __init__(self, mapping: dict[str, Any] | None = None):
        self._mapping = MappingProxyType(mapping or {})

    def __hash__(self) -> int:
        """Hash based on sorted items for consistent hashing."""
        return hash(tuple(sorted(self._mapping.items())))

    def __eq__(self, other: object) -> bool:
        """Equality based on underlying mapping."""
        if isinstance(other, HashableMapping):
            return self._mapping == other._mapping
        return self._mapping == other

    def __getitem__(self, key: str) -> Any:
        return self._mapping[key]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self) -> int:
        return len(self._mapping)

    def get(self, key: str, default: Any = None) -> Any:
        return self._mapping.get(key, default)

    def items(self):
        return self._mapping.items()

    def keys(self):
        return self._mapping.keys()

    def values(self):
        return self._mapping.values()

    def copy(self) -> dict[str, Any]:
        """Return a copy as a regular dict."""
        return dict(self._mapping)


# Type aliases for clarity
NodeParent: TypeAlias = "str | NodeInstance | hou.Node"
"""A parent node, either as a path string (e.g., "/obj"), NodeInstance, or hou.Node object."""

NodeType: TypeAlias = str
"""A Houdini node type name (e.g., "geo", "box", "xform"). Will expand to NodeTypeInstance later."""

CreatableNode: TypeAlias = 'NodeInstance | Chain'
"""A node or chain that can be created via .create() method."""

ChainableNode: TypeAlias = 'NodeInstance | Chain | hou.Node'
"""A node or chain that can be used in a chain - includes existing hou.Node objects."""

InputNode: TypeAlias = 'NodeInstance | Chain | hou.Node | None'
"""A node that can be used as input - NodeInstance, Chain (uses last node), actual hou.Node, or None for sparse connections."""


class HoudiniNodeBase(ABC):
    """
    Base class for Houdini node representations.

    Provides common functionality for NodeInstance and Chain classes.
    """

    def __init__(self, parent: NodeParent, attributes: dict[str, Any] | None = None,
                 inputs: tuple[InputNode, ...] | None = None):
        self.parent = parent
        self.attributes = attributes if attributes is not None else {}
        self.inputs = inputs if inputs is not None else tuple()

    @abstractmethod
    @functools.cache
    def create(self) -> Any:
        """Create the actual Houdini node(s). Return type varies by implementation."""
        pass

    @abstractmethod
    def copy(self) -> 'HoudiniNodeBase':
        """Return a copy of this node/chain object. Copies are independent for creation.

        This is used by Chain.create() to avoid mutating original definitions when
        creating Houdini nodes. Implementations should deep-copy mutable containers
        like attributes and inputs but need not copy hou.Node objects.
        """
        pass

    def __hash__(self) -> int:
        """Hash based on object identity - these represent specific node instances."""
        return id(self)

    def __eq__(self, other: object) -> bool:
        """Equality based on object identity - these represent specific node instances."""
        return self is other


@dataclasses.dataclass(frozen=True)
class NodeInstance(HoudiniNodeBase):
    """
    Represents a single Houdini node with parameters and inputs.

    This is an immutable node definition that can be cached and reused.
    Node creation is deferred until create() is called.
    """
    parent: NodeParent
    node_type: str
    name: str | None = None
    attributes: HashableMapping = field(default_factory=HashableMapping)
    inputs: tuple["InputNode", ...] = field(default_factory=tuple)
    _node: "hou.Node | None" = field(default=None, hash=False)

    @functools.cache
    def create(self) -> hou.Node:
        """
        Create the actual Houdini node.

        Returns:
            The created Houdini node object (cached via @functools.cache).
        """

        # Return existing node if provided
        if self._node is not None:
            return self._node

        # Resolve parent node
        match self.parent:
            case str() as parent_path:
                parent_node = hou.node(parent_path)
                if parent_node is None:
                    raise ValueError(f"Parent node not found: {parent_path}")
            case NodeInstance() as parent_instance:
                # Parent is another NodeInstance - it should be created first
                parent_node = parent_instance.create()
            case hou.Node() as houdini_node:
                # It's already a Houdini node
                parent_node = houdini_node
            case _:
                raise TypeError(
                    f"Parent must be a path string, NodeInstance, or hou.Node object, "
                    f"got {type(self.parent).__name__}"
                )

        # Create the node
        created_node = parent_node.createNode(self.node_type, self.name)

        # Set attributes/parameters
        if self.attributes:
            try:
                created_node.setParms(dict(self.attributes))
            except Exception as e:
                print(f"Warning: Failed to set parameters: {e}")

        # Connect inputs
        if self.inputs:
            for i, input_node in enumerate(self.inputs):
                # Skip None inputs (for sparse input connections)
                if input_node is None:
                    continue

                try:
                    match input_node:
                        case NodeInstance() as node_instance:
                            # Input is a NodeInstance - create it first
                            input_hou_node = node_instance.create()
                        case Chain() as chain:
                            # Input is a Chain - create it and use the last node's created hou.Node
                            created_nodes = chain.create()
                            if not created_nodes:
                                raise ValueError(f"Input {i} is an empty chain, cannot use as input")
                            last_node_instance = created_nodes[-1]
                            input_hou_node = last_node_instance.create()  # Use last node in chain
                        case hou.Node() as houdini_node:
                            # It's already a Houdini node object
                            input_hou_node = houdini_node
                        case _:
                            raise TypeError(
                                f"Input {i} must be a NodeInstance, Chain, or Houdini node object, "
                                f"got {type(input_node).__name__}"
                            )
                    created_node.setInput(i, input_hou_node)
                except Exception as e:
                    print(f"Warning: Failed to connect input {i}: {e}")

        # Register this NodeInstance as the creator of this hou.Node
        _node_registry[created_node] = self

        return created_node

    def copy(self) -> 'NodeInstance':
        """Return a shallow copy suitable for creation.

        Attributes dict and inputs list are copied to avoid mutating originals.
        """
        copied_inputs = []
        if self.inputs:
            for inp in self.inputs:
                # If input is a Chain or NodeInstance, prefer to keep the object
                # but if it's a Chain we call its copy to avoid shared state.
                if isinstance(inp, Chain):
                    copied_inputs.append(inp.copy())
                else:
                    copied_inputs.append(inp)

        return NodeInstance(
            parent=self.parent,
            node_type=self.node_type,
            name=self.name,
            attributes=HashableMapping(self.attributes.copy()) if self.attributes else HashableMapping(),
            inputs=tuple(copied_inputs),
            _node=None  # Copy should not preserve the created node reference
        )


@dataclass(frozen=True)
class Chain(HoudiniNodeBase):
    """
    Represents a chain of Houdini nodes that can be created.

    Nodes in the chain are automatically connected in sequence.
    """
    parent: NodeParent
    nodes: tuple[ChainableNode, ...]
    name_prefix: str | None = None
    attributes: HashableMapping | None = None
    inputs: tuple[InputNode, ...] | None = None

    @functools.cache
    def _flatten_nodes(self) -> tuple['NodeInstance', ...]:
        """
        Flatten the chain, splicing in any Chain objects.

        Returns:
            A tuple of NodeInstance objects (immutable for caching).
        """
        flattened: list[NodeInstance] = []
        for item in self.nodes:
            match item:
                case NodeInstance():
                    flattened.append(item)
                case Chain():
                    flattened.extend(item._flatten_nodes())
                case _ if isinstance(item, hou.Node):
                    # It's a Houdini node - wrap it using the registry-aware helper
                    wrapped = _wrap_hou_node(item)
                    flattened.append(wrapped)
                case _:
                    raise TypeError(
                        f"Chain nodes must be NodeInstance, Chain, or hou.Node objects, "
                        f"got {type(item).__name__}"
                    )

        # Return immutable tuple for caching
        return tuple(flattened)

    @overload
    def __getitem__(self, key: int) -> NodeInstance: ...

    @overload
    def __getitem__(self, key: slice) -> 'Chain': ...

    @overload
    def __getitem__(self, key: str) -> NodeInstance: ...

    def __getitem__(self, key: int | slice | str) -> ChainableNode:
        """
        Access nodes in the chain by index, slice, or name.

        Args:
            key: Integer index, slice, or node name string

        Returns:
            NodeInstance for int/str keys, Chain for slice keys
        """
        flattened = self._flatten_nodes()

        match key:
            case int() as index:
                return flattened[index]
            case slice() as slice_obj:
                # Return a new Chain with the subset of nodes
                subset = flattened[slice_obj]
                return Chain(
                    parent=self.parent,
                    nodes=subset,
                    name_prefix=self.name_prefix,
                    attributes=HashableMapping(self.attributes.copy()) if self.attributes else None,
                    inputs=self.inputs  # Tuples are immutable, no need to copy
                )
            case str() as name:
                # Find node by name
                for node_instance in flattened:
                    if node_instance.name == name:
                        return node_instance
                raise KeyError(f"No node found with name '{name}'")
            case _:
                raise TypeError(f"Chain indices must be integers, slices, or strings, not {type(key).__name__}")

    def __len__(self) -> int:
        """Return the number of nodes in the flattened chain."""
        return len(self._flatten_nodes())

    def __iter__(self) -> "Iterator[NodeInstance]":
        """Return an iterator over the flattened nodes in the chain."""
        return iter(self._flatten_nodes())

    def first_node(self) -> hou.Node:
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

    def last_node(self) -> hou.Node:
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

    def hou_nodes(self) -> tuple[hou.Node, ...]:
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

        Returns:
            Tuple of NodeInstance objects for created nodes. Same instances
            returned on subsequent calls (cached via @functools.cache).
        """
        flattened_nodes = self._flatten_nodes()
        if not flattened_nodes:
            return tuple()

        created_node_instances: list[NodeInstance] = []
        previous_node: hou.Node | None = None

        # Handle inputs to the first node in the chain
        # Note: objects are frozen, so we modify during copying below

        # Create each node (using copies) and connect them in sequence. We return
        # the NodeInstance copies used for creation so callers can inspect them.
        for i, node_instance in enumerate(flattened_nodes):
            # Handle chain inputs to first node and previous node connections
            if i == 0 and self.inputs:
                # First node gets chain inputs plus its own inputs
                if node_instance.inputs:
                    modified_inputs = node_instance.inputs + self.inputs
                else:
                    modified_inputs = self.inputs
                node_copy = node_instance.copy()
                # Create new instance with modified inputs using dataclasses.replace
                import dataclasses
                node_copy = dataclasses.replace(node_copy, inputs=modified_inputs)
            elif i > 0 and previous_node is not None:
                # Subsequent nodes get previous node as input
                node_copy = node_instance.copy()
                if node_copy.inputs:
                    modified_inputs = (previous_node,) + node_copy.inputs
                else:
                    modified_inputs = (previous_node,)
                import dataclasses
                node_copy = dataclasses.replace(node_copy, inputs=modified_inputs)
            else:
                node_copy = node_instance.copy()

            # Create the node in Houdini (NodeInstance.create caches result)
            node_copy.create()
            created_node_instances.append(node_copy)

            # For the next iteration, pass the actual created Houdini node as input
            previous_node = node_copy.create()

        return tuple(created_node_instances)

    def copy(self) -> 'Chain':
        """Return a copy of this Chain (copies contained NodeInstances/Chains)."""
        copied_nodes: list[ChainableNode] = []
        for item in self.nodes:
            if isinstance(item, NodeInstance):
                copied_nodes.append(item.copy())
            elif isinstance(item, Chain):
                copied_nodes.append(item.copy())
            else:
                # hou.Node or other: keep as-is
                copied_nodes.append(item)

        return Chain(
            parent=self.parent,
            nodes=tuple(copied_nodes),
            name_prefix=self.name_prefix,
            attributes=HashableMapping(self.attributes.copy()) if self.attributes else None,
            inputs=self.inputs  # Tuples are immutable, no need to copy
        )


def node(
    parent: NodeParent,
    node_type: NodeType,
    name: str | None = None,
    _input: 'InputNode | list[InputNode] | None' = None,
    _node: 'hou.Node | None' = None,
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
        **attributes: Node parameter values

    Returns:
        NodeInstance that can be created with .create()
    """
    inputs = []
    if _input is not None:
        match _input:
            case list() as input_list:
                inputs.extend(input_list)  # List can contain None values for sparse inputs
            case _ as single_input:
                inputs.append(single_input)

    return NodeInstance(
        parent=parent,
        node_type=node_type,
        name=name,
        attributes=HashableMapping(attributes) if attributes else HashableMapping(),
        inputs=tuple(inputs),
        _node=_node
    )


def chain(
    parent: NodeParent,
    *nodes: ChainableNode,
    _input: "InputNode | list[InputNode] | None" = None,
    name_prefix: str | None = None,
    **attributes: Any
) -> Chain:
    """
    Create a chain of nodes definition.

    Args:
        parent: Parent node (path string or NodeInstance)
        *nodes: Sequence of NodeInstance objects, Chain objects, or Houdini nodes to chain together
        _input: Optional input node(s) to connect to start of chain (NodeInstance, Chain, hou.Node, or None)
        name_prefix: Optional prefix for generated node names
        **attributes: Shared attributes for all nodes in chain

    Returns:
        Chain that can be created with .create()
    """
    inputs = []
    if _input is not None:
        match _input:
            case list() as input_list:
                inputs.extend(input_list)
            case _ as single_input:
                inputs.append(single_input)

    return Chain(
        parent=parent,
        nodes=nodes,  # nodes is already a tuple from *nodes
        name_prefix=name_prefix,
        attributes=HashableMapping(attributes) if attributes else None,
        inputs=tuple(inputs) if inputs else None
    )


def hou_node(path: str) -> 'hou.Node':
    """Get a Houdini node, raising exception if not found."""
    n = hou.node(path)
    if n is None:
        raise ValueError(f"Node at path '{path}' does not exist.")
    return n


def get_node_instance(hou_node: hou.Node) -> 'NodeInstance | None':
    """
    Get the original NodeInstance that created a hou.Node, if any.

    Args:
        hou_node: The Houdini node to look up

    Returns:
        The original NodeInstance that created this node, or None if not found
    """
    return _node_registry.get(hou_node)


def wrap_node(hou_node: hou.Node) -> 'NodeInstance':
    """
    Wrap a hou.Node in a NodeInstance, preferring the original if available.

    This is the public interface to _wrap_hou_node.

    Args:
        hou_node: The Houdini node to wrap

    Returns:
        NodeInstance object (either original or newly created wrapper)
    """
    return _wrap_hou_node(hou_node)
