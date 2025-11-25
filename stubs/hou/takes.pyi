"""Takes management module (hou.takes).

This module provides access to Houdini's take system for managing
different versions of parameter values within the same scene.

See: https://www.sidefx.com/docs/houdini/hom/hou/takes.html
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Take


def takes() -> tuple[Take, ...]:
    """Return a tuple of all the takes in the scene.

    Returns:
        Tuple of all takes in the scene.

    See: https://www.sidefx.com/docs/houdini/hom/hou/takes.html#takes
    """
    ...


def currentTake() -> Take:
    """Return the current take.

    Returns:
        The currently active take.

    See: https://www.sidefx.com/docs/houdini/hom/hou/takes.html#currentTake
    """
    ...


def setCurrentTake(take: Take) -> None:
    """Set the current take to the specified take.

    Args:
        take: The take to make current.

    See: https://www.sidefx.com/docs/houdini/hom/hou/takes.html#setCurrentTake
    """
    ...


def rootTake() -> Take:
    """Return the main (master) take.

    Returns:
        The root/master take.

    See: https://www.sidefx.com/docs/houdini/hom/hou/takes.html#rootTake
    """
    ...


def findTake(take_name: str) -> Take | None:
    """Return the take with the specified name or None if no such take exists.

    Args:
        take_name: Name of the take to find.

    Returns:
        The found take or None if no take with that name exists.

    See: https://www.sidefx.com/docs/houdini/hom/hou/takes.html#findTake
    """
    ...


def defaultTakeName() -> str:
    """Return the default take name used for new takes.

    Returns:
        The default take name.

    See: https://www.sidefx.com/docs/houdini/hom/hou/takes.html#defaultTakeName
    """
    ...


def setDefaultTakeName(name: str) -> None:
    """Set the default take name.

    Args:
        name: The new default take name.

    See: https://www.sidefx.com/docs/houdini/hom/hou/takes.html#setDefaultTakeName
    """
    ...
