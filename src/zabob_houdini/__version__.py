'''
Get the version number.
'''

from importlib.metadata import version, PackageNotFoundError

__distribution__ = "zabob-houdini"

try:
    __version__ = version(__distribution__)
except PackageNotFoundError:
    # Package is not installed, fallback for development
    __version__ = "0.0.0-dev"

__all__ = ['__version__', '__distribution__']
