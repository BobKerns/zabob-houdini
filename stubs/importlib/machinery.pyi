

from importlib.abc import SourceLoader, ResourceLoader, Loader


class ModuleSpec:
    def __init__(self, name: str, loader: Loader, origin: str | None = ...) -> None: ...
    loader: Loader | None
    name: str


class SourceFileLoader(SourceLoader, ResourceLoader):
    def __init__(self, fullname: str, path: str) -> None: ...
