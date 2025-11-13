'''
Utility functions and types.
'''

from typing import TypeAlias


JsonAtomicValue: TypeAlias = str | int | float | bool | None
'''An atomic JSON value, such as a string, number, boolean, or null.'''
JsonArray: TypeAlias = 'list[JsonValue]'
'''A Json array, which is a list of JSON values.'''
JsonObject: TypeAlias = 'dict[str, JsonValue]'
'''A Json object, which is a dictionary with string keys and JSON values.'''
JsonValue: TypeAlias = 'JsonAtomicValue | JsonArray | JsonObject'
'''A Json value, which can be an atomic value, array, or object.'''
