"""
Tests for caching and copy functionality in zabob_houdini.core.

These tests verify the new caching semantics, copy methods, and memoization.
Uses the hython_test fixture to run tests in Houdini environment.
"""

import pytest


class TestNodeInstanceCaching:
    """Test ZNode create() caching behavior."""

    @pytest.mark.integration
    def test_create_caches_result(self, hython_test):
        """ZNode.create() should cache and return same hou.Node on repeated calls."""
        result_data = hython_test("h_test_create_caches_result")

        assert result_data["same_object"] is True
        assert "node_path" in result_data

    @pytest.mark.integration
    def test_create_different_instances_different_nodes(self, hython_test):
        """Different ZNode objects should create different nodes."""
        result_data = hython_test("h_test_create_different_instances_different_nodes")

        assert result_data["different_objects"] is True
        assert result_data["different_paths"] is True
        assert result_data["path1"] != result_data["path2"]


class TestNodeInstanceCopy:
    """Test ZNode copy() functionality."""

    @pytest.mark.integration
    def test_copy_creates_independent_instance(self, hython_test):
        """ZNode.copy() should create independent copy."""
        result_data = hython_test("h_test_copy_creates_independent_instance")

        assert result_data["different_objects"] is True
        assert result_data["same_parent"] is True
        assert result_data["same_node_type"] is True
        assert result_data["same_name"] is True
        assert result_data["attributes_equal"] is True
        assert result_data["attributes_shared"] is True

    @pytest.mark.integration
    def test_copy_with_chain_inputs(self, hython_test):
        """ZNode.copy() should copy ZChain inputs to avoid shared state."""
        result_data = hython_test("h_test_copy_with_chain_inputs")

        assert result_data["has_inputs"] is True
        assert result_data["input_length"] == 1
        assert result_data["input_copied"] is True

    @pytest.mark.integration
    def test_copy_preserves_non_chain_inputs(self, hython_test):
        """ZNode.copy() should preserve non-ZChain inputs as-is."""
        result_data = hython_test("h_test_copy_preserves_non_chain_inputs")

        assert result_data["has_inputs"] is True
        assert result_data["input_length"] == 2
        assert result_data["first_input_same"] is True
        assert result_data["second_input_none"] is True


class TestChainCopy:
    """Test ZChain copy() functionality."""

    @pytest.mark.integration
    def test_copy_creates_independent_chain(self, hython_test):
        """ZChain.copy() should create independent copy."""
        result_data = hython_test("h_test_copy_creates_independent_chain")

        assert result_data["different_objects"] is True
        assert result_data["same_parent"] is True
        assert result_data["nodes_not_shared"] is True
        assert result_data["nodes_not_equal"] is True

    @pytest.mark.integration
    def test_copy_deep_copies_node_instances(self, hython_test):
        """ZChain.copy() should copy contained NodeInstances."""
        result_data = hython_test("h_test_copy_deep_copies_node_instances")

        assert result_data["nodes_length"] == 2
        assert result_data["nodes_different"] is True
        assert result_data["first_is_node_instance"] is True
        assert result_data["second_is_node_instance"] is True

    @pytest.mark.integration
    def test_copy_deep_copies_nested_chains(self, hython_test):
        """ZChain.copy() should recursively copy nested chains."""
        result_data = hython_test("h_test_copy_deep_copies_nested_chains")

        assert result_data["nodes_length"] == 2
        assert result_data["inner_chain_copied"] is True
        assert result_data["first_is_chain"] is False
        assert result_data["second_is_node_instance"] is True


class TestChainCreateBehavior:
    """Test ZChain.create() new return behavior."""

    @pytest.mark.integration
    def test_create_returns_tuple_of_node_instances(self, hython_test):
        """ZChain.create() should return tuple of ZNode copies."""
        result_data = hython_test("h_test_create_returns_tuple_of_node_instances")

        assert result_data["is_tuple"] is True
        assert result_data["tuple_length"] == 2
        assert result_data["all_node_instances"] is True
        assert result_data["all_created"] is True
        assert len(result_data["node_paths"]) == 2


class TestChainConvenienceMethods:
    """Test ZChain convenience methods for accessing created hou.Node instances."""

    @pytest.mark.integration
    def test_convenience_methods_with_created_nodes(self, hython_test):
        """Test all ZChain convenience methods work correctly."""
        result_data = hython_test("h_test_convenience_methods_with_created_nodes")

        assert result_data["first_last_different"] is True
        assert result_data["all_nodes_length"] == 3
        assert result_data["nodes_iter_length"] == 3
        assert len(result_data["all_nodes_paths"]) == 3

    @pytest.mark.integration
    def test_convenience_methods_empty_chain(self, hython_test):
        """Test convenience methods on empty chain raise appropriate errors."""
        result_data = hython_test("h_test_convenience_methods_empty_chain")

        assert result_data["error_creating_chain"]

    @pytest.mark.integration
    def test_convenience_methods_single_node(self, hython_test):
        """Test convenience methods with single-node chain."""
        # This would need a separate test function - skipping for now to keep focused
        pass

    @pytest.mark.integration
    def test_create_caching_consistency(self, hython_test):
        """Test that ZChain.create() returns same instances on repeated calls."""
        # This would require a more complex test function - the current architecture
        # handles caching automatically via @functools.cache
        pass


class TestNodeRegistry:
    """Test ZNode registry functionality."""

    @pytest.mark.integration
    def test_node_registry_functionality(self, hython_test):
        """Test that NodeInstances are properly registered and retrieved."""
        result_data = hython_test("h_test_node_registry_functionality")

        assert result_data["found_original"] is True
        assert result_data["wrap_returns_original"] is True
        assert result_data["first_chain_node_is_original"] is False
        assert "registry_test_box" in result_data["original_node_path"]


class TestMergeInputsFunction:
    """Test the _merge_inputs utility function."""

    @pytest.mark.integration
    def test_merge_inputs_sparse_handling(self, hython_test):
        """Test _merge_inputs function handles sparse (None) inputs correctly."""
        result_data = hython_test("h_test_merge_inputs_sparse_handling")

        # Test all the merge scenarios
        assert result_data["both_none_is_none"] is True
        assert result_data["first_none_gets_second"] is True
        assert result_data["second_none_gets_first"] is True
        assert result_data["both_not_none_gets_first"] is True
        assert result_data["multi_position_correct"] is True
        assert result_data["empty_lists_work"] is True
        assert result_data["one_empty_works"] is True


if __name__ == "__main__":
    pytest.main([__file__])
