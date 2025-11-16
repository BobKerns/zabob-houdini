"""
Core Zabob-Houdini API for creating Houdini node graphs.

This module assumes it's running in a Houdini environment (mediated by bridge or test fixture).
"""

from __future__ import annotations

from collections import defaultdict
import functools
from abc import ABC, abstractmethod
import dataclasses
from dataclasses import dataclass, field
from typing import Any, TypeVar, cast, TypeAlias, overload, TYPE_CHECKING
from types import MappingProxyType
import weakref
from itertools import zip_longest, islice
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from abc import ABC, abstractmethod
import functools

# This isn't functionally needed, but it avoids mpy SIGSEGVing from trying
# to actually import the real module under some circumstances.
if TYPE_CHECKING:
    import hou
else:
    try:
        import hou
    except ImportError:
        # hou module not available - this will be handled at runtime
        hou = None  # type: ignore

if TYPE_CHECKING:
    T = TypeVar('T', bound=hou.Node)
else:
    T = TypeVar('T')

# Global registry to map hou.Node objects back to their originating NodeInstance
# Uses WeakKValueDictionary. It turns out that hou.Node objects do not have
# stable identity; each hou.node() call returns a new object, so we need
# to key by path instead of object identity.
_node_registry: weakref.WeakValueDictionary[str, 'NodeInstance'] = weakref.WeakValueDictionary()


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
    path = hou_node.path()
    if path in _node_registry:
        return _node_registry[path]

    # Create a new wrapper NodeInstance
    parent_path = '/'.join(path.split('/')[:-1]) or ROOT
    node_name = path.split('/')[-1]

    wrapped = NodeInstance(
        _parent=parent_path,
        node_type=hou_node.type().name(),
        name=node_name,
        _node=hou_node  # Pass the existing node so create() returns it
    )

    # Register this wrapper in case it gets referenced again
    _node_registry[hou_node.path()] = wrapped

    return wrapped

_generated_names: dict[str, int] = defaultdict(lambda: 1)
def _generate_name(parent: str, type: str) -> str:
    """Generate a unique name with the given prefix."""
    while True:
        count = _generated_names[type]
        _generated_names[type] += 1
        name = f"{type}{count}"
        path = f"{parent}/{name}"
        if hou.node(path) is None:
            return name

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


# Type aliases for clarity
NodeParent: TypeAlias = "str | NodeInstance | hou.Node"
"""A parent node, either as a path string (e.g., "/obj"), NodeInstance, or hou.Node object."""

NodeType: TypeAlias = str
"""A Houdini node type name (e.g., "geo", "box", "xform"). Will expand to NodeTypeInstance later."""

CreatableNode: TypeAlias = 'NodeInstance | Chain'
"""A node or chain that can be created via .create() method."""

ChainableNode: TypeAlias = 'NodeInstance | Chain'
"""A node or chain that can be used in a chain - includes existing hou.Node objects."""

InputNodeSpec: TypeAlias = 'NodeInstance | Chain | hou.Node | str'

InstanceNodeSpec: TypeAlias = 'tuple[InputNodeSpec, int] | InputNodeSpec'
"""A connection specification: either (<node>, <output_index>) tuple or just <node> (defaults to output 0)."""

InputNode: TypeAlias = 'InstanceNodeSpec | None'
"""A node that can be used as input - InputConnection or None for sparse connections."""

InputNodes: TypeAlias = 'Sequence[InputNode]'

ResolvedConnection: TypeAlias = 'tuple[NodeInstance, int]'
"""A resolved connection: (node, output_index)."""

Inputs: TypeAlias = 'tuple[ResolvedConnection | None, ...]'
"""The inputs for a node or chain, as a tuple of ResolvedConnection objects or None for sparse connections."""

ChainCopyParam: TypeAlias = 'int | str | NodeInstance'
"""A parameter for Chain.copy() reordering: index, name, or NodeInstance to insert."""


def _merge_inputs(in1: Inputs, in2: Inputs) -> Inputs:
    """Merge two input lists, preferring non-None values from the first list."""
    if not in1:
        return tuple(in2)
    if not in2:
        return tuple(in1)

    merged = [
        l if l else r
        for l, r in zip_longest(in1, in2, fillvalue=None)
    ]
    return tuple(merged)

