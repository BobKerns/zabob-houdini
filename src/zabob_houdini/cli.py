
"""
Zabob-Houdini CLI - Simple utilities for development and testing.

Note: hython has severe virtual environment compatibility issues due to
linked symbol requirements. This CLI is designed for development and testing
with regular Python. For actual Houdini node creation, use the package
within Houdini's Python shelf tools or HDA scripts.
"""

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from typing import cast
import click
import os
import subprocess
import sys

from zabob_houdini.houdini_bridge import call_houdini_function, houdini_command, minimal_env
from zabob_houdini.utils import JsonValue
from zabob_houdini.__version__ import __version__, __distribution__

CATEGORIES = [
    'Chop', 'Cop', 'Cop2', 'Cop2Net', 'CopNet', 'Director',
    'Dop', 'Driver', 'Lop', 'Manager', 'Object', 'Shop',
    'Sop', 'Top', 'Vop']


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
    hython_found = False
    if hython_path:
        click.echo(f"hython: {hython_path}")
        hython_found = True
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
                        click.echo("✓ Virtual environment points to current worktree")
                        click.echo("  {venv_points_to}")
                    else:
                        click.echo("⚠ Virtual environment points to DIFFERENT location!")
                        click.echo("  Expected: {current_src}")
                        click.echo("  Actual:   {venv_src}")
                        click.echo("  → Fix: deactivate 2>/dev/null; rm -rf .venv && uv sync")
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

    # Houdini pythonrc.py check
    if hython_found:
        click.echo("\n[Houdini pythonrc.py]")
        from zabob_houdini.houdini_config import find_houdini_pref_dir
        from zabob_houdini.package_installer import get_houdini_python_version

        user_prefs = find_houdini_pref_dir()
        if user_prefs:
            py_version_str = get_houdini_python_version()
            if py_version_str:
                py_version = f"python{py_version_str}libs"
                pythonrc_path = user_prefs / py_version / "pythonrc.py"

                if pythonrc_path.exists():
                    content = pythonrc_path.read_text()
                    if 'zabob-houdini' in content:
                        click.echo(f"✓ Installed: {pythonrc_path}")
                    else:
                        click.echo(f"⚠ Exists but not zabob-houdini: {pythonrc_path}")
                        click.echo("  → Run: zabob-houdini install-package")
                else:
                    click.echo(f"✗ Not installed: {pythonrc_path}")
                    click.echo("  → Run: zabob-houdini install-package")
            else:
                click.echo("✗ Could not determine Houdini Python version")
        else:
            click.echo("✗ Could not find Houdini preferences directory")

    click.echo("\n" + "=" * 70)
    click.echo("Troubleshooting Tips:")
    click.echo("• If zabob-houdini is not from .venv, run: source .venv/bin/activate")
    click.echo("• If venv points to wrong worktree: deactivate; rm -rf .venv && uv sync")
    click.echo("• After fixing venv, run: zabob-houdini install-package")
    click.echo("  (This points Houdini to your current worktree's src/ directory)")
    if hython_found:
        click.echo("• For detailed Houdini installation info: zabob-houdini houdini show")
    else:
        click.echo("• To find Houdini installations: zabob-houdini houdini installations")
    click.echo("• To download other versions from SideFX: zabob-houdini sidefx versions")
    click.echo("=" * 70)


@click.group("houdini")
def houdini():
    """
    Commands for working with local Houdini installations and querying node information.
    """
    pass


@houdini.command('categories')
@houdini_command
@click.argument('args', nargs=-1, type=str)
def categories(args: tuple[str, ...]) -> None:
    """
    Analyze node categories in the current Houdini session and print the results.
    """
    pass


@houdini.command('types')
@houdini_command
@click.argument('category', type=click.Choice(CATEGORIES, case_sensitive=False))
def types(category: str) -> None:
    """
    List node types in the specified category with basic information.

    CATEGORY: The name of the node category to analyze (e.g., 'Sop', 'Object', 'Dop')
    """
    pass


@houdini.command('installations')
def installations() -> None:
    """
    List all installed Houdini versions on the system.
    """
    from zabob_houdini.find_houdini import find_houdini_installations

    installs = find_houdini_installations()
    if not installs:
        click.echo("No Houdini installations found.")
        return

    click.echo("Installed Houdini Versions:")
    click.echo()

    for version, install in sorted(installs.items(), key=lambda x: x[0]):
        if version.patch != 0:
            # MM.nn.0 versions are generic, not specific builds
            click.echo(f"{version}: (Python {install.python_version})")
            click.echo(f"    {install.version_dir}")


