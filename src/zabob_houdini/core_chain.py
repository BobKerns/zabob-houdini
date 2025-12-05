"""
ZChain and ZChainBuilder classes for Zabob-Houdini.

This module contains the ZChain class for representing sequences of connected nodes,
and the ZChainBuilder class for building chains within a context manager interface.
"""

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

import functools
from typing import Any, Generic, cast, overload
from collections.abc import Iterator, Sequence, Mapping

import hou

from zabob_houdini.core_types import (
    NativeNodeType,
    NativeParmData,
    RawInputs,
    RawChainCopyNode,
    ResolvedConnections,
    TypeVar,
    UnresolvedConnections,
)

# Import actual dependencies
from zabob_houdini.core_utils import _generate_name
from zabob_houdini.utils import HashableMapping
from zabob_houdini.core_node import (
    ZNodeBase, ZNode, _merge_inputs,
    ZNodeForwardRef, ZChainFirstRef, ZChainLastRef, ZChainRef,
)
from zabob_houdini.core_context import ZContext


T_Child = TypeVar('T_Child', bound=ZNodeBase)


class ZChain(Generic[T_Child]):
    """
    Represents a chain of Houdini nodes that can be created.

    Nodes in the chain are automatically connected in sequence.
    """
    nodes: tuple[ZNodeBase, ...]
    by_name: dict[str, ZNodeBase]
    context: 'ZContext'
    subset: bool
    '''
    True if this chain is a subset of another chain,
    meaning it may not be complete and should not be added to
    the context on its own.
    '''

    def __init__(self, nodes: Sequence[ZNodeBase], *,
                 context: ZContext,
                 subset: bool = False,
                 ):
        '''
        Initialize a ZChain with the given nodes. We don't copy here,
        but rather where we can receive non-context nodes.

        There's no need to copy ZChainBuilder's nodes.
        '''
        self.context = context
        self.nodes = tuple(nodes)
        self.by_name = {
            n.name: n
            for n in self.nodes
            if n.name is not None
        }
        self.subset = subset

    @property
    def parent(self) -> ZNode:
        match self.nodes:
            case ():
                return self.context.parent
            case ZNodeBase() as n, *_:
                return n.parent
            case _:
                raise RuntimeError(f"Invalid parent: {self.nodes[0]}")

    @property
    def first(self) -> ZNodeBase:
        """Return the first node in this chain."""
        if not self.nodes:
            raise RuntimeError("ZChain is empty.")
        return self.nodes[0]

    @property
    def last(self) -> ZNodeBase:
        """Return the last node in this chain."""
        if not self.nodes:
            raise RuntimeError("ZChain is empty.")
        return self.nodes[-1]

    @functools.cached_property
    def inputs(self) -> ResolvedConnections:
        """Return the input nodes for this chain, which are the inputs of the first node."""
        if not self.nodes:
            return tuple()
        return self.first.resolved_inputs

    @overload
    def __getitem__(self, key: int) -> ZNode: ...

    @overload
    def __getitem__(self, key: slice) -> ZChain: ...

    @overload
    def __getitem__(self, key: str) -> ZNodeBase: ...

    def __getitem__(self, key: int | slice | str) -> ZNodeBase | ZChain:
        """
        Access nodes in the chain by index, slice, or name.

        Args:
            key: Integer index, slice, or node name string

        Returns:
            ZNode for int/str keys, ZChain for slice keys
        """
        nodes = self.nodes

        match key:
            case int() as index:
                return nodes[index]
            case slice() as slice_obj:
                # Return a new ZChain with the subset of nodes
                subset = nodes[slice_obj]
                return ZChain(
                    nodes=subset,
                    context=self.context,
                    subset=True
                )
            case str() as name:
                # Find node by name
                return self.by_name[name]
            case _:
                raise TypeError(f"ZChain indices must be integers, slices, or strings, not {type(key).__name__}")

    def __len__(self) -> int:
        """Return the number of nodes in the chain."""
        return len(self.nodes)

    def __iter__(self) -> Iterator[ZNodeBase]:
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

        return created_instances[0]

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

        return created_instances[-1]

    def nodes_iter(self) -> Iterator[hou.Node]:
        """
        Return an iterator over the created hou.Node instances in the chain.

        Creates the chain if not already created.

        Yields:
            hou.Node objects for each node in the chain.
        """
        created_instances = self.create()
        for instance in created_instances:
            yield instance

    @property
    def hou_nodes(self) -> tuple[hou.Node, ...]:
        """
        Get all created hou.Node instances in the chain as a tuple.

        Creates the chain if not already created.

        Returns:
            Tuple of hou.Node objects for all nodes in the chain.
        """
        return tuple(self.nodes_iter())

    @overload
    def resolve(self, key: int | str | slice) -> ZNode: ...

    @overload
    def resolve(self) -> tuple[ZNode, ...]: ...

    def resolve(self, key: int | str | slice | None = None) -> tuple[ZNode, ...] | ZNode | None:
        """
        Resolve the chain to its constituent ZNode objects.

        Args:
            key: Optional index or name to resolve a specific node. If None, resolves all nodes

        Returns: tuple[ZNode, ...] | None
            ZNode objects for each node in the chain.
        """
        match key:
            case int() as index:
                return self.nodes[index].resolved
            case str() as name:
                return self.by_name[name].resolved
            case None:
                if all(n.resolve() for n in self.nodes):
                    return cast(tuple[ZNode, ...], tuple(n.resolve() for n in self.nodes))
                return tuple(node.resolved for node in self.nodes)

    @functools.cache
    def create(self) -> tuple[hou.Node, ...]:
        """
        Create the actual chain of Houdini nodes.

        ZChain connections are now handled through each node's _inputs,
        so we just need to create each node.

        Returns:
            Tuple of ZNode objects for created nodes. Same instances
            returned on subsequent calls (cached via @functools.cache).
        """
        return tuple(
            node.resolved.create()
            for node in self.nodes
        )

    def copy(self, *nodes: RawChainCopyNode,
             _inputs: RawInputs | None = None,
             _display: bool | None = None,
             _render: bool | None = None,
             **copy_params: 'Mapping[str, NativeParmData]',
             ) -> 'ZChain':
        """
        Return a copy of this ZChain with nodes reordered, dropped, or inserted.

        Args:
            *copy_params: Parameters specifying nodes to copy:
                - int: Index of existing node to copy (can reorder/duplicate)
                - str: Name of existing node to copy
                - ZNode: New node to insert at this position
                If no arguments given, copies all nodes in original order
            _inputs: Input nodes for the first node in the new chain

        Returns:
            New ZChain with specified nodes in specified order

        Examples:
            chain.copy(3, 2, 1, 0)      # Reverse 4-element chain
            chain.copy(0, 2)            # Copy only nodes 0 and 2
            chain.copy("box", "sphere") # Copy by name
            chain.copy(0, new_node, 1)  # Insert new_node between positions 0 and 1
        """
        empty: dict[str, NativeParmData] = {}
        if not nodes:
            nodes = tuple(self.nodes)
        # Build new node list

        def resolve(node_spec: RawChainCopyNode, *, _inputs: RawInputs = None) -> ZNodeBase:
            match node_spec:
                case int() as index:
                    return self.nodes[index]
                case str() as name:
                    return self.by_name[name]
                case ZNodeBase() as node:
                    return node
                case _:
                    raise TypeError(f"Invalid node specification: {node_spec}")
        with self.context.chain() as ctx:
            inputs = _inputs or ()

            def dup(node: RawChainCopyNode) -> ZNodeBase:
                nonlocal inputs
                n = resolve(node)
                params = copy_params.get(n.name, empty)
                result = n.copy(n.name, _inputs=inputs,
                                _display=_display,
                                _render=_render,
                                **params)
                inputs = ()
                return result
            ctx._nodes = [
                dup(n)
                for n in nodes
            ]
        return ctx.chain


