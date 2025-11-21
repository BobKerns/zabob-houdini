"""Node creation test functions."""

from typing import Any
import hou
from zabob_houdini.core import ROOT, node, hou_node
from zabob_houdini.utils import JsonObject


def _test_zabob_node_creation() -> JsonObject:
    """Test Zabob NodeInstance creation in Houdini."""
    # Create a geometry object for testing
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a Zabob node and execute it
    box_node = node(geo.path(), "box", name="zabob_box", sizex=2.0, sizey=2.0, sizez=2.0)
    created_node = box_node.create(hou.OpNode)
    sizex_parm = created_node.parm('sizex')
    return {
        'created_path': created_node.path(),
        'sizex': sizex_parm.eval() if sizex_parm else None,
    }


def _test_node_parentage() -> JsonObject:
    """Test that parentage is correctly handled in NodeInstance."""
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
