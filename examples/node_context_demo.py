"""
Example demonstrating ZContext usage.

This shows how to use the zcontext() function and ZContext class to organize
node creation under a specific parent.
"""

from zabob_houdini import znode, zcontext


def demo_node_context():
    """Demonstrate zcontext() function usage patterns."""

    # Create a geometry container
    geo = znode("/obj", "geo", "geometry1")

    # Method 1: Use zcontext() function with context manager for node creation
    with zcontext(geo) as ctx:
        print(f"Created context with parent: {ctx.parent.path}")

        # Create nodes using the context's znode() method
        box = ctx.znode("box", "input_box")
        transform = ctx.znode("xform", "transform1")

        print(f"Box created via ctx.znode(): {box.parent.path}")
        print(f"Transform created via ctx.znode(): {transform.parent.path}")

        # Look up nodes by name
        retrieved_box = ctx["input_box"]
        retrieved_transform = ctx["transform1"]

        print(f"Retrieved box is same instance: {retrieved_box is box}")
        print(f"Retrieved transform is same instance: {retrieved_transform is transform}")

    # Advanced usage with the same context
        # Create nodes using both methods
        sphere = ctx.znode("sphere", "my_sphere")  # Using ctx.znode()
        merge = znode(ctx.parent, "merge", "my_merge")  # Using global znode()

        print(f"Sphere parent: {sphere.parent.path}")
        print(f"Merge parent: {merge.parent.path}")

        # Named node lookup
        retrieved_sphere = ctx["my_sphere"]
        print(f"Can lookup sphere by name: {retrieved_sphere is sphere}")

        # All should have the same parent
        assert sphere.parent == geo
        assert merge.parent == geo

    # Method 2: Context with string path
    with zcontext("/obj") as obj_ctx:
        # Create geometry nodes under /obj using ctx.znode()
        geo1 = obj_ctx.znode("geo", "geo1")
        geo2 = obj_ctx.znode("geo", "geo2")

        print(f"Geo1 parent: {geo1.parent.path}")
        print(f"Geo2 parent: {geo2.parent.path}")

        # Lookup by name
        print(f"Can lookup geo1: {obj_ctx['geo1'] is geo1}")
        print(f"Can lookup geo2: {obj_ctx['geo2'] is geo2}")


if __name__ == "__main__":
    demo_node_context()