@dataclasses.dataclass(frozen=True)
class NodeBase(ABC):
    """
    Base class for Houdini node representations.

    Provides common functionality for NodeInstance and Chain classes.
    """

    @functools.cached_property
    @abstractmethod
    def parent(self) -> NodeInstance:
        """Return the parent NodeInstance for this node/chain."""
        pass

    @functools.cached_property
    @abstractmethod
    def inputs(self) -> Inputs:
        """Return the input nodes for this node/chain."""
        pass

    @functools.cached_property
    @abstractmethod
    def first(self) -> NodeInstance:
        """Return the first node for this node/chain."""
        pass

    @functools.cached_property
    @abstractmethod
    def last(self) -> NodeInstance:
        """Return the last node for this node/chain."""
        pass

    @abstractmethod
    def copy(self, /, _inputs: InputNodes=(), _chain: Chain | None=None) -> 'NodeBase':
        """Return a copy of this node/chain object. Copies are independent for creation.

        This is used by Chain.create() to avoid mutating original definitions when
        creating Houdini nodes.
        """
        pass

    def __hash__(self) -> int:
        """Hash based on object identity - these represent specific node instances."""
        return id(self)

    def __eq__(self, other: object) -> bool:
        """Equality based on object identity - these represent specific node instances."""
        return self is other

