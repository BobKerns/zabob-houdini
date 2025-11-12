"""
Test input connection architecture and functionality.

These tests use the hython_test fixture to run in Houdini environment.
"""

import pytest


class TestInputConnections:
    """Test input connection architecture and functionality."""

    @pytest.mark.integration
    def test_input_connections_basic(self, hython_test):
        """Test that input connections are set up correctly on nodes."""
        result = hython_test("test_basic_input_connections")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        # Verify chain structure
        assert result_data["chain_A_length"] == 2
        assert result_data["chain_B2_length"] == 2
        assert result_data["chain_B3_length"] == 2
        assert result_data["chain_C_length"] == 2

        # Check architecture - chains should NOT have _inputs field
        assert result_data["chains_no_inputs_field"] is True

        # Check delegation works
        assert result_data["chain_A_no_inputs"] is True
        assert result_data["chain_B2_has_inputs"] is True
        assert result_data["chain_B3_has_inputs"] is True
        assert result_data["chain_C_has_inputs"] is True

    @pytest.mark.integration
    def test_chain_input_delegation(self, hython_test):
        """Test that Chain.inputs properly delegates to first node."""
        result = hython_test("test_chain_input_delegation")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        assert result_data["no_input_chain_empty"] is True
        assert result_data["single_input_chain_has_one"] is True
        assert result_data["delegation_works"] is True

    @pytest.mark.integration
    def test_multiple_inputs_basic(self, hython_test):
        """Test that nodes can accept multiple inputs correctly."""
        result = hython_test("test_multiple_inputs_basic")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        # Test that merge node can accept multiple chain inputs
        assert result_data["merge_has_multiple_inputs"] is True
        assert result_data["input_count"] >= 2
