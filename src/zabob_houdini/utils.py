'''
Utility functions and types.
'''

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from typing import (
    Hashable, NotRequired, TypeAlias, TypedDict,
    Any, TypeVar, Generic, cast, overload,
)
from types import MappingProxyType
from collections.abc import Callable
import json
import sys
import traceback
from pathlib import Path


K = TypeVar('K', bound=Hashable)
V = TypeVar('V')
D = TypeVar('D')


class HashableMapping(Generic[K, V]):
    """
    A hashable immutable mapping for use in frozen dataclasses.

    Wraps a MappingProxyType and provides hash functionality.
    """

    _mapping: MappingProxyType[K, V]

    def __init__(self, mapping: dict[K, V] | None = None):
        self._mapping = MappingProxyType(mapping or {})

    def __hash__(self) -> int:
        """Hash based on sorted items for consistent hashing."""
        return hash(tuple(sorted(self._mapping.items())))

    def __eq__(self, other: object) -> bool:
        """Equality based on underlying mapping."""
        if isinstance(other, HashableMapping):
            return self._mapping == other._mapping
        return self._mapping == other

    def __getitem__(self, key: K) -> Any:
        return self._mapping[key]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self) -> int:
        return len(self._mapping)

    @overload
    def get(self, key: K) -> V | None: ...

    @overload
    def get(self, key: K, default: D) -> V | D: ...

    def get(self, key: K, default: D | None = None) -> V | D | None:
        return self._mapping.get(key, default)

    def items(self):
        return self._mapping.items()

    def keys(self):
        return self._mapping.keys()

    def values(self):
        return self._mapping.values()


# ============================================================================
# JSON and Houdini Result Types
# ============================================================================
# WARNING: These type definitions are duplicated in tests/conftest.py to avoid
# WARNING: importing zabob_houdini into the pytest environment.
# WARNING: Keep both copies synchronized when making changes!
# ============================================================================

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
    test_location: Location | None
    error: NotRequired[str]
    traceback: NotRequired[str]
    error_location: NotRequired[Location | None]
    step_location: NotRequired[Location | None]

# ============================================================================
# End of duplicated type definitions
# ============================================================================


def frame_location(frame: traceback.FrameSummary) -> Location:
    """Convert a traceback FrameSummary to a Location dict."""
    return Location(
        file=frame.filename,
        name=frame.name,
        line=frame.lineno or 0,
    )


_excluded_frames = {
    "invoke_houdini_function",
    "_exec",
    "_batch_exec",
    "_run_test",
    "filtered_stack",
    'custom_getattr',
    'get_symbol',
}


_excluded_file_suffixes = {
    "/houdini_bridge.py",
    "/conftest.py",
    "/houdini_dev.py",
    ">",
    "__main__.py",
    "/click/core.py",
    "/contextlib.py",
    "/dyn_import.py",
}


def exclude_traceback(*, function: str | None = None,
                      filename: str | None = None,
                      ):
    '''
    Exclude a function or a file from tracebacks.
    If neither a function name nor a filename are provided,
    it will use the filename of the caller.

    Filenames are matched at the end. Typically, this
    will be something like: "/houdini_bridge.py",
    with a leading slash to match the entire filename.
    '''
    if function is None and filename is None:
        tb = sys.exc_info()[2]
        if tb is not None:
            stack = traceback.extract_tb(tb)
        else:
            stack = traceback.extract_stack()[:-1]
        caller_frame = stack[-1]
        filename = caller_frame.filename
    if function is not None:
        _excluded_frames.add(function)
    if filename is not None:
        _excluded_file_suffixes.add(filename)


def current_stack() -> list:
    """Get the current traceback object."""
    try:
        raise Exception()
    except Exception as e:
        tb = e.__traceback__
        if tb is not None and tb.tb_frame is not None:
            return traceback.extract_stack(e.__traceback__.tb_frame)[:-1]  # type: ignore
        return traceback.extract_stack()[:-1]


def stack_filter(frame: traceback.FrameSummary) -> bool:
    """Filter function for stack frames."""
    if frame.name in _excluded_frames:
        return False
    if any(frame.filename.endswith(sfx) for sfx in _excluded_file_suffixes):
        return False
    return True


