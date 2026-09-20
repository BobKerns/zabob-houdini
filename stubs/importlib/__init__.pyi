from . import abc, machinery
__all__ = ['abc', 'machinery']


def import_module(name: str, package: str | None = None) -> object: ...
