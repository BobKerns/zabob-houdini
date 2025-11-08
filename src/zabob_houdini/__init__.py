"""
Zabob-Houdini: A simple API for creating Houdini node graphs.
"""

from importlib.metadata import version, PackageNotFoundError

from .main import main

try:
    __version__ = version("zabob-houdini")
except PackageNotFoundError:
    # Package is not installed, fallback for development
    __version__ = "0.0.0-dev"

__all__ = ["main"]
