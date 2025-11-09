"""
Example using the hython bridge.
"""

from zabob_houdini import in_hython


@in_hython
def simple_houdini_test():
    """Simple test that creates a box node."""
    import hou

    # Get or create geometry node
    obj = hou.node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a box
    box = geo.createNode("box", "test_box")

    return f"Created box at: {box.path()}"


@in_hython
def chain_creation_test():
    """Test creating a chain using Zabob API in hython."""
    import hou
    import sys
    from pathlib import Path

    # Add project to path (redundant but explicit)
    project_src = Path(__file__).parent.parent / "src"
    if str(project_src) not in sys.path:
        sys.path.insert(0, str(project_src))

    from zabob_houdini.core import node, chain

    # Get or create geometry node
    obj = hou.node("/obj")
    geo = obj.createNode("geo", "chain_test_geo")

    # Create chain using Zabob API
    box_node = node(geo.path(), "box", name="source")
    xform_node = node(geo.path(), "xform", name="transform")
    subdivide_node = node(geo.path(), "subdivide", name="refine")

    processing_chain = chain(geo.path(), box_node, xform_node, subdivide_node)

    # Create the chain
    created_nodes = processing_chain.create()

    return f"Created chain with {len(created_nodes)} nodes in {geo.path()}"




if __name__ == "__main__": 
    print("Testing hython bridge...")

    try:
        result1 = simple_houdini_test()
        print(f"✓ Simple test: {result1}")
    except Exception as e:
        print(f"✗ Simple test failed: {e}")

    try:
        result2 = chain_creation_test()
        print(f"✓ Chain test: {result2}")
    except Exception as e:
        print(f"✗ Chain test failed: {e}")
