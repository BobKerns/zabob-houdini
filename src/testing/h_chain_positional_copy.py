"""Chain positional copy test functions."""


from zabob_houdini.solo_fns import node, chain
from zabob_houdini.utils import JsonArray, JsonObject


def h_test_positional_reordering() -> JsonObject:
    """Test Chain.copy() positional reordering functionality."""
    geo = node("/obj", "geo")
    # Create chain with named nodes
    n1 = node(geo, "box", name="first")
    n2 = node(geo, "sphere", name="second")
    n3 = node(geo, "merge", name="third")

    original_chain = chain(n1, n2, n3)

    # Test various reordering patterns
    reversed_chain = original_chain.copy(2, 1, 0)
    partial_chain = original_chain.copy(0, 2)
    duplicate_chain = original_chain.copy(1, 1, 0)
    default_copy = original_chain.copy()

    # Test name-based access
    by_name_chain = original_chain.copy("third", "first")
    mixed_chain = original_chain.copy(0, "third")

    # Test node insertion
    new_node = node(geo, "xform", name="inserted")
    inserted_chain = original_chain.copy(0, new_node, 2)

    return {
        'original_names': [n.name for n in original_chain],
        'reversed_names': [n.name for n in reversed_chain],
        'partial_names': [n.name for n in partial_chain],
        'duplicate_names': [n.name for n in duplicate_chain],
        'default_names': [n.name for n in default_copy],
        'by_name_names': [n.name for n in by_name_chain],
        'mixed_names': [n.name for n in mixed_chain],
        'inserted_names': [n.name for n in inserted_chain],
    }


def h_test_copy_signature_includes_args() -> JsonObject:
    """Collect copy method signature information for validation."""
    import inspect

    # Create a simple node to test the signature
    geo = node("/obj", "geo")
    box = node(geo, "box")

    # Check the copy method signature
    sig = inspect.signature(box.copy)
    params = sig.parameters

    # Collect signature information
    param_names: JsonArray = list(params.keys())
    keyword_only: JsonArray = [p.name for p in params.values() if p.kind == p.KEYWORD_ONLY]

    # Also test Chain signature
    chain_obj = chain(box)
    chain_sig = inspect.signature(chain_obj.copy)
    chain_params = list(chain_sig.parameters.values())
    chain_uses_args: bool = any(p.kind == p.VAR_POSITIONAL for p in chain_params)
    chain_param_names: JsonArray = [p.name for p in chain_params]
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
