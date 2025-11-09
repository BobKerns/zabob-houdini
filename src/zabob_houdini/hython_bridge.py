"""
Bridge for running code in hython subprocess when not already in hython.
"""

import inspect
import pickle
import subprocess
import sys
import tempfile
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


def _is_in_hython() -> bool:
    """Check if we're currently running in hython."""
    try:
        import hou
        return hasattr(hou, 'applicationName') and hou.applicationName() == 'hython'
    except ImportError:
        return False


def _find_hython() -> str:
    """Find hython executable."""
    # Try common locations
    possible_paths = [
        "/Applications/Houdini/Houdini20.5.370/Frameworks/Houdini.framework/Versions/20.5/Resources/bin/hython",
        "/opt/hfs20.5/bin/hython",
        "hython"  # Hope it's in PATH
    ]

    for path in possible_paths:
        if Path(path).exists() or path == "hython":
            return path

    raise RuntimeError("hython executable not found. Please ensure Houdini is installed.")


def in_hython(func: F) -> F:  # type: ignore
    """
    Decorator that ensures function runs in hython environment.

    If already in hython, runs directly. Otherwise, executes in hython subprocess.

    Args:
        func: Function to run in hython

    Returns:
        Decorated function that automatically handles hython execution

    Example:
        @in_hython
        def create_box():
            import hou
            geo = hou.node("/obj").createNode("geo")
            box = geo.createNode("box")
            return box.path()
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if _is_in_hython():
            # Already in hython, run directly
            return func(*args, **kwargs)

        # Not in hython, execute in subprocess
        return _run_in_hython_subprocess(func, args, kwargs)

    return wrapper


def _run_in_hython_subprocess(func: Callable, args: tuple, kwargs: dict) -> Any:
    """Execute function in hython subprocess."""
    hython_path = _find_hython()

    # Get function source and prepare execution script
    func_source = inspect.getsource(func)
    func_name = func.__name__

    # Clean up the function source - remove decorator and fix indentation
    func_lines = func_source.strip().split('\n')

    # Remove @in_hython decorator if present
    clean_lines = []
    for line in func_lines:
        if not line.strip().startswith('@in_hython'):
            clean_lines.append(line)

    # Find the function definition and normalize indentation
    func_def_indent = 0
    for line in clean_lines:
        if line.strip().startswith('def '):
            func_def_indent = len(line) - len(line.lstrip())
            break

    # Remove the base indentation
    normalized_lines = []
    for line in clean_lines:
        if line.strip():  # Skip empty lines for indentation calculation
            if len(line) - len(line.lstrip()) >= func_def_indent:
                normalized_lines.append(line[func_def_indent:])
            else:
                normalized_lines.append(line)
        else:
            normalized_lines.append('')

    clean_func_source = '\n'.join(normalized_lines)

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

# Define the function
{clean_func_source}

# Load arguments
with open(sys.argv[1], 'rb') as f:
    args, kwargs = pickle.load(f)

# Execute function
try:
    result = {func_name}(*args, **kwargs)
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
    if _is_in_hython():
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
