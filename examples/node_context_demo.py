"""
Example demonstrating NodeContext usage.

This shows how to use the context() function and NodeContext class to organize
node creation under a specific parent.
"""

from zabob_houdini import node, context

def demo_node_context():
    """Demonstrate context() function usage patterns."""

    # Create a geometry container
    geo = node("/obj", "geo", "geometry1")

    # Method 1: Use context() function with context manager for node creation
    with context(geo) as ctx:
        print(f"Created context with parent: {ctx.parent.path}")

        # Create nodes using the context's node() method
        box = ctx.node("box", "input_box")
        transform = ctx.node("xform", "transform1")

        print(f"Box created via ctx.node(): {box.parent.path}")
        print(f"Transform created via ctx.node(): {transform.parent.path}")

        # Look up nodes by name
        retrieved_box = ctx["input_box"]
        retrieved_transform = ctx["transform1"]

        print(f"Retrieved box is same instance: {retrieved_box is box}")
        print(f"Retrieved transform is same instance: {retrieved_transform is transform}")

    # Advanced usage with the same context
        # Create nodes using both methods
        sphere = ctx.node("sphere", "my_sphere")  # Using ctx.node()
        merge = node(ctx.parent, "merge", "my_merge")  # Using global node()

        print(f"Sphere parent: {sphere.parent.path}")
        print(f"Merge parent: {merge.parent.path}")

        # Named node lookup
        retrieved_sphere = ctx["my_sphere"]
        print(f"Can lookup sphere by name: {retrieved_sphere is sphere}")

        # All should have the same parent
        assert sphere.parent == geo
        assert merge.parent == geo

    # Method 2: Context with string path
    with context("/obj") as obj_ctx:
        # Create geometry nodes under /obj using ctx.node()
        geo1 = obj_ctx.node("geo", "geo1")
        geo2 = obj_ctx.node("geo", "geo2")

        print(f"Geo1 parent: {geo1.parent.path}")
        print(f"Geo2 parent: {geo2.parent.path}")

        # Lookup by name
        print(f"Can lookup geo1: {obj_ctx['geo1'] is geo1}")
        print(f"Can lookup geo2: {obj_ctx['geo2'] is geo2}")

if __name__ == "__main__":
    demo_node_context()
