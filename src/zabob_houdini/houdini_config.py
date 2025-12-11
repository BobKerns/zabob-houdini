"""
Houdini configuration utilities.
"""

from __future__ import annotations, _dynamic_import # noqa: F407 E261 # type: ignore


import subprocess
import shutil
from pathlib import Path


def find_houdini_pref_dir() -> Path | None:
    """
    Find Houdini user preferences directory using hconfig.

    Returns:
        Path to HOUDINI_USER_PREF_DIR or None if not found
    """
    hython = shutil.which("hython")
    if not hython:
        return None

    try:
        result = subprocess.run([
            hython, "-c", "print(hou.expandString('$HOUDINI_USER_PREF_DIR'))"
        ], capture_output=True, text=True, check=True)
        pref_dir = result.stdout.strip()
        print(f"Pref dir: {pref_dir}")
        if pref_dir:
            return Path(pref_dir)
    except subprocess.CalledProcessError:
        return None


def find_houdini_package_dirs() -> list[Path]:
    """
    Find Houdini package directories where we can install packages.

    Returns:
        List of writable package directory paths
    """
    package_dirs = []

    # Try user preferences directory first (most likely to be writable)
    pref_dir = find_houdini_pref_dir()
    if pref_dir:
        user_packages = pref_dir / "packages"
        package_dirs.append(user_packages)

    # Could add more locations here if needed
    # e.g., site-wide package directories

    return package_dirs


def ensure_houdini_package_dir() -> Path:
    """
    Ensure a writable Houdini package directory exists.

    Returns:
        Path to writable package directory

    Raises:
        RuntimeError: If no writable package directory can be found/created
    """
    package_dirs = find_houdini_package_dirs()

    for pkg_dir in package_dirs:
        try:
            pkg_dir.mkdir(parents=True, exist_ok=True)
            # Test if writable
            test_file = pkg_dir / ".test_write"
            test_file.write_text("test")
            test_file.unlink()
            return pkg_dir
        except (OSError, PermissionError):
            continue

    raise RuntimeError(
        "No writable Houdini package directory found. "
        "Ensure Houdini is installed and accessible."
    )
