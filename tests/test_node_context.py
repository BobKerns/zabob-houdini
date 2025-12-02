"""
Integration tests for NodeContext class and context function.
"""

import pytest

from tests.conftest import HythonSessionFn


@pytest.mark.integration
class TestNodeContext:
    """Test NodeContext class behavior."""

    def test_node_context_dataclass(self, hython_test: HythonSessionFn):
        """Test NodeContext is a proper dataclass with parent attribute."""
        result = hython_test("h_test_node_context_dataclass")

        assert result['is_context'] is True
        assert result['parent_equal'] is True
        assert result['parent_node_type'] == "geo"
        assert result['parent_name'] == "test_geo"

    def test_node_context_context_manager(self, hython_test: HythonSessionFn):
        """Test NodeContext works as a context manager."""
        result = hython_test("h_test_node_context_context_manager")

        assert result['entered_is_ctx'] is True
        assert result['parent_equal'] is True

    def test_node_context_mutable(self, hython_test: HythonSessionFn):
        """Test NodeContext is mutable (no longer frozen)."""
        result = hython_test("h_test_node_context_mutable")

        assert result['can_modify'] is True
        assert result['nodes_dict_exists'] is True


@pytest.mark.integration
class TestContextFunction:
    """Test context function behavior."""

    def test_context_with_node_instance(self, hython_test: HythonSessionFn):
        """Test context function with NodeInstance parent."""
        result = hython_test("h_test_context_with_node_instance")

        assert result['is_context'] is True
        assert result['parent_is_same'] is True

    def test_context_with_string_path(self, hython_test: HythonSessionFn):
        """Test context function with string path parent."""
        result = hython_test("h_test_context_with_string_path")

        assert result['is_context'] is True
        assert result['is_node_instance'] is True
        assert result['parent_path'] == "/obj"

    def test_context_usage_example(self, hython_test: HythonSessionFn):
        """Test realistic usage pattern with context manager."""
        result = hython_test("h_test_context_usage_example")

        assert result['box_parent_equal'] is True
        assert result['sphere_parent_equal'] is True
        assert result['box_node_type'] == "box"
        assert result['sphere_node_type'] == "sphere"

    def test_context_preserves_parent_type(self, hython_test: HythonSessionFn):
        """Test context function preserves NodeInstance type."""
        result = hython_test("h_test_context_preserves_parent_type")

        assert result['parent_is_same'] is True
        assert result['parent_type_correct'] is True

    def test_node_context_node_method(self, hython_test: HythonSessionFn):
        """Test NodeContext.node() method creates nodes under the context parent."""
        result = hython_test("h_test_node_context_node_method")

        assert result['box_parent_correct'] is True
        assert result['sphere_parent_correct'] is True
        assert result['box_node_type'] == "box"
        assert result['sphere_node_type'] == "sphere"

    def test_node_context_name_lookup(self, hython_test: HythonSessionFn):
        """Test NodeContext name registration and lookup."""
        result = hython_test("h_test_node_context_name_lookup")

        assert result['can_lookup_box'] is True
        assert result['can_lookup_sphere'] is True
        assert result['lookup_returns_same'] is True
        assert result['keyerror_for_missing'] is True

    def test_node_context_integration(self, hython_test: HythonSessionFn):
        """Test full NodeContext workflow with node creation and lookup."""
        result = hython_test("h_test_node_context_integration")

        assert result['created_nodes_count'] == 3
        assert result['all_have_correct_parent'] is True
        assert result['can_access_by_name'] is True
        assert result['node_types_correct'] is True

    def test_node_context_chain_method(self, hython_test: HythonSessionFn):
        """Test NodeContext.chain() method with string name lookup."""
        result = hython_test("h_test_node_context_chain_method")

        assert result['chain_created'] is True
        assert result['chain_length'] == 3
        assert result['string_lookup_worked'] is True
        assert result['nodes_connected'] is True
        assert result['context_preserved'] is True

    def test_node_context_chain_registration(self, hython_test: HythonSessionFn):
        """Test NodeContext.chain() registers new named nodes in context."""
        result = hython_test("h_test_node_context_chain_registration")

        assert result['external_nodes_registered'] is True
        assert result['can_lookup_after_chain'] is True
        assert result['existing_nodes_preserved'] is True

    def test_node_context_merge_method(self, hython_test: HythonSessionFn):
        """Test NodeContext.merge() method with string name lookup."""
        result = hython_test("h_test_node_context_merge_method")

        assert result['merge_created'] is True
        assert result['string_lookup_worked'] is True
        assert result['merge_has_correct_inputs'] is True
        assert result['merge_parent_correct'] is True

    def test_node_context_merge_registration(self, hython_test: HythonSessionFn):
        """Test NodeContext.merge() registers named merge node in context."""
        result = hython_test("h_test_node_context_merge_registration")

        assert result['named_merge_registered'] is True
        assert result['external_nodes_registered'] is True
        assert result['can_lookup_merge'] is True
        assert result['existing_nodes_preserved'] is True

    def test_parent_validation_chain(self, hython_test: HythonSessionFn):
        """Test chain() validates all nodes have same parent."""
        result = hython_test("h_test_parent_validation_chain")

        assert result['validation_works'] is True
        assert result['error_contains_parent'] is True
        assert result['valid_chain_works'] is True

    def test_parent_validation_merge(self, hython_test: HythonSessionFn):
        """Test merge() validates all nodes have same parent."""
        result = hython_test("h_test_parent_validation_merge")

        assert result['validation_works'] is True
        assert result['error_contains_parent'] is True
        assert result['valid_merge_works'] is True

    def test_node_context_parent_validation(self, hython_test: HythonSessionFn):
        """
        Test NodeContext validates nodes have same parent as context.
        @see(`../src/testing/_node_context.py::_test_node_context_parent_validation`)
        """
        result = hython_test("h_test_node_context_parent_validation")

        assert result['chain_validation_works'] is True
        assert result['merge_validation_works'] is True
        assert result['chain_error_mentions_context'] is True
        assert result['merge_error_mentions_context'] is True
