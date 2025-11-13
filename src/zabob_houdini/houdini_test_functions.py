"""
Houdini-specific test functions that require the hou module.

This module contains test functions that can only run within Houdini's Python environment.
These functions are called by the hython bridge for testing purposes.

## Usage Guidelines

All test functions in this module should use the `@houdini_result` decorator:

```python
@houdini_result
def test_my_feature() -> JsonObject:
    # Test implementation
    return {
        'test_passed': True,
        'node_count': 3,
        'details': 'All nodes created successfully'
    }
```

The decorator handles:
- Exception catching with detailed traceback reporting
- Consistent return structure with success/error fields
- JSON serialization for bridge communication
- Type safety (always returns JsonObject in result field)

Test functions should return structured data that describes the test results,
making it easy for external callers to understand what was tested and the outcome.
"""

from typing import Any
import hou
from zabob_houdini.core import ROOT, Inputs, NodeInstance, get_node_instance, hou_node, node, chain, wrap_node
from zabob_houdini.houdini_bridge import houdini_result
from zabob_houdini.utils import JsonObject, JsonArray

# Import pytest but make it optional for when running standalone
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False


@houdini_result
def test_basic_node_creation() -> JsonObject:
    """Test basic node creation in Houdini."""
    # Clear the scene
    hou.hipFile.clear()

    # Create a geometry object
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a box node
    box = geo.createNode("box", "test_box")

    if PYTEST_AVAILABLE:
        assert geo is not None, "Geometry node should be created"
        assert box is not None, "Box node should be created"
        assert geo.path().endswith("test_geo"), "Geo node should have correct name"
        assert box.path().endswith("test_box"), "Box node should have correct name"
    return {
        'geo_path': geo.path(),
        'box_path': box.path(),
    }



@houdini_result
def test_zabob_node_creation() -> JsonObject:
    """Test Zabob NodeInstance creation in Houdini."""
    # Clear the scene
    hou.hipFile.clear()

    # Create a geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a Zabob node and execute it
    box_node = node(geo.path(), "box", name="zabob_box", sizex=2.0, sizey=2.0, sizez=2.0)
    created_node = box_node.create(hou.OpNode)

        # Use pytest assertions if available
    if PYTEST_AVAILABLE:
        assert created_node is not None, "Node creation should succeed"
        assert created_node.path().endswith("zabob_box"), "Node should have correct name"
        sizex_parm = created_node.parm('sizex')
        assert sizex_parm is not None, "sizex parameter should exist"
        assert abs(sizex_parm.eval() - 2.0) < 0.001, "sizex should be set to 2.0"

    sizex_parm = created_node.parm('sizex')
    return {
        'created_path': created_node.path(),
        'sizex': sizex_parm.eval() if sizex_parm else None,
    }


@houdini_result
def test_zabob_chain_creation() -> JsonObject:
    """Test Zabob Chain creation in Houdini."""
    # Clear the scene
    hou.hipFile.clear()

    # Create a geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a chain of nodes
    box_node = node(geo.path(), "box", name="chain_box")
    xform_node = node(geo.path(), "xform", name="chain_xform")
    subdivide_node = node(geo.path(), "subdivide", name="chain_subdivide")

    processing_chain = chain(box_node, xform_node, subdivide_node)
    created_nodes = processing_chain.create()

    if PYTEST_AVAILABLE:
        assert len(created_nodes) == 3, "Chain should create 3 nodes"
        assert all(node_inst is not None for node_inst in created_nodes), "All nodes should be created"

    # Get the paths from the created NodeInstance objects
    node_paths: JsonArray = [created_node.create().path() for created_node in created_nodes]

    return {
        'chain_length': len(created_nodes),
        'node_paths': node_paths,
    }


@houdini_result
def test_node_with_inputs() -> JsonObject:
    """Test node creation with input connections."""
    # Clear the scene
    hou.hipFile.clear()

    # Create a geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create source node
    box_node = node(geo.path(), "box", name="input_box")
    box_created = box_node.create()

    # Create node with input connection using the hou.Node directly
    xform_node = node(geo.path(), "xform", name="connected_xform", _input=box_created)
    xform_created = xform_node.create()

    # Check connection
    inputs_tuple = xform_created.inputs()
    input_node = inputs_tuple[0] if inputs_tuple else None

    if PYTEST_AVAILABLE:
        assert box_created is not None, "Box node should be created"
        assert xform_created is not None, "Transform node should be created"
        assert input_node is not None, "Transform node should have input connection"
        assert input_node.path() == box_created.path(), "Input should be connected to box node"

    return {
        'box_path': box_created.path(),
        'xform_path': xform_created.path(),
        'connection_exists': input_node is not None,
        'connected_to': input_node.path() if input_node else None,
    }


