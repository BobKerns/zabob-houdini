"""Text utilities module (hou.text)."""

def compareVersionString(str1: str, str2: str) -> int:
    """
    Compares two version strings which have numbered components separated by dots (eg X.Y.Z).

    Returns negative if str1 < str2, zero if equal, positive if str1 > str2.
    """
    ...

def decode(str: str) -> str:
    """
    Decode a Houdini-encoded string back to its original form.

    Houdini VEX variable names are only allowed to contain letters, numbers, and
    underscores, and must not begin with a number.
    """
    ...

def encode(str: str) -> str:
    """
    Encode a string for use as a Houdini VEX variable name.

    Houdini VEX variable names are only allowed to contain letters, numbers, and
    underscores, and must not begin with a number.
    """
    ...

def decodeAttrib(str: str) -> str:
    """
    Decode a Houdini-encoded attribute name back to its original form.

    Houdini geometry attributes and group names are only allowed to contain letters,
    numbers, and underscores, and must not begin with a number.
    """
    ...

def encodeAttrib(str: str) -> str:
    """
    Encode a string for use as a Houdini attribute name.

    Houdini geometry attributes and group names are only allowed to contain letters,
    numbers, and underscores, and must not begin with a number.
    """
    ...

def decodeParm(str: str) -> str:
    """
    Decode a Houdini-encoded parameter name back to its original form.

    Houdini parameter names are only allowed to contain letters, numbers, hash
    characters (for multiparms), and underscores, and must not begin with a number.
    """
    ...

def encodeParm(str: str) -> str:
    """
    Encode a string for use as a Houdini parameter name.

    Houdini parameter names are only allowed to contain letters, numbers, hash
    characters (for multiparms), and underscores, and must not begin with a number.
    """
    ...

def expandString(str: str, expand_tilde: bool = True) -> str:
    """
    Expands global variables in the expression.
    """
    ...

def expandStringAtFrame(str: str, frame_number: float, expand_tilde: bool = True) -> str:
    """
    Expands global variables in the expression at a specific frame.
    """
    ...

def expandHuskFilePath(str: str, frame_start: float = 1.0, frame_inc: float = 1.0, frame_idx: int = 0) -> str:
    """
    Expands global variables in the expression using the same formatting supported
    by husk to evaluate time varying file paths.
    """
    ...

def incrementNumberedString(str: str) -> str:
    """
    If the string ends with a number, that number is incremented, and the resulting
    new string is returned.
    """
    ...

def alphaNumeric(str: str) -> str:
    """
    Return a string that consists of only numbers, letters, and underscores.
    """
    ...

def variableName(str: str, safe_chars: str = "") -> str:
    """
    Returns a string that is valid to use as a variable or node name.
    """
    ...

def abspath(path: str, base_path: str | None = None) -> str:
    """
    Returns the supplied path converted to an absolute path.
    """
    ...

def relpath(path: str, base_path: str | None = None, allow_relative_path_from_root: bool = True) -> str:
    """
    Returns the supplied path converted to a relative path, expressed as relative to
    the directory specified by base_path.
    """
    ...

def normpath(path: str) -> str:
    """
    Returns a normalized version of the supplied path.
    """
    ...

def collapseCommonVars(path: str, vars: list[str] = ['$HIP', '$JOB']) -> str:
    """
    Tests if the path starts with the expanded form of any variable passed in
    through the provided vars list.
    """
    ...

def oclExtractBindings(code: str) -> tuple[dict, ...]:
    """
    Parses provided OpenCL code for #bind commands and returns the set of bindings
    specified.
    """
    ...

def oclExtractRunOver(code: str) -> str:
    """
    Parses provided OpenCL code for #runover commands and returns the runover
    specified.
    """
    ...

def patternMatch(pattern_string: str, input_string: str, ignore_case: bool = False, path_match: bool = False) -> bool:
    """
    This function is case-sensitive by default.

    Matches input_string against pattern_string using Houdini pattern matching syntax.
    """
    ...

def patternRename(input_string: str, pattern_find: str, pattern_replace: str) -> str:
    """
    This function finds the pattern given in pattern_find and replaces any
    occurrences with the pattern given in pattern_replace.
    """
    ...
