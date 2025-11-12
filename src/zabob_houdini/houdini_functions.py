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

import os
import sys
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

    processing_chain = chain(box_node, xform_node, subdivide_node)

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

    processing_chain = chain(box_node, xform_node, subdivide_node)

    # Create the chain
    result = processing_chain.create()
    return f"Chain created successfully: {len(result)} nodes"


@houdini_result
def get_houdini_info() -> JsonObject:
    """Get Houdini environment information."""
    try:
        return {
            'houdini_app': hou.applicationName(),
            'houdini_version': list(hou.applicationVersion()),
            'houdini_build': hou.applicationVersionString(),
            "hython_version": sys.version,
            "houdini_environment": dict(os.environ),
        }
    except Exception as e:
        return {'houdini_error': str(e)}


def run(script_path: str, script_args: tuple[str, ...], hipfile: str | None, verbose: bool) -> None:
    """
    Run a Python script in hython and optionally save the resulting hip file.

    This is the actual implementation that gets called by the @houdini_command decorator.
    """
    import click

    script_path_abs = os.path.abspath(script_path)

    if verbose:
        click.echo(f"Running script: {script_path_abs}")
        if script_args:
            click.echo(f"Script arguments: {' '.join(script_args)}")
        if hipfile:
            click.echo(f"Will save scene to: {hipfile}")

    try:
        # Add script directory to Python path so imports work
        script_dir = os.path.dirname(script_path_abs)
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        # Store original sys.argv to restore later
        original_argv = sys.argv.copy()

        try:
            # Set up sys.argv as if the script was called directly
            sys.argv = [script_path_abs] + list(script_args)

            # Read and execute the script
            with open(script_path_abs, 'r') as script_file:
                script_code = script_file.read()

            # Execute in global namespace so imports and variables persist
            exec(script_code, {'__name__': '__main__', '__file__': script_path_abs})

            click.echo(f"✓ Script executed successfully: {os.path.basename(script_path_abs)}")

            # Save hip file if requested
            if hipfile:
                # Ensure directory exists
                os.makedirs(os.path.dirname(hipfile), exist_ok=True)
                hou.hipFile.save(hipfile)
                click.echo(f"✓ Scene saved to: {hipfile}")

        finally:
            # Restore original sys.argv
            sys.argv = original_argv

    except Exception as e:
        import traceback
        click.echo(f"✗ Error executing script: {e}")
        if verbose:
            traceback.print_exc()
        sys.exit(1)