@houdini_result
def test_caching_node_instance_create() -> JsonObject:
    """Test NodeInstance.create() caching behavior."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create NodeInstance and test caching
    box_node = node(geo.path(), "box", name="cache_test_box")

    # First call should create the node
    created_node1 = box_node.create()

    # Second call should return cached node
    created_node2 = box_node.create()

    # Verify they're the same object (cached)
    same_object = created_node1 is created_node2

    return {
        'same_object': same_object,
        'node_path': created_node1.path(),
    }


@houdini_result
def test_different_instances_different_nodes() -> JsonObject:
    """Test different NodeInstance objects create different nodes."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create two different NodeInstance objects
    node1 = node(geo.path(), "box", name="box1")
    node2 = node(geo.path(), "box", name="box2")

    created1 = node1.create()
    created2 = node2.create()

    different_objects = created1 is not created2
    different_paths = created1.path() != created2.path()

    return {
        'different_objects': different_objects,
        'different_paths': different_paths,
        'path1': created1.path(),
        'path2': created2.path(),
    }


@houdini_result
def test_chain_create_returns_node_instances() -> JsonObject:
    """Test Chain.create() returns tuple of NodeInstance copies."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a chain
    node1 = node(geo.path(), "box", name="chain_box")
    node2 = node(geo.path(), "sphere", name="chain_sphere")
    test_chain = chain(node1, node2)

    result_tuple = test_chain.create()

    # Check return type and length
    is_tuple = isinstance(result_tuple, tuple)
    tuple_length = len(result_tuple)

    # Check that items are NodeInstance objects
    all_node_instances = all(isinstance(item, NodeInstance) for item in result_tuple)

    # Test that they can create hou nodes
    hou_nodes = [item.create() for item in result_tuple]
    all_created = all(node is not None for node in hou_nodes)

    return {
        'is_tuple': is_tuple,
        'tuple_length': tuple_length,
        'all_node_instances': all_node_instances,
        'all_created': all_created,
        'node_paths': [node.path() for node in hou_nodes],
    }


@houdini_result
def test_chain_convenience_methods() -> JsonObject:
    """Test Chain convenience methods."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a 3-node chain
    node1 = node(geo.path(), "box", name="first_box")
    node2 = node(geo.path(), "sphere", name="middle_sphere")
    node3 = node(geo.path(), "merge", name="last_merge")
    test_chain = chain(node1, node2, node3)

    # Test convenience methods
    first = test_chain.first_node()
    last = test_chain.last_node()
    all_nodes = test_chain.hou_nodes()
    nodes_list = list(test_chain.nodes_iter())

    first_last_different = first is not last
    all_nodes_length = len(all_nodes)
    nodes_iter_length = len(nodes_list)

    return {
        'first_path': first.path(),
        'last_path': last.path(),
        'first_last_different': first_last_different,
        'all_nodes_length': all_nodes_length,
        'nodes_iter_length': nodes_iter_length,
        'all_nodes_paths': [node.path() for node in all_nodes],
    }


@houdini_result
def test_chain_empty_methods() -> JsonObject:
    """Test Chain convenience methods on empty chain."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create empty chain
    test_chain = chain()

    # Test methods that should work with empty chain
    all_nodes = test_chain.hou_nodes()
    nodes_list = list(test_chain.nodes_iter())

    # Test methods that should raise ValueError
    first_error = None
    last_error = None

    try:
        test_chain.first_node()
    except ValueError as e:
        first_error = str(e)

    try:
        test_chain.last_node()
    except ValueError as e:
        last_error = str(e)

    return {
        'all_nodes_empty': len(all_nodes) == 0,
        'nodes_iter_empty': len(nodes_list) == 0,
        'parent': test_chain.parent.name,
        'first_error': first_error,
        'last_error': last_error,
    }


@houdini_result
def test_node_instance_copy() -> JsonObject:
    """Test NodeInstance.copy() creates independent copies."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create original NodeInstance
    original = node(geo.path(), "box", name="original", sizex=2.0)
    copied = original.copy()

    # Test that they're different objects
    different_objects = copied is not original

    # Test that they have same basic properties
    same_parent = copied.parent == original.parent
    same_node_type = copied.node_type == original.node_type
    same_name = copied.name == original.name

    # Test that attributes are copied (not shared)
    attributes_equal = copied.attributes == original.attributes
    attributes_shared = copied.attributes is original.attributes

    return {
        'different_objects': different_objects,
        'same_parent': same_parent,
        'same_node_type': same_node_type,
        'same_name': same_name,
        'attributes_equal': attributes_equal,
        'attributes_shared': attributes_shared,
    }


