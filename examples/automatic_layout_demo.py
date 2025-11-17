#!/usr/bin/env python3
"""
Zabob-Houdini Automatic Layout Demo

This example demonstrates the bidirectional layout algorithm and automatic
context management features.

Key Features Demonstrated:
- Automatic bidirectional layout (upward space allocation, downward positioning)
- Context automatic exit behavior (layout + node creation)
- Dependency tracking with sink node detection
- No manual .create() calls needed
- Smart conflict resolution and centering
"""

from zabob_houdini import node, context

def main():
    print("📐 Automatic Layout Demo")
    print("=" * 40)

    print("Creating complex node network with automatic layout...")

    with context(node("/obj", "geo", "layout_demo")) as ctx:
        # Create source nodes
        print("📦 Creating source geometry...")
        box1 = ctx.node("box", "source_box", sizex=1, sizey=1, sizez=1)
        sphere1 = ctx.node("sphere", "source_sphere", radius=0.8)

        # Create multiple processing paths that will be automatically laid out
        print("🔄 Building processing chains...")

        # Path 1: Box -> Transform -> Subdivide
        with ctx.chain(_input=box1) as box_path:
            box_path.node("xform", "box_transform", tx=2, ry=45)
            box_path.node("subdivide", "box_subdivide", iterations=2)

        # Path 2: Sphere -> Transform -> Noise
        with ctx.chain(_input=sphere1) as sphere_path:
            sphere_path.node("xform", "sphere_transform", tx=-2, rx=30)
            sphere_path.node("mountain", "sphere_noise", amp=0.2)

        # Path 3: Combined processing
        combined = ctx.merge(box_path, sphere_path, name="combined")

        with ctx.chain(_input=combined) as final_path:
            final_path.node("xform", "final_transform", ty=2)
            final_path.node("color", "final_color", color=(1, 0.5, 0))

        # Create a secondary branch for comparison
        with ctx.chain(_input=combined) as alt_path:
            alt_path.node("blast", "alt_blast", group="0")
            alt_path.node("extrude", "alt_extrude", dist=0.5)

        # Final merge of both branches
        output = ctx.merge(final_path, alt_path, name="final_output")

        print(f"📊 Network Statistics:")
        print(f"  Total nodes: {len(ctx._dependency_registry)}")
        print(f"  Source nodes: {len([n for n in ctx._dependency_registry if len(n.inputs) == 0])}")
        print(f"  Processing nodes: {len([n for n in ctx._dependency_registry if 0 < len(n.inputs) < 2])}")
        print(f"  Merge nodes: {len([n for n in ctx._dependency_registry if len(n.inputs) >= 2])}")

        print("\n🎯 Layout Algorithm Features:")
        print("  ✓ Bidirectional layout (upward + downward passes)")
        print("  ✓ Automatic conflict resolution")
        print("  ✓ Smart centering and spacing")
        print("  ✓ Dependency-aware positioning")

        print("\n🔄 Context will auto-apply layout and create all nodes on exit...")

    print("\n✅ Layout demo completed!")
    print("📝 The layout algorithm:")
    print("   1. Upward pass: Calculate required space for each layer")
    print("   2. Downward pass: Position nodes in allocated space")
    print("   3. Automatic sink detection and creation")
    print("   4. All nodes positioned optimally for readability")

if __name__ == "__main__":
    main()
