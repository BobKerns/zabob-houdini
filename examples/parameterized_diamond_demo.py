#!/usr/bin/env python3
"""
Parameterized Diamond Demo - Accepts command line arguments.
"""

import sys
from zabob_houdini import chain, node

def create_parameterized_diamond(box_size=1.0, scale_factor=1.5, rotation=45):
    """Create a diamond pattern with parameters."""

    print(f"Creating diamond with box_size={box_size}, scale_factor={scale_factor}, rotation={rotation}")

    # Chain A: Create base geometry
    chain_A = chain(
        node("/obj", "geo", "param_base"),
        node("/obj/param_base", "box", "param_box", sizex=box_size, sizey=box_size, sizez=box_size),
        node("/obj/param_base", "xform", "center", tx=0, ty=0, tz=0),
    )

    # Chain B2: First processing path
    chain_B2 = chain(
        node("/obj", "geo", "param_branch2"),
        node("/obj/param_branch2", "xform", "scale_up", sx=scale_factor, sy=scale_factor, sz=scale_factor),
        node("/obj/param_branch2", "xform", "rotate_y", ry=rotation),
        _input=chain_A,
    )

    # Chain B3: Second processing path
    chain_B3 = chain(
        node("/obj", "geo", "param_branch3"),
        node("/obj/param_branch3", "xform", "scale_down", sx=1/scale_factor, sy=1/scale_factor, sz=1/scale_factor),
        node("/obj/param_branch3", "xform", "rotate_x", rx=rotation/2),
        _input=chain_A,
    )

    # Chain C: Merge both processing paths
    chain_C = chain(
        node("/obj", "geo", "param_result"),
        node("/obj/param_result", "merge", "combine", _input=[chain_B2, chain_B3]),
        node("/obj/param_result", "xform", "final_pos", ty=3),
    )

    return chain_A, chain_B2, chain_B3, chain_C

if __name__ == "__main__":
    # Parse command line arguments
    box_size = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    scale_factor = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
    rotation = float(sys.argv[3]) if len(sys.argv) > 3 else 45.0

    print(f"Script arguments: {sys.argv}")

    chain_A, chain_B2, chain_B3, chain_C = create_parameterized_diamond(box_size, scale_factor, rotation)

    print("Creating parameterized chains...")
    chain_A.create()
    chain_B2.create()
    chain_B3.create()
    chain_C.create()

    print("✓ Parameterized diamond pattern created!")
