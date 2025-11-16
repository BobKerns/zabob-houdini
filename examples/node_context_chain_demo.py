"""
Example demonstrating NodeContext.chain() method with string lookup.

This shows how to use ctx.chain() with string names for convenient
chain creation using already defined nodes.
"""

from zabob_houdini import context, node

def demo_context_chain():
    """Demonstrate NodeContext.chain() with string name lookup."""

    # Create a geometry container and use context manager
    with context(node("/obj", "geo", "modeling")) as ctx:

        print("=== Creating individual nodes ===")

        # Create individual nodes with names
        box = ctx.node("box", "base_shape")
        subdivide = ctx.node("subdivide", "add_detail")
        transform = ctx.node("xform", "position")
        material = ctx.node("material", "shader")
        output = ctx.node("null", "final_output")

        print(f"Created nodes: {[n.name for n in [box, subdivide, transform, material, output]]}")

        print("\n=== Creating chains using string lookup ===")

        # Create chain using string names - much cleaner than passing NodeInstance objects
        modeling_chain = ctx.chain("base_shape", "add_detail", "position", "shader", "final_output")

        print(f"Modeling chain length: {len(modeling_chain)}")
        print("Chain node sequence:")
        for i, node_instance in enumerate(modeling_chain):
            print(f"  {i+1}. {node_instance.name} ({node_instance.node_type})")

        # Create a partial chain for processing steps only
        processing_chain = ctx.chain("base_shape", "add_detail", "position")

        print(f"\nProcessing chain length: {len(processing_chain)}")
        print("Processing steps:")
        for i, node_instance in enumerate(processing_chain):
            print(f"  {i+1}. {node_instance.name} ({node_instance.node_type})")

        print("\n=== Mixed string and node lookup ===")

        # Create external node not in context
        external_node = node(ctx.parent, "merge", "external_merge")

        # Mix string names and NodeInstance objects
        mixed_chain = ctx.chain("base_shape", external_node, "final_output")

        print(f"Mixed chain length: {len(mixed_chain)}")
        print("Mixed chain nodes:")
        for i, node_instance in enumerate(mixed_chain):
            print(f"  {i+1}. {node_instance.name} ({node_instance.node_type})")

        # Check that external node got registered in context
        try:
            registered_merge = ctx["external_merge"]
            print(f"\nExternal node registered: {registered_merge.name} ({registered_merge.node_type})")
        except KeyError:
            print("\nExternal node was not registered (this shouldn't happen!)")

        print("\n=== Error handling ===")

        try:
            # This should fail because the node doesn't exist
            bad_chain = ctx.chain("base_shape", "nonexistent_node", "final_output")
        except KeyError as e:
            print(f"Expected KeyError for missing node: {e}")

        return modeling_chain, processing_chain, mixed_chain

if __name__ == "__main__":
    chains = demo_context_chain()
    print(f"\nSuccessfully created {len(chains)} chains!")
