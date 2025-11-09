"""
Entry point for hython -m zabob_houdini <function_name>
"""

import sys
from typing import Any


def main() -> None:
    """Main entry point for module execution."""
    if len(sys.argv) < 2:
        print("Usage: hython -m zabob_houdini <function_name> [args...]", file=sys.stderr)
        sys.exit(1)

    func_name = sys.argv[1]
    args = sys.argv[2:]  # Get remaining arguments

    try:
        # Import houdini_functions and call the requested function
        from zabob_houdini import houdini_functions
        func = getattr(houdini_functions, func_name)

        # Call function with arguments
        result = func(*args)

        # Print result to stdout
        print(result)

    except AttributeError:
        print(f"Function '{func_name}' not found in houdini_functions", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error executing {func_name}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
