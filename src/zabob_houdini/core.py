"""
Core Zabob-Houdini API for creating Houdini node graphs.
"""

from typing import Any
from dataclasses import dataclass


# Type aliases for clarity
type NodeParent = 'str | NodeInstance'
type NodeType = str  # Initially strings, will expand to NodeTypeInstance later


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
    inputs: list['NodeInstance'] | None = None

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
        # TODO: Implement actual Houdini node creation
        # This will call hou module functions
        raise NotImplementedError("Node creation not yet implemented")


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
    inputs: list[NodeInstance] | None = None

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
    _input: NodeInstance | list[NodeInstance] | None = None,
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
            inputs.extend(_input)
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
    _input: NodeInstance | list[NodeInstance] | None = None,
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
