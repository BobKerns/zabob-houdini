"""Type stubs for hou.webServer module.

This module provides functions and classes for running a web server inside a
graphical or non-graphical Houdini session.
"""

from typing import Any, Callable


class Request:
    """A request made to Houdini's web server.

    This object is passed to URL handler functions as a container for information
    from the client request.
    """

    def method(self) -> str:
        """Returns the HTTP method used in the request (GET, POST, etc.)."""
        ...

    def path(self) -> str:
        """Returns the path that was requested on the server."""
        ...

    def pathWithQueryString(self) -> str:
        """Returns the path including the query string part."""
        ...

    def queryString(self) -> str:
        """Returns the query string in the request, not including the leading ?."""
        ...

    def absoluteURI(self, location: str | None = None) -> str:
        """Returns the full URI used to make the current request.

        Args:
            location: Optional location to construct absolute URI for.
        """
        ...

    def isSecure(self) -> bool:
        """Returns True if the request was made using https instead of http."""
        ...

    def headers(self) -> dict[str, str]:
        """Returns a dictionary of the headers provided with the request."""
        ...

    def cookies(self) -> dict[str, str]:
        """Returns the parsed cookie data from the Cookie header."""
        ...

    def GET(self) -> dict[str, str]:
        """Returns a dictionary of parsed query string variables from the URL."""
        ...

    def POST(self) -> dict[str, str]:
        """Returns a dictionary of parsed query variables from the request body."""
        ...

    def files(self) -> dict[str, "UploadedFile"]:
        """Returns a dictionary of file uploads passed in multipart/form-data."""
        ...

    def port(self) -> int:
        """Returns the server port the request came from."""
        ...

    def body(self) -> str:
        """Returns the fully unparsed body of the request."""
        ...

    def contentLength(self) -> str:
        """Returns the content length header."""
        ...

    def contentType(self) -> str:
        """Returns the content type header."""
        ...

    def host(self) -> str:
        """Returns the host found in the request host header."""
        ...

    def protocol(self) -> str:
        """Returns the protocol used for the request."""
        ...


class Response:
    """A response made back from Houdini's web server."""

    def __init__(
        self,
        data: Any,
        status: int = 200,
        content_type: str = "text/html",
        is_file_name: bool = False,
        delete_file: bool = False,
    ) -> None:
        """Initialize a Response object.

        Args:
            data: The response data (string, bytes, or file path).
            status: HTTP status code (default 200).
            content_type: MIME type of the response (default "text/html").
            is_file_name: If True, data is treated as a file path.
            delete_file: If True, delete the file after sending.
        """
        ...

    def setHeader(self, header_name: str, header_value: str) -> str:
        """Add/change an HTTP header in the response.

        Args:
            header_name: Name of the header.
            header_value: Value for the header.
        """
        ...

    def headers(self) -> dict[str, str]:
        """Returns a dictionary of all headers in the response."""
        ...

    def statusLabel(self) -> str:
        """Return the status label of the response."""
        ...

    def body(self) -> str:
        """Returns the body of the response."""
        ...


class UploadedFile:
    """A file uploaded in a request made to Houdini's web server."""

    def name(self) -> str:
        """Returns the name of the file that was uploaded."""
        ...

    def size(self) -> int:
        """Returns the size of the file that was uploaded."""
        ...

    def isInMemory(self) -> bool:
        """Returns whether the uploaded file is stored in memory or on disk."""
        ...

    def temporaryFilePath(self) -> str:
        """If not in memory, returns the path to the uploaded file on disk."""
        ...

    def saveToDisk(self) -> None:
        """Force an in-memory file to be saved to a temporary file on disk."""
        ...

    def read(self, max_size: int = -1) -> bytes:
        """Read up to max_size bytes of the uploaded file.

        Args:
            max_size: Maximum number of bytes to read (-1 for all).

        Returns:
            Bytes object containing the file data.
        """
        ...


class APIError(Exception):
    """Raise this exception in apiFunction handlers to indicate an error.

    If raised, the server will return a 422 status with a JSON response
    containing an "error" key with the given error message.
    """

    def __init__(self, msg: Any) -> None:
        """Initialize an APIError.

        Args:
            msg: Error message string or any JSON-encodable object.
        """
        ...


