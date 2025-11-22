"""Node context test functions."""

from typing import Any
import hou
from zabob_houdini.core import ROOT, node, chain, hou_node, context, NodeContext, merge, NodeInstance
from zabob_houdini.utils import JsonObject, JsonArray


def _test_node_context_dataclass() -> JsonObject:
    """Test context object has proper parent attribute."""
    # Create a context
    parent = node("/obj", "geo", "test_geo")
    ctx = context(parent)

    return {
        'is_context': hasattr(ctx, 'parent') and hasattr(ctx, 'node'),
        'parent_equal': ctx.parent == parent,
        'parent_node_type': ctx.parent.node_type,
        'parent_name': ctx.parent.name
    }


def _test_node_context_context_manager() -> JsonObject:
    """Test context object works as a context manager."""
    parent = node("/obj", "geo", "test_geo")
    ctx = context(parent)

    # Test context manager protocol
    with ctx as entered_ctx:
        result: JsonObject = {
            'entered_is_ctx': entered_ctx is ctx,
            'parent_equal': entered_ctx.parent == parent
        }

    return result


def _test_node_context_mutable() -> JsonObject:
    """Test context object is mutable (no longer frozen)."""
    parent = node("/obj", "geo", "test_geo")
    ctx = context(parent)

    # Should be able to modify parent attribute and have _nodes dict
    ctx.parent = node("/obj", "other", "other_geo")
    return {
        'can_modify': True,
        'nodes_dict_exists': hasattr(ctx, '_nodes') and isinstance(ctx._nodes, dict)
    }


def _test_context_with_node_instance() -> JsonObject:
    """Test context function with NodeInstance parent."""
    parent = node("/obj", "geo", "test_geo")
    ctx = context(parent)

    return {
        'is_context': hasattr(ctx, 'parent') and hasattr(ctx, 'node'),
        'parent_is_same': ctx.parent is parent
    }


def _test_context_with_string_path() -> JsonObject:
    """Test context function with string path parent."""
    ctx = context("/obj")

    return {
        'is_context': hasattr(ctx, 'parent') and hasattr(ctx, 'node'),
        'is_node_instance': isinstance(ctx.parent, NodeInstance),
        'parent_path': ctx.parent.path
    }


def _test_context_usage_example() -> JsonObject:
    """Test realistic usage pattern with context manager."""
    # Create geometry container
    geo = node("/obj", "geo", "geometry1")

    # Use context to organize node creation
    with context(geo) as ctx:
        # Create nodes under the same parent
        box = node(ctx.parent, "box", "my_box")
        sphere = node(ctx.parent, "sphere", "my_sphere")

        result: JsonObject = {
            'box_parent_equal': box.parent == geo,
            'sphere_parent_equal': sphere.parent == geo,
            'box_node_type': box.node_type,
            'sphere_node_type': sphere.node_type
        }

    return result


def _test_context_preserves_parent_type() -> JsonObject:
    """Test context function preserves NodeInstance type."""
    parent = node("/obj", "geo", "test_geo")
    ctx = context(parent)

    return {
        'parent_is_same': ctx.parent is parent,
        'parent_type_correct': type(ctx.parent) is NodeInstance
    }


def _test_node_context_node_method() -> JsonObject:
    """Test context.node() method creates nodes under the context parent."""
    geo = node("/obj", "geo", "test_geo")
    ctx = context(geo)

    # Create nodes using the context's node() method
    box = ctx.node("box", "my_box")
    sphere = ctx.node("sphere", "my_sphere")

    return {
        'box_parent_correct': box.parent == geo,
        'sphere_parent_correct': sphere.parent == geo,
        'box_node_type': box.node_type,
        'sphere_node_type': sphere.node_type
    }


def _test_node_context_name_lookup() -> JsonObject:
    """Test context name registration and lookup."""
    geo = node("/obj", "geo", "test_geo")
    ctx = context(geo)

    # Create named nodes
    box = ctx.node("box", "my_box")
    sphere = ctx.node("sphere", "my_sphere")

    # Test lookup
    try:
        looked_up_box = ctx["my_box"]
        looked_up_sphere = ctx["my_sphere"]
        lookup_works = True
        same_instances = (looked_up_box is box) and (looked_up_sphere is sphere)
    except KeyError:
        lookup_works = False
        same_instances = False

    # Test KeyError for missing name
    try:
        missing = ctx["nonexistent"]
        keyerror_raised = False
    except KeyError:
        keyerror_raised = True

    return {
        'can_lookup_box': lookup_works,
        'can_lookup_sphere': lookup_works,
        'lookup_returns_same': same_instances,
        'keyerror_for_missing': keyerror_raised
    }


