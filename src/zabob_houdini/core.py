"""
Core Zabob-Houdini API for creating Houdini node graphs.

This module assumes it's running in a Houdini environment (mediated by bridge or test fixture).
"""

from __future__ import annotations

import sys
from collections import defaultdict
import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, TypeVar, cast, TypeAlias, overload, TYPE_CHECKING
from types import MappingProxyType
import weakref
from itertools import zip_longest
from collections.abc import Iterator, Sequence

if "hou" not in sys.modules:
    # Avoids SIGSEGV when importing hou in non-Houdini environments
    raise ImportError(
        "The 'hou' module is not available. This module requires Houdini's 'hou' module to run."
    )

import hou

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


@dataclass(frozen=True)
class ForwardReference:
    """
    A forward reference to a node that may not exist yet.

    This enables referencing nodes by string name before they're created,
    and accessing chain properties (.first, .last) before chains are complete.
    Resolution happens at create() time.
    """
    resolution_type: str  # 'context_lookup' or 'chain_property'
    context: 'NodeContext | None' = None
    name: str | None = None
    chain_builder: 'ChainBuilder | None' = None
    property_name: str | None = None  # 'first' or 'last'

    def resolve(self) -> 'NodeInstance':
        """Resolve the forward reference to an actual NodeInstance."""
        match self.resolution_type:
            case 'context_lookup':
                if self.context is None or self.name is None:
                    raise RuntimeError("Invalid context lookup forward reference")
                if self.name not in self.context._nodes:
                    raise RuntimeError(f"Forward reference failed: node '{self.name}' not found in context")
                return self.context._nodes[self.name]

            case 'chain_property':
                if self.chain_builder is None or self.property_name is None:
                    raise RuntimeError("Invalid chain property forward reference")

                # Check if the chain has been completed (created_chain exists)
                if hasattr(self.chain_builder, '_created_chain') and self.chain_builder._created_chain:
                    chain = self.chain_builder._created_chain
                    return getattr(chain, self.property_name)
                else:
                    # Chain not completed yet - this should not be resolved now
                    raise RuntimeError(f"Forward reference failed: chain property '{self.property_name}' accessed before chain completion")

            case _:
                raise RuntimeError(f"Unknown forward reference type: {self.resolution_type}")

    def __str__(self) -> str:
        match self.resolution_type:
            case 'context_lookup':
                return f"ForwardRef(name='{self.name}')"
            case 'chain_property':
                return f"ForwardRef(chain.{self.property_name})"
            case _:
                return f"ForwardRef({self.resolution_type})"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass(frozen=True)
class UnresolvedForwardReferenceNode:
    """
    A NodeInstance wrapper that defers ForwardReference resolution until create() time.

    This is used when a ForwardReference cannot be resolved during input wrapping
    (e.g., when accessing chain properties of incomplete chains).
    """
    forward_reference: ForwardReference

    def create(self, *, as_type: type[T] | None = None) -> T:
        """Resolve the ForwardReference and create the actual node."""
        resolved_node = self.forward_reference.resolve()
        return resolved_node.create(as_type=as_type)

    def _create(self, *, _skip_chain: bool = False, as_type: type[T] | None = None) -> T:
        """Internal create method that follows the same pattern as NodeInstance."""
        return self.create(as_type=as_type)

    # Make it behave like a NodeInstance for type checking
    def __getattr__(self, name):
        # Delegate attribute access to the resolved node when accessed
        resolved = self.forward_reference.resolve()
        return getattr(resolved, name)


@dataclass(frozen=True)
class DeferredChainPropertyReference(ForwardReference):
    """
    A ForwardReference that defers chain property access until the chain is complete.

    This is returned when accessing .first/.last on an incomplete chain.
    It will resolve to the actual node when the chain is completed and create() is called.
    """

    def resolve(self) -> 'NodeInstance':
        """
        Resolve the deferred chain property reference.

        This should only be called when the chain is actually complete.
        """
        if self.chain_builder is None or self.property_name is None:
            raise RuntimeError("Invalid deferred chain property reference")

        # The chain should be complete by now
        if hasattr(self.chain_builder, '_created_chain') and self.chain_builder._created_chain:
            chain = self.chain_builder._created_chain
            return getattr(chain, self.property_name)
        else:
            # If not complete, we need to force completion of the parent chain
            # This can happen when accessing chain properties before the with block exits
            raise RuntimeError(f"Cannot resolve chain property '{self.property_name}': parent chain not yet complete. This typically happens when accessing .first/.last on a chain that's still being built within a 'with' block.")

    def __str__(self) -> str:
        return f"DeferredChainRef(chain.{self.property_name})"


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

