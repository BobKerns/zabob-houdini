'''
Utility functions and types.
'''

from typing import NotRequired, TypeAlias, TypedDict, Any
import json
import sys


JsonAtomicValue: TypeAlias = str | int | float | bool | None
'''An atomic JSON value, such as a string, number, boolean, or null.'''
JsonArray: TypeAlias = 'list[JsonValue]'
'''A JSON array, which is a list of JSON values.'''
JsonObject: TypeAlias = 'dict[str, JsonValue]'
'''A JSON object, which is a dictionary with string keys and JSON values.'''
JsonValue: TypeAlias = 'JsonAtomicValue | JsonArray | JsonObject'
'''A JSON value, which can be an atomic value, array, or object.'''


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
