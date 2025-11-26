"""Functions related to playing audio using Houdini's playbar."""

def setAudioFileName(path: str) -> None:
    """Set the Audio Panel to play the sound inside an audio file."""
    ...

def setChopPath(path: str) -> None:
    """Set the Audio Panel to play the sound inside a CHOP node."""
    ...

def useAudioFile() -> None:
    """Set the Audio Panel to use a disk file for the audio."""
    ...

def useChops() -> None:
    """Set the Audio Panel to use a CHOP node for the audio."""
    ...

def setMono(on: bool) -> None:
    """Set whether the audio will play in mono or stereo mode."""
    ...

def setLeftVolume(value: float) -> None:
    """Set the volume for the left audio channel."""
    ...

def setRightVolume(value: float) -> None:
    """Set the volume for the right channel."""
    ...

def setVolumeTied(on: bool) -> None:
    """Set whether changing the volume of one channel affects the volume of the other channel."""
    ...

def setMeter(on: bool) -> None:
    """Set whether the meter will show the volume levels during the audio playback."""
    ...

def setAudioOffset(offset: float) -> None:
    """Set the time offset of the sound to sync the audio."""
    ...

def setAudioFrame(frame: float) -> None:
    """Set the frame to sync the audio."""
    ...

def useTestMode() -> None:
    """Put the Audio Panel into a mode that tests the audio playback."""
    ...

def useTimeLineMode() -> None:
    """Put the Audio Panel into a scrub mode."""
    ...

def useTimeSliceMode() -> None:
    """Put the Audio Panel into realtime mode."""
    ...

def turnOffAudio() -> None:
    """Turn off the audio playback."""
    ...

def play() -> None:
    """When the Audio Panel is in the test mode, start playing the Audio Panel's specified audio file or CHOP."""
    ...

def stop() -> None:
    """When the Audio Panel is in the test mode, stop the test playback if any audio is currently playing."""
    ...

def reverse() -> None:
    """When the Audio Panel is in the test mode, start playing the sound in reverse."""
    ...

def setLooping(on: bool) -> None:
    """When the Audio Panel is in the test mode, set whether the test should start playing from the beginning once the end is reached."""
    ...

def setRewind(on: bool) -> None:
    """When the Audio Panel is in the test mode, set whether the sound should rewind to the beginning when the test is stopped."""
    ...

def setScrubLength(value: float) -> None:
    """When the sustain period is non-zero, the audio from this many frames will be repeated when the scrubbing comes to a standstill at a single frame."""
    ...

def setScrubRepeat(on: bool) -> None:
    """Set whether the sound chunk is repeated during scrubbing."""
    ...

def setScrubSustain(value: float) -> None:
    """Set the length of time that the sound chunk is repeatedly played when scrubbing comes to a standstill on a particular single frame."""
    ...
