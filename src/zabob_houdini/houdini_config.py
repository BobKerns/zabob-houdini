"""
Houdini configuration utilities.
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional


def find_houdini_pref_dir() -> Optional[Path]:
    """
    Find Houdini user preferences directory using hconfig.

    Returns:
        Path to HOUDINI_USER_PREF_DIR or None if not found
    """
    hconfig_path = shutil.which("hconfig")
    if not hconfig_path:
        return None

    try:
        result = subprocess.run([
            hconfig_path, "-ap", "HOUDINI_USER_PREF_DIR"
        ], capture_output=True, text=True, check=True)

        # Parse the output to find the HOUDINI_USER_PREF_DIR line
        for line in result.stdout.split('\n'):
            if line.startswith('$HOUDINI_USER_PREF_DIR = '):
                pref_dir = line.split(' = ', 1)[1].strip()
                if pref_dir and pref_dir != '<not defined>':
                    return Path(pref_dir)

    except subprocess.CalledProcessError:
        pass

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
