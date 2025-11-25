"""Data handling utilities module (hou.data)."""

from typing import Any, Sequence

import hou
from hou import _Floats2

# Recipe functions
def saveParmPresetRecipe(
    name: str,
    label: str,
    location: str,
    parm: hou.ParmTuple,
    parmtype_patterns: str = "",
    parmname_patterns: str = "",
    nodetype_patterns: str = "",
    visible: bool = True,
    submenu: str = "",
    record_data: bool = True,
    prescript: str = "",
    postscript: str = "",
    comment: str = "",
    expand_to_dir: bool = False,
    multiparm_operation: str = "set",
    multiparm_start_index: int = 0,
    multiparm_end_index: int = -1,
    evaluate_parmvalues: bool = False,
    metadata: bool = False,
    verbose: bool = False,
) -> None:
    """Saves parameter and multiparm instance values as a preset recipe."""
    ...

def applyParmPresetRecipe(
    name: str,
    parm: hou.ParmTuple,
    multiparm_operation: str = "",
    multiparm_start_index: int = 0,
    prescript: bool = True,
    postscript: bool = True,
) -> dict[str, Any]:
    """Applies the recipe specified by name to the given hou.ParmTuple instance."""
    ...

def saveNodePresetRecipe(
    name: str,
    label: str,
    location: str,
    node: hou.OpNode,
    nodetype_patterns: str = "",
    visible: bool = True,
    submenu: str = "",
    record_data: bool = True,
    prescript: str = "",
    postscript: str = "",
    expand_to_dir: bool = False,
    comment: str = "",
    nodes_only: bool = False,
    flags: bool = False,
    children: bool = False,
    editables: bool = False,
    inputs: bool = False,
    position: bool = False,
    parms: bool | Sequence[hou.ParmTuple] | Sequence[str] = True,
    default_parmvalues: bool = False,
    evaluate_parmvalues: bool = False,
    parms_as_brief: bool = True,
    parmtemplates: str = "spare_only",
    metadata: bool = False,
    verbose: bool = False,
) -> None:
    """
    Saves parameters, optionally children or the editable context of a node as a
    preset recipe.
    """
    ...

def applyNodePresetRecipe(
    name: str,
    node: hou.OpNode,
    prescript: bool = True,
    postscript: bool = True,
    parms: bool = True,
    parmtemplates: bool = True,
    children: bool = True,
    editables: bool = True,
    skip_notes: bool = True,
) -> dict[str, Any]:
    """Applies the recipe specified by name to the given hou.OpNode instance."""
    ...

def saveDecorationRecipe(
    name: str,
    label: str,
    location: str,
    central_node: hou.OpNode,
    decorator_items: Sequence[hou.NetworkMovableItem],
    nodetype_patterns: str = "",
    visible: bool = True,
    submenu: str = "",
    record_data: bool = True,
    prescript: str = "",
    postscript: str = "",
    expand_to_dir: bool = False,
    comment: str = "",
    frame_nodes: Sequence[hou.NetworkMovableItem] | None = None,
    selected_nodes: Sequence[hou.NetworkMovableItem] | None = None,
    current_node: hou.NetworkMovableItem | None = None,
    nodes_only: bool = False,
    flags: bool = False,
    central_children: bool = False,
    children: bool = True,
    central_editables: bool = False,
    editables: bool = True,
    central_parms: bool | Sequence[hou.ParmTuple] | Sequence[str] = True,
    parms: bool = True,
    default_parmvalues: bool = False,
    evaluate_parmvalues: bool = False,
    parms_as_brief: bool = True,
    parmtemplates: str = "spare_only",
    metadata: bool = False,
    verbose: bool = False,
) -> None:
    """Saves a set of network items as a decoration recipe."""
    ...

def applyDecorationRecipe(
    name: str,
    central_node: hou.OpNode,
    external_connections: bool = False,
    drop_on_wire: bool = False,
    click_to_place: bool = False,
    avoid_overlap: bool = False,
    frame: bool = False,
    parms: bool = True,
    parmtemplates: bool = True,
    children: bool = True,
    editables: bool = True,
    skip_notes: bool = True,
) -> dict[str, Any]:
    """
    Applies the decoration recipe specified by name to the given hou.OpNode
    instance.
    """
    ...

