#!/usr/bin/env python3
"""
Zabob-Houdini ZChainBuilder Context Manager Demo

This example demonstrates the new ZChainBuilder context manager pattern
that allows building chains with conditional logic and automatic registration.

Key Features Demonstrated:
- ZChainBuilder as context manager: ctx.chain() -> ZChainBuilder
- Automatic dependency tracking and node registration
- Conditional node inclusion in chains
- Automatic layout and node creation on context exit
- No need to manually call .create()
"""

from zabob_houdini import znode, zcontext


def main():
    print("🚀 ZChainBuilder Context Manager Demo")
    print("=" * 50)

    # Configuration for conditional processing
    add_subdivision = True
    add_noise = False
    add_deformation = True

    print(f"Configuration:")
    print(f"  Add subdivision: {add_subdivision}")
    print(f"  Add noise: {add_noise}")
    print(f"  Add deformation: {add_deformation}")
    print()

    # Create geometry context with automatic management
    with zcontext(znode("/obj", "geo", "chainbuilder_demo")) as ctx:
        print("📦 Creating source geometry...")
        source = ctx.node("box", "source", sizex=2, sizey=2, sizez=2)

        print("🔄 Building processing path A with ZChainBuilder...")
        with ctx.chain(_input=source) as path_a:
            path_a.node("xform", "transform_a", tx=3)

            if add_subdivision:
                print("  ➕ Adding subdivision to path A")
                path_a.node("subdivide", "subdivide_a")

        print("🔄 Building processing path B with ZChainBuilder...")
        with ctx.chain(_input=source) as path_b:
            path_b.node("xform", "transform_b", tx=-3)

            # Different conditions for path B
            if add_deformation:
                print("  ➕ Adding deformation to path B")
                path_b.node("twist", "twist_b", strength=45)

            # Always add a color node to path B
            path_b.node("color", "color_b", color=(0, 1, 0))

        print("🔀 Merging paths...")
        # final is available for use later.
        final_merge = ctx.merge(path_a, path_b, name="final_merge")

        print(f"📊 Created {len(ctx._dependency_registry)} nodes in context:")
        print(f"  Final merge node: {final_merge.name} ({final_merge.node_type})")
        for node_inst in ctx._dependency_registry:
            print(f"  - {node_inst.name} ({node_inst.resolved.node_type})")

        print("\n🎯 Context will auto-apply layout and create nodes on exit...")

    print("✅ Demo completed! Check the Houdini scene for results.")


if __name__ == "__main__":
    main()
