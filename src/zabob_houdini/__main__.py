"""
Entry point for hython -m zabob_houdini <function_name>
"""

import sys
from typing import Any


def main() -> None:
    """Main entry point for module execution."""
    if len(sys.argv) < 3:
        print("Usage: hython -m zabob_houdini <module_name> <function_name> [args...]", file=sys.stderr)
        sys.exit(1)

    module_name = sys.argv[1]
    func_name = sys.argv[2]
    args = sys.argv[3:]  # Get remaining arguments

    try:
        # Import the specified module and call the requested function
        houdini_module = __import__(f"zabob_houdini.{module_name}", fromlist=[module_name])
        func = getattr(houdini_module, func_name)

        # Call function with arguments
        result = func(*args)

        # Print result to stdout
        print(result)

    except ImportError:
        print(f"Module 'zabob_houdini.{module_name}' not found", file=sys.stderr)
        sys.exit(1)
    except AttributeError:
        print(f"Function '{func_name}' not found in {module_name}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error executing {module_name}.{func_name}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
