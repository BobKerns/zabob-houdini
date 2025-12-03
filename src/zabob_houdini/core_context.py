"""
Context management classes for Zabob-Houdini.

This module contains the NodeContext class that provides a context manager
interface for building node graphs with automatic layout and dependency tracking.
"""

from __future__ import _dynamic_import, annotations  # type: ignore # noqa: F407

from collections import deque
from dataclasses import dataclass, field
from typing import Any, TypeVar, overload
import weakref
from collections.abc import Iterator, Sequence

import hou

from zabob_houdini.core_types import (
    NativeNodeType,
    RawInput,
    RawInputs,
)
from zabob_houdini.core_utils import _generate_name
from zabob_houdini.core_node import (
    NodeInstance, ForwardReference, NodeBase, _wrap_inputs,
)
from zabob_houdini.core_chain import ChainBuilder
from zabob_houdini.solo_fns import (  # noqa: F401
    wrap_node, node,
)


D = TypeVar('D')


@dataclass
class NodeContext:
    """
    A context manager for creating nodes within a specific parent.

    Provides a convenient way to create multiple nodes under the same parent
    without having to specify the parent for each node() call.

    Named nodes can be looked up using dictionary-style access: ctx['name']
    """
    parent: NodeInstance
    _nodes: dict[str, NodeBase] = field(default_factory=dict, init=False)
    _dependency_registry: weakref.WeakKeyDictionary[NodeBase, list[NodeBase]] = field(
        default_factory=weakref.WeakKeyDictionary, init=False
    )
    _level: int = field(default=0, init=False)
    pending: deque[ForwardReference] = field(default_factory=deque, init=False)

    def __enter__(self) -> 'NodeContext':
        """Enter the context manager."""
        self._level += 1

        if self._level == 1:
            # Collect all existing nodes under the parent to populate the registry
            # We don't collect every dependency, just prepare to receive new ones,
            # and resolve forward references as they are resolved.
            for node in self.parent.create().allSubChildren():
                if node not in self._dependency_registry:
                    znode = wrap_node(node)
                    self._dependency_registry[znode] = []
                    self._nodes[node.name()] = znode

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager - apply layout and create sink nodes."""
        self._level -= 1
        if self._level > 0:
            return
        if exc_type is None:  # Only if no exception occurred
            for ref in self.resolved():
                pass

            # Create all sink nodes (nodes with no dependents)
            sink_nodes = set(self.get_sink_nodes())
            all_nodes = set(self._nodes.values())
            connect_queue = deque(sink_nodes)
            connect_queue.extend(all_nodes - sink_nodes)
            done: set[NodeBase] = set()
            while connect_queue:
                node = connect_queue.popleft()
                done.add(node)
                node.resolved._connect_inputs()
                for inp, _ in node.inputs:
                    if inp is not None and inp not in done:
                        connect_queue.append(inp)
            # Second pass for

            for node in self._nodes.values():
                node.resolved.create()

            # Apply layout to position all nodes
            self.apply_layout()

    def _create_forward_reference_for_name(self, name: str) -> ForwardReference:
        """Create a ForwardReference for an unknown string name."""
        return ForwardReference(
            _parent=self.parent,
            context=self,
            name=name
        )

    def resolved(self) -> Iterator[NodeInstance]:
        """
        Resolve forward references using deque-based algorithm.

        Algorithm:
        1. Add all refs to deque
        2. While deque not empty:
        a. Pop reference from front
        b. Try to resolve it
        c. If successful: add to resolved list, reset counter
        d. If fails: push to back, increment counter
        3. Terminate when:
        - Deque empty (success - all resolved)
        - Counter == deque length (deadlock - tried all, none resolved)
        """
        pending = self.pending
        attempts_without_progress = 0

        while pending:
            if attempts_without_progress >= len(pending):
                # Deadlock: tried all refs but none resolved
                unresolved_names = [ref.name for ref in pending]
                raise ValueError(f"Cannot resolve forward references: {unresolved_names}")

            ref = pending.popleft()

            # Attempt resolution
            resolved = ref.resolve()
            if resolved:
                self._nodes[ref.name] = resolved
                oldeps = self._dependency_registry.get(ref, [])
                newdeps = [
                    dep.resolve() or dep
                    for dep in oldeps

                ]
                self._dependency_registry[resolved] = newdeps
                self._dependency_registry[ref] = newdeps
                yield resolved
                attempts_without_progress = 0  # Reset counter on success
            else:
                pending.append(ref)
                attempts_without_progress += 1

    def node(self,
             node_type: 'NativeNodeType',
             /,
             name: str | None = None,
             *,
             _input: RawInputs | None = None,
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
        import zabob_houdini.solo_fns as solo

        inputs = solo._wrap_inputs(_input, self)

        name = name or str(node_type)
        while name in self._nodes:
            name = _generate_name(name, node_type)

        # Create the node using the global node() function
        node_instance = node(
            self.parent,
            node_type,
            name,
            _input=inputs,
            _node=_node,
            _display=_display,
            _render=_render,
            _context=self,
            **attributes
        )
        self._register_node(node_instance)
        return node_instance

    def _register_node(self, node_instance: NodeBase) -> None:
        name = node_instance.name
        # Ensure node is registered in dependency registry (even if no dependencies)
        if node_instance not in self._dependency_registry:
            self._dependency_registry[node_instance] = []

        # Register named nodes for lookup
        if name is not None:
            # Check if there was a ForwardReference for this name that needs to be replaced
            old_entry = self._nodes.get(name)
            if isinstance(node_instance, NodeInstance):
                if isinstance(old_entry, ForwardReference):
                    # Remove the ForwardReference from pending list
                    try:
                        self.pending.remove(old_entry)
                    except ValueError:
                        pass  # It may have already been removed
                    # Replace the ForwardReference with the actual NodeInstance
                    # Also update any other references in the context that point to the ForwardReference
                    self._replace_forward_reference(old_entry, node_instance)

            self._nodes[name] = node_instance

        # Track dependencies for inputs
        inputs = node_instance.inputs
        for input_spec, _ in inputs:
            if input_spec is not None:
                # Determine the input node for dependency tracking
                input_node: NodeBase | None = None

                # Resolve the input to a NodeInstance or ForwardReference
                if isinstance(input_spec, NodeInstance):
                    input_node = input_spec
                    # Auto-register named external NodeInstance objects in context
                    if input_spec.name is not None and input_spec.name not in self._nodes:
                        # Validate that the input node has the same parent as the context
                        if input_spec.parent != self.parent:
                            raise ValueError(
                                f"Cannot register node '{input_spec.name}' in context: "
                                f"node parent {input_spec.parent} does not match "
                                f"context parent {self.parent}"
                            )
                        self._nodes[input_spec.name] = input_spec
                elif hasattr(input_spec, 'last'):  # Chain object
                    # Import Chain here to avoid circular dependency
                    from zabob_houdini.core import Chain
                    if isinstance(input_spec, Chain):
                        input_node = input_spec.last
                    else:
                        continue
                elif isinstance(input_spec, ForwardReference):
                    input_node = input_spec
                else:
                    continue  # Skip other types (hou.Node, str, tuples)

                # Track the dependency (ForwardReferences are handled in _add_dependency)
                if input_node is not None and isinstance(node_instance, NodeInstance):
                    self._add_dependency(input_node, node_instance)

    def __getitem__(self, name: str) -> NodeBase:
        """Look up a named node created in this context."""
        if name not in self._nodes:
            raise KeyError(f"No node named '{name}' found in this context")
        return self._nodes[name]

    @overload
    def get(self, name: str) -> NodeBase | None: ...

    @overload
    def get(self, name: str, default: D) -> NodeBase | D: ...

    def get(self, name: str, default: D | None = None) -> D | NodeBase | None:
        """Get a named node created in this context, or None if it doesn't exist."""
        return self._nodes.get(name, default)

    def context(self, node_or_path: 'NodeInstance | str | hou.Node | None' = None) -> 'NodeContext':
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

    def chain(self, *, _input: 'RawInput | Sequence[RawInput] | None' = None, **attributes: Any) -> ChainBuilder:
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
        import zabob_houdini.core_chain as cchain

        # Process inputs to handle forward references
        processed_input = _wrap_inputs(_input, self)
        return cchain.ChainBuilder(self, _input=processed_input)

    def merge(self, *inputs: 'RawInput',
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

        return self.node("merge", name, _input=inputs, **attributes)

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
                for inp in node.inputs:
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

    def _add_dependency(self, input_node: 'NodeBase', dependent_node: NodeInstance) -> None:
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

    def get_dependents(self, node: NodeBase) -> list[NodeBase]:
        """Get list of nodes that depend on the given node."""
        return [dep.resolved for dep in self._dependency_registry.get(node, [])]

    def get_source_nodes(self) -> list[NodeBase]:
        """Get nodes in this context that have no inputs (source nodes).

        Returns:
            List of all context nodes (named and unnamed) that have no input connections
        """
        return [
            node
            for node in self._dependency_registry.keys()
            if (not node.inputs
                or all(inp is None for inp, _ in node.inputs)
                )
        ]

    def get_sink_nodes(self) -> list[NodeBase]:
        """Get nodes in this context that have no dependents (sink nodes).

        Returns:
            List of all context nodes (named and unnamed) that no other nodes depend on
        """
        return [
            node
            for node in self._dependency_registry.keys()
            if not self.get_dependents(node)
        ]

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

    def layout_nodes(
        self,
        layer_height: float = 2.0,
        node_width: float = 2.0,
        min_spacing: float = 0.5
    ) -> dict[NodeBase, tuple[float, float]]:
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
        all_nodes = [
            k.resolved
            for k in self._dependency_registry.keys()
            ]
        if not all_nodes:
            return {}

        # Calculate Y offset once at the start for consistency
        y_offset = self._get_lowest_existing_node_position()

        # Step 1: Compute topological layers
        layers = self._compute_layers(all_nodes)

        # Step 2: Compute space requirements (bottom-up)
        space_requirements = self._compute_space_requirements(layers, node_width, min_spacing)

        # Step 3: Position nodes within each layer
        positions = self._position_nodes_in_layers(
            layers, space_requirements, layer_height, node_width, min_spacing, y_offset
        )

        return positions

    def _compute_layers(self, all_nodes: Sequence[NodeBase]) -> dict[int, list[NodeBase]]:
        """Compute vertical layers using proper top-down traversal."""
        node_depths: dict[NodeBase, int] = {}
        resolved_nodes = {
            node.resolved
            for node in all_nodes
        }

        # Get actual source nodes (no inputs within our context)
        source_nodes = {
            node.resolved
            for node in all_nodes
            if not any(inp
                       for inp, idx in node.inputs)
        }
        unassigned = resolved_nodes - source_nodes

        # Top-down traversal to assign depths
        def assign_depth(node: NodeInstance, depth: int) -> None:
            unassigned.discard(node)
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
                    assign_depth(dependent.resolved, depth + 1)

        # Process all top-level source nodes
        for node in source_nodes:
            assign_depth(node, 0)

        # We can have left-overs due to loops with no clear top.

        while unassigned:
            node = next(iter(unassigned))
            assign_depth(node, 0)

        # Move all sink nodes to a common bottom layer
        sink_nodes = self.get_sink_nodes()
        if sink_nodes:
            max_depth = max(node_depths.values())
            sink_depth = max_depth + 1
            for sink in sink_nodes:
                node_depths[sink.resolved] = sink_depth

        # Create contiguous layer mapping (0, 1, 2, ...) from potentially sparse depths
        unique_depths = sorted(set(node_depths.values()))
        depth_to_layer = {depth: idx for idx, depth in enumerate(unique_depths)}

        # Group nodes by contiguous layer indices
        layers: dict[int, list[NodeBase]] = {}
        for node, depth in node_depths.items():
            layer_idx = depth_to_layer[depth]
            if layer_idx not in layers:
                layers[layer_idx] = []
            layers[layer_idx].append(node)

        return layers

    def _compute_space_requirements(
        self,
        layers: dict[int, list[NodeBase]],
        node_width: float,
        min_spacing: float
    ) -> dict[NodeBase, float]:
        """Compute space requirements for each node based on output fanout."""
        space_requirements: dict[NodeBase, float] = {}
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
                        space_requirements.get(dep.resolved, node_width + min_spacing)
                        for dep in dependents
                    )
                    space_requirements[node] = max(dependent_space, node_width + min_spacing)

        return space_requirements

    def _position_nodes_in_layers(
        self,
        layers: dict[int, list[NodeBase]],
        space_requirements: dict[NodeBase, float],
        layer_height: float,
        node_width: float,
        min_spacing: float,
        y_offset: float
    ) -> dict[NodeBase, tuple[float, float]]:
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
        node_required_width: dict[NodeBase, float] = {}

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
                    total_output_width = sum(node_required_width[output.resolved] for output in outputs)
                    # Node needs at least its own width or the sum of its outputs
                    node_required_width[node] = max(space_requirements[node], total_output_width)

        # Step 2: Downward pass - position nodes based on allocated space
        positions: dict[NodeBase, tuple[float, float]] = {}

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
            input_groups: dict[tuple[NodeBase, ...], list[NodeBase]] = {}

            for node in layer_nodes:
                # Resolve ForwardReferences in inputs before grouping
                input_nodes = tuple(
                    inp.resolved
                    for inp, _ in node.inputs
                    if inp is not None
                )
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
                    input_positions = [
                        positions[inp][0]
                        for inp in input_nodes
                        if inp in positions]
                    input_widths = [
                        node_required_width[inp]
                        for inp in input_nodes
                        if inp in positions
                    ]

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
            hou_node = node.resolved.create()

            # Set the position
            try:
                hou_node.setPosition((x, y))
            except Exception as e:
                print(f"Warning: Failed to set position for {node}: {e}")

    def __str__(self) -> str:
        return f"NodeContext({self.parent})"
