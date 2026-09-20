'''
Utilities for the core API layer.

Must not import core_node or core_chain to avoid circular dependencies
Should only import hou and standard library modules.
'''

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from collections import defaultdict
from typing import TypeVar, overload

import hou


T_Node = TypeVar('T_Node', bound=hou.Node)


@overload
def hou_node(path: str) -> hou.Node: ...


@overload
def hou_node(path: T_Node) -> T_Node: ...


@overload
def hou_node(path: str, typ: type[T_Node]) -> T_Node: ...


@overload
def hou_node(path: hou.Node, typ: type[T_Node]) -> T_Node: ...


def hou_node(path: str | hou.Node, typ: type[T_Node] | None = None) -> hou.Node:
    """
    Get a Houdini node, raising exception if not found, typecasting if needed.

    Args:
        path: The path to the Houdini node or the node itself.
        typ: The expected type of the node.

    Returns:
        The Houdini node.

    Raises:
        ValueError: If the node does not exist.
        TypeError: If the node is not of the expected type.
    """
    match path:
        case hou.Node() as n:
            pass
        case str():
            n = hou.node(path)
            if n is None:
                raise ValueError(f"Node at path '{path}' does not exist.")
        case _:
            raise TypeError(f"Invalid type for hou_node: {type(path)}")
    if n is None:
        raise ValueError(f"Node at path '{path}' does not exist.")
    if typ is None:
        return n
    if not isinstance(n, typ):
        raise TypeError(f"Node at path '{n.path()}' is not of type {typ.__name__}.")
    return n


_generated_names: dict[str, int] = defaultdict(lambda: 1)


def _generate_name(parent: str, type: str) -> str:
    """Generate a unique name with the given prefix."""
    while True:
        count = _generated_names[type]
        _generated_names[type] += 1
        name = f"{type}{count}"
        path = f"{parent}/{name}"
        if hou.node(path) is None:
            return name
