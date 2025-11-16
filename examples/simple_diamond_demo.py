#!/usr/bin/env python3
"""
Simple Diamond Chain Demo - Basic version without problematic nodes.

This demonstrates the basic A → B2 → C and A → B3 → C pattern.
"""

from zabob_houdini import chain, node, context

def create_simple_diamond():
    """Create a simple diamond pattern within a single geo node."""

    # Create the container geometry node and use context manager
    with context(node("/obj", "geo", name="diamond")) as ctx:
        # Chain A: Create base geometry
        chain_A = ctx.chain(
            ctx.node("box", "source_box", sizex=2, sizey=2, sizez=2),
            ctx.node("xform", "center", tx=0, ty=0, tz=0),
        )

        # Chain B2: First processing path - scale up and move right
        chain_B2 = ctx.chain(
            ctx.node("xform", "scale_up", sx=1.5, sy=1.5, sz=1.5, _input=chain_A),
            ctx.node("xform", "rotate_y", ry=45),
            ctx.node("xform", "translate_right", tx=3),  # Move right so we can see both
        )

        # Chain B3: Second processing path - scale down and move left
        chain_B3 = ctx.chain(
            ctx.node("xform", "scale_down", sx=0.8, sy=0.8, sz=0.8, _input=chain_A),
            ctx.node("xform", "rotate_x", rx=30),
            ctx.node("xform", "translate_left", tx=-3),  # Move left so we can see both
        )

        # Chain C: Merge both processing paths
        chain_C = ctx.chain(
            ctx.node("merge", "combine_branches", _input=[chain_B2, chain_B3]),
            ctx.node("xform", "final_position", ty=2, _display=True, _render=True),  # Set display and render flags
        )

        return ctx.parent, chain_A, chain_B2, chain_B3, chain_C

if __name__ == "__main__":
    print("Creating simple diamond chain pattern...")

    geo, chain_A, chain_B2, chain_B3, chain_C = create_simple_diamond()

    print("Creating chains...")
    # Only need to create the container and final chain - it will propagate through inputs
    geo.create()
    chain_C.create()

    print("✓ Simple diamond pattern created!")
    print("Topology: A → B2 → C")
    print("          A → B3 → C")
    print("Both cubes should be visible with translations to left and right")
