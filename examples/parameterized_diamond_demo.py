#!/usr/bin/env python3
"""
Parameterized Diamond Demo - Accepts command line arguments.
"""

import sys
from zabob_houdini import zchain, znode


def create_parameterized_diamond(box_size: float = 1.0, scale_factor: float = 1.5, rotation: float = 45):
    """Create a diamond pattern with parameters within a single geo node."""

    print(f"Creating diamond with box_size={box_size}, scale_factor={scale_factor}, rotation={rotation}")

    # Create the container geometry node
    geo = znode("/obj", "geo", name="param_diamond")

    # ZChain A: Create base geometry
    chain_A = zchain(
        znode(geo, "box", "param_box", sizex=box_size, sizey=box_size, sizez=box_size),
        znode(geo, "xform", "center", tx=0, ty=0, tz=0),
    )

    # ZChain B2: First processing path - scale up and move right
    chain_B2 = zchain(
        znode(geo, "xform", "scale_up", sx=scale_factor, sy=scale_factor, sz=scale_factor, _input=chain_A),
        znode(geo, "xform", "rotate_y", ry=rotation),
        znode(geo, "xform", "translate_right", tx=4),  # Move right for visibility
    )

    # ZChain B3: Second processing path - scale down and move left
    chain_B3 = zchain(
        znode(geo, "xform", "scale_down",
              sx=1 / scale_factor,
              sy=1 / scale_factor,
              sz=1 / scale_factor,
              _input=chain_A),
        znode(geo, "xform", "rotate_x", rx=rotation / 2),
        znode(geo, "xform", "translate_left", tx=-4),  # Move left for visibility
    )

    # ZChain C: Merge both processing paths
    chain_C = zchain(
        znode(geo, "merge", "combine", _input=[chain_B2, chain_B3]),
        znode(geo, "xform", "final_pos", ty=3, _display=True, _render=True),  # Set display and render flags
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
    # Only need to create the container and final chain - it will propagate through inputs
    geo.create()
    chain_C.create()

    print("✓ Parameterized diamond pattern created!")
    print("Both cubes should be visible with translations and display/render flags set")
