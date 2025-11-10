"""
Entry point for zabob-houdini CLI and hython dispatch.
"""

import click
import json
import sys

from zabob_houdini.cli import main as cli_main


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
cli_main.add_command(_exec)


def main() -> None:
    """Entry point that runs the CLI."""
    cli_main()


if __name__ == "__main__":
    main()