def saveToolRecipe(
    name: str,
    label: str,
    location: str,
    anchor_node: hou.OpNode,
    items: Sequence[hou.NetworkMovableItem] | None = None,
    tool_labels: Sequence[str] | None = None,
    tab_submenu: str = "Recipes",
    shelf_tab: str = 'Recipes',
    shelf_ordering_index: float = -1.0,
    help_url: str = "",
    example: bool = False,
    visible: bool = True,
    icon: str = "BUTTONS_recipe",
    record_data: bool = True,
    prescript: str = "",
    postscript: str = "",
    expand_to_dir: bool = False,
    comment: str = "",
    frame_nodes: Sequence[hou.NetworkMovableItem] | None = None,
    selected_nodes: Sequence[hou.NetworkMovableItem] | None = None,
    current_node: hou.NetworkMovableItem | None = None,
    nodes_only: bool = False,
    flags: bool = False,
    anchor_children: bool = False,
    children: bool = True,
    anchor_editables: bool = False,
    editables: bool = True,
    anchor_parms: bool | Sequence[hou.ParmTuple] | Sequence[str] = True,
    parms: bool = True,
    default_parmvalues: bool = False,
    evaluate_parmvalues: bool = False,
    parms_as_brief: bool = True,
    parmtemplates: str = "spare_only",
    metadata: bool = False,
    verbose: bool = False,
) -> None:
    """
    Saves a set of network items as a tool recipe to be displayed in the Tab Menu
    Submenu and/or on the Shelf Tab.
    """
    ...

def applyToolRecipe(
    name: str,
    network_editor: hou.NetworkEditor | None = None,
    parent: hou.OpNode | None = None,
    tool_inputs: Sequence[tuple[hou.NetworkMovableItem, int]] | None = None,
    tool_outputs: Sequence[tuple[hou.NetworkMovableItem, int]] | None = None,
    prompt: bool = True,
    drop_on_wire: bool = False,
    click_to_place: bool = False,
    avoid_overlap: bool = False,
    frame: bool = False,
    parms: bool = True,
    parmtemplates: bool = True,
    children: bool = True,
    editables: bool = True,
    skip_notes: bool = True,
) -> dict[str, Any]:
    """
    Recreates the contents of a tool recipe, as if the user had chosen the recipe
    from the tab menu in a network editor or from the shelf tab.
    """
    ...

def saveTabToolRecipe(
    name: str,
    label: str,
    location: str,
    anchor_node: hou.OpNode,
    items: Sequence[hou.NetworkMovableItem] | None = None,
    tab_submenu: str = "Recipes",
    help_url: str = "",
    visible: bool = True,
    icon: str = "BUTTONS_recipe",
    record_data: bool = True,
    prescript: str = "",
    postscript: str = "",
    expand_to_dir: bool = False,
    comment: str = "",
    frame_nodes: Sequence[hou.NetworkMovableItem] | None = None,
    selected_nodes: Sequence[hou.NetworkMovableItem] | None = None,
    current_node: hou.NetworkMovableItem | None = None,
    nodes_only: bool = False,
    flags: bool = False,
    anchor_children: bool = False,
    children: bool = True,
    anchor_editables: bool = False,
    editables: bool = True,
    anchor_parms: bool | Sequence[hou.ParmTuple] | Sequence[str] = True,
    parms: bool = True,
    default_parmvalues: bool = False,
    evaluate_parmvalues: bool = False,
    parms_as_brief: bool = True,
    parmtemplates: str = "spare_only",
    metadata: bool = False,
    verbose: bool = False,
) -> None:
    """
    Saves a set of network items as a tool recipe to be displayed in the Tab Menu
    Submenu.
    """
    ...

def applyTabToolRecipe(
    name: str,
    network_editor: hou.NetworkEditor | None = None,
    parent: hou.OpNode | None = None,
    tool_inputs: Sequence[tuple[hou.NetworkMovableItem, int]] | None = None,
    tool_outputs: Sequence[tuple[hou.NetworkMovableItem, int]] | None = None,
    drop_on_wire: bool = False,
    click_to_place: bool = False,
    avoid_overlap: bool = False,
    frame: bool = False,
    parms: bool = True,
    parmtemplates: bool = True,
    children: bool = True,
    editables: bool = True,
    skip_notes: bool = True,
) -> dict[str, Any]:
    """
    Recreates the contents of a tool recipe, as if the user had chosen the recipe
    from the tab menu.
    """
    ...

