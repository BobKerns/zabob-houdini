"""
Safe pytest fixtures for Houdini testing.

This version avoids importing anything that could trigger hou imports.
"""

from __future__ import annotations

from collections.abc import Generator
from typing import Protocol
from threading import RLock
import inspect
import os
import pytest
from pathlib import Path
import sys
import subprocess
import json
import shutil

from zabob_houdini.utils import (
    JsonValue, JsonObject, HoudiniResult, Location,
)


class HythonSessionFn(Protocol):
    """A function that can be called to execute a function in the hython environment."""
    def __call__(self, test_func_name: str, *args: JsonValue,
                 module: str = "") -> JsonObject: ...


def fmt_location(name: str, loc: Location | None) -> str:
    if loc is None:
        return ""
    file = str(Path(loc.get("file", "")).relative_to(Path.cwd()))

    line = loc.get("line", 0)
    fn = loc.get("name", "<unknown>")

    return f'{name} "{file}:{line}", in {fn}'


@pytest.fixture
def hython_test(hython_session: HythonSession, request) -> HythonSessionFn:
    """
    Fixture that provides a function to run test functions in hython.

    Uses persistent hython session that starts on first use.
    Returns just the result data, handling success/error internally.
    """
    def run_houdini_test(test_func_name: str, *args: JsonValue,
                         module: str = "") -> JsonObject:
        """Run a test function in hython and return the result data."""

        # If no module specified, determine it from the calling pytest module
        if not module:
            frame = inspect.currentframe()
            try:
                # Walk up the stack to find the calling test module
                if frame is not None:
                    caller_frame = frame.f_back
                    while caller_frame:
                        caller_file = Path(caller_frame.f_code.co_filename)
                        if caller_file.name.startswith('test_') and caller_file.suffix == '.py':
                            # Convert test_foo.py to testing.h_foo
                            pytest_module = caller_file.stem  # e.g., "test_houdini_integration"
                            hython_module = f"testing.h_{pytest_module[5:]}"  # "testing.h_houdini_integration"
                            module = hython_module
                            break
                        caller_frame = caller_frame.f_back

                # Fallback - this shouldn't happen with proper test organization
                if not module:
                    raise ValueError(f"Could not determine module for test function {test_func_name}. "
                                     "Make sure the test is called from a test_*.py file.")
            finally:
                del frame

        try:
            result = hython_session.call_function(test_func_name, *args,
                                                  module=module)
        except RuntimeError as e:
            if "Could not start hython" in str(e):
                pytest.skip("hython not found - Houdini not installed or not in PATH")
            else:
                pytest.fail(f"Hython session error: {e}")
        except Exception as e:
            pytest.fail(f"Hython call failed: {e}")

        # Validate the result structure and extract result data
        if not result['success']:
            heading = f"hython test {test_func_name} failed:"
            error_msg = result.get("error", "Unknown error")
            separator = "------Hython Error Traceback------"
            traceback_info = result.get("traceback", "")
            loc_sep = "------ Location (Test, Step, Error) ------"
            test_loc = fmt_location("Tst>", result.get('test_location'))
            step_loc = fmt_location("Stp>", result.get('step_location'))
            error_loc = fmt_location("Err>", result.get('error_location'))
            error_hdr = error_msg.split('\n', 1)[0]
            error_hdr = f'Error: {error_hdr}'
            msg = "\n".join(
                p for p in (
                    heading, error_msg, "",
                    separator, traceback_info,
                    error_hdr,
                    loc_sep, test_loc, step_loc, error_loc
                )
                if p.strip()
            )
            pytest.fail(msg)

        # At this point we know success=True, so result field must be present
        if "result" not in result:
            pytest.fail("Houdini test did not return a result field")
        print(fmt_location('Tst>', result['test_location']), file=sys.stderr)
        step_loc = result.get('step_location')
        if step_loc:
            print(fmt_location('Stp>', step_loc), file=sys.stderr)
        return result['result']

    return run_houdini_test