@houdini.command('show')
@click.argument('version', type=str, required=False, default=None)
def show(version: str | None = None) -> None:
    """
    Show detailed information about a Houdini installation.

    VERSION: Specific version to show ("20.5" or "20.5.584"), or latest if omitted
    """
    from pathlib import Path
    from zabob_houdini.find_houdini import get_houdini
    from zabob_houdini._find.types import _version

    try:
        houdini_install = get_houdini(_version(version) if version else None)
        click.echo(f"Found Houdini installation: {houdini_install}")
        click.echo(f"Installed applications: {', '.join(houdini_install.app_paths.keys())}")
        title = 'Python Version'
        click.echo(f"  {title:>14s}: {houdini_install.python_version}")
        title = 'Version Dir'
        version_dir = houdini_install.version_dir
        click.echo(f"  {title:>14s}: {version_dir}")
        for key in (
                    'exec_prefix',
                    'bin_dir',
                    'hython',
                    'hfs_dir',
                    'python_libs',
                    'hdso_libs',
                    'hh_dir',
                    'config_dir',
                    'toolkit_dir',
                    'sbin_dir',
                ):

            title = key.replace('_', ' ').title()
            title = title.replace('hfs', 'HFS')
            click.echo(f"      {title:>14s}: {Path(getattr(houdini_install, key)).relative_to(version_dir)}")
        click.echo("      PATH entries:")
        for p in houdini_install.env_path:
            click.echo(f"        {p.relative_to(version_dir)}")
        click.echo("      Python library paths:")
        for p in houdini_install.lib_paths:
            click.echo(f"        {p.relative_to(version_dir)}")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@main.command()
@click.argument('script_path', type=click.Path(exists=True, readable=True))
@click.argument('script_args', nargs=-1, type=str)
@click.option('--hipfile', '-o', type=click.Path(),
              help='Save the resulting Houdini scene to this file path')
@click.option('--save', '-s', is_flag=True,
              help='Save to <basename>.hip (shorthand for --hipfile <basename>.hip)')
@click.option('--open', 'open_app', is_flag=True,
              help='Open the saved HIP file in Houdini application (implies --save)')
@click.option('--verbose', '-v', is_flag=True,
              help='Show verbose output from script execution')
@click.option('--python', '-p', is_flag=True,
              help='Run with regular Python instead of hython (no Houdini environment)')
def run(script_path: str,
        script_args: tuple[str, ...],
        hipfile: str | None, save: bool,
        open_app: bool, verbose: bool,
        python: bool,
        ) -> None:
    """
    Run a Python script in hython (or regular Python with --python flag).

    By default, runs the script in hython (Houdini's Python environment).
    Use --python to run in regular Python without Houdini.

    Scripts using 'from __future__ import _dynamic_import' will have
    dynamic import transformation applied automatically.

    SCRIPT_PATH: Path to the Python script to execute
    SCRIPT_ARGS: Additional arguments to pass to the script

    Examples:
        zabob-houdini run examples/diamond_chain_demo.py
        zabob-houdini run examples/diamond_chain_demo.py --save
        zabob-houdini run my_script.py --hipfile /tmp/result.hip
        zabob-houdini run examples/diamond_chain_demo.py --save --open
        zabob-houdini run myscript.py --python
        zabob-houdini run myscript.py arg1 arg2 --python --verbose
    """
    from pathlib import Path
    import subprocess
    import sys

    # Validate option combinations
    if python and (save or hipfile or open_app):
        click.echo("Error: --python cannot be used with --save, --hipfile, or --open", err=True)
        sys.exit(1)

    # Handle --python mode: run in regular Python with dynamic import support
    if python:
        from zabob_houdini.dyn_loader import transform_script

        script_path_obj = Path(script_path).resolve()

        if verbose:
            click.echo(f"Running script in Python: {script_path_obj}")
            click.echo(f"Arguments: {script_args}")

        try:
            # Set up sys.argv as if the script was called directly
            sys.argv = [str(script_path_obj)] + list(script_args)

            # Read and transform the script if needed
            script_code = script_path_obj.read_text()
            script_obj, was_transformed = transform_script(script_code, str(script_path_obj))

            if verbose and was_transformed:
                click.echo("✓ Applied dynamic import transformation")

            # Execute in a namespace with __name__ set to '__main__'
            exec(script_obj, {'__name__': '__main__', '__file__': str(script_path_obj)})

            if verbose:
                click.echo("✓ Script executed successfully")
            return

        except Exception as e:
            import traceback
            click.echo(f"✗ Script failed with error: {e}", err=True)
            if verbose:
                traceback.print_exc()
            sys.exit(1)

    # --open implies --save
    if open_app:
        save = True

    # Calculate the hipfile path if --save is used
    script_path_obj = Path(script_path).resolve()
    if save and not hipfile:
        basename = script_path_obj.stem
        hipfile = str(script_path_obj.parent / f"{basename}.hip")

    # Call hython to run the script (manually construct the subprocess call to exclude --open)
    from zabob_houdini.houdini_bridge import _find_hython, _is_in_houdini

    if _is_in_houdini():
        # Already in houdini, call directly
        from zabob_houdini.houdini_functions import _run_in_hython
        _run_in_hython(script_path, *script_args,
                       hipfile=hipfile, save=save, verbose=verbose, open_app=open_app)
    else:
        hython_path = _find_hython()
        cmd = [str(hython_path), "-m", "zabob_houdini", "run", script_path]
        cmd.extend(script_args)
        if hipfile:
            cmd.extend(["--hipfile", hipfile])
        if save:
            cmd.append("--save")
        if verbose:
            cmd.append("--verbose")
        if open_app:
            cmd.append("--open")

        # Run with minimal environment

        try:
            subprocess.run(cmd, check=True, env=minimal_env())
        except subprocess.CalledProcessError as e:
            # Script failed - hython already printed the error, just exit with same code
            sys.exit(e.returncode)


main.add_command(houdini)

if __name__ == "__main__":
    main()
