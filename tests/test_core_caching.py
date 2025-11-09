"""
Tests for caching and copy functionality in zabob_houdini.core.

These tests verify the new caching semantics, copy methods, and memoization.
"""

import pytest
import sys
from unittest.mock import Mock, patch

# Mock hou module for testing
class MockHou:
    class Node:
        def __init__(self, path="/obj/test", node_type="box"):
            self._path = path
            self._node_type = node_type

        def path(self):
            return self._path

        def type(self):
            mock_type = Mock()
            mock_type.name.return_value = self._node_type
            return mock_type

        def createNode(self, node_type, name=None):
            child_path = f"{self._path}/{name or node_type}"
            return MockHou.Node(child_path, node_type)

        def setParms(self, parms):
            pass

        def setInput(self, index, node):
            pass

    @staticmethod
    def node(path):
        """Mock hou.node function."""
        return MockHou.Node(path)

mock_hou = MockHou()
sys.modules['hou'] = mock_hou  # type: ignore

from zabob_houdini.core import NodeInstance, Chain, node, chain


class TestNodeInstanceCaching:
    """Test NodeInstance create() caching behavior."""

    def test_create_caches_result(self):
        """NodeInstance.create() should cache and return same hou.Node on repeated calls."""
        parent_node = MockHou.Node("/obj")

        with patch('hou.node', return_value=parent_node):
            node_instance = NodeInstance("/obj", "box", name="test_box")

            # First call should create the node
            created_node1 = node_instance.create()
            assert created_node1 is not None

            # Second call should return cached node (via @functools.cache)
            created_node2 = node_instance.create()
            assert created_node2 is created_node1  # Same object

    def test_create_different_instances_different_nodes(self):
        """Different NodeInstance objects should create different nodes."""
        parent_node = MockHou.Node("/obj")

        with patch('hou.node', return_value=parent_node):
            node1 = NodeInstance("/obj", "box", name="box1")
            node2 = NodeInstance("/obj", "box", name="box2")

            created1 = node1.create()
            created2 = node2.create()

            assert created1 is not created2
            assert created1.path() != created2.path()


class TestNodeInstanceCopy:
    """Test NodeInstance copy() functionality."""

    def test_copy_creates_independent_instance(self):
        """NodeInstance.copy() should create independent copy."""
        from zabob_houdini.core import node
        original = node("/obj", "box", name="original", sizex=2.0)

        copied = original.copy()

        # Should be different objects
        assert copied is not original

        # Should have same basic properties
        assert copied.parent == original.parent
        assert copied.node_type == original.node_type
        assert copied.name == original.name

        # Attributes should be copied (not shared)
        assert copied.attributes == original.attributes
        assert copied.attributes is not original.attributes

        # Copies should be independent with @functools.cache handling caching automatically

    def test_copy_with_chain_inputs(self):
        """NodeInstance.copy() should copy Chain inputs to avoid shared state."""
        from zabob_houdini.core import node, chain
        inner_node = node("/obj", "sphere")
        inner_chain = chain("/obj", inner_node)

        original = node("/obj", "merge", _input=inner_chain)
        copied = original.copy()

        # Input chain should be copied
        assert copied.inputs is not None
        assert len(copied.inputs) == 1
        assert isinstance(copied.inputs[0], Chain)
        assert copied.inputs[0] is not inner_chain  # Different Chain object

    def test_copy_preserves_non_chain_inputs(self):
        """NodeInstance.copy() should preserve non-Chain inputs as-is."""
        from zabob_houdini.core import node
        # Create a NodeInstance to use as input (valid InputNode type)
        input_node = node("/obj", "box", name="input_box")

        # Create node with multiple inputs including None for sparse connections
        original = node("/obj", "merge", _input=[input_node, None])
        copied = original.copy()

        assert copied.inputs is not None
        assert len(copied.inputs) == 2
        assert copied.inputs[0] is input_node  # Same object (not copied since it's not a Chain)
        assert copied.inputs[1] is None


