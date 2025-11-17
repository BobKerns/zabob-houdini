#!/usr/bin/env python3

from zabob_houdini import node, context

# Test automatic layout and sink node creation on context exit
print("Testing automatic context exit behavior...")

with context(node("/obj", "geo", "auto_test_geo")) as ctx:
    source = ctx.node("box", "source")
    print(f"Source: {source.name}, inputs: {len(source.inputs)}")

    with ctx.chain(_input=source) as path_a:
        path_a.node("xform", "path_a")

    with ctx.chain(_input=source) as path_b:
        path_b.node("xform", "path_b")

    print(f"Path A last: {path_a.last.name}")
    print(f"Path B last: {path_b.last.name}")

    final = ctx.merge(path_a, path_b, name="final")
    print(f"Final: {final.name}, inputs: {len(final.inputs)}")

    print(f"Created {len(ctx._dependency_registry)} nodes in context")

    print(f"Created {len(ctx._dependency_registry)} nodes in context")

print("Context will now auto-apply layout and create sink nodes on exit...")
# Context __exit__ will automatically handle layout and node creation
