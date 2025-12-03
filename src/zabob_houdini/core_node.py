"""
NodeBase and NodeInstance classes for Zabob-Houdini.

This module contains the base class for node representations and the
NodeInstance class for representing individual Houdini nodes.
"""

from __future__ import annotations, _dynamic_import # noqa: F407 E261 # type: ignore

import functools
from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import zip_longest
import sys
from typing import Any, Generic, Self, TypeVar, cast, TYPE_CHECKING, overload
import weakref

import hou

from zabob_houdini.core_types import (
    NativeParmData,
    RawInput,
    RawInputs,
    UnresolvedConnection,
    UnresolvedConnections,
    ResolvedConnection,
    ResolvedConnections,
    T_Node,
)
from zabob_houdini.utils import HashableMapping
from zabob_houdini.core_utils import hou_node
import zabob_houdini.core_chain as cchain

if TYPE_CHECKING:
    from zabob_houdini.core_chain import Chain
    import zabob_houdini.core_context as cctx
else:
    import zabob_houdini.core_context as cctx

T = TypeVar('T', bound='hou.Node')
AS = TypeVar('AS', bound='NodeInstance | hou.Node')


# Global registry to map hou.Node objects back to their originating NodeInstance
# Uses WeakKValueDictionary. It turns out that hou.Node objects do not have
# stable identity; each hou.node() call returns a new object, so we need
# to key by path instead of object identity.
_node_registry: weakref.WeakValueDictionary[str, 'NodeBase'] = weakref.WeakValueDictionary()