@dataclasses.dataclass(frozen=True, eq=False)
class NodeInstance(NodeBase):
    """
    Represents a single Houdini node with parameters and inputs.

    This is an immutable node definition that can be cached and reused.
    Node creation is deferred until create() is called.
    """

    _parent: NodeParent = field(repr=False)
    node_type: str
    name: str | None = None
    attributes: HashableMapping = field(default_factory=HashableMapping)
    _inputs: Inputs = field(default_factory=tuple)
    _node: "hou.Node | None" = field(default=None, hash=False)
    _display: bool = field(default=False, hash=False)
    _render: bool = field(default=False, hash=False)
    _chain: "Chain | None" = field(default=None, hash=False)

    @functools.cached_property
    def parent(self) -> NodeInstance:
        match self._parent:
            case '/' | None:
                return ROOT
            case str():
                return wrap_node(hou_node(self._parent))
            case NodeInstance():
                return self._parent
            case hou.Node():
                return wrap_node(self._parent)
            case _:
                raise RuntimeError(f"Invalid parent: {self._parent!r}")

    @functools.cached_property
    def first(self) -> NodeInstance:
        """Return the first node in this instance, which is itself."""
        return self

    @functools.cached_property
    def last(self) -> NodeInstance:
        """Return the last node in this instance, which is itself."""
        return self

    @functools.cached_property
    def inputs(self) -> Inputs:
        """
        Return the input nodes for this node/chain.

        Each input will be either None or a ResolvedConnection tuple of (NodeInstance, output_index).
        """
        return tuple((_wrap_input(inp, 0) for inp in self._inputs))

    def create(self, as_type: type[T] | None = None, _skip_chain: bool = False) -> T:
        """
        Create the actual Houdini node.

        Args:
            as_type: Expected node type to narrow the return type to (e.g., hou.SopNode).
                    Defaults to hou.Node for maximum compatibility.
            _skip_chain: Internal flag to avoid recursion when creating chain nodes.

        Returns:
            The created Houdini node object, cast to the specified type.
            Result is cached via @functools.cache.

        Raises:
            TypeError: If the created node cannot be cast to the specified type,
                      or if an existing node is not of the expected type.
        """
        # Default as_type to hou.Node if not specified
        actual_type: type[T] = as_type if as_type is not None else hou.Node  # type: ignore

        # If this node is part of a chain, create the entire chain first
        if self._chain is not None and not _skip_chain:
            self._chain.create()
            # Now call _do_create again to get the cached result
            node = self._do_create()
            return self._asType(node, actual_type)

        node = self._do_create()
        return self._asType(node, actual_type)

    @functools.cache
    def _do_create(self) -> hou.Node:
        '''
        Actually create and cache the node. This is separated from `create`
        to allow caching independent of the arguments passed to `create`.
        The caching is essential to avoid recursion.
        '''
        # Don't create the parent if we've been supplied _node.
        #
        # Or we'll get infinite recursion at the root.
        if self._node is not None:
            # Use existing node if provided
            created_node = self._node
        else:
            parent_node = self.parent.create()
            # Create the node
            created_node: hou.Node = parent_node.createNode(self.node_type, self.name)

        # Set attributes/parameters
        if self.attributes:
            match created_node:
                case hou.OpNode():
                    try:
                        created_node.setParms(dict(self.attributes))
                    except Exception as e:
                        print(f"Warning: Failed to set parameters: {e}")
                case _:
                    print(f"Warning: Cannot set parameters on node type {created_node.type().name()} - skipping attributes")

        # Connect inputs
        if self.inputs:
            for i, connection in enumerate(self.inputs):
                # Skip None inputs (for sparse input connections)
                if connection is None:
                    continue

                input_node, output_idx = connection

                try:
                    match input_node:
                        case NodeInstance() as node_instance:
                            # Input is a NodeInstance - create it first
                            input_hou_node = node_instance.create()
                        case _:
                            raise TypeError(
                                f"Input {i} must be a NodeInstance, Chain, or Houdini node object, "
                                f"got {type(input_node).__name__}"
                            )
                    created_node.setInput(i, input_hou_node, output_idx)
                except Exception as e:
                    print(f"Warning: Failed to connect input {i}: {e}")

        # Set display and render flags (only works on SopNode types)
        if self._display:
            try:
                if hasattr(created_node, 'setDisplayFlag'):
                    created_node.setDisplayFlag(True)  # type: ignore
            except Exception as e:
                print(f"Warning: Failed to set display flag: {e}")

        if self._render:
            try:
                if hasattr(created_node, 'setRenderFlag'):
                    created_node.setRenderFlag(True)  # type: ignore
            except Exception as e:
                print(f"Warning: Failed to set render flag: {e}")

        # Register this NodeInstance as the creator of this hou.Node
        _node_registry[created_node.path()] = self

        # TODO: Create our own placement algorithm, calling moveToGoodPosition is really ugly
        created_node.moveToGoodPosition()

        return created_node

    def _asType(self, node: hou.Node, cls: type[T]) -> T:
        """
        Narrow the type of a node to the specified type if possible.

        Throws a TypeError if the created node cannot be cast to the specified type.
        """
        if isinstance(node, cls):
            return node
        raise TypeError(f"Cannot convert NodeInstance to {cls.__name__}")

    @property
    def path(self) -> str:
        """Return the path of the node."""
        if self._node is not None:
            return self._node.path()
        else:
           return f'{self.parent.path}/{self.name or self.node_type}'

    def copy(self, /,
             _inputs: InputNodes = (),
             _chain: 'Chain | None' = None,
             *,
             name: str | None = None,
             attributes: dict[str, Any] | None = None,
             _display: bool | None = None,
             _render: bool | None = None) -> 'NodeInstance':
        """Return a copy with optional modifications.

        Args:
            _inputs: New input connections (merged with existing)
            _chain: Chain this node belongs to
            name: New name for the node (if provided)
            attributes: Additional/override attributes (merged with existing)
            _display: Override display flag
            _render: Override render flag

        Returns:
            New NodeInstance with merged properties
        """
        inputs = _wrap_inputs(_inputs)
        merged_inputs = _merge_inputs(inputs, self.inputs)

        # Merge attributes: existing + new/override
        if attributes:
            merged_attributes = dict(self.attributes)
            merged_attributes.update(attributes)
            final_attributes = HashableMapping(merged_attributes)
        else:
            # Preserve original attributes object when no modifications
            final_attributes = self.attributes

        return NodeInstance(
            _parent=self._parent,
            node_type=self.node_type,
            name=name if name is not None else self.name,
            attributes=final_attributes,
            _inputs=tuple(merged_inputs),
            _node=None,  # Copy should not preserve the created node reference
            _display=_display if _display is not None else self._display,
            _render=_render if _render is not None else self._render,
            _chain=_chain,
        )


