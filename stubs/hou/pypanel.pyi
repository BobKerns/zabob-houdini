"""Module containing functions related to Python panels."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import PythonPanelInterface

def installFile(file_path: str) -> None:
    """Install all the Python Panel interfaces defined in the given .pypanel file into the current Houdini session."""
    ...

def interfaceByName(name: str) -> PythonPanelInterface:
    """Return the Python Panel interface definition that corresponds to the given interface name."""
    ...

def interfacesInFile(file_path: str) -> tuple[PythonPanelInterface, ...]:
    """Return all the Python Panel interface definitions inside the given .pypanel file."""
    ...

def interfaces() -> dict[str, PythonPanelInterface]:
    """Return all the Python Panel interface definitions currently installed."""
    ...

def menuInterfaces() -> tuple[str, ...]:
    """Return a tuple of the names of the interfaces currently shown in the Python Panel drop-down menu."""
    ...

def setMenuInterfaces(names: tuple[str, ...]) -> None:
    """Set the Python Panel drop-down menu to the list of interface names."""
    ...
