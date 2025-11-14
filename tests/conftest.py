"""
Safe pytest fixtures for Houdini testing.

This version avoids importing anything that could trigger hou imports.
"""

from collections.abc import Generator
from typing import Protocol
from threading import RLock
import pytest
from pathlib import Path
import sys
import subprocess
import json
import shutil

from zabob_houdini.utils import JsonValue, HoudiniResult


class HythonSessionFn(Protocol):
    """A function that can be called to execute a function in the hython environment."""
    def __call__(self, test_func_name: str, *args: JsonValue,
                 module: str = "houdini_test_functions") -> HoudiniResult: ...


@pytest.fixture
def hython_test(hython_session: 'HythonSession') -> HythonSessionFn:
    """
    Fixture that provides a function to run test functions in hython.

    Uses persistent hython session that starts on first use.
    """
    def run_houdini_test(test_func_name: str, *args: JsonValue,
                         module: str = "houdini_test_functions") -> HoudiniResult:
        """Run a test function in hython and validate the result."""
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

        # Validate the result structure
        if not result['success']:
            error_msg = result.get("error", "Unknown error")
            traceback_info = result.get("traceback", "")
            pytest.fail(f"Houdini test failed: {error_msg}\n{traceback_info}")

        return result

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
                    self.process = subprocess.Popen(
                        [hython_path, "-m", "zabob_houdini", "_batch_exec"],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        # Pass stderr through for transparency in case of errors
                        stderr=None,
                        text=True,
                        bufsize=1  # Line buffered
                    )
                    if (self.process.poll() is None
                        and self.process.stdout
                        and self.process.stdin
                        and not self.process.stdout.closed
                        and not self.process.stdin.closed
                        ):
                            self._started = True
                            return True
                except Exception:
                    pass # Ignore exceptions and retry
            return False

    def call_function(self, func_name: str, *args, module: str = "houdini_test_functions") -> HoudiniResult:
        """
        Call a function in the persistent hython process.

        Args:
            func_name: Name of the function to call in the specified module.
            args: Arguments to pass to the function.
            module: Module name where the function is defined (default "houdini_test_functions").

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
