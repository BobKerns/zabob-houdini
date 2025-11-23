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
    @click.command(name='_exec', hidden=True)
    @click.argument('module_name')
    @click.argument('function_name')
    @click.argument('args', nargs=-1)
    def _exec(module_name: str, function_name: str, args: tuple[str, ...]) -> None:
        """
        Internal dispatcher for hython execution.

        Usage: hython -m zabob_houdini _exec <module_name> <function_name> [args...]

        This command is hidden from help and used internally by the houdini_bridge
        to execute functions within the Houdini Python environment.
        """
        with invoke_houdini_function(module_name, function_name, args) as result:
            json.dump(result, sys.stdout)
            sys.stdout.write('\n')
            sys.stdout.flush()
            if not result["success"]:
                import os
                os._exit(1)


    @click.command(name='_batch_exec', hidden=True)
    def _batch_exec() -> None:
        """
        Internal batch executor for multiple hython function calls.

        Reads JSON lines from stdin, each containing:
        {"module": "module_name", "function": "function_name", "args": ["arg1", "arg2"]}

        Outputs one JSON result per line to stdout.
        """
        import hou
        from zabob_houdini.core import _node_registry
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            _node_registry.clear()  # Clear the node registry to avoid stale references between tests
            hou.hipFile.clear()  # Clear the current hip file to avoid stale state between tests
            try:
                request = json.loads(line)
            except json.JSONDecodeError as e:
                write_error_result(f'Invalid JSON in request: {e}')
                continue
            if 'module' not in request or 'function' not in request:
                write_error_result(f'Missing "module" or "function" field in JSON request: {request}')
                continue
            module_name = request['module']
            function_name = request['function']
            args = request.get('args', [])
            if not isinstance(args, list):
                write_error_result(f'"args" field must be a list, got {type(args).__name__}')
                continue

            with invoke_houdini_function(module_name, function_name, args) as result:
                write_response(result)

    # Add the hidden commands to the existing CLI when module is imported
    main.add_command(_exec)
    main.add_command(_batch_exec)
    from zabob_houdini.houdini_info import houdini as houdini_info
    main.add_command(houdini_info, "houdini")
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

if __name__ == "__main__":
    main()