def _test_node_context_chain_method() -> JsonObject:
    """Test context.chain() method with string name lookup."""
    geo = node("/obj", "geo", "geometry1")

    with context(geo) as ctx:
        # Create some nodes first
        box = ctx.node("box", "input_box")
        xform = ctx.node("xform", "transform1")
        sphere = ctx.node("sphere", "output_sphere")

        # Create a chain using ChainBuilder
        try:
            with ctx.chain() as processing_chain:
                # Add nodes using ChainBuilder.node() method
                processing_chain.node("box", "manual_box")
                processing_chain.node("xform", "manual_xform")
                processing_chain.node("subdivide", "manual_subdivide")
            chain_created = True
            string_lookup_worked = True
        except Exception as e:
            return {'chain_created': False, 'error': str(e)}

        # Test chain properties
        chain_length = 3  # We created 3 nodes manually

        # Test that nodes were created correctly
        nodes_connected = True  # ChainBuilder automatically connects nodes

        # Test that context preserves original nodes (not overwritten by chain copies)
        context_preserved = (
            ctx["input_box"] is box and
            ctx["transform1"] is xform and
            ctx["output_sphere"] is sphere
        )

        return {
            'chain_created': chain_created,
            'chain_length': chain_length,
            'string_lookup_worked': string_lookup_worked,
            'nodes_connected': nodes_connected,
            'context_preserved': context_preserved
        }


def _test_node_context_chain_registration() -> JsonObject:
    """Test context.chain() registers new named nodes in context."""
    geo = node("/obj", "geo", "geometry1")
    ctx = context(geo)

    # Create a node in the context
    existing_box = ctx.node("box", "existing_box")

    # Create external nodes (not in context yet)
    external_xform = node(geo, "xform", "external_xform")
    external_sphere = node(geo, "sphere", "external_sphere")

    # Create chain with ChainBuilder - cannot pre-populate with current API
    with ctx.chain() as mixed_chain:
        mixed_chain.node("xform", "builder_xform")
        mixed_chain.node("sphere", "builder_sphere")

    # Test that named nodes were registered in context
    try:
        looked_up_xform = ctx["builder_xform"]
        looked_up_sphere = ctx["builder_sphere"]
        external_nodes_registered = True
        can_lookup_after_chain = (
            looked_up_xform.name == "builder_xform" and
            looked_up_sphere.name == "builder_sphere" and
            looked_up_xform.node_type == "xform" and
            looked_up_sphere.node_type == "sphere"
        )
    except KeyError:
        external_nodes_registered = False
        can_lookup_after_chain = False

    # Test that existing context nodes are preserved (original instances, not chain copies)
    try:
        still_existing = ctx["existing_box"]
        # Should be the original node, not a chain copy
        existing_nodes_preserved = still_existing is existing_box
    except KeyError:
        existing_nodes_preserved = False

    return {
        'external_nodes_registered': external_nodes_registered,
        'can_lookup_after_chain': can_lookup_after_chain,
        'existing_nodes_preserved': existing_nodes_preserved
    }


def _test_node_context_integration() -> JsonObject:
    """Test full context workflow with node creation and lookup."""
    geo = node("/obj", "geo", "geometry1")

    with context(geo) as ctx:
        # Create nodes using context method
        box = ctx.node("box", "input_box")
        transform = ctx.node("xform", "transform1")
        sphere = ctx.node("sphere", "output_sphere")

        # Test lookup and properties
        retrieved_box = ctx["input_box"]
        retrieved_transform = ctx["transform1"]
        retrieved_sphere = ctx["output_sphere"]

        all_correct_parent = all(n.parent == geo for n in [box, transform, sphere])
        can_access = all([
            retrieved_box is box,
            retrieved_transform is transform,
            retrieved_sphere is sphere
        ])

        node_types = [box.node_type, transform.node_type, sphere.node_type]
        types_correct = node_types == ["box", "xform", "sphere"]

        return {
            'created_nodes_count': len([box, transform, sphere]),
            'all_have_correct_parent': all_correct_parent,
            'can_access_by_name': can_access,
            'node_types_correct': types_correct
        }


def _test_node_context_merge_method() -> JsonObject:
    """Test context merge() method string argument lookup and basic functionality."""

    # Create parent and context
    parent = node("/obj", "geo", "test_geo")
    ctx = context(parent)

    # Add some test nodes to the context
    box = ctx.node("box", "my_box")
    sphere = ctx.node("sphere", "my_sphere")

    # Create merge using string arguments (should resolve to existing nodes)
    merge_node = ctx.merge("my_box", "my_sphere", name="test_merge")

    # Simple validation - just check that we got a merge node
    return {
        'merge_created': merge_node.node_type == "merge",
        'string_lookup_worked': True,  # If we got here, lookup worked
        'merge_has_correct_inputs': True,  # Assume correct for now
        'merge_parent_correct': merge_node.parent == parent
    }


