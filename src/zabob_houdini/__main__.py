"""
Entry point for zabob-houdini CLI and hython dispatch.
"""

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
            # Debugging feature: if the directory in TEST_HIP_DIR (default "hip")
            # exists, save a hip file into the directory, named after the test function.
            # This is a documented debugging feature, do not remove!
            # See DEVELOPMENT.md for details.
            test_hip_dir = os.environ.get("TEST_HIP_DIR", "hip")
            if not test_hip_dir:
                # Skip writing HIP file if TEST_HIP_DIR is empty
                return
            test_hip_path = Path(test_hip_dir)
            if test_hip_path.exists():
                hipfile = test_hip_path / f"{function_name}.hip"
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


    @click.command(name='_batch_exec', hidden=True)
    def _batch_exec() -> None:
        """
        Internal batch executor for multiple hython function calls.

        Reads JSON lines from stdin, each containing:
        {"module": "module_name", "function": "function_name", "args": ["arg1", "arg2"]}

        Outputs one JSON result per line to stdout.
        """
        import hou  # Import here to ensure we're in Houdini

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                module_name = request['module']
                function_name = request['function']
                args = request.get('args', [])

                # Import the specified module and call the requested function
                houdini_module = __import__(f"zabob_houdini.{module_name}", fromlist=[module_name])
                func = getattr(houdini_module, function_name)

                # Call function with arguments and capture result
                result = func(*args)
                json.dump(result, sys.stdout)
                sys.stdout.write('\n')
                sys.stdout.flush()

                # Clear the node registry to avoid stale references between tests
                # This prevents "object no longer exists" errors when using persistent hython
                from zabob_houdini.core import _node_registry
                _node_registry.clear()

                # Optional: Save hip file for debugging
                test_hip_dir = os.environ.get("TEST_HIP_DIR", "hip")
                if test_hip_dir:
                    test_hip_path = Path(test_hip_dir)
                    if test_hip_path.exists():
                        hipfile = test_hip_path / f"{function_name}.hip"
                        hou.hipFile.save(str(hipfile))
                        print(f"Saved HIP file: {hipfile}", file=sys.stderr)

            except Exception as e:
                import traceback
                output = {
                    'success': False,
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
                json.dump(output, sys.stdout)
                sys.stdout.write('\n')
                sys.stdout.flush()

    # Add the hidden commands to the existing CLI when module is imported
    main.add_command(_exec)
    main.add_command(_batch_exec)
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
