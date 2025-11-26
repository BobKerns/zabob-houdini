'''
Developer support commands, python side
'''

from pathlib import Path

import click

from zabob_houdini.utils_dev import DEV_LAYOUT as layout

@click.group("_examples")
def _examples() -> None:
    """Example file support functions for python environment."""
    pass

@_examples.command('_generate-example-list')
@click.option('--show', is_flag=True, help="List example files to stdout.")
def _generate_example_list(show: bool) -> None:
    """
    Generate a list of example files from the examples/ directory.

    This function:
    1. Locates the examples/ folder relative to __file__
    2. Lists all Python files in examples/
    3. Writes the filenames (without extension), sorted, one per line to .vscode/tmp/example-files.txt
    """
    examples_dir = layout.examples
    vscode_tmp_dir = layout.vscode_tmp
    if examples_dir is None or vscode_tmp_dir is None:
        # Silently do nothing if layout is incomplete
        return

    # 2. Collect all Python file names (without extension)
    example_names = sorted(
        py_file.stem
        for py_file in examples_dir.glob("*.py")
        if not py_file.name.startswith("_")
    )

    # Ensure .vscode/tmp/ directory exists
    vscode_tmp_dir.mkdir(parents=True, exist_ok=True)

    # 3. Write sorted names to text file
    txt_path = vscode_tmp_dir / "example-files.txt"
    with open(txt_path, "w") as f:
        for example_name in example_names:
            if show:
                print(example_name)
            f.write(f"{example_name}\n")
