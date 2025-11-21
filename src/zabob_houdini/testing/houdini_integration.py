"""Houdini integration test functions."""

from typing import Any
import hou
from zabob_houdini.core import ROOT, node, chain, hou_node
from zabob_houdini.utils import JsonObject, JsonArray


def _test_basic_node_creation_in_houdini() -> JsonObject:
    """Test basic node creation in Houdini."""
    # Create a geometry object
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a box node
    box = geo.createNode("box", "test_box")

    return {
        'geo_path': geo.path(),
        'box_path': box.path(),
    }


def _test_zabob_chain_creation() -> JsonObject:
    """Test Zabob Chain creation in Houdini."""
    # Create a geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a chain of nodes
    box_node = node(geo.path(), "box", name="chain_box")
    xform_node = node(geo.path(), "xform", name="chain_xform")
    subdivide_node = node(geo.path(), "subdivide", name="chain_subdivide")

    processing_chain = chain(box_node, xform_node, subdivide_node)
    created_nodes = processing_chain.create()

    # Get the paths from the created NodeInstance objects
    node_paths = [created_node.create().path() for created_node in created_nodes]

    return {
        'chain_length': len(created_nodes),
        'node_paths': node_paths,
    }


def _test_hou_module_available() -> JsonObject:
    """Simple test to verify hou module is available."""
    version = hou.applicationVersion()
    app_name = hou.applicationName()

    return {
        'hou_version': list(version),
        'hou_app': app_name,
    }
