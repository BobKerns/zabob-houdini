"""
Tests that require Houdini environment.

These tests use the hython_test fixture to safely run tests in Houdini.
"""

import pytest


def test_hou_module_available(hython_test):
    """Test that hou module is available in Houdini environment."""
    result = hython_test("test_hou_available")

    assert result["success"] is True
    assert "hou_version" in result
    assert "hou_app" in result
    assert isinstance(result["hou_version"], str)
    assert len(result["hou_version"]) > 0


def test_basic_node_creation_in_houdini(hython_test):
    """Test basic Houdini node creation."""
    result = hython_test("test_basic_node_creation")

    assert result["success"] is True
    assert "geo_path" in result
    assert "box_path" in result
    assert result["geo_path"].endswith("test_geo")
    assert result["box_path"].endswith("test_box")


def test_zabob_node_creation(hython_test):
    """Test Zabob NodeInstance creation and execution in Houdini."""
    result = hython_test("test_zabob_node_creation")

    assert result["success"] is True
    assert "created_path" in result
    assert "sizex" in result
    assert result["created_path"].endswith("zabob_box")
    assert abs(result["sizex"] - 2.0) < 0.001  # Check sizex parameter was set


def test_zabob_chain_creation(hython_test):
    """Test Zabob Chain creation and execution in Houdini."""
    result = hython_test("test_zabob_chain_creation")

    assert result["success"] is True
    assert "chain_length" in result
    assert "node_paths" in result
    assert result["chain_length"] == 3
    assert len(result["node_paths"]) == 3

    # Verify the node names in the chain
    paths = result["node_paths"]
    assert any("chain_box" in path for path in paths)
    assert any("chain_xform" in path for path in paths)
    assert any("chain_subdivide" in path for path in paths)


def test_node_input_connections(hython_test):
    """Test node input connections work correctly."""
    result = hython_test("test_node_with_inputs")

    assert result["success"] is True
    assert "box_path" in result
    assert "xform_path" in result
    assert "connection_exists" in result
    assert "connected_to" in result

    assert result["connection_exists"] is True
    assert result["connected_to"] == result["box_path"]


@pytest.mark.skip(reason="Example of environment-specific test")
def test_direct_houdini_check(houdini_available):
    """Example test that checks if running directly in Houdini."""
    if not houdini_available:
        pytest.skip("Not running in Houdini environment")

    # This would only run if we're actually in hython
    assert houdini_available is True
