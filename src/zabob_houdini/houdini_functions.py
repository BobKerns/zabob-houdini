"""
Houdini-specific functions that require the hou module.

This module contains functions that can only run within Houdini's Python environment.
These functions are called by the hython bridge decorator.
"""

import hou
from zabob_houdini.core import node, chain

def hou_node(path: str) -> 'hou.Node':
    n =  hou.node(path)
    if n is None:
        raise ValueError(f"Node at path '{path}' does not exist.")
    return n

def simple_houdini_test():
    """Simple test that creates a box node."""
    # Get or create geometry node
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a box
    box = geo.createNode("box", "test_box")

    return f"Created box at: {box.path()}"


def chain_creation_test():
    """Test creating a chain using Zabob API in hython."""
    # Get or create geometry node
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "chain_test_geo")

    # Create chain using Zabob API
    box_node = node(geo.path(), "box", name="source")
    xform_node = node(geo.path(), "xform", name="transform")
    subdivide_node = node(geo.path(), "subdivide", name="refine")

    processing_chain = chain(geo.path(), box_node, xform_node, subdivide_node)

    # Create the chain
    created_nodes = processing_chain.create()

    return f"Created chain with {len(created_nodes)} nodes in {geo.path()}"


def create_test_chain():
    """Create a test processing chain for CLI testing."""
    # Ensure we have a geometry node
    geo = hou.node("/obj/geo1")
    if not geo:
        geo = hou_node("/obj").createNode("geo", "geo1")

    # Create chain using Zabob API
    box_node = node(geo.path(), "box", name="source")
    xform_node = node(geo.path(), "xform", name="transform")
    subdivide_node = node(geo.path(), "subdivide", name="refine")

    processing_chain = chain(geo.path(), box_node, xform_node, subdivide_node)

    # Create the chain
    result = processing_chain.create()
    return f"Chain created successfully: {len(result)} nodes"
