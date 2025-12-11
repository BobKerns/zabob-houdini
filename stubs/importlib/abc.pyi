'''
Minimal stubs for importlib.abc
'''


from types import ModuleType


class MetaPathFinder:
    ...


class Loader:
    def execute_module(self, module: ModuleType) -> None: ...


class ResourceLoader(Loader):
    ...


class FileLoader(ResourceLoader):
    ...


class SourceLoader(ResourceLoader):
    ...


class InspectLoader(Loader):
    ...


class ExecutionLoader(Loader):
    ...
