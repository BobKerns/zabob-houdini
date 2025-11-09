#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click>=8.0.0",
#     "typing-extensions>=4.0.0",
# ]
# ///
"""
Zabob-Houdini CLI - Simple utilities for development and testing.

Note: hython has severe virtual environment compatibility issues due to
linked symbol requirements. This CLI is designed for development and testing
with regular Python. For actual Houdini node creation, use the package
within Houdini's Python shelf tools or HDA scripts.
"""

import click
import os
import sys
from typing import Optional

def _check_houdini_available() -> bool:
    """Check if Houdini is available."""
    try:
        import hou
        return True
    except ImportError:
        return False


def get_environment_info() -> dict[str, str]:
    """Get information about the current Python and Houdini environment."""
    info = {
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'python_executable': sys.executable or 'unknown',
        'platform': sys.platform,
        'houdini_available': str(_check_houdini_available()),
    }

    # Add Houdini-specific info if available
    if _check_houdini_available():
        try:
            from zabob_houdini.houdini_bridge import call_houdini_function
            houdini_info = call_houdini_function('get_houdini_info')
            if isinstance(houdini_info, dict):
                info.update(houdini_info)
        except Exception as e:
            info['houdini_error'] = str(e)

    return info


@click.group()
@click.version_option(version="0.1.0", prog_name="zabob-houdini")
def main() -> None:
    """
    Zabob-Houdini development utilities.

    Simple CLI for validating Houdini integration and listing node types.
    """
    pass


@main.command()
@click.option(
    "--category", "-c",
    type=click.Choice(["sop", "obj", "dop", "cop", "vop", "top"], case_sensitive=False),
    help="Filter by node category"
)
def list_types(category: Optional[str]) -> None:
    """
    List available Houdini node types.
    """
    try:
        # TODO: Import your existing node enumeration code here
        if category:
            click.echo(f"Available {category.upper()} node types:")
            # TODO: Call your enumeration function with category filter
            click.echo("Node type enumeration not yet implemented")
        else:
            click.echo("Available node types:")
            # TODO: Call your enumeration function for all types
            click.echo("Node type enumeration not yet implemented")

    except ImportError:
        click.echo("✗ Cannot access Houdini module. Check your environment setup.")
    except Exception as e:
        click.echo(f"✗ Error listing node types: {e}")


@main.command()
def test_node() -> None:
    """
    Test creating a simple node (requires Houdini).
    """
    if not _check_houdini_available():
        click.echo("ℹ  Running in development mode")
        click.echo("  For actual node creation, use zabob-houdini within Houdini:")
        click.echo("  - Python shelf tools")
        click.echo("  - HDA script sections")
        click.echo("  - Houdini's built-in Python shell")
        click.echo()

    try:
        from zabob_houdini.core import node
        click.echo("Testing node creation...")

        # Test node definition (should work without Houdini)
        test_node = node("/obj", "geo", name="test_geometry")
        click.echo("✓ Node definition created successfully")
        click.echo(f"  Parent: {test_node.parent}")
        click.echo(f"  Type: {test_node.node_type}")
        click.echo(f"  Name: {test_node.name}")

        # Test actual creation (requires Houdini)
        if _check_houdini_available():
            click.echo("Testing node creation in Houdini...")
            result = test_node.create()
            click.echo("✓ Node created successfully in Houdini")
            click.echo(f"  Created node: {result.path()}")
        else:
            click.echo("⚠  Skipping Houdini node creation (Houdini not available)")
            click.echo("  Node definition is valid and ready for .create() call")

    except ImportError as e:
        if "hou" in str(e):
            click.echo("ℹ  Cannot import Houdini module (expected in development mode)")
            click.echo("  Use zabob-houdini within Houdini's Python environment for node creation")
        elif "core" in str(e):
            click.echo("✗ Cannot import zabob_houdini.core module")
            click.echo("  The core API module may not be implemented yet")
        else:
            click.echo(f"✗ Import error: {e}")
    except Exception as e:
        click.echo(f"✗ Test failed: {e}")


@main.command()
@click.option('--use-hython', is_flag=True, help='Actually create nodes in hython')
def test_chain(use_hython):
    """Test chain functionality."""
    from zabob_houdini.core import node, chain

    if not use_hython:
        click.echo("ℹ  Running in development mode")
        click.echo("  For actual chain creation, use --use-hython flag")

    click.echo("\nTesting chain functionality...")

    try:
        # Create individual nodes
        box_node = node("/obj/geo1", "box", name="source")
        xform_node = node("/obj/geo1", "xform", name="transform")
        subdivide_node = node("/obj/geo1", "subdivide", name="refine")

        # Create chain
        processing_chain = chain("/obj/geo1", box_node, xform_node, subdivide_node)

        # Verify chain properties
        click.echo("✓ Chain definition created successfully")
        click.echo(f"  Chain length: {len(processing_chain)}")

        # Test indexing
        click.echo("✓ Chain indexing:")
        click.echo(f"  First node: {processing_chain[0].name}")
        click.echo(f"  Last node: {processing_chain[-1].name}")
        click.echo(f"  Node by name 'transform': {processing_chain['transform'].name}")

        # Test slicing
        subset = processing_chain[1:3]
        click.echo(f"  Slice [1:3] has {len(subset)} nodes")

        # Test splicing
        detail_chain = chain("/obj/geo1",
                           node("/obj/geo1", "normal", name="normals"),
                           processing_chain,  # This should be spliced in
                           node("/obj/geo1", "output", name="output"))
        click.echo(f"✓ Chain splicing: master chain has {len(detail_chain)} nodes")

        # Try to create chain
        if use_hython:
            try:
                click.echo("✓ Creating chain in hython...")

                from zabob_houdini.houdini_bridge import call_houdini_function
                result = call_houdini_function("create_test_chain")
                click.echo(f"  {result}")

            except Exception as e:
                click.echo(f"⚠  Failed to create chain in hython: {e}")
        elif _check_houdini_available():
            try:
                click.echo("✓ Creating chain in current Houdini session...")
                created_chain = processing_chain.create()
                click.echo(f"  Chain created successfully: {len(created_chain)} nodes")
            except Exception as e:
                click.echo(f"⚠  Failed to create chain: {e}")
        else:
            click.echo("⚠  Skipping Houdini chain creation (use --use-hython to try hython)")
            click.echo("  Chain definition is valid and ready for .create() call")

    except Exception as e:
        click.echo(f"✗ Chain test failed: {e}")


