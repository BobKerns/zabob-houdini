"""HDA utilities module (hou.hda).

Module containing functions related to Houdini Digital Assets.
"""

from __future__ import annotations
from typing import Callable, Any
import hou


# File management functions

def definitionsInFile(file_path: str) -> tuple[hou.HDADefinition, ...]:
    """Return all the digital asset definitions inside an hda file."""
    ...


def installFile(
    file_path: str,
    oplibraries_file: str | None = None,
    change_oplibraries_file: bool = True,
    force_use_assets: bool = False
) -> None:
    """Install all the node types defined in an hda file into the current Houdini session."""
    ...


def uninstallFile(
    file_path: str,
    oplibraries_file: str | None = None,
    change_oplibraries_file: bool = True
) -> None:
    """Uninstall an hda file and all the node type definitions it provides from
    the current Houdini session.
    """
    ...


def reloadFile(file_path: str) -> None:
    """Reload the contents of an hda file, loading any updated digital asset
    definitions inside it.
    """
    ...


def installFiles(
    file_paths: list[str],
    oplibraries_file: str | None = None,
    change_oplibraries_file: bool = True,
    force_use_assets: bool = False
) -> None:
    """Batch install all the node types defined in the list of hda files into
    the current Houdini session.
    """
    ...


def uninstallFiles(
    file_paths: list[str],
    oplibraries_file: str | None = None,
    change_oplibraries_file: bool = True
) -> None:
    """Batch uninstall a list of hda file and all the node type definitions it
    provides from the current Houdini session.
    """
    ...


def reloadFiles(file_paths: list[str]) -> None:
    """Batch reload the contents of a list of hda file, loading any updated
    digital asset definitions inside them.
    """
    ...


def reloadAllFiles(rescan: bool = True) -> None:
    """Reload the digital asset files and update asset definitions in the current session."""
    ...


def reloadNamespaceOrder() -> None:
    """Check HOUDINI_OPNAMESPACE_HIERARCHY environment variable and rebuild the node
    type preference order that determines the node type to use when only unqualified
    root name is used in scripts, or, when Tab menu settings specify to show only a
    single preferred entry among several potential choices from different namespaces.
    """
    ...


def loadedFiles() -> tuple[str, ...]:
    """Return a tuple of paths to the hda files that are loaded into the current
    Houdini session.
    """
    ...


# Directory expansion/collapse functions

def expandToDirectory(file_path: str, directory_path: str) -> None:
    """Expand the contents of the hda file in file_path into the directory directory_path."""
    ...


def collapseFromDirectory(file_path: str, directory_path: str) -> None:
    """Given a directory that contains a previously expanded hda file, collapse it
    into the hda file specified by file_path.
    """
    ...


# Source naming functions

def renameSource(oplibraries_file: str, source_name: str | None = None) -> None:
    """Give a name to an OPlibraries file."""
    ...


# Node type name functions

def componentsFromFullNodeTypeName(node_type_name: str) -> tuple[str, ...]:
    """Returns a tuple of operator type name components that constitute the full node type name."""
    ...


def fullNodeTypeNameFromComponents(
    scope_node_type: str,
    name_space: str,
    name: str,
    version: str
) -> str:
    """Returns a full node type name build out of the given components."""
    ...


# Module reload functions

def reloadHDAModule(hda_module: hou.HDAModule) -> None:
    """Reload the code in the PythonModule section corresponding to hda_module."""
    ...


def reloadHDAViewerStateModule(hda_module: hou.HDAModule) -> None:
    """Reload the code in the ViewerStateModule section corresponding to hda_module."""
    ...


def reloadHDAViewerHandleModule(hda_module: hou.HDAModule) -> None:
    """Reload the code in the ViewerHandleModule section of hda_module."""
    ...


# Safeguard functions

def safeguardHDAs() -> bool:
    """Return True if the Safeguard Operator Definitions configuration option is turned on."""
    ...


def setSafeguardHDAs(on: bool) -> None:
    """Set whether the Safeguard Operator Definitions configuration option should be
    turned on or off.
    """
    ...


# Event callbacks

def setStateEventCallback(
    hda_globals: dict,
    state_name: str,
    event_name: str,
    callback: Callable
) -> None:
    """Register a Python callback that the given state will call whenever a particular
    event (or action) occurs on the node of a particular type.
    """
    ...


def addEventCallback(event_types: tuple[Any, ...], callback: Callable) -> None:
    """Register a Python callback that Houdini will call whenever a particular action,
    or event, occurs with digital asset libraries.

    Args:
        event_types: Tuple of hou.hdaEventType enumerated values
        callback: Callback function to register
    """
    ...


def removeEventCallback(event_types: tuple[Any, ...], callback: Callable) -> None:
    """Given a callback that was previously added and a sequence of hou.hdaEventType
    enumerated values, remove those event types from the set of event types for the callback.

    Args:
        event_types: Tuple of hou.hdaEventType enumerated values
        callback: Callback function to remove
    """
    ...


def removeAllEventCallbacks() -> None:
    """Remove all event callbacks for all event types."""
    ...


def eventCallbacks() -> tuple[tuple[tuple[Any, ...], Callable], ...]:
    """Return a tuple of all the Python callbacks that have been registered with calls
    to hou.hda.addEventCallback.
    """
    ...


# Utility functions

def defaultFileExtension() -> str:
    """Returns the default hda file extension for the current session based on the taint."""
    ...
