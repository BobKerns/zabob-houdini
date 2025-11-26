"""Module containing viewport visualizer functionality."""

from typing import TYPE_CHECKING, Callable, Any

if TYPE_CHECKING:
    from . import (
        ViewportVisualizer, ViewportVisualizerType,
        viewportVisualizerCategory, viewportVisualizerEventType,
        Node, GeometryViewport
    )

def visualizers(
    category: viewportVisualizerCategory = ...,
    node: Node | None = None
) -> tuple[ViewportVisualizer, ...]:
    """Return a tuple of viewport visualizers registered with Houdini for the given category."""
    ...

def createVisualizer(
    type: ViewportVisualizerType | str,
    category: viewportVisualizerCategory = ...,
    node: Node | None = None
) -> ViewportVisualizer:
    """Create a new viewport visualizer for the specified type."""
    ...

def copyVisualizer(source: ViewportVisualizer) -> ViewportVisualizer:
    """Create a duplicate of the specified source visualizer."""
    ...

def types() -> tuple[ViewportVisualizerType, ...]:
    """Return a tuple of visualizer types registered with Houdini."""
    ...

def type(name: str) -> ViewportVisualizerType:
    """Return the visualizer type registered with the specified name."""
    ...

def isCategoryActive(
    category: viewportVisualizerCategory,
    node: Node | None = None,
    viewport: GeometryViewport | None = None
) -> bool:
    """Return True if the visualizer category is active and False otherwise."""
    ...

def setIsCategoryActive(
    on: bool,
    category: viewportVisualizerCategory,
    node: Node | None = None,
    viewport: GeometryViewport | None = None
) -> bool:
    """Set the activation state of the specified visualizer category."""
    ...

def addEventCallback(
    event_types: tuple[viewportVisualizerEventType, ...],
    callback: Callable,
    category: viewportVisualizerCategory = ...,
    node: Node | None = None
) -> None:
    """Register a Python callback that Houdini will call whenever a particular action, or event, occurs related to a particular visualizer category."""
    ...

def removeEventCallback(
    event_types: tuple[viewportVisualizerEventType, ...],
    callback: Callable,
    category: viewportVisualizerCategory = ...,
    node: Node | None = None
) -> None:
    """Given a callback that was previously added on this category and a sequence of hou.viewportVisualizerEventType enumerated values, remove those event types from the set of event types for the callback."""
    ...

def removeAllEventCallbacks(
    category: viewportVisualizerCategory = ...,
    node: Node | None = None
) -> None:
    """Remove all event callbacks for all event types from this category."""
    ...

def eventCallbacks(
    category: viewportVisualizerCategory = ...,
    node: Node | None = None
) -> tuple[tuple[viewportVisualizerEventType, Callable], ...]:
    """Return a tuple of all the Python callbacks that have been registered with this category with calls to hou.viewportVisualizers.addEventCallback."""
    ...
