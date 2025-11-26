
from typing import Any, Callable


class Stage:
    "USD Stage stub"
    Traversal: Callable[..., Any]

class PrimRange:
    def PreAndPostVisit(self, arg: Any) -> Any: ...
