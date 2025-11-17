#!/usr/bin/env python3
"""
Layout Algorithm Stress Test Demo

This demo creates various complex node graph patterns to stress test
the layout algorithm and generate a .hip file for visual inspection.

Test patterns include:
1. Simple chain
2. Diamond pattern (fan-out then fan-in)
3. Multiple merge operations
4. Deep hierarchy with branches
5. Wide fan-out with multiple levels
6. Complex mixed patterns

Run with: python examples/layout_stress_test_demo.py
Or via hython for direct Houdini execution.
"""

from zabob_houdini import node, chain, context, ROOT, merge
import hou

def create_layout_stress_test():
    """Create comprehensive layout stress test scenarios."""

    # Clear the scene
    hou.hipFile.clear()

    # Get the main geometry container
    obj = hou.node("/obj")
    geo_container = obj.createNode("geo", "layout_test_geo")

    print("Creating layout stress test scenarios...")

    with context(geo_container) as ctx:
        print("\n=== Test 1: Simple Chain ===")
        # Simple linear chain
        box1 = ctx.node("box", "chain_box", sizex=1.0, sizey=1.0, sizez=1.0)
        transform1 = ctx.node("xform", "chain_xform1", _input=box1, tx=1.0)
        subdivide1 = ctx.node("subdivide", "chain_subdivide", _input=transform1, iterations=2)

        print("\n=== Test 2: Diamond Pattern ===")
        # Diamond: single source, split to multiple, then merge back
        source_sphere = ctx.node("sphere", "diamond_source", rad=(0.8, 0.8, 0.8))

        # Split into multiple paths
        path_a = ctx.node("mountain", "diamond_path_a", _input=source_sphere)
        path_b = ctx.node("subdivide", "diamond_path_b", _input=source_sphere, iterations=1)
        path_c = ctx.node("subdivide", "diamond_path_c", _input=source_sphere, iterations=1)

        # Merge back together
        diamond_merge = ctx.merge(path_a, path_b, path_c, name="diamond_merge")
        diamond_final = ctx.node("smooth", "diamond_final", _input=diamond_merge)

        print("\n=== Test 3: Multiple Merge Operations ===")
        # Create multiple independent sources
        cube_a = ctx.node("box", "merge_cube_a", sizex=0.5)
        cube_b = ctx.node("box", "merge_cube_b", sizey=0.7)
        cube_c = ctx.node("box", "merge_cube_c", sizez=0.9)
        sphere_a = ctx.node("sphere", "merge_sphere_a", rad=(0.6, 0.6, 0.6))
        sphere_b = ctx.node("sphere", "merge_sphere_b", rad=(0.4, 0.4, 0.4))

        # Multiple merge operations
        cubes_merge = ctx.merge(cube_a, cube_b, cube_c, name="cubes_merge")
        spheres_merge = ctx.merge(sphere_a, sphere_b, name="spheres_merge")
        all_geo_merge = ctx.merge(cubes_merge, spheres_merge, name="all_geo_merge")

        print("\n=== Test 4: Deep Hierarchy with Branches ===")
        # Deep tree with multiple branches at different levels
        root_torus = ctx.node("torus", "tree_root", radx=1.0, rady=0.3)

        # Level 1 branches
        branch_1a = ctx.node("mountain", "tree_1a", _input=root_torus)
        branch_1b = ctx.node("twist", "tree_1b", _input=root_torus, strength=45)

        # Level 2 branches from 1a
        branch_2a = ctx.node("subdivide", "tree_2a", _input=branch_1a, iterations=1)
        branch_2b = ctx.node("smooth", "tree_2b", _input=branch_1a, strength=0.5)

        # Level 2 branches from 1b
        branch_2c = ctx.node("xform", "tree_2c", _input=branch_1b, s=(1.1, 1.1, 1.1))
        branch_2d = ctx.node("normal", "tree_2d", _input=branch_1b)

        # Level 3 - merge some branches
        level3_merge_a = ctx.merge(branch_2a, branch_2b, name="tree_merge_3a")
        level3_merge_b = ctx.merge(branch_2c, branch_2d, name="tree_merge_3b")

        # Final merge
        tree_final = ctx.merge(level3_merge_a, level3_merge_b, name="tree_final")

        print("\n=== Test 5: Wide Fan-out with Multiple Levels ===")
        # Single source with very wide fan-out
        fan_source = ctx.node("grid", "fan_source", sizex=2.0, sizey=2.0)

        # First level - wide fan-out (6 branches)
        fan_branches = []
        for i in range(6):
            branch = ctx.node("mountain", f"fan_branch_{i}",
                            _input=fan_source)
            fan_branches.append(branch)

        # Second level - pair up branches
        fan_pairs = []
        for i in range(0, len(fan_branches), 2):
            if i + 1 < len(fan_branches):
                pair_merge = ctx.merge(fan_branches[i], fan_branches[i+1],
                                     name=f"fan_pair_{i//2}")
                pair_transform = ctx.node("xform", f"fan_transform_{i//2}",
                                        _input=pair_merge, ty=i * 0.2)
                fan_pairs.append(pair_transform)

        # Third level - final merge
        if len(fan_pairs) > 1:
            fan_final = ctx.merge(*fan_pairs, name="fan_final")

        print("\n=== Test 6: Complex Mixed Pattern ===")
        # Combination of multiple patterns

        # Create multiple independent sources
        mixed_sources = []
        for i in range(4):
            if i % 2 == 0:
                rad_val = 0.3 + i * 0.1
                source = ctx.node("sphere", f"mixed_sphere_{i}", rad=(rad_val, rad_val, rad_val))
            else:
                source = ctx.node("box", f"mixed_box_{i}", sizex=0.4 + i * 0.1)
            mixed_sources.append(source)

        # Create diamond patterns from some sources
        diamond_results = []
        for i, source in enumerate(mixed_sources[:2]):
            # Each source splits into 3 paths
            path1 = ctx.node("smooth", f"mixed_diamond_{i}_path1", _input=source, strength=0.3)
            path2 = ctx.node("smooth", f"mixed_diamond_{i}_path2", _input=source, strength=0.3)
            path3 = ctx.node("subdivide", f"mixed_diamond_{i}_path3", _input=source, iterations=1)

            # Merge the paths
            diamond_result = ctx.merge(path1, path2, path3, name=f"mixed_diamond_{i}_result")
            diamond_results.append(diamond_result)

        # Create chains from remaining sources
        chain_results = []
        for i, source in enumerate(mixed_sources[2:], start=2):
            transform = ctx.node("xform", f"mixed_chain_{i}_xform", _input=source, rx=30)
            mountain = ctx.node("mountain", f"mixed_chain_{i}_mountain", _input=transform)
            chain_results.append(mountain)

        # Final complex merge
        all_mixed = diamond_results + chain_results
        if len(all_mixed) > 1:
            mixed_final = ctx.merge(*all_mixed, name="mixed_final")

        print("\n=== Test 7: Stress Test - Very Complex Graph ===")
        # Create an extremely complex graph to really test the algorithm

        # Multiple source types
        stress_sources = []
        source_types = ["sphere", "box", "torus", "circle", "grid"]
        for i, stype in enumerate(source_types):
            source = ctx.node(stype, f"stress_source_{stype}_{i}")
            stress_sources.append(source)

        # Create multiple processing layers with cross-connections
        layer1_nodes = []
        for i, source in enumerate(stress_sources):
            # Each source gets processed by 2 different operations
            proc1 = ctx.node("mountain", f"stress_l1_mountain_{i}", _input=source)
            proc2 = ctx.node("subdivide", f"stress_l1_subdivide_{i}", _input=source, iterations=1)
            layer1_nodes.extend([proc1, proc2])

        # Layer 2: Cross-connect some nodes (creates complex dependencies)
        layer2_nodes = []
        for i in range(0, len(layer1_nodes), 3):
            # Take groups of 3 nodes and merge them
            group = layer1_nodes[i:i+3]
            if len(group) >= 2:
                merge_node = ctx.merge(*group, name=f"stress_l2_merge_{i//3}")
                # Add processing after merge
                processed = ctx.node("smooth", f"stress_l2_smooth_{i//3}", _input=merge_node, strength=0.4)
                layer2_nodes.append(processed)

        # Layer 3: Final convergence
        if len(layer2_nodes) > 1:
            # Split layer2 into two groups and merge each
            mid = len(layer2_nodes) // 2
            group1 = layer2_nodes[:mid]
            group2 = layer2_nodes[mid:]

            final1 = None
            final2 = None

            if group1:
                merge1 = ctx.merge(*group1, name="stress_final_merge_1")
                final1 = ctx.node("normal", "stress_final_normal_1", _input=merge1)

            if group2:
                merge2 = ctx.merge(*group2, name="stress_final_merge_2")
                final2 = ctx.node("subdivide", "stress_final_subdivide_2", _input=merge2, iterations=1)

            # Ultimate final merge
            if final1 is not None and final2 is not None:
                ultimate_final = ctx.merge(final1, final2, name="stress_ultimate_final")

        print(f"\n=== Applying Layout Algorithm ===")
        print(f"Total nodes in context: {len(list(ctx._dependency_registry.keys()))}")

        # Apply the layout with custom spacing for better visualization
        ctx.apply_layout(
            layer_height=3.0,    # More vertical space between layers
            node_width=2.5,      # Assume wider nodes
            min_spacing=1.0      # More horizontal spacing
        )

        print("Layout applied successfully!")

        # Get some statistics about the layout
        positions = ctx.layout_nodes()
        if positions:
            x_positions = [pos[0] for pos in positions.values()]
            y_positions = [pos[1] for pos in positions.values()]

            print(f"\nLayout Statistics:")
            print(f"  X range: {min(x_positions):.2f} to {max(x_positions):.2f}")
            print(f"  Y range: {min(y_positions):.2f} to {max(y_positions):.2f}")
            print(f"  Total width: {max(x_positions) - min(x_positions):.2f}")
            print(f"  Total height: {max(y_positions) - min(y_positions):.2f}")

        # Get layer information
        all_nodes = list(ctx._dependency_registry.keys())
        layers = ctx._compute_layers(all_nodes)
        print(f"  Number of layers: {len(layers)}")
        print(f"  Nodes per layer: {[len(nodes) for nodes in layers.values()]}")

        return ctx

def main():
    """Main function for running the stress test."""
    print("Starting Layout Algorithm Stress Test Demo")
    print("=" * 50)

    try:
        ctx = create_layout_stress_test()

        print("\n" + "=" * 50)
        print("Stress test completed successfully!")
        print("\nTo examine the results:")
        print("1. Navigate to /obj/layout_test_geo in Houdini")
        print("2. Examine the node layout in the network editor")
        print("3. Check how complex patterns are handled")
        print("4. Hip file will be saved if --hipfile option was used")

        # Print some final analysis
        all_nodes = list(ctx._dependency_registry.keys())
        source_nodes = ctx.get_source_nodes()
        sink_nodes = ctx.get_sink_nodes()

        print(f"\nFinal Graph Analysis:")
        print(f"  Total nodes: {len(all_nodes)}")
        print(f"  Source nodes: {len(source_nodes)}")
        print(f"  Sink nodes: {len(sink_nodes)}")
        print(f"  Internal nodes: {len(all_nodes) - len(source_nodes) - len(sink_nodes)}")

        return True

    except Exception as e:
        print(f"Error during stress test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
