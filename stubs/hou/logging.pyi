"""Type stubs for hou.logging module.

Logging module for warnings and errors with sources and sinks system.

Houdini's logging system consists of sources and sinks. Sources generate and
distribute log entries. Sinks receive log entries from sources, and do something
with them. Sources are global, and identified by a unique name string.
"""

from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from . import severityType


class LogEntry:
    """Represents a single log message sent by a source to a sink.

    See https://www.sidefx.com/docs/houdini/hom/hou/logging/LogEntry.html
    """
    def __init__(
        self,
        message: str | None = None,
        source: str | None = None,
        source_context: str | None = None,
        severity: severityType | None = None,
        verbosity: int = 0,
        time: float = 0.0,
        thread_id: int = 0,
        has_external_info: bool = False,
        external_host_name: str | None = None,
        external_identifier: str | None = None,
        external_command_line: str | None = None,
        external_process_id: int = 0
    ) -> None: ...
    def source(self) -> str: ...
    def sourceContext(self) -> str: ...
    def message(self) -> str: ...
    def severity(self) -> severityType: ...
    def verbosity(self) -> int: ...
    def time(self) -> float: ...
    def threadId(self) -> int: ...
    def hasExternalInfo(self) -> bool: ...
    def externalHostName(self) -> str: ...
    def externalIdentifier(self) -> str: ...
    def externalCommandLine(self) -> str: ...
    def externalProcessId(self) -> int: ...


class Sink:
    """Base class for logging sinks that receive and process log entries.

    See https://www.sidefx.com/docs/houdini/hom/hou/logging/Sink.html
    """
    def connect(self, source_name: str) -> None:
        """Connect this sink to a logging source to receive its entries."""
        ...

    def disconnect(self, source_name: str) -> None:
        """Disconnect this sink from a logging source."""
        ...

    def isConnected(self, source_name: str) -> bool:
        """Check if this sink is connected to a logging source."""
        ...

    def connectedSources(self) -> tuple[str, ...]:
        """Return tuple of source names this sink is connected to."""
        ...


class FileSink(Sink):
    """File-based sink that writes log entries to a file.

    FileSink is a logging sink that writes log entries to a file on disk.
    Used by hou.logging.defaultFileSink().

    See https://www.sidefx.com/docs/houdini/hom/hou/logging/FileSink.html
    """
    def __init__(self, filepath: str) -> None:
        """Create a new file sink that writes to the specified file."""
        ...

    def filePath(self) -> str:
        """Return the file path this sink writes to."""
        ...

    def setFilePath(self, filepath: str) -> None:
        """Set the file path this sink writes to."""
        ...

    def flush(self) -> None:
        """Flush any buffered log entries to disk."""
        ...

    def close(self) -> None:
        """Close the log file."""
        ...


class MemorySink(Sink):
    """Memory-based sink that stores log entries in memory.

    MemorySink is a logging sink that stores log entries in memory for
    later retrieval. Used by hou.logging.defaultSink().

    See https://www.sidefx.com/docs/houdini/hom/hou/logging/MemorySink.html
    """
    def __init__(self, max_entries: int = 0) -> None:
        """Create a new memory sink with optional maximum entry limit."""
        ...

    def logEntries(self) -> tuple[LogEntry, ...]:
        """Return tuple of all stored log entries."""
        ...

    def clear(self) -> None:
        """Clear all stored log entries."""
        ...

    def maxEntries(self) -> int:
        """Return maximum number of entries to store (0 for unlimited)."""
        ...

    def setMaxEntries(self, max_entries: int) -> None:
        """Set maximum number of entries to store (0 for unlimited)."""
        ...

    def numEntries(self) -> int:
        """Return current number of stored entries."""
        ...


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
