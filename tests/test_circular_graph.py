"""
Unit tests for circular graph construction.

Tests the ability to construct circular/cyclic node graphs where nodes
reference each other in a loop.
"""

import pytest

# @pytest.skip("Circular work in progress", allow_module_level=True)


@pytest.mark.integration
def test_circular_three_node_cycle(hython_test):
    """Test creating a 3-node circular graph."""
    result = hython_test("test_circular_three_node_cycle")
    assert result["success"] is True
    assert result["node_count"] == 3
    assert result["has_cycle"] is True


@pytest.mark.integration
def test_self_referencing_node(hython_test):
    """Test a node that references itself."""
    result = hython_test("test_self_referencing_node")
    assert result["success"] is True
    assert result["node_count"] == 1
    assert result["has_self_reference"] is True


@pytest.mark.integration
def test_two_node_cycle(hython_test):
    """Test a simple 2-node cycle: A -> B -> A."""
    result = hython_test("test_two_node_cycle")
    assert result["success"] is True
    assert result["node_count"] == 2
    assert result["has_cycle"] is True


@pytest.mark.integration
def test_circular_with_context(hython_test):
    """Test circular graph construction using NodeContext."""
    result = hython_test("test_circular_with_context")
    assert result["success"] is True
    assert result["node_count"] == 3
    assert result["has_cycle"] is True


@pytest.mark.integration
def test_complex_intersecting_cycles(hython_test):
    """Test a graph with multiple intersecting cycles."""
    result = hython_test("test_complex_intersecting_cycles")
    assert result["success"] is True
    assert result["node_count"] == 5
    assert result["cycle_count"] == 2
