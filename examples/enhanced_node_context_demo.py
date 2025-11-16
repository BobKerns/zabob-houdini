"""
Enhanced NodeContext example showing node() method and name lookup.

This demonstrates the convenient ctx.node() method and dictionary-style
name lookup functionality.
"""

from zabob_houdini import context, node

def demo_enhanced_context():
    """Show the enhanced NodeContext with node() method and name lookup."""

    # Create a geometry container and use context manager
    with context(node("/obj", "geo", "processing")) as ctx:

        # Use ctx.node() instead of node(ctx.parent, ...)
        # This is more concise and readable

        # Create input geometry
        input_box = ctx.node("box", "input_geometry",
                            size=[2, 2, 2])

        # Transform operations
        scale_transform = ctx.node("xform", "scale_up",
                                  sx=1.5, sy=1.5, sz=1.5)

        rotate_transform = ctx.node("xform", "rotate",
                                   ry=45)

        # Processing nodes
        subdivide = ctx.node("subdivide", "smooth")

        # Output
        output = ctx.node("null", "OUTPUT")

        print("Created nodes:")
        print(f"- Input: {input_box.name} ({input_box.node_type})")
        print(f"- Scale: {scale_transform.name} ({scale_transform.node_type})")
        print(f"- Rotate: {rotate_transform.name} ({rotate_transform.node_type})")
        print(f"- Subdivide: {subdivide.name} ({subdivide.node_type})")
        print(f"- Output: {output.name} ({output.node_type})")

        # Demonstrate name lookup
        print("\nName lookup demonstration:")
        retrieved_input = ctx["input_geometry"]
        retrieved_output = ctx["OUTPUT"]

        print(f"Retrieved input same as original: {retrieved_input is input_box}")
        print(f"Retrieved output same as original: {retrieved_output is output}")

        # NEW: Demonstrate ctx.chain() method with string lookup
        print("\nChain creation with string lookup:")

        # Create a processing chain using node names
        processing_chain = ctx.chain("input_geometry", "scale_up", "rotate", "smooth", "OUTPUT")

        print(f"Created chain with {len(processing_chain)} nodes")
        print("Chain nodes:")
        for i, node_instance in enumerate(processing_chain):
            print(f"  {i}: {node_instance.name} ({node_instance.node_type})")

        # Demonstrate that context preserves original nodes (doesn't overwrite with chain copies)
        print(f"\nAfter chain creation:")
        chain_input = ctx["input_geometry"]
        print(f"Context preserves original node: {chain_input is input_box}")
        print(f"Original identity maintained: {chain_input.name} ({chain_input.node_type})")

        # Show error handling for missing names
        try:
            missing = ctx["nonexistent_node"]
        except KeyError as e:
            print(f"KeyError for missing node: {e}")

        # All nodes should have the same parent (context parent)
        all_nodes = [input_box, scale_transform, rotate_transform, subdivide, output]
        parents_match = all(n.parent == ctx.parent for n in all_nodes)
        print(f"\nAll original nodes have correct parent: {parents_match}")

        return all_nodes, processing_chain

if __name__ == "__main__":
    nodes, chain = demo_enhanced_context()
    print(f"\nCreated {len(nodes)} nodes and 1 chain with {len(chain)} nodes successfully!")
