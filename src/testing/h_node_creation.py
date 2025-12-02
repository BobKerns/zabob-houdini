"""Node creation test functions."""

from typing import Any
import hou
from zabob_houdini.core import node, hou_node
from zabob_houdini.utils import JsonObject


def _test_parameter_setting() -> JsonObject:
    '''Test setting and retrieving node parameters.'''
    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", "test_params")

    # Create node with parameters
    box_node = node(geo_node, "box", "param_box", sizex=2.0, sizey=3.0, sizez=4.0)
    created_node = box_node.create(hou.OpNode)

    def val(node: hou.OpNode, parm_name: str) -> Any:
        parm = node.parm(parm_name)
        return parm.eval() if parm else None

    # Check parameters
    sizex = val(created_node, "sizex")
    sizey = val(created_node, "sizey")
    sizez = val(created_node, "sizez")

    parameters_set = (
        abs(sizex - 2.0) < 0.001 and
        abs(sizey - 3.0) < 0.001 and
        abs(sizez - 4.0) < 0.001
    )

    return {
        'parameters_set': parameters_set,
        'sizex': sizex,
        'sizey': sizey,
        'sizez': sizez,
    }


def _test_geometry_creation(node_type: str) -> JsonObject:
    """Test creation of various geometry node types."""
    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", f"test_{node_type}")

    # Create the specified node type
    test_node = node(geo_node, node_type, f"test_{node_type}_node")
    created_node = test_node.create()

    return {
        'node_type': created_node.type().name(),
        'node_path': created_node.path(),
    }


def _test_diamond_pattern_creation() -> JsonObject:
    """Test diamond pattern node creation without duplication."""
    from zabob_houdini.core import chain
    from zabob_houdini.utils import JsonArray

    # Create the container geometry node
    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", "test_diamond")

    # Chain A: Create base geometry (should be created once)
    chain_A = chain(
        node(geo_node, "box", name="source_box"),
        node(geo_node, "xform", "center"),
    )

    # Chain B2: Should connect to chain_A
    chain_B2 = chain(
        node(geo_node, "xform", "scale_up", _input=chain_A),
        node(geo_node, "xform", "rotate_y"),
    )

    # Chain B3: Should also connect to chain_A (not duplicate it)
    chain_B3 = chain(
        node(geo_node, "xform", "scale_down", _input=chain_A),
        node(geo_node, "xform", "rotate_x"),
    )

    # Create the nodes
    chain_A_created = chain_A.create()
    chain_B2_created = chain_B2.create()
    chain_B3_created = chain_B3.create()

    # Get all node paths for validation
    all_nodes = list(chain_A_created) + list(chain_B2_created) + list(chain_B3_created)
    node_paths: JsonArray = [node.path() for node in all_nodes]

    # Check for duplicates (there shouldn't be any in chain_A since B2/B3 reference it)
    unique_paths = list(set(node_paths))
    no_duplicates = len(unique_paths) == len(node_paths)

    # Verify connections
    scale_up_node = chain_B2_created[0]
    scale_down_node = chain_B3_created[0]
    center_node = chain_A_created[-1]

    scale_up_input = scale_up_node.inputs()[0] if scale_up_node.inputs() else None
    scale_down_input = scale_down_node.inputs()[0] if scale_down_node.inputs() else None

    connections_valid = (
        scale_up_input and scale_up_input.path() == center_node.path() and
        scale_down_input and scale_down_input.path() == center_node.path()
    )

    return {
        'node_paths': node_paths,
        'no_duplicates': no_duplicates,
        'connections_valid': connections_valid,
    }


def _test_multiple_input_merge() -> JsonObject:
    """Test merge node with multiple inputs."""
    from zabob_houdini.core import chain

    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", "test_merge")

    # Create two source chains
    chain1 = chain(node(geo_node, "box", "box1"))
    chain2 = chain(node(geo_node, "sphere", "sphere1"))

    # Create merge chain
    merge_chain = chain(
        node(geo_node, "merge", "combine", _input=[chain1, chain2]),
        node(geo_node, "xform", "final"),
    )

    # Create the nodes
    chain1.create()
    chain2.create()
    merge_created = merge_chain.create()

    # Check merge node inputs
    merge_node = merge_created[0]
    merge_inputs = len([inp for inp in merge_node.inputs() if inp])  # Count non-None inputs

    return {
        'merge_inputs': merge_inputs,
        'merge_path': merge_node.path(),
    }


def _test_chain_input_connections() -> JsonObject:
    """Test that chain input connections work correctly."""
    from zabob_houdini.core import chain

    _obj = hou_node("/obj")
    geo_node = _obj.createNode("geo", "test_connections")

    # Create source chain
    source_chain = chain(
        node(geo_node, "box", "source"),
        node(geo_node, "xform", "transform"),
    )

    # Create chain that connects to source
    connected_chain = chain(
        node(geo_node, "xform", "processor", _input=source_chain),
        node(geo_node, "subdivide", "refine"),
    )

    # Create the nodes
    source_created = source_chain.create()
    connected_created = connected_chain.create()

    # Verify connection
    processor_node = connected_created[0]
    transform_node = source_created[-1]

    processor_input = processor_node.inputs()[0] if processor_node.inputs() else None
    connections_valid = processor_input and processor_input.path() == transform_node.path()

    return {
        'connections_valid': connections_valid,
        'processor_path': processor_node.path(),
        'transform_path': transform_node.path(),
    }
