"""Module containing user interface related functions."""

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from . import (
        Desktop, Pane, PaneTab, FloatingPanel, Dialog, Color,
        severityType, confirmType, fileChooserMode, fileType,
        ParameterEditor, NetworkEditor, Parm, ParmTuple, Node,
        ShellIO, scrollPosition, updateMode as _updateMode, orientUpAxis,
        handleOrientToNormalAxis as _handleOrientToNormalAxis,
        valueLadderDataType, valueLadderType
    )

# Pane layout
def curDesktop() -> Desktop:
    """Return the current desktop."""
    ...

def desktop(name: str) -> Desktop:
    """Return the desktop with the specified name."""
    ...

def desktops() -> tuple[Desktop, ...]:
    """Return all the desktops."""
    ...

def panes() -> tuple[Pane, ...]:
    """Return a tuple of all visible panes, including those in all floating windows."""
    ...

def paneTabs() -> tuple[PaneTab, ...]:
    """Return a tuple of all visible pane tabs, including those in all floating windows."""
    ...

def currentPaneTabs() -> tuple[PaneTab, ...]:
    """Return a tuple of all visible pane tabs that are selected in their containing panes, including those in all floating windows."""
    ...

def floatingPaneTabs() -> tuple[PaneTab, ...]:
    """Return all the pane tabs in floating panels."""
    ...

def paneTabOfType(type: Any, index: int = 0) -> PaneTab | None:
    """Find and return the pane tab with the desired type."""
    ...

def findPane(pane_id: int) -> Pane | None:
    """Return the pane with the given unique id, or None if no such pane exists."""
    ...

def findPaneTab(name: str) -> PaneTab | None:
    """Return the pane tab with the given name, or None if no such tab exists."""
    ...

def floatingPanels() -> tuple[FloatingPanel, ...]:
    """Return all the visible floating panels."""
    ...

def paneUnderCursor() -> Pane | None:
    """Return the hou.Pane object located under the mouse cursor."""
    ...

def paneTabUnderCursor() -> PaneTab | None:
    """Similar to hou.ui.paneUnderCursor but return the hou.PaneTab object instead located under the mouse cursor."""
    ...

# Scripted UI
def displayMessage(
    text: str,
    buttons: tuple[str, ...] = ("OK",),
    severity: severityType = ...,
    default_choice: int = 0,
    close_choice: int = -1,
    help: str | None = None,
    title: str | None = None,
    details: str | None = None,
    details_label: str | None = None,
    details_expanded: bool = False,
    suppress: confirmType = ...
) -> int:
    """Pop up a small window with a message and one or more buttons and wait for the user to press a button."""
    ...

def displayConfirmation(
    text: str,
    severity: severityType = ...,
    help: str | None = None,
    title: str | None = None,
    details: str | None = None,
    details_label: str | None = None,
    suppress: confirmType = ...
) -> bool:
    """Pop up a window with a message, OK and Cancel buttons, and wait for the user to press a button."""
    ...

def readInput(
    message: str,
    buttons: tuple[str, ...] = ("OK",),
    severity: severityType = ...,
    default_choice: int = 0,
    close_choice: int = -1,
    help: str | None = None,
    title: str | None = None,
    initial_contents: str | None = None
) -> tuple[int, str]:
    """Pop up a small window with a textbox and wait for the user to enter a line of text."""
    ...

def selectFile(
    start_directory: str | None = None,
    title: str | None = None,
    collapse_sequences: bool = False,
    file_type: fileType = ...,
    pattern: str | None = None,
    default_value: str | None = None,
    multiple_select: bool = False,
    image_chooser: bool | None = None,
    chooser_mode: fileChooserMode = ...,
    width: int = 0,
    height: int = 0
) -> str:
    """Pop up a window with a file chooser dialog and wait for the user to choose a file name."""
    ...

def selectColor(initial_color: Color | None = None, options: dict | None = None) -> Color | None:
    """Pop up a window with a color chooser, and waits for the user to choose a color and hit the OK or Cancel button."""
    ...

def isUIAvailable() -> bool:
    """Return True if the UI is available."""
    ...

# Status line
def setStatusMessage(message: str, severity: severityType = ...) -> None:
    """Display a message in Houdini's status bar."""
    ...

def statusMessage() -> tuple[str, severityType]:
    """Return the current message and severity from the status bar."""
    ...

