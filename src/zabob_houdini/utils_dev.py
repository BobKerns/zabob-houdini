'''
Utilities for developer support, both python and hython sides.
'''


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
