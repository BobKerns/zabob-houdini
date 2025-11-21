"""
Test for the layout algorithm stress test.

This test runs the comprehensive layout stress test and validates the results.
"""

import pytest


@pytest.mark.integration
def test_layout_stress_test(hython_test):
    """Test the layout algorithm with complex graph structures."""
    result = hython_test("_test_layout_stress_test")
    assert 'total_nodes' in result
    assert 'source_nodes' in result
    assert 'sink_nodes' in result
    assert 'num_layers' in result
    assert 'nodes_per_layer' in result
    assert 'layout_stats' in result

    # Verify we created a substantial graph
    assert result['total_nodes'] >= 20, f"Expected at least 20 nodes, got {result['total_nodes']}"
    assert result['num_layers'] >= 3, f"Expected at least 3 layers, got {result['num_layers']}"

    # Verify layout produces reasonable bounds
    layout_stats = result['layout_stats']
    if layout_stats:
        assert 'total_width' in layout_stats
        assert 'total_height' in layout_stats
        assert layout_stats['total_width'] > 0, "Layout should have positive width"
        assert layout_stats['total_height'] > 0, "Layout should have positive height"

    print(f"\nLayout Stress Test Results:")
    print(f"  Total nodes: {result['total_nodes']}")
    print(f"  Source nodes: {result['source_nodes']}")
    print(f"  Sink nodes: {result['sink_nodes']}")
    print(f"  Layers: {result['num_layers']}")
    print(f"  Nodes per layer: {result['nodes_per_layer']}")

    if layout_stats:
        print(f"  Layout width: {layout_stats['total_width']:.2f}")
        print(f"  Layout height: {layout_stats['total_height']:.2f}")


@pytest.mark.integration
def test_simple_layout_demo(hython_test):
    """Test a simpler layout demo to verify basic functionality."""
    test_result = hython_test("_test_simple_layout_demo")
    assert 'positions' in test_result
    assert len(test_result['positions']) > 0

    # Verify positions are reasonable
    positions = test_result['positions']
    x_coords = [pos['x'] for pos in positions.values()]
    y_coords = [pos['y'] for pos in positions.values()]

    print(f"\nSimple Layout Test Results:")
    print(f"  Nodes positioned: {len(positions)}")
    print(f"  X range: {min(x_coords):.2f} to {max(x_coords):.2f}")
    print(f"  Y range: {min(y_coords):.2f} to {max(y_coords):.2f}")