# Callbacks
def addEventLoopCallback(callback: Callable[[], None]) -> None:
    """Register a Python callback to be called whenever Houdini's event loop is idle."""
    ...

def removeEventLoopCallback(callback: Callable[[], None]) -> None:
    """Remove a Python callback that was previously registered with hou.ui.addEventLoopCallback."""
    ...

def eventLoopCallbacks() -> tuple[Callable[[], None], ...]:
    """Return a tuple of all the Python callbacks that have been registered with hou.ui.addEventLoopCallback."""
    ...

def addSelectionCallback(callback: Callable[[], None]) -> None:
    """Register a Python callback to be called whenever Houdini's global network item selection changes."""
    ...

def removeSelectionCallback(callback: Callable[[], None]) -> None:
    """Remove a Python callback that was previously registered with hou.ui.addSelectionCallback."""
    ...

def selectionCallbacks() -> tuple[Callable[[], None], ...]:
    """Return a tuple of all the Python callbacks that have been registered with hou.ui.addSelectionCallback."""
    ...

# Updating the viewport
def triggerUpdate() -> None:
    """Force the viewports to update and perform any cooks necessary."""
    ...

def reloadViewportColorSchemes() -> None:
    """Reloads all 3DSceneColors configuration files (in $HFS/houdini/config)."""
    ...

def isAutoKey() -> bool:
    """Returns if auto-key is currently enabled (changing an animated parameter will create a key at the current frame if it doesn't exist)."""
    ...

# Settings
def currentColorScheme() -> str:
    """Return the currently applied Houdini color scheme name."""
    ...

def reloadColorScheme() -> None:
    """Reloads all Houdini UI color settings from the configuration files (by default, in $HFS/houdini/config and $HOUDINI_USER_PREF_DIR/houdini/config)."""
    ...

def resourceValueFromName(name: str) -> str:
    """Return a string value from a symbolic resource name."""
    ...

def colorFromName(name: str) -> Color:
    """Return a color value from a symbolic color name."""
    ...

def orientationUpAxis() -> orientUpAxis:
    """Return a hou.orientUpAxis indicating the current orientation mode's up axis."""
    ...

def handleOrientToNormalAxis() -> _handleOrientToNormalAxis:
    """Return a hou.handleOrientToNormalAxis indicating the handle axis that is to be aligned to component normals when orienting."""
    ...

def globalScaleFactor() -> float:
    """Return the scale factor that is set by Houdini's Global UI Size preference."""
    ...

def scaledSize(size: int) -> int:
    """Scale the specified size by the global UI scale factor and return the scaled size."""
    ...

# Clipboard
def copyTextToClipboard(text: str) -> None:
    """Sets the supplied text into the system clipboard."""
    ...

def getTextFromClipboard() -> str:
    """Returns any text currently copied into the system clipboard."""
    ...

# Python shell
def shellIO() -> ShellIO:
    """Return the hou.ShellIO object used to implement Houdini's graphical Python shell."""
    ...

# Windows
def parameterPaneTabs(node: Node, include_node_editors: bool = True) -> tuple[ParameterEditor | NetworkEditor, ...]:
    """Return parameter editors displaying a given node."""
    ...

def scrollToParmsInEditors(parms: Parm | ParmTuple | list, pos: scrollPosition = ...) -> bool:
    """Given a list or a single instance of hou.Parm or hou.ParmTuple adjust the matching parameter editor scroll bars to make the parameters visible in the parameter editor scroll region."""
    ...

# Dialog scripts
def createDialog(ui_file_name: str) -> Dialog:
    """Parse the given .ui file and return the dialog defined in the file."""
    ...

def findDialog(ui_file_name: str) -> Dialog | None:
    """Return the dialog defined by the given .ui file name and created by hou.ui.createDialog."""
    ...

def dialogs() -> tuple[Dialog, ...]:
    """Return all dialogs created by hou.ui.createDialog."""
    ...

# Misc
def isUserInteracting() -> bool:
    """Return True if the user is currently interacting with the UI in a way that is likely to cause a stream of node or parameter changes."""
    ...

def setUserInteracting(on: bool) -> None:
    """Sets a flag checked by isUserInteracting()."""
    ...

def isValidObject(hom_obj: Any) -> bool:
    """Returns True if the HOM object is still valid."""
    ...

# Radial menus
def radialMenu(name: str) -> Any:  # Returns hou.RadialMenu or None
    """Returns a hou.RadialMenu object representing the named menu, or None if the menu does not exist."""
    ...

