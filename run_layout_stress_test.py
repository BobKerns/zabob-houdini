#!/usr/bin/env python3
"""
Quick Layout Stress Test Runner

This creates a comprehensive stress test .hip file to examine the layout algorithm.
Run this script directly in Houdini or via hython.

Usage:
    hython run_layout_stress_test.py
"""

import sys
import os

# Add the src directory to the path so we can import zabob_houdini
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from zabob_houdini import node, context, ROOT
    import hou

    def create_stress_test():
        """Create a comprehensive stress test for the layout algorithm."""

        print("Creating layout stress test...")

        # Clear scene
        hou.hipFile.clear()

        # Create geometry container
        obj = hou.node("/obj")
        geo = obj.createNode("geo", "layout_stress_test")

        with context(geo) as ctx:

            print("Creating test patterns...")

            # Pattern 1: Simple Diamond
            print("  - Diamond pattern")
            source1 = ctx.node("box", "diamond_source")
            branch1a = ctx.node("xform", "diamond_1a", _input=source1)
            branch1b = ctx.node("xform", "diamond_1b", _input=source1)
            branch1c = ctx.node("xform", "diamond_1c", _input=source1)
            diamond_merge = ctx.merge(branch1a, branch1b, branch1c, name="diamond_merge")

            # Pattern 2: Fan-out with multiple levels
            print("  - Multi-level fan-out")
            source2 = ctx.node("sphere", "fanout_source")

            # Level 1 fan-out
            fan_branches = []
            for i in range(4):
                branch = ctx.node("xform", f"fan_L1_{i}", _input=source2)
                fan_branches.append(branch)

            # Level 2 - pair up branches
            fan_pairs = []
            for i in range(0, len(fan_branches), 2):
                if i + 1 < len(fan_branches):
                    pair_merge = ctx.merge(fan_branches[i], fan_branches[i+1], name=f"fan_pair_{i//2}")
                    fan_pairs.append(pair_merge)

            # Level 3 - final merge
            if len(fan_pairs) > 1:
                fan_final = ctx.merge(*fan_pairs, name="fan_final")

            # Pattern 3: Complex cross-connections
            print("  - Complex cross-connections")
            sources = []
            for i in range(3):
                source = ctx.node("torus" if i % 2 else "tube", f"complex_source_{i}")
                sources.append(source)

            # Create processing layers with cross-connections
            layer1 = []
            for i, source in enumerate(sources):
                proc1 = ctx.node("xform", f"complex_L1_{i}a", _input=source)
                proc2 = ctx.node("xform", f"complex_L1_{i}b", _input=source)
                layer1.extend([proc1, proc2])

            # Layer 2 - cross-connect
            layer2 = []
            for i in range(0, len(layer1), 3):
                group = layer1[i:i+3]
                if len(group) >= 2:
                    merge_node = ctx.merge(*group, name=f"complex_L2_merge_{i//3}")
                    processed = ctx.node("xform", f"complex_L2_proc_{i//3}", _input=merge_node)
                    layer2.append(processed)

            # Final merge of everything interesting
            print("  - Final convergence")
            final_candidates = []
            if 'diamond_merge' in locals():
                final_candidates.append(diamond_merge)
            if 'fan_final' in locals():
                final_candidates.append(fan_final)
            if layer2:
                final_candidates.extend(layer2[:2])  # Just take first 2 to avoid too many inputs

            if len(final_candidates) > 1:
                ultimate_final = ctx.merge(*final_candidates, name="ultimate_final")
                final_output = ctx.node("xform", "final_output", _input=ultimate_final)

            print(f"\nTotal nodes created: {len(list(ctx._dependency_registry.keys()))}")

            # Apply layout
            print("Applying layout algorithm...")
            ctx.apply_layout(
                layer_height=3.0,
                node_width=2.5,
                min_spacing=1.0
            )

            # Get statistics
            all_nodes = list(ctx._dependency_registry.keys())
            layers = ctx._compute_layers(all_nodes)
            positions = ctx.layout_nodes()
            source_nodes = ctx.get_source_nodes()
            sink_nodes = ctx.get_sink_nodes()

            if positions:
                x_positions = [pos[0] for pos in positions.values()]
                y_positions = [pos[1] for pos in positions.values()]

                print(f"\nLayout Statistics:")
                print(f"  Total nodes: {len(all_nodes)}")
                print(f"  Source nodes: {len(source_nodes)}")
                print(f"  Sink nodes: {len(sink_nodes)}")
                print(f"  Layers: {len(layers)}")
                print(f"  Nodes per layer: {[len(nodes) for nodes in layers.values()]}")
                print(f"  X range: {min(x_positions):.2f} to {max(x_positions):.2f}")
                print(f"  Y range: {min(y_positions):.2f} to {max(y_positions):.2f}")
                print(f"  Total width: {max(x_positions) - min(x_positions):.2f}")
                print(f"  Total height: {max(y_positions) - min(y_positions):.2f}")

        # Save the file
        hip_path = os.path.join(current_dir, "layout_stress_test.hip")
        hou.hipFile.save(hip_path)
        print(f"\nSaved: {hip_path}")

        print("\nTo examine the results:")
        print("1. Open layout_stress_test.hip in Houdini")
        print("2. Go to /obj/layout_stress_test")
        print("3. Look at the node layout in the network editor")
        print("4. Observe how different patterns are handled:")
        print("   - Diamond patterns (fan-out then fan-in)")
        print("   - Multi-level hierarchies")
        print("   - Cross-connections between layers")
        print("   - Complex merge operations")

        return True

    if __name__ == "__main__":
        print("Layout Algorithm Stress Test")
        print("=" * 40)

        try:
            success = create_stress_test()
            if success:
                print("\n✓ Stress test completed successfully!")
            else:
                print("\n✗ Stress test failed!")
                sys.exit(1)

        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

except ImportError as e:
    print(f"Failed to import required modules: {e}")
    print("Make sure you're running this in Houdini (hython) with zabob_houdini available.")
    sys.exit(1)