@dataclass(frozen=True, eq=False)
class Chain(NodeBase):
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
        nodes = tuple(n.copy(_chain=self) for n in nodes)
        object.__setattr__(self, 'nodes', nodes)

    @functools.cached_property
    def parent(self) -> NodeInstance:
        match self.nodes:
            case ():
                return ROOT
            case NodeInstance() as n, *_:
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
    def inputs(self) -> Inputs:
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

    def __getitem__(self, key: int | slice | str) -> ChainableNode:
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
        nodes = self.nodes
        if not nodes:
            return tuple()

        created_node_instances: list[NodeInstance] = []
        previous_node: hou.Node | None = None

        # Create each node and connect them in sequence - NO COPYING!
        # Use _skip_chain=True to avoid recursion since we're already creating the chain
        for i, node_instance in enumerate(nodes):
            # Create the node in Houdini (NodeInstance.create caches result)
            created_hou_node = node_instance.create(_skip_chain=True)
            created_node_instances.append(node_instance)

            # Connect this node to the previous one if needed
            if i > 0 and previous_node is not None:
                try:
                    created_hou_node.setInput(0, previous_node)
                except Exception as e:
                    print(f"Warning: Failed to connect chain nodes: {e}")

            # For the next iteration
            previous_node = created_hou_node

        return tuple(created_node_instances)

    def copy(self, *copy_params: ChainCopyParam, _inputs: InputNodes=(), _chain: Chain | None=None) -> 'Chain':  # type: ignore[override]
        """
        Return a copy of this Chain with nodes reordered, dropped, or inserted.

        Args:
            *copy_params: Parameters specifying nodes to copy:
                - int: Index of existing node to copy (can reorder/duplicate)
                - str: Name of existing node to copy
                - NodeInstance: New node to insert at this position
                If no arguments given, copies all nodes in original order
            _inputs: Input nodes for the first node in the new chain
            _chain: Parent chain reference

        Returns:
            New Chain with specified nodes in specified order

        Examples:
            chain.copy(3, 2, 1, 0)      # Reverse 4-element chain
            chain.copy(0, 2)            # Copy only nodes 0 and 2
            chain.copy("box", "sphere") # Copy by name
            chain.copy(0, new_node, 1)  # Insert new_node between positions 0 and 1
        """
        # Build new node list using self[param] for uniform access
        new_nodes = (
            self.nodes if not copy_params
            else [
                param if isinstance(param, NodeInstance) else self[param]
                for param in copy_params
                ]
        )

        if not new_nodes:
            raise ValueError("Chain copy must result in at least one node")

        # Handle inputs for first node
        inputs = _wrap_inputs(_inputs)
        self_inputs: Inputs = ()
        if self.nodes and new_nodes and copy_params:
            # Get inputs from the original first node being copied
            first_param = copy_params[0]
            if not isinstance(first_param, NodeInstance):
                # It's an int or str - get the original node's inputs
                original_first = self[first_param]
                self_inputs = original_first.inputs
            # If first item is inserted NodeInstance, it keeps its own inputs

        merged_inputs = _merge_inputs(inputs, self_inputs)

        # Copy first node with merged inputs
        first_node = new_nodes[0].copy(_inputs=merged_inputs)

        # Copy remaining nodes
        remaining_nodes = [n.copy() for n in new_nodes[1:]]

        # Create new chain - __init__ will copy and set _chain references
        new_chain = Chain(
            nodes=(first_node, *remaining_nodes),
        )
        return new_chain


