"""
Bridge for running Houdini functions either directly or via hython subprocess.
"""

import json
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Any


def _is_in_houdini() -> bool:
    """Check if we're currently running in Houdini Python environment."""
    # Check if hou is already loaded in sys.modules instead of trying to import it
    # Attempting to import hou in regular Python causes segfaults
    return 'hou' in sys.modules


def _find_hython() -> Path:
    """Find hython executable."""
    loc = shutil.which("hython")
    if loc is not None:
        return Path(loc)
    raise RuntimeError("hython executable not found. Please ensure Houdini is installed and hython is on the path")


def call_houdini_function(func_name: str, *args: Any, module: str = "houdini_functions") -> dict[str, str]:
    """
    Call a function from a houdini module, either directly or via hython subprocess.

    Args:
        func_name: Name of the function to call
        *args: Arguments to pass to the function (will be converted to strings for subprocess)
        module: Module name to import from (default: "houdini_functions")

    Returns:
        Dictionary with result data

    Raises:
        RuntimeError: If hython is not found or function call fails
    """
    if _is_in_houdini():
        # Already in Houdini, call function directly
        houdini_module = __import__(f"zabob_houdini.{module}", fromlist=[module])
        func = getattr(houdini_module, func_name)
        result = func(*args)
        # Ensure we return a dict
        if isinstance(result, dict):
            return result
        elif isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"result": result}
        else:
            return {"result": str(result)}

    # Not in Houdini, execute via hython subprocess
    result_str = _run_function_via_subprocess(func_name, args, module)
    try:
        return json.loads(result_str)
    except json.JSONDecodeError:
        return {"result": result_str}


def _run_function_via_subprocess(func_name: str, args: tuple, module: str = "houdini_functions") -> Any:
    """Execute function using 'hython -m zabob_houdini <module> <function_name> <args...>'."""
    hython_path = _find_hython()

    # Convert arguments to strings
    str_args = [str(arg) for arg in args]

    try:
        result = subprocess.run([
            str(hython_path), "-m", "zabob_houdini", module, func_name, *str_args
        ], check=True, capture_output=True, text=True)

        # Return the stdout
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"hython -m zabob_houdini {module} {func_name} failed: {e.stderr}")

