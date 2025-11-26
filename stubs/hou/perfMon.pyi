"""Type stubs for hou.perfMon module.

The perfMon module contains performance monitor related functions.
Time and memory statistics are reported in milliseconds and bytes respectively.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Node, PerfMonEvent, PerfMonProfile, PerfMonRecordOptions


def startCookEvent(description: str, node: Node) -> PerfMonEvent:
    """Create an event related to node cooking and start it."""
    ...

def startEvent(description: str, auto_nest_events: bool = True) -> PerfMonEvent:
    """Create a generic event and start it."""
    ...

def startPaneEvent(panetype: str, operation: str) -> PerfMonEvent:
    """Create an event related to a scripted pane operation and start it."""
    ...

def startProfile(title: str, options: PerfMonRecordOptions | None = None) -> PerfMonProfile:
    """Create a new profile and start it so that it can record events."""
    ...

def startTimedCookEvent(description: str, node: Node) -> PerfMonEvent:
    """Deprecated: Use startCookEvent() instead."""
    ...

def startTimedEvent(description: str, auto_nest_events: bool = True) -> PerfMonEvent:
    """Deprecated: Use startEvent() instead."""
    ...
