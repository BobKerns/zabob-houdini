"""Houdini integration test functions."""

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

import hou

from zabob_houdini.utils import JsonObject, JsonValue
from zabob_houdini.core import ROOT, znode, zchain, hou_node


def h_test_basic_node_creation_in_houdini() -> JsonObject:
    """Test basic node creation in Houdini."""
    # Create a geometry object
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create a box node
    box = geo.createNode("box", "test_box")

    return {
        'geo_path': geo.path(),
        'box_path': box.path(),
    }


def h_test_zabob_chain_creation() -> JsonObject:
    """Test Zabob ZChain creation in Houdini."""
    # Create a geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create a chain of nodes
    _box_node = znode(geo.path(), "box", name="chain_box")
    _xform_node = znode(geo.path(), "xform", name="chain_xform")
    _subdivide_node = znode(geo.path(), "subdivide", name="chain_subdivide")

    processing_chain = zchain(_box_node, _xform_node, _subdivide_node)
    created_nodes = processing_chain.create()

    # Get the paths from the created ZNode objects
    node_paths: list[JsonValue] = [created_node.path() for created_node in created_nodes]

    return {
        'chain_length': len(created_nodes),
        'node_paths': node_paths,
    }


def h_test_zabob_node_creation() -> JsonObject:
    """Test Zabob ZNode creation in Houdini."""
    # Create a geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create a Zabob node and execute it
    box_node = znode(geo.path(), "box", name="zabob_box", sizex=2.0, sizey=2.0, sizez=2.0)
    created_node = box_node.create(hou.OpNode)
    sizex_parm = created_node.parm('sizex')
    return {
        'created_path': created_node.path(),
        'sizex': sizex_parm.eval() if sizex_parm else None,
    }


def h_test_node_input_connections() -> JsonObject:
    """Test node creation with input connections."""
    # Create a geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create source node
    box_node = znode(geo.path(), "box", name="input_box")
    box_created = box_node.create()

    # Create node with input connection using the hou.Node directly
    xform_node = znode(geo.path(), "xform",
                       name="connected_xform",
                       _input=box_created)
    xform_created = xform_node.create()

    # Check connection
    inputs_tuple = xform_created.inputs()
    input_node = inputs_tuple[0] if inputs_tuple else None

    return {
        'box_path': box_created.path(),
        'xform_path': xform_created.path(),
        'connection_exists': input_node is not None,
        'connected_to': input_node.path() if input_node else None,
    }


def h_test_node_parentage() -> JsonObject:
    """Test that parentage is correctly handled in ZNode."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")
    box = znode(geo, 'test_box')

    return {
        'box_path': box.path,
        'geo_path': box.parent.path,
        'obj_path': box.parent.parent.path,
        'root_path': box.parent.parent.parent.path,
        'root_is_root': box.parent.parent.parent is ROOT,
    }


def h_test_hou_module_available() -> JsonObject:
    """Simple test to verify hou module is available."""
    version = hou.applicationVersion()
    app_name = hou.applicationName()

    return {
        'hou_version': list(version),
        'hou_app': app_name,
    }
