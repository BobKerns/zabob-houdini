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

from typing import cast
import click
import os
import sys

from zabob_houdini.houdini_bridge import JsonValue, call_houdini_function, houdini_command
from zabob_houdini.__version__ import __version__, __distribution__

def get_environment_info() -> dict[str, JsonValue]:
    """Get information about the current Python and Houdini environment."""
    info: dict[str, JsonValue] = {
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'python_executable': sys.executable or 'unknown',
        'platform': sys.platform,
    }

    # Always try to get Houdini info via bridge
    try:
        houdini_result = call_houdini_function('get_houdini_info')
        if houdini_result['success'] and 'result' in houdini_result:
            info.update(houdini_result['result'])
            info['houdini_available'] = True
        else:
            info['houdini_available'] = False
            if 'error' in houdini_result:
                info['houdini_error'] = houdini_result['error']
    except Exception as e:
        info['houdini_available'] = False
        info['houdini_error'] = str(e)

    return info


@click.group()
@click.version_option(version=__version__, prog_name=__distribution__)
def main() -> None:
    """
    Zabob-Houdini development utilities.

    Simple CLI for validating Houdini integration and listing node types.
    """
    pass

@click.group("diagnostics")
@click.version_option(version=__version__, prog_name=__distribution__)
def diagnostics() -> None:
    """
    Diagnostic commands for checking Houdini environment and functionality.
    """
    pass

main.add_command(diagnostics)

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


@diagnostics.command()
def test_node() -> None:
    """
    Test creating a simple node (requires Houdini).
    """
    click.echo("Testing node creation via Houdini bridge...")

    try:
        result = call_houdini_function('test_zabob_node_creation',
                                                     module='houdini_test_functions')

        if result['success']:
            click.echo("✓ Node creation test passed")
            if 'result' in result:
                result_data = result['result']
                click.echo(f"  Created node: {result_data.get('node_path', 'N/A')}")
                if 'node_type' in result_data:
                    click.echo(f"  Node type: {result_data['node_type']}")
        else:
            error_msg = result.get('error', 'Unknown error')
            click.echo(f"✗ Node creation test failed: {error_msg}")

    except RuntimeError as e:
        if "hython not found" in str(e):
            click.echo("⚠  Hython not available")
            click.echo("  For actual node creation, ensure Houdini is installed and hython is on PATH")
        else:
            click.echo(f"✗ Runtime error: {e}")
    except Exception as e:
        click.echo(f"✗ Test failed: {e}")


@diagnostics.command()
def test_chain():
    """Test chain functionality."""
    click.echo("Testing chain functionality...")

    try:
        result = call_houdini_function('test_zabob_chain_creation',
                                                        module='houdini_test_functions')

        if result['success']:
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
def environment() -> None:
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

    def show_path(title: str, path: JsonValue):
        match path:
            case str() if path:
                click.echo(f"{title}:")
                for p in path.split(os.pathsep):
                    click.echo(f"  {p}")
            case _:
                click.echo(f"{title}: Not set")
    # Always try to get Houdini info via bridge
    try:
        houdini_result = call_houdini_function('get_houdini_info')
        if houdini_result['success'] and 'result' in houdini_result:
            houdini_info = houdini_result['result']
            if 'houdini_app' in houdini_info:
                click.echo("\nHoudini Information:")
                click.echo("-" * 30)
                click.echo(f"Application: {houdini_info['houdini_app']}")
                click.echo(f"Version: {'.'.join(map(str, cast(list, houdini_info['houdini_version'])))}")
                if 'houdini_build' in houdini_info:
                    click.echo(f"Build: {houdini_info['houdini_build']}")
                click.echo(f"Hython Version: {houdini_info.get('hython_version', 'N/A')}")
                env = houdini_info.get('houdini_environment', {})
                if not isinstance(env, dict):
                    env = {}
                houdini_path = env.get('HOUDINI_PATH', '')
                python_path = env.get('PYTHONPATH', '')
                show_path('HOUDINI_PATH', houdini_path)
                show_path('PYTHONPATH', python_path)
    except Exception:
        # Silently handle no Houdini availability
        pass

    # Environment variables
    click.echo("\nGlobal Environment Variables:")
    click.echo("-" * 30)
    houdini_path = os.getenv("HOUDINI_PATH")
    show_path('HOUDINI_PATH', houdini_path)
    python_path = os.getenv("PYTHONPATH")
    show_path('PYTHONPATH', python_path)


@main.command()
def validate() -> None:
    """
    Validate Houdini installation and Python environment.
    """
    env_info = get_environment_info()

    if env_info.get('houdini_available'):
        click.echo("✓ Houdini environment is available and working")
    else:
        click.echo("✗ Houdini environment is not available")
        sys.exit(1)

@click.group("info")
def info():
    """
    Commands for extracting information about the Houdini environment.
    """
    pass


@info.command('categories')
@houdini_command
@click.argument('args', nargs=-1, type=str)
def categories(args: tuple[str, ...]) -> None:
    """
    Analyze node categories in the current Houdini session and print the results.
    """
    pass


@info.command('types')
@houdini_command
@click.argument('category', type=str)
def types(category: str) -> None:
    """
    List node types in the specified category with basic information.

    CATEGORY: The name of the node category to analyze (e.g., 'Sop', 'Object', 'Dop')
    """
    pass

if __name__ == "__main__":
    main()