@houdini_result
def test_node_instance_copy_with_inputs() -> JsonObject:
    """Test NodeInstance.copy() with various input types."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a chain to use as input
    inner_node = node(geo, "sphere")
    inner_chain = chain(inner_node)

    # Create node with chain input
    original = node(geo, "merge", _input=inner_chain)
    copied = original.copy()

    # Test input structure
    has_inputs = copied.inputs is not None
    input_length = len(copied.inputs) if copied.inputs else 0

    # The input chain should be copied (different object)
    input_copied = False
    if copied.inputs and len(copied.inputs) > 0:
    # Check if it's a different Chain object - inputs now returns (node, output_index) tuples or None
        input_copied = copied.inputs[0] is not None and copied.inputs[0][0] is not inner_chain

    return {
        'has_inputs': has_inputs,
        'input_length': input_length,
        'input_copied': input_copied,
    }


@houdini_result
def test_chain_copy() -> JsonObject:
    """Test Chain.copy() creates independent copy."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create original chain
    node1 = node(geo, "box")
    node2 = node(geo, "sphere")
    original = chain(node1, node2)

    # Copy the chain
    copied = original.copy()

    # Test basic properties
    different_objects = copied is not original
    same_parent = copied.parent == original.parent
    nodes_not_equal = all(a != b for (a, b) in zip(original.nodes, copied.nodes))
    nodes_not_shared = copied.nodes is not original.nodes

    return {
        'different_objects': different_objects,
        'same_parent': same_parent,
        "nodes_length": len(original.nodes) == len(copied.nodes),
        'nodes_not_shared': nodes_not_shared,
        'nodes_not_equal': nodes_not_equal,
    }

@houdini_result
def test_chain_copy_deep_nodes() -> JsonObject:
    """Test Chain.copy() deep copies NodeInstances."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create original chain with attributed nodes
    node1 = node(geo, "box", sizex=1.0)
    node2 = node(geo, "sphere")
    original = chain(node1, node2)

    # Copy the chain
    copied = original.copy()

    # Test that nodes are copied
    nodes_length = len(copied.nodes)
    nodes_different = all(copied.nodes[i] is not original.nodes[i] for i in range(len(copied.nodes)))

    # Test basic structure - just verify we have NodeInstance objects
    first_is_node_instance = isinstance(copied.nodes[0], NodeInstance)
    second_is_node_instance = isinstance(copied.nodes[1], NodeInstance)

    return {
        'nodes_length': nodes_length,
        'nodes_different': nodes_different,
        'first_is_node_instance': first_is_node_instance,
        'second_is_node_instance': second_is_node_instance,
    }


@houdini_result
def test_chain_copy_nested() -> JsonObject:
    """Test Chain.copy() recursively copies nested chains."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create nested structure
    inner_node = node(geo.path(), "box")
    inner_chain = chain(inner_node)

    outer_node = node(geo, "merge")
    original = chain(inner_chain, outer_node)

    # Copy the chain
    copied = original.copy()

    # Test structure
    nodes_length = len(copied.nodes)
    inner_chain_copied = copied.nodes[0] is not inner_chain

    # Test that first node is a Chain-like object
    first_is_chain = hasattr(copied.nodes[0], 'nodes')
    second_is_node_instance = hasattr(copied.nodes[1], 'node_type')

    return {
        'nodes_length': nodes_length,
        'inner_chain_copied': inner_chain_copied,
        'first_is_chain': first_is_chain,
        'second_is_node_instance': second_is_node_instance,
    }


