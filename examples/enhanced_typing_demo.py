"""
Test file to demonstrate enhanced Houdini type stubs.
This shows the improved type checking and IntelliSense capabilities.
"""
from zabob_houdini import node
import hou

# This should now have excellent IntelliSense with the enhanced stubs
def demo_enhanced_typing():
    """Demonstrate the enhanced typing capabilities."""

    # Create nodes with type-safe parameter setting
    box = node("/obj/geo1", "box", name="my_box",
               sizex=2.0, sizey=2.0, sizez=2.0)

    sphere = node("/obj/geo1", "sphere", name="my_sphere",
                  radx=1.5, rady=1.5, radz=1.5)

    # Connect with sparse inputs (enhanced support)
    merge = node("/obj/geo1", "merge", name="result",
                 _input=[box, None, sphere])  # Skip input 1

    # The enhanced stubs should provide IntelliSense for:
    # - box.create() returns Node with proper methods
    # - Parameter names and types are clear
    # - Optional return types are properly handled
    # - Exception patterns are documented

    # NEW: Type narrowing with as_type parameter
    # Get specifically-typed nodes for better IntelliSense
    box_sop = box.create(as_type=hou.SopNode)      # Returns hou.SopNode
    sphere_sop = sphere.create(as_type=hou.SopNode) # Returns hou.SopNode
    merge_sop = merge.create(as_type=hou.SopNode)   # Returns hou.SopNode

    # Now you have access to SOP-specific methods with full type safety:
    # box_sop.geometry()        # Get output geometry
    # box_sop.inputGeometry(0)  # Get input geometry
    # box_sop.isDisplayFlagSet() # Check display flag
    # etc.

    return merge

if __name__ == "__main__":
    # This won't actually run without Houdini, but demonstrates the API
    print("Enhanced stubs provide better type checking!")
    print("Try opening this file in VS Code to see improved IntelliSense.")