class ZChainBuilder:
    """Context manager for building chains without registering intermediate nodes."""

    _inputs: UnresolvedConnections
    _context: ZContext
    _nodes: list[ZNodeBase]
    _chain: ZChain | None = None

    def __init__(self, context: ZContext, *,
                 _input: UnresolvedConnections | None = None,
                 ):
        self._context = context
        self._inputs = _input or ()
        self._nodes = []

    @property
    def chain(self) -> ZChain:
        """
        Return the ZChain we built.
        If the chain is not yet complete, raise an error.
        """
        if self._chain is None:
            raise RuntimeError("ZChain is not yet complete.")
        return self._chain

    @property
    def context(self) -> ZContext:
        """Return the ZContext associated with this ZChainBuilder."""
        return self._context

    def __enter__(self) -> ZChainBuilder:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            # Exception occurred: discard any partially built chain, clean up temporary state
            self._nodes.clear()
            return
        if not self._nodes:
            raise RuntimeError("Cannot create an empty chain.")
        inputs: UnresolvedConnections = self.inputs or ()
        for node in self._nodes:
            for inp, _ in inputs:
                if inp:
                    self._context._add_dependency(inp, node.resolved)
        # First, create the chain without inputs to mark it as complete
        self._chain = ZChain(self._nodes, context=self._context)

    @property
    def parent(self) -> ZNode:
        """Return the parent ZNode for this chain."""
        return self.context.parent

    def copy(self, node: ZNodeBase, /,
             **copy_params: 'NativeParmData'
             ) -> 'ZNodeBase':
        """Add a copy of the given node to this chain."""
        if self._chain is not None:
            raise RuntimeError("Cannot modify a completed chain.")
        copied_node = node._copy(
            _chain=None,
            name=None,
            _inputs=None,
            _display=None,
            _render=None,
            **copy_params
        )
        self._nodes.append(copied_node)
        return copied_node

    def node(self, node_type: NativeNodeType, /,
             name: str | None = None,
             **attributes: Any
             ) -> ZNode:
        """Add a node to this chain (not registered with context until chain completes)."""
        if self._chain is not None:
            raise RuntimeError("Cannot modify a completed chain.")
        # Create node without registering it with the context
        node_instance = ZNode(
            _parent=self.context.parent,  # Use the context's parent
            node_type=node_type,

            name=name or _generate_name(self._context.parent.resolved.path,
                                        node_type),
            attributes=HashableMapping(attributes) if attributes else HashableMapping(),
        )
        self._nodes.append(node_instance)
        self.context._register_node(node_instance)
        return node_instance

    @property
    def last(self) -> ZNodeForwardRef:
        """Return the last node that will be in this chain."""
        return ZChainLastRef(
            _parent=self.context.parent,
            context=self.context,
            builder=self,
            name=""
        )

    @property
    def first(self) -> ZNodeBase:
        """Return the first node that will be in this chain."""
        if self.chain:
            return self.chain.first

        name = self._nodes[0].name if self._nodes else ""

        # During chain construction - return a forward reference
        return ZChainFirstRef(
            _parent=self.context.parent,
            context=self.context,
            builder=self,
            name=name
        )

    @overload
    def __getitem__(self, index: int | str) -> ZNodeBase: ...

    @overload
    def __getitem__(self, index: slice) -> ZChain | ZChainRef: ...

    def __getitem__(self, index: int | str | slice) -> ZNodeBase | ZChain:
        """Access nodes in the chain by index."""
        if self._chain:
            return self._chain[index]
        match index:
            case int() as idx:
                if idx < len(self._nodes):
                    return self._nodes[idx]
            case str() as name:
                for n in self._nodes:
                    if n.name == name:
                        return n
            case slice() as slice_obj:
                if (
                    (slice_obj.stop is not None)
                    and (0 <= slice_obj.stop <= len(self._nodes))
                    and (0 <= slice_obj.start <= len(self._nodes))
                ):
                    subset = self._nodes[slice_obj]
                    return ZChain(
                        nodes=subset,
                        context=self.context,
                        subset=True
                    )
            case _:
                raise TypeError(f"ZChain indices must be integers, slices, or strings, not {type(index).__name__}")

        return ZChainRef(
            _parent=self.context.parent,
            context=self.context,
            builder=self,
            index=index,
            name=str(index)
        )

    @functools.cached_property
    def inputs(self) -> UnresolvedConnections:
        """Return the inputs of the first node in the chain."""
        if self._chain:
            return self.chain.first.inputs
        if self._nodes:
            return _merge_inputs(self._inputs, self._nodes[0].inputs or ())
        raise RuntimeError("Cannot access inputs of an empty chain.")
