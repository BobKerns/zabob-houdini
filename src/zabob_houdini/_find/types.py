from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Sequence
from semver import Version
import re


_RE_DIR_NAME = re .compile (r'^(?:Houdini ?)(\d+\.\d+(?:\.\d+)?)$', re.IGNORECASE)

###
# Note to Copilot:
# For future reference, note that while python technically does not deal with
# attribute docstrings at all, tools such as pylance and various doc generators do.
# Notably, IDEs such as VSCode will use these docstrings to provide mouse-over
# tooltips and other helpful information about the attributes.
# This is why we use them here, even though they are discarded at runtime.
# While I could probably use dataclass field metadata to achieve the same effect,
# I have not tested it, and the extra complexity brings no benefit.
#
# Note to developers, who may have been referred here by bad advice from Copilot:
# If you add a new attribute to HoudiniInstall, please also add a docstring
# to the attribute, as this will help with documentation and IDE support.
# It is required to begin on the vary next line. It cannot be computed,
# it must be a literal string.

@dataclass
class HoudiniInstall:
    """Information about a Houdini installation."""
    houdini_version: Version
    'The version of this Houdini installation, e.g., 20.5.584'
    python_version: Version
    'The version of python used by this houdini installation.'
    version_dir: Path
    'The root of the houdini installation, specific to version'
    bin_dir: Path
    "${HB}: Houdini's bin directory, containing executables like houdini, hython, etc."
    hfs_dir: Path
    "${HFS}: Houdini's built-in types, scripts, extensions, and more."
    hython: Path
    'Path to the hython executable'
    hdso_libs: Path
    "${HDSO}: Houdini's shared libraries directory, containing .so/.dynld/.dll files"
    python_libs: Path
    '${HHP}: # Houdini Python library directory'
    hh_dir: Path
    '${HH}'
    config_dir: Path
    '${HHC}'
    toolkit_dir: Path
    '${HHT}: Houdini toolkit directory'
    sbin_dir: Path
    "${HHS}: Houdini's sbin directory, containing system binaries like sesinetd"
    lib_paths: Sequence[Path]
    'Additional library paths for Houdini, e.g., for plugins or custom libraries'
    env_path: Sequence[Path]
    'Additional entries to add to the PATH environment variable'
    exec_prefix: Path  # Python executable prefix directory
    app_paths: dict[str, Path] # application installation directories

    def __repr__(self) -> str:
        return f"HoudiniInstall({self.houdini_version}, {self.python_version})"

def _version(version: str|Version) -> Version:
    """Convert version string to semver.Version object."""
    if isinstance(version, Version):
        return version
    return Version.parse(version, True)

# Add other shared utility functions
def _get_houdini_version(name_hint: str) -> Version:
    """
    Extract Houdini version from directory name.

    Note: hython does not report the version of Houdini, only Python."""

    m = _RE_DIR_NAME.match(name_hint)
    if m:
        # Extract version from app name
        version_str = m.group(1)
        return _version(version_str)
    return Version(0)

def _get_major_minor(version: str|Version) -> Version:
    """Extract major.minor version from full version string."""
    v = _version(version)
    return Version(v.major, v.minor)  # Set patch and pre-release to zero

def _group_by_major_minor(
    installations: dict[Version, HoudiniInstall]
) -> dict[Version, list[HoudiniInstall]]:
    """Group installations by major.minor version."""
    def by_major_minor(a: dict[Version, list[HoudiniInstall]], i: HoudiniInstall) -> dict[Version, list[HoudiniInstall]]:
        major_minor = _get_major_minor(i.houdini_version)
        a[major_minor].append(i)
        return a
    return reduce(by_major_minor,
                installations.values(),
                defaultdict(list))


def _if_exists(path: Path, suffix: str|None = None):
    """
    Check if the path exists.

    Args:
    The path to check.
    suffix: Optional suffix to add to the path.

    Yields:
    The path if it exists, otherwise nothing.
    """
    if suffix is not None:
        path = path.with_suffix(suffix)
    if path.exists():
        yield path


def _parse_pyversion(path: Path) -> Iterable[Version]:
    """
    Parse Python version from library directory name.

    Args:
    path: The path to check.
    Yields:
    A tuple of Python version and the path, if it matches the pattern.
    """
    py_match = re.match(r'^python(\d+\.\d+)libs$', path.name, re.IGNORECASE)
    if py_match:
        yield _version(py_match.group(1))
