"""File system utilities module (hou.fs)."""

from typing import BinaryIO, TextIO

class FileReader:
    """
    Convenience class for reading plain text or binary files.

    Works with any custom file system handlers registered with Houdini
    (i.e. paths with custom `handler://` prefixes).
    """

    def __init__(self, path: str, binary: bool = False) -> None:
        """
        Initialize a FileReader for the given path.

        Args:
            path: The file path to read from
            binary: If True, open in binary mode; otherwise text mode
        """
        ...

    def read(self, size: int = -1) -> str | bytes:
        """Read and return up to size bytes/characters."""
        ...

    def readline(self, size: int = -1) -> str | bytes:
        """Read and return one line."""
        ...

    def readlines(self, hint: int = -1) -> list[str] | list[bytes]:
        """Read and return a list of lines."""
        ...

    def close(self) -> None:
        """Close the file."""
        ...

    def __enter__(self) -> 'FileReader':
        """Context manager entry."""
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        ...

class FileWriter:
    """
    Convenience class for writing plain text or binary files.

    Works with any custom file system handlers registered with Houdini
    (i.e. paths with custom `handler://` prefixes).
    """

    def __init__(self, path: str, binary: bool = False, append: bool = False) -> None:
        """
        Initialize a FileWriter for the given path.

        Args:
            path: The file path to write to
            binary: If True, open in binary mode; otherwise text mode
            append: If True, append to existing file; otherwise overwrite
        """
        ...

    def write(self, data: str | bytes) -> int:
        """Write data to the file and return number of bytes/characters written."""
        ...

    def writelines(self, lines: list[str] | list[bytes]) -> None:
        """Write a list of lines to the file."""
        ...

    def close(self) -> None:
        """Close the file."""
        ...

    def flush(self) -> None:
        """Flush the write buffer."""
        ...

    def __enter__(self) -> 'FileWriter':
        """Context manager entry."""
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        ...

class Path:
    """
    Represents a path in a filesystem.

    Modeled after Python's pathlib, but works with any custom file system handlers
    registered with Houdini (i.e. paths with custom `handler://` prefixes).
    """

    def __init__(self, *pathsegments: str) -> None:
        """Initialize a Path from path segments."""
        ...

    def __str__(self) -> str:
        """Return the string representation of the path."""
        ...

    def __truediv__(self, other: str | 'Path') -> 'Path':
        """Join paths using the / operator."""
        ...

    def exists(self) -> bool:
        """Return True if the path exists."""
        ...

    def is_file(self) -> bool:
        """Return True if the path is a file."""
        ...

    def is_dir(self) -> bool:
        """Return True if the path is a directory."""
        ...

    def is_absolute(self) -> bool:
        """Return True if the path is absolute."""
        ...

    def absolute(self) -> 'Path':
        """Return an absolute version of the path."""
        ...

    def resolve(self) -> 'Path':
        """
        Make the path absolute, resolving any symlinks.
        """
        ...

    def parent(self) -> 'Path':
        """Return the parent directory."""
        ...

    def name(self) -> str:
        """Return the final component of the path."""
        ...

    def stem(self) -> str:
        """Return the final component without its suffix."""
        ...

    def suffix(self) -> str:
        """Return the file extension."""
        ...

    def suffixes(self) -> list[str]:
        """Return a list of the path's file extensions."""
        ...

    def with_name(self, name: str) -> 'Path':
        """Return a new path with the name changed."""
        ...

    def with_stem(self, stem: str) -> 'Path':
        """Return a new path with the stem changed."""
        ...

    def with_suffix(self, suffix: str) -> 'Path':
        """Return a new path with the suffix changed."""
        ...

    def joinpath(self, *other: str | 'Path') -> 'Path':
        """Join path components."""
        ...

    def relative_to(self, other: str | 'Path') -> 'Path':
        """Return a relative version of this path."""
        ...

    def iterdir(self) -> list['Path']:
        """Yield Path objects for each item in the directory."""
        ...

    def glob(self, pattern: str) -> list['Path']:
        """Find all files matching the pattern."""
        ...

    def rglob(self, pattern: str) -> list['Path']:
        """Find all files matching the pattern recursively."""
        ...

    def mkdir(self, parents: bool = False, exist_ok: bool = False) -> None:
        """Create a directory at this path."""
        ...

    def rmdir(self) -> None:
        """Remove the directory at this path."""
        ...

    def unlink(self, missing_ok: bool = False) -> None:
        """Remove the file at this path."""
        ...

    def rename(self, target: str | 'Path') -> 'Path':
        """Rename the file or directory to target."""
        ...

    def replace(self, target: str | 'Path') -> 'Path':
        """Rename the file or directory to target, overwriting if it exists."""
        ...

    def read_text(self, encoding: str = 'utf-8') -> str:
        """Read and return the file contents as text."""
        ...

    def read_bytes(self) -> bytes:
        """Read and return the file contents as bytes."""
        ...

    def write_text(self, data: str, encoding: str = 'utf-8') -> int:
        """Write text data to the file."""
        ...

    def write_bytes(self, data: bytes) -> int:
        """Write binary data to the file."""
        ...

    def open(self, mode: str = 'r', encoding: str | None = None) -> TextIO | BinaryIO:
        """Open the file."""
        ...