@dataclass(frozen=True)
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

    def __hash__(self) -> int:
        """Hash based on object identity - these represent specific node instances."""
        return id(self)

    def __eq__(self, other: object) -> bool:
        """Equality based on object identity - these represent specific node instances."""
        return self is other

@dataclass(frozen=True, eq=False)
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
        ForwardReferences will be returned as-is - they need to be resolved later.
        """
        # For ForwardReferences, we can't resolve them yet, so we create a dummy ResolvedConnection
        # They will be properly resolved in _do_create via resolved_inputs
        resolved = []
        for inp in self._inputs:
            if isinstance(inp, ForwardReference):
                # Create a dummy NodeInstance that will be resolved later
                # We'll identify these in _do_create and replace them
                resolved.append(None)  # Mark as unresolved for now
            else:
                resolved.append(_wrap_input(inp, 0))
        return tuple(resolved)

    @functools.cached_property
    def resolved_inputs(self) -> Inputs:
        """
        Return fully resolved inputs with ForwardReferences resolved.

        This property resolves all ForwardReferences to their actual NodeInstances
        and properly wraps them. Should be used during create() time when all
        nodes are available.
        """
        resolved = []
        for inp in self._inputs:
            if isinstance(inp, ForwardReference):
                resolved_input = inp.resolve()
                resolved.append(_wrap_input(resolved_input, 0))
            else:
                resolved.append(_wrap_input(inp, 0))
        return tuple(resolved)

    def create(self, as_type: type[T] | None = None) -> T:
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
        return self._create(as_type)

    def _create(self, as_type: type[T] | None = None, /, _skip_chain: bool = False) -> T:
        """
        Create the actual Houdini node.

        Args:
            as_type: Expected node type to narrow the return type to (e.g., hou.SopNode).
                    Defaults to hou.Node for maximum compatibility.

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
            try:
                created_node: hou.Node = parent_node.createNode(self.node_type, self.name)
            except Exception as e:
                parent_type = parent_node.type().name() if parent_node else "unknown"
                parent_path = parent_node.path() if parent_node else "unknown"
                # Extract the actual error message, skipping generic "The attempted operation failed"
                error_msg = str(e).strip()
                if "The attempted operation failed." in error_msg:
                    error_msg = error_msg.replace("The attempted operation failed.", "").strip()
                if not error_msg:
                    error_msg = "Unknown error"
                name = self.name or f"<<{self.node_type}>>"
                raise RuntimeError(f"Invalid node type '{self.node_type}' for node '{name}' in {parent_type} ({parent_path}): {error_msg}")

        # Set attributes/parameters
        if self.attributes:
            match created_node:
                case hou.OpNode():
                    try:
                        created_node.setParms(dict(self.attributes))
                    except Exception as e:
                        node_type = created_node.type().name()
                        node_name = created_node.name()
                        node_path = created_node.path()
                        print(f"Warning: Failed to set parameters on {node_type} node '{node_name}' ({node_path}): {e}")
                        print(f"  Attempted parameters: {dict(self.attributes)}")
                        # Try to identify which parameters are invalid
                        valid_parms = {parm.name() for parm in created_node.parms()}
                        invalid_parms = set(self.attributes.keys()) - valid_parms
                        if invalid_parms:
                            print(f"  Invalid parameters for {node_type}: {invalid_parms}")
                        print(f"  Valid parameters for {node_type}: {sorted(valid_parms)}")
                case _:
                    print(f"Warning: Cannot set parameters on node type {created_node.type().name()} - skipping attributes")

        # Connect inputs - resolve ForwardReferences at creation time
        resolved_inputs = self.resolved_inputs
        if resolved_inputs:
            for i, connection in enumerate(resolved_inputs):
                # Skip None inputs (for sparse input connections)
                if connection is None:
                    continue

                input_node, output_idx = connection

                try:
                    match input_node:
                        case NodeInstance() as node_instance:
                            # Input is a NodeInstance - create it first
                            # Pass _skip_chain=True to avoid recursion during chain creation
                            input_hou_node = node_instance._create(_skip_chain=True)
                        case ForwardReference() as forward_ref:
                            # Resolve ForwardReference at connection time
                            resolved_node = forward_ref.resolve()
                            input_hou_node = resolved_node._create(_skip_chain=True)
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

    def copy(self,
             /,
             name: str | None = None,
             *,
             _inputs: InputNodes = (),
             _display: bool | None = None,
             _render: bool | None = None,
            **attributes: Any,
            ) -> 'NodeInstance':
        """Return a copy with optional modifications.

        Args:
            _inputs: New input connections (merged with existing)
            name: New name for the node (if provided)
            attributes: Additional/override attributes (merged with existing)
            _display: Override display flag
            _render: Override render flag

        Returns:
            New NodeInstance with merged properties
        """
        return self._copy(
                          name=name,
                          _display=_display,
                          _render=_render,
                          _inputs=_inputs,
                          **attributes
        )


    def _copy(self,
             /,
             name: str | None = None,
             *,
             _inputs: InputNodes = (),
             _display: bool | None = None,
             _render: bool | None = None,
             _chain: 'Chain | None' = None,
             **attributes: Any,
            ) -> 'NodeInstance':
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
            _inputs=tuple(merged_inputs),
            _node=None,  # Copy should not preserve the created node reference
            _display=_display if _display is not None else self._display,
            _render=_render if _render is not None else self._render,
            _chain=_chain,
            attributes=final_attributes,
        )

    def __repr__(self) -> str:
        """Custom repr that avoids circular references from _chain attribute."""
        # Generate input names for display
        input_names = []
        for inp in self._inputs:
            match inp:
                case None:
                    pass
                case NodeInstance() | ForwardReference():
                    input_names.append(node.name)
                case _:
                    input_names.append(f"<output {inp}>")

        inputs_str = f"[{', '.join(input_names)}]" if input_names else "[]"

        return f"NodeInstance(type={self.node_type!r}, name={self.name!r}, inputs={inputs_str})"


