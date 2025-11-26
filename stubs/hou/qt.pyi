"""Qt integration module providing Houdini-styled Qt widgets and utilities.

This module provides lower-level Qt building blocks that are used by the ui module.
It gives access to Houdini-styled Qt widgets, color/style utilities, key event handling,
and integration with Houdini's UI system.

See: https://www.sidefx.com/docs/houdini/hom/hou/qt/index.html
"""

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from typing import Callable, Sequence
    from hou import Color, Node
    import PySide6.QtWidgets as QtWidgets
    import PySide6.QtCore as QtCore
    import PySide6.QtGui as QtGui

# Widget Classes
class ColorField(QtWidgets.QWidget):
    """A widget for color input.

    The widget contains a color swatch button and an input field for RGBA values.
    Inherits from QtWidgets.QWidget.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ColorField.html
    """
    def __init__(self, label: str = "", include_alpha: bool = False) -> None:
        """Create and return a new ColorField object."""
        pass

    def color(self) -> Any:
        """Return the field's current color as a QColor."""
        pass

    def setColor(self, color: Any) -> None:
        """Set the field's current color."""
        pass

class ColorPalette(QtWidgets.QWidget):
    """A convenient widget for quick color selection from a small palette of colors.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ColorPalette.html
    """
    def __init__(
        self,
        colors: list[Any] | None = None,
        size: int = 32,
        by_column: bool = False,
        show_at_pointer: bool = True,
        columns: int | None = None,
        rows: int | None = None,
        allow_editing: bool = True,
        selected_index: int = -1,
        bg_color: Any | None = None,
        empty_color: Any | None = None,
        parent: Any | None = None
    ) -> None:
        """Create and return a new ColorPalette object."""
        pass

    def colorCount(self) -> int:
        """The number of colors in the current color list."""
        pass

    def colorList(self) -> list[Any]:
        """Returns the list of colors used to create the palette."""
        pass

    def setColorList(self, colors: list[Any]) -> None:
        """Replaces the current color list with a new list."""
        pass

    def color(self, n: int) -> Any:
        """Returns the nth color in the color list."""
        pass

    def setColor(self, n: int, color: Any) -> None:
        """Sets the nth color in the color list to the given QColor (or QBrush)."""
        pass

    def swatchSize(self) -> int:
        """The size (in pixels) of the individual swatches (color squares) in the palette."""
        pass

    def setSwatchSize(self, size: int) -> None:
        """Sets the size (in pixels) of the individual swatches (color squares) in the palette."""
        pass

    def isEditingAllowed(self) -> bool:
        """Returns True if the user can alt-click a color to edit it."""
        pass

    def setEditingAllowed(self, allow: bool) -> None:
        """Pass True to allow the user to alt-click a color to edit it, or False to prevent the user from editing colors."""
        pass

    def selectedIndex(self) -> int:
        """Returns the index of the selected color in the current color list."""
        pass

    def setSelectedIndex(self, ix: int) -> None:
        """Selects the color at the given index."""
        pass

    def selectedColor(self) -> Any:
        """Returns the currently selected color."""
        pass

class ColorSwatchButton(QtWidgets.QPushButton):
    """A button used for selecting colors with the Houdini look and feel.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ColorSwatchButton.html
    """
    def __init__(self) -> None:
        """Create and return a new ColorSwatchButton object."""
        pass

class ComboBox(QtWidgets.QWidget):
    """A non-scrollable combo box (menu button and menu) with the Houdini look and feel.

    Based on QtWidgets.QComboBox.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ComboBox.html
    """
    def __init__(self) -> None:
        """Create and return a new ComboBox object."""
        pass

class Dialog(QtWidgets.QDialog):
    """A simple dialog with the Houdini look and feel.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/Dialog.html
    """
    def __init__(self) -> None:
        """Create and return a new Dialog object."""
        pass

class FieldLabel(QtWidgets.QLabel):
    """A simple label for input fields.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/FieldLabel.html
    """
    def __init__(self) -> None:
        """Create and return a new FieldLabel object."""
        pass

