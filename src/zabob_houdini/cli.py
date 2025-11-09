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
import json
import os
import sys

from zabob_houdini.houdini_bridge import call_houdini_function

def get_environment_info() -> dict[str, str]:
    """Get information about the current Python and Houdini environment."""
    info = {
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'python_executable': sys.executable or 'unknown',
        'platform': sys.platform,
    }

    # Always try to get Houdini info via bridge
    try:
        from zabob_houdini.houdini_bridge import call_houdini_function
        houdini_info = call_houdini_function('get_houdini_info')
        if isinstance(houdini_info, dict):
            info.update(houdini_info)
            info['houdini_available'] = 'true'
        else:
            info['houdini_available'] = 'false'
    except Exception as e:
        info['houdini_available'] = 'false'
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
def list_types(category: str | None) -> None:
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
    click.echo("Testing node creation via Houdini bridge...")

    try:
        from zabob_houdini.houdini_bridge import call_houdini_function
        result = call_houdini_function('test_node_creation')

        if isinstance(result, str):
            import json
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                click.echo(f"✓ Node test result: {result}")
                return

        if isinstance(result, dict) and result.get('success'):
            click.echo("✓ Node creation test passed")
            click.echo(f"  Created node: {result.get('node_path', 'N/A')}")
            if 'node_type' in result:
                click.echo(f"  Node type: {result['node_type']}")
        else:
            error_msg = result.get('error', 'Unknown error') if isinstance(result, dict) else str(result)
            click.echo(f"✗ Node creation test failed: {error_msg}")

    except RuntimeError as e:
        if "hython not found" in str(e):
            click.echo("⚠  Hython not available")
            click.echo("  For actual node creation, ensure Houdini is installed and hython is on PATH")
        else:
            click.echo(f"✗ Runtime error: {e}")
    except Exception as e:
        click.echo(f"✗ Test failed: {e}")


@main.command()
def test_chain():
    """Test chain functionality."""
    click.echo("Testing chain functionality...")

    try:
        result_str = call_houdini_function('houdini_test_functions', 'test_basic_availability')
        result = json.loads(result_str)

        if result.get('success'):
            click.echo("✓ Chain functionality test passed")
            click.echo("  Basic chain operations are available")
        else:
            error_msg = result.get('error', 'Unknown error')
            click.echo(f"✗ Chain functionality test failed: {error_msg}")
    except RuntimeError as e:
        if "hython not found" in str(e):
            click.echo("⚠  Hython not available")
            click.echo("  For actual chain functionality, ensure Houdini is installed and hython is on PATH")
        else:
            click.echo(f"✗ Runtime error: {e}")
    except Exception as e:
        click.echo(f"✗ Test failed: {e}")


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

    # Always try to get Houdini info via bridge
    try:
        houdini_info_str = call_houdini_function('get_houdini_info')
        if houdini_info_str and houdini_info_str.strip():
            try:
                houdini_info = json.loads(houdini_info_str)
                if 'houdini_app' in houdini_info:
                    click.echo("\nHoudini Information:")
                    click.echo("-" * 30)
                    click.echo(f"Application: {houdini_info['houdini_app']}")
                    click.echo(f"Version: {houdini_info['houdini_version']}")
                    if 'houdini_build' in houdini_info:
                        click.echo(f"Build: {houdini_info['houdini_build']}")
            except json.JSONDecodeError:
                click.echo(f"\nHoudini Info: {houdini_info_str}")
    except Exception:
        # Silently handle no Houdini availability
        pass

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
    env_info = get_environment_info()

    if env_info.get('houdini_available') == 'true':
        click.echo("✓ Houdini environment is available and working")
    else:
        click.echo("✗ Houdini environment is not available")
        sys.exit(1)



if __name__ == "__main__":
    main()
