"""
Houdini-specific test functions that require the hou module.

This module contains test functions that can only run within Houdini's Python environment.
These functions are called by the hython bridge for testing purposes.
"""

import hou
import json
import traceback
from zabob_houdini.core import node, chain

# Import pytest but make it optional for when running standalone
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False


def hou_node(path: str) -> 'hou.Node':
    """Get a Houdini node, raising exception if not found."""
    n = hou.node(path)
    if n is None:
        raise ValueError(f"Node at path '{path}' does not exist.")
    return n


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
            assert all(node is not None for node in created_nodes), "All nodes should be created"

        result = {
            'chain_length': len(created_nodes),
            'node_paths': [node.path() for node in created_nodes],
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

        # Create node with input connection
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
