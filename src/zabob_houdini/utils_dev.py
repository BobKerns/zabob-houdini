'''
Utilities for developer support, both python and hython sides.
'''

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from typing import NamedTuple
from pathlib import Path
import os

import click


@click.group("generate")
def generate() -> None:
    """Generate various development support files."""
    pass


class DevLayout(NamedTuple):
    '''
    Layout of directories in the development hierarchy.
    '''

    workspace_root: Path
    src: Path
    zabob_houdini: Path
    testing: Path | None
    examples: Path | None
    vscode_tmp: Path | None


def get_dev_layout() -> DevLayout:
    '''
    Get the directory layout for development.

    Returns:
        DevLayout: NamedTuple with paths to key directories.
    '''
    houdini_functions = Path(__file__).resolve()
    zabob_houdini = houdini_functions.parent
    src = zabob_houdini.parent
    workspace_root = src.parent
    testing = workspace_root / "src" / "testing"
    examples = workspace_root / "examples"
    vscode_tmp = workspace_root / ".vscode" / "tmp"

    def or_none(path: Path, envvar: str) -> Path | None:
        envvar_value = os.getenv(envvar)
        if envvar_value is not None:
            path = Path(envvar_value)
        return path if path.is_dir() else None

    return DevLayout(
        workspace_root=workspace_root,
        src=src,
        zabob_houdini=zabob_houdini,
        testing=or_none(testing, "ZABOB_HOUDINI_TESTING_DIR"),
        examples=or_none(examples, "ZABOB_HOUDINI_EXAMPLES_DIR"),
        vscode_tmp=or_none(vscode_tmp, "ZABOB_HOUDINI_VSCODE_TMP_DIR")
    )


DEV_LAYOUT: DevLayout = get_dev_layout()


def update_option_list(name: str, options: list[str], move_to_top: str | None = None) -> None:
    """
    Update an option list file in .vscode/tmp/ with sorted options, optionally moving one to the top.

    This maintains a list of options where:
    - If move_to_top is provided, that option appears first
    - Otherwise, the first line from the existing file is preserved (if still valid)
    - All other options are sorted alphabetically
    - If no options exist, creates file with "__initialize__" placeholder

    Args:
        name: Name of the file (e.g., "test-functions.txt" or just "test-functions")
        options: List of all valid options
        move_to_top: Optional option to move to the top of the list
    """
    if DEV_LAYOUT.vscode_tmp is None:
        return

    # Ensure .txt extension
    if not name.endswith('.txt'):
        name = f"{name}.txt"

    file_path = DEV_LAYOUT.vscode_tmp / name

    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # If no options provided, create placeholder file
    if not options:
        if not file_path.exists():
            with open(file_path, "w") as f:
                f.write("__initialize__\n")
        return

    # Determine which option should be first
    first_option = None

    if move_to_top and move_to_top in options:
        first_option = move_to_top
    elif file_path.exists():
        # Preserve existing first line if still valid (skip placeholder)
        with open(file_path, "r") as f:
            first_line = f.readline().strip()
            if first_line and first_line in options and first_line != "__initialize__":
                first_option = first_line

    # Write the file
    with open(file_path, "w") as f:
        written = set()

        # Write the first option if we have one
        if first_option:
            f.write(f"{first_option}\n")
            written.add(first_option)

        # Write remaining options sorted
        for option in sorted(options):
            if option not in written:
                f.write(f"{option}\n")
