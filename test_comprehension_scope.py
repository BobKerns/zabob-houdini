"""Test that comprehension iteration variables aren't transformed."""
from __future__ import dynamic_import  # type: ignore # noqa: F401,F403,F407
from typing import Any

from zabob_houdini.core import node, NodeInstance, ROOT  # noqa: F401


def test_function():
    """Test function with list comprehension."""
    nodes = [NodeInstance(ROOT, node_type="box", name=f"box{i}") for i in range(3)]

    # This should NOT transform 'node' to __getattr__('node')
    result = [
        node
        for node in nodes  # type: ignore # pyright: ignore[reportUnboundVariable] # noqa: F811
        if node.name.startswith("box")
    ]

    return result


def ignore(*args: Any):
    '''
    Example function to illustrate that 'node' in comprehensions
    should not be transformed.
    '''
    pass


if __name__ == "__main__":
    from zabob_houdini.dyn import show_source, show_ast, show_code
    import inspect

    # Get source and compile
    source = inspect.getsource(test_function)
    print("Original source:")
    print(source)
    print("\n" + "="*60 + "\n")
    print("Transformed source:")
    show_source(source)
    print("AST:")
    show_ast(source)

    print("\n" + "="*60 + "\n")
    # Show bytecode
    print("Bytecode:")
    show_code(source)
