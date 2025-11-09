"""
Tests for Chain functionality.
"""

import pytest
from unittest.mock import Mock, patch
from zabob_houdini import node, chain


def test_chain_with_node_instances():
    """Test creating a chain with NodeInstance objects."""
    # Create individual nodes
    box_node = node("/obj/geo1", "box", name="source")
    xform_node = node("/obj/geo1", "xform", name="transform")
    subdivide_node = node("/obj/geo1", "subdivide", name="refine")

    # Create chain
    processing_chain = chain("/obj/geo1", box_node, xform_node, subdivide_node)

    # Verify chain properties
    assert processing_chain is not None
    assert processing_chain.parent == "/obj/geo1"
    assert len(processing_chain.nodes) == 3
    assert len(processing_chain) == 3  # Test __len__


def test_chain_indexing_by_integer():
    """Test chain indexing by integer."""
    # Create nodes
    box_node = node("/obj/geo1", "box", name="source")
    xform_node = node("/obj/geo1", "xform", name="transform")
    subdivide_node = node("/obj/geo1", "subdivide", name="refine")

    # Create chain
    processing_chain = chain("/obj/geo1", box_node, xform_node, subdivide_node)

    # Test integer indexing
    assert processing_chain[0] == box_node
    assert processing_chain[1] == xform_node
    assert processing_chain[2] == subdivide_node
    assert processing_chain[-1] == subdivide_node


def test_chain_indexing_by_name():
    """Test chain indexing by name."""
    # Create nodes
    box_node = node("/obj/geo1", "box", name="source")
    xform_node = node("/obj/geo1", "xform", name="transform")
    subdivide_node = node("/obj/geo1", "subdivide", name="refine")

    # Create chain
    processing_chain = chain("/obj/geo1", box_node, xform_node, subdivide_node)

    # Test name indexing
    assert processing_chain["source"] == box_node
    assert processing_chain["transform"] == xform_node
    assert processing_chain["refine"] == subdivide_node

    # Test KeyError for non-existent name
    with pytest.raises(KeyError, match="No node found with name 'nonexistent'"):
        processing_chain["nonexistent"]


def test_chain_indexing_by_slice():
    """Test chain indexing by slice."""
    # Create nodes
    box_node = node("/obj/geo1", "box", name="source")
    xform_node = node("/obj/geo1", "xform", name="transform")
    subdivide_node = node("/obj/geo1", "subdivide", name="refine")
    output_node = node("/obj/geo1", "output", name="out")

    # Create chain
    processing_chain = chain("/obj/geo1", box_node, xform_node, subdivide_node, output_node)

    # Test slice indexing
    subset_chain = processing_chain[1:3]

    # Verify it's a new Chain object
    assert isinstance(subset_chain, type(processing_chain))
    assert len(subset_chain) == 2
    assert subset_chain[0] == xform_node
    assert subset_chain[1] == subdivide_node

    # Test empty slice
    empty_chain = processing_chain[5:10]
    assert len(empty_chain) == 0


def test_chain_splicing():
    """Test chain splicing when a Chain is passed to another chain."""
    # Create individual nodes
    box_node = node("/obj/geo1", "box", name="source")
    normal_node = node("/obj/geo1", "normal", name="normals")
    output_node = node("/obj/geo1", "output", name="out")

    # Create a processing chain
    xform_node = node("/obj/geo1", "xform", name="transform")
    subdivide_node = node("/obj/geo1", "subdivide", name="refine")
    processing_chain = chain("/obj/geo1", xform_node, subdivide_node)

    # Create a master chain that includes the processing chain (should be spliced)
    master_chain = chain("/obj/geo1", box_node, normal_node, processing_chain, output_node)

    # Verify splicing - the processing_chain should be flattened into the master chain
    flattened = master_chain._flatten_nodes()
    assert len(flattened) == 5  # box, normal, xform, subdivide, output
    assert flattened[0] == box_node
    assert flattened[1] == normal_node
    assert flattened[2] == xform_node  # From processing_chain
    assert flattened[3] == subdivide_node  # From processing_chain
    assert flattened[4] == output_node

    # Test indexing on the master chain works correctly
    assert master_chain[2] == xform_node
    assert master_chain["transform"] == xform_node


def test_chain_with_input():
    """Test chain with _input parameter."""
    # Create source node
    source_node = node("/obj/geo1", "box", name="source")

    # Create processing nodes
    xform_node = node("/obj/geo1", "xform", name="transform")
    subdivide_node = node("/obj/geo1", "subdivide", name="refine")

    # Create chain with input
    processing_chain = chain("/obj/geo1", xform_node, subdivide_node, _input=source_node)

    # Verify chain has input
    assert processing_chain.inputs is not None
    assert len(processing_chain.inputs) == 1
    assert processing_chain.inputs[0] == source_node


