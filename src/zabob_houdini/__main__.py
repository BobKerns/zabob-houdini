"""
Entry point for zabob-houdini CLI and hython dispatch.
"""

from ctypes.util import test
import click
import json
import sys
import os
from pathlib import Path

from zabob_houdini.cli import main as dev_main, diagnostics, info
from zabob_houdini.__version__ import __version__, __distribution__

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
        try:
            # Import the specified module and call the requested function
            houdini_module = __import__(f"zabob_houdini.{module_name}", fromlist=[module_name])
            func = getattr(houdini_module, function_name)

            # Call function with arguments and capture result
            result = func(*args)
            json.dump(result, sys.stdout)
            test_hip = Path(os.environ.get("TEST_HIP_DIR", "hip"))
            if test_hip.exists():
                hipfile = test_hip / f"{function_name}.hip"
                import hou
                hou.hipFile.save(str(hipfile))
                print(f"Saved HIP file: {hipfile}", file=sys.stderr)


        except ImportError as e:
            output = {
                'success': False,
                'error': f"Module 'zabob_houdini.{module_name}' not found: {e}"
            }
            json.dump(output, sys.stdout)
            sys.exit(1)

        except AttributeError as e:
            output = {
                'success': False,
                'error': f"Function '{function_name}' not found in {module_name}: {e}"
            }
            print(json.dumps(output))
            sys.exit(1)

        except Exception as e:
            output = {
                'success': False,
                'error': f"Error executing {module_name}.{function_name}: {e}"
            }
            print(json.dumps(output))
            sys.exit(1)


    # Add the hidden _exec command to the existing CLI when module is imported
    main.add_command(_exec)
    from zabob_houdini.houdini_info import info as houdini_info
    main.add_command(houdini_info, "info")
else:
    # Don't load houdini_versions in hython.
    # It is not needed, and depends on dotenv, which is not installed
    # by default.
    from zabob_houdini.houdini_versions import cli as houdini_cli
    main.add_command(houdini_cli, "houdini")
    main.add_command(info, "info")

main.add_command(diagnostics, "diagnostics")
for cmd in dev_main.commands.values():
    if not isinstance(cmd, click.Group):
        main.add_command(cmd)

if __name__ == "__main__":
    main()
