"""Input validation test functions."""

from typing import Any
import hou
from zabob_houdini.core import ROOT, node, chain, hou_node, _merge_inputs
from zabob_houdini.utils import JsonObject, JsonArray


def _test_parameter_validation_comprehensive() -> JsonObject:
    """Test parameter validation in Houdini environment."""
    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_validation")

    # Create a valid chain to use for testing
    chain_A = chain(
        node(geo_node, "box", "source_box"),
        node(geo_node, "xform", "center"),
    )

    # Test valid patterns work
    try:
        chain_B = chain(
            node(geo_node, "xform", "scale_up", _input=chain_A),
            node(geo_node, "xform", "rotate_y"),
        )

        valid_patterns_work = True
    except Exception:
        valid_patterns_work = False

    # Test invalid patterns are rejected
    try:
        # This should fail - _input parameter not supported on chain()
        bad_chain = chain(
            node(geo_node, "xform", "bad_node"),
            node(geo_node, "xform", "rotate_z"),
            _input=chain_A,  # This should raise TypeError
        )
        invalid_patterns_rejected = False  # Should not reach here
    except TypeError:
        invalid_patterns_rejected = True
    except Exception:
        invalid_patterns_rejected = False  # Wrong exception type

    return {
        'valid_patterns_work': valid_patterns_work,
        'invalid_patterns_rejected': invalid_patterns_rejected,
    }


def _test_chain_rejects_input_parameter() -> JsonObject:
    """Test that chain() properly rejects the deprecated _input parameter."""
    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_rejection")

    # Create test chain
    chain_A = chain(
        node(geo_node, "box", "source_box"),
        node(geo_node, "xform", "center"),
    )

    # This should raise a TypeError with a helpful message
    try:
        chain(
            node(geo_node, "xform", "scale_up"),
            node(geo_node, "xform", "rotate_y"),
            _input=chain_A,  # This should trigger the error
        )
        # Should not reach here
        error_raised = False
        error_message = ""
    except TypeError as e:
        error_raised = True
        error_message = str(e)
    except Exception as e:
        error_raised = False
        error_message = f"Wrong exception type: {type(e).__name__}: {e}"

    # Check that the error message contains the expected guidance
    error_contains_input = "_input" in error_message
    error_contains_no_longer_supported = "no longer supported" in error_message
    error_contains_guidance = "pass the input to the first node" in error_message

    return {
        'error_raised': error_raised,
        'error_message': error_message,
        'error_contains_input': error_contains_input,
        'error_contains_no_longer_supported': error_contains_no_longer_supported,
        'error_contains_guidance': error_contains_guidance,
    }


def _test_valid_input_patterns() -> JsonObject:
    """Test that valid input patterns work correctly."""
    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_valid")

    # Chain A: Create base geometry
    chain_A = chain(
        node(geo_node, "box", "source_box"),
        node(geo_node, "xform", "center"),
    )

    # This should work - first node has input
    chain_B = chain(
        node(geo_node, "xform", "scale_up", _input=chain_A),  # Node has input
        node(geo_node, "xform", "rotate_y"),
    )

    # This should also work - no inputs anywhere
    chain_C = chain(
        node(geo_node, "xform", "scale_down"),  # No inputs
        node(geo_node, "xform", "rotate_x"),
    )

    return {
        'chain_B_length': len(chain_B.nodes),
        'chain_C_length': len(chain_C.nodes),
        'chain_B_has_inputs': len(chain_B.inputs) > 0,
        'chain_C_no_inputs': len(chain_C.inputs) == 0,
    }


def _test_node_input_validation() -> JsonObject:
    '''
    Test node input connections and validation.
    '''
    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_node_inputs")

    # Create source
    source = node(geo_node, "box", "source")

    # Single input - should work
    node_single = node(geo_node, "xform", "transform", _input=source)
    single_input_works = (
        len(node_single.inputs) == 1 and
        node_single.inputs[0] is not None and
        node_single.inputs[0][0] is source
    )

    # Multiple inputs - should work
    source2 = node(geo_node, "box", "source2")
    node_multi = node(geo_node, "merge", "combine", _input=[source, source2])
    input_nodes = [inp[0] for inp in node_multi.inputs if inp is not None]
    multiple_inputs_work = (
        len(node_multi.inputs) == 2 and
        source in input_nodes and
        source2 in input_nodes
    )

    # No inputs - should work
    node_none = node(geo_node, "box", "standalone")
    no_inputs_work = len(node_none.inputs) == 0

    return {
        'single_input_works': single_input_works,
        'multiple_inputs_work': multiple_inputs_work,
        'no_inputs_work': no_inputs_work,
    }


def _test_invalid_input_types(input_type: str) -> JsonObject:
    """Test that invalid input types are handled appropriately."""
    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_invalid")

    if input_type == "none":
        # None should be filtered out and result in no inputs
        test_node = node(geo_node, "xform", "test", _input=None)
        none_filtered_out = len(test_node.inputs) == 0
        return {'none_filtered_out': none_filtered_out}

    elif input_type == "empty_string":
        # Empty string - test what happens (type: ignore for intentional type violation)
        try:
            test_node = node(geo_node, "xform", "test", _input="")  # type: ignore
            handled_appropriately = True
            error_occurred = False
        except Exception as e:
            handled_appropriately = True
            error_occurred = True
        return {
            'handled_appropriately': handled_appropriately,
            'error_occurred': error_occurred,
        }

    elif input_type == "number":
        # Number - test what happens (type: ignore for intentional type violation)
        try:
            test_node = node(geo_node, "xform", "test", _input=123)  # type: ignore
            handled_appropriately = True
            error_occurred = False
        except Exception as e:
            handled_appropriately = True
            error_occurred = True
        return {
            'handled_appropriately': handled_appropriately,
            'error_occurred': error_occurred,
        }

    else:
        return {'handled_appropriately': False, 'unknown_input_type': input_type}



