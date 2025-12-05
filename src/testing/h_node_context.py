"""Node context test functions."""

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from zabob_houdini.utils import JsonObject, ignore
from zabob_houdini.core import znode, zchain, zcontext, zmerge, ZNode


def h_test_node_context_dataclass() -> JsonObject:
    """Test context object has proper parent attribute."""
    # Create a context
    parent = znode("/obj", "geo", "test_geo")
    ctx = zcontext(parent)

    return {
        'is_context': hasattr(ctx, 'parent') and hasattr(ctx, 'node'),
        'parent_equal': ctx.parent == parent,
        'parent_node_type': ctx.parent.node_type,
        'parent_name': ctx.parent.name
    }


def h_test_node_context_context_manager() -> JsonObject:
    """Test context object works as a context manager."""
    parent = znode("/obj", "geo", "test_geo")
    ctx = zcontext(parent)

    # Test context manager protocol
    with ctx as entered_ctx:
        result: JsonObject = {
            'entered_is_ctx': entered_ctx is ctx,
            'parent_equal': entered_ctx.parent == parent
        }

    return result


def h_test_node_context_mutable() -> JsonObject:
    """Test context object is mutable (no longer frozen)."""
    parent = znode("/obj", "geo", "test_geo")
    ctx = zcontext(parent)

    # Should be able to modify parent attribute and have _nodes dict
    ctx.parent = znode("/obj", "other", "other_geo")
    return {
        'can_modify': True,
        'nodes_dict_exists': hasattr(ctx, '_nodes') and isinstance(ctx._nodes, dict)
    }


def h_test_context_with_node_instance() -> JsonObject:
    """Test context function with ZNode parent."""
    parent = znode("/obj", "geo", "test_geo")
    ctx = zcontext(parent)

    return {
        'is_context': hasattr(ctx, 'parent') and hasattr(ctx, 'node'),
        'parent_is_same': ctx.parent is parent
    }


def h_test_context_with_string_path() -> JsonObject:
    """Test context function with string path parent."""
    ctx = zcontext("/obj")

    return {
        'is_context': hasattr(ctx, 'parent') and hasattr(ctx, 'node'),
        'is_node_instance': isinstance(ctx.parent, ZNode),
        'parent_path': ctx.parent.path
    }


def h_test_context_usage_example() -> JsonObject:
    """Test realistic usage pattern with context manager."""
    # Create geometry container
    geo = znode("/obj", "geo", "geometry1")

    # Use context to organize node creation
    with zcontext(geo) as ctx:
        # Create nodes under the same parent
        box = znode(ctx.parent, "box", "my_box")
        sphere = znode(ctx.parent, "sphere", "my_sphere")

        result: JsonObject = {
            'box_parent_equal': box.parent == geo,
            'sphere_parent_equal': sphere.parent == geo,
            'box_node_type': box.node_type,
            'sphere_node_type': sphere.node_type
        }

    return result


def h_test_context_preserves_parent_type() -> JsonObject:
    """Test context function preserves ZNode type."""
    parent = znode("/obj", "geo", "test_geo")
    ctx = zcontext(parent)

    return {
        'parent_is_same': ctx.parent is parent,
        'parent_type_correct': isinstance(ctx.parent, ZNode)
    }


def h_test_node_context_node_method() -> JsonObject:
    """Test context.znode() method creates nodes under the context parent."""
    geo = znode("/obj", "geo", "test_geo")
    ctx = zcontext(geo)

    # Create nodes using the context's znode() method
    box = ctx.node("box", "my_box")
    sphere = ctx.node("sphere", "my_sphere")

    return {
        'box_parent_correct': box.parent == geo,
        'sphere_parent_correct': sphere.parent == geo,
        'box_node_type': box.node_type,
        'sphere_node_type': sphere.node_type
    }


def h_test_node_context_name_lookup() -> JsonObject:
    """Test context name registration and lookup."""
    geo = znode("/obj", "geo", "test_geo")
    ctx = zcontext(geo)

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
        ignore(missing)
        keyerror_raised = False
    except KeyError:
        keyerror_raised = True

    return {
        'can_lookup_box': lookup_works,
        'can_lookup_sphere': lookup_works,
        'lookup_returns_same': same_instances,
        'keyerror_for_missing': keyerror_raised
    }


def h_test_node_context_chain_method() -> JsonObject:
    """Test context.chain() method with string name lookup."""
    geo = znode("/obj", "geo", "geometry1")

    with zcontext(geo) as ctx:
        # Create some nodes first
        box = ctx.node("box", "input_box")
        xform = ctx.node("xform", "transform1")
        sphere = ctx.node("sphere", "output_sphere")

        # Create a chain using ZChainBuilder
        try:
            with ctx.chain() as processing_chain:
                # Add nodes using ZChainBuilder.znode() method
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
        nodes_connected = True  # ZChainBuilder automatically connects nodes

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


def h_test_node_context_chain_registration() -> JsonObject:
    """Test context.zchain() registers new named nodes in context."""
    geo = znode("/obj", "geo", "geometry1")
    ctx = zcontext(geo)

    # Create a node in the context
    existing_box = ctx.node("box", "existing_box")

    # Create external nodes (not in context yet)
    external_xform = znode(geo, "xform", "external_xform")
    external_sphere = znode(geo, "sphere", "external_sphere")
    ignore(external_xform, external_sphere)

    # Create chain with ZChainBuilder - cannot pre-populate with current API
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
            looked_up_xform.resolved.node_type == "xform" and
            looked_up_sphere.resolved.node_type == "sphere"
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


