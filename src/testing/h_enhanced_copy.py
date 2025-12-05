"""Enhanced copy test functions."""

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from zabob_houdini.core import znode, zchain
from zabob_houdini.utils import JsonArray, JsonObject


def h_test_enhanced_copy_integration() -> JsonObject:
    """Collect data about enhanced copy functionality for test validation."""
    # Create a geometry container
    geo = znode("/obj", "geo", name="test_geo")

    # Create a base node
    box = znode(geo, "box", name="original_box", sizex=2, sizey=3, _display=False)

    # Test 1: Copy with new attributes
    box_with_attrs = box.copy(sizex=5, sizey=3)  # sizex should override

    # Test 2: Copy with new name
    renamed_box = box.copy(name="renamed_box")

    # Test 3: Copy with display/render flags
    display_box = box.copy(_display=True, _render=True)

    # Test 4: Copy with all parameters
    sphere = znode(geo, "sphere", name="input_sphere")
    complex_copy = box.copy(
        _inputs=[sphere],
        name="complex_box",
        _display=True,
        _render=False,
        sizex=4,
        sizey=5,
        divisions=10,
    )

    # Test 5: None parameters preserve originals
    preserved = box.copy(
        name=None,
        _display=None,
        _render=None
    )

    # Collect all data for assertions in the test case
    return {
        "original": {
            "name": box.name,
            "attributes": dict(box.attributes),
            "display": box._display,
            "render": box._render
        },
        "attributes_copy": {
            "name": box_with_attrs.name,
            "attributes": dict(box_with_attrs.attributes)
        },
        "renamed_copy": {
            "name": renamed_box.name
        },
        "display_copy": {
            "display": display_box._display,
            "render": display_box._render
        },
        "complex_copy": {
            "name": complex_copy.name,
            "attributes": dict(complex_copy.attributes),
            "has_inputs": len(complex_copy.inputs) > 0,
            "display": complex_copy._display,
            "render": complex_copy._render
        },
        "preserved_copy": {
            "name": preserved.name,
            "attributes": dict(preserved.attributes),
            "display": preserved._display,
            "render": preserved._render
        }
    }


def h_test_copy_signature_includes_args() -> JsonObject:
    """Collect copy method signature information for validation."""
    import inspect

    # Create a simple node to test the signature
    geo = znode("/obj", "geo")
    box = znode(geo, "box")

    # Check the copy method signature
    sig = inspect.signature(box.copy)
    params = sig.parameters

    # Collect signature information
    param_names: JsonArray = list(params.keys())
    keyword_only: JsonArray = [p.name for p in params.values() if p.kind == p.KEYWORD_ONLY]

    # Also test ZChain signature
    chain_obj = zchain(box)
    chain_sig = inspect.signature(chain_obj.copy)
    chain_params = chain_sig.parameters
    chain_param_names: JsonArray = list(chain_params.keys())
    chain_uses_args = any(p.kind == p.VAR_POSITIONAL for p in chain_params.values())
    return {
        "node_all_parameters": param_names,
        "node_keyword_only_parameters": keyword_only,
        "node_has_inputs": "_inputs" in params,
        "node_has_chain": "_chain" in params,
        "node_has_name": "name" in params,
        "node_has_attributes": "attributes" in params,
        "node_has_display": "_display" in params,
        "node_has_render": "_render" in params,
        "chain_all_parameters": chain_param_names,
        "chain_uses_args": chain_uses_args,
    }
