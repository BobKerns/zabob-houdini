"""
Integration tests for actual node creation in Houdini.

These tests require hython and test the full creation pipeline.
"""

import pytest


def test_diamond_pattern_creation(hython_test):
    """Test that diamond pattern creates nodes correctly without duplication."""

    # This test will be run in hython via the test bridge
    validation_data = hython_test("_test_diamond_pattern_creation")

    # Check that the expected nodes were created
    assert 'node_paths' in validation_data
    assert 'connections_valid' in validation_data

    # Verify no duplicate nodes were created
    node_paths = validation_data['node_paths']
    assert len(set(node_paths)) == len(node_paths), "Duplicate nodes detected"


def test_chain_input_connections(hython_test):
    """Test that chain input connections work correctly in actual Houdini."""

    validation_data = hython_test("_test_chain_input_connections")

    # Verify connection data
    assert 'connections_valid' in validation_data
    assert validation_data['connections_valid'], "Connections are not valid"


def test_multiple_input_merge(hython_test):
    """Test that merge nodes with multiple inputs work correctly."""

    validation_data = hython_test("_test_multiple_input_merge")

    # Verify merge behavior
    assert 'merge_inputs' in validation_data
    assert validation_data['merge_inputs'] >= 2, "Merge node should have multiple inputs"


@pytest.mark.parametrize("node_type", ["box", "sphere", "tube", "grid"])
def test_geometry_creation(hython_test, node_type):
    """Test creation of various geometry types."""

    validation_data = hython_test("_test_geometry_creation", node_type)

    # Verify the node was created with correct type
    assert validation_data.get('node_type') == node_type


def test_parameter_setting(hython_test):
    """Test that node parameters are set correctly."""

    validation_data = hython_test("_test_parameter_setting")

    # Verify parameters were applied
    assert 'parameters_set' in validation_data
    assert validation_data['parameters_set'], "Parameters were not set correctly"