def run(
    port: int = 8008,
    debug: bool = False,
    max_num_threads: int = 4,
    in_background: bool | None = None,
    reload_source_changes: bool | None = None,
    max_in_memory_file_upload_size: int | None = None,
    max_request_size: int | None = None,
    settings: str | None = None,
    ports: list[int] = [],
) -> None:
    """Starts Houdini's web server.

    Args:
        port: The port number to listen on (default 8008).
        debug: Enable debug mode with verbose logging and stack traces.
        max_num_threads: Maximum number of simultaneous worker threads.
        in_background: Run server in separate thread (auto-detected if None).
        reload_source_changes: Auto-reload when Python files change.
        max_in_memory_file_upload_size: Max size for in-memory uploads (bytes).
        max_request_size: Maximum HTTP request size in bytes (default 3 GB).
        settings: Path to settings file for additional configuration.
        ports: Extra ports the server should listen on.
    """
    ...


def requestShutdown() -> None:
    """Tells Houdini's web server to shut down after serving all open requests.

    Call from a URL handler or API function to tell the server to shut down
    when it is finished handling all active requests.
    """
    ...


def isInDebugMode() -> bool:
    """Returns True if Houdini's web server was started in debug mode."""
    ...


def urlHandler(
    path: str,
    is_prefix: bool = False,
    ports: list[int] = [],
) -> Callable[[Callable[[Request], Response]], Callable[[Request], Response]]:
    """Decorator for functions that handle requests to Houdini's web server.

    Args:
        path: Server path starting with "/" to handle.
        is_prefix: If True, handle all paths starting with this prefix.
        ports: Specific ports to bind to (empty list = main port).

    Returns:
        Decorator function that registers the handler.

    Example:
        @hou.webServer.urlHandler("/hello")
        def my_handler(request):
            return hou.webServer.Response("Hello world")
    """
    ...


def apiFunction(
    namespace: str | None = None,
    return_binary: bool = False,
    arg_types: dict[str, type] | None = None,
    ports: list[int] = [],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator for functions callable through API endpoint on web server.

    Decorated functions can be called via remote procedure call, returning
    JSON or binary responses.

    Args:
        namespace: Prefix for the function name (e.g., "geo" for "geo.function").
        return_binary: If True, return value always treated as binary data.
        arg_types: Dict mapping argument names to Python types for conversion.
        ports: Specific ports to bind to (empty list = main port).

    Returns:
        Decorator function that registers the API function.

    Example:
        @hou.webServer.apiFunction(namespace="geo")
        def vector_length(request, x, y, z):
            return hou.Vector3(x, y, z).length()
    """
    ...


def errorResponse(
    request: Request,
    error_message: Any,
    status: int,
    use_heading: bool = True,
) -> Response:
    """Generates a Response object representing an HTTP error.

    Args:
        request: The request object.
        error_message: Error message string or JSON-encodable value.
        status: HTTP status code.
        use_heading: Wrap message in <h1> for HTML responses.

    Returns:
        Response object with error details.
    """
    ...


def notFoundResponse(request: Request) -> Response:
    """Generates a Response object representing a 404 Not Found HTTP error.

    Args:
        request: The request object.

    Returns:
        Response object with 404 status.
    """
    ...


def fileResponse(
    file_path: str,
    content_type: str | None = None,
    delete_file: bool = False,
    download_as_filename: str | None = None,
) -> Response:
    """Generates a Response object that sends the contents of a file.

    Args:
        file_path: Path to the file on disk to send to client.
        content_type: MIME type (auto-detected if None).
        delete_file: If True, delete file after sending.
        download_as_filename: Client-side filename for download.

    Returns:
        Response object that streams the file.
    """
    ...


def redirect(
    request: Request,
    path: str,
    permanent: bool = False,
) -> Response:
    """Generates a Response object representing a 301/302 redirect.

    Args:
        request: The request object.
        path: Server path to redirect the client to.
        permanent: If True, use 301 Moved Permanently; otherwise 302 Found.

    Returns:
        Response object with redirect headers.
    """
    ...


def registerStaticFilesDirectory(
    directory: str,
    url_prefix: str = "/static",
) -> None:
    """Register a directory for automatic static file serving.

    When requests start with url_prefix, the server automatically serves
    files from the specified directory.

    Args:
        directory: Path to directory containing static files.
        url_prefix: URL prefix for accessing these files (default "/static").

    Note:
        Call this before hou.webServer.run(), not from a URL handler.
    """
    ...


def registerOpdefPath(prefix: str = "/opdef") -> None:
    """Register a prefix as a handler to serve opdef requests.

    When requests start with prefix, the server responds with corresponding
    opdef section data.

    Args:
        prefix: URL prefix for opdef requests (default "/opdef").

    Note:
        Call this before hou.webServer.run(), not from a URL handler.
    """
    ...
