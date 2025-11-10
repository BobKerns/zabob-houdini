"""
Houdini-specific test functions that require the hou module.

This module contains test functions that can only run within Houdini's Python environment.
These functions are called by the hython bridge for testing purposes.
"""

import hou
import json
import traceback
from zabob_houdini.core import hou_node, node, chain

# Import pytest but make it optional for when running standalone
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False


def test_basic_node_creation():
    """Test basic node creation in Houdini."""
    try:
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

        result = {
            'geo_path': geo.path(),
            'box_path': box.path(),
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_zabob_node_creation():
    """Test Zabob NodeInstance creation in Houdini."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create a geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create a Zabob node and execute it
        box_node = node(geo.path(), "box", name="zabob_box", sizex=2.0, sizey=2.0, sizez=2.0)
        created_node = box_node.create()

        # Use pytest assertions if available
        if PYTEST_AVAILABLE:
            assert created_node is not None, "Node creation should succeed"
            assert created_node.path().endswith("zabob_box"), "Node should have correct name"
            sizex_parm = created_node.parm('sizex')
            assert sizex_parm is not None, "sizex parameter should exist"
            assert abs(sizex_parm.eval() - 2.0) < 0.001, "sizex should be set to 2.0"

        sizex_parm = created_node.parm('sizex')
        result = {
            'created_path': created_node.path(),
            'sizex': sizex_parm.eval() if sizex_parm else None,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_zabob_chain_creation():
    """Test Zabob Chain creation in Houdini."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create a geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create a chain of nodes
        box_node = node(geo.path(), "box", name="chain_box")
        xform_node = node(geo.path(), "xform", name="chain_xform")
        subdivide_node = node(geo.path(), "subdivide", name="chain_subdivide")

        processing_chain = chain(geo.path(), box_node, xform_node, subdivide_node)
        created_nodes = processing_chain.create()

        if PYTEST_AVAILABLE:
            assert len(created_nodes) == 3, "Chain should create 3 nodes"
            assert all(node_inst is not None for node_inst in created_nodes), "All nodes should be created"

        # Get the paths from the created NodeInstance objects
        node_paths = []
        for node_instance in created_nodes:
            created_hou_node = node_instance.create()
            node_paths.append(created_hou_node.path())

        result = {
            'chain_length': len(created_nodes),
            'node_paths': node_paths,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_node_with_inputs():
    """Test node creation with input connections."""
    try:
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

        result = {
            'box_path': box_created.path(),
            'xform_path': xform_created.path(),
            'connection_exists': input_node is not None,
            'connected_to': input_node.path() if input_node else None,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_caching_node_instance_create():
    """Test NodeInstance.create() caching behavior."""
    try:
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

        result = {
            'same_object': same_object,
            'node_path': created_node1.path(),
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_different_instances_different_nodes():
    """Test different NodeInstance objects create different nodes."""
    try:
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

        result = {
            'different_objects': different_objects,
            'different_paths': different_paths,
            'path1': created1.path(),
            'path2': created2.path(),
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_chain_create_returns_node_instances():
    """Test Chain.create() returns tuple of NodeInstance copies."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create a chain
        node1 = node(geo.path(), "box", name="chain_box")
        node2 = node(geo.path(), "sphere", name="chain_sphere")
        test_chain = chain(geo.path(), node1, node2)

        result_tuple = test_chain.create()

        # Check return type and length
        is_tuple = isinstance(result_tuple, tuple)
        tuple_length = len(result_tuple)

        # Check that items are NodeInstance objects
        all_node_instances = all(hasattr(item, 'create') and hasattr(item, 'node_type') for item in result_tuple)

        # Test that they can create hou nodes
        hou_nodes = [item.create() for item in result_tuple]
        all_created = all(node is not None for node in hou_nodes)

        result = {
            'is_tuple': is_tuple,
            'tuple_length': tuple_length,
            'all_node_instances': all_node_instances,
            'all_created': all_created,
            'node_paths': [node.path() for node in hou_nodes],
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_chain_convenience_methods():
    """Test Chain convenience methods."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create a 3-node chain
        node1 = node(geo.path(), "box", name="first_box")
        node2 = node(geo.path(), "sphere", name="middle_sphere")
        node3 = node(geo.path(), "merge", name="last_merge")
        test_chain = chain(geo.path(), node1, node2, node3)

        # Test convenience methods
        first = test_chain.first_node()
        last = test_chain.last_node()
        all_nodes = test_chain.hou_nodes()
        nodes_list = list(test_chain.nodes_iter())

        first_last_different = first is not last
        all_nodes_length = len(all_nodes)
        nodes_iter_length = len(nodes_list)

        result = {
            'first_path': first.path(),
            'last_path': last.path(),
            'first_last_different': first_last_different,
            'all_nodes_length': all_nodes_length,
            'nodes_iter_length': nodes_iter_length,
            'all_nodes_paths': [node.path() for node in all_nodes],
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_chain_empty_methods():
    """Test Chain convenience methods on empty chain."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create empty chain
        test_chain = chain(geo.path())

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

        result = {
            'all_nodes_empty': len(all_nodes) == 0,
            'nodes_iter_empty': len(nodes_list) == 0,
            'first_error': first_error,
            'last_error': last_error,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_node_instance_copy():
    """Test NodeInstance.copy() creates independent copies."""
    try:
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

        result = {
            'different_objects': different_objects,
            'same_parent': same_parent,
            'same_node_type': same_node_type,
            'same_name': same_name,
            'attributes_equal': attributes_equal,
            'attributes_not_shared': attributes_not_shared,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_node_instance_copy_with_inputs():
    """Test NodeInstance.copy() with various input types."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create a chain to use as input
        inner_node = node(geo.path(), "sphere")
        inner_chain = chain(geo.path(), inner_node)

        # Create node with chain input
        original = node(geo.path(), "merge", _input=inner_chain)
        copied = original.copy()

        # Test input structure
        has_inputs = copied.inputs is not None
        input_length = len(copied.inputs) if copied.inputs else 0

        # The input chain should be copied (different object)
        input_copied = False
        if copied.inputs and len(copied.inputs) > 0:
            # Check if it's a different Chain object
            input_copied = copied.inputs[0] is not inner_chain

        result = {
            'has_inputs': has_inputs,
            'input_length': input_length,
            'input_copied': input_copied,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_chain_flatten_memoization():
    """Test Chain._flatten_nodes() memoization."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create a chain
        node1 = node(geo.path(), "box")
        node2 = node(geo.path(), "sphere")
        test_chain = chain(geo.path(), node1, node2)

        # First call to _flatten_nodes
        flattened1 = test_chain._flatten_nodes()
        flattened1_length = len(flattened1)

        # Second call should return cached result
        flattened2 = test_chain._flatten_nodes()
        same_object = flattened2 is flattened1

        result = {
            'flattened1_length': flattened1_length,
            'same_object': same_object,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_chain_flatten_nested():
    """Test Chain._flatten_nodes() with nested chains."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create nested chains
        node1 = node(geo.path(), "box")
        node2 = node(geo.path(), "sphere")
        inner_chain = chain(geo.path(), node1, node2)

        node3 = node(geo.path(), "merge")
        outer_chain = chain(geo.path(), inner_chain, node3)

        # Flatten the outer chain
        flattened = outer_chain._flatten_nodes()
        flattened_length = len(flattened)

        # Should have 3 individual NodeInstance objects
        # Test memoization as well
        flattened2 = outer_chain._flatten_nodes()
        same_object = flattened2 is flattened

        result = {
            'flattened_length': flattened_length,
            'same_object': same_object,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_chain_copy():
    """Test Chain.copy() creates independent copy."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create original chain
        node1 = node(geo.path(), "box")
        node2 = node(geo.path(), "sphere")
        original = chain(geo.path(), node1, node2)

        # Copy the chain
        copied = original.copy()

        # Test basic properties
        different_objects = copied is not original
        same_parent = copied.parent == original.parent
        nodes_equal = copied.nodes == original.nodes
        nodes_not_shared = copied.nodes is not original.nodes

        result = {
            'different_objects': different_objects,
            'same_parent': same_parent,
            'nodes_equal': nodes_equal,
            'nodes_not_shared': nodes_not_shared,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_chain_copy_deep_nodes():
    """Test Chain.copy() deep copies NodeInstances."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create original chain with attributed nodes
        node1 = node(geo.path(), "box", sizex=1.0)
        node2 = node(geo.path(), "sphere")
        original = chain(geo.path(), node1, node2)

        # Copy the chain
        copied = original.copy()

        # Test that nodes are copied
        nodes_length = len(copied.nodes)
        nodes_different = all(copied.nodes[i] is not original.nodes[i] for i in range(len(copied.nodes)))

        # Test basic structure - just verify we have NodeInstance-like objects
        first_is_node_instance = hasattr(copied.nodes[0], 'node_type') and hasattr(copied.nodes[0], 'attributes')
        second_is_node_instance = hasattr(copied.nodes[1], 'node_type') and hasattr(copied.nodes[1], 'attributes')

        result = {
            'nodes_length': nodes_length,
            'nodes_different': nodes_different,
            'first_is_node_instance': first_is_node_instance,
            'second_is_node_instance': second_is_node_instance,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_chain_copy_nested():
    """Test Chain.copy() recursively copies nested chains."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create nested structure
        inner_node = node(geo.path(), "box")
        inner_chain = chain(geo.path(), inner_node)

        outer_node = node(geo.path(), "merge")
        original = chain(geo.path(), inner_chain, outer_node)

        # Copy the chain
        copied = original.copy()

        # Test structure
        nodes_length = len(copied.nodes)
        inner_chain_copied = copied.nodes[0] is not inner_chain

        # Test that first node is a Chain-like object
        first_is_chain = hasattr(copied.nodes[0], 'nodes')
        second_is_node_instance = hasattr(copied.nodes[1], 'node_type')

        result = {
            'nodes_length': nodes_length,
            'inner_chain_copied': inner_chain_copied,
            'first_is_chain': first_is_chain,
            'second_is_node_instance': second_is_node_instance,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_empty_chain_create():
    """Test Chain.create() with empty chain returns empty tuple."""
    try:
        # Clear the scene
        hou.hipFile.clear()

        # Create geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "test_geo")

        # Create empty chain
        test_chain = chain(geo.path())  # Empty chain
        result = test_chain.create()

        is_tuple = isinstance(result, tuple)
        tuple_length = len(result)

        result_data = {
            'is_tuple': is_tuple,
            'tuple_length': tuple_length,
            'success': True
        }
        return json.dumps(result_data)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_node_copy_non_chain_inputs():
    """Test NodeInstance.copy() preserves non-Chain inputs as-is."""
    try:
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
        first_input_same = copied.inputs[0] is input_node if copied.inputs and len(copied.inputs) > 0 else False
        second_input_none = copied.inputs[1] is None if copied.inputs and len(copied.inputs) > 1 else False

        result = {
            'has_inputs': has_inputs,
            'input_length': input_length,
            'first_input_same': first_input_same,
            'second_input_none': second_input_none,
            'success': True
        }
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)


def test_hou_available():
    """Simple test to verify hou module is available."""
    try:
        version = '.'.join(map(str, hou.applicationVersion()))
        app_name = hou.applicationName()

        if PYTEST_AVAILABLE:
            assert version is not None, "Houdini version should be available"
            assert app_name is not None, "Houdini application name should be available"

        result = {
            'hou_version': version,
            'hou_app': app_name,
            'success': True
        }

        # Return JSON string for subprocess compatibility
        return json.dumps(result)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return json.dumps(error_result)