def radialMenus() -> tuple[Any, ...]:  # tuple of hou.RadialMenu
    """Returns a tuple of hou.RadialMenu objects representing existing menus."""
    ...

def createRadialMenu(name: str, label: str) -> Any:  # Returns hou.RadialMenu
    """Creates a new radial menu object with the given name and label."""
    ...

def createRadialItem(submenu: bool = False, callback: Any = None) -> Any:  # Returns hou.RadialScriptItem
    """Creates a temporary radial menu item."""
    ...

def injectRadialItem(location: Any, item: Any) -> None:
    """Injects a temporary radial menu item into the current menu."""
    ...

def injectRadialMenu(name: str) -> None:
    """Injects a registered menu and override the current menu."""
    ...

def setDefaultRadialSubmenu(location: Any) -> None:
    """Sets the top-level submenu that opens when the radial menu is opened."""
    ...

def updateMainMenuBar() -> None:
    """Forces label expressions to be re-evaluated for the main Houdini menu bar."""
    ...

def hideAllMinimizedStowbars() -> bool:
    """Return the value of a global flag that hides all the minimized stowbars and split panes."""
    ...

def setHideAllMinimizedStowbars(on: bool) -> None:
    """Set the value of a global flag that hides all the minimized stowbars and split panes."""
    ...

# More scripted UI functions
def readMultiInput(
    message: str,
    input_labels: tuple[str, ...],
    password_input_indices: tuple[int, ...] = (),
    buttons: tuple[str, ...] = ("OK",),
    severity: severityType = ...,
    default_choice: int = 0,
    close_choice: int = -1,
    help: str | None = None,
    title: str | None = None,
    initial_contents: tuple[str, ...] = ()
) -> tuple[int, tuple[str, ...]]:
    """Pop up a small window with a textbox and wait for the user to enter a text into several input fields."""
    ...

def selectMultipleNodes(
    relative_to_node: Node | None = None,
    initial_node: Node | None = None,
    node_type_filter: Any = None,
    title: str | None = None,
    width: int = 0,
    height: int = 0,
    custom_node_filter_callback: Any = None
) -> tuple[str, ...] | None:
    """This method is deprecated in favor of hou.ui.selectNode with multiple_select=True."""
    ...

def selectFromTree(
    choices: Any,
    picked: tuple = (),
    exclusive: bool = False,
    message: str | None = None,
    title: str | None = None,
    clear_on_cancel: bool = False,
    width: int = 0,
    height: int = 0,
    allow_branch_selection: bool = False,
    allow_compound_selection: bool = True
) -> tuple[str, ...]:
    """Pop up a window with a set of choices in a tree chooser and prompt the user to choose zero or more of them."""
    ...

def selectAttrib(
    initial_selection: tuple = (),
    multiple_select: bool = False,
    expand_components: bool = True,
    width: int = 0,
    height: int = 0
) -> tuple[Any, int]:  # tuple of (hou.Attrib, int)
    """Pop up a chooser dialog that prompts the user to select a geometry attribute in the scene."""
    ...

def selectNodeData(
    title: str | None = None,
    message: str | None = None,
    width: int = 0,
    height: int = 0,
    initial_selection: int = 0,
    node_type_filter: Any = None,
    multiple_select: bool = False,
    include_data_type_headers: bool = True,
    include_parms: bool = True,
    include_object_transforms: bool = True,
    include_geometry_bounding_boxes: bool = True,
    include_geometry_attributes: bool = True,
    expand_components: bool = True,
    custom_data_callback: Any = None,
    custom_node_filter_callback: Any = None,
    help_url: str | None = None
) -> dict:
    """Pop up a chooser dialog that prompts the user to select data from a node."""
    ...

def selectParmTag(width: int = 0, height: int = 0) -> tuple[str, ...]:
    """Pop up a window with a tree view of recognized parameter tags and prompt the user to choose a tag."""
    ...

def selectParm(
    category: Any = None,
    bound_parms_only: bool = False,
    relative_to_node: Node | None = None,
    message: str | None = None,
    title: str | None = None,
    initial_parms: tuple = (),
    multiple_select: bool = True,
    width: int = 0,
    height: int = 0
) -> tuple[str, ...]:
    """Pop up a window with a parameter tree view and prompts the user to select parameters."""
    ...

