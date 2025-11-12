"""
Test parameter validation and error handling.

All tests use the hython_test fixture to run in Houdini environment
since they need access to the zabob-houdini API.
"""

import pytest


class TestParameterValidation:
    """Test parameter validation and error handling."""

    @pytest.mark.integration
    def test_chain_rejects_input_parameter(self, hython_test):
        """Test that chain() properly rejects the deprecated _input parameter."""
        result = hython_test("test_chain_rejects_input_parameter")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        # Check that the error message contains the expected guidance
        assert result_data["error_contains_input"] is True
        assert result_data["error_contains_no_longer_supported"] is True
        assert result_data["error_contains_guidance"] is True

    @pytest.mark.integration
    def test_valid_input_patterns(self, hython_test):
        """Test that valid input patterns work correctly."""
        result = hython_test("test_valid_input_patterns")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        # Verify they were created successfully
        assert result_data["chain_B_length"] == 2
        assert result_data["chain_C_length"] == 2
        assert result_data["chain_B_has_inputs"] is True
        assert result_data["chain_C_no_inputs"] is True

    @pytest.mark.integration
    def test_node_input_validation(self, hython_test):
        """Test that individual node input validation works."""
        result = hython_test("test_node_input_validation")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        assert result_data["single_input_works"] is True
        assert result_data["multiple_inputs_work"] is True
        assert result_data["no_inputs_work"] is True

    @pytest.mark.integration
    @pytest.mark.parametrize("invalid_input", [
        "none",  # None should be filtered out
        "empty_string",    # Empty string should cause issues
        "number",   # Numbers should cause issues
    ])
    def test_invalid_input_types(self, hython_test, invalid_input):
        """Test that invalid input types are handled appropriately."""
        result = hython_test("test_invalid_input_types", invalid_input)

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        if invalid_input == "none":
            # None should be filtered out and result in no inputs
            assert result_data["none_filtered_out"] is True
        else:
            # Other types should be handled (specific behavior depends on implementation)
            assert "handled_appropriately" in result_data

    @pytest.mark.integration
    def test_parameter_validation_comprehensive(self, hython_test):
        """Test comprehensive parameter validation in Houdini environment."""
        result = hython_test("test_parameter_validation")

        assert result['success'] is True
        assert 'result' in result
        result_data = result['result']

        assert result_data["valid_patterns_work"] is True
        assert result_data["invalid_patterns_rejected"] is True
