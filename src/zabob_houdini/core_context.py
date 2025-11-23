"""
Context management classes for Zabob-Houdini.

This module contains the NodeContext class that provides a context manager
interface for building node graphs with automatic layout and dependency tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import weakref
from collections.abc import Sequence

import hou

from zabob_houdini.core_types import (
    NodeParent, NodeType,
    InputNode,
    InstanceNodeSpec,
)

# Import actual dependencies
from zabob_houdini.core_node import (
    NodeInstance, node, wrap_node,
    ForwardReference,
)
from zabob_houdini.core_chain import ChainBuilder


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
             node_type: 'NodeType',
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
                        # Auto-register named external NodeInstance objects in context
                        if input_spec.name is not None and input_spec.name not in self._nodes:
                            # Validate that the input node has the same parent as the context
                            if input_spec.parent != self.parent:
                                raise ValueError(f"Cannot register node '{input_spec.name}' in context: "
                                               f"node parent {input_spec.parent} does not match context parent {self.parent}")
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

    def chain(self, *, _input: 'InputNode | Sequence[InputNode] | None' = None, **attributes: Any) -> ChainBuilder:
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

    def merge(self, *inputs: 'InstanceNodeSpec',
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
