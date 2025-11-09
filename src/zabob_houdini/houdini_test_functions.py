"""
Houdini-specific test functions that require the hou module.

This module contains test functions that can only run within Houdini's Python environment.
These functions are called by the hython bridge for testing purposes.
"""

import hou
from zabob_houdini.core import node, chain


def hou_node(path: str) -> 'hou.Node':
    """Get a Houdini node, raising exception if not found."""
    n = hou.node(path)
    if n is None:
        raise ValueError(f"Node at path '{path}' does not exist.")
    return n


def test_basic_node_creation():
    """Test basic node creation in Houdini."""
    # Clear the scene
    hou.hipFile.clear()

    # Create a geometry object
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a box node
    box = geo.createNode("box", "test_box")

    return {
        'geo_path': geo.path(),
        'box_path': box.path(),
        'success': True
    }


def test_zabob_node_creation():
    """Test Zabob NodeInstance creation in Houdini."""
    # Clear the scene
    hou.hipFile.clear()

    # Create a geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a Zabob node and execute it
    box_node = node(geo.path(), "box", name="zabob_box", sizex=2.0, sizey=2.0, sizez=2.0)
    created_node = box_node.create()

    return {
        'created_path': created_node.path(),
        'sizex': created_node.parm('sizex').eval(),
        'success': True
    }


def test_zabob_chain_creation():
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

    processing_chain = chain(geo.path(), box_node, xform_node, subdivide_node)
    created_nodes = processing_chain.create()

    return {
        'chain_length': len(created_nodes),
        'node_paths': [node.path() for node in created_nodes],
        'success': True
    }


def test_node_with_inputs():
    """Test node creation with input connections."""
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
    input_node = xform_created.input(0)

    return {
        'box_path': box_created.path(),
        'xform_path': xform_created.path(),
        'connection_exists': input_node is not None,
        'connected_to': input_node.path() if input_node else None,
        'success': True
    }


def test_hou_available():
    """Simple test to verify hou module is available."""
    return {
        'hou_version': '.'.join(map(str, hou.applicationVersion())),
        'hou_app': hou.applicationName(),
        'success': True
    }