class TestChainMemoization:
    """Test Chain._flatten_nodes() memoization."""

    def test_flatten_nodes_memoized(self):
        """Chain._flatten_nodes() should cache results."""
        from zabob_houdini.core import node, chain
        node1 = node("/obj", "box")
        node2 = node("/obj", "sphere")
        test_chain = chain("/obj", node1, node2)

        # First call
        flattened1 = test_chain._flatten_nodes()
        assert len(flattened1) == 2

        # Second call should return cached result (via @functools.cache)
        flattened2 = test_chain._flatten_nodes()
        assert flattened2 is flattened1  # Same object

    def test_flatten_handles_nested_chains(self):
        """Chain._flatten_nodes() should properly flatten nested chains."""
        from zabob_houdini.core import node, chain
        node1 = node("/obj", "box")
        node2 = node("/obj", "sphere")
        inner_chain = chain("/obj", node1, node2)

        node3 = node("/obj", "merge")
        outer_chain = chain("/obj", inner_chain, node3)

        flattened = outer_chain._flatten_nodes()
        assert len(flattened) == 3
        assert all(isinstance(n, NodeInstance) for n in flattened)

        # Should be memoized
        flattened2 = outer_chain._flatten_nodes()
        assert flattened2 is flattened


class TestChainCopy:
    """Test Chain copy() functionality."""

    def test_copy_creates_independent_chain(self):
        """Chain.copy() should create independent copy."""
        from zabob_houdini.core import node, chain
        node1 = node("/obj", "box")
        node2 = node("/obj", "sphere")

        # Note: chain() function doesn't support name_prefix or attributes parameters
        # For this test, we'll use a simpler chain and test copy behavior
        original = chain("/obj", node1, node2)

        copied = original.copy()

        # Should be different objects
        assert copied is not original

        # Should have same basic properties
        assert copied.parent == original.parent

        # Nodes should be copied (not shared references)
        assert copied.nodes == original.nodes
        assert copied.nodes is not original.nodes

        # Cache is handled by @functools.cache - copies should be independent

    def test_copy_deep_copies_node_instances(self):
        """Chain.copy() should copy contained NodeInstances."""
        from zabob_houdini.core import node, chain
        node1 = node("/obj", "box", sizex=1.0)
        node2 = node("/obj", "sphere")

        original = chain("/obj", node1, node2)
        copied = original.copy()

        # Nodes should be copied
        assert len(copied.nodes) == 2
        assert isinstance(copied.nodes[0], NodeInstance)
        assert isinstance(copied.nodes[1], NodeInstance)

        # Should be different objects
        assert copied.nodes[0] is not node1
        assert copied.nodes[1] is not node2

        # But should have same properties
        assert copied.nodes[0].node_type == node1.node_type
        assert copied.nodes[0].attributes == node1.attributes

    def test_copy_deep_copies_nested_chains(self):
        """Chain.copy() should recursively copy nested chains."""
        from zabob_houdini.core import node, chain
        inner_node = node("/obj", "box")
        inner_chain = chain("/obj", inner_node)

        outer_node = node("/obj", "merge")
        original = chain("/obj", inner_chain, outer_node)

        copied = original.copy()

        # Should have copied the inner chain
        assert len(copied.nodes) == 2
        assert isinstance(copied.nodes[0], Chain)
        assert isinstance(copied.nodes[1], NodeInstance)

        # Inner chain should be different object
        assert copied.nodes[0] is not inner_chain

        # But should have same structure
        inner_copied = copied.nodes[0]
        assert len(inner_copied.nodes) == 1
        assert isinstance(inner_copied.nodes[0], NodeInstance)
        assert inner_copied.nodes[0].node_type == inner_node.node_type


