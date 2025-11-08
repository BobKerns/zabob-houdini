"""
Test file to demonstrate enhanced Houdini type stubs.
This shows the improved type checking and IntelliSense capabilities.
"""
from zabob_houdini import node

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

    return merge

if __name__ == "__main__":
    # This won't actually run without Houdini, but demonstrates the API
    print("Enhanced stubs provide better type checking!")
    print("Try opening this file in VS Code to see improved IntelliSense.")