@dataclass(frozen=True, eq=False)
class NodeBase(Generic[T_Node]):
    """
    Base class for Houdini node representations.

    Provides common functionality for NodeInstance and Chain classes.
    """

    _parent: 'NodeInstance' = field(repr=False)

    @property
    def parent(self) -> 'NodeInstance':
        """Return the parent NodeInstance for this node/chain."""
        return self._parent

    name: str

    @property
    def inputs(self) -> 'UnresolvedConnections':
        """Return the input nodes for this node/chain."""
        return ()

    @functools.cached_property
    def resolved_inputs(self) -> 'ResolvedConnections':
        """Return the resolved input nodes for this node/chain."""
        return tuple(
            (node.resolved, idx)
            if node
            else NO_CONNECTION
            for node, idx in self.inputs
        )

    @property
    def first(self) -> 'NodeBase':
        """Return the first node for this node/chain."""
        return self

    @property
    def last(self) -> 'NodeBase':
        """Return the last node for this node/chain."""
        return self

    def resolve(self) -> 'NodeInstance | None':
        """
        Resolve this node to a NodeInstance, if possible.

        Returns: NodeInstance | None
        """
        return None

    @property
    def resolved(self) -> 'NodeInstance':
        """Return the resolved NodeInstance for this node/chain, if possible.

        Raises RuntimeError if the node cannot be resolved.
        """
        resolved = self.resolve()
        if resolved is None:
            raise RuntimeError(f"Failed to resolve node: {self}")
        return resolved

    @property
    def node(self) -> hou.Node:
        """Return the actual Houdini node.

        Raises RuntimeError if the node cannot be resolved.
        """
        return self.resolved.create()

    def as_node(self, as_type: type[T] = hou.Node) -> T:
        """
        Returns the actual Houdini node.

        Args:
            as_type: Expected node type to narrow the return type to (e.g., hou.SopNode).
                    Defaults to hou.Node for maximum compatibility.

        Returns:
            The created Houdini node object, cast to the specified type.
        """
        return self.resolved.create(as_type)

    def copy(self, /,
             name: str | None = None, *,
             _display: bool | None = None,
             _render: bool | None = None,
             _inputs: 'RawInputs | None' = None,
             **kwargs: NativeParmData) -> Self:
        """Return a copy with optional modifications."""
        return self._copy(
            name=name,
            _display=_display,
            _render=_render,
            _chain=None,
            _inputs=_inputs,
            **kwargs
        )

    def _copy(self, /,
              name: str | None = None, *,
              _chain: 'Chain | None' = None,
              _inputs: 'RawInputs|None' = None,
              _display: bool | None = None,
              _render: bool | None = None,
              **kwargs: NativeParmData,
              ) -> Self:
        """Return a copy with optional modifications."""
        raise NotImplementedError(f"Copy not implemented for {type(self).__name__}")

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

    node_type: str
    attributes: HashableMapping = field(default_factory=HashableMapping)
    _inputs: 'UnresolvedConnections' = field(default_factory=tuple, repr=False)
    _node: "hou.Node | None" = field(default=None, hash=False)
    _display: bool = field(default=False, hash=False)
    _render: bool = field(default=False, hash=False)
    _chain: "Chain | None" = None

    @property
    def parent(self) -> 'NodeInstance':
        # Import this here to avoid circular imports
        from zabob_houdini.core import ROOT

        if self is ROOT:
            return self
        return self._parent

    @property
    def inputs(self) -> 'UnresolvedConnections':
        return self._inputs

    @overload
    def create(self, as_type: type[T]) -> T: ...

    @overload
    def create(self) -> hou.Node: ...

    def create(self, as_type: type[T] = hou.Node) -> T:
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
        The caching is essential to avoid recursion and duplicate nodes.
        '''

        # Don't create the parent if we've been supplied _node.
        #
        # Or we'll get infinite recursion at the root.
        if self._node is not None:
            # Use existing node if provided
            return self._node
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
                raise RuntimeError(
                    f"Invalid node type '{self.node_type}' for node '{name}' "
                    f"in {parent_type} ({parent_path}): {error_msg}"
                )

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
                        print(f"Warning: Failed to set parameters on {node_type} node '{node_name}' ({node_path}): {e}",
                              file=sys.stderr)
                        print(f"  Attempted parameters: {dict(self.attributes)}",
                              file=sys.stderr)
                        # Try to identify which parameters are invalid
                        valid_parms = {parm.name() for parm in created_node.parms()}
                        invalid_parms = set(self.attributes.keys()) - valid_parms
                        if invalid_parms:
                            print(f"  Invalid parameters for {node_type}: {invalid_parms}", file=sys.stderr)
                        print(f"  Valid parameters for {node_type}: {sorted(valid_parms)}", file=sys.stderr)
                case _:
                    print(
                        f"Warning: Cannot set parameters on node type "
                        f"{created_node.type().name()} - skipping attributes",
                        file=sys.stderr
                    )
        _node_registry[created_node.path()] = self
        return created_node

    def _connect_inputs(self) -> hou.Node:
        """Connect inputs - resolve ForwardReferences at creation time"""
        created_node = self._do_create()
        for i, (input_node, output_idx) in enumerate(self.resolved_inputs):
            try:
                match input_node:
                    case NodeInstance() as node_instance:
                        # Input is a NodeInstance - create it first
                        # Pass _skip_chain=True to avoid recursion during chain creation
                        input_hou_node = node_instance._create(_skip_chain=True)
                        created_node.setInput(i, input_hou_node, output_idx)
                    case None:
                        pass
                    case _:
                        raise TypeError(
                            f"Input {i} must be a NodeInstance, Chain, or Houdini node object, "
                            f"got {type(input_node).__name__}"
                        )
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

        # Register this NodeInstance under the full path.
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

    def as_type(self, cls: type[AS]) -> AS:
        """
        Narrow the type of a node to the specified type if possible.
        type can be any subtype of hou.Node or NodeInstance.

        Throws a TypeError if the node cannot be cast to the specified type.
        """
        if issubclass(cls, NodeInstance):
            resolved = self.resolve()
            if resolved is None:
                raise TypeError(f"Cannot resolve NodeInstance to {cls.__name__}")
            if isinstance(resolved, cls):
                return cast(AS, resolved)
            raise TypeError(f"Cannot convert NodeInstance to {cls.__name__}")
        elif issubclass(cls, hou.Node):
            if isinstance(self, NodeInstance):
                return cast(AS, self._do_create())
                raise TypeError(f"Cannot convert NodeInstance to {cls.__name__}")
            return self._asType(self._do_create(), cls)
        node = self.create()
        return self._asType(node, cls)

    @functools.cached_property
    def path(self) -> str:
        """Return the path of the node."""
        if self._node is not None:
            return self._node.path()
        else:
            return f'{self.parent.path}/{self.name or self.node_type}'

    def resolve(self) -> 'NodeInstance':
        """
        Resolve this node to a NodeInstance, if possible.

        Returns: NodeInstance | None
        """
        return self

    def copy(self, /,
             name: str | None = None, *,
             _inputs: 'RawInputs | None' = None,
             _input: 'RawInput | None' = None,
             _display: bool | None = None,
             _render: bool | None = None,
             **attributes: NativeParmData,
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
        _inputs = _inputs or _input
        inputs = _wrap_inputs(_inputs)
        inputs = _merge_inputs(inputs, self.inputs)
        return self._copy(
                          name=name,
                          _display=_display,
                          _render=_render,
                          _inputs=inputs,
                          _chain=None,
                          **attributes
        )

    def _copy(self, /,
              name: str | None = None, *,
              _inputs: 'RawInputs|None' = None,
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
        """
        Custom repr that avoids circular references from _chain or _inputs.
        """
        # Generate input names for display
        def input_name(inp: UnresolvedConnection) -> str:
            node, idx = inp
            if node is None:
                return f"<input {idx}>"
            return f"{node.name}[{idx}]"
        inputs_str = ', '.join(
            input_name(inp)
            for inp in self._inputs
        )
        return f"NodeInstance(type={self.node_type!r}, name={self.name!r}, inputs=({inputs_str})"


class ImmediateNode(NodeInstance):
    """
    A NodeInstance that wraps an existing hou.Node.

    This is used the standalone `node` function is called without a context.
    Inputs are set immediately on creation.
    """

    def create(self, as_type: type[T] = hou.Node) -> T:
        """Return the existing hou.Node, connecting inputs as needed."""
        if self._node is not None:
            self._connect_inputs()
            return self._asType(self._node, as_type)
        else:
            node = self._do_create()
            self._connect_inputs()
        return self._asType(node, as_type)


def _wrap_hou_node(hnode: hou.Node) -> 'NodeBase':
    """
    Wrap a hou.Node in a NodeInstance, checking the global registry first.

    If the hou.Node was originally created by a NodeInstance, returns that original.
    Otherwise, creates a new NodeInstance wrapper.

    Args:
        hnode: The Houdini node to wrap

    Returns:
        NodeInstance object (either original or newly created wrapper)
    """
    # Check if we already have this node in our registry
    path = hnode.path()
    if path in _node_registry:
        return _node_registry[path]

    node_name = path.split('/')[-1]
    parent_node = hnode.parent()

    wrapped = NodeInstance(
        _parent=wrap_node(parent_node),
        node_type=hnode.type().name(),
        name=node_name,
        _node=hnode,
    )

    # Register this wrapper in case it gets referenced again
    _node_registry[hnode.path()] = wrapped
    _node_registry[hnode.name()] = wrapped

    return wrapped


def _attribute_dict() -> HashableMapping[str, NativeParmData]:
    """Convert a HashableMapping of attributes to a regular dict."""
    return cast(HashableMapping[str, NativeParmData], HashableMapping({}))


@dataclass(frozen=True, eq=False)
class ForwardReference(NodeBase):
    """
    A forward reference to a node that may not exist yet.

    This enables referencing nodes by string name before they're created,
    and accessing chain properties (.first, .last) before chains are complete.
    Resolution happens at create() time.
    """
    context: 'cctx.NodeContext'
    name: str

    def __post_init__(self):
        """Register for resolution on context exit"""
        self.context.pending.append(self)

    def resolve(self) -> 'NodeInstance | None':
        """
        Resolve the forward reference to an actual NodeInstance.
        Returns `None` if the reference cannot be resolved at
        this time.

        Returns: NodeInstance | None
        """
        # Try to resolve the reference from the context
        current = self.context.get(self.name)
        if isinstance(current, NodeInstance):
            return current
        return None

    def _copy(self, /,
              name: str | None = None, *,
              _inputs: 'RawInputs|None' = None,
              _display: bool | None = None,
              _render: bool | None = None,
              _chain: 'Chain | None' = None,
              **kwargs: NativeParmData) -> 'CopyReference':
        """Return a copy with optional modifications."""
        inputs = _wrap_inputs(_inputs) if _inputs is not None else ()
        return CopyReference(
            _parent=self.parent,
            context=self.context,
            name=name if name is not None else self.name,
            _inputs=inputs,
            attributes=HashableMapping(kwargs),
            copy_of=self,
        )

    def __str__(self) -> str:
        return f"ForwardRef(name='{self.name}')"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass(frozen=True, eq=False)
class CopyReference(ForwardReference):
    """
    A forward reference to a node that may not exist yet, with the intention to copy it.

    Used when .copy() is called on a ForwardReference before it resolves. The copy
    operation is deferred until the original reference resolves, then the resolved
    node is copied with any specified modifications.

    Resolution happens at create() time.
    """
    copy_of: ForwardReference
    attributes: HashableMapping[str, NativeParmData] = field(default_factory=_attribute_dict)
    _inputs: 'UnresolvedConnections' = field(default_factory=tuple)

    def resolve(self) -> 'NodeInstance | None':
        """
        Resolve the forward reference to an actual NodeInstance.
        Returns `None` if the reference cannot be resolved at
        this time.

        Returns: NodeInstance | None
        """
        if self.copy_of is None:
            return super().resolve()

        original = self.copy_of.resolve()
        if original is None:
            return None
        return original.copy(name=self.name,
                             _inputs=self._inputs,
                             **self.attributes)

    def copy(self, /,
             name: str | None = None, *,
             _inputs: 'RawInputs|None' = None,
             **kwargs: NativeParmData) -> 'CopyReference':
        """Return a copy with optional modifications."""
        our_inputs = _wrap_inputs(_inputs) if _inputs is not None else self._inputs
        inputs = _merge_inputs(our_inputs, self._inputs)
        return CopyReference(
            _parent=self.parent,
            context=self.context,
            name=name if name is not None else self.name,
            _inputs=inputs,
            attributes=HashableMapping({**kwargs, **self.attributes}),
            copy_of=self.copy_of,
        )

    def __str__(self) -> str:
        if self.name is not None:
            return f"CopyRef({self.copy_of}, name='{self.name}')"
        return f"CopyRef({self.copy_of})"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass(frozen=True, eq=False)
class ContextReference(ForwardReference):
    """
    A forward reference to a node by index within a NodeContext.

    Used when accessing nodes via context dictionary-style lookup (ctx['name']) before
    the node has been created. Resolution happens during context exit when all nodes
    have been registered.
    """

    index: str

    def resolve(self) -> 'NodeInstance | None':
        """
        Resolve the forward reference to an actual NodeInstance.
        Returns `None` if the reference cannot be resolved at
        this time.

        Returns: NodeInstance | None
        """
        val = self.context.get(self.index)
        if isinstance(val, NodeInstance):
            return val
        return None

    def __str__(self) -> str:
        return f"Context[{self.index}]"


@dataclass(frozen=True, eq=False)
class ChainForwardReference(ForwardReference):
    """
    Base class for forward references to chain elements.

    Used when accessing properties or elements of a ChainBuilder before the chain
    construction is complete (while still inside the 'with chain()' block).
    """
    context: 'cctx.NodeContext'
    builder: 'cchain.ChainBuilder'


@dataclass(frozen=True, eq=False)
class ChainFirstReference(ChainForwardReference):
    """
    A forward reference to a chain's .first property.

    Used when accessing .first on a ChainBuilder inside its 'with' block before
    the chain has been finalized. Resolution happens at context exit.
    """

    def resolve(self) -> 'NodeInstance | None':
        """
        Resolve the forward reference to an actual NodeInstance.
        Returns `None` if the reference cannot be resolved at
        this time.

        Returns: NodeInstance | None
        """
        chain = self.builder.chain
        if chain is None:
            return None
        return chain.first.resolve()

    def __str__(self) -> str:
        return "ForwardRef(chain.first)"


@dataclass(frozen=True, eq=False)
class ChainLastReference(ChainForwardReference):
    """
    A forward reference to a chain's .last property.

    Used when accessing .last on a ChainBuilder inside its 'with' block before
    the chain has been finalized. Resolution happens at context exit.
    """

    def resolve(self) -> 'NodeInstance | None':
        """
        Resolve the forward reference to an actual NodeInstance.
        Returns `None` if the reference cannot be resolved at
        this time.

        Returns: NodeInstance | None
        """
        chain = self.builder.chain
        if chain is None:
            return None
        return chain.last.resolve()

    def __str__(self) -> str:
        return "ForwardRef(chain.last)"


@dataclass(frozen=True, eq=False)
class ChainReference(ChainForwardReference):
    """
    A forward reference to a chain element by index.

    Used when accessing chain elements via indexing (chain[0], chain['name'])
    before the chain has been finalized. Resolution happens at context exit.
    """

    index: int | str | slice

    def resolve(self) -> 'NodeInstance | None':
        """
        Resolve the forward reference to an actual NodeInstance.
        Returns `None` if the reference cannot be resolved at
        this time.

        Returns: NodeInstance | None
        """
        chain = self.builder.chain
        if chain is None:
            return None
        return chain.resolve(self.index)

    def __str__(self) -> str:
        return f"ForwardRef(chain[{self.index}])"


@overload
def wrap_node(hnode: hou.Node) -> 'NodeInstance': ...


@overload
def wrap_node(hnode: str, context: 'cctx.NodeContext') -> 'NodeBase': ...


@overload
def wrap_node(hnode: str) -> 'NodeInstance': ...


@overload
def wrap_node(hnode: 'NodeInstance') -> 'NodeInstance': ...


@overload
def wrap_node(hnode: 'ForwardReference') -> 'ForwardReference': ...


@overload
def wrap_node(hnode: 'NodeBase') -> 'NodeBase': ...


def wrap_node(hnode: hou.Node | NodeBase | str, context: 'cctx.NodeContext | None' = None) -> 'NodeBase':

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
            if hnode in _node_registry:
                return _node_registry[hnode]
            if context is not None:
                resolved = context.get(hnode)
                if resolved is not None:
                    return resolved
                resolved = _node_registry.get(hnode)
                if resolved is not None:
                    return resolved
                ref = ForwardReference(context.parent, hnode,
                                       context=context,
                                       )
                _node_registry[hnode] = ref
                return ref
            existing = _node_registry.get(hnode)
            if existing is not None:
                return existing
            hnode = hou_node(hnode)
            n = NodeInstance(wrap_node(hnode.parent()),
                             name=hnode.name(),
                             node_type=hnode.type().name(),
                             _node=hnode,
                             )
            _node_registry[hnode.path()] = n
            return n

        case NodeInstance():
            # If it's already a NodeInstance, just return it
            return hnode
        case _:
            pass
    raise TypeError(f"Invalid node type: {type(hnode).__name__}")


NO_CONNECTION: ResolvedConnection = (None, 0)
'''No connection placeholder for sparse inputs.'''


def _wrap_inputs(inputs: 'RawInputs | None',
                 context: 'cctx.NodeContext | None' = None,
                 ) -> UnresolvedConnections:
    """
    Wrap input specifications (plural) and extract output indices.

    Handles sequences of inputs or single inputs, converting them to a tuple
    of UnresolvedConnection objects. Singular form (_wrap_input) processes
    individual input specifications.

    This handles both singular and plural forms as a convenience for the
    user, as single inputs are much more common. Internally, we always store
    inputs as tuples of UnresolvedConnection, a consistent format that avoids
    errors due the need to special cases. We limit that to interpreting use-
    specified input;

    Args:
        inputs: Sequence of input specifications - either (<node>, <output_index>) tuples or just <node>

    Returns:
        Tuple of (wrapped_node, output_index) for actual nodes, or None for None inputs
    """

    match inputs:
        case _ as input, int() as idx:
            wrapped = _wrap_input(input, idx, context)
            return (wrapped,)
        case None:
            return ()
        case str() as input:
            wrapped = _wrap_input(input, 0, context)
            return (wrapped,)
        case Sequence():
            return tuple(_wrap_input(inp, 0, context) for inp in inputs)
        case NodeBase() | cchain.Chain() | hou.Node() as input:
            wrapped = _wrap_input(input, 0, context)
            return (wrapped,)
        case _:
            raise TypeError(f"Invalid input specification: {inputs}")


def _wrap_input(input: RawInput, idx: int,
                context: 'cctx.NodeContext | None' = None,
                ) -> UnresolvedConnection:
    """
    Wrap a single input specification and extract output index.

    Processes individual input specs (singular), handling various forms:
    - Direct node references (NodeInstance, hou.Node)
    - String names (creates ForwardReference if context provided)
    - Chains (extracts .last node)
    - (node, output_idx) tuples

    Args:
        input: Input specification - either (<node>, <output_index>) tuple or just <node>

    Returns:
        Tuple of (wrapped_node, output_index) for actual no )des, or None for None inputs
    """

    # Copilot: There are no implicit returns in _wrap_single_input. (DO NOT REMOVE)
    def _wrap_single_input(input: RawInput) -> NodeBase | None:
        """Wrap a single input node specification."""
        match input:
            case None:
                return None
            case NodeBase():
                return input
            case cchain.Chain() if len(input.nodes) == 0:
                return None
            case cchain.Chain():
                return input.last
            case cchain.ChainBuilder():
                return input.last
            case hou.Node():
                return wrap_node(input)
            case str():
                if context is not None:
                    resolved = context.get(input)
                    if resolved is not None:
                        return resolved
                    resolved = _node_registry.get(input)
                    if resolved is not None:
                        return resolved
                    ref = ForwardReference(context.parent, input,
                                           context=context,
                                           )
                    _node_registry[input] = ref
                    return ref
                return wrap_node(hou_node(input), )
            case _:
                raise TypeError(
                    f"Invalid input specification: {input}. "
                    f"Expected NodeInstance, Chain, ChainBuilder, hou.Node, str, or ForwardReference."
                )

    match input:
        case None:
            return NO_CONNECTION
        case node_spec, output_idx:
            if not isinstance(output_idx, int) or output_idx < 0:
                raise ValueError(f"Output index must be a non-negative integer, got {output_idx}")
            wrapped = _wrap_single_input(node_spec)
            if wrapped is None:
                return NO_CONNECTION
            return (wrapped, output_idx)
        case tuple():
            raise ValueError("Input tuple must have exactly 2 elements: (<node>, <output_index>)")
        case NodeInstance() | cchain.Chain() | cchain.ChainBuilder() | hou.Node() | str() | ForwardReference():
            # Single node specification, default to output 0
            wrapped = _wrap_single_input(input)
            if wrapped is None:
                return NO_CONNECTION
            return (wrapped, idx)
        case _:
            raise TypeError(f"Invalid input specification: {input}. Expected None, (<node>, <output_index>), or <node>")


def _merge_inputs(in1: UnresolvedConnections,
                  in2: UnresolvedConnections) -> UnresolvedConnections:
    """Merge two input lists, preferring non-None values from the first list."""
    if not in1:
        return tuple(in2)
    if not in2:
        return tuple(in1)

    merged = (
        (left if (left and left[0]) else right) or NO_CONNECTION
        for left, right in zip_longest(in1, in2, fillvalue=None)
    )
    return tuple(merged)


def get_node_instance(hnode: hou.Node) -> 'NodeBase | None':
    """
    Get the original NodeInstance that created a hou.Node, if any.

    Args:
        hnode: The Houdini node to look up

    Returns:
        The original NodeInstance that created this node, or None if not found
    """

    if hnode.path() not in _node_registry:
        raise RuntimeError(f"No NodeInstance found for hou.Node at path: {hnode.path()}")
    return _node_registry.get(hnode.path())


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