class TestChainCreateBehavior:
    """Test Chain.create() new return behavior."""

    def test_create_returns_tuple_of_node_instances(self):
        """Chain.create() should return tuple of NodeInstance copies."""
        parent_node = MockHou.Node("/obj")

        with patch('hou.node', return_value=parent_node):
            from zabob_houdini.core import node, chain
            node1 = node("/obj", "box")
            node2 = node("/obj", "sphere")
            test_chain = chain("/obj", node1, node2)

            result = test_chain.create()

            # Should return tuple
            assert isinstance(result, tuple)
            assert len(result) == 2

            # Should contain NodeInstance objects (copies)
            assert all(isinstance(n, NodeInstance) for n in result)

            # Should be different objects than originals (copies)
            assert result[0] is not node1
            assert result[1] is not node2

            # Each should have created node cached
            # NodeInstances should have their hou nodes created via .create()
            assert result[0].create() is not None
            assert result[1].create() is not None

    def test_create_empty_chain_returns_empty_tuple(self):
        """Chain.create() with empty chain should return empty tuple."""
        from zabob_houdini.core import chain
        test_chain = chain("/obj")  # Empty chain
        result = test_chain.create()

        assert isinstance(result, tuple)
        assert len(result) == 0


class TestChainConvenienceMethods:
    """Test Chain convenience methods for accessing created hou.Node instances."""

    def test_convenience_methods_with_created_nodes(self):
        """Test all Chain convenience methods work correctly."""
        parent_node = MockHou.Node("/obj")

        with patch('hou.node', return_value=parent_node):
            from zabob_houdini.core import node, chain
            node1 = node("/obj", "box")
            node2 = node("/obj", "sphere")
            node3 = node("/obj", "merge")
            test_chain = chain("/obj", node1, node2, node3)

            # Test first_node() - should create chain automatically
            first = test_chain.first_node()
            assert isinstance(first, MockHou.Node)

            # Test last_node()
            last = test_chain.last_node()
            assert isinstance(last, MockHou.Node)

            # First and last should be different nodes in a 3-node chain
            assert first is not last

            # Test nodes_iter()
            nodes_list = list(test_chain.nodes_iter())
            assert len(nodes_list) == 3
            assert all(isinstance(node, MockHou.Node) for node in nodes_list)

            # Test hou_nodes()
            all_nodes = test_chain.hou_nodes()
            assert isinstance(all_nodes, tuple)
            assert len(all_nodes) == 3
            assert all(isinstance(node, MockHou.Node) for node in all_nodes)

            # First and last should match nodes from the tuple
            assert first is all_nodes[0]
            assert last is all_nodes[2]

    def test_convenience_methods_empty_chain(self):
        """Test convenience methods on empty chain raise appropriate errors."""
        from zabob_houdini.core import chain
        test_chain = chain("/obj")  # Empty chain

        # Empty chain methods should raise ValueError
        with pytest.raises(ValueError, match="Cannot get first node of empty chain"):
            test_chain.first_node()

        with pytest.raises(ValueError, match="Cannot get last node of empty chain"):
            test_chain.last_node()

        # But iteration methods should work and return empty results
        assert list(test_chain.nodes_iter()) == []
        assert test_chain.hou_nodes() == ()

    def test_convenience_methods_single_node(self):
        """Test convenience methods with single-node chain."""
        parent_node = MockHou.Node("/obj")

        with patch('hou.node', return_value=parent_node):
            from zabob_houdini.core import node, chain
            node1 = node("/obj", "box")
            test_chain = chain("/obj", node1)

            # First and last should be the same node
            first = test_chain.first_node()
            last = test_chain.last_node()
            assert first is last

            # Should have one node in iteration
            nodes_list = list(test_chain.nodes_iter())
            assert len(nodes_list) == 1
            assert nodes_list[0] is first

            # Tuple should have one node
            all_nodes = test_chain.hou_nodes()
            assert len(all_nodes) == 1
            assert all_nodes[0] is first

    def test_create_caching_consistency(self):
        """Test that Chain.create() returns same instances on repeated calls."""
        parent_node = MockHou.Node("/obj")

        with patch('hou.node', return_value=parent_node):
            from zabob_houdini.core import node, chain
            node1 = node("/obj", "box")
            node2 = node("/obj", "sphere")
            test_chain = chain("/obj", node1, node2)

            # Call create multiple times
            first_call = test_chain.create()
            second_call = test_chain.create()
            third_call = test_chain.create()

            # Should get the same tuple of instances
            assert first_call is second_call
            assert second_call is third_call

            # Convenience methods should be consistent with create()
            assert test_chain.first_node() is first_call[0].create()
            assert test_chain.last_node() is first_call[1].create()


if __name__ == "__main__":
    pytest.main([__file__])
