"""Node duplication test functions."""

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from zabob_houdini.core import znode, zchain, hou_node
from zabob_houdini.utils import JsonObject, ignore


def h_test_diamond_no_duplication() -> JsonObject:
    """Test that diamond pattern doesn't create duplicate nodes - this should expose the bug!"""
    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", "test_diamond_duplication")

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

    # Create all chains - this is where duplication might happen
    chain_A_created = chain_A.create()
    chain_B2_created = chain_B2.create()
    chain_B3_created = chain_B3.create()

    # Get ALL nodes that were created in the geo container
    all_children = geo_node.children()
    all_node_paths = [child.path() for child in all_children]
    unique_node_paths = list(set(all_node_paths))

    # Check connections to verify they're connecting to the right nodes
    scale_up_node = chain_B2_created[0]
    scale_down_node = chain_B3_created[0]
    center_node = chain_A_created[-1]

    scale_up_input = scale_up_node.inputs()[0] if scale_up_node.inputs() else None
    scale_down_input = scale_down_node.inputs()[0] if scale_down_node.inputs() else None

    scale_up_connected_to_center = (
        scale_up_input and scale_up_input.path() == center_node.path()
    )
    scale_down_connected_to_center = (
        scale_down_input and scale_down_input.path() == center_node.path()
    )

    # Critical test: both should connect to the SAME center node
    both_connect_to_same_center = (
        scale_up_input and scale_down_input and
        scale_up_input.path() == scale_down_input.path()
    )

    return {
        'all_node_paths': all_node_paths,  # type: ignore  # str is JsonValue
        'unique_node_paths': unique_node_paths,  # type: ignore  # str is JsonValue
        'scale_up_connected_to_center': scale_up_connected_to_center,
        'scale_down_connected_to_center': scale_down_connected_to_center,
        'both_connect_to_same_center': both_connect_to_same_center,
        'total_nodes_created': len(all_node_paths),
        'unique_nodes_count': len(unique_node_paths),
    }


def h_test_chain_reference_vs_copy() -> JsonObject:
    """Test that chains are referenced, not copied when used as inputs."""
    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", "test_reference_vs_copy")

    # Create chain A
    chain_A = zchain(
        znode(geo_node, "box", "box_a"),
        znode(geo_node, "xform", "xform_a"),
        znode(geo_node, "subdivide", "subdivide_a"),
    )

    # Use chain A as input to two different nodes
    node_1 = znode(geo_node, "xform", "node_1", _input=chain_A)
    node_2 = znode(geo_node, "xform", "node_2", _input=chain_A)

    # Create everything
    chain_a_created = chain_A.create()
    _node_1_created = node_1.create()
    _node_2_created = node_2.create()
    ignore(_node_1_created, _node_2_created)  # Avoid unused variable warning

    # Count actual nodes in the scene
    all_children = geo_node.children()
    total_created_node_count = len(all_children)

    # Expected: 3 nodes from chain A + 2 individual nodes = 5 total
    chain_a_node_count = len(chain_a_created)
    other_nodes_count = 2  # node_1 and node_2

    return {
        'chain_a_node_count': chain_a_node_count,
        'other_nodes_count': other_nodes_count,
        'total_created_node_count': total_created_node_count,
        'all_node_paths': [child.path() for child in all_children],  # type: ignore  # str is JsonValue
    }
