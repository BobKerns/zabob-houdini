"""Dynamics utilities module (hou.dop).

Functions for working with Python script solver DOPs during simulations.

See also:
    https://www.sidefx.com/docs/houdini/hom/hou/dop.html
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import DopData, DopObject, DopSimulation, OpNode


def isScriptSolverRunning() -> bool:
    """Return whether or not a Python script solver DOP is currently running.

    Returns:
        True if a Python script solver DOP is currently running, False otherwise.

    See:
        https://www.sidefx.com/docs/houdini/hom/hou/dop.html#isScriptSolverRunning
    """
    ...


def scriptSolverData() -> DopData:
    """Return the solver data corresponding to the currently running Python script solver DOP.

    Returns:
        The DopData object for the currently running script solver.

    Raises:
        hou.Error: If no script solver is currently running.

    See:
        https://www.sidefx.com/docs/houdini/hom/hou/dop.html#scriptSolverData
    """
    ...


def scriptSolverNetwork() -> OpNode | None:
    """Return the DOP network node that contains the script solver DOP that is currently running.

    Returns:
        The DOP network OpNode, or None if no script solver is running.

    See:
        https://www.sidefx.com/docs/houdini/hom/hou/dop.html#scriptSolverNetwork
    """
    ...


def scriptSolverSimulation() -> DopSimulation | None:
    """Return the DOP simulation that contains the script solver DOP that is currently running.

    Returns:
        The DopSimulation object, or None if no script solver is running.

    See:
        https://www.sidefx.com/docs/houdini/hom/hou/dop.html#scriptSolverSimulation
    """
    ...


def scriptSolverObjects() -> tuple[DopObject, ...]:
    """Return a tuple of DOP objects being solved by the current script solver DOP.

    Returns:
        Tuple of DopObject instances being processed by the current script solver.

    Raises:
        hou.Error: If no script solver is currently running.

    See:
        https://www.sidefx.com/docs/houdini/hom/hou/dop.html#scriptSolverObjects
    """
    ...


def scriptSolverNewObjects() -> tuple[DopObject, ...]:
    """Return a tuple of newly-created DOP objects to later be solved by the current script solver DOP.

    Returns:
        Tuple of DopObject instances that are newly created and will be processed.

    Raises:
        hou.Error: If no script solver is currently running.

    See:
        https://www.sidefx.com/docs/houdini/hom/hou/dop.html#scriptSolverNewObjects
    """
    ...


def scriptSolverTimestepSize() -> float:
    """Return the timestep size for the script solver that is currently running.

    Returns:
        The timestep size as a float, or 0.0 if no script solver is running.

    See:
        https://www.sidefx.com/docs/houdini/hom/hou/dop.html#scriptSolverTimestepSize
    """
    ...