def selectParmTuple(
    category: Any = None,
    bound_parms_only: bool = False,
    relative_to_node: Node | None = None,
    message: str | None = None,
    title: str | None = None,
    initial_parm_tuples: tuple = (),
    multiple_select: bool = True,
    width: int = 0,
    height: int = 0
) -> tuple[str, ...]:
    """Pop up a window with a parameter tree view and prompts the user to select parameter tuples."""
    ...

def colorEditorOptions() -> dict:
    """Returns a dictionary containing all the current named options values for the color editor."""
    ...

def selectRawColor(initial_color: Color | None = None) -> Color | None:
    """Pop up a window with a raw color chooser, and waits for the user to choose a color and hit the OK or Cancel button."""
    ...

def openBookmarkEditor(bookmark: Any) -> None:
    """Open the Houdini Bookmark Edit Dialog and return immediately."""
    ...

def openColorEditor(
    color_change_callback: Callable,
    include_alpha: bool = False,
    initial_color: Color | None = None,
    initial_alpha: float = 1.0,
    options: dict | None = None
) -> None:
    """Open the Houdini color editor and return immediately."""
    ...

def openRawColorEditor(
    color_change_callback: Callable,
    include_alpha: bool = False,
    initial_color: Color | None = None,
    initial_alpha: float = 1.0
) -> None:
    """Open the Houdini color editor without color correction and return immediately."""
    ...

def openValueLadder(
    initial_value: float,
    value_changed_callback: Callable,
    type: valueLadderType = ...,
    data_type: valueLadderDataType = ...
) -> None:
    """Displays a value ladder control, the UI that typically appears when you press on a field in Houdini."""
    ...

def updateValueLadder(cursor_x: int, cursor_y: int, alt_key: bool, shift_key: bool) -> None:
    """Updates the value in the currently opened ladder value window based on the given cursor position and boolean arguments."""
    ...

def closeValueLadder() -> None:
    """Closes the current value ladder window that was open by a previous call to hou.ui.openValueLadder."""
    ...

def openParameterExpressionEditor(parm: Parm) -> None:
    """Open the expression editor to edit the expression of the given parameter."""
    ...

def openPreferences(page: str) -> None:
    """Open the preferences dialog and show the given page."""
    ...

# Windows - additional functions
def setMultiParmTabInEditors(parm: Parm, tab_index: int) -> bool:
    """Given a hou.Parm representing a multi parameter parent, set the multi parameter tab index in the parameter editor dialogs."""
    ...

def switchTabsToParmInEditors(parm: Parm) -> bool:
    """Given a hou.Parm switch all the parent tabs folder to show the parameter in the opened parameter editors."""
    ...

def setParmFilterInEditors(node: Node, parm_names: str) -> bool:
    """Given a node and a list of comma separated parameter names apply a search filter on the corresponding parameter editors."""
    ...

def showFloatingParameterEditor(node: Node, reuse: bool) -> ParameterEditor:
    """Show a floating hou.ParameterEditor for a given hou.OpNode."""
    ...

def openCaptureWeightSpreadsheet(node: Node, pattern: str | None = None) -> None:
    """Given an instance of a hou.SopNode that is a captureoverride type, open the edit capture weight spreadsheet for the node."""
    ...

def openFileEditor(
    title: str,
    file_path: str,
    action_callback: Callable | None = None,
    params: dict | None = None
) -> None:
    """Open a window for editing and saving a text file."""
    ...

def showInFileBrowser(file_path: str) -> None:
    """Launch the system's file browser, navigating to the parent directory of the specified file and selecting it."""
    ...

def openViewerStateCodeGenDialog(
    category: str,
    action_callback: Callable,
    operator_name: str | None = None
) -> None:
    """Open a modal dialog window for generating a template implementation and registration code for a python viewer state."""
    ...

# Help
def displayNodeHelp(node_type: Any) -> None:
    """Display the help for the specified node type."""
    ...

# Callbacks - additional functions
def postEventCallback(callback: Callable[[], None]) -> None:
    """Register a Python callback to be called next in Houdini's event loop."""
    ...

def removePostedEventCallback(callback: Callable[[], None]) -> None:
    """Remove a posted event callback from the queue if it is still there."""
    ...

def postRedrawFence() -> None:
    """Puts a redraw fence on the event queue."""
    ...

def addTriggerUpdateCallback(callback: Callable[[], None]) -> None:
    """Add a callback to be run when the Update Once button is clicked in Houdini, or the hou.ui.triggerUpdate method is called."""
    ...