@main.command()
def install_package():
    """Install zabob-houdini as a Houdini package."""
    from zabob_houdini.package_installer import install_houdini_package

    click.echo("Installing zabob-houdini as Houdini package...")

    if install_houdini_package():
        click.echo("✓ Installation successful!")
        click.echo("  Package is now available in Houdini Python nodes and shelf tools")
    else:
        click.echo("✗ Installation failed")
        click.echo("  Check that Houdini is installed and you have write permissions")


@main.command()
def uninstall_package():
    """Remove zabob-houdini Houdini package."""
    from zabob_houdini.package_installer import uninstall_houdini_package

    click.echo("Removing zabob-houdini Houdini package...")

    if uninstall_houdini_package():
        click.echo("✓ Package removed successfully")
    else:
        click.echo("ℹ  No package found to remove")


@main.command()
def info() -> None:
    """
    Display Python and Houdini environment information.
    """
    click.echo("Environment Information:")
    click.echo("=" * 50)

    env_info = get_environment_info()

    # Python info
    click.echo(f"Python Version: {env_info['python_version']}")
    click.echo(f"Python Executable: {env_info['python_executable']}")
    click.echo(f"Platform: {env_info['platform']}")
    click.echo(f"Houdini Available: {env_info['houdini_available']}")

    # Houdini info if available
    if _check_houdini_available():
        click.echo("\nHoudini Information:")
        click.echo("-" * 30)
        if 'houdini_app' in env_info:
            click.echo(f"Application: {env_info['houdini_app']}")
            click.echo(f"Version: {env_info['houdini_version']}")
            click.echo(f"Build: {env_info['houdini_build']}")
        if 'houdini_error' in env_info:
            click.echo(f"Error: {env_info['houdini_error']}")

    # Environment variables
    click.echo("\nEnvironment Variables:")
    click.echo("-" * 30)
    houdini_path = os.getenv("HOUDINI_PATH")
    if houdini_path:
        click.echo(f"HOUDINI_PATH: {houdini_path}")
    else:
        click.echo("HOUDINI_PATH: Not set")

    pythonpath = os.getenv("PYTHONPATH")
    if pythonpath:
        click.echo(f"PYTHONPATH: {pythonpath}")
    else:
        click.echo("PYTHONPATH: Not set")


@main.command()
def validate() -> None:
    """
    Validate Houdini installation and Python environment.
    """
    click.echo("Validating Houdini integration...")

    if _check_houdini_available():
        click.echo("✓ Houdini module available")
        try:
            from zabob_houdini.houdini_bridge import call_houdini_function
            houdini_info = call_houdini_function('get_houdini_info')
            if isinstance(houdini_info, dict) and 'houdini_app' in houdini_info:
                click.echo(f"  Application: {houdini_info['houdini_app']}")
                click.echo(f"  Version: {houdini_info['houdini_version']}")
                click.echo("✓ Full Houdini functionality available")
        except Exception as e:
            click.echo(f"✗ Houdini module error: {e}")
    else:
        click.echo("ℹ  Houdini module not available (development mode)")
        click.echo("  For actual Houdini integration:")
        click.echo("  1. Install zabob-houdini: pip install zabob-houdini")
        click.echo("  2. Use within Houdini's Python shelf tools or HDA scripts")
        click.echo("  3. hython has severe virtual environment compatibility issues")

        # Check environment variables as fallback info
        houdini_path = os.getenv("HOUDINI_PATH")
        if houdini_path:
            click.echo(f"ℹ  HOUDINI_PATH: {houdini_path}")
            if os.path.exists(houdini_path):
                click.echo("  Path exists")
            else:
                click.echo("  Path does not exist")
        else:
            click.echo("ℹ  HOUDINI_PATH not set")



def run_as_script() -> None:
    """
    Entry point when running as a script with hython or uv run.
    """
    if _check_houdini_available():
        # Running with Houdini - full functionality available
        click.echo("🚀 Running with Houdini - full functionality available")
    else:
        # Running without Houdini
        click.echo("🐍 Running in development mode (no Houdini)")
        click.echo("   For actual node creation, use zabob-houdini within Houdini's Python environment")

    click.echo()
    main()


if __name__ == "__main__":
    run_as_script()