def dataFromRecipe(name: str) -> dict[str, Any]:
    """
    Given an internal recipe name, returns a python dictionary of the JSON-like data
    structure stored in the recipe.
    """
    ...

# As data functions
def dataFromParms(
    parms: Sequence[hou.ParmTuple],
    values: bool = True,
    evaluate_values: bool = False,
    locked: bool = True,
    brief: bool = True,
    multiparm_instances: bool = True,
    metadata: bool = False,
    verbose: bool = False,
) -> dict[str, Any]:
    """
    Returns a JSON-like data structure representing the given list of hou.ParmTuple
    objects from a node.
    """
    ...

def selectedItemsAsData(
    nodes_only: bool = False,
    children: bool = True,
    editables: bool = True,
    inputs: bool = True,
    position: bool = True,
    anchor_position: _Floats2 = (0, 0),
    flags: bool = True,
    parms: bool = True,
    parms_as_brief: bool = True,
    default_parmvalues: bool = False,
    evaluate_parmvalues: bool = False,
    parmtemplates: str = "spare_only",
    metadata: bool = False,
    verbose: bool = False,
) -> dict[str, Any]:
    """
    Returns a JSON-like data structure representing the currently selected network
    items.
    """
    ...

def itemsAsData(
    items: Sequence[hou.NetworkMovableItem],
    nodes_only: bool = False,
    children: bool = True,
    editables: bool = True,
    inputs: bool = True,
    position: bool = True,
    anchor_position: _Floats2 = (0, 0),
    flags: bool = True,
    parms: bool = True,
    parms_as_brief: bool = True,
    default_parmvalues: bool = False,
    evaluate_parmvalues: bool = False,
    parmtemplates: str = "spare_only",
    metadata: bool = False,
    verbose: bool = False,
) -> dict[str, Any]:
    """Returns a JSON-like data structure representing the given network items."""
    ...

def createItemsFromData(
    parent: hou.OpNode,
    data: dict[str, Any],
    clear_content: bool = False,
    force_item_creation: bool = True,
    offset_position: _Floats2 = (0, 0),
    external_connections: bool = True,
    parms: bool = True,
    parmtemplates: bool = True,
    children: bool = True,
    editables: bool = True,
    skip_notes: bool = False,
) -> dict[str, hou.NetworkMovableItem]:
    """
    Given a network node and JSON-like data structure as returned by
    hou.data.selectedItemsAsData() or hou.data.itemsAsData() recreate the data items inside the
    network.
    """
    ...

def clusterItemsAsData(
    items: Sequence[hou.NetworkMovableItem],
    target_node: hou.OpNode,
    frame_nodes: Sequence[hou.NetworkMovableItem] | None = None,
    selected_nodes: Sequence[hou.NetworkMovableItem] | None = None,
    current_node: hou.NetworkMovableItem | None = None,
    flags: bool = True,
    nodes_only: bool = False,
    target_children: bool = False,
    children: bool = True,
    target_editables: bool = False,
    editables: bool = True,
    target_parms: bool | Sequence[hou.ParmTuple] | Sequence[str] = True,
    parms: bool = True,
    default_parmvalues: bool = False,
    evaluate_parmvalues: bool = False,
    parms_as_brief: bool = True,
    parmtemplates: str = "spare_only",
    metadata: bool = False,
    verbose: bool = False,
) -> dict[str, Any]:
    """Returns a JSON-like data structure representing the given network items."""
    ...

def createClusterItemsFromData(
    parent: hou.OpNode,
    data: dict[str, Any],
    target_node: hou.OpNode | None = None,
    clear_content: bool = False,
    force_item_creation: bool = True,
    external_connections: bool = True,
    parms: bool = True,
    parmtemplates: bool = True,
    children: bool = True,
    editables: bool = True,
    offset_position: _Floats2 = (0, 0),
    skip_notes: bool = False,
) -> dict[str, hou.NetworkMovableItem]:
    """
    Given a network node and JSON-like data structure as returned by
    hou.data.clusterItemsAsData(), recreate the data items inside the network.
    """
    ...
