"""
Zabob-Houdini CLI - Simple utilities for development and testing.
"""

import click
import os
from typing import Optional


@click.group()
@click.version_option()
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
    try:
        from .core import node
        click.echo("Testing node creation...")

        # Test node definition (should work without Houdini)
        test_node = node("/obj", "geo", name="test_geometry")
        click.echo("✓ Node definition created successfully")
        click.echo(f"  Parent: {test_node.parent}")
        click.echo(f"  Type: {test_node.node_type}")
        click.echo(f"  Name: {test_node.name}")

        # Test actual creation (requires Houdini)
        click.echo("Testing node creation in Houdini...")
        result = test_node.create()
        click.echo("✓ Node created successfully in Houdini")
        click.echo(f"  Created node: {result.path()}")

    except ImportError as e:
        if "hou" in str(e):
            click.echo("✗ Cannot import Houdini module")
            click.echo("  This test requires running within Houdini's Python environment")
            click.echo("  Run 'zabob-houdini validate' to check your setup")
        else:
            click.echo(f"✗ Import error: {e}")
    except Exception as e:
        click.echo(f"✗ Test failed: {e}")
@main.command()
def validate() -> None:
    """
    Validate Houdini installation and Python environment.
    """
    click.echo("Validating Houdini integration...")

    # Check environment variables
    houdini_path = os.getenv("HOUDINI_PATH")
    if houdini_path:
        click.echo(f"✓ HOUDINI_PATH: {houdini_path}")
        if os.path.exists(houdini_path):
            click.echo("✓ Path exists")
        else:
            click.echo("✗ Path does not exist")
    else:
        click.echo("✗ HOUDINI_PATH not set")
        click.echo("  Copy .env.example.<platform> to .env and configure")
        return

    # Try importing hou
    try:
        import hou
        click.echo("✓ Houdini module imported successfully")
        click.echo(f"  Application: {hou.applicationName()}")
        click.echo(f"  Version: {'.'.join(map(str, hou.applicationVersion()))}")
    except ImportError:
        click.echo("✗ Cannot import Houdini module")
        click.echo("  Check PYTHONPATH in your .env file")
    except Exception as e:
        click.echo(f"✗ Houdini module error: {e}")


if __name__ == "__main__":
    main()