@dataclass
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
            self._created_chain = chain(*self._nodes)

            # Now process inputs - DeferredChainPropertyReferences can now resolve
            if self._input is not None:
                # Apply input to the first node (ForwardReferences should resolve now)
                first_node = self._nodes[0]._copy(_inputs=_wrap_inputs(self._input))
                nodes_with_input = [first_node] + self._nodes[1:]
                # Recreate the chain with the connected input
                self._created_chain = chain(*nodes_with_input)

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

    def node(self, node_type: NodeType, /, name: str | None = None, **attributes: Any) -> NodeInstance:
        """Add a node to this chain (not registered with context until chain completes)."""
        # Create node without registering it with the context
        node_instance = NodeInstance(
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
    def inputs(self) -> Inputs:
        """Return the inputs of the first node in the chain."""
        if hasattr(self, '_created_chain') and self._created_chain:
            return self._created_chain.inputs
        elif self._nodes:
            return self._nodes[0].inputs
        else:
            raise RuntimeError("Chain is empty")


@dataclass
class NodeContext:
    """
    A context manager for creating nodes within a specific parent.

    Provides a convenient way to create multiple nodes under the same parent
    without having to specify the parent for each node() call.

    Named nodes can be looked up using dictionary-style access: ctx['name']
    """
    parent: NodeInstance
    _nodes: dict[str, NodeInstance] = field(default_factory=dict, init=False)
    _dependency_registry: weakref.WeakKeyDictionary[NodeInstance, list[NodeInstance]] = field(default_factory=weakref.WeakKeyDictionary, init=False)
    _level: int = field(default=0, init=False)

    def __enter__(self) -> 'NodeContext':
        """Enter the context manager."""
        self._level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager - apply layout and create sink nodes."""
        self._level -= 1
        if self._level > 0:
            return
        if exc_type is None:  # Only if no exception occurred
            # Apply layout to position all nodes
            self.apply_layout()

            # Create all sink nodes (nodes with no dependents)
            sink_nodes = self.get_sink_nodes()
            for node in sink_nodes:
                node.create()

    def _create_forward_reference_for_name(self, name: str) -> ForwardReference:
        """Create a ForwardReference for an unknown string name."""
        return ForwardReference(
            resolution_type='context_lookup',
            context=self,
            name=name
        )

    def node(self,
             node_type: NodeType,
             /,
             name: str | None = None,
             *,
             _input: 'InputNode | Sequence[InputNode] | None' = None,
             _node: 'hou.Node | None' = None,
             _display: bool = False,
             _render: bool = False,
             **attributes: Any
            ) -> NodeInstance:
        """
        Create a node under this context's parent.

        Args:
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
        # Process inputs to handle forward references
        processed_input = self._process_inputs(_input)

        # Create the node using the global node() function
        node_instance = node(
            self.parent,
            node_type,
            name,
            _input=processed_input,
            _node=_node,
            _display=_display,
            _render=_render,
            **attributes
        )

        # Ensure node is registered in dependency registry (even if no dependencies)
        if node_instance not in self._dependency_registry:
            self._dependency_registry[node_instance] = []

        # Register named nodes for lookup
        if name is not None:
            # Check if there was a ForwardReference for this name that needs to be replaced
            old_entry = self._nodes.get(name)
            if isinstance(old_entry, ForwardReference):
                # Replace the ForwardReference with the actual NodeInstance
                # Also update any other references in the context that point to the ForwardReference
                self._replace_forward_reference(old_entry, node_instance)

            self._nodes[name] = node_instance

        # Track dependencies for inputs
        if _input is not None:
            inputs = _input if isinstance(_input, (list, tuple)) else [_input]
            for input_spec in inputs:
                if input_spec is not None:
                    # Resolve the input to a NodeInstance or ForwardReference
                    if isinstance(input_spec, NodeInstance):
                        input_node = input_spec
                    elif isinstance(input_spec, Chain):
                        input_node = input_spec.last
                    elif isinstance(input_spec, ForwardReference):
                        input_node = input_spec
                    else:
                        continue  # Skip other types (hou.Node, str, tuples)

                    # Track the dependency (ForwardReferences are handled in _add_dependency)
                    self._add_dependency(input_node, node_instance)

        return node_instance

    def _process_input(self, input_spec) -> 'InputNode':
        """
        Process an input specification, converting string names to ForwardReferences.

        Args:
            input_spec: The input specification to process

        Returns:
            Processed input spec with ForwardReferences for string names
        """
        if isinstance(input_spec, str):
            # String name - create a forward reference for deferred resolution
            return ForwardReference(
                resolution_type='context_lookup',
                context=self,
                name=input_spec
            )
        return input_spec

    def _process_inputs(self, _input):
        """
        Process input specifications, converting unknown string names to ForwardReferences.

        Args:
            _input: The input specification(s) to process

        Returns:
            Processed input specs with ForwardReferences for unknown string names
        """
        if _input is None:
            return None

        if isinstance(_input, (list, tuple)) and not isinstance(_input, str):
            # Process each item in the sequence, but be careful about tuples that are (node, index) pairs
            if (len(_input) == 2 and
                not isinstance(_input[0], (list, tuple)) and
                isinstance(_input[1], int)):
                # This looks like a (node_spec, output_index) tuple
                node_spec, output_idx = _input
                processed_node_spec = self._process_input(node_spec)
                return (processed_node_spec, output_idx)
            else:
                # This is a sequence of inputs
                return [self._process_input(inp) for inp in _input]
        else:
            # Single input specification
            return self._process_input(_input)

    def __getitem__(self, name: str) -> NodeInstance:
        """Look up a named node created in this context."""
        if name not in self._nodes:
            raise KeyError(f"No node named '{name}' found in this context")
        return self._nodes[name]

    def context(self, node_or_path: NodeInstance | str | hou.Node | None = None) -> 'NodeContext':
        """
        Create a new context for layout purposes.

        This method creates a logical grouping context for nodes. The exact behavior
        is implementation-defined and may evolve in future versions (e.g., to support
        network boxes, nested layouts, or other organizational features).

        Current behavior: Returns self, meaning nodes are created in the same context
        but the syntax allows for clearer organization of code that logically groups
        related nodes.

        Args:
            node_or_path: Context specification (behavior is implementation-defined)

        Returns:
            A NodeContext for creating and organizing nodes (currently self)

        Usage:
            with global_ctx.context() as ctx:
                # Creates nodes with logical grouping
                ctx.node("topnet", "my_network")

        Example with nested organization:
            with context("/obj") as obj_ctx:
                with obj_ctx.context(node("/obj", "topnet", name="demo1")) as top_ctx:
                    # All nodes created here are organized under demo1
                    top_ctx.node("pythonscript", "task1")
        """
        return self

    def chain(self, *, _input: 'InputNode | Sequence[InputNode] | None' = None, **attributes: Any) -> 'ChainBuilder':
        """
        Create a ChainBuilder context manager for building chains.

        Args:
            _input: Optional input node(s) to connect to the first node in the chain
            **attributes: Additional attributes (currently unused, for future compatibility)

        Returns:
            ChainBuilder context manager for building chains

        Usage:
            # Context manager style
            with ctx.chain(_input=source) as c:
                c.node("xform", "path_a")
                c.node("subdivide", "path_b")

        Note:
            - After exiting the context, any named nodes in the result will be registered
            - Use the ChainBuilder.node() method to add nodes to the chain
        """
        # Process inputs to handle forward references
        processed_input = self._process_inputs(_input)
        return ChainBuilder(self, processed_input)

    def merge(self, *inputs: InstanceNodeSpec,
              name: str | None = None,
              **attributes: Any) -> NodeInstance:
        """
        Create a merge node with multiple inputs.

        Args:
            *inputs: Input nodes to merge
            name: Optional name for the merge node
            **attributes: Additional merge node parameters

        Returns:
            NodeInstance for the merge node
        """
        if not inputs:
            raise ValueError("merge() requires at least one input")

        return self.node("merge", name, _input=list(inputs), **attributes)

    def _replace_forward_reference(self,
                                   forward_ref: ForwardReference,
                                   actual_node: NodeInstance,
                                   ) -> None:
        """Replace all occurrences of a ForwardReference with the actual NodeInstance."""
        # Check all nodes in the registry for inputs that reference the ForwardReference
        for node in self._dependency_registry:
            if hasattr(node, '_inputs'):
                # Check if any inputs contain the ForwardReference and replace them
                updated_inputs = []
                needs_update = False
                for inp in node._inputs:
                    if inp is forward_ref:
                        updated_inputs.append(actual_node)
                        needs_update = True
                    else:
                        updated_inputs.append(inp)

                if needs_update:
                    # Update the node's inputs - we need to create a new NodeInstance with updated inputs
                    # This is tricky because NodeInstance is frozen, so we'd need to recreate it
                    # For now, let's just note that this forward reference has been resolved
                    pass

        # Note: The above is complex because NodeInstance is frozen.
        # The key insight is that ForwardReferences should be resolved during create() time,
        # not stored in the context permanently.

    def _add_dependency(self, input_node: 'NodeInstance | ForwardReference', dependent_node: NodeInstance) -> None:
        """Add a dependency relationship: dependent_node depends on input_node."""
        if isinstance(input_node, ForwardReference):
            # Skip dependency tracking for ForwardReferences at definition time
            # Dependencies will be resolved and tracked at create time
            return

        if input_node not in self._dependency_registry:
            self._dependency_registry[input_node] = []
        if dependent_node not in self._dependency_registry[input_node]:
            self._dependency_registry[input_node].append(dependent_node)

    def _remove_dependency(self, input_node: NodeInstance, dependent_node: NodeInstance) -> None:
        """Remove a dependency relationship."""
        if input_node in self._dependency_registry:
            try:
                self._dependency_registry[input_node].remove(dependent_node)
                # Clean up empty lists
                if not self._dependency_registry[input_node]:
                    del self._dependency_registry[input_node]
            except ValueError:
                pass  # Dependency wasn't there

    def get_dependents(self, node: NodeInstance) -> list[NodeInstance]:
        """Get list of nodes that depend on the given node."""
        return list(self._dependency_registry.get(node, []))

    def get_source_nodes(self) -> list[NodeInstance]:
        """Get nodes in this context that have no inputs (source nodes).

        Returns:
            List of all context nodes (named and unnamed) that have no input connections
        """
        return [node for node in self._dependency_registry.keys() if not node.inputs or all(inp is None for inp in node.inputs)]

    def get_sink_nodes(self) -> list[NodeInstance]:
        """Get nodes in this context that have no dependents (sink nodes).

        Returns:
            List of all context nodes (named and unnamed) that no other nodes depend on
        """
        return [node for node in self._dependency_registry.keys() if not self.get_dependents(node)]

    def _get_lowest_existing_node_position(self) -> float:
        """Get the Y position to start layout below existing nodes in parent.

        Returns:
            Y offset to position new nodes below existing ones (0 if no existing nodes)
        """
        try:
            # Ensure parent exists before checking for existing nodes
            parent_hou_node = self.parent.create()
            if parent_hou_node is None:
                return 0.0

            # Get all existing nodes in parent (including schedulers via allSubChildren)
            existing_nodes = parent_hou_node.allSubChildren()
            if not existing_nodes:
                return 0.0

            # Find the lowest Y position among existing nodes
            lowest_y = min(node.position()[1] for node in existing_nodes)

            # Start our nodes 3 units below the lowest existing node
            return lowest_y - 3.0

        except Exception:
            # If anything fails, start at 0
            return 0.0

    def layout_nodes(self, layer_height: float = 2.0, node_width: float = 2.0, min_spacing: float = 0.5) -> dict[NodeInstance, tuple[float, float]]:
        """Compute optimal layout positions for all nodes in the context.

        Uses a topological layering approach:
        1. Start with source nodes (no inputs) at the top layer
        2. Position each subsequent layer below based on dependencies
        3. Center nodes between their inputs when possible
        4. Allocate space based on output fanout, propagating upward
        5. Resolve conflicts by adding space at each layer

        For TOP networks, checks for existing nodes (like schedulers) and positions
        our nodes below them to avoid conflicts.

        Args:
            layer_height: Vertical spacing between layers
            node_width: Estimated width of each node for spacing calculations
            min_spacing: Minimum horizontal spacing between nodes

        Returns:
            Dictionary mapping NodeInstance to (x, y) position tuples
        """
        all_nodes = list(self._dependency_registry.keys())
        if not all_nodes:
            return {}

        # Calculate Y offset once at the start for consistency
        y_offset = self._get_lowest_existing_node_position()

        # Step 1: Compute topological layers
        layers = self._compute_layers(all_nodes)

        # Step 2: Compute space requirements (bottom-up)
        space_requirements = self._compute_space_requirements(layers, node_width, min_spacing)

        # Step 3: Position nodes within each layer
        positions = self._position_nodes_in_layers(layers, space_requirements, layer_height, node_width, min_spacing, y_offset)

        return positions

    def _compute_layers(self, all_nodes: list[NodeInstance]) -> dict[int, list[NodeInstance]]:
        """Compute vertical layers using proper top-down traversal."""
        node_depths: dict[NodeInstance, int] = {}

        # Get actual source nodes (no inputs within our context)
        source_nodes = []
        for node in all_nodes:
            has_inputs_in_context = any(
                inp is not None and inp[0] in all_nodes
                for inp in node.inputs
            )
            if not has_inputs_in_context:
                source_nodes.append(node)

        # Top-down traversal to assign depths
        def assign_depth(node: NodeInstance, depth: int) -> None:
            # Update depth if this path is deeper
            if node in node_depths:
                if depth > node_depths[node]:
                    node_depths[node] = depth
                else:
                    return  # Already processed with equal or deeper path
            else:
                node_depths[node] = depth

            # Process all dependents with updated depth
            dependents = self.get_dependents(node)
            for dependent in dependents:
                if dependent in all_nodes:
                    assign_depth(dependent, depth + 1)

        # Start from source nodes at depth 0
        for source in source_nodes:
            assign_depth(source, 0)

        # Handle any remaining unprocessed nodes (shouldn't happen in a proper DAG)
        for node in all_nodes:
            if node not in node_depths:
                # Fallback: assign based on input depths
                input_nodes = [
                    inp[0] for inp in node.inputs
                    if inp is not None and inp[0] in all_nodes
                ]
                if input_nodes:
                    # Resolve ForwardReferences for depth calculation
                    resolved_nodes = []
                    for inp in input_nodes:
                        if isinstance(inp, ForwardReference):
                            resolved_nodes.append(inp.resolve())
                        else:
                            resolved_nodes.append(inp)
                    max_input_depth = max(node_depths.get(inp, 0) for inp in resolved_nodes)
                    node_depths[node] = max_input_depth + 1
                else:
                    node_depths[node] = 0

        # Move all sink nodes to a common bottom layer
        sink_nodes = self.get_sink_nodes()
        if sink_nodes:
            max_depth = max(node_depths.values())
            sink_depth = max_depth + 1
            for sink in sink_nodes:
                if sink in all_nodes:
                    node_depths[sink] = sink_depth

        # Create contiguous layer mapping (0, 1, 2, ...) from potentially sparse depths
        unique_depths = sorted(set(node_depths.values()))
        depth_to_layer = {depth: idx for idx, depth in enumerate(unique_depths)}

        # Group nodes by contiguous layer indices
        layers: dict[int, list[NodeInstance]] = {}
        for node, depth in node_depths.items():
            layer_idx = depth_to_layer[depth]
            if layer_idx not in layers:
                layers[layer_idx] = []
            layers[layer_idx].append(node)

        return layers

    def _compute_space_requirements(self, layers: dict[int, list[NodeInstance]],
                                   node_width: float, min_spacing: float) -> dict[NodeInstance, float]:
        """Compute space requirements for each node based on output fanout."""
        space_requirements: dict[NodeInstance, float] = {}
        max_layer = max(layers.keys()) if layers else 0

        # Start from bottom layer and work upward
        for layer_idx in range(max_layer, -1, -1):
            layer_nodes = layers[layer_idx]

            for node in layer_nodes:
                dependents = self.get_dependents(node)

                if not dependents:
                    # Sink node - use minimum space
                    space_requirements[node] = node_width + min_spacing
                else:
                    # Space is sum of dependent space requirements
                    dependent_space = sum(
                        space_requirements.get(dep, node_width + min_spacing)
                        for dep in dependents
                    )
                    space_requirements[node] = max(dependent_space, node_width + min_spacing)

        return space_requirements

    def _position_nodes_in_layers(self, layers: dict[int, list[NodeInstance]],
                                 space_requirements: dict[NodeInstance, float],
                                 layer_height: float, node_width: float,
                                 min_spacing: float, y_offset: float) -> dict[NodeInstance, tuple[float, float]]:
        """Position nodes using bidirectional layout algorithm.

        Args:
            layers: Nodes organized by layer depth
            space_requirements: Horizontal space needed for each node
            layer_height: Vertical spacing between layers
            node_width: Width of each node
            min_spacing: Minimum horizontal spacing
            y_offset: Vertical offset to position below existing nodes
        """

        # Step 1: Upward pass - compute required horizontal space for each node
        # based on outputs that need to be positioned below it
        node_required_width: dict[NodeInstance, float] = {}

        # Process layers from bottom (sinks) to top (sources)
        for layer_idx in sorted(layers.keys(), reverse=True):
            layer_nodes = layers[layer_idx]

            for node in layer_nodes:
                # Find all outputs (nodes that depend on this node)
                outputs = self.get_dependents(node)

                if not outputs:
                    # Sink node: only needs its own space
                    node_required_width[node] = space_requirements[node]
                else:
                    # Sum the required width of all direct outputs
                    total_output_width = sum(node_required_width[output] for output in outputs)
                    # Node needs at least its own width or the sum of its outputs
                    node_required_width[node] = max(space_requirements[node], total_output_width)

        # Step 2: Downward pass - position nodes based on allocated space
        positions: dict[NodeInstance, tuple[float, float]] = {}

        # Start with top layer (sources)
        min_layer = min(layers.keys())
        source_nodes = layers[min_layer]
        y_pos = y_offset + (-min_layer * layer_height)

        # Position sources to use their required width
        total_width = sum(node_required_width[node] for node in source_nodes)
        current_x = -total_width / 2

        for node in source_nodes:
            allocated_width = node_required_width[node]
            x_pos = current_x + allocated_width / 2
            positions[node] = (x_pos, y_pos)
            current_x += allocated_width

        # Position remaining layers
        for layer_idx in sorted(layers.keys())[1:]:
            layer_nodes = layers[layer_idx]
            y_pos = y_offset + (-layer_idx * layer_height)

            # Group nodes by their inputs to distribute within input spans
            input_groups: dict[tuple[NodeInstance, ...], list[NodeInstance]] = {}

            for node in layer_nodes:
                # Resolve ForwardReferences in inputs before grouping
                resolved_inputs = []
                for inp in node.inputs:
                    if inp is not None:
                        input_node = inp[0]
                        if isinstance(input_node, ForwardReference):
                            resolved_inputs.append(input_node.resolve())
                        else:
                            resolved_inputs.append(input_node)
                input_nodes = tuple(resolved_inputs)
                if input_nodes not in input_groups:
                    input_groups[input_nodes] = []
                input_groups[input_nodes].append(node)

            # Position each group within its input span
            for input_nodes, group_nodes in input_groups.items():
                if not input_nodes:
                    # No inputs - center at origin
                    available_center = 0.0
                    available_width = sum(node_required_width[node] for node in group_nodes)
                else:
                    # Calculate span from leftmost to rightmost input
                    # Resolve ForwardReferences for layout calculations
                    resolved_input_nodes = []
                    for inp in input_nodes:
                        if isinstance(inp, ForwardReference):
                            resolved_inp = inp.resolve()
                            resolved_input_nodes.append(resolved_inp)
                        else:
                            resolved_input_nodes.append(inp)
                    input_positions = [positions[inp][0] for inp in resolved_input_nodes]
                    input_widths = [node_required_width[inp] for inp in resolved_input_nodes]

                    # Find the allocated span
                    leftmost = min(pos - width/2 for pos, width in zip(input_positions, input_widths))
                    rightmost = max(pos + width/2 for pos, width in zip(input_positions, input_widths))
                    available_width = rightmost - leftmost
                    available_center = (leftmost + rightmost) / 2

                # Distribute group nodes within the available span
                group_total_width = sum(node_required_width[node] for node in group_nodes)

                if group_total_width <= available_width:
                    # Nodes fit - center them within available space
                    start_x = available_center - group_total_width / 2
                else:
                    # Nodes exceed space - pack them tightly
                    # currently the same as above, but could be modified to add extra spacing if desired
                    start_x = available_center - group_total_width / 2

                current_x = start_x
                for node in group_nodes:
                    allocated_width = node_required_width[node]
                    x_pos = current_x + allocated_width / 2
                    positions[node] = (x_pos, y_pos)
                    current_x += allocated_width

        return positions


    def apply_layout(self, **layout_kwargs) -> None:
        """Compute and apply layout positions to all created nodes.

        Args:
            **layout_kwargs: Arguments passed to layout_nodes()
        """
        positions = self.layout_nodes(**layout_kwargs)

        for node, (x, y) in positions.items():
            # Create the node first to get the hou.Node
            hou_node = node.create()

            # Set the position
            try:
                hou_node.setPosition((x, y))
            except Exception as e:
                print(f"Warning: Failed to set position for {node}: {e}")


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

    def copy(self, *copy_params: ChainCopyParam, _inputs: InputNodes=()) -> 'Chain':  # type: ignore[override]
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
                param if isinstance(param, NodeInstance) else self[param]
                for param in copy_params
                ]
        )

        if not new_nodes:
            raise ValueError("Chain copy must result in at least one node")

        # Handle inputs for first node
        inputs = _wrap_inputs(_inputs)
        self_inputs: Inputs = ()
        if self.nodes and new_nodes:
            if copy_params:
                # Get inputs from the original first node being copied
                first_param = copy_params[0]
                if not isinstance(first_param, NodeInstance):
                    # It's an int or str - get the original node's inputs
                    original_first = self[first_param]
                    self_inputs = original_first.inputs
            else:
                # Default copy: preserve first node's inputs
                self_inputs = self.nodes[0].inputs

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
    /,
    name: str | None = None,
    *,
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

    # Validate that all nodes have the same parent
    if flattened_nodes:
        first_parent = flattened_nodes[0].parent
        for i, node in enumerate(flattened_nodes[1:], 1):
            if node.parent != first_parent:
                raise ValueError(
                    f"All chain nodes must have same parent. "
                    f"Node 0 has parent {first_parent}, node {i} has parent {node.parent}"
                )

    return Chain(
        nodes=flattened_nodes,  # Only NodeInstance objects now
    )


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