def node(
    parent: NodeParent,
    node_type: NodeType,
    name: str | None = None,
    _input: 'InputNode | Sequence[InputNode] | None' = None,
    _node: 'hou.Node | None' = None,
    _display: bool = False,
    _render: bool = False,
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
    inputs = _wrap_inputs(_input)

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

    return NodeInstance(
        _parent=parent,
        node_type=node_type,
        name=name,
        attributes=HashableMapping(attributes) if attributes else HashableMapping(),
        _inputs=tuple(inputs),
        _node=_node,
        _display=_display,
        _render=_render
    )


def chain(
    *nodes: ChainableNode,
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
    # Check for the old _input parameter and provide a helpful error message
    if '_input' in attributes:
        raise TypeError(
            "The '_input' parameter is no longer supported on chain(). "
            "Instead, pass the input to the first node: "
            "chain(node(parent, 'type', 'name', _input=your_input), ...)"
        )

    def _handle_entry(item: ChainableNode) -> Iterator[NodeInstance]:
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

    return Chain(
        nodes=flattened_nodes,  # Only NodeInstance objects now
    )


def merge(*inputs: NodeInstance, **attributes: Any) -> NodeInstance:
    """
    Create a merge node with multiple inputs.

    Args:
        *inputs: NodeInstance objects to merge (must have same parent)
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

        # Merge with parameters
        merged = merge(box, sphere, tol=0.01)
    """
    if not inputs:
        raise ValueError("merge() requires at least one input")

    # Get parent from first input and verify all have same parent
    first_parent = inputs[0].parent
    for i, inp in enumerate(inputs[1:], 1):
        if inp.parent != first_parent:
            raise ValueError(
                f"All merge inputs must have same parent. "
                f"Input 0 has parent {first_parent}, input {i} has parent {inp.parent}"
            )

    return node(
        first_parent,
        "merge",
        _input=inputs,
        **attributes
    )


def hou_node(path: str) -> 'hou.Node':
    """Get a Houdini node, raising exception if not found."""
    n = hou.node(path)
    if n is None:
        raise ValueError(f"Node at path '{path}' does not exist.")
    return n


def get_node_instance(hnode: hou.Node) -> 'NodeInstance | None':
    """
    Get the original NodeInstance that created a hou.Node, if any.

    Args:
        hnode: The Houdini node to look up

    Returns:
        The original NodeInstance that created this node, or None if not found
    """
    return _node_registry.get(hnode.path())


def wrap_node(hnode: hou.Node | NodeInstance | str) -> 'NodeInstance':
    """
    Wrap a hou.Node in a NodeInstance, preferring the original if available.

    This is the public interface to _wrap_hou_node.

    Args:
        hnode: The Houdini node to wrap

    Returns:
        NodeInstance object (either original or newly created wrapper)
    """

    match hnode:
        case hou.Node():
            return _wrap_hou_node(hnode)
        case str():
            existing = _node_registry.get(hnode)
            if existing is not None:
                return existing
            return _wrap_hou_node(hou_node(hnode))
        case NodeInstance():
            # If it's already a NodeInstance, just return it
            return hnode
        case _:
            raise TypeError(f"Invalid node type: {type(hnode).__name__}")

# Copilot: There are no implicit returns in _wrap_inputs. (DO NOT REMOVE)
def _wrap_inputs(inputs: Sequence[InputNode] | InputNode) -> Inputs:
    """
    Wrap a sequence of input nodes and extract output indices.

    Args:
        inputs: Sequence of input specifications - either (<node>, <output_index>) tuples or just <node>

    Returns:
        Tuple of (wrapped_node, output_index) for actual nodes, or None for None inputs
    """
    match inputs:
        case NodeInstance()|Chain()|hou.Node()|str() as input, int() as idx:
            resolved = _wrap_input(input, idx)
            return (resolved,)
        case NodeInstance()|Chain()|hou.Node()|str() as input:
            resolved = _wrap_input(input, 0)
            return (resolved,)
        case None:
            return ()
        case _:
            return tuple(_wrap_input(inp, 0) for inp in inputs)


# Copilot: There are no implicit returns in _wrap_input. (DO NOT REMOVE)
def _wrap_input(input: InputNode, idx: int) -> ResolvedConnection | None:
    """
    Wrap an input node and extract output index.

    Args:
        input: Input specification - either (<node>, <output_index>) tuple or just <node>

    Returns:
        Tuple of (wrapped_node, output_index) for actual nodes, or None for None inputs
    """
    # Copilot: There are no implicit returns in _wrap_single_input. (DO NOT REMOVE)
    def _wrap_single_input(input: InputNodeSpec) -> NodeInstance|None:
        """Wrap a single input node specification."""
        match input:
            case NodeInstance():
                return input
            case Chain() if len(input.nodes) == 0:
                return None
            case Chain():
                return input.last
            case hou.Node():
                return wrap_node(input)
            case str():
                return wrap_node(hou_node(input))
            case _:
                raise TypeError(f"Invalid input specification: {input}. Expected NodeInstance, Chain, hou.Node, or str.")

    match input:
        case None:
            return None
        case node_spec, output_idx:
            if not isinstance(output_idx, int) or output_idx < 0:
                raise ValueError(f"Output index must be a non-negative integer, got {output_idx}")
            wrapped = _wrap_single_input(node_spec)
            if wrapped is None:
                return None
            return (wrapped, output_idx)
        case tuple():
            raise ValueError(f"Input tuple must have exactly 2 elements: (<node>, <output_index>)")
        case NodeInstance() | Chain() | hou.Node() | str():
            # Single node specification, default to output 0
            wrapped = _wrap_single_input(input)
            if wrapped is None:
                return None
            return (wrapped, idx)
        case _:
            raise TypeError(f"Invalid input specification: {input}. Expected None, (<node>, <output_index>), or <node>")

if TYPE_CHECKING:
    _ROOT: hou.Node
    '''
    The root node, unwrapped.
    '''

    ROOT: NodeInstance
    '''
    The root node, wrapped as a `NodeInstance`.
    '''
else:
    # Runtime initialization - only when hou is available
    if hou is not None:
        _ROOT = hou_node('/')
        ROOT = NodeInstance(
            _parent=cast(NodeInstance, None),
            node_type='root',
            name='/',
            attributes=HashableMapping({}),
            _inputs=(),
            _node=_ROOT
        )
        # Register it
        _node_registry['/'] = ROOT
    else:
        # Placeholder when hou is not available
        ROOT = None  # type: ignore
