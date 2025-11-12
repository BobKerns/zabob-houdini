#!/usr/bin/env python3
"""
Parameterized Diamond Demo - Accepts command line arguments.
"""

import sys
from zabob_houdini import chain, node

def create_parameterized_diamond(box_size:float=1.0, scale_factor:float=1.5, rotation:float=45):
    """Create a diamond pattern with parameters within a single geo node."""

    print(f"Creating diamond with box_size={box_size}, scale_factor={scale_factor}, rotation={rotation}")

    # Create the container geometry node
    geo = node("/obj", "geo", name="param_diamond")

    # Chain A: Create base geometry
    chain_A = chain(
        node(geo, "box", "param_box", sizex=box_size, sizey=box_size, sizez=box_size),
        node(geo, "xform", "center", tx=0, ty=0, tz=0),
    )

    # Chain B2: First processing path
    chain_B2 = chain(
        node(geo, "xform", "scale_up", sx=scale_factor, sy=scale_factor, sz=scale_factor, _input=chain_A),
        node(geo, "xform", "rotate_y", ry=rotation),
    )

    # Chain B3: Second processing path
    chain_B3 = chain(
        node(geo, "xform", "scale_down", sx=1/scale_factor, sy=1/scale_factor, sz=1/scale_factor, _input=chain_A),
        node(geo, "xform", "rotate_x", rx=rotation/2),
    )

    # Chain C: Merge both processing paths
    chain_C = chain(
        node(geo, "merge", "combine", _input=[chain_B2, chain_B3]),
        node(geo, "xform", "final_pos", ty=3),
    )

    return geo, chain_A, chain_B2, chain_B3, chain_C

if __name__ == "__main__":
    # Parse command line arguments
    box_size = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    scale_factor = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
    rotation = float(sys.argv[3]) if len(sys.argv) > 3 else 45.0

    print(f"Script arguments: {sys.argv}")

    geo, chain_A, chain_B2, chain_B3, chain_C = create_parameterized_diamond(box_size, scale_factor, rotation)

    print("Creating parameterized chains...")
    geo.create()
    chain_A.create()
    chain_B2.create()
    chain_B3.create()
    chain_C.create()

    print("✓ Parameterized diamond pattern created!")
