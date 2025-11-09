"""
Tests that require Houdini environment via hython fixture.
"""

import pytest


def test_houdini_availability(houdini_available):
    """Test that we can detect Houdini availability."""
    # This test works regardless of environment
    assert isinstance(houdini_available, bool)


def test_basic_houdini_integration(hython_required):
    """Test basic Houdini integration via hython fixture."""
    result = hython_required("test_hou_available")

    # Parse result (it comes back as string from subprocess)
    if isinstance(result, str):
        # When run via subprocess, we get string output
        assert "success" in result.lower()
    else:
        # When run directly in hython, we get dict
        assert result["success"] is True
        assert "hou_version" in result
        assert "hou_app" in result


def test_zabob_node_creation_in_hython(hython_required):
    """Test Zabob node creation via hython fixture."""
    result = hython_required("test_zabob_node_creation")

    if isinstance(result, str):
        # Subprocess result
        assert "success" in result.lower()
        assert "created_path" in result
    else:
        # Direct result
        assert result["success"] is True
        assert result["sizex"] == 2.0  # We set sizex=2.0 in the test


def test_zabob_chain_creation_in_hython(hython_required):
    """Test Zabob chain creation via hython fixture."""
    result = hython_required("test_zabob_chain_creation")

    if isinstance(result, str):
        # Subprocess result
        assert "success" in result.lower()
        assert "chain_length" in result
    else:
        # Direct result
        assert result["success"] is True
        assert result["chain_length"] == 3  # box, xform, subdivide


def test_node_input_connections_in_hython(hython_required):
    """Test node input connections via hython fixture."""
    result = hython_required("test_node_with_inputs")

    if isinstance(result, str):
        # Subprocess result
        assert "success" in result.lower()
        assert "connection_exists" in result
    else:
        # Direct result
        assert result["success"] is True
        assert result["connection_exists"] is True
        assert result["connected_to"] is not None


@pytest.mark.skip(reason="Example of conditional skip based on environment")
def test_direct_houdini_only(houdini_available):
    """Example test that only runs when directly in Houdini."""
    if not houdini_available:
        pytest.skip("This test requires running directly in hython")

    import hou  # This import only works in hython
    assert hou.applicationName() is not None
