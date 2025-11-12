"""
Integration tests for actual node creation in Houdini.

These tests require hython and test the full creation pipeline.
"""

import pytest


def test_diamond_pattern_creation(hython_test):
    """Test that diamond pattern creates nodes correctly without duplication."""

    # This test will be run in hython via the test bridge
    result = hython_test("test_diamond_creation")

    # The test function should return success and validation data
    assert result['success']

    # Check that the expected nodes were created
    validation_data = result['result']
    assert 'node_paths' in validation_data
    assert 'connections_valid' in validation_data

    # Verify no duplicate nodes were created
    node_paths = validation_data['node_paths']
    assert len(set(node_paths)) == len(node_paths), "Duplicate nodes detected"


def test_chain_input_connections(hython_test):
    """Test that chain input connections work correctly in actual Houdini."""

    result = hython_test("test_chain_connections")

    assert result['success']

    # Verify connection data
    validation_data = result['result']
    assert 'connections_valid' in validation_data
    assert validation_data['connections_valid'], "Connections are not valid"


def test_multiple_input_merge(hython_test):
    """Test that merge nodes with multiple inputs work correctly."""

    result = hython_test("test_merge_connections")

    assert result['success']

    # Verify merge behavior
    validation_data = result['result']
    assert 'merge_inputs' in validation_data
    assert validation_data['merge_inputs'] >= 2, "Merge node should have multiple inputs"


@pytest.mark.parametrize("node_type", ["box", "sphere", "tube", "grid"])
def test_geometry_creation(hython_test, node_type):
    """Test creation of various geometry types."""

    result = hython_test("test_geometry_node_creation", node_type)

    assert result['success']

    # Verify the node was created with correct type
    validation_data = result['result']
    assert validation_data.get('node_type') == node_type


def test_parameter_setting(hython_test):
    """Test that node parameters are set correctly."""

    result = hython_test("test_node_parameters")

    assert result['success']

    # Verify parameters were applied
    validation_data = result['result']
    assert 'parameters_set' in validation_data
    assert validation_data['parameters_set'], "Parameters were not set correctly"
