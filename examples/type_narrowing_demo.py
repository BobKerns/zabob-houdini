#!/usr/bin/env python3
"""
Example script demonstrating Zabob-Houdini type narrowing with as_type parameter.

This script shows how to use the as_type parameter in .create() to get
properly typed Houdini node objects for better type safety and IntelliSense.
"""

from zabob_houdini import node
import hou


def main():
    print("=== Zabob-Houdini Type Narrowing Examples ===\n")

    print("Note: This example demonstrates the API. To run with actual")
    print("node creation, execute within Houdini's Python environment.\n")

    # Example 1: Basic type narrowing
    print("1. Basic type narrowing:")
    geo_node = node("/obj", "geo", name="mygeometry")
    box_node = node(geo_node, "box", name="mybox",
                   sizex=2.0, sizey=2.0, sizez=2.0)

    print("   Without type narrowing:")
    print("   geo_instance = geo_node.create()           # Returns hou.Node")
    print("   box_instance = box_node.create()           # Returns hou.Node")
    print()

    print("   With type narrowing:")
    print("   # Get specifically-typed nodes for better IntelliSense")
    print("   geo_instance = geo_node.create(as_type=hou.ObjNode)  # Returns hou.ObjNode")
    print("   box_instance = box_node.create(as_type=hou.SopNode)  # Returns hou.SopNode")
    print()

    # Example 2: Benefits of type narrowing
    print("2. Benefits of type narrowing:")
    print("   With proper typing, you get:")
    print("   - Better IntelliSense in your IDE")
    print("   - Type checking catches errors at development time")
    print("   - Access to type-specific methods without casting")
    print()

    print("   Examples of type-specific methods:")
    print("   # SopNode-specific methods")
    print("   sop_node = box_node.create(as_type=hou.SopNode)")
    print("   # sop_node.geometry()        # Get output geometry")
    print("   # sop_node.inputGeometry(0)  # Get input geometry")
    print("   # sop_node.isDisplayFlagSet() # Check display flag")
    print()

    print("   # ObjNode-specific methods")
    print("   obj_node = geo_node.create(as_type=hou.ObjNode)")
    print("   # obj_node.worldTransform()   # Get world transform")
    print("   # obj_node.localTransform()   # Get local transform")
    print("   # obj_node.isSelectableFlagSet() # Check selectable flag")
    print()

    # Example 3: Error handling
    print("3. Error handling:")
    print("   If you specify an incorrect type, a TypeError is raised:")
    print("   try:")
    print("       # This would fail - box is a SOP, not an OBJ")
    print("       wrong_type = box_node.create(as_type=hou.ObjNode)")
    print("   except TypeError as e:")
    print("       print(f'Type error: {e}')")
    print()

    # Example 4: Common node types
    print("4. Common node types for as_type:")
    node_types = [
        ("hou.Node", "Base class for all nodes"),
        ("hou.ObjNode", "Object-level nodes (/obj/*)"),
        ("hou.SopNode", "Surface operators (geometry nodes)"),
        ("hou.ChopNode", "Channel operators (animation/audio)"),
        ("hou.RopNode", "Render operators (output drivers)"),
        ("hou.VopNode", "VEX operators (shaders)"),
        ("hou.LopNode", "Lighting operators (USD/Solaris)"),
        ("hou.TopNode", "Task operators (PDG/TOPs)"),
    ]

    for node_type, description in node_types:
        print(f"   {node_type:<12} - {description}")
    print()

    # Example 5: Using with chains
    print("5. Type narrowing with chains:")
    print("   # Chains return tuples of NodeInstance objects")
    print("   from zabob_houdini import chain")
    print("   processing_chain = chain(geo_node,")
    print("                           box_node,")
    print("                           node(geo_node, 'xform', name='transform'),")
    print("                           node(geo_node, 'subdivide', name='refine'))")
    print()
    print("   # Create the chain and get typed nodes")
    print("   chain_instances = processing_chain.create()")
    print("   for instance in chain_instances:")
    print("       typed_node = instance.create(as_type=hou.SopNode)")
    print("       # Now typed_node has full SopNode IntelliSense")
    print()

    print("6. Best practices:")
    print("   - Use as_type when you need type-specific functionality")
    print("   - Default hou.Node is fine for basic operations")
    print("   - Type narrowing helps catch errors during development")
    print("   - Your IDE will provide better autocomplete with specific types")
    print("   - Consider using typed variables for clarity:")
    print("     sop_node: hou.SopNode = my_node.create(as_type=hou.SopNode)")


if __name__ == "__main__":
    main()
