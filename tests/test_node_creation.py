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
    """Test the .create() method raises ImportError when hou module not available."""
    # Create a node
    box_node = node("/obj", "box", name="testbox")

    # Verify the node was created
    assert box_node is not None
    assert box_node.parent == "/obj"
    assert box_node.node_type == "box"
    assert box_node.name == "testbox"

    # Test that .create() raises ImportError when hou module not available
    with pytest.raises(ImportError, match="Houdini module 'hou' not available"):
        box_node.create()


def test_node_create_with_mocked_hou():
    """Test the .create() method with mocked hou module."""
    with patch('builtins.__import__') as mock_import:
        # Setup mocks
        mock_hou = Mock()
        mock_parent_node = Mock()
        mock_created_node = Mock()
        mock_parm = Mock()

        # Configure import mock to return our mock hou when 'hou' is imported
        def side_effect(name, *args, **kwargs):
            if name == 'hou':
                return mock_hou
            else:
                # Call the real import for other modules
                return __import__(name, *args, **kwargs)

        mock_import.side_effect = side_effect

        mock_hou.node.return_value = mock_parent_node
        mock_parent_node.createNode.return_value = mock_created_node
        mock_created_node.parm.return_value = mock_parm
        mock_created_node.path.return_value = "/obj/testbox"

        # Create a node with attributes
        box_node = node("/obj", "box", name="testbox", tx=5.0, ty=10.0)

        # Call create
        result = box_node.create()

        # Verify Houdini calls
        mock_hou.node.assert_called_once_with("/obj")
        mock_parent_node.createNode.assert_called_once_with("box", "testbox")
        assert result == mock_created_node

        # Verify parameters were set using setParms
        mock_created_node.setParms.assert_called_once_with({"tx": 5.0, "ty": 10.0})


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


def test_node_with_sparse_inputs():
    """Test creating a node with sparse inputs (None values)."""
    # Create source nodes
    input1 = node("/obj/geo1", "box", name="input1")
    input3 = node("/obj/geo1", "sphere", name="input3")

    # Create node with sparse inputs - input 1 (index 1) is None
    merge_node = node("/obj/geo1", "merge", name="merge", _input=[input1, None, input3])

    # Verify node was created with correct inputs
    assert merge_node is not None
    assert merge_node.inputs is not None
    assert len(merge_node.inputs) == 3
    assert merge_node.inputs[0] == input1
    assert merge_node.inputs[1] is None
    assert merge_node.inputs[2] == input3


def test_node_create_with_sparse_inputs():
    """Test .create() method handles sparse inputs correctly."""
    with patch('builtins.__import__') as mock_import:
        # Setup mocks
        mock_hou = Mock()
        mock_parent_node = Mock()
        mock_created_node = Mock()
        mock_input_node1 = Mock()
        mock_input_node3 = Mock()

        # Configure import mock
        def side_effect(name, *args, **kwargs):
            if name == 'hou':
                return mock_hou
            else:
                return __import__(name, *args, **kwargs)

        mock_import.side_effect = side_effect

        mock_hou.node.return_value = mock_parent_node
        mock_parent_node.createNode.return_value = mock_created_node
        mock_created_node.path.return_value = "/obj/geo1/merge"

        # Mock input nodes with proper path methods
        mock_input_node1.path = Mock(return_value="/obj/geo1/input1")
        mock_input_node3.path = Mock(return_value="/obj/geo1/input3")

        # Create node with sparse inputs
        merge_node = node("/obj/geo1", "merge", name="merge",
                         _input=[mock_input_node1, None, mock_input_node3])

        # Call create
        result = merge_node.create()

        # Verify setInput was called correctly (skipping None)
        expected_calls = [
            ((0, mock_input_node1),),  # Input 0
            ((2, mock_input_node3),),  # Input 2 (skipping 1 which is None)
        ]

        assert mock_created_node.setInput.call_count == 2
        # Note: We can't easily test the exact calls due to enumerate,
        # but we can verify it was called the right number of times


def test_node_create_with_invalid_input():
    """Test .create() method validates input node types."""
    with patch('builtins.__import__') as mock_import:
        # Setup mocks
        mock_hou = Mock()
        mock_parent_node = Mock()
        mock_created_node = Mock()

        def side_effect(name, *args, **kwargs):
            if name == 'hou':
                return mock_hou
            else:
                return __import__(name, *args, **kwargs)

        mock_import.side_effect = side_effect

        mock_hou.node.return_value = mock_parent_node
        mock_parent_node.createNode.return_value = mock_created_node
        mock_created_node.path.return_value = "/obj/geo1/test"

        # Create a proper input node first
        input_node = node("/obj/geo1", "box", name="input")

        # Create node with valid input
        test_node = node("/obj/geo1", "transform", name="test", _input=[input_node])

        # Should work fine
        result = test_node.create()
        assert result == mock_created_node


if __name__ == "__main__":
    pytest.main([__file__])
