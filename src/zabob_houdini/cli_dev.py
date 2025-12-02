'''
Developer support commands, python side
'''

import click

from zabob_houdini.utils_dev import DEV_LAYOUT as layout, update_option_list


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

    # 3. Write sorted names to text file with last-used first
    update_option_list("example-files", example_names)

    # Print to stdout if requested
    if show:
        for example_name in example_names:
            print(example_name)


@_examples.command('_run-example')
@click.argument('example_name', type=str)
def _run_example(example_name: str) -> None:
    """
    Run an example file and update the example list to put it first.

    This is used internally by launch configurations to track last-run example.
    """
    # Exit quietly if escape was pressed or placeholder selected
    if example_name in ('__escape__', '__initialize__'):
        return

    examples_dir = layout.examples
    vscode_tmp_dir = layout.vscode_tmp

    if examples_dir is None or vscode_tmp_dir is None:
        click.echo("Error: Could not locate examples or .vscode/tmp directory", err=True)
        return

    # Update the example list to put this example first
    example_names = sorted(
        py_file.stem
        for py_file in examples_dir.glob("*.py")
        if not py_file.name.startswith("_")
    )

    if example_name not in example_names:
        click.echo(f"Error: Example '{example_name}' not found", err=True)
        return

    update_option_list("example-files", example_names, move_to_top=example_name)

    # Execute the example by importing and running it
    example_file = examples_dir / f"{example_name}.py"
    import sys
    if str(examples_dir) not in sys.path:
        sys.path.insert(0, str(examples_dir))

    # Read and execute the script
    from zabob_houdini.dyn_loader import transform_script
    script_code = example_file.read_text()
    script_obj, _ = transform_script(script_code, str(example_file))
    exec(script_obj, {'__name__': '__main__', '__file__': str(example_file)})