@houdini_result
def test_empty_chain_create() -> JsonObject:
    """Test Chain.create() with empty chain returns empty tuple."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create empty chain
    test_chain = chain()  # Empty chain
    result = test_chain.create()

    is_tuple = isinstance(result, tuple)
    tuple_length = len(result)

    return {
        'is_tuple': is_tuple,
        'tuple_length': tuple_length,
    }

@houdini_result
def test_node_copy_non_chain_inputs() -> JsonObject:
    """Test NodeInstance.copy() preserves non-Chain inputs as-is."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a NodeInstance to use as input
    input_node = node(geo.path(), "box", name="input_box")

    # Create node with multiple inputs including None for sparse connections
    original = node(geo.path(), "merge", _input=[input_node, None])
    copied = original.copy()

    has_inputs = copied.inputs is not None
    input_length = len(copied.inputs) if copied.inputs else 0
    # inputs now returns (node, output_index) tuples for actual nodes, None for None inputs
    first_input_same = (copied.inputs[0][0] is input_node and copied.inputs[0][1] == 0) if copied.inputs and len(copied.inputs) > 0 and copied.inputs[0] is not None else False
    second_input_none = copied.inputs[1] is None if copied.inputs and len(copied.inputs) > 1 else False

    return {
        'has_inputs': has_inputs,
        'input_length': input_length,
        'first_input_same': first_input_same,
        'second_input_none': second_input_none,
    }


@houdini_result
def test_node_registry() -> JsonObject:
    """Test NodeInstance registry functionality."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a NodeInstance and get its hou.Node
    box_node = node(geo, "box", name="registry_test_box")
    created_hou_node = box_node.create()

    # Test 1: get_node_instance should return the original NodeInstance
    retrieved_instance = get_node_instance(created_hou_node)
    found_original = retrieved_instance is box_node

    # Test 2: wrap_node should return the original NodeInstance, not create a new one
    wrapped_instance = wrap_node(created_hou_node)
    wrap_returns_original = wrapped_instance is box_node

    # Test 3: Create another node with the hou.Node in a chain - should use original
    sphere_node = node(geo, "sphere", name="registry_test_sphere")
    # Create a chain that includes the raw hou.Node
    test_chain = chain(box_node, sphere_node)
    created_chain_nodes = test_chain.create()

    # The first node in the chain should not be the original NodeInstance
    # Chain creates new Nodeinstances owned by the chain.
    first_chain_node_is_original = created_chain_nodes[0].create() is created_hou_node

    return {
        'found_original': found_original,
        'wrap_returns_original': wrap_returns_original,
        'first_chain_node_is_original': first_chain_node_is_original,
        'original_node_path': created_hou_node.path(),
    }


@houdini_result
def test_hou_available() -> JsonObject:
    """Simple test to verify hou module is available."""
    version = hou.applicationVersion()
    app_name = hou.applicationName()

    if PYTEST_AVAILABLE:
        assert version is not None, "Houdini version should be available"
        assert app_name is not None, "Houdini application name should be available"

    return {
        'hou_version': list(version),
        'hou_app': app_name,
    }

@houdini_result
def test_node_parentage() -> JsonObject:
    """Test that parentage is correctly handled in NodeInstance."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")
    box = node(geo, 'test_box')

    return {
        'box_path': box.path,
        'geo_path': box.parent.path,
        'obj_path': box.parent.parent.path,
        'root_path': box.parent.parent.parent.path,
        'root_is_root': box.parent.parent.parent is ROOT,
    }


