"""Type stubs for hou.logging module.

Logging module for warnings and errors with sources and sinks system.

Houdini's logging system consists of sources and sinks. Sources generate and
distribute log entries. Sinks receive log entries from sources, and do something
with them. Sources are global, and identified by a unique name string.
"""

from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from . import LogEntry, FileSink, MemorySink


def createSource(source_name: str) -> None:
    """Create a new logging source that can send log entries."""
    ...

def defaultFileSink() -> FileSink | None:
    """Return shared file sink for the current Houdini session."""
    ...

def defaultSink(force_create: bool = False) -> MemorySink | None:
    """Return shared memory sink for the current Houdini session."""
    ...

def loadLogsFromFile(filepath: str) -> tuple[LogEntry, ...]:
    """Load tuple of LogEntry objects from JSON file."""
    ...

def log(entry: LogEntry, source_name: str | None = None) -> None:
    """Send LogEntry to all sinks connected to a logging source."""
    ...

def renderLogVerbosity() -> int:
    """Return Karma logging verbosity level (0-9)."""
    ...

def saveLogsToFile(logs: Sequence[LogEntry], filepath: str) -> None:
    """Save tuple of LogEntry objects to JSON file."""
    ...

def setRenderLogVerbosity(verbosity: int) -> None:
    """Set Karma logging verbosity level (0-9)."""
    ...

def sources() -> tuple[str, ...]:
    """Return tuple of all available log source names."""
    ...