def removeTriggerUpdateCallback(callback: Callable[[], None]) -> None:
    """Remove a callback previously added with the hou.ui.addTriggerUpdateCallback method."""
    ...

def waitUntil(condition_callback: Callable[[], bool]) -> None:
    """Keep calling the supplied callback until it returns True."""
    ...

def removeAllSelectionCallbacks() -> None:
    """Remove all Python callbacks previously registered with hou.ui.addSelectionCallback."""
    ...

# Updating the viewport - additional functions
def updateMode() -> _updateMode:
    """This method is deprecated in favor of hou.updateModeSetting()."""
    ...

def setUpdateMode(mode: _updateMode) -> None:
    """This method is deprecated in favor of hou.setUpdateMode()."""
    ...

# Settings - additional functions
def inchesToPixels(inches: float) -> float:
    """Return the supplied inches argument, expressing a distance on the screen, converted to a number of pixels."""
    ...

def pixelsToInches(pixels: float) -> float:
    """Return the supplied pixels argument, expressing a number of pixels on the screen, converted to a distance in inches."""
    ...

def loadPaletteFile(file: str) -> tuple[Color, ...]:
    """Load a palette file and return the colors listed in the palette."""
    ...

def savePaletteFile(file: str, colors: tuple[Color, ...]) -> None:
    """Save a palette file with the contents of the colors parameter, a tuple of hou.Color objects."""
    ...

# Python shell - additional functions
def writePythonShellHistoryFile(filename: str | None = None) -> None:
    """Save the command history from the current Python Shell to disk."""
    ...

def readPythonShellHistoryFile(filename: str | None = None) -> None:
    """Load the contents from the specified file into the command history of the Python Shell."""
    ...

# Drag and drop
def hasDragSourceData(label: str) -> bool:
    """Query the current drag source to determine if the specified data type is available."""
    ...

def getDragSourceData(label: str, index: int) -> Any:
    """Query the current drag source to obtain the dragged data."""
    ...

# Qt integration (deprecated)
def mainQtWindow() -> Any:
    """This method is deprecated."""
    ...

def createQtIcon(name: str, width: int = 32, height: int = 32) -> Any:
    """This method is deprecated."""
    ...

def qtStyleSheet() -> str:
    """This method is deprecated."""
    ...

# Viewer states
def registerViewerState(template: Any) -> None:
    """Registers a hou.ViewerStateTemplate object representing a custom viewer state."""
    ...

def registerViewerStateFile(file_path: str) -> None:
    """Registers a viewer state type implemented in a given python file."""
    ...

def registerViewerStates() -> None:
    """Scans the viewer state folders ($HH/viewer_states and $HOUDINI_USER_PREF_DIR/viewer_states) to register all viewer states they both contain."""
    ...

def unregisterViewerState(state_name: str) -> None:
    """Unregisters an existing viewer state type."""
    ...

def unregisterViewerStateFile(file_path: str) -> None:
    """Unregisters a viewer state previously registered with a given python file."""
    ...

def isRegisteredViewerState(state_name: str) -> bool:
    """Returns True if state_name has previously been registered with hou.ui.registerViewerState."""
    ...

def reloadViewerState(state_name: str) -> None:
    """Update a registered viewer state by reloading its python module file from a viewer_states folder."""
    ...

def reloadViewerStates(state_names: tuple[str, ...] | None = None) -> None:
    """Reload multiple viewer states as specified in the state_names array."""
    ...

def viewerStateInfo(state_names: tuple[str, ...]) -> str:
    """Return a JSON dictionary string describing all registered viewer states keyed by state type."""
    ...

def viewerStateInfoFromFile(state_filepath: str) -> tuple[str, str]:
    """Returns the viewer state information for a given python state file."""
    ...

# Viewer handles
def registerViewerHandle(template: Any) -> None:
    """Registers a hou.ViewerHandleTemplate object representing a custom viewer handle."""
    ...

def registerViewerHandles() -> None:
    """Scans the viewer handle folders (e.g. $HH/viewer_handles) to register all handles."""
    ...

def registerViewerHandleFile(handle_file: str) -> None:
    """Registers a viewer handle type implemented in a given python file."""
    ...

def unregisterViewerHandleFile(handle_file: str) -> None:
    """Unregisters a viewer handle previously registered with a given python file."""
    ...

