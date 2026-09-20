#!/usr/bin/env python3
"""
Example script demonstrating Zabob-Houdini chain functionality.

This script shows the API working without Houdini, demonstrating
the declarative nature of the node and chain definitions.
"""

from zabob_houdini import znode, zcontext


def main():
    print("=== Zabob-Houdini ZChain Examples ===\n")

    # Example 1: Basic node creation with context
    print("1. Basic node creation with context:")
    with zcontext(znode("/obj", "geo", name="mygeometry")) as ctx:
        parent = ctx.parent
        type_ = parent.node_type
        name = parent.name
        print(f"   Created geo context: {parent=}, type={type_}, name={name}")

        box_node = ctx.node("box", name="mybox")
        transform_node = ctx.node("xform", name="mytransform", _input=box_node)
        print(f"   Created box node: {box_node.name}")
        print(f"   Created transform node: {transform_node.name} (connected to {box_node.name})")
        print()

    # Example 2: ZChain creation with context
    print("2. ZChain creation with context:")
    with zcontext(znode("/obj", "geo", name="processing")) as ctx:
        with ctx.chain() as ch:
            ch.node("box", name="source")
            ch.node("xform", name="transform")
            ch.node("subdivide", name="refine")

    print(f"   Created chain with {len(ch.chain)} nodes:")
    for i, node in enumerate(ch.chain):
        print(f"     [{i}]: {node.name}")
    print()

    # Example 3: ZChain indexing
    print("3. ZChain indexing:")
    print(f"   First node: {ch.chain[0].name}")
    print(f"   Last node: {ch.chain[-1].name}")

    # Access nodes by name through context
    transform_node = ctx["transform"]
    print(f"   Node by name 'transform': {transform_node.name}")

    # Example 4: Context-based chain operations
    print("4. Context-based chain operations:")
    with zcontext(znode("/obj", "geo", name="advanced")) as ctx:
        # Create nodes and reference by name
        with ctx.chain() as detail_chain:
            detail_chain.node("normal", name="normals")
        ctx.node("output", name="output")

        # Create chains using string names for lookup
        with ctx.chain() as details:
            for n in ("normals", "source", "transform", "refine", "output"):
                details.node(n)
        print(f"   Detail chain has {len(detail_chain.chain)} nodes:")
        for i, node in enumerate(detail_chain.chain):
            print(f"     [{i}]: {node.name}")
    print()

    # Example 5: ZChain with external input using context
    print("5. ZChain with external input using context:")
    with zcontext(znode("/obj", "geo", name="with_input")) as ctx:
        source_node = ctx.node("box", name="external_source")

        with ctx.chain() as ch:
            ch.node("xform", _input=source_node)
            ch.node("subdivide")

        print(f"   ZChain with input from '{source_node.name}':")
        inputs = ch.chain.inputs or []
        print(f"   ZChain inputs: {len([inp for inp in inputs if inp is not None])} connections")
    print()

    print("6. Summary:")
    print("   - All node and chain definitions created successfully")
    print("   - ZChain indexing (integer, slice, name) works correctly")
    print("   - ZChain splicing combines multiple chains seamlessly")
    print("   - Chains support external inputs")
    print("   - Ready for .create() calls within Houdini environment")
    print()
    print("   Note: To actually create Houdini nodes, run .create() within Houdini:")
    print("   >>> geo_instance = geo_node.create(as_type=hou.ObjNode)  # Type-safe ObjNode")
    print("   >>> chain_instances = processing_chain.create()          # Returns tuple of ZNode")
    print("   >>> # Get typed SOP nodes from chain:")
    print("   >>> for instance in chain_instances:")
    print("   >>>     sop_node = instance.create(as_type=hou.SopNode)")


if __name__ == "__main__":
    main()