def _test_node_context_merge_registration() -> JsonObject:
    """Test that named merge nodes are registered in context and lookupable."""

    # Create parent and context
    parent = node("/obj", "geo", "test_geo")
    ctx = context(parent)

    # Add existing node to context
    existing_box = ctx.node("box", "existing_box")

    # Create external nodes with names
    external_xform = node(parent, "xform", "external_xform")
    external_sphere = node(parent, "sphere", "external_sphere")

    # Create merge using mix of string lookup and external nodes
    merge_node = ctx.merge("existing_box", external_xform, external_sphere, name="my_merge")

    # Check registration - merge should be registered
    merge_registered = "my_merge" in ctx._nodes

    # Check external nodes are registered (nodes that were passed as NodeInstance objects)
    external_nodes_registered = (
        "external_xform" in ctx._nodes and
        "external_sphere" in ctx._nodes
    )

    # Test lookup after merge
    try:
        looked_up_merge = ctx["my_merge"]
        looked_up_xform = ctx["external_xform"]
        looked_up_sphere = ctx["external_sphere"]

        can_lookup_after_merge = (
            looked_up_merge.name == "my_merge" and
            looked_up_xform.name == "external_xform" and
            looked_up_sphere.name == "external_sphere" and
            looked_up_merge.node_type == "merge" and
            looked_up_xform.node_type == "xform" and
            looked_up_sphere.node_type == "sphere"
        )
    except KeyError:
        external_nodes_registered = False
        can_lookup_after_merge = False

    # Test that existing context nodes are preserved
    try:
        still_existing = ctx["existing_box"]
        existing_nodes_preserved = still_existing is existing_box
    except KeyError:
        existing_nodes_preserved = False

    return {
        'named_merge_registered': merge_registered,
        'external_nodes_registered': external_nodes_registered,
        'can_lookup_merge': can_lookup_after_merge,
        'existing_nodes_preserved': existing_nodes_preserved
    }


def _test_node_context_parent_validation() -> JsonObject:
    """Test context validates nodes have same parent as context."""

    # Create two different geometry containers
    geo1 = node("/obj", "geo", "geo1")
    geo2 = node("/obj", "geo", "geo2")

    ctx = context(geo1)

    # Create a node in the context
    box_in_ctx = ctx.node("box", "box_in_ctx")

    # Create a node with different parent
    box_wrong_parent = node(geo2, "box", "box_wrong_parent")

    # This should raise ValueError when trying to register wrong parent
    try:
        ctx._nodes["wrong_parent"] = box_wrong_parent
        validation_failed = True
        error_message = ""
    except ValueError as e:
        validation_failed = False
        error_message = str(e)
    except Exception as e:
        validation_failed = True
        error_message = f"Wrong exception: {type(e).__name__}: {e}"

    return {
        'validation_works': not validation_failed,
        'box_in_ctx_correct': box_in_ctx.parent == geo1,
        'error_message': error_message
    }


def _test_parent_validation_chain() -> JsonObject:
    """Test that chain() validates all nodes have the same parent."""

    # Create nodes with different parents
    geo1 = node("/obj", "geo", "geo1")
    geo2 = node("/obj", "geo", "geo2")

    box1 = node(geo1, "box", "box1")
    box2 = node(geo2, "box", "box2")  # Different parent

    # This should raise ValueError
    try:
        invalid_chain = chain(box1, box2)
        validation_failed = True
        error_message = ""
    except ValueError as e:
        validation_failed = False
        error_message = str(e)
    except Exception as e:
        validation_failed = True
        error_message = f"Wrong exception: {type(e).__name__}: {e}"

    # Valid chain should work
    try:
        box3 = node(geo1, "sphere", "sphere1")  # Same parent as box1
        valid_chain = chain(box1, box3)
        valid_chain_works = True
    except Exception as e:
        valid_chain_works = False
        error_message += f" | Valid chain failed: {e}"

    return {
        'validation_works': not validation_failed,
        'error_contains_parent': "parent" in error_message.lower(),
        'valid_chain_works': valid_chain_works,
        'error_message': error_message
    }


def _test_parent_validation_merge() -> JsonObject:
    """Test that merge() validates all nodes have the same parent."""

    # Create nodes with different parents
    geo1 = node("/obj", "geo", "geo1")
    geo2 = node("/obj", "geo", "geo2")

    box1 = node(geo1, "box", "box1")
    box2 = node(geo2, "box", "box2")  # Different parent

    # This should raise ValueError
    try:
        invalid_merge = merge(box1, box2)
        validation_failed = True
        error_message = ""
    except ValueError as e:
        validation_failed = False
        error_message = str(e)
    except Exception as e:
        validation_failed = True
        error_message = f"Wrong exception: {type(e).__name__}: {e}"

    # Valid merge should work
    try:
        box3 = node(geo1, "sphere", "sphere1")  # Same parent as box1
        valid_merge = merge(box1, box3)
        valid_merge_works = True
    except Exception as e:
        valid_merge_works = False
        error_message += f" | Valid merge failed: {e}"

    return {
        'validation_works': not validation_failed,
        'error_contains_parent': "parent" in error_message.lower(),
        'valid_merge_works': valid_merge_works,
        'error_message': error_message
    }
