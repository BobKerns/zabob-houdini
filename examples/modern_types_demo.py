"""
Modern typing example for Zabob-Houdini.
Demonstrates the use of modern Python 3.9+ built-in types instead of typing module equivalents.
"""
from typing import Any
from zabob_houdini import node

def demonstrate_modern_types():
    """Show modern type annotations in action."""

    # Modern types used in stubs:
    # tuple[T, ...] instead of Tuple[T, ...]
    # list[T] instead of List[T]
    # dict[K, V] instead of Dict[K, V]

    # Example: tuple return type
    def get_nodes() -> tuple[str, ...]:
        return ("box", "sphere", "merge")

    # Example: list with optional items
    def get_inputs() -> list[Any]:  # NodeInstance | None in practice
        box = node("/obj/geo1", "box")
        return [box, None, box]  # Sparse inputs

    # Example: dict parameter mapping
    def get_params() -> dict[str, float | int | str]:
        return {"tx": 1.0, "ty": 2, "name": "my_node"}

    print("Modern type annotations working correctly!")
    print(f"Node types: {get_nodes()}")
    print(f"Parameter example: {get_params()}")

if __name__ == "__main__":
    demonstrate_modern_types()
