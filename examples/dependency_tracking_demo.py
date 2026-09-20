#!/usr/bin/env python3
"""
Dependency tracking demonstration.

This example shows how to track which nodes depend on other nodes,
useful for understanding node graph structure and managing changes.
"""

from zabob_houdini import znode, zcontext


def main():
    """Demonstrate dependency tracking functionality."""

    # Create a geometry container
    geo = znode("/obj", "geo", "dependency_demo")

    with zcontext(geo) as ctx:
        # Create some source nodes
        box = ctx.node("box", "source_box")
        sphere = ctx.node("sphere", "source_sphere")

        # Create nodes that depend on the sources
        xform1 = ctx.node("xform", "transform_box", _input=box)
        xform2 = ctx.node("xform", "transform_sphere", _input=sphere)

        # Create a merge that depends on both transforms
        merge = ctx.node("merge", "combine_both", _input=[xform1, xform2])
        # Create a final output node
        output = ctx.node("xform", "final_output", _input=merge)

        # Create the entire graph
        output.create()

        # Now demonstrate dependency tracking
        print("Dependency Analysis:")
        print("==================")

        # Check what depends on each node using context methods
        box_deps = ctx.get_dependents(box)
        print(f"Box dependencies: {[n.name for n in box_deps]}")

        sphere_deps = ctx.get_dependents(sphere)
        print(f"Sphere dependencies: {[n.name for n in sphere_deps]}")

        xform1_deps = ctx.get_dependents(xform1)
        print(f"Transform1 dependencies: {[n.name for n in xform1_deps]}")

        xform2_deps = ctx.get_dependents(xform2)
        print(f"Transform2 dependencies: {[n.name for n in xform2_deps]}")

        merge_deps = ctx.get_dependents(merge)
        print(f"Merge dependencies: {[n.name for n in merge_deps]}")

        output_deps = ctx.get_dependents(output)
        print(f"Output dependencies: {[n.name for n in output_deps]}")        # Also demonstrate with a chain
        print("\nChain Dependencies:")
        print("==================")

        # Create a processing chain through context for dependency tracking
        with ctx.chain() as chn:
            chn.node("box", "chain_source")
            chn.node("noise", "add_noise")
            chn.node("smooth", "smooth_out")
            chn.node("xform", "final_transform")
        processing_chain = chn.chain

        # Check dependencies in the chain using context
        for i, node_in_chain in enumerate(processing_chain):
            deps = ctx.get_dependents(node_in_chain)
            print(f"ZChain node {i} ({node_in_chain.name}): {[n.name for n in deps]}")

        # Network topology analysis
        print("\nNetwork Topology Analysis:")
        print("==========================")

        # Network topology analysis using context methods
        sources = ctx.get_source_nodes()
        sinks = ctx.get_sink_nodes()

        print(f"Source nodes (no inputs): {[n.name for n in sources]}")
        print(f"Sink nodes (no dependents): {[n.name for n in sinks]}")

        # This helps identify entry and exit points of the node graph
        print(f"\nGraph has {len(sources)} entry points and {len(sinks)} exit points")


if __name__ == "__main__":
    main()
