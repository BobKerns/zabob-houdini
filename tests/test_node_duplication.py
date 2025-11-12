"""
Test for node duplication bug in diamond patterns.

This test should catch the issue where nodes are being duplicated
instead of properly referenced in diamond connection patterns.
"""

import pytest


class TestNodeDuplication:
    """Test that nodes are not duplicated in diamond patterns."""

    @pytest.mark.integration
    def test_diamond_no_duplication(self, hython_test):
        """Test that diamond pattern doesn't create duplicate nodes."""
        result = hython_test("test_diamond_no_duplication")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        # The key test: all nodes should be unique (no duplicates)
        all_node_paths = result_data['all_node_paths']
        unique_node_paths = result_data['unique_node_paths']

        assert len(all_node_paths) == len(unique_node_paths), (
            f"Node duplication detected! "
            f"All nodes: {len(all_node_paths)}, "
            f"Unique nodes: {len(unique_node_paths)}, "
            f"Paths: {all_node_paths}"
        )

        # Verify the connections are correct
        assert result_data['scale_up_connected_to_center'] is True
        assert result_data['scale_down_connected_to_center'] is True

        # Both should connect to the SAME center node
        assert result_data['both_connect_to_same_center'] is True

    @pytest.mark.integration
    def test_chain_reference_vs_copy(self, hython_test):
        """Test that chains are referenced, not copied when used as inputs."""
        result = hython_test("test_chain_reference_vs_copy")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        # When chain A is used as input to multiple nodes,
        # the nodes in chain A should only be created once
        chain_a_nodes = result_data['chain_a_node_count']
        all_created_nodes = result_data['total_created_node_count']

        # This should be equal - chain A nodes shouldn't be duplicated
        expected_total = chain_a_nodes + result_data['other_nodes_count']

        assert all_created_nodes == expected_total, (
            f"Node duplication detected in chain references! "
            f"Chain A has {chain_a_nodes} nodes, "
            f"Other nodes: {result_data['other_nodes_count']}, "
            f"Total created: {all_created_nodes}, "
            f"Expected: {expected_total}"
        )
