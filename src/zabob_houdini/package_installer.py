"""
Houdini package installation utilities.

Handles installing zabob-houdini as a proper Houdini package for use in
Python nodes, shelf tools, and HDAs.
"""

import json
import os
import shutil
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


def get_houdini_python_version() -> str | None:
    """
    Get the Python version string used by Houdini (e.g., '3.11').

    Returns:
        Version string like '3.11' or None if cannot determine
    """
    from zabob_houdini.find_houdini import find_houdini_installations

    installations = find_houdini_installations()
    if not installations:
        return None

    # Use the highest version installation
    highest_version = max(installations.keys())
    install = installations[highest_version]

    py_version = install.python_version
    # Version object has major and minor attributes
    return f"{py_version.major}.{py_version.minor}"


def install_pythonrc() -> tuple[bool, str | None]:
    """
    Install pythonrc.py to enable dynamic imports in Houdini.

    Returns:
        Tuple of (success, installed_path or error_message)
    """
    # Find Houdini user prefs directory
    user_prefs = find_houdini_pref_dir()
    if not user_prefs:
        return False, "Could not find Houdini preferences directory"

    # Get Houdini's Python version
    py_version_str = get_houdini_python_version()
    if not py_version_str:
        return False, "Could not determine Houdini Python version"

    py_version = f"python{py_version_str}libs"
    pythonlibs_dir = user_prefs / py_version

    try:
        pythonlibs_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return False, f"Could not create {py_version} directory: {e}"

    # Get source template
    template_path = Path(__file__).parent / "pythonrc_template.py"
    if not template_path.exists():
        return False, f"Template not found: {template_path}"

    # Install pythonrc.py
    pythonrc_path = pythonlibs_dir / "pythonrc.py"
    try:
        shutil.copy2(template_path, pythonrc_path)
        return True, str(pythonrc_path)
    except Exception as e:
        return False, f"Could not install pythonrc.py: {e}"


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
        possible_src = current_file.parent.parent  # Go up from zabob_houdini/ to src/
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

    success = True

    try:
        # Create package JSON file
        package_file = create_package_json(package_dir, src_dir)
        print(f"✓ Created Houdini package: {package_file}")
        print(f"  Points to: {src_dir}")

    except Exception as e:
        print(f"Error creating package: {e}")
        success = False

    # Install pythonrc.py for dynamic imports
    pythonrc_success, pythonrc_result = install_pythonrc()
    if pythonrc_success:
        print(f"✓ Installed pythonrc.py: {pythonrc_result}")
    else:
        print(f"Warning: Could not install pythonrc.py: {pythonrc_result}")
        print("  Dynamic imports may not work in Houdini Python nodes")
        # Don't fail installation if pythonrc install fails
        # success = False

    return success


def uninstall_houdini_package() -> bool:
    """
    Remove zabob-houdini Houdini package.

    Returns:
        True if uninstallation successful, False otherwise
    """
    removed_any = False

    # Remove package JSON files
    for package_dir in get_houdini_package_dirs():
        package_file = package_dir / "zabob_houdini.json"
        if package_file.exists():
            try:
                package_file.unlink()
                print(f"✓ Removed package: {package_file}")
                removed_any = True
            except Exception as e:
                print(f"Error removing {package_file}: {e}")

    # Remove pythonrc.py if it exists
    user_prefs = find_houdini_pref_dir()
    if user_prefs:
        py_version_str = get_houdini_python_version()
        if py_version_str:
            py_version = f"python{py_version_str}libs"
            pythonrc_path = user_prefs / py_version / "pythonrc.py"
            if pythonrc_path.exists():
                try:
                    # Check if it's our file (contains zabob-houdini marker)
                    content = pythonrc_path.read_text()
                    if 'zabob-houdini' in content:
                        pythonrc_path.unlink()
                        print(f"✓ Removed pythonrc.py: {pythonrc_path}")
                        removed_any = True
                    else:
                        print(f"ℹ  Skipped pythonrc.py (not installed by zabob-houdini): {pythonrc_path}")
                except Exception as e:
                    print(f"Error removing pythonrc.py: {e}")

    if not removed_any:
        print("No zabob-houdini package found to remove")

    return removed_any


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_houdini_package()
    else:
        install_houdini_package()