class FileChooserButton(QtWidgets.QWidget):
    """A button with the Houdini look and feel that opens the Houdini file chooser dialog when clicked.

    Based on QtWidgets.QToolButton.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/FileChooserButton.html
    """
    def __init__(self) -> None:
        """Create and return a new FileChooserButton object."""
        pass

    def setFileChooserStartDirectory(self, start_dir: str) -> None:
        """Set the initial directory that the file chooser dialog will open in."""
        pass

    def setFileChooserTitle(self, title: str) -> None:
        """Set the window title of the file chooser dialog."""
        pass

    def setFileChooserFilter(self, file_filter: str) -> None:
        """Set the file filter in the chooser dialog."""
        pass

    def setFileChooserPattern(self, file_pattern: str) -> None:
        """Set the pattern used by the file chooser dialog."""
        pass

    def setFileChooserDefaultValue(self, default_value: str) -> None:
        """Set the default value in the file chooser dialog."""
        pass

    def setFileChooserMultipleSelect(self, multiple_select: bool) -> None:
        """Set whether the file chooser dialog accepts multiple selection."""
        pass

    def setFileChooserIsImageChooser(self, is_image_chooser: bool) -> None:
        """Set whether the file chooser dialog will be used to select image files."""
        pass

    def setFileChooserMode(self, chooser_mode: Any) -> None:
        """Set the mode of the file chooser dialog (hou.fileChooserMode)."""
        pass

class FileLineEdit(QtWidgets.QLineEdit):
    """QLineEdit widget customized for use as a file chooser field.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/FileLineEdit.html
    """
    def __init__(self) -> None:
        """Create and return a new FileLineEdit object."""
        pass

class GridLayout(QtWidgets.QGridLayout):
    """A grid layout specific for Houdini UI with layout properties that render consistently across all supported platforms.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/GridLayout.html
    """
    def __init__(self) -> None:
        """Create and return a new GridLayout object."""
        pass

class HelpButton(QtWidgets.QPushButton):
    """A button with the Houdini look and feel that opens a help page when clicked.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/HelpButton.html
    """
    def __init__(self) -> None:
        """Create and return a new HelpButton object."""
        pass

