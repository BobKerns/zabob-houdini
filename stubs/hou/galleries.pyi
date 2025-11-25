"""Module for managing galleries and their entries.

Galleries are collections of node templates and parameter presets that can be applied to
operator nodes. Gallery entries represent individual presets within a gallery.

See https://www.sidefx.com/docs/houdini/hom/hou/galleries.html
"""

from typing import Sequence
from . import Gallery, GalleryEntry, Node, NodeType


def createGalleryEntry(
    gallery_path: str,
    entry_name: str,
    node: Node,
) -> GalleryEntry | None:
    """Create and return a new gallery entry in the specified gallery.

    Args:
        gallery_path: The file path to the gallery
        entry_name: The name for the new gallery entry
        node: The node to create the gallery entry from

    Returns:
        The newly created GalleryEntry, or None if creation failed

    See https://www.sidefx.com/docs/houdini/hom/hou/galleries.html#createGalleryEntry
    """
    ...


def galleries() -> tuple[Gallery, ...]:
    """Return a tuple of all galleries currently installed in the Houdini session.

    Returns:
        Tuple of all Gallery objects installed in the session

    See https://www.sidefx.com/docs/houdini/hom/hou/galleries.html#galleries
    """
    ...


def galleryEntries(
    name_pattern: str | None = None,
    label_pattern: str | None = None,
    keyword_pattern: str | None = None,
    category: str | None = None,
    node_type: NodeType | None = None,
) -> tuple[GalleryEntry, ...]:
    """Return gallery entries matching the specified search criteria.

    All parameters are optional filters. If a parameter is None, it will not be used
    to filter results.

    Args:
        name_pattern: Pattern to match against entry names (optional)
        label_pattern: Pattern to match against entry labels (optional)
        keyword_pattern: Pattern to match against entry keywords (optional)
        category: Category to filter by (optional)
        node_type: Node type to filter by (optional)

    Returns:
        Tuple of GalleryEntry objects matching the search criteria

    See https://www.sidefx.com/docs/houdini/hom/hou/galleries.html#galleryEntries
    """
    ...


def installGallery(gallery_path: str) -> Gallery | None:
    """Load a gallery file into the current Houdini session.

    Args:
        gallery_path: The file path to the gallery to install

    Returns:
        The installed Gallery object, or None if installation failed

    See https://www.sidefx.com/docs/houdini/hom/hou/galleries.html#installGallery
    """
    ...


def removeGallery(gallery_path: str) -> bool:
    """Remove a gallery from the current Houdini session.

    Args:
        gallery_path: The file path to the gallery to remove

    Returns:
        True if the gallery was successfully removed, False otherwise

    See https://www.sidefx.com/docs/houdini/hom/hou/galleries.html#removeGallery
    """
    ...
