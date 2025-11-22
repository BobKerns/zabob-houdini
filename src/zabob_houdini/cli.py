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
import subprocess
import sys

from zabob_houdini.houdini_bridge import call_houdini_function, houdini_command
from zabob_houdini.utils import JsonValue
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


@main.command()
def diagnose() -> None:
    """
    Print diagnostic information for troubleshooting environment issues.

    Shows Python executable paths, package installation locations, hython availability,
    and Houdini package configuration. Useful for debugging worktree and virtual
    environment issues.
    """
    import shutil
    from pathlib import Path
    from zabob_houdini.package_installer import get_houdini_package_dirs

    click.echo("Zabob-Houdini Diagnostic Information")
    click.echo("=" * 70)

    # Python environment
    click.echo("\n[Python Environment]")
    click.echo(f"Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    click.echo(f"Python Executable: {sys.executable}")

    # Find zabob-houdini installation location
    try:
        import zabob_houdini
        install_path = Path(zabob_houdini.__file__).parent.parent.resolve()
        click.echo(f"Zabob Package Location: {install_path}")
    except Exception as e:
        click.echo(f"Zabob Package Location: Error - {e}")

    # Check for zabob-houdini command in PATH
    click.echo("\n[Command Locations]")
    zabob_cmd = shutil.which("zabob-houdini")
    if zabob_cmd:
        click.echo(f"zabob-houdini command: {zabob_cmd}")
        # Check if it's in a venv
        if ".venv" in zabob_cmd:
            click.echo("  ✓ Running from virtual environment")
        elif "Library/Python" in zabob_cmd:
            click.echo("  ⚠ Running from user site-packages (may conflict with venv)")
    else:
        click.echo("zabob-houdini command: Not found in PATH")

    # hython availability
    hython_path = shutil.which("hython")
    if hython_path:
        click.echo(f"hython: {hython_path}")
        try:
            result = subprocess.run(
                [hython_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            version_output = result.stderr.strip() if result.stderr else result.stdout.strip()
            if version_output:
                click.echo(f"  Version: {version_output.split()[0] if version_output else 'Unknown'}")
        except Exception as e:
            click.echo(f"  Version: Error getting version - {e}")
    else:
        click.echo("hython: ⚠ Not found in PATH")
        click.echo("  Houdini may not be installed or not in your PATH")

    # Houdini package configuration
    click.echo("\n[Houdini Package Configuration]")
    package_dirs = get_houdini_package_dirs()
    if package_dirs:
        click.echo("Houdini package directories:")
        for pkg_dir in package_dirs:
            exists = "✓" if pkg_dir.exists() else "✗"
            click.echo(f"  {exists} {pkg_dir}")

            # Check for zabob_houdini.json
            package_json = pkg_dir / "zabob_houdini.json"
            if package_json.exists():
                try:
                    import json
                    with open(package_json) as f:
                        config = json.load(f)
                    pythonpath = config.get("env", [{}])[0].get("PYTHONPATH", {}).get("value", "")
                    click.echo(f"    Installed - points to: {pythonpath}")
                except Exception as e:
                    click.echo(f"    Installed - error reading: {e}")
    else:
        click.echo("No Houdini package directories found")

    # Environment variables
    click.echo("\n[Environment Variables]")
    houdini_path = os.getenv("HOUDINI_PATH")
    if houdini_path:
        click.echo("HOUDINI_PATH:")
        for p in houdini_path.split(os.pathsep):
            click.echo(f"  {p}")
    else:
        click.echo("HOUDINI_PATH: Not set")

    pythonpath = os.getenv("PYTHONPATH")
    if pythonpath:
        click.echo("PYTHONPATH:")
        for p in pythonpath.split(os.pathsep):
            click.echo(f"  {p}")
    else:
        click.echo("PYTHONPATH: Not set")

    virtual_env = os.getenv("VIRTUAL_ENV")
    if virtual_env:
        click.echo(f"VIRTUAL_ENV: {virtual_env}")
    else:
        click.echo("VIRTUAL_ENV: Not set (no virtual environment active)")

    # Worktree detection
    click.echo("\n[Git Worktree Information]")
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            repo_root = result.stdout.strip()
            click.echo(f"Repository root: {repo_root}")

            # Check if this is a worktree
            git_dir = Path.cwd() / ".git"
            if git_dir.is_file():
                click.echo("  ✓ This is a git worktree")
                with open(git_dir) as f:
                    click.echo(f"  {f.read().strip()}")
            else:
                click.echo("  This is the main repository (not a worktree)")
    except Exception:
        click.echo("Not in a git repository")

    # Virtual environment consistency check
    click.echo("\n[Virtual Environment Consistency]")
    venv_path = Path.cwd() / ".venv"
    if venv_path.exists():
        # Find the .pth file in site-packages
        site_packages = list(venv_path.glob("lib/*/site-packages"))
        if site_packages:
            pth_file = site_packages[0] / "_zabob_houdini.pth"
            if pth_file.exists():
                try:
                    with open(pth_file) as f:
                        venv_points_to = f.read().strip()
                    current_src = (Path.cwd() / "src").resolve()
                    venv_src = Path(venv_points_to).resolve()

                    if venv_src == current_src:
                        click.echo(f"✓ Virtual environment points to current worktree")
                        click.echo(f"  {venv_points_to}")
                    else:
                        click.echo(f"⚠ Virtual environment points to DIFFERENT location!")
                        click.echo(f"  Expected: {current_src}")
                        click.echo(f"  Actual:   {venv_src}")
                        click.echo(f"  → Fix: deactivate 2>/dev/null; rm -rf .venv && uv sync")
                except Exception as e:
                    click.echo(f"Error reading .pth file: {e}")
            else:
                click.echo("⚠ No _zabob_houdini.pth found in site-packages")
                click.echo("  → Run 'uv sync' to create it")
        else:
            click.echo("⚠ No site-packages directory found in .venv")
    else:
        click.echo("✗ No .venv directory found")
        click.echo("  → Run 'uv sync' to create virtual environment")

    click.echo("\n" + "=" * 70)
    click.echo("Troubleshooting Tips:")
    click.echo("• If zabob-houdini is not from .venv, run: source .venv/bin/activate")
    click.echo("• If venv points to wrong worktree: deactivate; rm -rf .venv && uv sync")
    click.echo("• After fixing venv, run: zabob-houdini install-package")
    click.echo("  (This points Houdini to your current worktree's src/ directory)")
    click.echo("=" * 70)

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


@main.command()
@houdini_command
@click.argument('script_path', type=click.Path(exists=True, readable=True))
@click.argument('script_args', nargs=-1, type=str)
@click.option('--hipfile', '-o', type=click.Path(),
              help='Save the resulting Houdini scene to this file path')
@click.option('--verbose', '-v', is_flag=True,
              help='Show verbose output from script execution')
def run(script_path: str, script_args: tuple[str, ...], hipfile: str | None, verbose: bool) -> None:
    """
    Run a Python script in hython and optionally save the resulting hip file.

    SCRIPT_PATH: Path to the Python script to execute in hython
    SCRIPT_ARGS: Additional arguments to pass to the script

    Examples:
        zabob-houdini run examples/diamond_chain_demo.py
        zabob-houdini run my_script.py --hipfile /tmp/result.hip
        zabob-houdini run examples/diamond_chain_demo.py arg1 arg2 --hipfile scene.hip
    """
    # This is just a stub - the real implementation is in houdini_functions.py
    pass

main.add_command(info)

if __name__ == "__main__":
    main()