class Icon(QtGui.QIcon):
    """An icon generated from a Houdini icon name.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/Icon.html
    """
    def __init__(
        self,
        icon_name: str,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        """Create and return a new icon for the specified Houdini icon name.

        Args:
            icon_name: The Houdini icon name
            width: Optional icon width in pixels
            height: Optional icon height in pixels
        """
        pass

class InputField(QtWidgets.QWidget):
    """A vector of text fields (one to four) that store either integers, floats or strings.

    Supports integer, float, and string input with multi-component values.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/InputField.html
    """

    # Type enum values
    IntegerType: int
    FloatType: int
    StringType: int

    def __init__(
        self,
        data_type: int,
        num_components: int = 1,
        label: str = "",
        size_policy: Any = None,
    ) -> None:
        """Create an input field.

        Args:
            data_type: IntegerType, FloatType, or StringType
            num_components: Number of components (1 for scalar, >1 for vector)
            label: Optional label text
            size_policy: Optional QSizePolicy for the widget
        """
        pass

    def setValue(self, value: Any, index: int = 0) -> None:
        """Set the value at the specified component index."""
        pass

    def setValues(self, values: Sequence[Any]) -> None:
        """Set all component values at once."""
        pass

    def value(self, index: int = 0) -> Any:
        """Get the value at the specified component index."""
        pass

    def values(self) -> list[Any]:
        """Get all component values as a list."""
        pass

    def setMenu(self, menu: Any) -> None:
        """Set a context menu for the input field."""
        pass

    def menu(self) -> Any:
        """Return the context menu for the input field."""
        pass

    def setAlignment(self, alignment: Any) -> None:
        """Set text alignment (Qt.AlignmentFlag)."""
        pass

    def setValidator(self, validator: Any) -> None:
        """Set a validator for input validation."""
        pass

    def setWidth(self, width: int) -> None:
        """Set the width of the input field in pixels."""
        pass

    def setState(self, state_name: str, state_value: Any, index: int = -1) -> None:
        """Set a state value for the input field.

        Args:
            state_name: Name of the state to set
            state_value: Value for the state
            index: Component index (-1 for all components)
        """
        pass

    def state(self, state_name: str, index: int = 0) -> Any:
        """Get a state value for the input field.

        Args:
            state_name: Name of the state to get
            index: Component index
        """
        pass

    def onContextMenuEvent(self, event: Any, context_menu: Any) -> None:
        """Override to customize context menu behavior.

        Args:
            event: QContextMenuEvent
            context_menu: QMenu to populate
        """
        pass

    def onMousePressEvent(self, event: Any) -> None:
        """Override to customize mouse press behavior.

        Args:
            event: QMouseEvent
        """
        pass

    def onMouseWheelEvent(self, event: Any) -> None:
        """Override to customize mouse wheel behavior.

        Args:
            event: QWheelEvent
        """
        pass

class ListEditor(QtWidgets.QWidget):
    """A convenient user interface (as a dialog or a reusable widget) for displaying/editing a list of strings.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ListEditor.html
    """
    def __init__(
        self,
        strings: tuple[str, ...] = (),
        top_message: str | None = None,
        bottom_message: str | None = None,
        allow_editing: bool = True,
        allow_add_remove: bool = True,
        allow_reorder: bool = True,
        allow_empty_string: bool = True,
        show_checkboxes: bool = False,
        keep_sorted: bool = False,
        initial_string: str = "",
        initial_check: bool = True,
        allow_empty_list: bool = True
    ) -> None:
        """Create and return a new ListEditor object."""
        pass

    def itemCount(self) -> int:
        """Returns the number of rows in the editor."""
        pass

    def setStrings(self, strings: list[str]) -> None:
        """Sets the list of strings to display in the dialog."""
        pass

    def strings(self) -> list[str]:
        """Returns a list of the string contents of each item."""
        pass

    def setStringsAndChecks(self, strings_and_checks: list[tuple[str, bool]]) -> None:
        """Takes a sequence of (str, bool) tuples, where the first item in each tuple is the string content of an item and the second is a boolean indicating whether the item is checked."""
        pass

    def stringsAndChecks(self) -> list[tuple[str, bool]]:
        """Returns a list of tuples, where the first item of each tuple is the string content of an item and the second is a boolean indicating whether the item was checked."""
        pass

    def rowIsChecked(self, row_num: int) -> bool:
        """Returns True if the item in the given row number (starting at 0) is checked."""
        pass

    def setRowChecked(self, row_num: int, checked: bool) -> None:
        """Sets the checked state of the item on the given row (starting at 0)."""
        pass

    def rowString(self, row_num: int) -> str:
        """Returns the string in the given row number (starting at 0)."""
        pass

    def checkedRows(self) -> list[int]:
        """Returns a list of row numbers corresponding to the checked items."""
        pass

    def checkedStrings(self) -> list[str]:
        """Returns a list of strings corresponding to the checked items."""
        pass

    def checkedRow(self) -> int | None:
        """Returns the row number of the first checked item, or None if there are no checked items."""
        pass

    def checkedString(self) -> str | None:
        """Returns the text of the first checked item, or None if there are no checked items."""
        pass

    def addListItem(self, text: str, checked: bool | None = None, insert_at: int = -1) -> None:
        """Adds a single item to the current list."""
        pass

    def removeRow(self, row_num: int) -> None:
        """Removes the row at the given position (starting at 0)."""
        pass

    def clear(self) -> None:
        """Clears the list, leaving the dialog empty."""
        pass

    def setShowCheckboxes(self, show: bool) -> None:
        """Sets whether to show checkboxes next to items in the list."""
        pass

    def showCheckboxes(self) -> bool:
        """Whether the widget shows checkboxes next to items in the list."""
        pass

    def setKeepSorted(self, keep_sorted: bool) -> None:
        """Sets whether the widget should maintain the list in sorted order."""
        pass

    def keepSorted(self) -> bool:
        """Whether the widget maintains the list in sorted order."""
        pass

    def setTopMessage(self, text: str) -> None:
        """Sets the text above the list widget."""
        pass

    def topMessage(self) -> str:
        """Returns the current text in the label above the list."""
        pass

    def setBottomMessage(self, text: str) -> None:
        """Sets the text below the list."""
        pass

    def bottomMessage(self) -> str:
        """Returns the current text in the label below the list."""
        pass

    def setAllowEditing(self, allow: bool) -> None:
        """Sets whether editing (rewriting) the string content of items is allowed."""
        pass

    def isEditingAllowed(self) -> bool:
        """Whether the user is allowed to edit (rewrite) the string contents of items."""
        pass

    def setAllowEmptyList(self, allow: bool) -> None:
        """Sets whether the user is allowed to delete the last item to leave the list empty."""
        pass

    def isEmptyListAllowed(self) -> bool:
        """Whether the user is allowed to delete the last item to leave the list empty."""
        pass

    def setAllowAddRemove(self, allow: bool) -> None:
        """Sets whether the user can add or remove items."""
        pass

    def isAddRemoveAllowed(self) -> bool:
        """Whether the user can add or remove items."""
        pass

    def setAllowReorder(self, allow: bool) -> None:
        """Sets whether the user is allowed to drag items in the list to reorder them."""
        pass

    def isReorderAllowed(self) -> bool:
        """Whether the user is allowed to drag items in the list to reorder them."""
        pass

    def setAllowEmptyString(self, allow: bool) -> None:
        """Sets whether the user can enter an empty string as the contents for an item."""
        pass

    def isEmptyStringAllowed(self) -> bool:
        """Whether the user can enter an empty string as the contents for an item."""
        pass

    def setInitialString(self, text: str) -> None:
        """Sets the initial text of a newly added item."""
        pass

    def initialString(self) -> str:
        """The initial text in the text edit field when the user creates a new item with the Add button."""
        pass

    def setInitialCheck(self, checked: bool) -> None:
        """Sets whether newly created items will be checked by default."""
        pass

    def initialCheck(self) -> bool:
        """Whether newly created items are checked by default."""
        pass

class Menu(QtWidgets.QMenu):
    """A menu with the Houdini look and feel.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/Menu.html
    """
    def __init__(self) -> None:
        """Create and return a new Menu object."""
        pass

class MenuBar(QtWidgets.QMenuBar):
    """A menubar with the Houdini look and feel.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/MenuBar.html
    """
    def __init__(self) -> None:
        """Create and return a new MenuBar object."""
        pass

class MenuButton(QtWidgets.QPushButton):
    """A button with the Houdini look and feel that opens a drop-down menu when clicked.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/MenuButton.html
    """
    def __init__(self) -> None:
        """Create and return a new MenuButton object."""
        pass

class NodeChooserButton(QtWidgets.QPushButton):
    """A button with the Houdini look and feel that opens the Houdini node chooser dialog when clicked.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/NodeChooserButton.html
    """
    def __init__(self) -> None:
        """Create and return a new NodeChooserButton object."""
        pass

class ParmChooserButton(QtWidgets.QPushButton):
    """A button with the Houdini look and feel that opens the Houdini parameter chooser dialog when clicked.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ParmChooserButton.html
    """
    def __init__(self) -> None:
        """Create and return a new ParmChooserButton object."""
        pass

class ParmDialog(QtWidgets.QWidget):
    """A Houdini parameters dialog.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ParmDialog.html
    """
    def __init__(
        self,
        node: Any,
        showTitleBar: bool = True,
        compact: bool = False,
        labelsize: int = -1,
    ) -> None:
        """Create and return a Houdini parameters dialog.

        Args:
            node: The node whose parameters to display
            showTitleBar: Whether to show the title bar
            compact: Whether to use compact layout
            labelsize: Custom label size (-1 for default)
        """
        pass

    def setNode(self, node: Any) -> None:
        """Sets the parameters dialog to use the provided node."""
        pass

    def node(self) -> Any:
        """Returns the node that the parameters dialog is set to."""
        pass

    def scrollPosition(self) -> Any:
        """Return the Parameter Editor scroll bars position as percentages."""
        pass

    def setScrollPosition(self, pos: Any) -> None:
        """Set Parameter Editor scroll bars position as hou.Vector2 percentages."""
        pass

    def setMultiParmTab(self, parm: Any, tab_index: int) -> None:
        """Switch a Multi Parameter Tab to a given tab using a parameter name."""
        pass

    def multiParmTab(self, parm: Any) -> int:
        """Returns the currently visible tab index using a parameter name."""
        pass

    def visibleParms(self) -> tuple[Any, ...]:
        """Returns the currently visible parameters."""
        pass

class ParmTupleChooserButton(QtWidgets.QPushButton):
    """A button with the Houdini look and feel that opens the Houdini parameter tuple chooser dialog when clicked.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ParmTupleChooserButton.html
    """
    def __init__(self) -> None:
        """Create and return a new ParmTupleChooserButton object."""
        pass

class SearchLineEdit(QtWidgets.QLineEdit):
    """QLineEdit widget customized for use as a search or filter field.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/SearchLineEdit.html
    """
    def __init__(self) -> None:
        """Create and return a new SearchLineEdit object."""
        pass

class Separator(QtWidgets.QFrame):
    """A simple separator widget with the Houdini look and feel.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/Separator.html
    """
    def __init__(self) -> None:
        """Create and return a new Separator object."""
        pass

class ToolTip(QtWidgets.QWidget):
    """A tooltip window with the Houdini look and feel that can be used for hover tooltips.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ToolTip.html
    """
    def __init__(self) -> None:
        """Create and return a new ToolTip object."""
        pass

class TrackChooserButton(QtWidgets.QPushButton):
    """A button with the Houdini look and feel that opens the Houdini track chooser dialog when clicked.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/TrackChooserButton.html
    """
    def __init__(self) -> None:
        """Create and return a new TrackChooserButton object."""
        pass

class ViewerOverlay(WindowOverlay):
    """A base window class to implement a viewer Qt window overlay.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/ViewerOverlay.html
    """
    def __init__(self, scene_viewer: Any) -> None:
        """Creates and returns a new ViewerOverlay object.

        Args:
            scene_viewer: The scene viewer for the overlay
        """
        pass

    def sceneViewer(self) -> Any:
        """Returns the scene viewer of the overlay window."""
        pass

    def onBeginResize(self) -> None:
        """Called when the scene viewer has started to resize."""
        pass

    def onEndResize(self) -> None:
        """Called when the scene viewer resizing has ended."""
        pass

    def onResizing(self) -> None:
        """Called when the scene viewer is resizing interactively."""
        pass

    def onSizeChanged(self) -> None:
        """Called when the scene viewer size has changed."""
        pass

    def onLayoutChanged(self) -> None:
        """Called when the scene viewer viewport layout has changed."""
        pass

    def onColorSchemeChanged(self) -> None:
        """Called when the scene viewer background color has changed."""
        pass

    def onViewerActivated(self) -> None:
        """Called when the scene viewer is selected."""
        pass

    def onViewerDeactivated(self) -> None:
        """Called when the scene viewer is deselected."""
        pass

    def onParentWindowEvent(self, event: Any) -> None:
        """Called when a window event is sent to the parent."""
        pass

    def onContainerWindowEvent(self, event: Any) -> None:
        """Called when a window event is sent to the container window."""
        pass

    def onWindowPlacement(self) -> None:
        """Called when the window position needs to be updated to maintain the window between the viewer boundaries."""
        pass

    def onMoveContainerWindow(self) -> None:
        """Called when the window is moved as a result of the parent window moving."""
        pass

    def moveTo(self, pos: Any) -> None:
        """Moves the window to position pos."""
        pass

    def moveBy(self, delta: Any) -> None:
        """Moves the window by offset delta."""
        pass

class Window(QtWidgets.QWidget):
    """A generic window with the Houdini look and feel.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/Window.html
    """
    def __init__(self) -> None:
        """Create and return a new Window object."""
        pass

class WindowOverlay(QtWidgets.QWidget):
    """A base window class to implement a Qt overlay window.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/WindowOverlay.html
    """
    def __init__(self, parent: Any, win_floating_panel: bool) -> None:
        """Creates and returns a new WindowOverlay object.

        Args:
            parent: The parent widget
            win_floating_panel: Whether this is a floating panel window
        """
        pass

    def windowContainer(self) -> Any:
        """Returns the window container."""
        pass

    def onInitWindow(self, event: Any) -> None:
        """Called when the window is being initialized."""
        pass

    def onParentWindowEvent(self, event: Any) -> None:
        """Called when a window event is sent to the parent."""
        pass

    def onContainerWindowEvent(self, event: Any) -> None:
        """Called when a window event is sent to the container window."""
        pass

class XMLMenuParser(QtCore.QObject):
    """Object for dealing with XML menus.

    Builds QMenus based on XML menu definitions and simplifies keyboard shortcut handling.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/XMLMenuParser.html
    """
    def __init__(
        self,
        context: str | None = None,
        kwargs: dict[str, Any] | None = None,
        xmlfile: str | None = None,
        xmlstring: str | None = None,
    ) -> None:
        """Create and return a new XMLMenuParser object.

        One of xmlstring or xmlfile must be provided.

        Args:
            context: Hotkey context for the menu
            kwargs: Custom kwargs passed to expressions/code in menu.xml
            xmlfile: Path to XML menu file
            xmlstring: XML menu definition as string
        """
        pass

    def parseString(self, xmlstring: str) -> None:
        """Parse an XML menu string and aggregate its contents into this menu."""
        pass

    def setHotkeyContext(self, hotkey_context: str) -> None:
        """Sets or modifies the hotkey context for this XML menu."""
        pass

    def hotkeyContext(self) -> str:
        """Returns the current hotkey context used by this XML menu."""
        pass

    def parseFile(self, xmlfile: str) -> None:
        """Parse an XML menu file and aggregate its contents into this menu."""
        pass

    def parseFiles(self, xmlfilename: str) -> None:
        """Search HOUDINI_PATH for and parse XML menu files that match given filename and aggregate their contents into this menu."""
        pass

    def generateMenu(
        self,
        kwargs: dict[str, Any],
        menu: Any | None = None,
        actionitem_callback: Callable[[str, dict[str, Any]], None] | None = None,
    ) -> Any:
        """Generate a QMenu hierarchy based on the already parsed XML menu definition.

        Returns:
            hou.qt.Menu object
        """
        pass

    def handleKeyPress(
        self,
        keystring: str,
        kwargs: dict[str, Any],
        actionitem_callback: Callable[[str, dict[str, Any]], None] | None = None,
    ) -> bool:
        """Look up and trigger menu actions based on their shortcut key assigned in the hotkey manager.

        Returns:
            True if the key was handled
        """
        pass

class mimeType:
    """Enumeration of Houdini MIME types used to identify data in drag-and-drop operations.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/mimeType.html
    """
    asset: str  # application/sidefx-houdini-asset.catalog.entry
    channelPath: str  # application/sidefx-houdini-channel.path
    chopTrackPath: str  # application/sidefx-houdini-chop.track.path
    galleryEntry: str  # application/sidefx-houdini-gallery.entry
    galleryEntryName: str  # application/sidefx-houdini-gallery.entry.name
    itemPath: str  # application/sidefx-houdini-item.path
    nodeFlagPath: str  # application/sidefx-houdini-node.flag.path
    nodePath: str  # application/sidefx-houdini-node.path
    nodePathAndUsdPrimitivePath: str  # application/sidefx-houdini-node.and.usd.primitive.path
    orboltNodeTypeName: str  # application/sidefx-houdini-orbolt.node.type.name
    paneTabName: str  # application/sidefx-houdini-pane.tab.name
    parmPath: str  # application/sidefx-houdini-parm.path
    persistentHandleName: str  # application/sidefx-houdini-persistent.handle.name
    primitivePath: str  # application/sidefx-houdini-primitive.path
    shelfName: str  # application/sidefx-houdini-shelf.name
    shelfToolName: str  # application/sidefx-houdini-shelf.tool.name
    takeName: str  # application/sidefx-houdini-take.name
    usdPrimitivePath: str  # application/sidefx-houdini-usd.primitive.path
    usdPrimitivePython: str  # application/sidefx-houdini-usd.primitive.python
    usdPropertyPath: str  # application/sidefx-houdini-usd.property.path
    usdPropertyPython: str  # application/sidefx-houdini-usd.property.python

# Functions
def canCreateIcon(icon_name: str) -> bool:
    """Return true if a valid (non-empty) icon can be created from the supplied icon name.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/canCreateIcon.html
    """
    pass

def editList(
    strings: list[str],
    title: str = "",
    allow_empty_strings: bool = False,
    allow_duplicates: bool = False
) -> list[str]:
    """Returns an edited string list.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/editList.html
    """
    pass

def extendedKeyEventInfo(qt_key_event: Any) -> dict[str, Any]:
    """Returns a dictionary containing some extended info that Houdini maintains for Qt key events.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/extendedKeyEventInfo.html
    """
    pass

def floatingPanelWindow(floating_panel_name: str) -> Any:
    """Return a QWidget instance representing the window for the specified floating panel.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/floatingPanelWindow.html
    """
    pass

def fromQColor(qcolor: Any) -> tuple[Color, float]:
    """Convert the given QColor to a HOM color and alpha value.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/fromQColor.html
    """
    pass

def getBrush(resource_name: str) -> Any:
    """Return a QBrush object for a specified Houdini resource color.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/getBrush.html
    """
    pass

def getColor(resource_name: str) -> Any:
    """Return a QColor object for a specified Houdini resource color.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/getColor.html
    """
    pass

def getCursor(cursor_name: str) -> Any:
    """Return a QCursor object for a Houdini cursor.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/getCursor.html
    """
    pass

def hotkeyAssignments(hotkey_symbols: tuple[str, ...]) -> tuple[str, ...]:
    """Return a tuple of strings that represent the hotkeys currently assigned to each action associated with a tuple of hotkey symbols.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/hotkeyAssignments.html
    """
    pass

def inchesToPixels(inches: float) -> float:
    """Converts inches to pixels, accounting for both Qt and Houdini's dpi settings.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/inchesToPixels.html
    """
    pass

def mainWindow() -> Any:
    """Return a QWidget instance representing the main Houdini Window.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/mainWindow.html
    """
    pass

def nativeModifierIndependentKeyCode(qt_key_event: Any) -> int:
    """Interprets the native scan code and virtual key code from a Qt key event to return an integer value that is unaffected by held modifiers.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/nativeModifierIndependentKeyCode.html
    """
    pass

def pixelsToInches(pixels: float) -> float:
    """Converts pixels to inches, accounting for both Qt and Houdini's dpi settings.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/pixelsToInches.html
    """
    pass

def qtKeyEventToString(qt_key_event: Any) -> str:
    """Converts a Qt key event into a string that is suitable for UI display or to pass to the hot key manager.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/qtKeyEventToString.html
    """
    pass

def qtKeyForUI(qt_key_event: Any) -> int:
    """Uses the available extended key event info maintained by Houdini to return the Qt key value for a Qt key event if modifiers were ignored.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/qtKeyForUI.html
    """
    pass

def qtKeyToString(qt_key: int, qt_modifiers: Any, event_text: str) -> str:
    """Converts a Qt key with Qt modifiers and the key event's text into a string that is suitable for UI display or to pass to the hot key manager.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/qtKeyToString.html
    """
    pass

def qtKeyToUIKey(qt_key: int, qt_modifiers: Any) -> tuple[int, Any]:
    """Converts a Qt key with Qt modifiers into a UI key and UI modifiers if possible.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/qtKeyToUIKey.html
    """
    pass

def registerKeyResolveInfoCallback(widget: Any, callback: Callable) -> None:
    """Registers a Python callback that Houdini will call for the given widget when building the key resolve info against which key events are resolved.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/registerKeyResolveInfoCallback.html
    """
    pass

def resolveKeyEvent(qt_key_event: Any, widget: Any) -> str:
    """Resolves a Qt key event to a hotkey symbol representing a command/action.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/resolveKeyEvent.html
    """
    pass

def selectColorFromPalette(
    initial_color: Any = None,
    include_alpha: bool = False,
    parent_widget: Any = None
) -> Any:
    """Returns a selected QColor value from a color palette.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/selectColorFromPalette.html
    """
    pass

def skipClosingMenusForCurrentButtonPress() -> None:
    """Disable automatic closing of menus for the current mouse button event.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/skipClosingMenusForCurrentButtonPress.html
    """
    pass

def styleSheet() -> str:
    """Return the Houdini style sheet.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/styleSheet.html
    """
    pass

def toQColor(color: Color, alpha: float = 1.0) -> Any:
    """Convert the given HOM color and alpha value to a QColor.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/toQColor.html
    """
    pass

def unregisterKeyResolveInfoCallback(widget: Any, callback: Callable) -> None:
    """Unregisters a previously registered Python callback that Houdini will call for the given widget when building the key resolve info.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/unregisterKeyResolveInfoCallback.html
    """
    pass

# Deprecated Functions (noted in documentation but still included for completeness)
def createCheckBox() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createCheckBox.html
    """
    pass

def createComboBox() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createComboBox.html
    """
    pass

def createDialog() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createDialog.html
    """
    pass

def createFileChooserButton() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createFileChooserButton.html
    """
    pass

def createHelpButton() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createHelpButton.html
    """
    pass

def createIcon() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createIcon.html
    """
    pass

def createMenu() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createMenu.html
    """
    pass

def createMenuBar() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createMenuBar.html
    """
    pass

def createMenuButton() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createMenuButton.html
    """
    pass

def createNodeChooserButton() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createNodeChooserButton.html
    """
    pass

def createSeparator() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createSeparator.html
    """
    pass

def createToolTip() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createToolTip.html
    """
    pass

def createWindow() -> Any:
    """DEPRECATED: This function is deprecated.

    See: https://www.sidefx.com/docs/houdini/hom/hou/qt/createWindow.html
    """
    pass
