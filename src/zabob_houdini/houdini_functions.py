"""
Houdini-specific functions that require the hou module.

This module contains functions that can only run within Houdini's Python environment.
These functions are called by the hython bridge for external access.

## Usage Guidelines

All functions in this module should use one of two decorators:

### @houdini_result
Use for functions that return structured data (JsonObject):
```python
@houdini_result
def my_function() -> JsonObject:
    return {
        'node_count': 5,
        'paths': ['/obj/geo1', '/obj/geo2'],
        'success': True
    }
```

### @houdini_message
Use for functions that return simple string messages:
```python
@houdini_message
def my_function() -> str:
    return "Operation completed successfully"
```

The decorators handle:
- Exception catching and error reporting
- Consistent return structure for bridge communication
- JSON serialization compatibility
"""

import hou
from zabob_houdini.core import node, chain, hou_node
from zabob_houdini.houdini_bridge import houdini_message, houdini_result, JsonObject


@houdini_message
def simple_houdini_test() -> str:
    """Simple test that creates a box node."""
    # Get or create geometry node
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "test_geo")

    # Create a box
    box = geo.createNode("box", "test_box")

    return f"Created box at: {box.path()}"


@houdini_result
def chain_creation_test() -> JsonObject:
    """Test creating a chain using Zabob API in hython."""
    # Get or create geometry node
    obj = hou_node("/obj")
    geo = obj.createNode("geo", "chain_test_geo")

    # Create chain using Zabob API
    box_node = node(geo.path(), "box", name="source")
    xform_node = node(geo.path(), "xform", name="transform")
    subdivide_node = node(geo.path(), "subdivide", name="refine")

    processing_chain = chain(geo.path(), box_node, xform_node, subdivide_node)

    # Create the chain
    created_nodes = processing_chain.create()

    return {
        "message": f"Created chain with {len(created_nodes)} nodes in {geo.path()}",
        "node_count": len(created_nodes),
        "parent_path": geo.path()
    }


@houdini_message
def create_test_chain() -> str:
    """Create a test processing chain for CLI testing."""
    # Ensure we have a geometry node
    geo = hou.node("/obj/geo1")
    if not geo:
        geo = hou_node("/obj").createNode("geo", "geo1")

    # Create chain using Zabob API
    box_node = node(geo.path(), "box", name="source")
    xform_node = node(geo.path(), "xform", name="transform")
    subdivide_node = node(geo.path(), "subdivide", name="refine")

    processing_chain = chain(geo.path(), box_node, xform_node, subdivide_node)

    # Create the chain
    result = processing_chain.create()
    return f"Chain created successfully: {len(result)} nodes"


@houdini_result
def get_houdini_info() -> JsonObject:
    """Get Houdini environment information."""
    try:
        return {
            'houdini_app': hou.applicationName(),
            'houdini_version': '.'.join(map(str, hou.applicationVersion())),
            'houdini_build': hou.applicationVersionString(),
        }
    except Exception as e:
        return {'houdini_error': str(e)}