@houdini_result
def test_merge_inputs_sparse_handling() -> JsonObject:
    """Test _merge_inputs function with sparse (None) inputs."""
    from zabob_houdini.core import _merge_inputs, node

    # Clear the scene
    hou.hipFile.clear()

    # Create test nodes to use as inputs
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")
    node1 = node(geo.path(), "box", name="box1")
    node2 = node(geo.path(), "sphere", name="sphere1")
    c1 = (node1, 0)
    c2 = (node2, 0)
    in1: Inputs = (c1, )
    in2: Inputs = (c2, )

    # Test case 1: Both inputs are None - result should be None
    result1 = _merge_inputs((None,), (None,))
    both_none_result = result1[0] if result1 else None

    # Test case 2: First is None, second is not None - result should be second
    result2 = _merge_inputs((None,), in2)
    first_none_result = result2[0] if result2 else None
    first_none_is_node2 = first_none_result is c2

    # Test case 3: First is not None, second is None - result should be first
    result3 = _merge_inputs(in1, (None,))
    second_none_result = result3[0] if result3 else None
    second_none_is_node1 = second_none_result is c1

    # Test case 4: Both are not None - result should be first (preferring in1)
    result4 = _merge_inputs(in1, in2)
    both_not_none_result = result4[0] if result4 else None
    both_not_none_is_node1 = both_not_none_result is c1

    # Test case 5: Multiple positions with mixed None/not-None
    result5 = _merge_inputs((c1, None, c1), (None, c2, c2))
    multi_pos_correct = (
        len(result5) == 3 and
        result5[0] is c1 and  # First prefers in1
        result5[1] is c2 and  # None in1, so use in2
        result5[2] is c1      # Both not None, prefer in1
    )

    # Test case 6: Empty lists
    result6 = _merge_inputs((), ())
    empty_result = len(result6) == 0

    # Test case 7: One empty, one with content
    result7 = _merge_inputs((), (c1, c2))
    one_empty_result = len(result7) == 2 and result7[0] is c1 and result7[1] is c2

    return {
        'both_none_is_none': both_none_result is None,
        'first_none_gets_second': first_none_is_node2,
        'second_none_gets_first': second_none_is_node1,
        'both_not_none_gets_first': both_not_none_is_node1,
        'multi_position_correct': multi_pos_correct,
        'empty_lists_work': empty_result,
        'one_empty_works': one_empty_result,
    }


# New test functions for integration tests

