"""The animation playbar module.

Provides functions to control and query the playbar's state, playback settings,
keyframe display, and animation toolbar.

See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable
    from . import (
        AnimBar,
        BaseKeyframe,
        Bookmark,
        ChannelList,
        Node,
        PaneTab,
        Parm,
        ParmTuple,
        Vector2,
        playMode as PlayMode,
    )

# Playbar event callbacks

def addEventCallback(callback: Callable[[], None]) -> None:
    """Register a Python callback to be called whenever a playbar event occurs.

    Args:
        callback: Function to call on playbar events.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#addEventCallback
    """
    ...

def clearEventCallbacks() -> None:
    """Remove all Python callbacks registered with addEventCallback.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#clearEventCallbacks
    """
    ...

def eventCallbacks() -> tuple[Callable[[], None], ...]:
    """Return a tuple of all Python callbacks registered with addEventCallback.

    Returns:
        Tuple of registered callback functions.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#eventCallbacks
    """
    ...

def removeEventCallback(callback: Callable[[], None]) -> None:
    """Remove a Python callback previously registered with addEventCallback.

    Args:
        callback: Function to remove from callback list.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#removeEventCallback
    """
    ...

# Display settings

def areKeysShown() -> bool:
    """Return True if the display of keyframes in the playbar is turned on.

    Returns:
        Whether keyframes are displayed.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#areKeysShown
    """
    ...

def areTicksShown() -> bool:
    """Return True if the display of frame ticks in the playbar is turned on.

    Returns:
        Whether frame ticks are displayed.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#areTicksShown
    """
    ...

def isAudioShown() -> bool:
    """Return True if the display of audio in the playbar is turned on.

    Returns:
        Whether audio waveform is displayed.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#isAudioShown
    """
    ...

def isRangeSliderShown() -> bool:
    """Return True if the display of the range slider in the playbar is turned on.

    Returns:
        Whether range slider is displayed.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#isRangeSliderShown
    """
    ...

def showAudio(on: bool) -> None:
    """Turn display of audio on the playbar on or off.

    Args:
        on: Whether to show audio waveform.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#showAudio
    """
    ...

def showKeys(on: bool) -> None:
    """Turn display of keyframes on the playbar on or off.

    Args:
        on: Whether to show keyframes.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#showKeys
    """
    ...

def showRangeSlider(on: bool) -> None:
    """Turn display of the range slider on the playbar on or off.

    Args:
        on: Whether to show range slider.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#showRangeSlider
    """
    ...

def showTicks(on: bool) -> None:
    """Turn display of the frame ticks on the playbar on or off.

    Args:
        on: Whether to show frame ticks.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#showTicks
    """
    ...

# Playback control

def isPlaying() -> bool:
    """Return True if the playbar is playing.

    Returns:
        Whether playback is active.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#isPlaying
    """
    ...

def play() -> None:
    """Play in the forward direction.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#play
    """
    ...

def reverse() -> None:
    """Play in the reverse direction.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#reverse
    """
    ...

def stop() -> None:
    """Stop playing.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#stop
    """
    ...

# Playback settings

def playMode() -> PlayMode:
    """Return the playbar's play mode.

    Returns:
        Current play mode (Loop, Once, Zigzag, etc.).

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#playMode
    """
    ...

def setPlayMode(mode: PlayMode) -> None:
    """Set the play mode.

    Args:
        mode: Play mode to set (hou.playMode.Loop, Once, Zigzag, etc.).

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setPlayMode
    """
    ...

def isRealTime() -> bool:
    """Return True if realtime playback is turned on.

    Returns:
        Whether realtime playback is enabled.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#isRealTime
    """
    ...

def setRealTime(on: bool) -> None:
    """Turn realtime playback either on or off.

    Args:
        on: Whether to enable realtime playback.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setRealTime
    """
    ...

def isRealTimeSkipping() -> bool:
    """Return True if realtime playback skipping is turned on.

    Returns:
        Whether realtime skipping is enabled.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#isRealTimeSkipping
    """
    ...

def setRealTimeSkipping(on: bool) -> None:
    """Turn realtime playback skipping either on or off.

    Args:
        on: Whether to enable realtime skipping.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setRealTimeSkipping
    """
    ...

def realTimeFactor() -> float:
    """Return the multiplier factor used when playing with realtime playback turned on.

    Returns:
        Realtime playback speed multiplier.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#realTimeFactor
    """
    ...

def setRealTimeFactor(factor: float) -> None:
    """Set the realtime playback multiplier.

    Args:
        factor: Speed multiplier for realtime playback.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setRealTimeFactor
    """
    ...

# Frame ranges

def frameRange() -> Vector2:
    """Return a 2-tuple containing the start and end frame of the global time range.

    Returns:
        Vector2 with (start_frame, end_frame).

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#frameRange
    """
    ...

def setFrameRange(start: float, end: float) -> None:
    """Set the global time range using frame numbers.

    Args:
        start: Starting frame number.
        end: Ending frame number.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setFrameRange
    """
    ...

def timeRange() -> Vector2:
    """Return a 2-tuple containing the start and end times of the global time range.

    Returns:
        Vector2 with (start_time, end_time) in seconds.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#timeRange
    """
    ...

def setTimeRange(start: float, end: float) -> None:
    """Set the global time range using time in seconds.

    Args:
        start: Starting time in seconds.
        end: Ending time in seconds.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setTimeRange
    """
    ...

def timelineRange() -> Vector2:
    """Return a 2-tuple containing the start and end frames of the global frame range.

    Returns:
        Vector2 with (start_frame, end_frame).

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#timelineRange
    """
    ...

def playbackRange() -> Vector2:
    """Return a 2-tuple containing the start and end frame of the playback range.

    Returns:
        Vector2 with (start_frame, end_frame) for playback.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#playbackRange
    """
    ...

def setPlaybackRange(start: float, end: float) -> None:
    """Set the playback range.

    Args:
        start: Starting frame for playback.
        end: Ending frame for playback.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setPlaybackRange
    """
    ...

def isRangeRestricted() -> bool:
    """Return true if playback is restricted to within the playbar's start and end frame.

    Returns:
        Whether playback range restriction is enabled.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#isRangeRestricted
    """
    ...

def setRestrictRange(on: bool) -> None:
    """Turn restriction on the playback range on or off.

    Args:
        on: Whether to restrict playback to the defined range.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setRestrictRange
    """
    ...

def selectionRange() -> Vector2 | None:
    """This function exists for backwards compatibility.

    Returns:
        Selection range or None if no selection.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#selectionRange
    """
    ...

def selectionRanges() -> tuple[Vector2, ...]:
    """Returns a list of 2-tuples containing the start and end frame of each selection range.

    Returns:
        Tuple of Vector2 objects representing selection ranges.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#selectionRanges
    """
    ...

# Frame increment

def frameIncrement() -> float:
    """Return the frame increment step size.

    Returns:
        Frame increment value.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#frameIncrement
    """
    ...

def setFrameIncrement(increment: float) -> None:
    """Set the frame increment step size.

    Args:
        increment: Frame increment value.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setFrameIncrement
    """
    ...

def usesIntegerFrames() -> bool:
    """Return True if playback uses integer frame values.

    Returns:
        Whether integer frame values are used.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#usesIntegerFrames
    """
    ...

def setUseIntegerFrames(on: bool) -> None:
    """Turn integer frame values on or off.

    Args:
        on: Whether to use integer frame values.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setUseIntegerFrames
    """
    ...

# Keyframe navigation

def jumpToNextKeyframe() -> None:
    """Sets the frame to the time of the next scoped keyframe.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#jumpToNextKeyframe
    """
    ...

def jumpToPreviousKeyframe() -> None:
    """Sets the frame to the time of the previous scoped keyframe.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#jumpToPreviousKeyframe
    """
    ...

def selectedKeyframes() -> dict[Parm, tuple[BaseKeyframe, ...]]:
    """Returns a dictionary of (hou.Parm, keyframes) which are currently selected in the playbar.

    Returns:
        Dictionary mapping parameters to their selected keyframes.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#selectedKeyframes
    """
    ...

# Bookmarks

def frameBookmark(bookmark: Bookmark) -> None:
    """Frames the given bookmark by setting the playback range to the start and end time of that bookmark.

    Args:
        bookmark: Bookmark to frame.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#frameBookmark
    """
    ...

# Playbar position

def moveToBottom() -> None:
    """Move the playbar to the bottom of the desktop.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#moveToBottom
    """
    ...

def moveToPane(pane: PaneTab) -> None:
    """Move the playbar to the bottom of the specified pane.

    Args:
        pane: Pane to move playbar to.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#moveToPane
    """
    ...

# Continuous cook

def setContinuousCook(enable: bool) -> None:
    """Enables the continuous cooking of nodes that are flagged to do so.

    Args:
        enable: Whether to enable continuous cooking.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setContinuousCook
    """
    ...

def isContinuousCook() -> bool:
    """Returns if continuous cook nodes are currently engaged.

    Returns:
        Whether continuous cooking is enabled.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#isContinuousCook
    """
    ...

# Channel list

def channelList() -> ChannelList:
    """Return a copy of the current channel list.

    Returns:
        Current channel list.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#channelList
    """
    ...

def setChannelList(channel_list: ChannelList) -> None:
    """Set the current channel list.

    Args:
        channel_list: Channel list to set.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#setChannelList
    """
    ...

def channelListFromSelection() -> ChannelList:
    """Return a channel list from the selected nodes.

    Returns:
        Channel list from selected nodes.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#channelListFromSelection
    """
    ...

def channelListFromNodes(nodes: tuple[Node, ...]) -> ChannelList:
    """Return a channel list from a list of nodes.

    Args:
        nodes: Tuple of nodes to create channel list from.

    Returns:
        Channel list from specified nodes.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#channelListFromNodes
    """
    ...

def channelListFromParmTuples(parms: tuple[ParmTuple, ...]) -> ChannelList:
    """Return a channel list from a list of parameter tuples.

    Args:
        parms: Tuple of parameter tuples to create channel list from.

    Returns:
        Channel list from specified parameter tuples.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#channelListFromParmTuples
    """
    ...

def channelListFromParms(parms: tuple[Parm, ...]) -> ChannelList:
    """Return a channel list from a list of parameters.

    Args:
        parms: Tuple of parameters to create channel list from.

    Returns:
        Channel list from specified parameters.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#channelListFromParms
    """
    ...

# Animation toolbar

def isAnimBarShown() -> bool:
    """Return whether or not the Animation Toolbar is currently displayed.

    Returns:
        Whether Animation Toolbar is visible.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#isAnimBarShown
    """
    ...

def showAnimBar(show: bool) -> None:
    """Shows or hides the Animation Toolbar.

    Args:
        show: Whether to show the Animation Toolbar.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#showAnimBar
    """
    ...

def animBar() -> AnimBar:
    """Return a hou.AnimBar which provides control over the playbar's Animation Toolbar.

    Returns:
        AnimBar object for controlling the Animation Toolbar.

    See https://www.sidefx.com/docs/houdini/hom/hou/playbar.html#animBar
    """
    ...
