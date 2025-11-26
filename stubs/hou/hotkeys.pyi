"""Module containing hotkey related functions."""

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import PluginHotkeyDefinitions

def installDefinitions(definitions: PluginHotkeyDefinitions) -> None:
    """Installs any command categories, commands, binding contexts and default bindings used by a plugin."""
    ...

def uninstallDefinitions(definitions: PluginHotkeyDefinitions) -> None:
    """Uninstalls any command categories, commands, binding contexts and default bindings used by a plugin."""
    ...

def hotkeySymbol(context_label_path: str, command_label: str | None = None) -> str | None:
    """Does a reverse-lookup to retrieve the hotkey symbol given the human-readable context label(s)."""
    ...

def changeIndex() -> int:
    """Return the monotonically increasing change index from the hotkey manager."""
    ...

def assignments(context: str, hotkey_symbol: str, resolve_refs: bool = True) -> tuple[str, ...]:
    """Return a list of shortcuts assigned to the specified hotkey symbol in a context."""
    ...

def assignmentsAsTuples(context: str, hotkey_symbol: str, resolve_refs: bool = True) -> tuple[tuple[str, ...], ...]:
    """Return a list of shortcuts assigned to the specified hotkey symbol in a context, with each shortcut as a tuple of strings."""
    ...

def hotkeyLabel(hotkey_symbol: str) -> str:
    """Return the human-readable label for a symbol string."""
    ...

def hotkeyDescription(hotkey_symbol: str) -> str:
    """Returns the long description/help for a the given symbol string."""
    ...

def isKeyMatch(key: str, hotkey_symbol: str) -> bool:
    """Return True if the key matches the hotkey symbol."""
    ...

def saveAsKeymap(name: str, path: str | None = None) -> bool:
    """Save the currently defined hotkeys as a keymap."""
    ...

def loadKeymap(name: str, path: str | None = None) -> bool:
    """Load the specified keymap."""
    ...

def importKeymap(name: str, path: str | None = None) -> bool:
    """Copy the specified keymap into the user preferences directory and save it with an appropriate name."""
    ...

def keymaps() -> tuple[str, ...]:
    """Return a list of tuples of all the keymaps found."""
    ...

def currentKeymap() -> str:
    """Return the name of the currently loaded keymap."""
    ...

def availableKeycodes(context: str, hotkey_symbol: str, layout_keys: tuple[int, ...], modifiers: int = 0) -> tuple[int, ...]:
    """Return all available shortcut keycodes with their conflict status bits set."""
    ...

def stringToKeycode(key: str, modifiers: int = 0) -> int:
    """Convert a keystring to a hotkeymanager keycode."""
    ...

def keycodeToString(keycode: int, modifiers: int = 0) -> str:
    """Convert a hotkeymanager keycode to a key string."""
    ...

def splitKeySequenceString(key: str) -> tuple[str, ...]:
    """Splits a string specifying a key sequence into its component key strings."""
    ...

def resolveAssignments(contexts: tuple[str, ...], hotkey_symbols: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
    """Return a tuple of strings that represent the hotkeys that will invoke each action from a tuple of hotkey symbols when resolved against a specific list of hotkey contexts."""
    ...
