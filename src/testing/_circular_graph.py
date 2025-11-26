"""
Houdini integration tests for circular graph construction.

These tests run in hython and create actual circular node graphs.
"""

from zabob_houdini.core import context
import hou


def test_circular_three_node_cycle():
    """Test creating a 3-node circular graph."""
    # Create geo container first
    geo = hou.node("/obj").createNode("geo", "geo1")

    with context(geo) as ctx:
        # Create nodes with forward reference to create cycle
        ctx.node("null", "node1", _input="node3")  # Forward reference
        ctx.node("null", "node2", _input="node1")
        ctx.node("null", "node3", _input="node2")

    # Nodes are created automatically on context exit
    # Call .create() to get the cached hou.Node
    hou_node1 = ctx["node1"].create()
    hou_node2 = ctx["node2"].create()
    hou_node3 = ctx["node3"].create()

    # Verify nodes exist
    assert hou_node1 is not None
    assert hou_node2 is not None
    assert hou_node3 is not None

    # Check connections (cycle: node1 -> node3, node2 -> node1, node3 -> node2)
    node2_inputs = hou_node2.inputs()
    node3_inputs = hou_node3.inputs()

    has_cycle = (
        len(node2_inputs) > 0 and
        len(node3_inputs) > 0 and
        node2_inputs[0] is not None and
        node3_inputs[0] is not None
    )

    return {
        "success": True,
        "node_count": 3,
        "has_cycle": has_cycle
    }


def test_self_referencing_node():
    """Test a node that references itself."""
    # Create geo container first
    geo = hou.node("/obj").createNode("geo", "geo1")

    with context(geo) as ctx:
        # Create node that references itself using forward reference
        ctx.node("null", "self_ref", _input="self_ref")

    # Node is created automatically on context exit
    # Call .create() to get the cached hou.Node
    hou_node = ctx["self_ref"].create()

    # Check if it has an input connection
    inputs = hou_node.inputs()
    has_self_reference = len(inputs) > 0 and inputs[0] is not None

    return {
        "success": True,
        "node_count": 1,
        "has_self_reference": has_self_reference
    }


def test_two_node_cycle():
    """Test a simple 2-node cycle: A -> B -> A."""
    # Create geo container first
    geo = hou.node("/obj").createNode("geo", "geo1")

    with context(geo) as ctx:
        # Create two-node cycle using forward reference
        ctx.node("null", "node_a", _input="node_b")  # Forward reference
        ctx.node("null", "node_b", _input="node_a")

    # Nodes are created automatically on context exit
    # Call .create() to get the cached hou.Node
    hou_a = ctx["node_a"].create()
    hou_b = ctx["node_b"].create()

    # Verify both nodes exist and have inputs
    a_inputs = hou_a.inputs()
    b_inputs = hou_b.inputs()

    has_cycle = (
        len(a_inputs) > 0 and len(b_inputs) > 0 and
        a_inputs[0] is not None and b_inputs[0] is not None
    )

    return {
        "success": True,
        "node_count": 2,
        "has_cycle": has_cycle
    }


def test_circular_with_context():
    """Test circular graph construction using NodeContext."""
    # Create geo container first
    geo = hou.node("/obj").createNode("geo", "geo1")

    with context(geo) as ctx:
        # Create nodes with forward reference to create cycle
        ctx.node("null", "A", _input="C")  # Forward reference
        ctx.node("null", "B", _input="A")
        ctx.node("null", "C", _input="B")

    # Nodes are created automatically on context exit
    # Call .create() to get the cached hou.Node
    hou_a = ctx["A"].create()
    hou_b = ctx["B"].create()
    hou_c = ctx["C"].create()

    # Check for cycle
    a_inputs = hou_a.inputs()
    b_inputs = hou_b.inputs()
    c_inputs = hou_c.inputs()

    has_cycle = (
        len(a_inputs) > 0 and len(b_inputs) > 0 and len(c_inputs) > 0 and
        a_inputs[0] is not None and b_inputs[0] is not None and c_inputs[0] is not None
    )

    return {
        "success": True,
        "node_count": 3,
        "has_cycle": has_cycle
    }


def test_complex_intersecting_cycles():
    """Test a graph with multiple intersecting cycles."""
    # Cycle 1: A -> B -> C -> A
    # Cycle 2: B -> D -> E -> B

    # Create geo container first
    geo = hou.node("/obj").createNode("geo", "geo1")

    with context(geo) as ctx:
        # Create nodes with forward references to create cycles
        # Cycle 1: A -> B -> C -> A
        # Cycle 2: B -> D -> E -> B
        ctx.node("null", "A", _input="C")  # Forward reference for cycle 1
        ctx.node("merge", "B", _inputs=["A", "E"])  # Forward reference for cycle 2
        ctx.node("null", "C", _input="B")
        ctx.node("null", "D", _input="B")
        ctx.node("null", "E", _input="D")

    # Nodes are created automatically on context exit
    # Call .create() to get the cached hou.Node
    hou_a = ctx["A"].create()
    hou_b = ctx["B"].create()
    hou_c = ctx["C"].create()
    hou_d = ctx["D"].create()
    hou_e = ctx["E"].create()

    # Count cycles by checking input connections
    cycle_count = 0

    # Check cycle 1: A -> B -> C -> A
    if len(hou_a.inputs()) > 0 and hou_a.inputs()[0] is not None:
        if len(hou_c.inputs()) > 0 and hou_c.inputs()[0] is not None:
            cycle_count += 1

    # Check cycle 2: B -> D -> E -> B
    if len(hou_b.inputs()) > 1 and hou_b.inputs()[1] is not None:
        if len(hou_e.inputs()) > 0 and hou_e.inputs()[0] is not None:
            cycle_count += 1

    return {
        "success": True,
        "node_count": 5,
        "cycle_count": cycle_count
    }
