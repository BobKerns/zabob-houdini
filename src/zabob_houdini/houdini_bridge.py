"""
Bridge for running Houdini functions either directly or via hython subprocess.
"""

import json
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Any, TypedDict, NotRequired


class HoudiniResult(TypedDict):
    """Result structure from Houdini function calls."""
    success: bool
    result: NotRequired[dict[str, str]]
    error: NotRequired[str]
    traceback: NotRequired[str]


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


def call_houdini_function(func_name: str, *args: Any, module: str = "houdini_functions") -> HoudiniResult:
    """
    Call a function from a houdini module, either directly or via hython subprocess.

    Args:
        func_name: Name of the function to call
        *args: Arguments to pass to the function (will be converted to strings for subprocess)
        module: Module name to import from (default: "houdini_functions")

    Returns:
        HoudiniResult with success boolean and optional result/error data

    Raises:
        RuntimeError: If hython is not found or function call fails
    """
    if _is_in_houdini():
        # Already in Houdini, call function directly
        houdini_module = __import__(f"zabob_houdini.{module}", fromlist=[module])
        func = getattr(houdini_module, func_name)
        raw_result = func(*args)
        return _normalize_result(raw_result)

    # Not in Houdini, execute via hython subprocess
    result_str = _run_function_via_subprocess(func_name, args, module)
    return _normalize_result(result_str)


def _normalize_result(raw_result: Any) -> HoudiniResult:
    """Convert raw function result to normalized HoudiniResult."""
    if isinstance(raw_result, str):
        try:
            parsed = json.loads(raw_result)
            if isinstance(parsed, dict):
                # Convert parsed dict to HoudiniResult
                result: HoudiniResult = {"success": bool(parsed.get("success", False))}
                if "error" in parsed:
                    result["error"] = str(parsed["error"])
                if "traceback" in parsed:
                    result["traceback"] = str(parsed["traceback"])

                # Add remaining fields as result data (preserve original types)
                result_data = {k: v for k, v in parsed.items()
                             if k not in ["success", "error", "traceback"]}
                if result_data:
                    result["result"] = result_data

                return result
            else:
                return {"success": True, "result": {"value": str(parsed)}}
        except json.JSONDecodeError:
            return {"success": True, "result": {"value": raw_result}}

    elif isinstance(raw_result, dict):
        # Convert dict to HoudiniResult
        result: HoudiniResult = {"success": bool(raw_result.get("success", True))}
        if "error" in raw_result:
            result["error"] = str(raw_result["error"])
        if "traceback" in raw_result:
            result["traceback"] = str(raw_result["traceback"])

        # Add remaining fields as result data (preserve original types)
        result_data = {k: v for k, v in raw_result.items()
                     if k not in ["success", "error", "traceback"]}
        if result_data:
            result["result"] = result_data

        return result

    else:
        return {"success": True, "result": {"value": str(raw_result)}}


def _run_function_via_subprocess(func_name: str, args: tuple, module: str = "houdini_functions") -> Any:
    """Execute function using 'hython -m zabob_houdini <module> <function_name> <args...>'."""
    hython_path = _find_hython()

    # Convert arguments to strings
    str_args = [str(arg) for arg in args]

    cmd = [str(hython_path), "-m", "zabob_houdini", module, func_name, *str_args]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"hython -m zabob_houdini {module} {func_name} failed: {e.stderr}")

