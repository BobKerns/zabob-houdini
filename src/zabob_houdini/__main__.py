"""
Entry point for zabob-houdini CLI and hython dispatch.
"""

import click
import json
import sys


from zabob_houdini.cli import main as dev_main, houdini
from zabob_houdini.__version__ import __version__, __distribution__
from zabob_houdini.houdini_bridge import invoke_houdini_function
from zabob_houdini.utils import write_error_result, write_response
from zabob_houdini.utils_dev import DEV_LAYOUT as layout, generate


IN_HOUDINI: bool = 'hou' in sys.modules

@click.group()
@click.version_option(version=__version__, prog_name=__distribution__)
def main() -> None:
    """
    Zabob-Houdini development utilities.

    Simple CLI for validating Houdini integration and listing node types.
    """
    pass

if IN_HOUDINI:
    from zabob_houdini.houdini_dev import (
        _exec, _batch_exec, _run_test, _generate_test_list,
    )
    # Add the hidden commands to the existing CLI when module is imported
    main.add_command(_exec)
    main.add_command(_batch_exec)
    from zabob_houdini.houdini_info import houdini as houdini_info
    main.add_command(houdini_info, "houdini")
    if layout.testing is not None:
        if layout.vscode_tmp is not None:
            generate.add_command(_generate_test_list, "tests")
        houdini_info.add_command(_run_test, "runtest")
else:
    # Don't load houdini_versions in hython.
    # It is not needed, and depends on dotenv, which is not installed
    # by default.
    from zabob_houdini.houdini_versions import cli as sidefx_cli
    main.add_command(sidefx_cli, "sidefx")
    main.add_command(houdini, "houdini")

for cmd in dev_main.commands.values():
    if not isinstance(cmd, click.Group):
        main.add_command(cmd)


if layout.examples is not None:
    from zabob_houdini.cli_dev import _generate_example_list
    generate.add_command(_generate_example_list, "examples")

if len(generate.commands) > 0:
    main.add_command(generate, "generate")
if __name__ == "__main__":
    main()
