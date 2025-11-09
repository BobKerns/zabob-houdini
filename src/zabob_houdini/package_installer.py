"""
Houdini package installation utilities.

Handles installing zabob-houdini as a proper Houdini package for use in
Python nodes, shelf tools, and HDAs.
"""

import json
import os
from pathlib import Path
from zabob_houdini.houdini_config import find_houdini_pref_dir, ensure_houdini_package_dir


def get_houdini_package_dirs() -> list[Path]:
    """
    Get all possible Houdini package installation directories.

    Returns:
        List of package directories, ordered by preference
    """
    dirs = []

    # User packages directory (most preferred - writable)
    user_packages = None
    user_prefs = find_houdini_pref_dir()
    if user_prefs:
        user_packages = user_prefs / "packages"
        dirs.append(user_packages)

    # System packages (if writable)
    houdini_path = os.getenv('HOUDINI_PATH', '').split(os.pathsep)
    for path_str in houdini_path:
        if path_str:
            path = Path(path_str)
            if path.exists():
                packages_dir = path / "packages"
                if packages_dir != user_packages:  # Avoid duplicates
                    dirs.append(packages_dir)

    return dirs


def find_writable_package_dir() -> Path | None:
    """
    Find the first writable package directory.

    Returns:
        Path to writable package directory, or None if none found
    """
    # Try the hconfig-based approach first
    try:
        return ensure_houdini_package_dir()
    except RuntimeError:
        pass

    # Fallback to testing each directory
    for pkg_dir in get_houdini_package_dirs():
        try:
            # Create directory if it doesn't exist
            pkg_dir.mkdir(parents=True, exist_ok=True)

            # Test if writable
            test_file = pkg_dir / ".write_test"
            test_file.write_text("test")
            test_file.unlink()

            return pkg_dir
        except (OSError, PermissionError):
            continue

    return None


def create_package_json(package_dir: Path, zabob_src_path: Path) -> Path:
    """
    Create a Houdini package JSON file for zabob-houdini.

    Args:
        package_dir: Directory to create package file in
        zabob_src_path: Path to zabob-houdini src directory

    Returns:
        Path to created package file
    """
    package_config = {
        "env": [
            {
                "PYTHONPATH": {
                    "method": "prepend",
                    "value": str(zabob_src_path)
                }
            }
        ]
    }

    package_file = package_dir / "zabob_houdini.json"
    with open(package_file, 'w') as f:
        json.dump(package_config, f, indent=2)

    return package_file


def install_houdini_package(src_dir: Path | None = None) -> bool:
    """
    Install zabob-houdini as a Houdini package.

    Args:
        src_dir: Path to zabob-houdini src directory.
                If None, attempts to find it relative to this file.

    Returns:
        True if installation successful, False otherwise
    """
    if src_dir is None:
        # Try to find src directory relative to this file
        current_file = Path(__file__).resolve()
        possible_src = current_file.parent.parent / "src"
        if possible_src.exists():
            src_dir = possible_src
        else:
            print("Error: Could not find zabob-houdini src directory")
            return False

    # Find writable package directory
    package_dir = find_writable_package_dir()
    if not package_dir:
        print("Error: No writable Houdini package directory found")
        print("Available directories:", get_houdini_package_dirs())
        return False

    try:
        # Create package JSON file
        package_file = create_package_json(package_dir, src_dir)
        print(f"✓ Created Houdini package: {package_file}")
        print(f"  Points to: {src_dir}")
        return True

    except Exception as e:
        print(f"Error creating package: {e}")
        return False


def uninstall_houdini_package() -> bool:
    """
    Remove zabob-houdini Houdini package.

    Returns:
        True if uninstallation successful, False otherwise
    """
    removed_any = False

    for package_dir in get_houdini_package_dirs():
        package_file = package_dir / "zabob_houdini.json"
        if package_file.exists():
            try:
                package_file.unlink()
                print(f"✓ Removed package: {package_file}")
                removed_any = True
            except Exception as e:
                print(f"Error removing {package_file}: {e}")

    if not removed_any:
        print("No zabob-houdini package found to remove")

    return removed_any


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_houdini_package()
    else:
        install_houdini_package()
