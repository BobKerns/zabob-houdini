"""
Bridge for running code in hython subprocess when not already in hython.
"""

import inspect
import pickle
import subprocess
import sys
import shutil
import tempfile
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])


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


def get_houdini_function(func_name: str) -> Callable:
    """
    Get a Houdini function safely, only when in hython environment.

    Args:
        func_name: Name of the function in houdini_functions module

    Returns:
        The function from houdini_functions module

    Raises:
        RuntimeError: If not in hython environment
    """
    if not _is_in_houdini():
        raise RuntimeError("Houdini functions only available in hython environment")

    from . import houdini_functions
    return getattr(houdini_functions, func_name)


def in_hython(func: F) -> F:  # type: ignore
    """
    Decorator that ensures function runs in hython environment.

    If already in hython, calls the corresponding function from houdini_functions module.
    Otherwise, executes that function in hython subprocess.

    The decorated function should have a corresponding function with the same name
    in the houdini_functions module.

    Args:
        func: Function to run in hython (used only for name and signature)

    Returns:
        Decorated function that automatically handles hython execution

    Example:
        @in_hython
        def create_box():
            pass  # Implementation is in houdini_functions.create_box()
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__

        if _is_in_houdini():
            # Already in hython, get and call the function safely
            houdini_func = get_houdini_function(func_name)
            return houdini_func(*args, **kwargs)

        # Not in hython, execute in subprocess
        return _run_function_in_hython_subprocess(func_name, args, kwargs)

    return cast(F, wrapper)


def _run_function_in_hython_subprocess(func_name: str, args: tuple, kwargs: dict) -> Any:
    """Execute function from houdini_functions module in hython subprocess."""
    hython_path = _find_hython()

    script_content = f'''
import pickle
import sys
from pathlib import Path

# Add the project to Python path so imports work
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

# Also add current working directory for development
import os
sys.path.insert(0, os.getcwd())

# Load arguments
with open(sys.argv[1], 'rb') as f:
    args, kwargs = pickle.load(f)

# Execute function from houdini_functions module
try:
    from zabob_houdini import houdini_functions
    func = getattr(houdini_functions, "{func_name}")
    result = func(*args, **kwargs)
    # Save result
    with open(sys.argv[2], 'wb') as f:
        pickle.dump(('success', result), f)
except Exception as e:
    # Save error
    with open(sys.argv[2], 'wb') as f:
        pickle.dump(('error', str(e), type(e).__name__), f)
'''

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Write script file
        script_file = temp_path / "hython_script.py"
        script_file.write_text(script_content)

        # Write arguments file
        args_file = temp_path / "args.pkl"
        with open(args_file, 'wb') as f:
            pickle.dump((args, kwargs), f)

        # Prepare result file
        result_file = temp_path / "result.pkl"

        # Execute in hython
        try:
            subprocess.run([
                hython_path, str(script_file), str(args_file), str(result_file)
            ], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"hython execution failed: {e.stderr}")

        # Read result
        if not result_file.exists():
            raise RuntimeError("hython script did not produce result file")

        with open(result_file, 'rb') as f:
            result_data = pickle.load(f)

        if result_data[0] == 'success':
            return result_data[1]
        else:
            # Re-raise the original exception type if possible
            error_msg, error_type = result_data[1], result_data[2]
            if error_type in dir(__builtins__):
                exception_class = getattr(__builtins__, error_type)
                raise exception_class(error_msg)
            else:
                raise RuntimeError(f"{error_type}: {error_msg}")


def run_hython_script(script: str) -> Any:
    """
    Run a script string in hython.

    Args:
        script: Python code to execute in hython

    Returns:
        Result of script execution
    """
    if _is_in_houdini():
        # Already in hython, execute directly
        local_vars = {}
        exec(script, {"__builtins__": __builtins__}, local_vars)
        return local_vars.get('result')

    # Execute in subprocess
    hython_path = _find_hython()

    script_content = f'''
import sys
from pathlib import Path

# Add the project to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

# Execute the script
{script}

# Save result if it exists
try:
    import pickle
    with open(sys.argv[1], 'wb') as f:
        pickle.dump(('success', locals().get('result')), f)
except Exception as e:
    with open(sys.argv[1], 'wb') as f:
        pickle.dump(('error', str(e), type(e).__name__), f)
'''

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Write script file
        script_file = temp_path / "hython_script.py"
        script_file.write_text(script_content)

        # Prepare result file
        result_file = temp_path / "result.pkl"

        # Execute in hython
        try:
            subprocess.run([
                hython_path, str(script_file), str(result_file)
            ], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"hython execution failed: {e.stderr}")

        # Read result
        if result_file.exists():
            with open(result_file, 'rb') as f:
                result_data = pickle.load(f)

            if result_data[0] == 'success':
                return result_data[1]
            else:
                error_msg, error_type = result_data[1], result_data[2]
                raise RuntimeError(f"{error_type}: {error_msg}")

        return None
