"""
Tests that require Houdini environment.

These tests use the hython_test fixture to safely run tests in Houdini.
"""

import pytest


@pytest.mark.integration
def test_hou_module_available(hython_test):
    """Test that hou module is available in Houdini environment."""
    result = hython_test("test_hou_available")

    assert result['success'] is True
    assert 'result' in result
    result_data = result['result']
    assert "hou_version" in result_data
    assert "hou_app" in result_data
    assert isinstance(result_data["hou_version"], str)
    assert len(result_data["hou_version"]) > 0


@pytest.mark.integration
def test_basic_node_creation_in_houdini(hython_test):
    """Test basic Houdini node creation."""
    result = hython_test("test_basic_node_creation")

    assert result['success'] is True
    assert 'result' in result
    result_data = result['result']
    assert "geo_path" in result_data
    assert "box_path" in result_data
    assert result_data["geo_path"].endswith("test_geo")
    assert result_data["box_path"].endswith("test_box")


@pytest.mark.integration
def test_zabob_node_creation(hython_test):
    """Test Zabob NodeInstance creation and execution in Houdini."""
    result = hython_test("test_zabob_node_creation")

    assert result['success'] is True
    assert 'result' in result
    result_data = result['result']
    assert "created_path" in result_data
    assert "sizex" in result_data
    assert result_data["created_path"].endswith("zabob_box")
    assert abs(float(result_data["sizex"]) - 2.0) < 0.001  # Check sizex parameter was set


@pytest.mark.integration
def test_zabob_chain_creation(hython_test):
    """Test Zabob Chain creation and execution in Houdini."""
    result = hython_test("test_zabob_chain_creation")

    assert result['success'] is True
    assert 'result' in result
    result_data = result['result']
    assert "chain_length" in result_data
    assert "node_paths" in result_data
    assert result_data["chain_length"] == 3
    assert len(result_data["node_paths"]) == 3

    # Verify the node names in the chain
    paths = result_data["node_paths"]
    assert any("chain_box" in path for path in paths)
    assert any("chain_xform" in path for path in paths)
    assert any("chain_subdivide" in path for path in paths)


@pytest.mark.integration
def test_node_input_connections(hython_test):
    """Test node input connections work correctly."""
    result = hython_test("test_node_with_inputs")

    assert result['success'] is True
    assert 'result' in result
    result_data = result['result']
    assert "box_path" in result_data
    assert "xform_path" in result_data
    assert "connection_exists" in result_data
    assert "connected_to" in result_data

    assert result_data["connection_exists"] is True
    assert result_data["connected_to"] == result_data["box_path"]


@pytest.mark.skip(reason="Example of environment-specific test")
@pytest.mark.integration
def test_direct_houdini_check(houdini_available):
    """Example test that checks if running directly in Houdini."""
    if not houdini_available:
        pytest.skip("Not running in Houdini environment")

    # This would only run if we're actually in hython
    assert houdini_available is True
