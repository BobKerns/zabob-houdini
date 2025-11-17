#!/usr/bin/env python3

from zabob_houdini import node, context

# Test the new ChainBuilder API
print("🧪 Testing ChainBuilder API")

with context(node("/obj", "geo", "chainbuilder_test")) as ctx:
    print("📦 Creating source...")
    source = ctx.node("box", "source")

    print("🔗 Building chain with ChainBuilder...")
    with ctx.chain(_input=source) as chain_builder:
        transform = chain_builder.node("xform", "transform")
        subdivide = chain_builder.node("subdivide", "subdivide")

        print(f"  Chain has {len(chain_builder)} nodes")
        print(f"  First: {chain_builder.first.name}")
        print(f"  Last: {chain_builder.last.name}")
        print(f"  Can access [0]: {chain_builder[0].name}")
        print(f"  Can access [1]: {chain_builder[1].name}")

    print(f"✅ Chain created with {len(ctx._dependency_registry)} total nodes in context")

print("🎯 Context will auto-create nodes on exit...")
