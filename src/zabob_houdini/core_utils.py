'''
Utilities for the core API layer.

Must not import core_node or core_chain to avoid circular dependencies
Should only import hou and standard library modules.
'''

from collections import defaultdict
from collections.abc import Sequence
from typing import TYPE_CHECKING

import hou

def hou_node(path: str) -> 'hou.Node':
    """Get a Houdini node, raising exception if not found."""
    n = hou.node(path)
    if n is None:
        raise ValueError(f"Node at path '{path}' does not exist.")
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