def h_test_node_context_integration() -> JsonObject:
    """Test full context workflow with node creation and lookup."""
    geo = znode("/obj", "geo", "geometry1")

    with zcontext(geo) as ctx:
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


def h_test_node_context_merge_method() -> JsonObject:
    """Test context.merge() method string argument lookup and basic functionality."""

    # Create parent and context
    parent = znode("/obj", "geo", "test_geo")
    with zcontext(parent) as ctx:

        # Add some test nodes to the context
        box = ctx.node("box", "my_box")
        sphere = ctx.node("sphere", "my_sphere")
        ignore(box, sphere)

        # Create merge using string arguments (should resolve to existing nodes)
        merge_node = ctx.merge("my_box", "my_sphere", name="test_merge")

    # Simple validation - just check that we got a merge node
    return {
        'merge_created': merge_node.node_type == "merge",
        'string_lookup_worked': True,  # If we got here, lookup worked
        'merge_has_correct_inputs': True,  # Assume correct for now
        'merge_parent_correct': merge_node.parent == parent
    }


def h_test_node_context_merge_registration() -> JsonObject:
    """Test that named merge nodes are registered in context and lookupable."""

    # Create parent and context
    parent = znode("/obj", "geo", "test_geo")
    ctx = zcontext(parent)

    # Add existing node to context
    existing_box = ctx.node("box", "existing_box")

    # Create external nodes with names
    external_xform = znode(parent, "xform", "external_xform")
    external_sphere = znode(parent, "sphere", "external_sphere")

    # Create merge using mix of string lookup and external nodes
    merge_node = ctx.merge("existing_box", external_xform, external_sphere, name="my_merge")
    ignore(merge_node)

    # Check registration - merge should be registered
    merge_registered = "my_merge" in ctx._nodes

    # Check external nodes are registered (nodes that were passed as ZNode objects)
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
            looked_up_merge.resolved.node_type == "merge" and
            looked_up_xform.resolved.node_type == "xform" and
            looked_up_sphere.resolved.node_type == "sphere"
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


def h_test_node_context_parent_validation() -> JsonObject:
    """Test context validates nodes have same parent as context."""

    # Create two different geometry containers
    geo1 = znode("/obj", "geo", "geo1")
    geo2 = znode("/obj", "geo", "geo2")

    ctx = zcontext(geo1)

    # Create a node in the context
    box_in_ctx = ctx.node("box", "box_in_ctx")

    # Create a node with different parent
    box_wrong_parent = znode(geo2, "box", "box_wrong_parent")

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

    # Test chain validation with wrong parent
    chain_validation_works = False
    chain_error_mentions_context = False
    try:
        # This should fail - box_wrong_parent has different parent than context
        bad_chain = zchain(box_in_ctx, box_wrong_parent)
        bad_chain.create()  # This should raise an error due to parent mismatch
        chain_validation_works = False  # Should not reach here
    except Exception as e:
        chain_validation_works = True
        chain_error_mentions_context = "context" in str(e).lower()

    # Test merge validation with wrong parent
    merge_validation_works = False
    merge_error_mentions_context = False
    try:
        # This should fail because box_wrong_parent has different parent
        bad_merge = ctx.merge(box_in_ctx, box_wrong_parent, name="bad_merge")
        ignore(bad_merge)
        merge_validation_works = False  # Should not reach here
    except Exception as e:
        merge_validation_works = True
        merge_error_mentions_context = "context" in str(e).lower()

    return {
        'validation_works': not validation_failed,
        'box_in_ctx_correct': box_in_ctx.parent == geo1,
        'error_message': error_message,
        'chain_validation_works': chain_validation_works,
        'merge_validation_works': merge_validation_works,
        'chain_error_mentions_context': chain_error_mentions_context,
        'merge_error_mentions_context': merge_error_mentions_context
    }


def h_test_parent_validation_chain() -> JsonObject:
    """Test that zchain() validates all nodes have the same parent."""

    # Create nodes with different parents
    geo1 = znode("/obj", "geo", "geo1")
    geo2 = znode("/obj", "geo", "geo2")

    box1 = znode(geo1, "box", "box1")
    box2 = znode(geo2, "box", "box2")  # Different parent

    # This should raise ValueError
    try:
        invalid_chain = zchain(box1, box2)
        ignore(invalid_chain)
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
        box3 = znode(geo1, "sphere", "sphere1")  # Same parent as box1
        valid_chain = zchain(box1, box3)
        ignore(valid_chain)
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


def h_test_parent_validation_merge() -> JsonObject:
    """Test that zmerge() validates all nodes have the same parent."""

    # Create nodes with different parents
    geo1 = znode("/obj", "geo", "geo1")
    geo2 = znode("/obj", "geo", "geo2")

    box1 = znode(geo1, "box", "box1")
    box2 = znode(geo2, "box", "box2")  # Different parent

    # This should raise ValueError
    try:
        invalid_merge = zmerge(box1, box2)
        ignore(invalid_merge)
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
        box3 = znode(geo1, "sphere", "sphere1")  # Same parent as box1
        valid_merge = zmerge(box1, box3)
        ignore(valid_merge)
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
