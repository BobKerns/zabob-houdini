#!/usr/bin/env python3
"""
Example script demonstrating Zabob-Houdini chain functionality.

This script shows the API working without Houdini, demonstrating
the declarative nature of the node and chain definitions.
"""

from zabob_houdini import node, chain


def main():
    print("=== Zabob-Houdini Chain Examples ===\n")

    # Example 1: Basic node creation
    print("1. Basic node creation:")
    geo_node = node("/obj", "geo", name="mygeometry")
    print(f"   Created geo node: parent={geo_node.parent}, type={geo_node.node_type}, name={geo_node.name}")

    box_node = node(geo_node, "box", name="mybox")
    transform_node = node(geo_node, "xform", name="mytransform", _input=box_node)
    print(f"   Created box node: {box_node.name}")
    print(f"   Created transform node: {transform_node.name} (connected to {box_node.name})")
    print()

    # Example 2: Chain creation
    print("2. Chain creation:")
    box_node2 = node(geo_node, "box", name="source")
    xform_node = node(geo_node, "xform", name="transform")
    subdivide_node = node(geo_node, "subdivide", name="refine")
    processing_chain = chain(geo_node, box_node2, xform_node, subdivide_node)

    print(f"   Created chain with {len(processing_chain)} nodes:")
    for i in range(len(processing_chain)):
        print(f"     [{i}]: {processing_chain[i].name}")
    print()

    # Example 3: Chain indexing
    print("3. Chain indexing:")
    print(f"   First node: {processing_chain[0].name}")
    print(f"   Last node: {processing_chain[-1].name}")
    print(f"   Node by name 'transform': {processing_chain['transform'].name}")

    # Slice indexing
    subset_chain = processing_chain[1:3]
    print(f"   Subset chain [1:3] has {len(subset_chain)} nodes:")
    for i in range(len(subset_chain)):
        print(f"     [{i}]: {subset_chain[i].name}")
    print()

    # Example 4: Chain splicing
    print("4. Chain splicing:")
    normal_node = node(geo_node, "normal", name="normals")
    output_node = node(geo_node, "output", name="output")

    # Create a chain that includes another chain (will be spliced)
    detail_chain = chain(geo_node,
                        normal_node,
                        processing_chain,  # This chain is spliced in
                        output_node)

    print(f"   Detail chain with spliced processing_chain has {len(detail_chain)} nodes:")
    for i in range(len(detail_chain)):
        print(f"     [{i}]: {detail_chain[i].name}")
    print()

    # Example 5: Chain with input
    print("5. Chain with external input:")
    source_node = node(geo_node, "box", name="external_source")
    processing_chain_with_input = chain(geo_node,
                                       xform_node,
                                       subdivide_node,
                                       _input=source_node)

    print(f"   Chain with input from '{source_node.name}':")
    inputs = processing_chain_with_input.inputs or []
    print(f"   Chain inputs: {[inp.name if inp else None for inp in inputs]}")
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
