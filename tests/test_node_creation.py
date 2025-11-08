"""
Basic test for creating a single node.
"""

import pytest
from unittest.mock import Mock, patch
from zabob_houdini import node, chain


def test_node_creation_with_string_parent():
    """Test creating a node with a string parent path."""
    # Create a node (this should not call Houdini yet)
    box_node = node("/obj", "box", name="testbox")

    # Verify the node instance was created
    assert box_node is not None
    # TODO: Add assertions for node properties once NodeInstance is implemented


def test_node_creation_with_node_parent():
    """Test creating a node with another node as parent."""
    # Create parent node
    geo_node = node("/obj", "geo", name="testgeo")

    # Create child node
    box_node = node(geo_node, "box", name="testbox")

    # Verify both nodes were created
    assert geo_node is not None
    assert box_node is not None
    # TODO: Add assertions for parent-child relationship


def test_node_create_method():
    """Test the .create() method raises NotImplementedError for now."""
    # Create a node
    box_node = node("/obj", "box", name="testbox")

    # Verify the node was created
    assert box_node is not None
    assert box_node.parent == "/obj"
    assert box_node.node_type == "box"
    assert box_node.name == "testbox"

    # Test that .create() raises NotImplementedError (stub behavior)
    with pytest.raises(NotImplementedError, match="Node creation not yet implemented"):
        box_node.create()


def test_node_with_input_connection():
    """Test creating a node with _input parameter."""
    # Create source node
    box_node = node("/obj/geo1", "box", name="source")

    # Create node with input connection
    transform_node = node("/obj/geo1", "xform", name="transform", _input=box_node)

    # Verify nodes were created
    assert box_node is not None
    assert transform_node is not None
    # TODO: Add assertions for input connection once implemented


def test_chain_creation():
    """Test creating a chain of nodes with parent argument."""
    # Create a chain with parent
    node_chain = chain("/obj/geo1", "box", "xform", "subdivide")

    # Verify chain was created
    assert node_chain is not None
    # TODO: Add assertions for chain properties once Chain is implemented


def test_chain_with_input():
    """Test creating a chain with _input parameter."""
    # Create source node
    source_node = node("/obj/geo1", "box", name="source")

    # Create chain with input connection
    processing_chain = chain("/obj/geo1", "xform", "subdivide", _input=source_node)

    # Verify both were created
    assert source_node is not None
    assert processing_chain is not None
    # TODO: Add assertions for chain input connection once implemented


if __name__ == "__main__":
    pytest.main([__file__])
