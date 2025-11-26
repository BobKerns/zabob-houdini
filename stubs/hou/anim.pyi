"""Animation utilities module for bookmark and geometry channel management.

See https://www.sidefx.com/docs/houdini/hom/hou/anim.html
"""

from typing import Any, Callable

import hou

# Bookmark Management Functions

def newBookmark(name: str, start_frame: float, end_frame: float) -> hou.Bookmark:
    """Create a new animation bookmark with the specified name and frame range.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/newBookmark.html
    """
    ...

def bookmarks() -> tuple[hou.Bookmark, ...]:
    """Return a tuple of all animation bookmarks.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/bookmarks.html
    """
    ...

def bookmark(session_id: str) -> hou.Bookmark:
    """Return the bookmark with the specified session ID.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/bookmark.html
    """
    ...

def getBookmark(session_id: str) -> hou.Bookmark:
    """Deprecated: Use bookmark() instead.

    Return the bookmark with the specified session ID.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/getBookmark.html
    """
    ...

def saveBookmarks(filename: str, bookmarks: tuple[hou.Bookmark, ...] | None = None, include_temporary: bool = False) -> bool:
    """Save bookmarks to a file.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/saveBookmarks.html
    """
    ...

def loadBookmarks(filename: str, remove_existing: bool = True) -> bool:
    """Load bookmarks from a file.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/loadBookmarks.html
    """
    ...

def saveBookmarksToString(bookmarks: tuple[hou.Bookmark, ...] | None = None, include_temporary: bool = False, binary: bool = True) -> bytes:
    """Serialize bookmarks to a byte string.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/saveBookmarksToString.html
    """
    ...

def loadBookmarksFromString(data: bytes, remove_existing: bool = True) -> None:
    """Deserialize bookmarks from a byte string.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/loadBookmarksFromString.html
    """
    ...

def clearBookmarks() -> None:
    """Remove all bookmarks.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/clearBookmarks.html
    """
    ...

def removeBookmarks(bookmarks: tuple[hou.Bookmark, ...]) -> None:
    """Remove the specified bookmarks.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/removeBookmarks.html
    """
    ...

# Bookmark Callbacks

def addBookmarksChangedCallback(callback: Callable[..., Any]) -> None:
    """Add a callback that is called when bookmarks are added, removed, or modified.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/addBookmarksChangedCallback.html
    """
    ...

def removeBookmarksChangedCallback(callback: Callable[..., Any]) -> None:
    """Remove a previously registered bookmarks changed callback.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/removeBookmarksChangedCallback.html
    """
    ...

# Geometry Channel Functions

def mergeGeometryChannels(collection_name: str, geometry: hou.Geometry, channel_names: tuple[str, ...] | None = None) -> None:
    """Merge geometry channels from the specified geometry into a collection.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/mergeGeometryChannels.html
    """
    ...

def getGeometryChannels(collection_name: str, geometry: hou.Geometry, channel_names: tuple[str, ...] | None = None) -> None:
    """Deprecated: Use mergeGeometryChannels() instead.

    Get geometry channels from the specified geometry into a collection.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/getGeometryChannels.html
    """
    ...

def setGeometryChannels(collection_name: str, geometry: hou.Geometry, channel_names: tuple[str, ...]) -> None:
    """Set geometry channels for the specified collection.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/setGeometryChannels.html
    """
    ...

def setGeometryChannelsFromPattern(collection_name: str, geometry: hou.Geometry, pattern: str) -> None:
    """Set geometry channels for the specified collection using a pattern.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/setGeometryChannelsFromPattern.html
    """
    ...

def setGeometryChannelPending(collection_name: str, channel_name: str, value: bool) -> None:
    """Mark a geometry channel as pending or not pending.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/setGeometryChannelPending.html
    """
    ...

def isGeometryChannelPending(collection_name: str, channel_name: str) -> bool:
    """Return True if the specified geometry channel is pending.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/isGeometryChannelPending.html
    """
    ...

def isGeometryChannelPinned(collection_name: str, channel_name: str | None = None) -> bool:
    """Return True if the specified geometry channel is pinned.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/isGeometryChannelPinned.html
    """
    ...

def pinnedGeometryChannels(collection_name: str) -> tuple[str, ...]:
    """Return a tuple of pinned geometry channel names for the collection.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/pinnedGeometryChannels.html
    """
    ...

def getPinnedGeometryChannels(collection_name: str) -> tuple[str, ...]:
    """Deprecated: Use pinnedGeometryChannels() instead.

    Return a tuple of pinned geometry channel names for the collection.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/getPinnedGeometryChannels.html
    """
    ...

def lockGeometryChannelCollection(collection_name: str, lock: bool) -> None:
    """Lock or unlock a geometry channel collection.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/lockGeometryChannelCollection.html
    """
    ...

# Geometry Channel Callbacks

def addGeometryChannelsChangedCallback(collection_name: str, callback: Callable[..., Any], on_mouse_up: bool = True) -> None:
    """Add a callback for when geometry channels in a collection change.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/addGeometryChannelsChangedCallback.html
    """
    ...

def removeGeometryChannelsChangedCallback(collection_name: str, callback: Callable[..., Any], on_mouse_up: bool = True) -> None:
    """Remove a previously registered geometry channels changed callback.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/removeGeometryChannelsChangedCallback.html
    """
    ...

# Slope Mode Functions

def slopeMode() -> hou.slopeMode:
    """Return the current channel editor slope mode setting.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/slopeMode.html
    """
    ...

def setSlopeMode(mode: hou.slopeMode) -> None:
    """Set the channel editor slope mode.

    See https://www.sidefx.com/docs/houdini/hom/hou/anim/setSlopeMode.html
    """
    ...