def context(parent: NodeParent) -> NodeContext:
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
    parent_instance = wrap_node(parent) if not isinstance(parent, NodeInstance) else parent
    return NodeContext(parent=parent_instance)


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
        case NodeInstance()|Chain()|hou.Node()|str()|ForwardReference() as input, int() as idx:
            resolved = _wrap_input(input, idx)
            return (resolved,)
        case NodeInstance()|Chain()|hou.Node()|str()|ForwardReference() as input:
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
    def _wrap_single_input(input: InputNodeSpec) -> NodeInstance|ForwardReference|None:
        """Wrap a single input node specification."""
        match input:
            case NodeInstance():
                return input
            case Chain() if len(input.nodes) == 0:
                return None
            case Chain():
                return input.last
            case ChainBuilder():
                # Use .last - may return a ForwardReference if chain isn't complete
                return input.last
            case hou.Node():
                return wrap_node(input)
            case str():
                return wrap_node(hou_node(input))
            case ForwardReference():
                # Don't resolve - just pass through as-is for later resolution
                return input
            case _:
                raise TypeError(f"Invalid input specification: {input}. Expected NodeInstance, Chain, ChainBuilder, hou.Node, str, or ForwardReference.")

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
        case NodeInstance() | Chain() | ChainBuilder() | hou.Node() | str() | ForwardReference():
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