class HythonSession:
    """Manages a persistent hython process for the test session."""
    process: subprocess.Popen | None = None
    _started: bool = False
    lock: RLock

    def __init__(self):
        self.lock = RLock()

    def _ensure_started(self) -> bool:
        """Start the hython process if not already started."""
        with self.lock:
            if self._started:
                if self.process and self.process.poll() is None:
                    return True
                # Process died, reset state
                self._started = False
                self.process = None
            hython_path = shutil.which("hython")
            if not hython_path:
                return False
            retries = 3
            for _ in range(retries):
                try:
                    # Set up environment with src directory in PYTHONPATH for testing modules
                    env = os.environ.copy()
                    project_root = Path(__file__).parent.parent
                    src_path = str(project_root / "src")

                    if "PYTHONPATH" in env:
                        env["PYTHONPATH"] = f"{src_path}{os.pathsep}{env['PYTHONPATH']}"
                    else:
                        env["PYTHONPATH"] = src_path

                    self.process = subprocess.Popen(
                        [hython_path, "-m", "zabob_houdini", "_batch_exec"],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        # Pass stderr through for transparency in case of errors
                        stderr=None,
                        text=True,
                        bufsize=1,  # Line buffered
                        env=env
                    )
                    if (
                            self.process.poll() is None
                            and self.process.stdout
                            and self.process.stdin
                            and not self.process.stdout.closed
                            and not self.process.stdin.closed
                            ):
                        self._started = True
                        return True
                except Exception:
                    pass  # Ignore exceptions and retry
            return False

    def call_function(self, func_name: str, *args, module: str) -> HoudiniResult:
        """
        Call a function in the persistent hython process.

        Args:
            func_name: Name of the function to call in the specified module.
            args: Arguments to pass to the function.
            module: Module name where the function is defined.

        Returns:
            A dictionary with the result of the function call, including success status and any returned data.
        """
        with self.lock:
            if not self._ensure_started():
                raise RuntimeError("Could not start hython process")

            if not self.process or not self.process.stdin or not self.process.stdout:
                raise RuntimeError("Process pipes not available")

            request = {
                "module": module,
                "function": func_name,
                "args": [str(arg) for arg in args]
            }

            try:
                # Send request
                request_line = json.dumps(request) + "\n"
                self.process.stdin.write(request_line)
                self.process.stdin.flush()

                # Read response
                if sys.platform == "win32":
                    # On windows, select does not work with pipes, so we just accept
                    # the possibility of a test hanging. If it becomes a problem,
                    # test under WSL.
                    pass
                else:
                    # Set timeout (e.g., 30 seconds)
                    timeout = 30
                    from select import select
                    ready, _, _ = select([self.process.stdout], [], [], timeout)
                    if not ready:
                        self.close()
                        raise RuntimeError("Timeout waiting for response from hython process")
                response_line = self.process.stdout.readline().strip()
                if not response_line:
                    self.close()
                    raise RuntimeError("No response from hython process")

                try:
                    return json.loads(response_line)
                except json.JSONDecodeError as e:
                    self.close()
                    raise RuntimeError(f"Invalid JSON response from hython process: {response_line[:100]}") from e
            except IOError as e:
                self.close()  # Ensure we clean up the process on error so we start fresh next time
                raise RuntimeError(f"Error communicating with hython process: {e}") from e

    def close(self):
        """Close the hython process."""
        with self.lock:
            if self.process:
                try:
                    if self.process.stdin:
                        self.process.stdin.close()
                    self.process.terminate()
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    try:
                        self.process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        pass  # Process did not terminate, but we tried our best
                except Exception:
                    pass  # Best effort cleanup
                finally:
                    self.process = None
                    self._started = False


@pytest.fixture(scope="session")
def hython_session() -> Generator[HythonSession, None, None]:
    """Session-scoped fixture for persistent hython process."""
    session = HythonSession()
    yield session
    session.close()


@pytest.fixture
def houdini_available() -> bool:
    """Check if we're running in hython environment."""
    executable = Path(sys.executable).name.lower()
    return 'hython' in executable or 'houdini' in executable


@pytest.fixture(scope="session", autouse=True)
def clean_houdini_environment():
    """Clean environment for all tests to avoid Houdini startup noise."""
    minimal_keys = {'PATH', 'TERM', 'HOME', 'USER', 'TMPDIR', 'TEMP', 'TMP'}

    # Store original env
    original_env = os.environ.copy()

    # Clear and set minimal env
    os.environ.clear()
    for key in minimal_keys:
        if key in original_env:
            os.environ[key] = original_env[key]

    yield

    # Restore (optional, since tests end anyway)
    os.environ.clear()
    os.environ.update(original_env)
