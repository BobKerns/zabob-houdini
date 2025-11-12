#!/usr/bin/env python3
"""
Diamond Chain Connection Demo

This example demonstrates creating a diamond/fork-and-merge pattern with chains:
- Chain A feeds into both B2 and B3
- Both B2 and B3 feed into Chain C
- Final topology: A → B2 → C
                   A → B3 → C

This is a common pattern in procedural workflows where you want to:
1. Create base geometry (Chain A)
2. Process it in two different ways (Chains B2 and B3)
3. Merge the results (Chain C)
"""

from zabob_houdini import chain, node

def create_diamond_chains():
    """Create a diamond pattern of connected chains."""

    # Chain A: Create base geometry
    chain_A = chain(
        node("/obj", "geo", "base_geometry"),
        node("/obj/base_geometry", "box", "source_box", sizex=2, sizey=2, sizez=2),
        node("/obj/base_geometry", "xform", "center", tx=0, ty=0, tz=0),
        name_prefix="base_"
    )

    # Chain B2: First processing path (e.g., scale and rotate)
    chain_B2 = chain(
        node("/obj", "geo", "process_branch2"),
        node("/obj/process_branch2", "xform", "scale_up", sx=1.5, sy=1.5, sz=1.5),
        node("/obj/process_branch2", "xform", "rotate_y", ry=45),
        _input=chain_A,  # Connect A → B2
        name_prefix="branch2_"
    )

    # Chain B3: Second processing path (e.g., different scale and rotation)
    chain_B3 = chain(
        node("/obj", "geo", "process_branch3"),
        node("/obj/process_branch3", "xform", "scale_down", sx=0.8, sy=0.8, sz=0.8),
        node("/obj/process_branch3", "xform", "rotate_x", rx=30),
        _input=chain_A,  # Connect A → B3
        name_prefix="branch3_"
    )

    # Chain C: Merge both processing paths
    chain_C = chain(
        node("/obj", "geo", "merged_result"),
        node("/obj/merged_result", "merge", "combine_branches", _input=[chain_B2, chain_B3]),
        node("/obj/merged_result", "xform", "final_position", ty=2),
        name_prefix="final_"
    )

    return {
        'A': chain_A,
        'B2': chain_B2,
        'B3': chain_B3,
        'C': chain_C
    }


def create_and_demonstrate():
    """Create the chains and demonstrate the connections."""

    print("Creating diamond chain pattern...")
    chains = create_diamond_chains()

    # Create all chains in Houdini
    print("\nCreating Chain A (base geometry)...")
    created_A = chains['A'].create()
    print(f"Chain A created with {len(created_A)} nodes")

    print("\nCreating Chain B2 (first processing path)...")
    created_B2 = chains['B2'].create()
    print(f"Chain B2 created with {len(created_B2)} nodes")

    print("\nCreating Chain B3 (second processing path)...")
    created_B3 = chains['B3'].create()
    print(f"Chain B3 created with {len(created_B3)} nodes")

    print("\nCreating Chain C (merged result)...")
    created_C = chains['C'].create()
    print(f"Chain C created with {len(created_C)} nodes")

    # Display the connection topology
    print("\n" + "="*50)
    print("CONNECTION TOPOLOGY:")
    print("="*50)
    print("Chain A (base_geometry)")
    print("├── Chain B2 (process_branch2) → Chain C (merged_result)")
    print("└── Chain B3 (process_branch3) → Chain C (merged_result)")
    print("\nFinal result: A → B2 → C")
    print("              A → B3 → C")

    # Show node paths for verification
    print("\n" + "="*50)
    print("CREATED NODE PATHS:")
    print("="*50)

    print("Chain A nodes:")
    for i, node_instance in enumerate(created_A):
        print(f"  {i+1}. {node_instance.path}")

    print("\nChain B2 nodes:")
    for i, node_instance in enumerate(created_B2):
        print(f"  {i+1}. {node_instance.path}")

    print("\nChain B3 nodes:")
    for i, node_instance in enumerate(created_B3):
        print(f"  {i+1}. {node_instance.path}")

    print("\nChain C nodes:")
    for i, node_instance in enumerate(created_C):
        print(f"  {i+1}. {node_instance.path}")

    return chains


def advanced_diamond_example():
    """More complex diamond pattern with multiple merge points."""

    print("\n" + "="*60)
    print("ADVANCED DIAMOND PATTERN")
    print("="*60)

    # Base chain
    base = chain(
        node("/obj", "geo", "advanced_base"),
        node("/obj/advanced_base", "sphere", "source_sphere", radx=1),
        name_prefix="adv_base_"
    )

    # Multiple processing branches
    branch_A = chain(
        node("/obj", "geo", "branch_a"),
        node("/obj/branch_a", "mountain", "noise_a", height=0.5),
        node("/obj/branch_a", "xform", "move_a", tx=-2),
        _input=base,
        name_prefix="branch_a_"
    )

    branch_B = chain(
        node("/obj", "geo", "branch_b"),
        node("/obj/branch_b", "twist", "twist_b", strength=90),
        node("/obj/branch_b", "xform", "move_b", tx=2),
        _input=base,
        name_prefix="branch_b_"
    )

    branch_C = chain(
        node("/obj", "geo", "branch_c"),
        node("/obj/branch_c", "bend", "bend_c", bend=45),
        node("/obj/branch_c", "xform", "move_c", tz=2),
        _input=base,
        name_prefix="branch_c_"
    )

    # First merge point: combine A and B
    merge_AB = chain(
        node("/obj", "geo", "merge_ab"),
        node("/obj/merge_ab", "merge", "combine_ab", _input=[branch_A, branch_B]),
        name_prefix="merge_ab_"
    )

    # Final merge: combine AB with C
    final_result = chain(
        node("/obj", "geo", "final_advanced"),
        node("/obj/final_advanced", "merge", "final_merge", _input=[merge_AB, branch_C]),
        node("/obj/final_advanced", "xform", "final_scale", sx=0.8, sy=0.8, sz=0.8),
        name_prefix="final_adv_"
    )

    # Create all chains
    print("Creating advanced diamond pattern...")
    base.create()
    branch_A.create()
    branch_B.create()
    branch_C.create()
    merge_AB.create()
    final_result.create()

    print("Advanced diamond pattern created!")
    print("Topology: base → branch_A → merge_AB → final_result")
    print("          base → branch_B → merge_AB → final_result")
    print("          base → branch_C → final_result")


if __name__ == "__main__":
    import hou

    # Basic diamond pattern
    chains = create_and_demonstrate()

    # Advanced diamond pattern
    advanced_diamond_example()

    # Save the scene to preserve the created nodes
    scene_path = "/tmp/diamond_chain_demo.hip"
    hou.hipFile.save(scene_path)

    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("Check your Houdini scene for the created node networks.")
    print("You should see the diamond connection patterns in the Network Editor.")
    print(f"Scene saved to: {scene_path}")

    # Also display current scene contents
    print("\nCurrent scene contents:")
    obj = hou.node('/obj')
    for child in obj.children():
        print(f"  - {child.path()} ({child.type().name()})")
        if child.type().name() == 'geo':
            for grandchild in child.children():
                print(f"    └─ {grandchild.name()} ({grandchild.type().name()})")
