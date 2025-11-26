'''
Utility functions and types.
'''

from typing import NotRequired, TypeAlias, TypedDict, Any
from types import MappingProxyType
import json
import sys
import traceback


class HashableMapping:
    """
    A hashable immutable mapping for use in frozen dataclasses.

    Wraps a MappingProxyType and provides hash functionality.
    """

    def __init__(self, mapping: dict[str, Any] | None = None):
        self._mapping = MappingProxyType(mapping or {})

    def __hash__(self) -> int:
        """Hash based on sorted items for consistent hashing."""
        return hash(tuple(sorted(self._mapping.items())))

    def __eq__(self, other: object) -> bool:
        """Equality based on underlying mapping."""
        if isinstance(other, HashableMapping):
            return self._mapping == other._mapping
        return self._mapping == other

    def __getitem__(self, key: str) -> Any:
        return self._mapping[key]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self) -> int:
        return len(self._mapping)

    def get(self, key: str, default: Any = None) -> Any:
        return self._mapping.get(key, default)

    def items(self):
        return self._mapping.items()

    def keys(self):
        return self._mapping.keys()

    def values(self):
        return self._mapping.values()


JsonAtomicValue: TypeAlias = str | int | float | bool | None
'''An atomic JSON value, such as a string, number, boolean, or null.'''
JsonArray: TypeAlias = 'list[JsonValue]'
'''A JSON array, which is a list of JSON values.'''
JsonObject: TypeAlias = 'dict[str, JsonValue]'
'''A JSON object, which is a dictionary with string keys and JSON values.'''
JsonValue: TypeAlias = 'JsonAtomicValue | JsonArray | JsonObject'
'''A JSON value, which can be an atomic value, array, or object.'''


class Location(TypedDict):
    """Location information for errors."""
    file: str
    name: str
    line: int

class HoudiniResult(TypedDict):
    """Result structure from Houdini function calls."""
    success: bool
    result: NotRequired[JsonObject]
    test_location: Location
    error: NotRequired[str]
    traceback: NotRequired[str]
    error_location: NotRequired[Location | None]

def frame_location(frame: traceback.FrameSummary) -> Location:
    """Convert a traceback FrameSummary to a Location dict."""
    return {
        'file': frame.filename,
        'name': frame.name,
        'line': frame.lineno or 9
    }

def test_location(stack: traceback.StackSummary, skip: int = 1) -> Location:
    i: int = len(stack) - skip
    frame = stack[i - 1]
    error_location: Location = frame_location(frame)
    while i > 0:
        if frame is None:
            break
        old_frame = frame
        if (frame.name == "invoke_houdini_function"
            or frame.filename.endswith("houdini_bridge.py")
            or frame.filename.endswith("conftest.py")
        ):
            frame = old_frame
            break
        i -= 1
    i = max(i, len(stack) - 1) - 1
    frame = stack[i + 1]
    return frame_location(frame)

def error_result(message: str, with_traceback: bool = True) -> HoudiniResult:
    """Helper to create an error result."""
    trace = traceback.format_exc().splitlines()
    tb = sys.exc_info()[2]
    stack = traceback.extract_tb(tb)
    error_location: Location = frame_location(stack[-1])
    test_loc: Location  = test_location(stack)
    if not with_traceback:
        return {
            'success': False,
            'error': message,
            'test_location': test_loc,
        }
    return {
        'success': False,
        'error': message,
        'traceback': '\n'.join(trace),
        'error_location': error_location,
        'test_location': test_loc,
    }


def write_response(result: HoudiniResult) -> None:
    """Helper to write a HoudiniResult to stdout as JSON."""
    json.dump(result, sys.stdout)
    sys.stdout.write('\n')
    sys.stdout.flush()


def write_error_result(message: str) -> None:
    """Helper to write an error result to stdout."""
    error_response = error_result(message, True)
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
