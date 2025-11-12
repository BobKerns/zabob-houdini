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

import re
import hou
import json
import traceback
from zabob_houdini.core import ROOT, NodeInstance, get_node_instance, hou_node, node, chain, wrap_node
from zabob_houdini.houdini_bridge import JsonArray, houdini_result, JsonObject

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
    attributes_not_shared = copied.attributes is not original.attributes

    return {
        'different_objects': different_objects,
        'same_parent': same_parent,
        'same_node_type': same_node_type,
        'same_name': same_name,
        'attributes_equal': attributes_equal,
        'attributes_not_shared': attributes_not_shared,
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
def test_chain_flatten_memoization() -> JsonObject:
    """Test Chain._flatten_nodes() memoization."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a chain
    node1 = node(geo, "box")
    node2 = node(geo, "sphere")
    test_chain = chain(node1, node2)

    # First call to _flatten_nodes
    flattened1 = test_chain._flatten_nodes()
    flattened1_length = len(flattened1)

    # Second call should return cached result
    flattened2 = test_chain._flatten_nodes()
    same_object = flattened2 is flattened1

    return {
        'flattened1_length': flattened1_length,
        'same_object': same_object,
    }


@houdini_result
def test_chain_flatten_nested() -> JsonObject:
    """Test Chain._flatten_nodes() with nested chains."""
    # Clear the scene
    hou.hipFile.clear()

    # Create geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create nested chains
    node1 = node(geo, "box")
    node2 = node(geo, "sphere")
    inner_chain = chain( node1, node2)

    node3 = node(geo, "merge")
    outer_chain = chain(inner_chain, node3)

    # Flatten the outer chain
    flattened = outer_chain._flatten_nodes()
    flattened_length = len(flattened)

    # Should have 3 individual NodeInstance objects
    # Test memoization as well
    flattened2 = outer_chain._flatten_nodes()
    same_object = flattened2 is flattened

    return {
        'flattened_length': flattened_length,
        'same_object': same_object,
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
    nodes_equal = copied.nodes == original.nodes
    nodes_not_shared = copied.nodes is not original.nodes

    return {
        'different_objects': different_objects,
        'same_parent': same_parent,
        'nodes_equal': nodes_equal,
        'nodes_not_shared': nodes_not_shared,
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
    box_node = node(geo.path(), "box", name="registry_test_box")
    created_hou_node = box_node.create()

    # Test 1: get_node_instance should return the original NodeInstance
    retrieved_instance = get_node_instance(created_hou_node)
    found_original = retrieved_instance is box_node

    # Test 2: wrap_node should return the original NodeInstance, not create a new one
    wrapped_instance = wrap_node(created_hou_node)
    wrap_returns_original = wrapped_instance is box_node

    # Test 3: Create another node with the hou.Node in a chain - should use original
    sphere_node = node(geo.path(), "sphere", name="registry_test_sphere")
    # Create a chain that includes the raw hou.Node
    test_chain = chain(box_node, sphere_node)
    created_chain_nodes = test_chain.create()

    # The first node in the chain should be the original NodeInstance
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

    # Test case 1: Both inputs are None - result should be None
    result1 = _merge_inputs((None,), (None,))
    both_none_result = result1[0] if result1 else None

    # Test case 2: First is None, second is not None - result should be second
    result2 = _merge_inputs((None,), (node2,))
    first_none_result = result2[0] if result2 else None
    first_none_is_node2 = first_none_result is node2

    # Test case 3: First is not None, second is None - result should be first
    result3 = _merge_inputs((node1,), (None,))
    second_none_result = result3[0] if result3 else None
    second_none_is_node1 = second_none_result is node1

    # Test case 4: Both are not None - result should be first (preferring in1)
    result4 = _merge_inputs((node1,), (node2,))
    both_not_none_result = result4[0] if result4 else None
    both_not_none_is_node1 = both_not_none_result is node1

    # Test case 5: Multiple positions with mixed None/not-None
    result5 = _merge_inputs((node1, None, node1), (None, node2, node2))
    multi_pos_correct = (
        len(result5) == 3 and
        result5[0] is node1 and  # First prefers in1
        result5[1] is node2 and  # None in1, so use in2
        result5[2] is node1      # Both not None, prefer in1
    )

    # Test case 6: Empty lists
    result6 = _merge_inputs((), ())
    empty_result = len(result6) == 0

    # Test case 7: One empty, one with content
    result7 = _merge_inputs((), (node1, node2))
    one_empty_result = len(result7) == 2 and result7[0] is node1 and result7[1] is node2

    return {
        'both_none_is_none': both_none_result is None,
        'first_none_gets_second': first_none_is_node2,
        'second_none_gets_first': second_none_is_node1,
        'both_not_none_gets_first': both_not_none_is_node1,
        'multi_position_correct': multi_pos_correct,
        'empty_lists_work': empty_result,
        'one_empty_works': one_empty_result,
    }
