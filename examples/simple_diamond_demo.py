#!/usr/bin/env python3
"""
Simple Diamond Chain Demo - Basic version without problematic nodes.

This demonstrates the basic A → B2 → C and A → B3 → C pattern.
"""

from zabob_houdini import chain, node

def create_simple_diamond():
    """Create a simple diamond pattern within a single geo node."""

    # Create the container geometry node
    geo = node("/obj", "geo", name="diamond")

    # Chain A: Create base geometry
    chain_A = chain(
        node(geo, "box", "source_box", sizex=2, sizey=2, sizez=2),
        node(geo, "xform", "center", tx=0, ty=0, tz=0),
    )

    # Chain B2: First processing path
    chain_B2 = chain(
        node(geo, "xform", "scale_up", sx=1.5, sy=1.5, sz=1.5, _input=chain_A),
        node(geo, "xform", "rotate_y", ry=45),
    )

    # Chain B3: Second processing path
    chain_B3 = chain(
        node(geo, "xform", "scale_down", sx=0.8, sy=0.8, sz=0.8, _input=chain_A),
        node(geo, "xform", "rotate_x", rx=30),
    )

    # Chain C: Merge both processing paths
    chain_C = chain(
        node(geo, "merge", "combine_branches", _input=[chain_B2, chain_B3]),
        node(geo, "xform", "final_position", ty=2),
    )

    return geo, chain_A, chain_B2, chain_B3, chain_C

if __name__ == "__main__":
    print("Creating simple diamond chain pattern...")

    geo, chain_A, chain_B2, chain_B3, chain_C = create_simple_diamond()

    print("Creating chains...")
    geo.create()
    chain_A.create()
    chain_B2.create()
    chain_B3.create()
    chain_C.create()

    print("✓ Simple diamond pattern created!")
    print("Topology: A → B2 → C")
    print("          A → B3 → C")
