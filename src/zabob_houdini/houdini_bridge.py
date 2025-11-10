"""
Bridge for running Houdini functions either directly or via hython subprocess.

## Architecture and Rationale

This module provides a consistent interface for calling Houdini functions, whether running
inside Houdini's Python environment or externally via subprocess calls to hython.

### Type-Safe Result Handling

All Houdini function calls return a `HoudiniResult` structure with consistent fields:
- `success: bool` - Whether the operation succeeded
- `result: JsonObject` - The actual result data (if successful)
- `error: str` - Error message (if failed)
- `traceback: str` - Full traceback (if failed)

### Decorator Pattern

Houdini-side functions use decorators to ensure consistent return types:

- `@houdini_result` for functions returning `JsonObject`
  - Wraps exceptions into error structure
  - Ensures `result` field contains the JsonObject return value

- `@houdini_message` for functions returning simple strings
  - Wraps string return in `{"message": string}` structure
  - Maintains type consistency (result is always JsonObject)

This approach provides:
1. **Type Safety**: All results have the same structure
2. **Error Handling**: Consistent exception catching and reporting
3. **Simplicity**: Calling code always knows what to expect
4. **JSON Compatibility**: All data is JSON-serializable for subprocess calls
"""

from collections.abc import Callable
from curses import raw
import functools
import json
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Any, ParamSpec, TypeAlias, TypedDict, NotRequired


JsonAtomicValue: TypeAlias = str | int | float | bool | None
'''An atomic JSON value, such as a string, number, boolean, or null.'''
JsonArray: TypeAlias = 'list[JsonValue]'
'''A Json array, which is a list of JSON values.'''
JsonObject: TypeAlias = 'dict[str, JsonValue]'
'''A Json object, which is a dictionary with string keys and JSON values.'''
JsonValue: TypeAlias = 'JsonAtomicValue | JsonArray | JsonObject'
'''A Json value, which can be an atomic value, array, or object.'''

class HoudiniResult(TypedDict):
    """Result structure from Houdini function calls."""
    success: bool
    result: NotRequired[JsonObject]
    error: NotRequired[str]
    traceback: NotRequired[str]

P = ParamSpec('P')

def houdini_result(func: Callable[P, dict[str, JsonValue]]) -> Callable[P, HoudiniResult]:
    """
    Decorator that converts function return values to JSON result values.

    The decorated function will return a JSON string representation of the
    original return value, while preserving the exact parameter types and names
    of the original function.

    Args:
        func: Function to decorate

    Returns:
        Decorated function that returns JSON strings with preserved parameter types

    Example:
        @json_result
        def get_node_info(node: hou.Node, include_parms: bool = False) -> str:
            return {"name": node.name(), "type": node.type().name()}

        # Type checker knows the parameters: get_node_info(node: hou.Node, include_parms: bool = False) -> str
        # Returns: '{"name": "geo1", "type": "geo"}'
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> HoudiniResult:
        try:
            result = func(*args, **kwargs)
            return {
                'success': True,
                'result': result
                }
        except Exception as e:
            import traceback
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }

    return wrapper

def houdini_message(func: Callable[P, str]) -> Callable[P, HoudiniResult]:
    """
    Decorator that converts a function returning a string message to a HoudiniResult.

    The decorated function will return a HoudiniResult with the message in the 'result' field.

    Args:
        func: Function to decorate

    Returns:
        Decorated function that returns a HoudiniResult with the message
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> dict[str, JsonValue]:
        message = func(*args, **kwargs)
        return {'message': message}
    return houdini_result(wrapper)

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
    return json.loads(raw_result)


def _run_function_via_subprocess(func_name: str, args: tuple, module: str = "houdini_functions") -> Any:
    """Execute function using 'hython -m zabob_houdini _exec <module> <function_name> <args...>'."""
    hython_path = _find_hython()

    # Convert arguments to strings
    str_args = [str(arg) for arg in args]

    cmd = [str(hython_path), "-m", "zabob_houdini", "_exec", module, func_name, *str_args]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"hython -m zabob_houdini _exec {module} {func_name} failed: {e.stderr}")

