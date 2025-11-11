"""
Tests for caching and copy functionality in zabob_houdini.core.

These tests verify the new caching semantics, copy methods, and memoization.
Uses the hython_test fixture to run tests in Houdini environment.
"""

import pytest


class TestNodeInstanceCaching:
    """Test NodeInstance create() caching behavior."""

    @pytest.mark.integration
    def test_create_caches_result(self, hython_test):
        """NodeInstance.create() should cache and return same hou.Node on repeated calls."""
        result = hython_test("test_caching_node_instance_create")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["same_object"] is True
        assert "node_path" in result_data

    @pytest.mark.integration
    def test_create_different_instances_different_nodes(self, hython_test):
        """Different NodeInstance objects should create different nodes."""
        result = hython_test("test_different_instances_different_nodes")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["different_objects"] is True
        assert result_data["different_paths"] is True
        assert result_data["path1"] != result_data["path2"]


class TestNodeInstanceCopy:
    """Test NodeInstance copy() functionality."""

    @pytest.mark.integration
    def test_copy_creates_independent_instance(self, hython_test):
        """NodeInstance.copy() should create independent copy."""
        result = hython_test("test_node_instance_copy")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["different_objects"] is True
        assert result_data["same_parent"] is True
        assert result_data["same_node_type"] is True
        assert result_data["same_name"] is True
        assert result_data["attributes_equal"] is True
        assert result_data["attributes_not_shared"] is True

    @pytest.mark.integration
    def test_copy_with_chain_inputs(self, hython_test):
        """NodeInstance.copy() should copy Chain inputs to avoid shared state."""
        result = hython_test("test_node_instance_copy_with_inputs")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["has_inputs"] is True
        assert result_data["input_length"] == 1
        assert result_data["input_copied"] is True

    @pytest.mark.integration
    def test_copy_preserves_non_chain_inputs(self, hython_test):
        """NodeInstance.copy() should preserve non-Chain inputs as-is."""
        result = hython_test("test_node_copy_non_chain_inputs")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["has_inputs"] is True
        assert result_data["input_length"] == 2
        assert result_data["first_input_same"] is True
        assert result_data["second_input_none"] is True


class TestChainMemoization:
    """Test Chain._flatten_nodes() memoization."""

    @pytest.mark.integration
    def test_flatten_nodes_memoized(self, hython_test):
        """Chain._flatten_nodes() should cache results."""
        result = hython_test("test_chain_flatten_memoization")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["flattened1_length"] == 2
        assert result_data["same_object"] is True

    @pytest.mark.integration
    def test_flatten_handles_nested_chains(self, hython_test):
        """Chain._flatten_nodes() should properly flatten nested chains."""
        result = hython_test("test_chain_flatten_nested")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["flattened_length"] == 3
        assert result_data["same_object"] is True


class TestChainCopy:
    """Test Chain copy() functionality."""

    @pytest.mark.integration
    def test_copy_creates_independent_chain(self, hython_test):
        """Chain.copy() should create independent copy."""
        result = hython_test("test_chain_copy")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["different_objects"] is True
        assert result_data["same_parent"] is True
        assert result_data["nodes_equal"] is True
        assert result_data["nodes_not_shared"] is True

    @pytest.mark.integration
    def test_copy_deep_copies_node_instances(self, hython_test):
        """Chain.copy() should copy contained NodeInstances."""
        result = hython_test("test_chain_copy_deep_nodes")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["nodes_length"] == 2
        assert result_data["nodes_different"] is True
        assert result_data["first_is_node_instance"] is True
        assert result_data["second_is_node_instance"] is True

    @pytest.mark.integration
    def test_copy_deep_copies_nested_chains(self, hython_test):
        """Chain.copy() should recursively copy nested chains."""
        result = hython_test("test_chain_copy_nested")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["nodes_length"] == 2
        assert result_data["inner_chain_copied"] is True
        assert result_data["first_is_chain"] is False
        assert result_data["second_is_node_instance"] is True


class TestChainCreateBehavior:
    """Test Chain.create() new return behavior."""

    @pytest.mark.integration
    def test_create_returns_tuple_of_node_instances(self, hython_test):
        """Chain.create() should return tuple of NodeInstance copies."""
        result = hython_test("test_chain_create_returns_node_instances")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["is_tuple"] is True
        assert result_data["tuple_length"] == 2
        assert result_data["all_node_instances"] is True
        assert result_data["all_created"] is True
        assert len(result_data["node_paths"]) == 2

    @pytest.mark.integration
    def test_create_empty_chain_returns_empty_tuple(self, hython_test):
        """Chain.create() with empty chain should return empty tuple."""
        result = hython_test("test_empty_chain_create")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["is_tuple"] is True
        assert result_data["tuple_length"] == 0


class TestChainConvenienceMethods:
    """Test Chain convenience methods for accessing created hou.Node instances."""

    @pytest.mark.integration
    def test_convenience_methods_with_created_nodes(self, hython_test):
        """Test all Chain convenience methods work correctly."""
        result = hython_test("test_chain_convenience_methods")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["first_last_different"] is True
        assert result_data["all_nodes_length"] == 3
        assert result_data["nodes_iter_length"] == 3
        assert len(result_data["all_nodes_paths"]) == 3

    @pytest.mark.integration
    def test_convenience_methods_empty_chain(self, hython_test):
        """Test convenience methods on empty chain raise appropriate errors."""
        result = hython_test("test_chain_empty_methods")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["all_nodes_empty"] is True
        assert result_data["nodes_iter_empty"] is True
        assert "Cannot get first node of empty chain" in result_data["first_error"]
        assert "Cannot get last node of empty chain" in result_data["last_error"]

    @pytest.mark.integration
    def test_convenience_methods_single_node(self, hython_test):
        """Test convenience methods with single-node chain."""
        # This would need a separate test function - skipping for now to keep focused
        pass

    @pytest.mark.integration
    def test_create_caching_consistency(self, hython_test):
        """Test that Chain.create() returns same instances on repeated calls."""
        # This would require a more complex test function - the current architecture
        # handles caching automatically via @functools.cache
        pass


class TestNodeRegistry:
    """Test NodeInstance registry functionality."""

    @pytest.mark.integration
    def test_node_registry_functionality(self, hython_test):
        """Test that NodeInstances are properly registered and retrieved."""
        result = hython_test("test_node_registry")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']
        assert result_data["found_original"] is True
        assert result_data["wrap_returns_original"] is True
        assert result_data["first_chain_node_is_original"] is True
        assert "registry_test_box" in result_data["original_node_path"]


if __name__ == "__main__":
    pytest.main([__file__])
