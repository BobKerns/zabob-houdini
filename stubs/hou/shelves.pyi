"""Contains functions for working with shelf tabs and shelf tools."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from . import Shelf, ShelfSet, Tool, scriptLanguage

def defaultFilePath() -> str:
    """Return the default file path for shelves."""
    ...

def newShelf(
    file_path: str | None = None,
    name: str | None = None,
    label: str | None = None
) -> Shelf:
    """Returns a new hou.Shelf object using the provided options."""
    ...

def newShelfSet(
    file_path: str | None = None,
    name: str | None = None,
    label: str | None = None
) -> ShelfSet:
    """Returns a new hou.ShelfSet object using the provided options."""
    ...

def newTool(
    file_path: str | None = None,
    name: str | None = None,
    label: str | None = None,
    script: str | None = None,
    language: scriptLanguage | None = None,
    icon: str | None = None,
    help: str | None = None,
    help_url: str | None = None,
    network_categories: tuple[str, ...] = (),
    viewer_categories: tuple[str, ...] = (),
    cop_viewer_categories: tuple[str, ...] = (),
    network_op_type: str | None = None,
    viewer_op_type: str | None = None,
    locations: tuple[str, ...] = (),
    hda_definition: Any = None
) -> Tool:
    """Returns a new hou.Tool object using the provided options."""
    ...

def loadFile(file_path: str) -> None:
    """Reads a shelf file and adds any shelves and tools defined in that file to Houdini."""
    ...

def reloadShelfFiles() -> None:
    """Reloading the shelf files found in the search path and update the shelf UI with any changed information."""
    ...

def runningTool() -> Tool | None:
    """Return the currently running tool, if any."""
    ...

def shelfSets() -> dict[str, ShelfSet]:
    """Returns a dictionary mapping the internal name of every known shelf tab to a corresponding hou.ShelfSet object."""
    ...

def shelves() -> dict[str, Shelf]:
    """Returns a dictionary mapping the internal name of every known shelf tab to a corresponding hou.Shelf object."""
    ...

def tools() -> dict[str, Tool]:
    """Returns a dictionary mapping the internal name of every known tool to a corresponding hou.Tool object."""
    ...

def tool(tool_name: str) -> Tool | None:
    """Gets a reference to a hou.Tool by its internal name."""
    ...

def beginChangeBlock() -> None:
    """Prevents Houdini from automatically rewriting shelf information files until endChangeBlock is called."""
    ...

def endChangeBlock() -> None:
    """See beginChangeBlock above."""
    ...
