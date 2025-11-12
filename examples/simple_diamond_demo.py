#!/usr/bin/env python3
"""
Simple Diamond Chain Demo - Basic version without problematic nodes.

This demonstrates the basic A → B2 → C and A → B3 → C pattern.
"""

from zabob_houdini import chain, node

def create_simple_diamond():
    """Create a simple diamond pattern."""

    # Chain A: Create base geometry
    chain_A = chain(
        node("/obj", "geo", "base_geometry"),
        node("/obj/base_geometry", "box", "source_box", sizex=2, sizey=2, sizez=2),
        node("/obj/base_geometry", "xform", "center", tx=0, ty=0, tz=0),
    )

    # Chain B2: First processing path
    chain_B2 = chain(
        node("/obj", "geo", "process_branch2"),
        node("/obj/process_branch2", "xform", "scale_up", sx=1.5, sy=1.5, sz=1.5),
        node("/obj/process_branch2", "xform", "rotate_y", ry=45),
        _input=chain_A,
    )

    # Chain B3: Second processing path
    chain_B3 = chain(
        node("/obj", "geo", "process_branch3"),
        node("/obj/process_branch3", "xform", "scale_down", sx=0.8, sy=0.8, sz=0.8),
        node("/obj/process_branch3", "xform", "rotate_x", rx=30),
        _input=chain_A,
    )

    # Chain C: Merge both processing paths
    chain_C = chain(
        node("/obj", "geo", "merged_result"),
        node("/obj/merged_result", "merge", "combine_branches", _input=[chain_B2, chain_B3]),
        node("/obj/merged_result", "xform", "final_position", ty=2),
    )

    return chain_A, chain_B2, chain_B3, chain_C

if __name__ == "__main__":
    print("Creating simple diamond chain pattern...")

    chain_A, chain_B2, chain_B3, chain_C = create_simple_diamond()

    print("Creating chains...")
    chain_A.create()
    chain_B2.create()
    chain_B3.create()
    chain_C.create()

    print("✓ Simple diamond pattern created!")
    print("Topology: A → B2 → C")
    print("          A → B3 → C")
