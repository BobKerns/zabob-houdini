"""Input connections test functions."""

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from zabob_houdini.core import znode, zchain, hou_node
from zabob_houdini.utils import JsonObject


def h_test_input_connections_basic() -> JsonObject:
    """Test that input connections are set up correctly on nodes."""
    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", "test_connections")

    # ZChain A: Create base geometry (should be created once)
    chain_A = zchain(
        znode(geo_node, "box", "source_box"),
        znode(geo_node, "xform", "center"),
    )

    # ZChain B2: Should connect to chain_A
    chain_B2 = zchain(
        znode(geo_node, "xform", "scale_up", _input=chain_A),
        znode(geo_node, "xform", "rotate_y"),
    )

    # ZChain B3: Should also connect to chain_A (not duplicate it)
    chain_B3 = zchain(
        znode(geo_node, "xform", "scale_down", _input=chain_A),
        znode(geo_node, "xform", "rotate_x"),
    )

    # ZChain C: Should merge B2 and B3
    chain_C = zchain(
        znode(geo_node, "merge", "combine", _input=[chain_B2, chain_B3]),
        znode(geo_node, "xform", "final"),
    )

    # Check that chains do NOT have _inputs field (architecture change)
    chains_no_inputs_field = (
        not hasattr(chain_A, '_inputs') and
        not hasattr(chain_B2, '_inputs') and
        not hasattr(chain_B3, '_inputs') and
        not hasattr(chain_C, '_inputs')
    )

    # Check that first node inputs are set correctly through delegation
    chain_A_no_inputs = len(chain_A.inputs) == 0
    chain_B2_has_inputs = len(chain_B2.inputs) == 1
    chain_B3_has_inputs = len(chain_B3.inputs) == 1
    chain_C_has_inputs = len(chain_C.inputs) == 2

    return {
        'chain_A_length': len(chain_A.nodes),
        'chain_B2_length': len(chain_B2.nodes),
        'chain_B3_length': len(chain_B3.nodes),
        'chain_C_length': len(chain_C.nodes),
        'chains_no_inputs_field': chains_no_inputs_field,
        'chain_A_no_inputs': chain_A_no_inputs,
        'chain_B2_has_inputs': chain_B2_has_inputs,
        'chain_B3_has_inputs': chain_B3_has_inputs,
        'chain_C_has_inputs': chain_C_has_inputs,
    }


def h_test_chain_input_delegation() -> JsonObject:
    """Test that ZChain.inputs properly delegates to first node."""
    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", "test_delegation")

    # ZChain with no inputs
    chain_no_input = zchain(
        znode(geo_node, "box", "source"),
        znode(geo_node, "xform", "transform"),
    )

    # ZChain with single input
    chain_single_input = zchain(
        znode(geo_node, "xform", "processor", _input=chain_no_input),
        znode(geo_node, "xform", "final"),
    )

    # Test delegation
    no_input_chain_empty = len(chain_no_input.inputs) == 0
    single_input_chain_has_one = len(chain_single_input.inputs) == 1

    # Verify this is actually delegating to the first node
    delegation_works = chain_single_input.inputs == chain_single_input.first.inputs

    return {
        'no_input_chain_empty': no_input_chain_empty,
        'single_input_chain_has_one': single_input_chain_has_one,
        'delegation_works': delegation_works,
    }


def h_test_multiple_inputs_basic() -> JsonObject:
    """Test that nodes can accept multiple inputs correctly."""
    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", "test_multi")

    # Create two source chains
    source_1 = zchain(znode(geo_node, "box", "source_1"))
    source_2 = zchain(znode(geo_node, "sphere", "source_2"))

    # Create a merge node that takes both as inputs
    merge_chain = zchain(
        znode(geo_node, "merge", "combiner", _input=[source_1, source_2])
    )

    # Test that the merge node has the expected inputs
    input_count = len(merge_chain.inputs)
    merge_has_multiple_inputs = input_count > 1

    return {
        'merge_has_multiple_inputs': merge_has_multiple_inputs,
        'input_count': input_count,
    }
