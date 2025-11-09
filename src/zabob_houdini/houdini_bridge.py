"""
Bridge for running Houdini functions either directly or via hython subprocess.
"""

import subprocess
import shutil
from pathlib import Path
from typing import Any


def _is_in_houdini() -> bool:
    """Check if we're currently running in Houdini Python environment."""
    try:
        import hou
        return True
    except ImportError:
        return False


def _find_hython() -> Path:
    """Find hython executable."""
    loc = shutil.which("hython")
    if loc is not None:
        return Path(loc)
    raise RuntimeError("hython executable not found. Please ensure Houdini is installed and hython is on the path")


def call_houdini_function(func_name: str, *args: Any) -> Any:
    """
    Call a function from houdini_functions module, either directly or via hython subprocess.

    Args:
        func_name: Name of the function in houdini_functions module
        *args: Arguments to pass to the function (will be converted to strings for subprocess)

    Returns:
        Result from the function call

    Raises:
        RuntimeError: If hython is not found or function call fails
    """
    if _is_in_houdini():
        # Already in Houdini, call function directly
        from . import houdini_functions
        func = getattr(houdini_functions, func_name)
        return func(*args)

    # Not in Houdini, execute via hython subprocess
    return _run_function_via_subprocess(func_name, args)


def _run_function_via_subprocess(func_name: str, args: tuple) -> Any:
    """Execute function using 'hython -m zabob_houdini <function_name> <args...>'."""
    hython_path = _find_hython()

    # Convert arguments to strings
    str_args = [str(arg) for arg in args]

    try:
        result = subprocess.run([
            str(hython_path), "-m", "zabob_houdini", func_name, *str_args
        ], check=True, capture_output=True, text=True)

        # Return the stdout
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"hython -m zabob_houdini {func_name} failed: {e.stderr}")

