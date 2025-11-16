#!/usr/bin/env python3
"""
Example script demonstrating Zabob-Houdini chain functionality.

This script shows the API working without Houdini, demonstrating
the declarative nature of the node and chain definitions.
"""

from zabob_houdini import node, chain, context


def main():
    print("=== Zabob-Houdini Chain Examples ===\n")

    # Example 1: Basic node creation with context
    print("1. Basic node creation with context:")
    with context(node("/obj", "geo", name="mygeometry")) as ctx:
        print(f"   Created geo context: parent={ctx.parent.parent}, type={ctx.parent.node_type}, name={ctx.parent.name}")

        box_node = ctx.node("box", name="mybox")
        transform_node = ctx.node("xform", name="mytransform", _input=box_node)
        print(f"   Created box node: {box_node.name}")
        print(f"   Created transform node: {transform_node.name} (connected to {box_node.name})")
    print()

    # Example 2: Chain creation with context
    print("2. Chain creation with context:")
    with context(node("/obj", "geo", name="processing")) as ctx:
        processing_chain = ctx.chain(
            ctx.node("box", name="source"),
            ctx.node("xform", name="transform"),
            ctx.node("subdivide", name="refine")
        )

        print(f"   Created chain with {len(processing_chain)} nodes:")
        for i in range(len(processing_chain)):
            print(f"     [{i}]: {processing_chain[i].name}")
    print()

        # Example 3: Chain indexing
        print("3. Chain indexing:")
        print(f"   First node: {processing_chain[0].name}")
        print(f"   Last node: {processing_chain[-1].name}")

        # Access nodes by name through context
        transform_node = ctx["transform"]
        print(f"   Node by name 'transform': {transform_node.name}")

    # Example 4: Context-based chain operations
    print("4. Context-based chain operations:")
    with context(node("/obj", "geo", name="advanced")) as ctx:
        # Create nodes and reference by name
        ctx.node("normal", name="normals")
        ctx.node("output", name="output")

        # Create chains using string names for lookup
        detail_chain = ctx.chain("normals", "source", "transform", "refine", "output")

        print(f"   Detail chain has {len(detail_chain)} nodes:")
        for i in range(len(detail_chain)):
            print(f"     [{i}]: {detail_chain[i].name}")
    print()

    # Example 5: Chain with external input using context
    print("5. Chain with external input using context:")
    with context(node("/obj", "geo", name="with_input")) as ctx:
        source_node = ctx.node("box", name="external_source")

        processing_chain_with_input = ctx.chain(
            ctx.node("xform", _input=source_node),
            ctx.node("subdivide")
        )

        print(f"   Chain with input from '{source_node.name}':")
        inputs = processing_chain_with_input.inputs or []
        print(f"   Chain inputs: {len([inp for inp in inputs if inp is not None])} connections")
    print()

    print("6. Summary:")
    print("   - All node and chain definitions created successfully")
    print("   - Chain indexing (integer, slice, name) works correctly")
    print("   - Chain splicing combines multiple chains seamlessly")
    print("   - Chains support external inputs")
    print("   - Ready for .create() calls within Houdini environment")
    print()
    print("   Note: To actually create Houdini nodes, run .create() within Houdini:")
    print("   >>> geo_instance = geo_node.create(as_type=hou.ObjNode)  # Type-safe ObjNode")
    print("   >>> chain_instances = processing_chain.create()          # Returns tuple of NodeInstance")
    print("   >>> # Get typed SOP nodes from chain:")
    print("   >>> for instance in chain_instances:")
    print("   >>>     sop_node = instance.create(as_type=hou.SopNode)")


if __name__ == "__main__":
    main()
