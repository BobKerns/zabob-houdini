"""
Core Zabob-Houdini API for creating Houdini node graphs.
"""

from typing import Any, TypeAlias
from dataclasses import dataclass


# Type aliases for clarity
NodeParent: TypeAlias = 'str | NodeInstance'
"""A parent node, either as a path string (e.g., "/obj") or an existing NodeInstance."""

NodeType: TypeAlias = str
"""A Houdini node type name (e.g., "geo", "box", "xform"). Will expand to NodeTypeInstance later."""


@dataclass
class NodeInstance:
    """
    Represents a Houdini node that can be created.

    This is a declarative representation - the actual Houdini node
    is created when .create() is called.
    """
    parent: NodeParent
    node_type: NodeType
    name: str | None = None
    attributes: dict[str, Any] | None = None
    inputs: list['NodeInstance | None'] | None = None

    def __post_init__(self) -> None:
        if self.attributes is None:
            self.attributes = {}
        if self.inputs is None:
            self.inputs = []

    def create(self) -> Any:
        """
        Create the actual Houdini node.

        Returns:
            The created Houdini node object.
        """
        try:
            import hou
        except ImportError:
            raise ImportError(
                "Houdini module 'hou' not available. "
                "This function must be run within Houdini's Python environment."
            )

        # Resolve parent node
        if isinstance(self.parent, str):
            parent_node = hou.node(self.parent)
            if parent_node is None:
                raise ValueError(f"Parent node not found: {self.parent}")
        elif isinstance(self.parent, NodeInstance):
            # Parent is another NodeInstance - it should be created first
            parent_node = self.parent.create()
        else:
            # Assume it's already a Houdini node
            parent_node = self.parent

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
                    if isinstance(input_node, NodeInstance):
                        # Input is a NodeInstance - create it first
                        input_hou_node = input_node.create()
                    else:
                        # Must be an actual Houdini node - validate it
                        if not hasattr(input_node, 'path') or not callable(getattr(input_node, 'path')):
                            raise TypeError(
                                f"Input {i} must be a NodeInstance or Houdini node object, "
                                f"got {type(input_node).__name__}"
                            )
                        input_hou_node = input_node

                    created_node.setInput(i, input_hou_node)
                except Exception as e:
                    print(f"Warning: Failed to connect input {i}: {e}")

        return created_node


@dataclass
class Chain:
    """
    Represents a chain of Houdini nodes that can be created.

    Nodes in the chain are automatically connected in sequence.
    """
    parent: NodeParent
    node_types: list[NodeType]
    name_prefix: str | None = None
    attributes: dict[str, Any] | None = None
    inputs: list[NodeInstance | None] | None = None

    def __post_init__(self) -> None:
        if self.attributes is None:
            self.attributes = {}
        if self.inputs is None:
            self.inputs = []

    def create(self) -> list[Any]:
        """
        Create the actual chain of Houdini nodes.

        Returns:
            List of created Houdini node objects.
        """
        # TODO: Implement actual chain creation
        # This will create nodes and connect them in sequence
        raise NotImplementedError("Chain creation not yet implemented")


def node(
    parent: NodeParent,
    node_type: NodeType,
    name: str | None = None,
    _input: NodeInstance | list[NodeInstance | None] | None = None,
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
        if isinstance(_input, list):
            inputs.extend(_input)  # List can contain None values for sparse inputs
        else:
            inputs.append(_input)

    return NodeInstance(
        parent=parent,
        node_type=node_type,
        name=name,
        attributes=attributes,
        inputs=inputs
    )


def chain(
    parent: NodeParent,
    *node_types: NodeType,
    _input: NodeInstance | list[NodeInstance | None] | None = None,
    name_prefix: str | None = None,
    **attributes: Any
) -> Chain:
    """
    Create a chain of nodes definition.

    Args:
        parent: Parent node (path string or NodeInstance)
        *node_types: Sequence of node types to chain together
        _input: Optional input node(s) to connect to start of chain
        name_prefix: Optional prefix for generated node names
        **attributes: Shared attributes for all nodes in chain

    Returns:
        Chain that can be created with .create()
    """
    inputs = []
    if _input is not None:
        if isinstance(_input, list):
            inputs.extend(_input)
        else:
            inputs.append(_input)

    return Chain(
        parent=parent,
        node_types=list(node_types),
        name_prefix=name_prefix,
        attributes=attributes,
        inputs=inputs
    )
