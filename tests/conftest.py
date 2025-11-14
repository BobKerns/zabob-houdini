"""
Safe pytest fixtures for Houdini testing.

This version avoids importing anything that could trigger hou imports.
"""

import pytest
from pathlib import Path
import sys
import subprocess
import json
import shutil


@pytest.fixture
def hython_test(hython_session):
    """
    Fixture that provides a function to run test functions in hython.

    Uses persistent hython session that starts on first use.
    """
    def run_houdini_test(test_func_name: str, *args):
        """Run a test function in hython and validate the result."""
        try:
            result = hython_session.call_function(test_func_name, *args)
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

    def __init__(self):
        self.process: subprocess.Popen | None = None
        self._started = False

    def _ensure_started(self):
        """Start the hython process if not already started."""
        if self._started and self.process and self.process.poll() is None:
            return True

        hython_path = shutil.which("hython")
        if not hython_path:
            return False

        try:
            self.process = subprocess.Popen(
                [hython_path, "-m", "zabob_houdini", "_batch_exec"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=None,
                text=True,
                bufsize=1  # Line buffered
            )
            self._started = True
            return True
        except Exception:
            return False

    def call_function(self, func_name: str, *args, module: str = "houdini_test_functions"):
        """Call a function in the persistent hython process."""
        if not self._ensure_started():
            raise RuntimeError("Could not start hython process")

        if not self.process or not self.process.stdin or not self.process.stdout:
            raise RuntimeError("Process pipes not available")

        request = {
            "module": module,
            "function": func_name,
            "args": [str(arg) for arg in args]
        }

        # Send request
        request_line = json.dumps(request) + "\n"
        self.process.stdin.write(request_line)
        self.process.stdin.flush()

        # Read response
        # TODO: Add timeout handling here to avoid hanging tests if hython process becomes unresponsive
        # On timeout, kill the process and raise an error
        response_line = self.process.stdout.readline().strip()
        if not response_line:
            raise RuntimeError("No response from hython process")

        try:
            return json.loads(response_line)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON response from hython process: {response_line[:100]}") from e

    def close(self):
        """Close the hython process."""
        if self.process:
            try:
                if self.process.stdin:
                    self.process.stdin.close()
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            except Exception:
                pass  # Best effort cleanup
            self.process = None
        self._started = False


@pytest.fixture(scope="session")
def hython_session():
    """Session-scoped fixture for persistent hython process."""
    session = HythonSession()
    yield session
    session.close()


@pytest.fixture
def houdini_available():
    """Check if we're running in hython environment."""
    executable = Path(sys.executable).name.lower()
    return 'hython' in executable or 'houdini' in executable