def filtered_stack(ex: Exception | None = None) -> tuple[
        Location | None,
        Location | None,
        list[traceback.FrameSummary]
        ]:  # noqa: E123
    """Get the current stack, filtering out internal frames."""
    stack: list[traceback.FrameSummary] | None = None
    if ex is not None:
        tb = ex.__traceback__
        if tb is not None and tb.tb_frame is not None:
            stack = traceback.extract_tb(tb)
    if stack is None:
        stack = current_stack()
    filtered = [frame for frame in stack if stack_filter(frame)]
    excluded = [frame for frame in stack if not stack_filter(frame)]
    for frame in excluded:
        frame.lineno = 0
    error_location = frame_location(filtered[-1]) if filtered else None
    test_location = frame_location(filtered[0]) if filtered else None

    return error_location, test_location, filtered


def error_result(message: str | None = None, /, *,
                 _error: Exception | None = None,
                 _func: Callable | None = None,
                 ) -> HoudiniResult:
    """Helper to create an error result."""
    message = message or str(_error)
    error_location, test_location, stack = filtered_stack(_error)
    step_location: Location | None = None
    if _func:
        test_location = get_test_location(_func)
        step_location = get_call_location(stack, _func)
    formatted = traceback.format_list(stack)
    traceback_str = ''.join(formatted)
    return HoudiniResult(
        success=False,
        error=message,
        traceback=traceback_str,
        error_location=error_location,
        test_location=test_location,
        step_location=step_location,
    )


def get_test_location(func: Callable) -> Location:
    return Location(
        file=func.__code__.co_filename,
        name=func.__name__,
        line=func.__code__.co_firstlineno
    )


def get_call_location(stack: list[traceback.FrameSummary], func: Callable) -> Location | None:
    """Get the location within the test."""
    for s in stack:
        if s.name == func.__name__:
            return Location(
                file=s.filename,
                name=s.name,
                line=s.lineno or 0,)
    return None


def success_result(result: 'JsonObject | None' = None, /, *,
                   _func: Callable,
                   **params) -> HoudiniResult:
    return HoudiniResult(
        success=True,
        result=result or params,
        test_location=get_test_location(_func),
    )


def encapsulate_result(result: JsonValue) -> JsonObject:
    match result:
        case str():
            return {
                'message': result
            }
        case int() | float() | bool() | list():
            return {'value': result}
        case tuple():
            return {'value': list(result)}
        case Path():
            return {'path': str(result)}
        case dict() if _is_houdini_success(result):
            return cast(JsonObject, result['result'])
        case dict() if _is_houdini_result(result):
            raise RuntimeError(f'Cannot encapsulate an error as success: {result}')
        case dict():
            return result
        case _:
            return {}


def write_success_result(result: 'JsonObject | None' = None, /, *,
                         _func: Callable, indent: bool = False) -> None:
    """Helper to write a successful HoudiniResult to stdout as JSON."""
    success_response = success_result(result, _func=_func)
    write_response(success_response, indent=indent)


def write_response(result: HoudiniResult, indent: bool = False) -> None:
    """Helper to write a HoudiniResult to stdout as JSON."""
    json.dump(result, sys.stdout, indent=2 if indent else None)
    sys.stdout.write('\n')
    sys.stdout.flush()


def write_error_result(message: str,
                       error: Exception | None = None,
                       func: Callable | None = None,
                       indent: bool = False,
                       ) -> None:
    """Helper to write an error result to stdout as JSON."""
    error_response = error_result(message,
                                  _error=error,
                                  _func=func)
    write_response(error_response, indent=indent)


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


def _is_houdini_success(result: Any) -> bool:
    """Check if the result is a successful HoudiniResult."""
    if not _is_houdini_result(result):
        return False
    return result['success']


T = TypeVar('T')


def check(_type: type[T], value: Any) -> T:
    """Check that the module is loaded correctly."""
    if not isinstance(value, _type):
        raise TypeError(f"Expected value of type {_type}, got {type(value)}")
    return cast(T, value)


def ignore(*_: Any) -> None:
    """
    Utility function to ignore values.

    This function explicitly ignores the given values, which can be useful
    to indicate that certain variables or return values are intentionally
    unused, helping to avoid linter warnings or improve code readability.

    Why have them at all if they are ignored?

    * It makes them available in the debugger for inspection.
    * It documents the intent that these values are intentionally unused.
    * It provides a clear name for values in unit tests, for example.
        * Tests that are expected to raise exception.
    * IDE tools can more easily navigate to the variable definitions.

    Args:
        *_: Any values to ignore
    """
    pass
