#!/usr/bin/env python3

from zabob_houdini import node, context

# Test simple chain creation
print("Testing simple chain creation...")

with context(node("/obj", "geo", "simple_test")) as ctx:
    source = ctx.node("box", "source")
    print(f"Created source: {source.name}")

    # Simple single-node chain
    path = ctx.chain(ctx.node("xform", "path"))
    print(f"Created chain with nodes: {[n.name for n in path.nodes]}")

print("Simple test completed!")
