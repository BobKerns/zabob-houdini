"""Logging utilities module (hou.logging).

Logging module for warnings and errors with sources and sinks system.

Houdini's logging system consists of sources and sinks. Sources generate and
distribute log entries. Sinks receive log entries from sources, and do something
with them. Sources are global, and identified by a unique name string.
"""

from typing import Any

# Classes are defined in the main hou module: FileSink, LogEntry, MemorySink, Sink

def createSource(source_name: str) -> None:
    """Create a new logging source that can send log entries."""
    ...

def defaultFileSink() -> Any | None:  # Returns FileSink or None
    """Return shared file sink for the current Houdini session."""
    ...

def defaultSink(force_create: bool = False) -> Any | None:  # Returns MemorySink or None
    """Return shared memory sink for the current Houdini session."""
    ...

def loadLogsFromFile(filepath: str) -> tuple[Any, ...]:  # tuple of LogEntry
    """Load tuple of LogEntry objects from JSON file."""
    ...

def log(entry: Any, source_name: str | None = None) -> None:  # entry is LogEntry
    """Send LogEntry to all sinks connected to a logging source."""
    ...

def renderLogVerbosity() -> int:
    """Return Karma logging verbosity level (0-9)."""
    ...

def saveLogsToFile(logs: Any, filepath: str) -> None:  # logs is Iterable[LogEntry]
    """Save tuple of LogEntry objects to JSON file."""
    ...

def setRenderLogVerbosity(verbosity: int) -> None:
    """Set Karma logging verbosity level (0-9)."""
    ...

def sources() -> tuple[str, ...]:
    """Return tuple of all available log source names."""
    ...
