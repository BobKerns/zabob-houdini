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

from __future__ import annotations, _dynamic_import # noqa: F407 E261 # type: ignore


from contextlib import contextmanager
import os
import sys
from pathlib import Path
import subprocess

import hou

from zabob_houdini.utils import JsonObject
from zabob_houdini.houdini_bridge import minimal_env


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


@contextmanager
def with_argv(*args: str):
    """Context manager to temporarily set sys.argv for a block of code."""
    original_argv = sys.argv.copy()
    try:
        sys.argv = list(args)
        yield
    finally:
        sys.argv = original_argv


def save_hipfile(hipfile: str | None = None, open_app: bool = False) -> None:
    import click
    if hipfile:
        hipfile_path = Path(hipfile)
        hipfile_path.parent.mkdir(parents=True, exist_ok=True)
        hou.hipFile.save(str(hipfile_path))
        click.echo(f"✓ Scene saved to: {hipfile_path}")

    # After hython exits, open the file if requested
    if open_app and hipfile:
        hipfile_name = Path(hipfile).name
        click.echo(f"Opening {hipfile_name}...")
        try:
            if sys.platform == "win32":
                os.startfile(hipfile)
            elif sys.platform == "darwin":
                # Use -n/--new to open in a new instance, avoiding crashes when Houdini is already running
                subprocess.Popen(["open", "-n", hipfile])
            else:  # Linux
                subprocess.Popen(["xdg-open", hipfile])
        except Exception as e:
            click.echo(f"Warning: Failed to open file: {e}", err=True)


def _run_in_hython(script_path: str, *script_args: str,
                   hipfile: str | None = None,
                   save: bool = False,
                   verbose: bool = False,
                   open_app: bool = False,
                   ) -> None:
    """
    Run a Python script in hython and optionally save the resulting hip file.
    """
    import click

    script_path_obj = Path(script_path).resolve()

    # Handle --save flag: use basename.hip in same directory as script if hipfile not specified
    if save and not hipfile:
        basename = script_path_obj.stem  # filename without extension
        hipfile = str(script_path_obj.parent / f"{basename}.hip")

    if verbose:
        click.echo(f"Running script: {script_path_obj}")
        if script_args:
            click.echo(f"Script arguments: {' '.join(script_args)}")
        if hipfile:
            click.echo(f"Will save scene to: {hipfile}")

    try:
        # Add script directory to Python path so imports work
        script_dir = str(script_path_obj.parent)
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        script_path_str = str(script_path_obj)
        try:
            with with_argv(script_path_str, *script_args):
                # Set up sys.argv as if the script was called directly
                sys.argv = [str(script_path_obj)] + list(script_args)

                # Read and execute the script
                from zabob_houdini.dyn_loader import transform_script
                script_code = script_path_obj.read_text()
                script_obj, _ = transform_script(script_code, str(script_path_obj))
                # Execute in global namespace so imports and variables persist
                exec(script_obj, {'__name__': '__main__', '__file__': str(script_path_obj)})

                click.echo(f"✓ Script executed successfully: {script_path_obj.name}")

        except Exception as e:
            import traceback

            # Extract exception traceback, including chained exceptions
            relevant_frames = []

            # Walk the exception chain (e.__cause__ and e.__context__)
            current_exception = e
            while current_exception is not None:
                tb = traceback.extract_tb(current_exception.__traceback__)

                for frame in tb:
                    # Include if it's from the user's script
                    if verbose or (
                                __file__ not in frame.filename
                                and '/hou.py' not in frame.filename
                            ):
                        relevant_frames.append(frame)

                # Move to the next exception in the chain
                current_exception = current_exception.__cause__ or current_exception.__context__
                # Avoid infinite loops
                if current_exception == e:
                    break

            if relevant_frames:
                # Show API frames (and script frames if any)
                click.echo("✗ Error executing script:", err=True)
                click.echo("\nTraceback (most recent call last):", err=True)
                for frame in relevant_frames:
                    click.echo(f'  File "{frame.filename}", line {frame.lineno}, in {frame.name}', err=True)
                    if frame.line:
                        click.echo(f"    {frame.line}", err=True)
                click.echo(f"{type(e).__name__}: {e}", err=True)
            else:
                # No relevant frames - this is an internal error before/after script execution
                click.echo(f"✗ Error: {e}", err=True)
                if verbose:
                    # Only show internal traceback if verbose is enabled
                    traceback.print_exc()
        save_hipfile(hipfile, open_app=open_app)
    except SystemExit:
        # Re-raise SystemExit to preserve exit codes
        raise
    except Exception as e:
        # Catch any errors outside the script execution (e.g., file reading errors)
        click.echo(f"✗ Error: {e}", err=True)
        save_hipfile(hipfile, open_app=open_app)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _run_with_more(*script_args: str) -> None:
    """
    Run a Python script in hython with more verbose error reporting and optionally save the resulting hip file.

    This is an enhanced version of _run_in_hython that provides more detailed error information.
    """
    import shlex

    args = shlex.split(script_args[-1])
    new_args = ["-m", "zabob_houdini", *script_args[0:-1], *args]
    os.execlpe(sys.executable, sys.executable, *new_args, minimal_env())