@houdini_result
def test_diamond_creation() -> JsonObject:
    """Test diamond pattern node creation without duplication."""
    # Clear the scene
    hou.hipFile.clear()

    # Create the container geometry node
    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_diamond")

    # Chain A: Create base geometry (should be created once)
    chain_A = chain(
        node(geo_node, "box", "source_box"),
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
    node_paths: JsonArray = [node.create().path() for node in all_nodes]

    # Check for duplicates (there shouldn't be any in chain_A since B2/B3 reference it)
    unique_paths = list(set(node_paths))
    no_duplicates = len(unique_paths) == len(node_paths)

    # Verify connections
    scale_up_node = chain_B2_created[0].create()
    scale_down_node = chain_B3_created[0].create()
    center_node = chain_A_created[-1].create()

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


@houdini_result
def test_chain_connections() -> JsonObject:
    """Test that chain input connections work correctly."""
    # Clear the scene
    hou.hipFile.clear()

    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_connections")

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
    processor_node = connected_created[0].create()
    transform_node = source_created[-1].create()

    processor_input = processor_node.inputs()[0] if processor_node.inputs() else None
    connections_valid = processor_input and processor_input.path() == transform_node.path()

    return {
        'connections_valid': connections_valid,
        'processor_path': processor_node.path(),
        'transform_path': transform_node.path(),
    }


@houdini_result
def test_merge_connections() -> JsonObject:
    """Test merge node with multiple inputs."""
    # Clear the scene
    hou.hipFile.clear()

    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_merge")

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
    merge_node = merge_created[0].create()
    merge_inputs = len([inp for inp in merge_node.inputs() if inp])  # Count non-None inputs

    return {
        'merge_inputs': merge_inputs,
        'merge_path': merge_node.path(),
    }


@houdini_result
def test_geometry_node_creation(node_type: str) -> JsonObject:
    """Test creation of various geometry node types."""
    # Clear the scene
    hou.hipFile.clear()

    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", f"test_{node_type}")

    # Create the specified node type
    test_node = node(geo_node, node_type, f"test_{node_type}_node")
    created_node = test_node.create()

    return {
        'node_type': created_node.type().name(),
        'node_path': created_node.path(),
    }


@houdini_result
def test_node_parameters() -> JsonObject:
    """Test that node parameters are set correctly."""
    # Clear the scene
    hou.hipFile.clear()

    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_params")

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


# Additional test functions for the new unit tests

@houdini_result
def test_basic_input_connections() -> JsonObject:
    """Test that input connections are set up correctly on nodes."""
    # Clear the scene
    hou.hipFile.clear()

    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_connections")

    # Chain A: Create base geometry (should be created once)
    chain_A = chain(
        node(geo_node, "box", "source_box"),
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

    # Chain C: Should merge B2 and B3
    chain_C = chain(
        node(geo_node, "merge", "combine", _input=[chain_B2, chain_B3]),
        node(geo_node, "xform", "final"),
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


@houdini_result
def test_chain_input_delegation() -> JsonObject:
    """Test that Chain.inputs properly delegates to first node."""
    # Clear the scene
    hou.hipFile.clear()

    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_delegation")

    # Chain with no inputs
    chain_no_input = chain(
        node(geo_node, "box", "source"),
        node(geo_node, "xform", "transform"),
    )

    # Chain with single input
    chain_single_input = chain(
        node(geo_node, "xform", "processor", _input=chain_no_input),
        node(geo_node, "xform", "final"),
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


@houdini_result
def test_multiple_inputs_basic() -> JsonObject:
    """Test that nodes can accept multiple inputs correctly."""
    # Clear the scene
    hou.hipFile.clear()

    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_multi")

    # Create two source chains
    source_1 = chain(node(geo_node, "box", "source_1"))
    source_2 = chain(node(geo_node, "sphere", "source_2"))

    # Create a merge node that takes both as inputs
    merge_chain = chain(
        node(geo_node, "merge", "combiner", _input=[source_1, source_2])
    )

    # Test that the merge node has the expected inputs
    input_count = len(merge_chain.inputs)
    merge_has_multiple_inputs = input_count > 1

    return {
        'merge_has_multiple_inputs': merge_has_multiple_inputs,
        'input_count': input_count,
    }


# Note: The required test functions are already defined above:
# - test_diamond_creation (for diamond pattern)
# - test_chain_connections (for chain input connections)
# - test_merge_connections (for multiple input merge)
# - test_geometry_node_creation (for various geometry types)
# - test_node_parameters (for parameter setting)


@houdini_result
def test_diamond_no_duplication() -> JsonObject:
    """Test that diamond pattern doesn't create duplicate nodes - this should expose the bug!"""
    # Clear the scene
    hou.hipFile.clear()

    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_diamond_duplication")

    # Chain A: Create base geometry (should be created once)
    chain_A = chain(
        node(geo_node, "box", "source_box"),
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

    # Create all chains - this is where duplication might happen
    chain_A_created = chain_A.create()
    chain_B2_created = chain_B2.create()
    chain_B3_created = chain_B3.create()

    # Get ALL nodes that were created in the geo container
    all_children = geo_node.children()
    all_node_paths = [child.path() for child in all_children]
    unique_node_paths = list(set(all_node_paths))

    # Check connections to verify they're connecting to the right nodes
    scale_up_node = chain_B2_created[0].create()
    scale_down_node = chain_B3_created[0].create()
    center_node = chain_A_created[-1].create()

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


@houdini_result
def test_chain_reference_vs_copy() -> JsonObject:
    """Test that chains are referenced, not copied when used as inputs."""
    # Clear the scene
    hou.hipFile.clear()

    obj = hou_node("/obj")
    geo_node = obj.createNode("geo", "test_reference_vs_copy")

    # Create chain A
    chain_A = chain(
        node(geo_node, "box", "box_a"),
        node(geo_node, "xform", "xform_a"),
        node(geo_node, "subdivide", "subdivide_a"),
    )

    # Use chain A as input to two different nodes
    node_1 = node(geo_node, "xform", "node_1", _input=chain_A)
    node_2 = node(geo_node, "xform", "node_2", _input=chain_A)

    # Create everything
    chain_a_created = chain_A.create()
    node_1_created = node_1.create()
    node_2_created = node_2.create()

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


@houdini_result
def test_parameter_validation() -> JsonObject:
    """Test parameter validation in Houdini environment."""
    # Clear the scene
    hou.hipFile.clear()

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


@houdini_result
def test_chain_rejects_input_parameter() -> JsonObject:
    """Test that chain() properly rejects the deprecated _input parameter."""
    # Clear the scene
    hou.hipFile.clear()

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


@houdini_result
def test_valid_input_patterns() -> JsonObject:
    """Test that valid input patterns work correctly."""
    # Clear the scene
    hou.hipFile.clear()

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


@houdini_result
def test_node_input_validation() -> JsonObject:
    """Test that individual node input validation works."""
    # Clear the scene
    hou.hipFile.clear()

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


@houdini_result
def test_invalid_input_types(input_type: str) -> JsonObject:
    """Test that invalid input types are handled appropriately."""
    # Clear the scene
    hou.hipFile.clear()

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
