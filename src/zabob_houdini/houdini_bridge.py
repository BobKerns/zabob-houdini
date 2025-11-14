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

from collections.abc import Callable, Generator
from contextlib import contextmanager
import functools
import json
import os
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Any, ParamSpec, Sequence, TypedDict, NotRequired, cast

import click

from zabob_houdini.utils import JsonObject

class HoudiniResult(TypedDict):
    """Result structure from Houdini function calls."""
    success: bool
    result: NotRequired[JsonObject]
    error: NotRequired[str]
    traceback: NotRequired[str]


def error_result(message: str) -> HoudiniResult:
    """Helper to create an error result."""
    return {
        'success': False,
        'error': message
    }


def write_response(result: HoudiniResult) -> None:
    """Helper to write a HoudiniResult to stdout as JSON."""
    json.dump(result, sys.stdout)
    sys.stdout.write('\n')
    sys.stdout.flush()


def write_error_result(message: str) -> None:
    """Helper to write an error result to stdout."""
    error_response = error_result(message)
    json.dump(error_response, sys.stdout)
    sys.stdout.write('\n')
    sys.stdout.flush()


def _is_houdini_result(result: Any) -> bool:
    """Check if the result is a valid HoudiniResult."""
    if not isinstance(result, dict):
        return False
    if 'success' not in result or not isinstance(result['success'], bool):
        return False
    if result['success'] and "result" in result:
        return True
    if not result['success'] and "error" in result:
        return True
    return False

P = ParamSpec('P')


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


def _run_function_via_subprocess(func_name: str, args: tuple,
                                 module: str = "houdini_functions",
                                 runner: str="_exec") -> Any:
    """Execute function using 'hython -m zabob_houdini _exec <module> <function_name> <args...>'."""
    hython_path = _find_hython()

    # Convert arguments to strings
    str_args = [str(arg) for arg in args]

    cmd = [str(hython_path), "-m", "zabob_houdini", runner, module, func_name, *str_args]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, stderr=None)
        return result.stdout
    except subprocess.CalledProcessError as e:
        cmdline_args = ' '.join(str_args)
        if cmdline_args:
            cmdline_args = f"{cmdline_args} "
        msg = f"ERROR: hython -m zabob_houdini {runner} {module} {func_name} {cmdline_args}failed: {e.stderr}"
    raise RuntimeError(msg)


def _run_command_via_subprocess(func_name: str, args: tuple) -> Any:
    """Execute function using 'hython -m zabob_houdini <runner> <module> <function_name> <args...>'."""
    hython_path = _find_hython()

    # Convert arguments to strings
    str_args = [str(arg) for arg in args]

    cmd = [str(hython_path), "-m", "zabob_houdini", *str_args]
    try:
        result = subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
        return
    except subprocess.CalledProcessError as e:
        # Return code 1 might be due to SIGPIPE on some systems
        # Don't treat this as an error if it's likely due to broken pipe
        if e.returncode == 1:
            # Assume broken pipe, which is normal when piping to head, etc.
            return
        joined = ' '.join(str_args)
        msg = f"ERROR: hython -m zabob_houdini {func_name} {joined} failed: {e.returncode}"
        print(msg, file=sys.stderr)


def houdini_command(fn: Callable[P, None]) -> Callable[P, None]:
    """
    Decorator to create a Houdini command that can be called from the command line.

    The decorated function will be wrapped in a HoudiniResult and can be executed via hython.

    Args:
        func: Function to decorate a Houdini command, to run hython if needed.
    Returns:
        Decorated function that invokes hython if needed.
    """
    @functools.wraps(fn)
    @click.pass_context
    def wrapper(ctx: click.Context, *args: P.args, **kwargs: P.kwargs) -> None:
        if _is_in_houdini():
            # Already in Houdini, call function directly
            import zabob_houdini.houdini_functions as houdini_functions
            import zabob_houdini.houdini_info as houdini_info
            for m in (houdini_functions, houdini_info):
                if hasattr(m, fn.__name__):
                    func = getattr(m, fn.__name__)
                    return func(*args, **kwargs)
        else:
            # Not in Houdini, execute via hython subprocess
            name = fn.__name__
            cmd_args = tuple(sys.argv[1:])
            _run_command_via_subprocess(name, cmd_args)

    return wrapper


@contextmanager
def invoke_houdini_function(module_name: str, function_name: str, args: Sequence[str]) -> Generator[HoudiniResult, None, None]:
    """
    Helper function to invoke a Houdini function and return the result as a dictionary.

    This is used by the _exec command to execute functions within the Houdini Python environment.
    """
    try:
        import hou
        from zabob_houdini.core import _node_registry
        _node_registry.clear()  # Clear the node registry to avoid stale references between tests
        hou.hipFile.clear()  # Clear the current hip file to avoid stale state between tests
        # Import the specified module and call the requested function
        houdini_module = __import__(f"zabob_houdini.{module_name}", fromlist=[module_name])
        func = getattr(houdini_module, function_name)

        # Call function with arguments and capture result
        result = func(*args)
        match result:
            case str():
                yield {
                    'success': True,
                    'result': {
                        'message': result
                    }
                }
            case int()|float()|bool()|list():
                yield {
                    'success': True,
                    'result': {
                        'value': result
                    }
                }
            case Path():
                yield {
                    'success': True,
                    'result': {
                        'path': str(result)
                    }
                }
            case dict() if _is_houdini_result(result):
                yield cast(HoudiniResult, result)
            case dict():
                yield {
                    'success': True,
                    'result': result
                }
            case _:
                yield {
                    'success': False,
                    'error': f"Unexpected return type: {type(result)}"
                }

    except ImportError as e:
        yield error_result(f"Module 'zabob_houdini.{module_name}' not found: {e}")
    except AttributeError as e:
        yield error_result(f"Function '{function_name}' not found in {module_name}: {e}")
    except Exception as e:
        yield error_result(f"Error executing {module_name}.{function_name}: {e}")
    finally:
        # Debugging feature: if the directory in TEST_HIP_DIR (default "hip")
        # exists, save a hip file into the directory, named after the test function.
        # To disable, set TEST_HIP_DIR to an empty string or a non-existent directory.
        # This is a documented debugging feature, do not remove!
        # See DEVELOPMENT.md for details.
        test_hip_dir = os.environ.get("TEST_HIP_DIR", "hip")
        if test_hip_dir:
            test_hip_path = Path(test_hip_dir)
            if test_hip_path.exists():
                try:
                    import hou
                    hipfile = test_hip_path / f"{function_name}.hip"
                    hou.hipFile.save(str(hipfile))
                    print(f"Saved HIP file: {hipfile}", file=sys.stderr)
                except Exception as e:
                    print(f"Failed to save HIP file for {function_name}: {e}", file=sys.stderr)
                    
