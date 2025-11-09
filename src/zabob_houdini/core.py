"""
Core Zabob-Houdini API for creating Houdini node graphs.

This module provides the core API for creating and managing Houdini nodes programmatically.
"""

"""
Core Zabob-Houdini API for creating Houdini node graphs.

This module assumes it's running in a Houdini environment (mediated by bridge or test fixture).
"""

from typing import Any, TypeAlias, overload
from dataclasses import dataclass
from abc import ABC, abstractmethod
import hou


# Type aliases for clarity
NodeParent: TypeAlias = "str | NodeInstance | hou.Node"
"""A parent node, either as a path string (e.g., "/obj"), NodeInstance, or hou.Node object."""

NodeType: TypeAlias = str
"""A Houdini node type name (e.g., "geo", "box", "xform"). Will expand to NodeTypeInstance later."""

CreatableNode: TypeAlias = 'NodeInstance | Chain'
"""A node or chain that can be created via .create() method."""

InputNode: TypeAlias = 'NodeInstance | hou.Node | None'
"""A node that can be used as input - NodeInstance, actual hou.Node, or None for sparse connections."""


class HoudiniNodeBase(ABC):
    """
    Base class for Houdini node representations.

    Provides common functionality for NodeInstance and Chain classes.
    """

    def __init__(self, parent: NodeParent, attributes: dict[str, Any] | None = None,
                 inputs: list[InputNode] | None = None):
        self.parent = parent
        self.attributes = attributes if attributes is not None else {}
        self.inputs = inputs if inputs is not None else []

    @abstractmethod
    def create(self) -> Any:
        """Create the actual Houdini node(s). Return type varies by implementation."""
        pass


@dataclass
class NodeInstance(HoudiniNodeBase):
    """
    Represents a Houdini node that can be created.

    This is a declarative representation - the actual Houdini node
    is created when .create() is called.
    """
    parent: NodeParent
    node_type: NodeType
    name: str|None= None
    attributes: dict[str, Any]|None = None

    inputs: list[InputNode]| None = None
    def __post_init__(self) -> None:
        super().__init__(self.parent, self.attributes, self.inputs)

    def create(self) -> hou.Node:
        """
        Create the actual Houdini node.

        Returns:
            The created Houdini node object.
        """
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
                created_node.setParms(self.attributes)
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
                        case hou.Node() as houdini_node:
                            # It's already a Houdini node object
                            input_hou_node = houdini_node
                        case _:
                            raise TypeError(
                                f"Input {i} must be a NodeInstance or Houdini node object, "
                                f"got {type(input_node).__name__}"
                            )
                    created_node.setInput(i, input_hou_node)
                except Exception as e:
                    print(f"Warning: Failed to connect input {i}: {e}")

        return created_node


@dataclass
class Chain(HoudiniNodeBase):
    """
    Represents a chain of Houdini nodes that can be created.

    Nodes in the chain are automatically connected in sequence.
    """
    parent: NodeParent
    nodes: list[CreatableNode]
    name_prefix: str | None = None
    attributes: dict[str, Any] | None = None
    inputs: list[InputNode] | None = None

    def __post_init__(self) -> None:
        super().__init__(self.parent, self.attributes, self.inputs)

    def _flatten_nodes(self) -> list['NodeInstance']:
        """
        Flatten the chain, splicing in any Chain objects.

        Returns:
            A flat list of NodeInstance objects.
        """
        flattened = []
        for item in self.nodes:
            match item:
                case NodeInstance():
                    flattened.append(item)
                case Chain():
                    flattened.extend(item._flatten_nodes())
                case _ if isinstance(item, hou.Node):
                    # It's a Houdini node - wrap it in a NodeInstance
                    node_path = item.path()
                    parent_path = '/'.join(node_path.split('/')[:-1]) or '/'
                    node_name = node_path.split('/')[-1]
                    wrapped = NodeInstance(
                        parent=parent_path,
                        node_type=item.type().name(),
                        name=node_name
                    )
                    flattened.append(wrapped)
                case _:
                    raise TypeError(
                        f"Chain nodes must be NodeInstance, Chain, or hou.Node objects, "
                        f"got {type(item).__name__}"
                    )
        return flattened

    @overload
    def __getitem__(self, key: int) -> NodeInstance: ...

    @overload
    def __getitem__(self, key: slice) -> 'Chain': ...

    @overload
    def __getitem__(self, key: str) -> NodeInstance: ...

    def __getitem__(self, key: int | slice | str) -> CreatableNode:
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
                # Cast to the type alias to satisfy type checker
                subset_nodes: list[CreatableNode] = list(subset)
                return Chain(
                    parent=self.parent,
                    nodes=subset_nodes,
                    name_prefix=self.name_prefix,
                    attributes=self.attributes.copy() if self.attributes else None,
                    inputs=self.inputs.copy() if self.inputs else None
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

    def create(self) -> list[Any]:
        """
        Create the actual chain of Houdini nodes.

        Returns:
            List of created Houdini node objects in order.
        """
        flattened_nodes = self._flatten_nodes()
        if not flattened_nodes:
            return []

        created_nodes = []
        previous_node = None

        # Handle inputs to the first node in the chain
        if self.inputs:
            # Set up inputs for the first node
            first_node = flattened_nodes[0]
            if first_node.inputs:
                # Extend existing inputs
                first_node.inputs.extend(self.inputs)
            else:
                first_node.inputs = self.inputs.copy()

        # Create each node and connect them in sequence
        for i, node_instance in enumerate(flattened_nodes):
            # Make a copy to avoid modifying the original
            node_copy = NodeInstance(
                parent=node_instance.parent,
                node_type=node_instance.node_type,
                name=node_instance.name,
                attributes=node_instance.attributes.copy() if node_instance.attributes else {},
                inputs=node_instance.inputs.copy() if node_instance.inputs else []
            )

            # Connect to previous node if this isn't the first node
            if i > 0 and previous_node is not None:
                # Add the previous node as input (at index 0)
                if node_copy.inputs:
                    # Insert at the beginning to maintain primary input at 0
                    node_copy.inputs.insert(0, previous_node)
                else:
                    node_copy.inputs = [previous_node]

            # Create the node
            created_node = node_copy.create()
            created_nodes.append(created_node)

            # For the next iteration, we need to pass the actual created Houdini node
            # as input. We'll store it directly as the previous_node reference.
            previous_node = created_node

        return created_nodes


def node(
    parent: NodeParent,
    node_type: NodeType,
    name: str | None = None,
    _input: 'InputNode | list[InputNode] | None' = None,
    **attributes: Any
) -> NodeInstance:
    """
    Create a node definition.

    Args:
        parent: Parent node (path string or NodeInstance)
        node_type: Type of node to create (e.g., "box", "xform")
        name: Optional name for the node
        _input: Optional input node(s) to connect
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
        attributes=attributes,
        inputs=inputs
    )


def chain(
    parent: NodeParent,
    *nodes: CreatableNode,
    _input: "NodeInstance | list[NodeInstance | None] | None" = None,
    name_prefix: str | None = None,
    **attributes: Any
) -> Chain:
    """
    Create a chain of nodes definition.

    Args:
        parent: Parent node (path string or NodeInstance)
        *nodes: Sequence of NodeInstance objects, Chain objects, or Houdini nodes to chain together
        _input: Optional input node(s) to connect to start of chain
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
        nodes=list(nodes),
        name_prefix=name_prefix,
        attributes=attributes,
        inputs=inputs
    )
