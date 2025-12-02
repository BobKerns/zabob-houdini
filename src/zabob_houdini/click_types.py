'''
Parameter types for the click cli library.
'''


from click import Context, ParamType, Parameter
from semver import Version


def _version(version: Version | str) -> Version:
    """
    Convert a version to a semver.Version object.

    Args:
        version (Version|str): The version to convert.

    Returns:
        Version: The converted version.
    """
    if isinstance(version, Version):
        return version
    return Version.parse(version, optional_minor_and_patch=True)


class SemVerParamType(ParamType):
    """Provide a custom click type for semantic versions.

    This custom click type provides validity checks for semantic versions.
    """
    name = 'semver'
    _min_parts: int = 3
    _max_parts: int = 3

    _min_version: Version | None = None
    _max_version: Version | None = None

    def __init__(self,
                 min_parts: int = 3,
                 max_parts: int = 3,
                 min_version: Version | None = None,
                 max_version: Version | None = None,
                 ) -> None:
        """
        Initialize the SemVerParamType.

        :param min_parts: If True, the minor version is optional.
        :type min_parts: int
        :param max_parts: If True, the patch version is optional.
        :type max_parts: int
        :param min_version: The minimum version allowed.
        :type min_version: semver.Version|None
        :param max_version: The maximum version allowed.
        :type max_version: semver.Version|None
        """
        super().__init__()
        self._min_parts = min(min_parts, max_parts)
        self._max_parts = max(max_parts, min_parts)
        self._min_version = min_version
        self._max_version = max_version

    def convert(self,
                value: str,
                param: Parameter | None,
                ctx: Context | None,
                ) -> Version:
        """Converts the value from string into semver type.

        This method takes a string and check if this string belongs to semantic version definition.
        If the test is passed the value will be returned. If not a error message will be prompted.

        :param value: the value passed
        :type value: str
        :param param: the parameter that we declared
        :type param: str
        :param ctx: context of the command
        :type ctx: str
        :return: the passed value as a checked semver
        :rtype: str
        """
        parts = value.count('.') + 1
        if parts > self._max_parts:
            segments = ('major', 'minor', 'patch', 'prerelease', 'build')
            expect = '.'.join(segments[:self._max_parts])
            self.fail(f"Not a valid version, expected at most {expect}", param, ctx)
        elif parts < self._min_parts:
            segments = ('major', 'minor', 'patch', 'prerelease', 'build')
            expect = '.'.join(segments[:self._min_parts])
            self.fail(f"Not a valid version, expected at least {expect}", param, ctx)
        else:
            try:
                result = _version(value)
                if self._min_version and self._max_version:
                    if result > self._max_version or result < self._min_version:
                        self.fail(f"Version {result} is not in range {self._min_version} - {self._max_version}",
                                  param,
                                  ctx)
                if self._min_version and result < self._min_version:
                    self.fail(f"Version {result} is less than minimum version {self._min_version}",
                              param,
                              ctx)
                if self._max_version and result > self._max_version:
                    self.fail(f"Version {result} is greater than maximum version {self._max_version}",
                              param,
                              ctx)
                return result
            except ValueError as e:
                self.fail('Not a valid version, {0}'.format(str(e)), param, ctx)


class OrType(ParamType):
    """A custom click type that accepts multiple types."""
    name = 'or_type'
    _types: tuple[ParamType, ...]

    def __init__(self, *types: ParamType) -> None:
        """
        Initialize the OrType with multiple types.

        :param types: The types to accept.
        """
        super().__init__()
        self._types = types

    def convert(self,
                value: str,
                param: Parameter | None,
                ctx: Context | None,
                ):
        """Convert the value to one of the accepted types."""
        for t in self._types:
            try:
                return t.convert(value, param, ctx)
            except Exception:
                continue
        self.fail(f"Value '{value}' does not match any of the accepted types: {self._types}",
                  param,
                  ctx)


class NoneType(ParamType):
    """A custom click type that accepts None."""
    name = 'none_type'

    def convert(self,
                value: str | None,
                param: Parameter | None,
                ctx: Context | None
                ):
        """Convert the value to None."""
        if value is None:
            return None
        if isinstance(value, str) and value.lower() == 'none':
            return None
        self.fail(f"Value '{value}' is not None", param, ctx)


class OptionalType(ParamType):
    """A custom click type that accepts a value or None."""
    name: str
    _type: ParamType | type

    def __init__(self, type: ParamType | type) -> None:
        """
        Initialize the OptionalType with a specific type.

        :param type: The type to accept.
        """
        super().__init__()
        self._type = type
        name = getattr(type, 'name',
                       getattr(type, '__name__',
                               str(type)))
        self.name = f'Optional[{name}]'

    def convert(self,
                value: str | None,
                param: Parameter | None,
                ctx: Context | None,
                ):
        """Convert the value to None if it is 'None' or empty."""
        if value is None:
            return None
        if isinstance(value, str) and value.lower() == 'none':
            return None
        if hasattr(self._type, 'convert'):
            # If value is already a ParamType, use its convert method
            return self._type.convert(value, param, ctx)
        return self._type(value)
