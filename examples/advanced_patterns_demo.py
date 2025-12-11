#!/usr/bin/env python3
"""
Advanced Zabob-Houdini Patterns

This example demonstrates advanced usage patterns combining multiple
new features for complex node graph construction.

Key Features Demonstrated:
- Nested ZChainBuilder contexts for complex branching
- Dynamic chain construction based on configuration
- Automatic dependency tracking across complex networks
- Integration of both manual chains and ZChainBuilder patterns
- Advanced merge operations with mixed input types

NOTE: This example is currently flawed by accessing the ZChainBuilder.last
property before the chain is fully built, which may lead to unexpected behavior.
This is a known issue and will be addressed in future updates, probably by
returning a forward reference.

"""

from zabob_houdini import znode, zcontext


def create_processing_network(config: dict):
    """
    Create a complex processing network based on configuration.

    Args:
        config: Dictionary with processing options
    """
    print(f"🏗️  Building network with config: {config}")

    with zcontext(znode("/obj", "geo", "advanced_demo")) as ctx:
        # Create multiple source geometries
        print("📦 Creating source geometries...")
        sources = []
        for i, geom_type in enumerate(config.get('sources', ['box'])):
            source = ctx.node(geom_type, f"source_{i}",
                              sizex=1 + i * 0.5 if geom_type == 'box' else None,
                              radius=0.8 + i * 0.2 if geom_type == 'sphere' else None)
            sources.append(source)

        # Create processing pipelines for each source
        processed_chains = []

        for i, source in enumerate(sources):
            print(f"🔄 Building processing pipeline {i + 1}...")

            with ctx.chain(_input=source) as pipeline:
                # Base transformation
                pipeline.node("xform", f"base_transform_{i}",
                              tx=i * 3, ry=i * 30)

                # Conditional processing based on config
                processing_steps = config.get('processing', {})

                if processing_steps.get('subdivision', False):
                    print(f"  ➕ Adding subdivision to pipeline {i + 1}")
                    pipeline.node("subdivide", f"subdivide_{i}",
                                  iterations=processing_steps.get('subdivision_levels', 1))

                if processing_steps.get('deformation', False):
                    print(f"  ➕ Adding deformation to pipeline {i + 1}")
                    deform_type = processing_steps.get('deformation_type', 'noise')

                    if deform_type == 'noise':
                        pipeline.node("mountain", f"noise_{i}",
                                      amp=0.1, freq=4)
                    elif deform_type == 'twist':
                        pipeline.node("twist", f"twist_{i}",
                                      strength=45, period=1)

                if processing_steps.get('coloring', False):
                    print(f"  🎨 Adding coloring to pipeline {i + 1}")
                    color = processing_steps.get('colors', [(1, 0, 0), (0, 1, 0), (0, 0, 1)])[i % 3]
                    pipeline.node("color", f"color_{i}", color=color)

                # Advanced: Nested branching within pipeline
                if processing_steps.get('branching', False):
                    print(f"  🌳 Adding branch processing to pipeline {i + 1}")

                    # Create a branch for additional processing
                    with ctx.chain(_input=pipeline.last) as branch:
                        branch.node("blast", f"branch_blast_{i}", group=f"{i}")
                        branch.node("extrude", f"branch_extrude_{i}", dist=0.3)

                    # Merge the branch back with the main pipeline
                    merged = ctx.merge(pipeline.last, branch, name=f"branch_merge_{i}")

                    # Continue the main pipeline from the merge
                    with ctx.chain(_input=merged) as continuation:
                        continuation.node("smooth", f"smooth_{i}")
                    # Replace the pipeline reference with the continuation
                    processed_chains.append(continuation)
                else:
                    processed_chains.append(pipeline)

        # Create output processing
        print("🔀 Creating output processing...")

        if len(processed_chains) > 1:
            # Multiple chains - merge them
            if config.get('merge_strategy') == 'sequential':
                print("  📦 Using sequential merge strategy")
                current = processed_chains[0]
                for i, chain_obj in enumerate(processed_chains[1:], 1):
                    current = ctx.merge(current, chain_obj, name=f"merge_step_{i}")
                final_input = current
            else:
                print("  📦 Using single merge strategy")
                final_input = ctx.merge(*processed_chains, name="final_merge")
        else:
            final_input = processed_chains[0]

        # Final output processing
        output_config = config.get('output', {})
        if output_config.get('post_processing', False):
            print("🎯 Adding post-processing...")

            with ctx.chain(_input=final_input) as post_process:
                if output_config.get('final_transform', False):
                    post_process.node("xform", "final_transform",
                                      ty=2, scale=1.2)

                if output_config.get('final_material', False):
                    post_process.node("material", "final_material")

                # Always add output node
                post_process.node("null", "OUTPUT")

            # final_output is available for use later.
            final_output = post_process.chain.last
        else:
            # Simple output node

            # final_output is available for use later.
            final_output = ctx.node("null", "OUTPUT", _input=final_input)

        print(f'Final output: {final_output.path}')
        print(f"📊 Network Statistics:")
        print(f"  Total nodes: {len(ctx._dependency_registry)}")
        print(f"  Source nodes: {len(sources)}")
        print(f"  Processing chains: {len(processed_chains)}")

        print("\n🎯 Context will auto-create all nodes with optimal layout...")

    print("✅ Advanced network creation completed!")


def main():
    """Run various configuration examples."""
    print("🚀 Advanced Zabob-Houdini Patterns Demo")
    print("=" * 50)

    # Example 1: Basic processing
    config1 = {
        'sources': ['box', 'sphere'],
        'processing': {
            'subdivision': True,
            'subdivision_levels': 2,
            'coloring': True,
            'colors': [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        },
        'output': {
            'post_processing': True,
            'final_transform': True
        }
    }

    print("\n📋 Example 1: Basic processing with subdivision and coloring")
    create_processing_network(config1)

    # Example 2: Complex branching
    config2 = {
        'sources': ['box'],
        'processing': {
            'deformation': True,
            'deformation_type': 'twist',
            'branching': True,
            'coloring': True
        },
        'merge_strategy': 'sequential',
        'output': {
            'post_processing': True,
            'final_material': True
        }
    }

    print("\n📋 Example 2: Complex branching with deformation")
    create_processing_network(config2)


if __name__ == "__main__":
    main()