def unregisterViewerHandle(handle_name: str) -> None:
    """Unregisters an existing viewer handle type."""
    ...

def reloadViewerHandle(handle_name: str) -> None:
    """Update a registered viewer handle by reloading its python module file from a viewer_handle folder."""
    ...

def isRegisteredViewerHandle(handle_name: str) -> bool:
    """Returns True if handle_name has previously been registered with hou.ui.registerViewerHandle."""
    ...

def viewerHandleInfo(handle_names: tuple[str, ...]) -> str:
    """Return a JSON dictionary string describing all registered viewer handles in Houdini."""
    ...

def openViewerHandleCodeGenDialog(categories: tuple, action_callback: Callable) -> None:
    """Open a modal dialog window for generating a template implementation and registration code for a python viewer handle."""
    ...

# Resources
def addResourceEventCallback(callback: Callable) -> None:
    """Register a Python callback to be called whenever a hou.resourceEventMessage event occurs."""
    ...

def removeResourceEventCallback(callback: Callable) -> None:
    """Remove a specific Python callback previously registered with hou.ui.addResourceEventCallback."""
    ...

def fireResourceCustomEvent(resource_type: Any, user_data: Any, queue: bool = True) -> None:
    """This function triggers a custom resource event which can be used for implementing specific workflows."""
    ...

def printResourceMessage(resource_type: Any, message: str, message_type: severityType = ...) -> None:
    """Print a user message in the message window of a Viewer State Browser or Viewer Handle Browser."""
    ...

# Packages
def loadPackage(file_path: str, force_unload: bool = False) -> None:
    """Packages are normally loaded on startup by Houdini, this API loads packages at runtime."""
    ...

def loadPackageArchive(file_path: str, extract_path: str | None = None) -> list[str]:
    """Extracts the content of a package archive file on disk and load the embedded plugin resources and installation package."""
    ...

def unloadPackage(file_path: str) -> None:
    """Unloads the plugin resources previously loaded with hou.ui.loadPackage."""
    ...

def reloadPackage(file_path: str) -> None:
    """Update a package previously loaded."""
    ...

def activatePackage(file_path: str) -> None:
    """The API is typically used by the Package Browser to activate a loaded package previously deactivated with hou.ui.deactivatePackage."""
    ...

def deactivatePackage(file_path: str) -> None:
    """Deactivates a loaded package."""
    ...

def packageInfo(file_paths: tuple[str, ...]) -> str:
    """Return a JSON dictionary string describing one or multiple package plugins previously loaded in Houdini."""
    ...

# Hotkeys
def hotkeys(hotkey_symbol: str) -> tuple[str, ...]:
    """Return a tuple of strings that represent the hotkeys currently assigned to the action associated with the hotkey symbol."""
    ...

def hotkeyDescription(hotkey_symbol: str) -> str:
    """Return a string that contains a description of the action associated with the hotkey symbol."""
    ...

def isKeyMatch(key: str, hotkey_symbol: str) -> bool:
    """Return True if the key described by the string key matches one of the hotkeys assigned to the provided hotkey symbol."""
    ...

# Layout LOP Asset Galleries
def sharedLayoutDataSource() -> Any:  # Returns hou.AssetGalleryDataSource
    """Return the hou.AssetGalleryDataSource object that is currently being used to populate the asset catalog browsers in all Layout LOP nodes."""
    ...

def setSharedLayoutDataSource(datasource: Any) -> None:
    """Set the hou.AssetGalleryDataSource object that should be used to populate the asset catalog browsers in all Layout LOP nodes."""
    ...

def reloadSharedLayoutDataSource() -> None:
    """Forces all Layout LOP asset catalog browsers to reload from the underlying shared hou.AssetGalleryDataSource."""
    ...

# Asset Galleries
def sharedAssetGalleryDataSource(gallery_name: str) -> Any:  # Returns hou.AssetGalleryDataSource
    """Return the hou.AssetGalleryDataSource object that is currently being used to populate the asset catalog browsers specified by gallery_name."""
    ...

def setSharedAssetGalleryDataSource(datasource: Any, gallery_name: str) -> None:
    """Set the hou.AssetGalleryDataSource object that should be used to populate the asset catalog browsers specified by gallery_name."""
    ...

def reloadSharedAssetGalleryDataSource(gallery_name: str) -> None:
    """Forces all asset catalog browsers specified by gallery_name to reload from the underlying shared hou.AssetGalleryDataSource."""
    ...
