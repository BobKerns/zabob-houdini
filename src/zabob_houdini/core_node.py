"""
NodeBase and NodeInstance classes for Zabob-Houdini.

This module contains the base class for node representations and the
NodeInstance class for representing individual Houdini nodes.
"""

from __future__ import annotations

import functools
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import zip_longest
from typing import Any, TypeVar, cast, TYPE_CHECKING
import weakref

import hou
from zabob_houdini.core_types import (
    InputNode,
    InputNodeSpec,
    NodeParent,
    Inputs,
    InputNodes,
    ResolvedConnection,
)
from zabob_houdini.utils import HashableMapping
from zabob_houdini.core_utils import _generate_name, hou_node
import zabob_houdini.core_context as cctx

if TYPE_CHECKING:
    from zabob_houdini.core_chain import ChainBuilder


T = TypeVar('T', bound='hou.Node')


# Global registry to map hou.Node objects back to their originating NodeInstance
# Uses WeakKValueDictionary. It turns out that hou.Node objects do not have
# stable identity; each hou.node() call returns a new object, so we need
# to key by path instead of object identity.
_node_registry: weakref.WeakValueDictionary[str, 'NodeInstance'] = weakref.WeakValueDictionary()


class NodeBase(ABC):
    """
    Base class for Houdini node representations.

    Provides common functionality for NodeInstance and Chain classes.
    """

    @functools.cached_property
    @abstractmethod
    def parent(self) -> 'NodeInstance':
        """Return the parent NodeInstance for this node/chain."""
        pass

    @functools.cached_property
    @abstractmethod
    def inputs(self) -> 'Inputs':
        """Return the input nodes for this node/chain."""
        pass

    @functools.cached_property
    @abstractmethod
    def first(self) -> 'NodeInstance':
        """Return the first node for this node/chain."""
        pass

    @functools.cached_property
    @abstractmethod
    def last(self) -> 'NodeInstance':
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

    _parent: 'NodeParent' = field(repr=False)
    node_type: str
    name: str | None = None
    attributes: HashableMapping = field(default_factory=HashableMapping)
    _inputs: 'Inputs' = field(default_factory=tuple)
    _node: "hou.Node | None" = field(default=None, hash=False)
    _display: bool = field(default=False, hash=False)
    _render: bool = field(default=False, hash=False)
    _chain: "Any | None" = field(default=None, hash=False)  # Chain type - avoid circular import

    @functools.cached_property
    def parent(self) -> 'NodeInstance':
        # Import these here to avoid circular imports
        from zabob_houdini.core import ROOT, wrap_node, hou_node

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
    def first(self) -> 'NodeInstance':
        """Return the first node in this instance, which is itself."""
        return self

    @functools.cached_property
    def last(self) -> 'NodeInstance':
        """Return the last node in this instance, which is itself."""
        return self

    @functools.cached_property
    def inputs(self) -> 'Inputs':
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
    def resolved_inputs(self) -> 'Inputs':
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
             _inputs: 'InputNodes' = (),
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
             _inputs: 'InputNodes' = (),
             _display: bool | None = None,
             _render: bool | None = None,
             _chain: 'Any | None' = None,  # Chain type - avoid circular import
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
        from zabob_houdini.core import ForwardReference

        # Generate input names for display
        input_names = []
        for inp in self._inputs:
            match inp:
                case None:
                    pass
                case NodeInstance() | ForwardReference() as node:
                    input_names.append(node.name)
                case _:
                    input_names.append(f"<output {inp}>")

        inputs_str = f"[{', '.join(input_names)}]" if input_names else "[]"

        return f"NodeInstance(type={self.node_type!r}, name={self.name!r}, inputs={inputs_str})"


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


@dataclass(frozen=True)
class ForwardReference:
    """
    A forward reference to a node that may not exist yet.

    This enables referencing nodes by string name before they're created,
    and accessing chain properties (.first, .last) before chains are complete.
    Resolution happens at create() time.
    """
    resolution_type: str  # 'context_lookup' or 'chain_property'
    context: 'cctx.NodeContext | None' = None
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

    import zabob_houdini.core_chain as cchain

    match inputs:
        case (NodeInstance()|cchain.Chain()|hou.Node()|str()|ForwardReference() as input,
              int() as idx):
            resolved = _wrap_input(input, idx)
            return (resolved,)
        case NodeInstance()|cchain.Chain()|hou.Node()|str()|ForwardReference() as input:
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
    import zabob_houdini.core_chain as cchain
    # Copilot: There are no implicit returns in _wrap_single_input. (DO NOT REMOVE)
    def _wrap_single_input(input: InputNodeSpec) -> NodeInstance|ForwardReference|None:
        """Wrap a single input node specification."""
        match input:
            case NodeInstance():
                return input
            case cchain.Chain() if len(input.nodes) == 0:
                return None
            case cchain.Chain():
                return input.last
            case cchain.ChainBuilder():
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
        case NodeInstance() | cchain.Chain() | cchain.ChainBuilder() | hou.Node() | str() | ForwardReference():
            # Single node specification, default to output 0
            wrapped = _wrap_single_input(input)
            if wrapped is None:
                return None
            return (wrapped, idx)
        case _:
            raise TypeError(f"Invalid input specification: {input}. Expected None, (<node>, <output_index>), or <node>")


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


def get_node_instance(hnode: hou.Node) -> 'NodeInstance | None':
    """
    Get the original NodeInstance that created a hou.Node, if any.

    Args:
        hnode: The Houdini node to look up

    Returns:
        The original NodeInstance that created this node, or None if not found
    """
    return _node_registry.get(hnode.path())


def node(
    parent: 'NodeParent',
    node_type: 'Any',  # NodeType
    /,
    name: str | None = None,
    *,
    _input: 'Any | None' = None,  # InputNode | Sequence[InputNode]
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