def test_chain_invalid_indexing():
    """Test chain raises appropriate errors for invalid indexing."""
    # Create nodes
    box_node = node("/obj/geo1", "box", name="source")
    xform_node = node("/obj/geo1", "xform", name="transform")

    # Create chain
    processing_chain = chain("/obj/geo1", box_node, xform_node)

    # Test invalid index types
    with pytest.raises(TypeError, match="Chain indices must be integers, slices, or strings"):
        processing_chain[1.5]  # type: ignore  # Testing invalid type

    with pytest.raises(TypeError, match="Chain indices must be integers, slices, or strings"):
        processing_chain[{"key": "value"}]  # type: ignore  # Testing invalid type


def test_chain_create_with_mocked_hou():
    """Test chain .create() method with mocked hou module."""
    with patch('builtins.__import__') as mock_import:
        # Setup mocks
        mock_hou = Mock()
        mock_parent_node = Mock()
        mock_created_nodes = [Mock(), Mock(), Mock()]

        # Configure import mock
        def side_effect(name, *args, **kwargs):
            if name == 'hou':
                return mock_hou
            else:
                return __import__(name, *args, **kwargs)

        mock_import.side_effect = side_effect

        # Configure mock returns
        mock_hou.node.return_value = mock_parent_node
        mock_parent_node.createNode.side_effect = mock_created_nodes

        # Configure created nodes
        for i, created_node in enumerate(mock_created_nodes):
            created_node.path.return_value = f"/obj/geo1/node{i}"
            created_node.parent.return_value.path.return_value = "/obj/geo1"
            created_node.type.return_value.name.return_value = f"type{i}"
            created_node.name.return_value = f"node{i}"

        # Create nodes
        box_node = node("/obj/geo1", "box", name="source")
        xform_node = node("/obj/geo1", "xform", name="transform")
        subdivide_node = node("/obj/geo1", "subdivide", name="refine")

        # Create chain
        processing_chain = chain("/obj/geo1", box_node, xform_node, subdivide_node)

        # Call create
        result = processing_chain.create()

        # Verify results
        assert len(result) == 3
        assert all(created_node in result for created_node in mock_created_nodes)

        # Verify Houdini calls
        assert mock_parent_node.createNode.call_count == 3


def test_chain_create_with_import_error():
    """Test chain .create() method raises ImportError when hou not available."""
    # Create nodes
    box_node = node("/obj/geo1", "box", name="source")
    xform_node = node("/obj/geo1", "xform", name="transform")

    # Create chain
    processing_chain = chain("/obj/geo1", box_node, xform_node)

    # Test that .create() raises ImportError when hou module not available
    with pytest.raises(ImportError, match="Houdini module 'hou' not available"):
        processing_chain.create()


def test_empty_chain():
    """Test behavior with empty chain."""
    # Create empty chain
    empty_chain = chain("/obj/geo1")

    # Test properties
    assert len(empty_chain) == 0
    assert empty_chain._flatten_nodes() == []

    # Test indexing raises appropriate errors
    with pytest.raises(IndexError):
        empty_chain[0]

    # Test create returns empty list
    with pytest.raises(ImportError):  # Will fail on hou import first
        empty_chain.create()


def test_nested_chain_splicing():
    """Test deeply nested chain splicing."""
    # Create individual nodes
    node1 = node("/obj/geo1", "box", name="node1")
    node2 = node("/obj/geo1", "xform", name="node2")
    node3 = node("/obj/geo1", "subdivide", name="node3")
    node4 = node("/obj/geo1", "normal", name="node4")
    node5 = node("/obj/geo1", "output", name="node5")

    # Create nested chains
    inner_chain = chain("/obj/geo1", node2, node3)
    middle_chain = chain("/obj/geo1", node1, inner_chain, node4)
    outer_chain = chain("/obj/geo1", middle_chain, node5)

    # Test flattening
    flattened = outer_chain._flatten_nodes()
    assert len(flattened) == 5
    assert flattened[0] == node1
    assert flattened[1] == node2  # From inner_chain
    assert flattened[2] == node3  # From inner_chain
    assert flattened[3] == node4
    assert flattened[4] == node5

    # Test indexing works through nested splicing
    assert outer_chain["node2"] == node2
    assert outer_chain[1] == node2


if __name__ == "__main__":
    pytest.main([__file__])
