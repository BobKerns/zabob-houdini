"""
Houdini hou module stubs for development.
This provides comprehensive type hints for the hou module when developing outside Houdini.
Hand-maintained for zabob-houdini project.

These stubs are designed to handle common type issues with Houdini's C++ bindings:
- Clear static vs instance method distinctions
- Comprehensive return type annotations
- Proper null handling and optional types
- Parameter type unions for flexible input acceptance
- Dynamic attribute access patterns

ENUMERATION IMPLEMENTATION NOTE:
Houdini's documentation inconsistently refers to enumerations as both "modules" (in
headings) and "enumerations" (in text). In reality, they are classes (subclassed from
object) with static hou.EnumValue instances as attributes.

This stub implements them as _Enum subclasses with typed _EnumValue class attributes
for better type safety. This allows type checkers to:
- Validate enum member access (e.g., hou.nodeFlag.Display)
- Catch typos in enum member names
- Provide autocomplete for enum members
- Distinguish between different enum types

If this approach causes type-checking issues, consider falling back to simpler class
definitions without generic typing, or using typing.Literal for specific enum values.
"""

from typing import Any, Generic, Sequence,  TypeAlias, overload, Type, TypeVar, Callable
from collections.abc import Iterator
import types
import datetime


from hrecipes.api.networkitems import SubnetIndirectInput
from searchbox.radialmenus import RadialMenus

# Type variables for generic operations
T = TypeVar('T')
NodeT = TypeVar('NodeT', bound='Node')

# Common type unions that Houdini uses (modern types)
ParameterValue = int | float | str | bool
ParameterDict = dict[str, ParameterValue]
NodePath = str | 'Node'
TransformValue = float | Sequence[float]

_Floats2: TypeAlias = 'tuple[float, float]|Sequence[float]|Vector2'
"""
A sequence of floats representing a 2D point (x, y).

Useful for functions that accept 2D coordinates in any of these forms.
"""

_Floats3: TypeAlias = 'tuple[float, float, float]|Sequence[float]|Vector3'
"""
A sequence of floats representing a 3D point (x, y, z).

Useful for functions that accept 3D coordinates in any of these forms.
"""

_FFloats4: TypeAlias = 'tuple[float, float, float, float]|Sequence[float]|Vector4'
"""
A sequence of floats representing a 4D point (x, y, z, w).

Useful for functions that accept 4D coordinates in any of these forms.
"""

class EnumValue:
    """A simple class to represent enum values in Houdini."""
    def name(self) -> str: ...


class _Enum:
    pass

E = TypeVar('E', bound=_Enum)
class _EnumValue(EnumValue, Generic[E]):
    pass



class saveMode(_Enum):
    """Enumeration of hip file save modes."""
    Text: '_EnumValue[saveMode]'
    Binary: '_EnumValue[saveMode]'

class networkItemType(_Enum):
    """Enum for Houdini network item types."""
    Connection: '_EnumValue[networkItemType]'
    NetworkBox: '_EnumValue[networkItemType]'
    NetworkDot: '_EnumValue[networkItemType]'
    Node: '_EnumValue[networkItemType]'
    StickyNote: '_EnumValue[networkItemType]'
    SubnetIndirectInput: '_EnumValue[networkItemType]'

class exprLanguage(_Enum):
    """Enum for Houdini expression languages."""
    Python: '_EnumValue[exprLanguage]'
    Hscript: '_EnumValue[exprLanguage]'

class scriptLanguage(_Enum):
    """Enum for Houdini expression languages."""
    Python: '_EnumValue[scriptLanguage]'
    Hscript: '_EnumValue[scriptLanguage]'

class parmTemplateType(_Enum):
    """Houdini parameter template type enum-like object."""
    Int: '_EnumValue[parmTemplateType]'
    Float: '_EnumValue[parmTemplateType]'
    String: '_EnumValue[parmTemplateType]'
    Toggle: '_EnumValue[parmTemplateType]'
    Button: '_EnumValue[parmTemplateType]'
    Menu: '_EnumValue[parmTemplateType]'
    FolderSet: '_EnumValue[parmTemplateType]'
    Folder: '_EnumValue[parmTemplateType]'
    Separator: '_EnumValue[parmTemplateType]'
    Label: '_EnumValue[parmTemplateType]'
    Ramp: '_EnumValue[parmTemplateType]'
    Data: '_EnumValue[parmTemplateType]'

class attribType(_Enum):
    """Houdini attribute type enum-like object."""
    Float: '_EnumValue[attribType]'
    Int: '_EnumValue[attribType]'
    String: '_EnumValue[attribType]'
    Vector2: '_EnumValue[attribType]'
    Vector3: '_EnumValue[attribType]'
    Vector4: '_EnumValue[attribType]'
    Matrix3: '_EnumValue[attribType]'
    Matrix4: '_EnumValue[attribType]'
    Quaternion: '_EnumValue[attribType]'
    Transform: '_EnumValue[attribType]'

class groupType(_Enum):
    """Houdini group type enum-like object."""
    Point: '_EnumValue[groupType]'
    Prim: '_EnumValue[groupType]'
    Edge: '_EnumValue[groupType]'
    Vertex: '_EnumValue[groupType]'

class geometryType(_Enum):
    """Houdini geometry type enum-like object."""
    Points: '_EnumValue[geometryType]'
    Primitives: '_EnumValue[geometryType]'
    Edges: '_EnumValue[geometryType]'
    Vertices: '_EnumValue[geometryType]'

class attribData(_Enum):
    """Houdini attribute data enum-like object."""
    Float: '_EnumValue[attribData]'
    Int: '_EnumValue[attribData]'
    String: '_EnumValue[attribData]'

class attribScope(_Enum):
    """Houdini attribute scope enum-like object."""
    Public: '_EnumValue[attribScope]'
    Private: '_EnumValue[attribScope]'

class groupScope(_Enum):
    """Houdini group scope enum-like object."""
    Public: '_EnumValue[groupScope]'
    Private: '_EnumValue[groupScope]'

class primType(_Enum):
    """Houdini primitive type enum-like object."""
    Polygon: '_EnumValue[primType]'
    Sphere: '_EnumValue[primType]'
    Circle: '_EnumValue[primType]'
    Tube: '_EnumValue[primType]'
    MetaBall: '_EnumValue[primType]'
    MetaSQuad: '_EnumValue[primType]'
    NURBSCurve: '_EnumValue[primType]'
    NURBSSurface: '_EnumValue[primType]'
    BezierCurve: '_EnumValue[primType]'
    BezierSurface: '_EnumValue[primType]'
    Mesh: '_EnumValue[primType]'
    Volume: '_EnumValue[primType]'
    VDB: '_EnumValue[primType]'
    PackedDisk: '_EnumValue[primType]'
    PackedGeometry: '_EnumValue[primType]'
    PackedFragment: '_EnumValue[primType]'

class componentLoopType(_Enum):
    """Houdini component loop type enum-like object."""
    Extended: '_EnumValue[componentLoopType]'
    Minimal: '_EnumValue[componentLoopType]'

class numericData(_Enum):
    """Houdini numeric data type enum-like object."""
    Int8: '_EnumValue[numericData]'
    Int16: '_EnumValue[numericData]'
    Int32: '_EnumValue[numericData]'
    Int64: '_EnumValue[numericData]'
    Float16: '_EnumValue[numericData]'
    Float32: '_EnumValue[numericData]'
    Float64: '_EnumValue[numericData]'

class volumeStorageType(_Enum):
    """Houdini volume storage type enum-like object."""
    Float16: '_EnumValue[volumeStorageType]'
    Float32: '_EnumValue[volumeStorageType]'
    Int8: '_EnumValue[volumeStorageType]'
    Int16: '_EnumValue[volumeStorageType]'

class volumeVisualization(_Enum):
    """Houdini volume visualization mode enum-like object."""
    Smoke: '_EnumValue[volumeVisualization]'
    Rainbow: '_EnumValue[volumeVisualization]'
    Blackbody: '_EnumValue[volumeVisualization]'
    Inferno: '_EnumValue[volumeVisualization]'
    Invisible: '_EnumValue[volumeVisualization]'

class colorType(_Enum):
    """Houdini color space type enum for ramp interpolation."""
    RGB: '_EnumValue[colorType]'
    HSV: '_EnumValue[colorType]'
    HSL: '_EnumValue[colorType]'
    LAB: '_EnumValue[colorType]'
    TMI: '_EnumValue[colorType]'
    XYZ: '_EnumValue[colorType]'

class rampParmType(_Enum):
    """Enumeration of ramp parameter types.

    These values control whether a ramp parameter is for color or float values.
    """
    Color: '_EnumValue[rampParmType]'
    Float: '_EnumValue[rampParmType]'

class scaleInheritanceMode(_Enum):
    """Enumeration of scale inheritance modes for transforms.

    Controls how child objects inherit scale transformations from parent objects.
    """
    Default: '_EnumValue[scaleInheritanceMode]'  # Simple inheritance: world = local * parent_world
    OffsetOnly: '_EnumValue[scaleInheritanceMode]'  # Child doesn't scale with parent local scales, but local translation is scaled
    OffsetAndScale: '_EnumValue[scaleInheritanceMode]'  # Local translation is scaled and parent local scaling is reapplied by child in local space
    ScaleOnly: '_EnumValue[scaleInheritanceMode]'  # Local translation is not scaled, but parent local scaling is reapplied by child in local space
    Ignore: '_EnumValue[scaleInheritanceMode]'  # Child completely ignores any parent local scaling

class parmData(_Enum):
    """Enumeration of parameter data types."""
    Int: '_EnumValue[parmData]'
    Float: '_EnumValue[parmData]'
    String: '_EnumValue[parmData]'
    Ramp: '_EnumValue[parmData]'

class parmNamingScheme(_Enum):
    """Enumeration of available naming schemes for a parameter."""
    Base1: '_EnumValue[parmNamingScheme]'
    XYZW: '_EnumValue[parmNamingScheme]'
    XYWH: '_EnumValue[parmNamingScheme]'
    UVW: '_EnumValue[parmNamingScheme]'
    RGBA: '_EnumValue[parmNamingScheme]'
    MinMax: '_EnumValue[parmNamingScheme]'
    MaxMin: '_EnumValue[parmNamingScheme]'
    StartEnd: '_EnumValue[parmNamingScheme]'
    BeginEnd: '_EnumValue[parmNamingScheme]'

class parmCondType(_Enum):
    """Enumeration of available parameter conditional types."""
    DisableWhen: '_EnumValue[parmCondType]'
    HideWhen: '_EnumValue[parmCondType]'
    NoCookWhen: '_EnumValue[parmCondType]'

class dataParmType(_Enum):
    """Enumeration of data parameter types."""
    Geometry: '_EnumValue[dataParmType]'
    KeyValueDictionary: '_EnumValue[dataParmType]'

class folderType(_Enum):
    """Enumeration of folder types for FolderParmTemplates."""
    Collapsible: '_EnumValue[folderType]'
    Simple: '_EnumValue[folderType]'
    Tabs: '_EnumValue[folderType]'
    RadioButtons: '_EnumValue[folderType]'
    MultiparmBlock: '_EnumValue[folderType]'
    ScrollingMultiparmBlock: '_EnumValue[folderType]'
    TabbedMultiparmBlock: '_EnumValue[folderType]'
    ImportBlock: '_EnumValue[folderType]'

class menuType(_Enum):
    """Enumeration of parameter menu types."""
    Normal: '_EnumValue[menuType]'
    Mini: '_EnumValue[menuType]'
    ControlNextParameter: '_EnumValue[menuType]'
    StringReplace: '_EnumValue[menuType]'
    StringToggle: '_EnumValue[menuType]'

class labelParmType(_Enum):
    """Enumeration of label parameter types."""
    Heading: '_EnumValue[labelParmType]'
    Label: '_EnumValue[labelParmType]'
    Message: '_EnumValue[labelParmType]'

class parmExtrapolate(_Enum):
    """Enumeration of Extrapolation methods when evaluating value outside the keyframe range."""
    Default: '_EnumValue[parmExtrapolate]'
    Hold: '_EnumValue[parmExtrapolate]'
    Cycle: '_EnumValue[parmExtrapolate]'
    Extend: '_EnumValue[parmExtrapolate]'
    Slope: '_EnumValue[parmExtrapolate]'
    CycleOffset: '_EnumValue[parmExtrapolate]'
    Oscillate: '_EnumValue[parmExtrapolate]'

class parmLook(_Enum):
    """Enumeration of available looks for a parameter."""
    Regular: '_EnumValue[parmLook]'
    Logarithmic: '_EnumValue[parmLook]'
    Angle: '_EnumValue[parmLook]'
    Vector: '_EnumValue[parmLook]'
    ColorSquare: '_EnumValue[parmLook]'
    HueCircle: '_EnumValue[parmLook]'
    CRGBAPlaneChooser: '_EnumValue[parmLook]'

class parmTemplateInterfaceType(_Enum):
    """Enumeration of parameter template types as available in the Operator Type Properties window."""
    Angle: '_EnumValue[parmTemplateInterfaceType]'
    Button: '_EnumValue[parmTemplateInterfaceType]'
    ButtonStrip: '_EnumValue[parmTemplateInterfaceType]'
    Color: '_EnumValue[parmTemplateInterfaceType]'
    ColorAndAlpha: '_EnumValue[parmTemplateInterfaceType]'
    Data: '_EnumValue[parmTemplateInterfaceType]'
    DirectionVector: '_EnumValue[parmTemplateInterfaceType]'
    File: '_EnumValue[parmTemplateInterfaceType]'
    FileDirectory: '_EnumValue[parmTemplateInterfaceType]'
    FileGeometry: '_EnumValue[parmTemplateInterfaceType]'
    FileImage: '_EnumValue[parmTemplateInterfaceType]'
    Float: '_EnumValue[parmTemplateInterfaceType]'
    FloatMono: '_EnumValue[parmTemplateInterfaceType]'
    FloatVector2: '_EnumValue[parmTemplateInterfaceType]'
    FloatVector3: '_EnumValue[parmTemplateInterfaceType]'
    FloatVector4: '_EnumValue[parmTemplateInterfaceType]'
    FolderCollapsible: '_EnumValue[parmTemplateInterfaceType]'
    FolderSimple: '_EnumValue[parmTemplateInterfaceType]'
    FolderTabs: '_EnumValue[parmTemplateInterfaceType]'
    FolderRadio: '_EnumValue[parmTemplateInterfaceType]'
    FolderMultiparmList: '_EnumValue[parmTemplateInterfaceType]'
    FolderMultiparmScroll: '_EnumValue[parmTemplateInterfaceType]'
    FolderMultiparmTabs: '_EnumValue[parmTemplateInterfaceType]'
    FolderImportBlock: '_EnumValue[parmTemplateInterfaceType]'
    GeometryData: '_EnumValue[parmTemplateInterfaceType]'
    HueCircle: '_EnumValue[parmTemplateInterfaceType]'
    IconStrip: '_EnumValue[parmTemplateInterfaceType]'
    Integer: '_EnumValue[parmTemplateInterfaceType]'
    IntegerVector2: '_EnumValue[parmTemplateInterfaceType]'
    IntegerVector3: '_EnumValue[parmTemplateInterfaceType]'
    IntegerVector4: '_EnumValue[parmTemplateInterfaceType]'
    KeyValueDictionary: '_EnumValue[parmTemplateInterfaceType]'
    Label: '_EnumValue[parmTemplateInterfaceType]'
    LabelHeading: '_EnumValue[parmTemplateInterfaceType]'
    LabelMessage: '_EnumValue[parmTemplateInterfaceType]'
    LogarithmicFloat: '_EnumValue[parmTemplateInterfaceType]'
    LogarithmicInteger: '_EnumValue[parmTemplateInterfaceType]'
    MinMaxFloat: '_EnumValue[parmTemplateInterfaceType]'
    MinMaxInteger: '_EnumValue[parmTemplateInterfaceType]'
    OperatorList: '_EnumValue[parmTemplateInterfaceType]'
    OperatorPath: '_EnumValue[parmTemplateInterfaceType]'
    OperatorMenu: '_EnumValue[parmTemplateInterfaceType]'
    OrderedMenu: '_EnumValue[parmTemplateInterfaceType]'
    RGBAMask: '_EnumValue[parmTemplateInterfaceType]'
    RampColor: '_EnumValue[parmTemplateInterfaceType]'
    RampFloat: '_EnumValue[parmTemplateInterfaceType]'
    Separator: '_EnumValue[parmTemplateInterfaceType]'
    Spacer: '_EnumValue[parmTemplateInterfaceType]'
    String: '_EnumValue[parmTemplateInterfaceType]'
    Toggle: '_EnumValue[parmTemplateInterfaceType]'
    UV: '_EnumValue[parmTemplateInterfaceType]'
    UVW: '_EnumValue[parmTemplateInterfaceType]'

class radialItemType(_Enum):
    """Enumeration of types for radial menu items in Houdini."""
    Script: '_EnumValue[radialItemType]'
    Submenu: '_EnumValue[radialItemType]'

class rampBasis(_Enum):
    """Enumeration of ramp interpolation types."""
    Linear: '_EnumValue[rampBasis]'
    Constant: '_EnumValue[rampBasis]'
    CatmullRom: '_EnumValue[rampBasis]'
    MonotoneCubic: '_EnumValue[rampBasis]'
    Bezier: '_EnumValue[rampBasis]'
    BSpline: '_EnumValue[rampBasis]'
    Hermite: '_EnumValue[rampBasis]'

class renderMethod(_Enum):
    """Enumeration of dependency rendering methods."""
    RopByRop: '_EnumValue[renderMethod]'
    FrameByFrame: '_EnumValue[renderMethod]'

class severityType(_Enum):
    """Enumeration of log message severity levels."""
    Message: '_EnumValue[severityType]'
    Warning: '_EnumValue[severityType]'
    Error: '_EnumValue[severityType]'
    Fatal: '_EnumValue[severityType]'

class paneTabType(_Enum):
    """Enumeration of pane tab types."""
    NetworkEditor: '_EnumValue[paneTabType]'
    SceneViewer: '_EnumValue[paneTabType]'
    ChannelEditor: '_EnumValue[paneTabType]'
    CompositorViewer: '_EnumValue[paneTabType]'
    PythonShell: '_EnumValue[paneTabType]'
    ParameterEditor: '_EnumValue[paneTabType]'
    PythonPanel: '_EnumValue[paneTabType]'
    PerformanceMonitor: '_EnumValue[paneTabType]'

class paneLinkType(_Enum):
    """Enumeration of pane link types for synchronizing pane tabs."""
    Pinned: '_EnumValue[paneLinkType]'
    Linked1: '_EnumValue[paneLinkType]'
    Linked2: '_EnumValue[paneLinkType]'
    Linked3: '_EnumValue[paneLinkType]'

class parmFilterMode(_Enum):
    """Enumeration of parameter filter modes."""
    ShowAll: '_EnumValue[parmFilterMode]'
    ShowMatching: '_EnumValue[parmFilterMode]'
    HideMatching: '_EnumValue[parmFilterMode]'

class parmFilterCriteria(_Enum):
    """Enumeration of parameter filter criteria."""
    AllParameters: '_EnumValue[parmFilterCriteria]'
    AnimatedParameters: '_EnumValue[parmFilterCriteria]'
    ChangedParameters: '_EnumValue[parmFilterCriteria]'

class scrollPosition(_Enum):
    """Enumeration of scroll positions for parameter editor."""
    Top: '_EnumValue[scrollPosition]'
    Center: '_EnumValue[scrollPosition]'
    Bottom: '_EnumValue[scrollPosition]'

class stringParmType(_Enum):
    """Enumeration of string parameter types."""
    Regular: '_EnumValue[stringParmType]'
    FileReference: '_EnumValue[stringParmType]'
    NodeReference: '_EnumValue[stringParmType]'
    NodeReferenceList: '_EnumValue[stringParmType]'

class fileType(_Enum):
    """Enumeration of file types."""
    Any: '_EnumValue[fileType]'
    Image: '_EnumValue[fileType]'
    Geometry: '_EnumValue[fileType]'
    Ramp: '_EnumValue[fileType]'
    Capture: '_EnumValue[fileType]'
    Clip: '_EnumValue[fileType]'
    Lut: '_EnumValue[fileType]'
    Cmd: '_EnumValue[fileType]'
    Midi: '_EnumValue[fileType]'
    I3d: '_EnumValue[fileType]'
    Chan: '_EnumValue[fileType]'
    Sim: '_EnumValue[fileType]'
    SimData: '_EnumValue[fileType]'
    Hip: '_EnumValue[fileType]'
    Otl: '_EnumValue[fileType]'
    Dae: '_EnumValue[fileType]'
    Gallery: '_EnumValue[fileType]'
    Directory: '_EnumValue[fileType]'
    Icon: '_EnumValue[fileType]'
    Ds: '_EnumValue[fileType]'
    Alembic: '_EnumValue[fileType]'
    Psd: '_EnumValue[fileType]'
    LightRig: '_EnumValue[fileType]'
    Gltf: '_EnumValue[fileType]'
    Movie: '_EnumValue[fileType]'
    Fbx: '_EnumValue[fileType]'
    Usd: '_EnumValue[fileType]'
    Sqlite: '_EnumValue[fileType]'

class fieldType(_Enum):
    """Enumeration of field types."""
    NoSuchField: '_EnumValue[fieldType]'
    Integer: '_EnumValue[fieldType]'
    Boolean: '_EnumValue[fieldType]'
    Float: '_EnumValue[fieldType]'
    String: '_EnumValue[fieldType]'
    Dict: '_EnumValue[fieldType]'
    Vector2: '_EnumValue[fieldType]'
    Vector3: '_EnumValue[fieldType]'
    Vector4: '_EnumValue[fieldType]'
    Quaternion: '_EnumValue[fieldType]'
    Matrix3: '_EnumValue[fieldType]'
    Matrix4: '_EnumValue[fieldType]'
    UV: '_EnumValue[fieldType]'
    UVW: '_EnumValue[fieldType]'
    IntArray: '_EnumValue[fieldType]'
    FloatArray: '_EnumValue[fieldType]'
    DictArray: '_EnumValue[fieldType]'

class topCookState(_Enum):
    """Enumeration of TOP Node cook states."""
    Uncooked: '_EnumValue[topCookState]'
    Cooking: '_EnumValue[topCookState]'
    Cooked: '_EnumValue[topCookState]'
    Failed: '_EnumValue[topCookState]'
    Warning: '_EnumValue[topCookState]'
    Waiting: '_EnumValue[topCookState]'
    Incomplete: '_EnumValue[topCookState]'

class trackExtend(_Enum):
    """Houdini CHOP track extend mode enum."""
    Hold: '_EnumValue[trackExtend]'
    Slope: '_EnumValue[trackExtend]'
    Cycle: '_EnumValue[trackExtend]'
    CycleOffset: '_EnumValue[trackExtend]'
    Oscillate: '_EnumValue[trackExtend]'
    Default: '_EnumValue[trackExtend]'

class clipMode(_Enum):
    """Houdini CHOP evaluation mode enum."""
    Locked: '_EnumValue[clipMode]'
    Current: '_EnumValue[clipMode]'
    CookFrame: '_EnumValue[clipMode]'
    CookRealTime: '_EnumValue[clipMode]'

class lopTraversalDemands(_Enum):
    """Specifies which primitives should be included/excluded during USD scene graph traversal."""
    # Values for specifying traversal behavior in LOP operations
    # See: https://www.sidefx.com/docs/houdini/hom/hou/lopTraversalDemands.html
    pass

class lopViewportOverridesLayer(_Enum):
    """Specifies choice between various pxr.Sdf.Layer objects in LopViewportOverrides."""
    # Values for selecting which layer to use for viewport overrides
    # See: https://www.sidefx.com/docs/houdini/hom/hou/lopViewportOverridesLayer.html
    pass

# ============================================================================
# ANIMATION ENUMERATIONS
# ============================================================================

class animBarToolSize(_Enum):
    """Enumeration of values for the size options for Animation Toolbar tools.

    See: https://www.sidefx.com/docs/houdini/hom/hou/animBarToolSize.html
    """
    Compact: '_EnumValue[animBarToolSize]'
    Standard: '_EnumValue[animBarToolSize]'
    Wide: '_EnumValue[animBarToolSize]'
    ExtraWide: '_EnumValue[animBarToolSize]'

class bookmarkEvent(_Enum):
    """Enumeration of the bookmark events that can be handled by callback functions.

    See: https://www.sidefx.com/docs/houdini/hom/hou/bookmarkEvent.html
    """
    Created: '_EnumValue[bookmarkEvent]'  # Triggered when a new bookmark has been created
    Modified: '_EnumValue[bookmarkEvent]'  # Triggered when a bookmark has been modified
    Deleted: '_EnumValue[bookmarkEvent]'  # Triggered when a bookmark has been deleted
    Reset: '_EnumValue[bookmarkEvent]'  # Triggered when the list of bookmarks has been reset or cleared
    InteractionStarted: '_EnumValue[bookmarkEvent]'  # Triggered when a new user interaction begins on a bookmark
    InteractionFinished: '_EnumValue[bookmarkEvent]'  # Triggered when releasing the bookmark after interacting with it

class segmentType(_Enum):
    """Enumeration of values for segment types used by channel primitives.

    See: https://www.sidefx.com/docs/houdini/hom/hou/segmentType.html
    """
    Bezier: '_EnumValue[segmentType]'
    Constant: '_EnumValue[segmentType]'
    Linear: '_EnumValue[segmentType]'
    Cubic: '_EnumValue[segmentType]'
    Ease: '_EnumValue[segmentType]'
    EaseIn: '_EnumValue[segmentType]'
    EaseOut: '_EnumValue[segmentType]'
    Quintic: '_EnumValue[segmentType]'

class slopeMode(_Enum):
    """Enumeration of values for default Slope Mode when inserting new keys into a channel.

    See: https://www.sidefx.com/docs/houdini/hom/hou/slopeMode.html
    """
    Manual: '_EnumValue[slopeMode]'
    Automatic: '_EnumValue[slopeMode]'

# ============================================================================
# DIGITAL ASSETS ENUMERATIONS
# ============================================================================

class hdaEventType(_Enum):
    """Enumeration of types of events that can happen for digital asset libraries.

    See: https://www.sidefx.com/docs/houdini/hom/hou/hdaEventType.html
    """
    AssetCreated: '_EnumValue[hdaEventType]'  # A new asset was created
    AssetDeleted: '_EnumValue[hdaEventType]'  # An asset was deleted
    AssetSaved: '_EnumValue[hdaEventType]'  # An asset was saved
    BeforeAssetCreated: '_EnumValue[hdaEventType]'  # A new asset is about to be created
    BeforeAssetSaved: '_EnumValue[hdaEventType]'  # An asset is about to be saved
    LibraryInstalled: '_EnumValue[hdaEventType]'  # A digital asset library has been installed
    LibraryUninstalled: '_EnumValue[hdaEventType]'  # A digital asset library has been uninstalled

class hdaLicenseType(_Enum):
    """Enumeration of digital asset license permission levels.

    See: https://www.sidefx.com/docs/houdini/hom/hou/hdaLicenseType.html
    """
    Execute: '_EnumValue[hdaLicenseType]'  # Execute permission level
    Read: '_EnumValue[hdaLicenseType]'  # Read permission level
    Full: '_EnumValue[hdaLicenseType]'  # Full permission level

# ============================================================================
# CHANNELS ENUMERATIONS
# ============================================================================

class channelListChangedReason(_Enum):
    """Enumeration of the reasons the hou.playbarEvent.ChannelListChanged event can be triggered.

    See: https://www.sidefx.com/docs/houdini/hom/hou/channelListChangedReason.html
    """
    Replaced: '_EnumValue[channelListChangedReason]'  # Triggered when the channel list has been fully replaced
    Filtered: '_EnumValue[channelListChangedReason]'  # Triggered when the channel list has been filtered

# ============================================================================
# COOKING ENUMERATIONS
# ============================================================================

class updateMode(_Enum):
    """Enumeration of interface update modes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/updateMode.html
    """
    AutoUpdate: '_EnumValue[updateMode]'  # Automatically update the interface
    OnMouseUp: '_EnumValue[updateMode]'  # Update the interface when the mouse button is released
    Manual: '_EnumValue[updateMode]'  # Manually update the interface

# ============================================================================
# CROWDS ENUMERATIONS
# ============================================================================

class agentShapeDeformerType(_Enum):
    """Enumeration of agent shape deformer types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/agentShapeDeformerType.html
    """
    LinearSkinning: '_EnumValue[agentShapeDeformerType]'  # Linear skinning deformer
    DualQuatSkinning: '_EnumValue[agentShapeDeformerType]'  # Dual quaternion skinning deformer
    DualQuatBlendSkinning: '_EnumValue[agentShapeDeformerType]'  # Dual quaternion blend skinning deformer
    BlendShape: '_EnumValue[agentShapeDeformerType]'  # Blend shape deformer
    BlendShapeAndLinearSkinning: '_EnumValue[agentShapeDeformerType]'  # Blend shape and linear skinning deformer
    BlendShapeAndDualQuatSkinning: '_EnumValue[agentShapeDeformerType]'  # Blend shape and dual quaternion skinning deformer
    BlendShapeAndDualQuatBlendSkinning: '_EnumValue[agentShapeDeformerType]'  # Blend shape and dual quaternion blend skinning deformer

# ============================================================================
# GENERAL ENUMERATIONS
# ============================================================================

class hipFileEventType(_Enum):
    """Enumeration of the hip file event types that can be handled by callback functions.

    See: https://www.sidefx.com/docs/houdini/hom/hou/hipFileEventType.html
    """
    BeforeClear: '_EnumValue[hipFileEventType]'  # Triggered immediately before the current .hip file is cleared
    AfterClear: '_EnumValue[hipFileEventType]'  # Triggered immediately after the current .hip file is cleared
    BeforeLoad: '_EnumValue[hipFileEventType]'  # Triggered immediately before a .hip file is loaded
    AfterLoad: '_EnumValue[hipFileEventType]'  # Triggered immediately after a .hip file is loaded
    BeforeMerge: '_EnumValue[hipFileEventType]'  # Triggered immediately before a .hip file is merged
    AfterMerge: '_EnumValue[hipFileEventType]'  # Triggered immediately after a .hip file is merged
    BeforeSave: '_EnumValue[hipFileEventType]'  # Triggered immediately before the current .hip file is saved
    AfterSave: '_EnumValue[hipFileEventType]'  # Triggered immediately after the current .hip file is saved

class licenseCategoryType(_Enum):
    """Enumeration of license category values.

    See: https://www.sidefx.com/docs/houdini/hom/hou/licenseCategoryType.html
    """
    Commercial: '_EnumValue[licenseCategoryType]'  # Commercial license
    Indie: '_EnumValue[licenseCategoryType]'  # Indie license
    Education: '_EnumValue[licenseCategoryType]'  # Education license
    ApprenticeHD: '_EnumValue[licenseCategoryType]'  # Apprentice HD license
    Apprentice: '_EnumValue[licenseCategoryType]'  # Apprentice license

# ============================================================================
# GEOMETRY ENUMERATIONS
# ============================================================================

class keyHalf(_Enum):
    """Enumeration of the halves of a key, used when setting keyframe data in a Channel Primitive.

    See: https://www.sidefx.com/docs/houdini/hom/hou/keyHalf.html
    """
    In: '_EnumValue[keyHalf]'  # Used to set only the in (left) side of a key
    Out: '_EnumValue[keyHalf]'  # Used to set only the out (right) side of a key
    InOut: '_EnumValue[keyHalf]'  # Used to set both sides of a key

class vdbData(_Enum):
    """Enumeration of voxel data types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/vdbData.html
    """
    Boolean: '_EnumValue[vdbData]'  # Boolean voxel data type
    Float: '_EnumValue[vdbData]'  # Float voxel data type
    Int: '_EnumValue[vdbData]'  # Integer voxel data type
    Vector3: '_EnumValue[vdbData]'  # Vector3 voxel data type

class vdbType(_Enum):
    """Enumeration of VDB types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/vdbType.html
    """
    Bool: '_EnumValue[vdbType]'  # Boolean VDB type
    Double: '_EnumValue[vdbType]'  # Double precision VDB type
    Float: '_EnumValue[vdbType]'  # Float VDB type
    Int32: '_EnumValue[vdbType]'  # 32-bit integer VDB type
    Int64: '_EnumValue[vdbType]'  # 64-bit integer VDB type
    Invalid: '_EnumValue[vdbType]'  # Invalid VDB type
    PointData: '_EnumValue[vdbType]'  # Point data VDB type
    PointIndex: '_EnumValue[vdbType]'  # Point index VDB type
    Vec3d: '_EnumValue[vdbType]'  # 3D double vector VDB type
    Vec3f: '_EnumValue[vdbType]'  # 3D float vector VDB type
    Vec3i: '_EnumValue[vdbType]'  # 3D integer vector VDB type

# ============================================================================
# IMAGES/LAYER ENUMERATIONS
# ============================================================================

class imageDepth(_Enum):
    """Enumeration of image depths (data formats) for representing the pixels in an image plane.

    See: https://www.sidefx.com/docs/houdini/hom/hou/imageDepth.html
    """
    Int8: '_EnumValue[imageDepth]'  # 8-bit integer format
    Int16: '_EnumValue[imageDepth]'  # 16-bit integer format
    Int32: '_EnumValue[imageDepth]'  # 32-bit integer format
    Float16: '_EnumValue[imageDepth]'  # 16-bit float format
    Float32: '_EnumValue[imageDepth]'  # 32-bit float format

class imageLayerBorder(_Enum):
    """Enumeration of ImageLayer Borders.

    See: https://www.sidefx.com/docs/houdini/hom/hou/imageLayerBorder.html
    """
    Clamp: '_EnumValue[imageLayerBorder]'  # Clamp to nearest valid location
    Constant: '_EnumValue[imageLayerBorder]'  # Use constant value (usually 0) for out of bound reads
    Mirror: '_EnumValue[imageLayerBorder]'  # Mirror across border to find valid internal location
    Wrap: '_EnumValue[imageLayerBorder]'  # Wrap around to far side

class imageLayerProjection(_Enum):
    """Enumeration of ImageLayer Projections.

    See: https://www.sidefx.com/docs/houdini/hom/hou/imageLayerProjection.html
    """
    Orthographic: '_EnumValue[imageLayerProjection]'  # Orthographic projection along local Z direction
    Perspective: '_EnumValue[imageLayerProjection]'  # Perspective transform focusing to camera position

class imageLayerStorageType(_Enum):
    """Enumeration of ImageLayer StorageTypes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/imageLayerStorageType.html
    """
    Float16: '_EnumValue[imageLayerStorageType]'  # 16-bit floats
    Float32: '_EnumValue[imageLayerStorageType]'  # 32-bit floats
    Int16: '_EnumValue[imageLayerStorageType]'  # 16-bit integers
    Int32: '_EnumValue[imageLayerStorageType]'  # 32-bit integers
    Int8: '_EnumValue[imageLayerStorageType]'  # 8-bit integers
    Fixed8: '_EnumValue[imageLayerStorageType]'  # Fractional 0-1 using 8 bits fixed precision
    Fixed16: '_EnumValue[imageLayerStorageType]'  # Fractional 0-1 using 16 bits fixed precision

class imageLayerTypeInfo(_Enum):
    """Enumeration of ImageLayer TypeInfos.

    See: https://www.sidefx.com/docs/houdini/hom/hou/imageLayerTypeInfo.html
    """
    Color: '_EnumValue[imageLayerTypeInfo]'  # Data interpreted as RGB
    Height: '_EnumValue[imageLayerTypeInfo]'  # Data interpreted as height map (usually Mono)
    ID: '_EnumValue[imageLayerTypeInfo]'  # Data interpreted as ID map (usually ID)
    Mask: '_EnumValue[imageLayerTypeInfo]'  # Data interpreted as 0-1 mask (usually Mono)
    Normal: '_EnumValue[imageLayerTypeInfo]'  # Data interpreted as signed normal (RGB, -1 to 1, normalized)
    OffsetNormal: '_EnumValue[imageLayerTypeInfo]'  # Data interpreted as offset normal (RGB, 0 to 1, normalized around 0.5)
    Position: '_EnumValue[imageLayerTypeInfo]'  # Data interpreted as XYZ location (3-tuples: space, 2-tuples: Image space)
    Raw: '_EnumValue[imageLayerTypeInfo]'  # Data not interpreted, no specific type hint
    SDF: '_EnumValue[imageLayerTypeInfo]'  # Data stores signed distance to curve (usually Mono)
    Texture: '_EnumValue[imageLayerTypeInfo]'  # Data interpreted as UV location (2-tuples: Texture space)
    Vector: '_EnumValue[imageLayerTypeInfo]'  # Data interpreted as direction with magnitude (UV or RGB)

# ============================================================================
# NODES ENUMERATIONS
# ============================================================================

class appearanceChangeType(_Enum):
    """Enumeration of types of appearance change events that can happen to nodes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/appearanceChangeType.html
    """
    Any: '_EnumValue[appearanceChangeType]'
    ErrorState: '_EnumValue[appearanceChangeType]'
    Pick: '_EnumValue[appearanceChangeType]'
    Color: '_EnumValue[appearanceChangeType]'
    DeleteScript: '_EnumValue[appearanceChangeType]'
    Comment: '_EnumValue[appearanceChangeType]'
    LockFlag: '_EnumValue[appearanceChangeType]'
    CompressFlag: '_EnumValue[appearanceChangeType]'
    OTLMatchState: '_EnumValue[appearanceChangeType]'
    ActiveInput: '_EnumValue[appearanceChangeType]'
    Connections: '_EnumValue[appearanceChangeType]'
    ExpressionLanguage: '_EnumValue[appearanceChangeType]'
    NetworkBox: '_EnumValue[appearanceChangeType]'
    PostIt: '_EnumValue[appearanceChangeType]'
    Dot: '_EnumValue[appearanceChangeType]'
    Preview: '_EnumValue[appearanceChangeType]'

class colorItemType(_Enum):
    """Enumeration for color item types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/colorItemType.html
    """
    NetworkBox: '_EnumValue[colorItemType]'
    StickyNote: '_EnumValue[colorItemType]'
    StickyNoteText: '_EnumValue[colorItemType]'

class nodeEventType(_Enum):
    """Enumeration of types of events that can happen to nodes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/nodeEventType.html
    """
    BeingDeleted: '_EnumValue[nodeEventType]'  # Runs before node deleted (cannot cancel deletion)
    NameChanged: '_EnumValue[nodeEventType]'  # Runs after node renamed
    FlagChanged: '_EnumValue[nodeEventType]'  # Runs after node flag changed
    AppearanceChanged: '_EnumValue[nodeEventType]'  # Runs after appearance change (includes change_type argument)

class nodeFlag(_Enum):
    """Enumeration of the different node flags.

    See: https://www.sidefx.com/docs/houdini/hom/hou/nodeFlag.html
    """
    Audio: '_EnumValue[nodeFlag]'
    Bypass: '_EnumValue[nodeFlag]'
    ColorDefault: '_EnumValue[nodeFlag]'
    Compress: '_EnumValue[nodeFlag]'
    Current: '_EnumValue[nodeFlag]'
    Debug: '_EnumValue[nodeFlag]'
    Display: '_EnumValue[nodeFlag]'
    DisplayComment: '_EnumValue[nodeFlag]'
    DisplayDescriptiveName: '_EnumValue[nodeFlag]'
    Export: '_EnumValue[nodeFlag]'
    Expose: '_EnumValue[nodeFlag]'
    Footprint: '_EnumValue[nodeFlag]'
    Highlight: '_EnumValue[nodeFlag]'
    InOutDetailLow: '_EnumValue[nodeFlag]'
    InOutDetailMedium: '_EnumValue[nodeFlag]'
    InOutDetailHigh: '_EnumValue[nodeFlag]'
    Material: '_EnumValue[nodeFlag]'
    Lock: '_EnumValue[nodeFlag]'
    SoftLock: '_EnumValue[nodeFlag]'
    Origin: '_EnumValue[nodeFlag]'
    OutputForDisplay: '_EnumValue[nodeFlag]'
    Pick: '_EnumValue[nodeFlag]'
    Render: '_EnumValue[nodeFlag]'
    Selectable: '_EnumValue[nodeFlag]'
    Template: '_EnumValue[nodeFlag]'
    Unload: '_EnumValue[nodeFlag]'
    Visible: '_EnumValue[nodeFlag]'
    XRay: '_EnumValue[nodeFlag]'

class nodeTypeSource(_Enum):
    """Enumeration of node type sources.

    See: https://www.sidefx.com/docs/houdini/hom/hou/nodeTypeSource.html
    """
    Internal: '_EnumValue[nodeTypeSource]'
    CompiledCode: '_EnumValue[nodeTypeSource]'
    VexCode: '_EnumValue[nodeTypeSource]'
    RslCode: '_EnumValue[nodeTypeSource]'
    Subnet: '_EnumValue[nodeTypeSource]'

class optionalBool(_Enum):
    """Enumeration of a generic tri-state value.

    See: https://www.sidefx.com/docs/houdini/hom/hou/optionalBool.html
    """
    Yes: '_EnumValue[optionalBool]'  # Equivalent to boolean True
    No: '_EnumValue[optionalBool]'  # Equivalent to boolean False
    NoOpinion: '_EnumValue[optionalBool]'  # Indicates lack of opinion

class ropRenderEventType(_Enum):
    """Enumeration of types of events that can happen when a ROP node is rendering.

    See: https://www.sidefx.com/docs/houdini/hom/hou/ropRenderEventType.html
    """
    PreRender: '_EnumValue[ropRenderEventType]'  # Runs once before ROP begins rendering
    PreFrame: '_EnumValue[ropRenderEventType]'  # Runs before each frame rendered
    PostFrame: '_EnumValue[ropRenderEventType]'  # Runs after each frame finishes rendering
    PostWrite: '_EnumValue[ropRenderEventType]'  # Runs after output files written to disk
    PostRender: '_EnumValue[ropRenderEventType]'  # Runs once after ROP finishes rendering

class videoDriver(_Enum):
    """Enumeration of drivers that provide video functionality.

    See: https://www.sidefx.com/docs/houdini/hom/hou/videoDriver.html
    """
    # Note: No specific enum values documented - accessed via hou.videoEncoders()
    pass

class nodeTypeFilter(_Enum):
    """Enumeration of available node type filters.

    See: https://www.sidefx.com/docs/houdini/hom/hou/nodeTypeFilter.html
    """
    NoFilter: '_EnumValue[nodeTypeFilter]'  # Any node
    Sop: '_EnumValue[nodeTypeFilter]'  # Any SOP
    Dop: '_EnumValue[nodeTypeFilter]'  # Any DOP
    Chop: '_EnumValue[nodeTypeFilter]'  # Any CHOP
    Chopnet: '_EnumValue[nodeTypeFilter]'  # Any CHOP Network
    Cop2: '_EnumValue[nodeTypeFilter]'  # Any COP2
    Copnet: '_EnumValue[nodeTypeFilter]'  # Any COP2 Network
    Vop: '_EnumValue[nodeTypeFilter]'  # Any VOP
    Vopnet: '_EnumValue[nodeTypeFilter]'  # Any VOP Network
    Rop: '_EnumValue[nodeTypeFilter]'  # Any ROP
    Lop: '_EnumValue[nodeTypeFilter]'  # Any LOP
    Top: '_EnumValue[nodeTypeFilter]'  # Any TOP
    Shop: '_EnumValue[nodeTypeFilter]'  # Any SHOP
    Obj: '_EnumValue[nodeTypeFilter]'  # Any Object
    ObjBone: '_EnumValue[nodeTypeFilter]'  # Object: Bone Only
    ObjCamera: '_EnumValue[nodeTypeFilter]'  # Object: Camera Only
    ObjFog: '_EnumValue[nodeTypeFilter]'  # Object: Fog Only
    ObjGeometry: '_EnumValue[nodeTypeFilter]'  # Object: Geometry Only
    ObjGeometryOrFog: '_EnumValue[nodeTypeFilter]'  # Object: Geometry and Fog Only
    ObjLight: '_EnumValue[nodeTypeFilter]'  # Object: Light Only
    ObjMuscle: '_EnumValue[nodeTypeFilter]'  # Object: Muscle Only
    ObjSubnet: '_EnumValue[nodeTypeFilter]'  # Object: Subnet Only
    ShopAtmosphere: '_EnumValue[nodeTypeFilter]'  # Shop: Atmosphere Only
    ShopCVEX: '_EnumValue[nodeTypeFilter]'  # Shop: CVEX Only
    ShopDisplacement: '_EnumValue[nodeTypeFilter]'  # Shop: Displacement Only
    ShopImage3D: '_EnumValue[nodeTypeFilter]'  # Shop: Image3D Only
    ShopInterior: '_EnumValue[nodeTypeFilter]'  # Shop: Interior Only
    ShopLight: '_EnumValue[nodeTypeFilter]'  # Shop: Light Only
    ShopLightShadow: '_EnumValue[nodeTypeFilter]'  # Shop: Light Shadow Only
    ShopMaterial: '_EnumValue[nodeTypeFilter]'  # Shop: Material Only
    ShopPhoton: '_EnumValue[nodeTypeFilter]'  # Shop: Photon Only
    ShopProperties: '_EnumValue[nodeTypeFilter]'  # Shop: Properties Only
    ShopSurface: '_EnumValue[nodeTypeFilter]'  # Shop: Surface Only
    TopScheduler: '_EnumValue[nodeTypeFilter]'  # Top: Schedulers Only
    TopPartitioner: '_EnumValue[nodeTypeFilter]'  # Top: Partitioners Only
    TopProcessor: '_EnumValue[nodeTypeFilter]'  # Top: Processors Only

# ============================================================================
# PARAMETERS ENUMERATIONS
# ============================================================================

class parmBakeChop(_Enum):
    """Enumeration of Bake Chop modes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/parmBakeChop.html
    """
    Off: '_EnumValue[parmBakeChop]'
    KeepExportFlag: '_EnumValue[parmBakeChop]'
    DisableExportFlag: '_EnumValue[parmBakeChop]'
    CreateDeleteChop: '_EnumValue[parmBakeChop]'

# ============================================================================
# PLAYBAR ENUMERATIONS
# ============================================================================

class playMode(_Enum):
    """Enumeration of play modes for the main playbar in Houdini.

    See: https://www.sidefx.com/docs/houdini/hom/hou/playMode.html
    """
    Loop: '_EnumValue[playMode]'  # Play through the frame range and loop back to the beginning
    Once: '_EnumValue[playMode]'  # Play through the frame range and stop at the end
    Zigzag: '_EnumValue[playMode]'  # Play through and reverse direction at the end
    Forever: '_EnumValue[playMode]'  # Play through and keep playing past the end

class playbarEvent(_Enum):
    """Enumeration of the playbar events that can be handled by callback functions.

    See: https://www.sidefx.com/docs/houdini/hom/hou/playbarEvent.html
    """
    FrameChanged: '_EnumValue[playbarEvent]'
    RangeChanged: '_EnumValue[playbarEvent]'
    ChannelListChanged: '_EnumValue[playbarEvent]'
    KeyChanged: '_EnumValue[playbarEvent]'

# ============================================================================
# RADIAL MENUS ENUMERATIONS
# ============================================================================

class radialItemLocation(_Enum):
    """Enumeration of locations for radial menu items in Houdini.

    See: https://www.sidefx.com/docs/houdini/hom/hou/radialItemLocation.html
    """
    Top: '_EnumValue[radialItemLocation]'
    TopLeft: '_EnumValue[radialItemLocation]'
    Left: '_EnumValue[radialItemLocation]'
    BottomLeft: '_EnumValue[radialItemLocation]'
    Bottom: '_EnumValue[radialItemLocation]'
    BottomRight: '_EnumValue[radialItemLocation]'
    Right: '_EnumValue[radialItemLocation]'
    TopRight: '_EnumValue[radialItemLocation]'

# ============================================================================
# SHADING ENUMERATIONS
# ============================================================================

class shaderType(_Enum):
    """Enumeration of SHOP shader types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/shaderType.html
    """
    Invalid: '_EnumValue[shaderType]'
    Surface: '_EnumValue[shaderType]'
    SurfaceShadow: '_EnumValue[shaderType]'
    Displacement: '_EnumValue[shaderType]'
    Geometry: '_EnumValue[shaderType]'
    Interior: '_EnumValue[shaderType]'
    Light: '_EnumValue[shaderType]'
    LightShadow: '_EnumValue[shaderType]'
    Atmosphere: '_EnumValue[shaderType]'
    Lens: '_EnumValue[shaderType]'
    Output: '_EnumValue[shaderType]'
    Background: '_EnumValue[shaderType]'
    Photon: '_EnumValue[shaderType]'
    Image3D: '_EnumValue[shaderType]'
    BSDF: '_EnumValue[shaderType]'
    CVEX: '_EnumValue[shaderType]'
    Mutable: '_EnumValue[shaderType]'
    Properties: '_EnumValue[shaderType]'
    Material: '_EnumValue[shaderType]'
    VopMaterial: '_EnumValue[shaderType]'
    ShaderClass: '_EnumValue[shaderType]'

# ============================================================================
# UTILITY ENUMERATIONS
# ============================================================================

class compressionType(_Enum):
    """Enumeration of compression types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/compressionType.html
    """
    Gzip: '_EnumValue[compressionType]'  # Compress using Gzip
    Blosc: '_EnumValue[compressionType]'  # Compress using Blosc
    NoCompression: '_EnumValue[compressionType]'  # Do not compress

# ============================================================================
# VEX ENUMERATIONS
# ============================================================================

class vopParmGenType(_Enum):
    """Enumeration of the different node configurations that can be created for the inputs of a VOP node.

    See: https://www.sidefx.com/docs/houdini/hom/hou/vopParmGenType.html
    """
    Constant: '_EnumValue[vopParmGenType]'  # Create a Constant VOP and connect it to the VOP node's input
    Parameter: '_EnumValue[vopParmGenType]'  # Create a Parameter VOP and connect it to the VOP node's input (promoted to network interface)
    SubnetInput: '_EnumValue[vopParmGenType]'  # Create a Parameter VOP with Subnet scope (promoted to owning Subnet VOP's interface)

# ============================================================================
# UI ENUMERATIONS
# ============================================================================

class confirmType(_Enum):
    """Enumeration of confirmation dialog suppression options.

    See: https://www.sidefx.com/docs/houdini/hom/hou/confirmType.html
    """
    NoConfirmType: '_EnumValue[confirmType]'
    OverwriteFile: '_EnumValue[confirmType]'
    UnlockNode: '_EnumValue[confirmType]'
    DeleteSpareParameters: '_EnumValue[confirmType]'
    DeleteWithoutReferences: '_EnumValue[confirmType]'
    NestedChannelGroups: '_EnumValue[confirmType]'
    SiblingChannelGroups: '_EnumValue[confirmType]'
    DeleteShelfElement: '_EnumValue[confirmType]'
    DeleteGalleryEntry: '_EnumValue[confirmType]'
    InactiveSnapMode: '_EnumValue[confirmType]'
    BackgroundSave: '_EnumValue[confirmType]'
    LockMultiNode: '_EnumValue[confirmType]'
    SaveEmbeddedDefinitions: '_EnumValue[confirmType]'
    OCIOChangeReminder: '_EnumValue[confirmType]'
    OCIOPackageExists: '_EnumValue[confirmType]'
    OverwriteRecipe: '_EnumValue[confirmType]'
    TopCookSave: '_EnumValue[confirmType]'
    TopDeleteResults: '_EnumValue[confirmType]'
    TopDeleteTempDir: '_EnumValue[confirmType]'
    TopHotKeyCancelCook: '_EnumValue[confirmType]'
    TopViewResults: '_EnumValue[confirmType]'
    TopTerminateRemoteSession: '_EnumValue[confirmType]'

class drawableDisplayMode(_Enum):
    """Enumerator for the drawable display mode.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawableDisplayMode.html
    """
    CurrentViewportMode: '_EnumValue[drawableDisplayMode]'  # Specifies the display mode currently active in the viewport
    WireframeMode: '_EnumValue[drawableDisplayMode]'  # Specifies the display mode as wireframe

class drawableGeometryPointStyle(_Enum):
    """Enumeration used to specify the style of points to draw.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawableGeometryPointStyle.html
    """
    LinearCircle: '_EnumValue[drawableGeometryPointStyle]'  # Linear circle
    LinearSquare: '_EnumValue[drawableGeometryPointStyle]'  # Linear square
    LinearDiamond: '_EnumValue[drawableGeometryPointStyle]'  # Linear Diamond
    RingsCircle: '_EnumValue[drawableGeometryPointStyle]'  # Circular rings
    RingsSquare: '_EnumValue[drawableGeometryPointStyle]'  # Square rings
    RingsDiamond: '_EnumValue[drawableGeometryPointStyle]'  # Rings Diamond
    SmoothCircle: '_EnumValue[drawableGeometryPointStyle]'  # Smooth circle
    SmoothSquare: '_EnumValue[drawableGeometryPointStyle]'  # Smooth square
    SmoothDiamond: '_EnumValue[drawableGeometryPointStyle]'  # Smooth Diamond
    ArrowUp: '_EnumValue[drawableGeometryPointStyle]'  # Arrow pointing up
    Cross: '_EnumValue[drawableGeometryPointStyle]'  # Cross
    Cube: '_EnumValue[drawableGeometryPointStyle]'  # 3D cube
    Diamond: '_EnumValue[drawableGeometryPointStyle]'  # Diamond shape
    Diamond2: '_EnumValue[drawableGeometryPointStyle]'  # Diamond shape with dash lines
    Diamond3: '_EnumValue[drawableGeometryPointStyle]'  # Diamond-cross shape with dash lines
    Flare: '_EnumValue[drawableGeometryPointStyle]'  # Flare shape
    Frame: '_EnumValue[drawableGeometryPointStyle]'  # Simple frame
    Frame2: '_EnumValue[drawableGeometryPointStyle]'  # Frame with dash lines
    Frame3: '_EnumValue[drawableGeometryPointStyle]'  # Frame with dotted line
    Locate: '_EnumValue[drawableGeometryPointStyle]'  # Locate-arrow shape
    Locate2: '_EnumValue[drawableGeometryPointStyle]'  # Simple locate shape
    Plus: '_EnumValue[drawableGeometryPointStyle]'  # Plus sign
    Ring: '_EnumValue[drawableGeometryPointStyle]'  # Simple ring
    Ring2: '_EnumValue[drawableGeometryPointStyle]'  # Simple ring with dashed line
    Ring3: '_EnumValue[drawableGeometryPointStyle]'  # Two color ring
    Ring4: '_EnumValue[drawableGeometryPointStyle]'  # Ring with triple lines
    Ring5: '_EnumValue[drawableGeometryPointStyle]'  # Dotted ring
    Target1: '_EnumValue[drawableGeometryPointStyle]'  # Target shape 1
    Target2: '_EnumValue[drawableGeometryPointStyle]'  # Target shape 2
    Target3: '_EnumValue[drawableGeometryPointStyle]'  # Target shape 3
    Target4: '_EnumValue[drawableGeometryPointStyle]'  # Target shape 4
    TriangleDown: '_EnumValue[drawableGeometryPointStyle]'  # Triangle pointing down
    TriangleUp: '_EnumValue[drawableGeometryPointStyle]'  # Triangle pointing up

class drawablePrimitive(_Enum):
    """Enumerator for the drawable primitive types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawablePrimitive.html
    """
    Circle: '_EnumValue[drawablePrimitive]'
    Sphere: '_EnumValue[drawablePrimitive]'
    Tube: '_EnumValue[drawablePrimitive]'

class drawableTextOrigin(_Enum):
    """Enumeration used to specify the reference point of the text within its bounding box.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawableTextOrigin.html
    """
    BottomLeft: '_EnumValue[drawableTextOrigin]'  # Set the text reference point at the bottom left position of the bounding box
    BottomCenter: '_EnumValue[drawableTextOrigin]'  # Set the text reference point at the bottom center position of the bounding box
    BottomRight: '_EnumValue[drawableTextOrigin]'  # Set the text reference point at the bottom right position of the bounding box
    LeftCenter: '_EnumValue[drawableTextOrigin]'  # Set the text reference point at the left center position of the bounding box
    RightCenter: '_EnumValue[drawableTextOrigin]'  # Set the text reference point at the right center position of the bounding box
    UpperLeft: '_EnumValue[drawableTextOrigin]'  # Set the text reference point at the upper left position of the bounding box
    UpperCenter: '_EnumValue[drawableTextOrigin]'  # Set the text reference point at the upper center position of the bounding box
    UpperRight: '_EnumValue[drawableTextOrigin]'  # Set the text reference point at the upper right position of the bounding box

class fileChooserMode(_Enum):
    """Enumeration of possible read/write modes for the file chooser.

    See: https://www.sidefx.com/docs/houdini/hom/hou/fileChooserMode.html
    """
    Read: '_EnumValue[fileChooserMode]'
    Write: '_EnumValue[fileChooserMode]'
    ReadAndWrite: '_EnumValue[fileChooserMode]'

class nodeFootprint(_Enum):
    """Enumeration of the specialized node footprints supported by the network editor.

    See: https://www.sidefx.com/docs/houdini/hom/hou/nodeFootprint.html
    """
    InsertionPoint: '_EnumValue[nodeFootprint]'  # Draw a footprint around the LOP node that is currently set as the insertion point

class perfMonObjectView(_Enum):
    """Enumeration of the different structures that are used to view objects in the Performance Monitor panetab.

    See: https://www.sidefx.com/docs/houdini/hom/hou/perfMonObjectView.html
    """
    List: '_EnumValue[perfMonObjectView]'
    Tree: '_EnumValue[perfMonObjectView]'
    EventLog: '_EnumValue[perfMonObjectView]'

class perfMonTimeFormat(_Enum):
    """Enumeration of the different formats used when viewing times in the Performance Monitor panetab.

    See: https://www.sidefx.com/docs/houdini/hom/hou/perfMonTimeFormat.html
    """
    Absolute: '_EnumValue[perfMonTimeFormat]'
    Percent: '_EnumValue[perfMonTimeFormat]'

class perfMonTimeUnit(_Enum):
    """Enumeration of the different units used when viewing times in the Performance Monitor panetab.

    See: https://www.sidefx.com/docs/houdini/hom/hou/perfMonTimeUnit.html
    """
    Seconds: '_EnumValue[perfMonTimeUnit]'  # Display times in seconds
    Milliseconds: '_EnumValue[perfMonTimeUnit]'  # Display times in milliseconds

class resourceEventMessage(_Enum):
    """Enumeration of the resource events that can be handled by callback functions.

    See: https://www.sidefx.com/docs/houdini/hom/hou/resourceEventMessage.html
    """
    OnActivate: '_EnumValue[resourceEventMessage]'  # Event triggered after a viewer handle has been activated
    OnCustomEvent: '_EnumValue[resourceEventMessage]'  # Event triggered when hou.ui.fireResourceCustomEvent is called
    OnDeactivate: '_EnumValue[resourceEventMessage]'  # Event triggered after a viewer handle has been deactivated
    OnEnter: '_EnumValue[resourceEventMessage]'  # Event triggered after a viewer state begins
    OnExit: '_EnumValue[resourceEventMessage]'  # Event triggered after a viewer state ends
    OnGenerate: '_EnumValue[resourceEventMessage]'  # Event triggered after a nodeless viewer state begins
    OnInterrupt: '_EnumValue[resourceEventMessage]'  # Event triggered after a viewer state has been interrupted
    OnLoad: '_EnumValue[resourceEventMessage]'  # Event triggered after a package has been successfully loaded
    OnPreEnter: '_EnumValue[resourceEventMessage]'  # Event triggered before a viewer state begins
    OnPrintMessage: '_EnumValue[resourceEventMessage]'  # Event triggered when hou.ui.printViewerStateMessage is called
    OnReload: '_EnumValue[resourceEventMessage]'  # Event triggered after a viewer state or package has been successfully reloaded
    OnResume: '_EnumValue[resourceEventMessage]'  # Event triggered after a viewer state has resumed after an interruption
    OnRegister: '_EnumValue[resourceEventMessage]'  # Event triggered after a viewer state has been successfully registered
    OnUnload: '_EnumValue[resourceEventMessage]'  # Event triggered after a package has been successfully unloaded
    OnUnregister: '_EnumValue[resourceEventMessage]'  # Event triggered after a viewer state has been successfully un-registered
    OnRuntimeError: '_EnumValue[resourceEventMessage]'  # Event triggered when a runtime error occurs during a viewer state operation
    NoEventType: '_EnumValue[resourceEventMessage]'  # An invalid viewer state event type

class secureSelectionOption(_Enum):
    """Enumeration of the secure selection options used by viewer state selectors.

    See: https://www.sidefx.com/docs/houdini/hom/hou/secureSelectionOption.html
    """
    Ignore: '_EnumValue[secureSelectionOption]'  # Selector ignores the viewer's secure selection setting
    Obey: '_EnumValue[secureSelectionOption]'  # Selector obeys the viewer's secure selection setting
    On: '_EnumValue[secureSelectionOption]'  # Selector sets the viewer's secure selection to On when it starts
    Off: '_EnumValue[secureSelectionOption]'  # Selector sets the viewer's secure selection to Off when it starts

class stateGenerateMode(_Enum):
    """Enumeration of possible node generation modes by states.

    See: https://www.sidefx.com/docs/houdini/hom/hou/stateGenerateMode.html
    """
    Insert: '_EnumValue[stateGenerateMode]'
    Branch: '_EnumValue[stateGenerateMode]'
    Enter: '_EnumValue[stateGenerateMode]'

class stateViewerType(_Enum):
    """Enumeration of state viewer types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/stateViewerType.html
    """
    Scene: '_EnumValue[stateViewerType]'
    Compositor: '_EnumValue[stateViewerType]'

class triggerSelectorAction(_Enum):
    """Enumerator representing the type of action a state selector can perform if triggered.

    See: https://www.sidefx.com/docs/houdini/hom/hou/triggerSelectorAction.html
    """
    Start: '_EnumValue[triggerSelectorAction]'  # Activate a selector
    Stop: '_EnumValue[triggerSelectorAction]'  # Deactivate a selector
    Toggle: '_EnumValue[triggerSelectorAction]'  # Start or stop a selector depending on the current selector state

class uiEventReason(_Enum):
    """Values representing reasons Houdini generated a particular UI event.

    See: https://www.sidefx.com/docs/houdini/hom/hou/uiEventReason.html
    """
    Picked: '_EnumValue[uiEventReason]'  # Quick mouse click without dragging
    Start: '_EnumValue[uiEventReason]'  # Left mouse button pressed (mouse down)
    Active: '_EnumValue[uiEventReason]'  # Mouse dragged with the left mouse button down
    Changed: '_EnumValue[uiEventReason]'  # Left mouse button released (mouse up)
    Located: '_EnumValue[uiEventReason]'  # Mouse pointer hovered over something in the interface
    ItemsChanged: '_EnumValue[uiEventReason]'  # Event generated as a change of values in hou.UIEvent
    New: '_EnumValue[uiEventReason]'  # Event generated when a UI element was assigned a different value
    RangeChanged: '_EnumValue[uiEventReason]'  # Event generated when a slider or scrollbar has changed
    NoReason: '_EnumValue[uiEventReason]'  # Event was likely explicitly generated

class uiEventValueType(_Enum):
    """Enumerator for UI event value types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/uiEventValueType.html
    """
    Float: '_EnumValue[uiEventValueType]'  # float value type
    FloatArray: '_EnumValue[uiEventValueType]'  # Array of float values
    IntArray: '_EnumValue[uiEventValueType]'  # Array of int values
    Integer: '_EnumValue[uiEventValueType]'  # int value type
    NoType: '_EnumValue[uiEventValueType]'  # invalid value type
    String: '_EnumValue[uiEventValueType]'  # string value type
    StringArray: '_EnumValue[uiEventValueType]'  # Array of string values

class valueLadderDataType(_Enum):
    """Enumeration of the different data types that may be manipulated by a value ladder.

    See: https://www.sidefx.com/docs/houdini/hom/hou/valueLadderDataType.html
    """
    Float: '_EnumValue[valueLadderDataType]'  # The ladder is being used to manipulate a single floating point value
    Int: '_EnumValue[valueLadderDataType]'  # The ladder is being used to manipulate a single integer value
    FloatArray: '_EnumValue[valueLadderDataType]'  # Array of floating point values
    IntArray: '_EnumValue[valueLadderDataType]'  # Array of integer values

class valueLadderType(_Enum):
    """Enumeration of the different value ladder types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/valueLadderType.html
    """
    Generic: '_EnumValue[valueLadderType]'  # Generic numeric value. Step sizes range from 0.0001 to 100.0
    Angle: '_EnumValue[valueLadderType]'  # Value representing an angle. Step sizes range from 1.0 to 45.0

# ============================================================================
# VIEWS/VIEWPORT ENUMERATIONS
# ============================================================================

class boundaryDisplay(_Enum):
    """Enum for viewport boundary overlay.

    See: https://www.sidefx.com/docs/houdini/hom/hou/boundaryDisplay.html
    """
    pass

class connectivityType(_Enum):
    """Enumeration of connectivity types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/connectivityType.html
    """
    pass

class displaySetType(_Enum):
    """Enum of viewport geometry contexts.

    See: https://www.sidefx.com/docs/houdini/hom/hou/displaySetType.html
    """
    pass

class drawable2DCapStyle(_Enum):
    """Enumerator for 2D drawable cap styles.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawable2DCapStyle.html
    """
    pass

class drawable2DLineStyle(_Enum):
    """Enumerator for 2D drawable line styles.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawable2DLineStyle.html
    """
    pass

class drawable2DMarkerSize(_Enum):
    """Enumerator for 2D drawable marker size.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawable2DMarkerSize.html
    """
    pass

class drawable2DMarkerStyle(_Enum):
    """Enumerator for 2D drawable marker style.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawable2DMarkerStyle.html
    """
    pass

class drawable2DType(_Enum):
    """Enumerator for 2D drawable types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawable2DType.html
    """
    pass

class drawableGeometryFaceStyle(_Enum):
    """Enumeration used to specify the style of faces to draw.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawableGeometryFaceStyle.html
    """
    pass

class drawableGeometryLineStyle(_Enum):
    """Enumeration used to specify the style of lines to draw.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawableGeometryLineStyle.html
    """
    pass

class drawableGeometryType(_Enum):
    """Enumeration of Geometry Drawable types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawableGeometryType.html
    """
    pass

class drawableHighlightMode(_Enum):
    """Enumeration used to specify the highlight mode of a drawable matte.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawableHighlightMode.html
    """
    pass

class drawableRampClamp(_Enum):
    """Enumeration used to specify how to wrap the texture generated when using a ramp color.

    See: https://www.sidefx.com/docs/houdini/hom/hou/drawableRampClamp.html
    """
    pass

class flipbookAntialias(_Enum):
    """Enum values for flipbook antialiasing settings.

    See: https://www.sidefx.com/docs/houdini/hom/hou/flipbookAntialias.html
    """
    pass

class flipbookMotionBlurBias(_Enum):
    """Enum values used to specify the motion blur subframe range.

    See: https://www.sidefx.com/docs/houdini/hom/hou/flipbookMotionBlurBias.html
    """
    pass

class flipbookObjectType(_Enum):
    """Enum values for setting the flipbook's visible object types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/flipbookObjectType.html
    """
    pass

class geometryViewportBackgroundImageFitMode(_Enum):
    """Enumeration of image fit modes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/geometryViewportBackgroundImageFitMode.html
    """
    pass

class geometryViewportEvent(_Enum):
    """Enumeration of the geometry viewport events that can be handled by callback functions.

    See: https://www.sidefx.com/docs/houdini/hom/hou/geometryViewportEvent.html
    """
    pass

class geometryViewportLayout(_Enum):
    """Enumeration of viewport layouts.

    See: https://www.sidefx.com/docs/houdini/hom/hou/geometryViewportLayout.html
    """
    pass

class geometryViewportType(_Enum):
    """Enumeration of scene viewer viewport types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/geometryViewportType.html
    """
    pass

class glShadingType(_Enum):
    """Enum for viewport shading modes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/glShadingType.html
    """
    pass

class groupListType(_Enum):
    """Enumeration of group list types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/groupListType.html
    """
    pass

class handleOrientToNormalAxis(_Enum):
    """Enumeration of handle axes that can be aligned to a geometry normal.

    See: https://www.sidefx.com/docs/houdini/hom/hou/handleOrientToNormalAxis.html
    """
    pass

class hudInfoState(_Enum):
    """Enumeration of states for controling the panel.

    See: https://www.sidefx.com/docs/houdini/hom/hou/hudInfoState.html
    """
    pass

class hudPanel(_Enum):
    """Enumeration to identify the HUD panel types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/hudPanel.html
    """
    pass

class markerVisibility(_Enum):
    """Enum of visibility options for marker visualizers.

    See: https://www.sidefx.com/docs/houdini/hom/hou/markerVisibility.html
    """
    pass

class orientUpAxis(_Enum):
    """Enumeration of global orientation mode.

    See: https://www.sidefx.com/docs/houdini/hom/hou/orientUpAxis.html
    """
    pass

class parameterInterfaceTabType(_Enum):
    """Enum values for selecting a specific parameter source tab in the parameter interface dialog.

    See: https://www.sidefx.com/docs/houdini/hom/hou/parameterInterfaceTabType.html
    """
    pass

class pickFacing(_Enum):
    """Enumeration for describing the facing direction of pickable components.

    See: https://www.sidefx.com/docs/houdini/hom/hou/pickFacing.html
    """
    Front: '_EnumValue[pickFacing]'
    Back: '_EnumValue[pickFacing]'
    FrontAndBack: '_EnumValue[pickFacing]'

class pickModifier(_Enum):
    """Enumeration of methods for modifying selections with new components.

    See: https://www.sidefx.com/docs/houdini/hom/hou/pickModifier.html
    """
    Add: '_EnumValue[pickModifier]'
    Toggle: '_EnumValue[pickModifier]'
    Remove: '_EnumValue[pickModifier]'
    Replace: '_EnumValue[pickModifier]'
    Intersect: '_EnumValue[pickModifier]'

class pickStyle(_Enum):
    """Enumeration of pick styles.

    See: https://www.sidefx.com/docs/houdini/hom/hou/pickStyle.html
    """
    Box: '_EnumValue[pickStyle]'
    Lasso: '_EnumValue[pickStyle]'
    Brush: '_EnumValue[pickStyle]'
    Laser: '_EnumValue[pickStyle]'

class positionType(_Enum):
    """Enumeration of spaces.

    See: https://www.sidefx.com/docs/houdini/hom/hou/positionType.html
    """
    WorldSpace: '_EnumValue[positionType]'
    ViewportXY: '_EnumValue[positionType]'
    ViewportUV: '_EnumValue[positionType]'

class resourceType(_Enum):
    """Enumeration of resources such as viewer states and viewer handles.

    See: https://www.sidefx.com/docs/houdini/hom/hou/resourceType.html
    """
    ViewerState: '_EnumValue[resourceType]'  # Viewer State resource
    ViewerHandle: '_EnumValue[resourceType]'  # Viewer Handle resource
    Package: '_EnumValue[resourceType]'  # Package resource
    NoType: '_EnumValue[resourceType]'  # Not a valid type

class sceneViewerEvent(_Enum):
    """Enumeration of the UI events a scene viewer can listen to via a callback.

    See: https://www.sidefx.com/docs/houdini/hom/hou/sceneViewerEvent.html
    """
    BeginResize: '_EnumValue[sceneViewerEvent]'  # Sent when the user has started resizing a viewer window
    EndResize: '_EnumValue[sceneViewerEvent]'  # Sent when the user has ended resizing a viewer window
    Resizing: '_EnumValue[sceneViewerEvent]'  # Sent whenever a viewer window is being resized interactively
    SizeChanged: '_EnumValue[sceneViewerEvent]'  # Sent whenever a viewer window size has changed
    LayoutChanged: '_EnumValue[sceneViewerEvent]'  # Sent when the viewport layout has been changed
    ColorSchemeChanged: '_EnumValue[sceneViewerEvent]'  # Sent when the viewer color scheme has changed
    SelectedViewportChanged: '_EnumValue[sceneViewerEvent]'  # Sent when a viewport has been selected
    ViewerActivated: '_EnumValue[sceneViewerEvent]'  # Sent when a viewer panel tab is selected
    ViewerDeactivated: '_EnumValue[sceneViewerEvent]'  # Sent when a viewer panel tab is deselected
    ViewerTerminated: '_EnumValue[sceneViewerEvent]'  # Sent when a viewer is terminated
    StateInterrupted: '_EnumValue[sceneViewerEvent]'  # Sent when a viewer state is interrupted
    StateResumed: '_EnumValue[sceneViewerEvent]'  # Sent when a viewer state is resumed
    StateEntered: '_EnumValue[sceneViewerEvent]'  # Sent when a viewer state has entered
    StateExited: '_EnumValue[sceneViewerEvent]'  # Sent when a viewer state has exited
    PrefChanged: '_EnumValue[sceneViewerEvent]'  # Sent when a preference has been changed

class selectionMode(_Enum):
    """Enumeration of selection modes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/selectionMode.html
    """
    Object: '_EnumValue[selectionMode]'
    Geometry: '_EnumValue[selectionMode]'
    Dynamics: '_EnumValue[selectionMode]'

class snappingMode(_Enum):
    """Enumeration of snapping modes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/snappingMode.html
    """
    Off: '_EnumValue[snappingMode]'
    Grid: '_EnumValue[snappingMode]'
    Prim: '_EnumValue[snappingMode]'
    Point: '_EnumValue[snappingMode]'
    Multi: '_EnumValue[snappingMode]'

class snappingPriority(_Enum):
    """Enumeration of snapping priority.

    See: https://www.sidefx.com/docs/houdini/hom/hou/snappingPriority.html
    """
    pass

class viewportAgentBoneDeform(_Enum):
    """Enum for deforming agent quality.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportAgentBoneDeform.html
    """
    pass

class viewportAgentWireframe(_Enum):
    """Enum for agent wireframe mode display.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportAgentWireframe.html
    """
    pass

class viewportBGImageView(_Enum):
    """Background image view target for the viewport display options.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportBGImageView.html
    """
    pass

class viewportClosureSelection(_Enum):
    """Viewport highlight of primitives with selected components.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportClosureSelection.html
    """
    pass

class viewportColorScheme(_Enum):
    """Viewport Color Schemes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportColorScheme.html
    """
    pass

class viewportDOFBokeh(_Enum):
    """Viewport Depth of Field Bokeh Shape.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportDOFBokeh.html
    """
    pass

class viewportDefaultMaterial(_Enum):
    """The default material shader for the 3D viewer.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportDefaultMaterial.html
    """
    pass

class viewportFogHeightMode(_Enum):
    """Viewport fog layer modes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportFogHeightMode.html
    """
    pass

class viewportFogQuality(_Enum):
    """Viewport volume fog quality.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportFogQuality.html
    """
    pass

class viewportGeometryInfo(_Enum):
    """Geometry information display state.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportGeometryInfo.html
    """
    pass

class viewportGridRuler(_Enum):
    """Enum for grid numbering on viewport grids.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportGridRuler.html
    """
    pass

class viewportGuide(_Enum):
    """Viewport guides.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportGuide.html
    """
    pass

class viewportGuideFont(_Enum):
    """Viewport font sizes for visualizer text.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportGuideFont.html
    """
    pass

class viewportHandleHighlight(_Enum):
    """Handle highlight size.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportHandleHighlight.html
    """
    pass

class viewportHomeClipMode(_Enum):
    """Automatic viewport clip plane adjustment during homing.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportHomeClipMode.html
    """
    pass

class viewportLighting(_Enum):
    """Lighting modes for the viewport.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportLighting.html
    """
    pass

class viewportMaterialUpdate(_Enum):
    """Enum for the update frequency of viewport material assignments.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportMaterialUpdate.html
    """
    pass

class viewportPackedBoxMode(_Enum):
    """Enum for the culled packed geometry display mode.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportPackedBoxMode.html
    """
    pass

class viewportParticleDisplay(_Enum):
    """Viewport display option for particle display visualization.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportParticleDisplay.html
    """
    pass

class viewportShadowQuality(_Enum):
    """The quality of shadows produced in the viewport.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportShadowQuality.html
    """
    pass

class viewportStandInGeometry(_Enum):
    """Replacement geometry for instances culled in the viewport.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportStandInGeometry.html
    """
    pass

class viewportStereoMode(_Enum):
    """Stereoscopic viewport display modes.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportStereoMode.html
    """
    pass

class viewportTextureDepth(_Enum):
    """Enum for the viewport texture bit depth limit.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportTextureDepth.html
    """
    pass

class viewportTransparency(_Enum):
    """Transparency rendering quality for the viewport.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportTransparency.html
    """
    pass

class viewportVisualizerCategory(_Enum):
    """Enumeration of the different categories of viewport visualizers.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportVisualizerCategory.html
    """
    pass

class viewportVisualizerEventType(_Enum):
    """Enumeration of types of events that can happen to viewport visualizers.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportVisualizerEventType.html
    """
    pass

class viewportVisualizerScope(_Enum):
    """Enumeration of the different scopes of viewport visualizers.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportVisualizerScope.html
    """
    pass

class viewportVolumeBSplines(_Enum):
    """Display options for viewport volume sampling quality.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportVolumeBSplines.html
    """
    pass

class viewportVolumeQuality(_Enum):
    """Display options for viewport volume rendering quality.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportVolumeQuality.html
    """
    pass

class viewportWorkLight(_Enum):
    """Work light type for the viewer.

    See: https://www.sidefx.com/docs/houdini/hom/hou/viewportWorkLight.html
    """
    pass

# ============================================================================
# VIEWER ENUMERATIONS
# ============================================================================

class promptMessageType(_Enum):
    """Viewport Prompt Message Type.

    See: https://www.sidefx.com/docs/houdini/hom/hou/promptMessageType.html
    """
    pass

class scenePrimMask(_Enum):
    """Scene Graph Selection Mask.

    See: https://www.sidefx.com/docs/houdini/hom/hou/scenePrimMask.html
    """
    pass

class snapSelectionMode(_Enum):
    """Filter for primitive snapping in the LOPs viewer.

    See: https://www.sidefx.com/docs/houdini/hom/hou/snapSelectionMode.html
    """
    pass

# ============================================================================
# WEBSERVER ENUMERATIONS
# ============================================================================

class webServerVerbosity(_Enum):
    """Enumeration of Web Server verbosity level.

    See: https://www.sidefx.com/docs/houdini/hom/hou/webServerVerbosity.html
    """
    pass

# ============================================================================
# CLASS DEFINITIONS
# ============================================================================

class BoundingRect:
    """Houdini bounding rectangle object."""
    @overload
    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None: ...
    @overload
    def __init__(self, p1: 'Vector2', p2: 'Vector2') -> None: ...
    def __init__(self, *args, **kwargs) -> None: ...
    def setTo(self, bounds_sequence: Sequence[float]) -> None: ...
    def isValid(self) -> bool: ...
    def isAlmostEqual(self, rect: 'BoundingRect', tolerance: float = 0.00001) -> bool: ...
    def min(self) -> 'Vector2': ...
    def max(self) -> 'Vector2': ...
    def size(self) -> 'Vector3': ...
    def center(self) -> 'Vector3': ...
    def contains(self, point: 'Vector2|BoundingRect') -> bool: ...
    def isEmpty(self) -> bool: ...
    @overload
    def intersects(self, other: 'NetworkMovableItem') -> bool: ...
    @overload
    def intersects(self, p1: _Floats2, p2: _Floats2) -> bool: ...
    @overload
    def intersects(self, p1: _Floats2, p2: _Floats2, p3: _Floats2) -> bool: ...
    def intersects(self, *args, **kwargs) -> bool: ...
    def closestPoint(self, point: '_Floats2') -> 'Vector2': ...
    def getOffsetToAvoid(self, bounds: 'BoundingRect', direction: 'Vector2|None' = None) -> 'Vector2': ...
    def translate(self, offset: '_Floats2') -> None: ...
    def scale(self, scale: _Floats2) -> None: ...
    def expand(self, offset: '_Floats2') -> None: ...
    def enlargeToContain(self, point_or_rect: '_Floats2|BoundingRect') -> None: ...
    def intersect(self, rect: 'BoundingRect') -> None: ...

class NetworkItem:
    """Base class for items that can be part of a network layout."""
    def networkItemType(self) -> 'networkItemType': ...

class NetworkMovableItem(NetworkItem):
    """Interface for items that can be moved in a network layout."""
    # Name and path
    def name(self) -> str: ...
    def setName(self, name: str) -> None: ...
    def digitsInName(self) -> int: ...
    def path(self) -> str: ...
    def relativePathTo(self, other: 'NetworkMovableItem') -> str: ...

    # Hierarchy
    def parent(self) -> 'NetworkMovableItem|None': ...
    def parentNetworkBox(self) -> 'NetworkBox|None': ...

    # Selection
    def isSelected(self) -> bool: ...
    def isPicked(self) -> bool: ...
    def setSelected(self, on: bool, clear_all_selected: bool=False, show_asset_if_selected: bool=False) -> None: ...
    def color(self) -> 'Color': ...
    def setColor(self, color: 'Color') -> None: ...
    def sessionId(self) -> int: ...

    # Layout
    def position(self) -> 'Vector2': ...
    def setPosition(self, position: '_Floats2') -> None: ...
    def move(self, vector2: '_Floats2') -> None: ...
    def shiftPosition(self, vector2: '_Floats2') -> None: ...
    def size(self) -> 'Vector2': ...

class StickyNote(NetworkMovableItem):
    """
    Base class for sticky notes in the network editor.

    This is the abstract base class. Use OpStickyNote for OP networks
    and ApexStickyNote for APEX networks.
    """
    # Content
    def text(self) -> str: ...
    def setText(self, text: str) -> None: ...
    def textColor(self) -> 'Color': ...
    def setTextColor(self, color: 'Color') -> None: ...
    def textSize(self) -> float: ...
    def setTextSize(self, size: float) -> None: ...

    # State
    def destroy(self) -> None: ...
    def drawBackground(self) -> bool: ...
    def setDrawBackground(self, on: bool) -> None: ...
    def isMinimized(self) -> bool: ...
    def setMinimized(self, on: bool) -> None: ...

    # Size
    def minimizedSize(self) -> 'Vector2': ...
    def restoredSize(self) -> 'Vector2': ...
    def resize(self, vector2: _Floats2) -> None: ...
    def setBounds(self, bounds: 'BoundingRect') -> None: ...
    def setSize(self, size: '_Floats2') -> None: ...

    # Serialization
    def asData(self, position: bool = False, metadata: bool = False, verbose: bool = False) -> dict[str, Any]: ...
    def setFromData(self, data: dict[str, Any]) -> None: ...

class OpStickyNote(StickyNote):
    """
    Represents a sticky note in an OP network (SOP/DOP/OBJ/etc).

    Inherits all methods from StickyNote, NetworkMovableItem, and NetworkItem.
    """
    def asCode(self, brief: bool = False, recurse: bool = False, save_box_contents: bool = False,
               save_channels_only: bool = False, save_creation_commands: bool = False,
               save_keys_in_frames: bool = False, save_parm_values_only: bool = False,
               save_spare_parms: bool = False, save_box_membership: bool = True,
               function_name: str | None = None) -> str:
        """
        Prints the Python code necessary to recreate this sticky note.

        Args:
            brief: If True, omit default parameter values
            recurse: If True, include code for child nodes
            save_box_contents: If True, save contents of network boxes
            save_channels_only: If True, only save channel data
            save_creation_commands: If True, include node creation commands
            save_keys_in_frames: If True, save keyframes in frames instead of time
            save_parm_values_only: If True, only save parameter values
            save_spare_parms: If True, include spare parameters
            save_box_membership: If True, save network box membership
            function_name: Name of function to wrap code in

        Returns:
            Python code string
        """
        ...

class ApexStickyNote(StickyNote):
    """
    Represents a sticky note in an APEX network.

    Inherits all methods from StickyNote, NetworkMovableItem, and NetworkItem.
    APEX sticky notes have the same interface as OP sticky notes but operate
    in APEX graph contexts.
    """
    pass

class NetworkBox(NetworkMovableItem):
    """
    Base class for network boxes.

    Network boxes are organizational containers in the network editor that can
    group nodes, sticky notes, and other network items.
    """
    # Adding items
    def addItem(self, item: NetworkMovableItem) -> None: ...
    def addNetworkBox(self, netbox: 'NetworkBox') -> None: ...
    def addNode(self, node: 'Node') -> None: ...
    def addStickyNote(self, stickynote: StickyNote) -> None: ...
    def addSubnetIndirectInput(self, indirect: 'SubnetIndirectInput') -> None: ...

    # Appearance
    def alpha(self) -> float: ...
    def setAlpha(self, alpha: float) -> None: ...
    def comment(self) -> str: ...
    def setComment(self, comment: str) -> None: ...

    # State
    def autoFit(self) -> bool: ...
    def setAutoFit(self, auto_fit: bool) -> None: ...
    def isMinimized(self) -> bool: ...
    def setMinimized(self, on: bool) -> None: ...
    def destroy(self, destroy_contents: bool = False) -> None: ...

    # Layout
    def fitAroundContents(self) -> None: ...
    def minimizedSize(self) -> 'Vector2': ...
    def restoredSize(self) -> 'Vector2': ...
    def resize(self, vector2: '_Floats2') -> None: ...
    def setBounds(self, bounds: 'BoundingRect') -> None: ...
    def setSize(self, size: '_Floats2') -> None: ...

    # Contents
    def items(self, recurse: bool = True) -> tuple[NetworkMovableItem, ...]: ...
    def nodes(self, recurse: bool = True) -> tuple['Node', ...]: ...
    def networkBoxes(self, recurse: bool = True) -> tuple['NetworkBox', ...]: ...
    def stickyNotes(self, recurse: bool = True) -> tuple[StickyNote, ...]: ...
    def subnetIndirectInputs(self, recurse: bool = True) -> tuple['SubnetIndirectInput', ...]: ...

    # Removing items
    def removeItem(self, item: NetworkMovableItem) -> None: ...
    def removeNetworkBox(self, netbox: 'NetworkBox') -> None: ...
    def removeNode(self, node: 'Node') -> None: ...
    def removeStickyNote(self, stickynote: StickyNote) -> None: ...
    def removeSubnetIndirectInput(self, indirect: 'SubnetIndirectInput') -> None: ...

    # Serialization
    def asData(self, box_content: bool = True, position: bool = False, metadata: bool = False,
               verbose: bool = False) -> dict[str, Any]: ...
    def setFromData(self, data: dict[str, Any]) -> None: ...

class OpNetworkBox(NetworkBox):
    """
    Represents a network box in an OP network (SOP/DOP/OBJ/etc).

    Inherits all methods from NetworkBox, NetworkMovableItem, and NetworkItem.
    """
    def asCode(self, brief: bool = False, recurse: bool = False, save_box_contents: bool = False,
               save_channels_only: bool = False, save_creation_commands: bool = False,
               save_keys_in_frames: bool = False, save_parm_values_only: bool = False,
               save_spare_parms: bool = False, save_box_membership: bool = True,
               function_name: str | None = None) -> str:
        """
        Prints the Python code necessary to recreate this network box.

        Args:
            brief: If True, omit default parameter values
            recurse: If True, include code for child nodes
            save_box_contents: If True, save contents of network boxes
            save_channels_only: If True, only save channel data
            save_creation_commands: If True, include node creation commands
            save_keys_in_frames: If True, save keyframes in frames instead of time
            save_parm_values_only: If True, only save parameter values
            save_spare_parms: If True, include spare parameters
            save_box_membership: If True, save network box membership
            function_name: Name of function to wrap code in

        Returns:
            Python code string
        """
        ...

class IndirectInput(NetworkMovableItem):
    """A subnet indirect input in the network editor."""
    # Inputs and Outputs
    def outputs(self) -> tuple['Node', ...]: ...
    def connections(self) -> tuple['NodeConnection', ...]: ...
    def input(self) -> 'Node|None': ...
    def inputOutputIndex(self) -> int: ...

    # Metadata
    def setColorDefault(self) -> None: ...
    def setSymbolicColorName(self, name: str) -> None: ...
    def setUseColorFromOutput(self, use_output_color: bool) -> None: ...
    def symbolicColorName(self) -> str: ...
    def useColorFromOutput(self) -> bool: ...


class NetworkDot(IndirectInput):
    """A network dot in the network editor."""
    def setPinned(self) -> bool: ...
    def isPinned(self) -> bool: ...
    @overload
    def setInput(self, node: 'Node|None', output_index: int = 0) -> None: ...
    @overload
    def setInput(self, input_index: int, node: 'Node|None', output_index: int = 0) -> None: ...
    def setInput(*args, **kwargs) -> None: ...
    def insertInput(self, input_index: int, node: 'Node|None', output_index: int = 0) -> None: ...
    def inputConnections(self) -> tuple['NodeConnection', ...]: ...
    def destroy(self) -> None: ...

    # As Data
    def asData(self) -> dict[str, Any]: ...
    def setFromData(self, data: dict[str, Any]) -> None: ...


class Node(NetworkMovableItem):
    """
    Houdini node object.

    Note: This class handles the complex type patterns in Houdini's C++ bindings
    where methods can return None unexpectedly and parameters accept multiple types.
    """
    def __init__(self) -> None: ...

    # Basic node info - these are generally reliable
    def type(self) -> 'NodeType': ...  # Can raise OperationFailed if node is invalid
    def children(self) -> tuple['Node', ...]: ...  # Empty tuple if no children

    def parent(self) -> 'Node': ...

    # Hierarchy methods
    def nodes(self, node_path_tuple: tuple[str, ...]) -> tuple['Node|None', ...]: ...
    def item(self, item_path: str) -> 'NetworkMovableItem|None': ...
    def items(self, item_path_tuple: tuple[str, ...]) -> tuple['NetworkMovableItem|None', ...]: ...
    def isNetwork(self) -> bool: ...
    def isEditable(self) -> bool: ...
    def allItems(self) -> tuple['NetworkMovableItem', ...]: ...
    def allNodes(self) -> Iterator['Node']: ...
    def recursiveGlob(self, pattern: str, filter: 'EnumValue' = ..., include_subnets: bool = True) -> tuple['Node', ...]: ...

    # Node connections - handle Houdini's sparse input patterns
    def inputs(self) -> tuple['Node|None', ...]: ...  # None for unconnected inputs
    def inputsFollowingOutputs(self) -> tuple['Node', ...]: ...
    def input(self, inputidx: int) -> 'Node|None': ...
    def inputFollowingOutputs(self, inputidx: int) -> 'Node|None': ...
    def outputs(self) -> tuple['Node', ...]: ...  # Connected outputs only
    def setInput(self, input_index: int, node: 'Node|None', output_index: int = 0) -> None: ...
    def inputConnections(self) -> tuple['NodeConnection', ...]: ...  # Only connected inputs
    def outputConnections(self) -> tuple['NodeConnection', ...]: ...  # All output connections
    def inputConnectors(self) -> tuple[tuple['NodeConnection', ...], ...]: ...
    def outputConnectors(self) -> tuple[tuple['NodeConnection', ...], ...]: ...

    # Extended input/output methods
    def indirectInputs(self) -> tuple['SubnetIndirectInput', ...]: ...
    def subnetOutputs(self) -> tuple['Node', ...]: ...
    def inputAncestors(self, include_ref_inputs: bool = True, follow_subnets: bool = False, only_used_inputs: bool = False) -> tuple['Node', ...]: ...
    def setNamedInput(self, input_name: str, item_to_become_input: 'Node|None', output_name_or_index: str|int) -> None: ...
    def setFirstInput(self, item_to_become_input: 'Node|None', output_index: int = 0) -> None: ...
    def setNextInput(self, item_to_become_input: 'Node|None', output_index: int = 0, unordered_only: bool = False) -> None: ...
    def insertInput(self, input_index: int, item_to_become_input: 'Node|None', output_index: int = 0) -> None: ...
    def numOrderedInputs(self) -> int: ...
    def createInputNode(self, input_index: int, node_type_name: str, node_name: str|None = None, run_init_scripts: bool = True, load_contents: bool = True, exact_type_name: bool = False) -> 'Node': ...
    def createOutputNode(self, node_type_name: str, node_name: str|None = None, run_init_scripts: bool = True, load_contents: bool = True, exact_type_name: bool = False) -> 'Node': ...
    def inputNames(self) -> tuple[str, ...]: ...
    def inputLabels(self) -> tuple[str, ...]: ...
    def outputNames(self) -> tuple[str, ...]: ...
    def outputLabels(self) -> tuple[str, ...]: ...
    def editableInputStrings(self, input_index: int) -> dict[str, str]: ...
    def editableInputString(self, input_index: int, key: str) -> str: ...
    def setEditableInputString(self, input_index: int, key: str, value: str) -> None: ...

    # Input/output info
    def inputIndex(self, node: 'Node') -> int: ...  # -1 if not connected
    def outputIndex(self, node: 'Node') -> int: ...  # -1 if not connected
    def createNode(self, node_type: str, name: str|None = None) -> 'Node': ...  # Can raise OperationFailed
    def node(self, path: str) -> 'Node|None': ...  # None if path doesn't exist
    def glob(self, pattern: str) -> tuple['Node', ...]: ...  # Empty if no matches
    def destroy(self) -> None: ...  # Can raise OperationFailed if locked/referenced

    # Adding and removing methods
    def copyItems(self, items: tuple['NetworkMovableItem', ...], channel_reference_originals: bool = False, relative_references: bool = True, connect_outputs_to_multi_inputs: bool = True) -> tuple['NetworkMovableItem', ...]: ...
    def deleteItems(self, items: tuple['NetworkMovableItem', ...], disable_safety_checks: bool = False) -> None: ...

    # Assets methods
    def canCreateDigitalAsset(self) -> bool: ...

    def allSubChildren(self,
                      filter_type: str|None = None,
                      recurse_in_locked: bool = False) -> tuple['Node', ...]: ...

    # Selection methods
    def isCurrent(self) -> bool: ...
    def setCurrent(self, on: bool, clear_all_selected: bool = False) -> None: ...
    def selectedChildren(self, include_hidden: bool = False, include_hidden_support_nodes: bool = False) -> tuple['Node', ...]: ...
    def selectedItems(self, include_hidden: bool = False, include_hidden_support_nodes: bool = False) -> tuple['NetworkMovableItem', ...]: ...
    def numItems(self, item_type: 'EnumValue|None' = None, selected_only: bool = False, include_hidden: bool = False) -> int: ...

    # Node context helpers
    def childTypeCategory(self) -> 'NodeTypeCategory': ...

    # Subnet methods
    def isSubNetwork(self) -> bool: ...
    def collapseIntoSubnet(self, child_nodes: tuple['Node', ...], subnet_name: str|None = None, subnet_type: str|None = None) -> 'Node': ...
    def extractAndDelete(self) -> tuple['NetworkMovableItem', ...]: ...

    # Layout
    def moveToGoodPosition(self, relative_to_inputs: bool=True, move_inputs: bool=True, move_outputs: bool=True, move_unconnected: bool=True) -> 'Vector2': ...
    def layoutChildren(self, items: tuple['NetworkMovableItem', ...]=(), horizontal_spacing=-1.0, vertical_spacing=-1.0) -> 'Vector2': ...
    def isHidden(self) -> bool: ...
    def hide(self, hidden: bool) -> None: ...

    # Metadata methods
    def comment(self) -> str: ...
    def setComment(self, comment: str) -> None: ...
    def appendComment(self, comment: str) -> None: ...
    def isDisplayDescriptiveNameFlagSet(self) -> bool: ...
    def setDisplayDescriptiveNameFlag(self, on: bool) -> None: ...
    def creator(self) -> 'Node': ...
    def network(self) -> 'Node': ...

    # Cooking and error handling
    def errors(self) -> tuple[str, ...]: ...
    def warnings(self) -> tuple[str, ...]: ...
    def messages(self) -> tuple[str, ...]: ...

    # NetworkBox Management
    def networkBoxes(self) -> tuple['NetworkBox', ...]: ...
    def iterNetworkBoxes(self) -> Iterator['NetworkBox']: ...
    def findNetworkBox(self, name: str) -> 'NetworkBox|None': ...
    def findNetworkBoxes(self, pattern: str) -> tuple['NetworkBox', ...]: ...
    def createNetworkBox(self, name: str|None=None) -> 'NetworkBox': ...
    def copyNetworkBox(self, network_box_to_copy: 'NetworkBox', new_name: str|None=None, channel_reference_original: bool=False) -> 'NetworkBox': ...

    # StickyNote Management
    def stickyNotes(self) -> tuple['StickyNote', ...]: ...
    def iterStickyNotes(self) -> Iterator['StickyNote']: ...
    def findStickyNote(self, name: str) -> 'StickyNote|None': ...
    def findStickyNotes(self, pattern: str) -> tuple['StickyNote', ...]: ...
    def createStickyNote(self, name: str|None=None) -> 'StickyNote': ...
    def copyStickyNote(self, sticky_note_to_copy: 'StickyNote', new_name: str|None=None) -> 'StickyNote': ...

    # Network Dots
    def networkDots(self) -> tuple['NetworkDot', ...]: ...
    def createNetworkDot(self) -> 'NetworkDot': ...

    # Serialization methods
    def copyItemsToClipboard(self, items: tuple['NetworkMovableItem', ...]) -> None: ...
    def pasteItemsFromClipboard(self, position: 'Vector2|None' = None) -> None: ...

    # Operators
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

    # User data methods
    def setUserData(self, name: str, value: str) -> None: ...
    def userDataDict(self) -> dict[str, str]: ...
    def userData(self, name: str) -> str|None: ...
    def destroyUserData(self, name: str, must_exist: bool = True) -> None: ...
    def clearUserDataDict(self) -> None: ...

    # Flag methods
    def isFlagReadable(self, flag: 'EnumValue') -> bool: ...
    def isFlagWritable(self, flag: 'EnumValue') -> bool: ...
    def isGenericFlagSet(self, flag: 'EnumValue') -> bool: ...
    def setGenericFlag(self, flag: 'EnumValue', value: bool) -> None: ...

class OpNode(Node):
    """A Houdini operator node."""
    # Adding and Removing
    def createOrMoveVisualizer(self, output_index: int) -> 'Node': ...
    def copyTo(self, destination_node: 'Node') -> 'Node': ...
    def reorderChild(self, src: int, dest: int) -> None: ...

    # parameters
    def parm(self, param_path: str) -> 'Parm|None': ...
    def globParms(self, pattern: str, ignore_case: bool=False, search_label: bool=False, single_pattern: bool=False) -> tuple['Parm', ...]: ...
    def evalParm(self, parm_path: str) -> ParameterValue: ...
    def parms(self) -> tuple['Parm', ...]: ...
    def parmsReferencingThis(self) -> tuple['Parm', ...]: ...
    def allParms(self) -> Iterator['Parm']: ...
    def setParms(self, parm_dict: dict[str, Any]) -> None: ...
    def setParmsPending(self, parm_dict: dict[str, Any]) -> None: ...
    def setParmExpressions(self, parm_dict: dict[str, str], language: exprLanguage) -> None: ...
    def parmTuple(self, param_path: str) -> 'ParmTuple|None': ...
    def evalParmTuple(self, parm_path: str) -> tuple[ParameterValue, ...]: ...
    def parmTuples(self) -> tuple['ParmTuple', ...]: ...
    def parmsInFolder(self, folder_names: Sequence[str]) -> tuple['Parm', ...]: ...
    def parmTuplesInFolder(self, folder_names: Sequence[str]) -> tuple['ParmTuple', ...]: ...
    def expressionLanguage(self) -> exprLanguage: ...
    def setExpressionLanguage(self, language: exprLanguage) -> None: ...
    def parmAliases(self, recurse: bool=False) -> dict[str, str]: ...
    def clearParmAliases(self) -> None: ...
    def spareParms(self) -> tuple['Parm', ...]: ...
    def removeSpareParms(self) -> None: ...
    def parmTemplateGroup(self) -> 'ParmTemplateGroup': ...
    def setParmTemplateGroup(self, parm_template_group: 'ParmTemplateGroup', rename_conflicting_parms: bool=False) -> None: ...

    # Deprecated methods for spare parm tuples - these are not recommended for use in new code

    #def addSpareParmTuple(self, parm_template: 'ParmTemplate', in_folder: Sequence[str]=(), create_missing_folders: bool=False) -> 'ParmTuple': ...
    #def removeSpareParmTuple(self, parm_tuple: 'ParmTuple') -> None: ...
    def addControlParmFolder(self, folder_name: str|None=None, parm_name: str|None=None) -> None: ...
    #def addSpareParmFolder(self, folder_name: str, in_folder: Sequence[str]=(), parm_name: str|None=None, create_missing_folders: bool=False) -> None: ...
    def removeSpareParmFolder(self, folder_name: Sequence[str]) -> None: ...
    def replaceSpareParmFolder(self, parm_tuple_name: str, parm_template : ParmTemplate) -> None: ...
    def localVariables(self) -> tuple[str, ...]: ...
    def localAttributes(self) -> tuple[str, ...]: ...
    def saveParmClip(self, file_name: str, start: int|None=None, end: int|None=None, sample_rate: int=0, scoped_only: bool=False) -> None: ...
    def loadParmClip(self, file_name: str, sample_rate: int=0, start: int|None=None) -> None: ...
    def parmClipData(self, start=None, end=None, binary=True, use_blosc_compression=True, sample_rate=0, scoped_only=False) -> bytes: ...
    def setParmClipData(self, data: bytes, binary: bool=True, blosc_compressed: bool=True, sample_rate: int=0, start: int=1) -> None: ...

    # Dependencies
    def references(self, include_children: bool=True) -> tuple['Node', ...]: ...
    def dependents(self, include_children: bool=True) -> tuple['Node', ...]: ...
    def fileReferences(self, recurse: bool=True, project_dir_variable: str="HIP", include_all_refs: bool=True) -> tuple[tuple[Parm, str], ...]: ...

    # Assets
    def createDigitalAsset(self, name: str|None=None, hda_file_name: str|None=None, description: str|None=None, min_num_inputs: int=0, max_num_inputs: int=0, compress_content: bool=False, comment: str|None=None, version: str|None=None, save_as_embedded: bool=False, ignore_external_references: bool=False, change_node_type: bool=True, create_backup: bool=True, install_path: str|None=None) -> 'Node': ...
    def createCompiledDigitalAsset(self, name: str|None=None, hda_file_name: str|None=None, description: str|None=None) -> None: ...
    def changeNodeType(self, new_node_type: str, keep_name: bool=True, keep_parms: bool=True, keep_network_contents: bool=True, force_change_on_node_type_match: bool=False) -> None: ...
    def allowEditingOfContents(self, propagate: bool=False) -> None: ...
    def matchCurrentDefinition(self) -> None: ...
    def syncDelayedDefinition(self) -> None: ...
    def isDelayedDefinition(self) -> bool: ...
    def isLockedHDA(self) -> bool: ...
    def isInsideLockedHDA(self) -> bool: ...
    def isEditableInsideLockedHDA(self) -> bool: ...
    def isMaterialManager(self) -> bool: ...
    def hdaModule(self) -> 'HDAModule': ...
    def hm(self) -> 'HDAModule': ...
    def hdaViewerStateModule(self) -> 'HDAViewerStateModule': ...
    def hdaViewerHandleModule(self) -> 'HDAViewerHandleModule': ...
    def syncNodeVersionIfNeeded(self, from_version: str) -> None: ...

    # Metadata methods
    def outputForViewFlag(self) -> int: ...
    def setOutputForViewFlag(self, output: int) -> None: ...
    def creationTime(self) -> 'datetime.datetime': ...
    def modificationTime(self) -> 'datetime.datetime': ...
    def creatorState(self) -> str: ...
    def setCreatorState(self, state: str) -> None: ...
    def isBuiltExplicitly(self) -> bool: ...
    def setBuiltExplicitly(self, built_explicitly: bool) -> None: ...
    def isTimeDependent(self, for_last_cook: bool = False) -> bool: ...
    def lastCookTime(self) -> float: ...
    def matchesCurrentDefinition(self) -> bool: ...

    # Cooking methods
    def cook(self, force: bool = False, frame_range: tuple = ()) -> None: ...
    def needsToCook(self, time: float = ...) -> bool: ...  # time defaults to hou.time()
    def invalidateOutput(self) -> None: ...
    def cookCount(self) -> int: ...
    def lastCookContextOptions(self, only_used_options: bool = False) -> dict[str, str|float]: ...
    def updateParmStates(self) -> None: ...
    def infoTree(self, verbose: bool = False, debug: bool = False, output_index: int = 0, force_cook: bool = False) -> 'NodeInfoTree': ...
    def infoData(self) -> dict[str, Any]: ...
    def cookPathNodes(self) -> tuple['Node', ...]: ...
    def canGenerateCookCode(self, check_parent: bool = False, check_auto_shader: bool = True) -> bool: ...
    def cookCodeGeneratorNode(self, check_parent: bool = False) -> 'Node': ...
    def cookCodeLanguage(self) -> str: ...
    def supportsMultiCookCodeContexts(self) -> bool: ...
    def saveCompiledCookCodeToFile(self, file_name: str, context_name: str|None = None) -> None: ...
    def saveCookCodeToFile(self, file_name: str, skip_header: bool = False, context_name: str|None = None) -> None: ...

    # Node groups methods
    def addNodeGroup(self, name: str|None = None) -> 'NodeGroup': ...
    def nodeGroup(self, name: str) -> 'NodeGroup|None': ...
    def nodeGroups(self) -> tuple['NodeGroup', ...]: ...

    # Scripts methods
    def runInitScripts(self) -> None: ...
    def deleteScript(self) -> str: ...
    def setDeleteScript(self, script_text: str, language: 'EnumValue' = ...) -> None: ...  # language defaults to hou.scriptLanguage.Python

    # Motion FX methods
    def motionEffectsNetworkPath(self) -> str: ...
    def findOrCreateMotionEffectsNetwork(self, create: bool = True) -> 'Node': ...

    # Stamping methods
    def stampValue(self, parm_name: str, default_value: Any) -> Any: ...

    # Extended serialization methods
    def saveItemsToFile(self, items: tuple['NetworkMovableItem', ...], file_name: str, save_hda_fallbacks: bool = False) -> None: ...
    def saveChildrenToFile(self, nodes: tuple['Node', ...], network_boxes: tuple['NetworkBox', ...], file_name: str) -> None: ...
    def loadItemsFromFile(self, file_name: str, ignore_load_warnings: bool = False) -> None: ...
    def loadChildrenFromFile(self, file_name: str, ignore_load_warnings: bool = False) -> None: ...
    def asCode(self, brief: bool = False, recurse: bool = False, save_channels_only: bool = False, save_creation_commands: bool = True, save_keys_in_frames: bool = False, save_outgoing_wires: bool = False, save_parm_values_only: bool = False, save_spare_parms: bool = True, save_box_membership: bool = True, function_name: str|None = None) -> str: ...

    # Callbacks methods
    def addEventCallback(self, event_types: tuple['EnumValue', ...], callback: Callable) -> None: ...
    def removeEventCallback(self, event_types: tuple['EnumValue', ...], callback: Callable) -> None: ...
    def addParmCallback(self, callback: Callable, parm_names: tuple[str, ...]) -> None: ...
    def removeAllEventCallbacks(self) -> None: ...
    def eventCallbacks(self) -> tuple[tuple[tuple['EnumValue', ...], Callable], ...]: ...

    # Cached user data methods
    def setCachedUserData(self, name: str, value: Any) -> None: ...
    def cachedUserDataDict(self) -> dict[str, Any]: ...
    def cachedUserData(self, name: str) -> Any|None: ...
    def destroyCachedUserData(self, name: str, must_exist: bool = True) -> None: ...
    def clearCachedUserDataDict(self) -> None: ...

    # Data blocks methods
    def dataBlockKeys(self, blocktype: str) -> tuple[str, ...]: ...
    def dataBlockType(self, key: str) -> str: ...
    def dataBlock(self, key: str) -> bytes: ...
    def setDataBlock(self, key: str, block: bytes, block_type: str|None = None) -> None: ...
    def removeDataBlock(self, key: str) -> None: ...

    # Dynamics methods
    def simulation(self) -> 'DopSimulation': ...
    def findNodesThatProcessedObject(self, dop_object: 'DopObject') -> tuple['DopNode', ...]: ...

    # PDG Work Items methods
    def selectNextVisibleWorkItem(self) -> None: ...
    def selectPreviousVisibleWorkItem(self) -> None: ...
    def deselectWorkItem(self) -> None: ...
    def setCurrentTOPPage(self, page_index: int) -> None: ...

    # Badges methods
    def addMessage(self, message: str) -> None: ...
    def addWarning(self, message: str) -> None: ...
    def addError(self, message: str, severity: 'EnumValue' = ...) -> None: ...  # severity defaults to hou.severityType.Error

    # Extended inputs and outputs methods
    def inputsWithIndices(self, ignore_network_dots: bool = False, ignore_subnet_indirect_inputs: bool = False, use_names: bool = False) -> tuple[tuple['OpNode', int|str, int|str], ...]: ...
    def outputsWithIndices(self, ignore_network_dots: bool = False, use_names: bool = False) -> tuple[tuple['OpNode', int|str, int|str], ...]: ...
    def outputLabel(self, output_index: int) -> str: ...

    # As data methods - comprehensive serialization API
    def asData(self, nodes_only: bool = False, children: bool = False, editables: bool = False, inputs: bool = False, position: bool = False, flags: bool = False, parms: bool|tuple['ParmTuple', ...]|tuple[str, ...] = True, default_parmvalues: bool = False, evaluate_parmvalues: bool = False, parms_as_brief: bool = True, parmtemplates: str = "spare_only", metadata: bool = False, verbose: bool = False) -> dict[str, Any]: ...
    def setFromData(self, data: dict[str, Any], clear_content: bool = False, force_item_creation: bool = True, parms: bool = True, parmtemplates: bool = True, children: bool = True, editables: bool = True, skip_notes: bool = False) -> None: ...
    def parmsAsData(self, values: bool = True, parms: bool = True, default_values: bool = False, evaluate_values: bool = False, locked: bool = True, brief: bool = True, multiparm_instances: bool = True, metadata: bool = False, verbose: bool = False) -> dict[str, Any]: ...
    def setParmsFromData(self, data: dict[str, Any]) -> None: ...
    def childrenAsData(self, nodes_only: bool = False, children: bool = True, editables: bool = True, inputs: bool = True, position: bool = True, flags: bool = True, parms: bool = True, default_parmvalues: bool = False, evaluate_parmvalues: bool = False, parms_as_brief: bool = True, parmtemplates: str = "spare_only", metadata: bool = False, verbose: bool = False) -> dict[str, Any]: ...
    def setChildrenFromData(self, data: dict[str, Any], clear_content: bool = True, force_item_creation: bool = True, offset_position: 'Vector2' = ..., external_connections: bool = True, parms: bool = True, parmtemplates: bool = True, children: bool = True, editables: bool = True, skip_notes: bool = False) -> None: ...
    def editablesAsData(self, nodes_only: bool = False, children: bool = True, editables: bool = True, inputs: bool = True, position: bool = True, flags: bool = True, parms: bool = True, default_parmvalues: bool = False, evaluate_parmvalues: bool = False, parms_as_brief: bool = True, parmtemplates: str = "spare_only", metadata: bool = False, verbose: bool = False) -> dict[str, Any]: ...
    def setEditablesFromData(self, data: dict[str, Any], clear_content: bool = True, force_item_creation: bool = True, offset_position: 'Vector2' = ..., external_connections: bool = True, parms: bool = True, parmtemplates: bool = True, children: bool = True, editables: bool = True, skip_notes: bool = False) -> None: ...
    def createDecorationItemsFromData(self, items: tuple['NetworkMovableItem', ...], frame_nodes: tuple['NetworkMovableItem', ...]|None = None, selected_nodes: tuple['NetworkMovableItem', ...]|None = None, current_node: 'NetworkMovableItem|None' = None, flags: bool = True, nodes_only: bool = False, target_children: bool = False, children: bool = True, target_editables: bool = False, editables: bool = True, target_parms: bool|tuple['ParmTuple', ...]|tuple[str, ...] = True, parms: bool = True, default_parmvalues: bool = False, evaluate_parmvalues: bool = False, parms_as_brief: bool = True, parmtemplates: str = "spare_only", metadata: bool = False, verbose: bool = False) -> dict[str, Any]: ...
    def parmTemplatesAsData(self, name: str = "", children: bool = True, parmtemplate_order: bool = False) -> dict[str, Any]: ...
    def parmTemplateChildrenAsData(self, name: str = "", parmtemplate_order: bool = False) -> dict[str, Any]: ...
    def appendParmTemplatesFromData(self, data: dict[str, Any], rename_conflicts: bool = True) -> dict[str, 'ParmTuple']: ...
    def replaceParmTemplatesFromData(self, data: dict[str, Any]) -> dict[str, 'ParmTuple']: ...
    def insertParmTemplatesBeforeFromData(self, data: dict[str, Any], parm_name: str, rename_conflicts: bool = True) -> dict[str, 'ParmTuple']: ...
    def insertParmTemplatesAfterFromData(self, data: dict[str, Any], parm_name: str, rename_conflicts: bool = True) -> dict[str, 'ParmTuple']: ...
    def appendParmTemplatesToFolderFromData(self, data: dict[str, Any], parm_name: str, rename_conflicts: bool = True) -> dict[str, 'ParmTuple']: ...
    def prependParmTemplatesToFolderFromData(self, data: dict[str, Any], parm_name: str, rename_conflicts: bool = True) -> dict[str, 'ParmTuple']: ...
    def inputsAsData(self, ignore_network_dots: bool = False, ignore_subnet_indirect_inputs: bool = False, use_names: bool = False) -> tuple[dict[str, Any], ...]: ...
    def setInputsFromData(self, data: dict[str, Any]) -> None: ...
    def outputsAsData(self, ignore_network_dots: bool = False, ignore_subnet_indirect_inputs: bool = False, use_names: bool = False) -> tuple[dict[str, Any], ...]: ...
    def setOutputsFromData(self, data: dict[str, Any]) -> None: ...


class HDAModule(types.ModuleType):
    """
    User-defined Python module containing functions, classes, and constants
    stored with and accessed from a digital asset.

    This module lets you organize Python code in one location in your asset
    and invoke it from parameters, event handlers, and callbacks.

    Access via hou.NodeType.hdaModule() or hou.OpNode.hdaModule().
    """
    # HDAModule is essentially a Python module wrapper with no specific methods beyond
    # what's available in types.ModuleType. The module's attributes are defined by
    # the user's code in the Python Module section of the digital asset.
    pass

class HDAViewerStateModule(types.ModuleType):
    """
    User-defined Python module containing the implementation and registration code
    of a python viewer state stored in a digital asset.

    Similar to HDAModule but dedicated for python viewer states. Used mainly by
    Houdini for registering python states embedded in digital assets.

    Source code is stored in the ViewerState Module section of the Interactive|State
    Script tab in the Type Properties dialog.

    Access via hou.OpNode.hdaViewerStateModule() or hou.NodeType.hdaViewerStateModule().
    """
    # HDAViewerStateModule is essentially a Python module wrapper with no specific methods
    # beyond what's available in types.ModuleType. The module's attributes are defined by
    # the user's code in the ViewerState Module section of the digital asset.
    pass

class HDAViewerHandleModule(types.ModuleType):
    """
    User-defined Python module containing the implementation and registration code
    of a python viewer handle stored in a digital asset.

    Similar to HDAViewerStateModule but dedicated for python viewer handles. Used
    mainly by Houdini for registering python handles embedded in digital assets.

    Source code is stored in the ViewerHandle Module section of the Interactive|Handle
    Script tab in the Type Properties dialog.

    Access via hou.OpNode.hdaViewerHandleModule() or hou.NodeType.hdaViewerHandleModule().
    """
    # HDAViewerHandleModule is essentially a Python module wrapper with no specific methods
    # beyond what's available in types.ModuleType. The module's attributes are defined by
    # the user's code in the ViewerHandle Module section of the digital asset.
    pass

class HDADefinition:
    """
    Digital asset definition containing the type definition, parameter interface,
    and embedded content sections.

    Represents a specific version of a digital asset stored in an HDA library file.
    """
    def nodeType(self) -> 'NodeType': ...
    def nodeTypeCategory(self) -> 'NodeTypeCategory': ...
    def nodeTypeName(self) -> str: ...
    def libraryFilePath(self) -> str: ...
    def sections(self) -> dict[str, 'HDASection']: ...
    def addSection(self, section_name: str, contents: str = '') -> 'HDASection': ...
    def removeSection(self, section_name: str) -> None: ...
    def section(self, section_name: str) -> 'HDASection | None': ...
    def options(self) -> 'HDAOptions': ...
    def setOptions(self, options: 'HDAOptions') -> None: ...
    def isInstalled(self) -> bool: ...
    def isPreferred(self) -> bool: ...
    def isCurrent(self) -> bool: ...
    def version(self) -> str: ...
    def setVersion(self, version: str) -> None: ...
    def description(self) -> str: ...
    def setDescription(self, description: str) -> None: ...
    def embeddedHelp(self) -> str: ...
    def setEmbeddedHelp(self, help_text: str) -> None: ...
    def icon(self) -> str: ...
    def setIcon(self, icon_name: str) -> None: ...
    def extraFileOptions(self) -> dict[str, bool]: ...
    def save(self, file_name: str, template_node: 'Node | None' = None, create_backup: bool = True, compress_contents: bool = True) -> None: ...
    def updateFromNode(self, node: 'Node') -> None: ...
    def copyToHDAFile(self, file_name: str, new_name: str | None = None, new_menu_name: str | None = None) -> 'HDADefinition': ...
    def destroy(self) -> None: ...

class HDASection:
    """
    Named data section within a digital asset definition.

    Sections store various content like Python modules, scripts, embedded files,
    and other data associated with the digital asset.
    """
    def name(self) -> str: ...
    def contents(self) -> str: ...
    def setContents(self, contents: str) -> None: ...
    def dataType(self) -> str: ...
    def isCompressed(self) -> bool: ...
    def definition(self) -> 'HDADefinition': ...
    def destroy(self) -> None: ...

class HDAOptions:
    """
    Options and metadata for a digital asset definition.

    Controls various behavioral and organizational aspects of how the
    digital asset appears and functions in Houdini.
    """
    def minNumInputs(self) -> int: ...
    def setMinNumInputs(self, num: int) -> None: ...
    def maxNumInputs(self) -> int: ...
    def setMaxNumInputs(self, num: int) -> None: ...
    def compressContents(self) -> bool: ...
    def setCompressContents(self, on: bool) -> None: ...
    def saveInitialParmsAndContents(self) -> bool: ...
    def setSaveInitialParmsAndContents(self, on: bool) -> None: ...
    def saveSpareParms(self) -> bool: ...
    def setSaveSpareParms(self, on: bool) -> None: ...
    def lockContents(self) -> bool: ...
    def setLockContents(self, on: bool) -> None: ...
    def unlockedHDAData(self) -> dict[str, Any]: ...
    def setUnlockedHDAData(self, data: dict[str, Any]) -> None: ...

class Parm:
    """Houdini parameter object."""
    def __init__(self) -> None: ...

    # Metadata
    def name(self) -> str: ...
    def tuple(self) -> 'ParmTuple': ...
    def path(self) -> str: ...
    def description(self) -> str: ...
    def node(self) -> 'OpNode': ...
    def parmTemplate(self) -> 'ParmTemplate': ...
    def componentIndex(self) -> int: ...
    def isLocked(self) -> bool: ...
    def isSpare(self) -> bool: ...
    def isTimeDependent(self) -> bool: ...
    def disable(self, on: bool) -> None: ...
    def isDisabled(self) -> bool: ...
    def hide(self, on: bool) -> None: ...
    def isHidden(self) -> bool: ...
    def isVisible(self) -> bool: ...

    # Animation
    def alias(self) -> str: ...
    def setAlias(self, alias_name: str) -> None: ...
    def isAutoscoped(self) -> bool: ...
    def isAutoSelected(self) -> bool: ...
    def deleteAllKeyframes(self) -> None: ...
    def deleteKeyframeAtFrame(self, frame: float) -> None: ...
    def keyframes(self) -> tuple: ...  # Returns tuple of BaseKeyframe objects
    def keyframesAfter(self, frame: float) -> tuple: ...  # Returns tuple of BaseKeyframe objects
    def keyframesBefore(self, frame: float) -> tuple: ...  # Returns tuple of BaseKeyframe objects
    def keyframeExtrapolation(self, before: bool) -> 'parmExtrapolate': ...
    def keyframesInRange(self, start_frame: float, end_frame: float) -> tuple: ...  # Returns tuple of BaseKeyframe objects
    def keyframesRefit(self, refit: bool, refit_tol: float, refit_preserve_extrema: bool, refit_bezier: bool, resample: bool, resample_rate: float, resample_tol: float, range: bool, range_start: float, range_end: float, bake_chop: bool) -> None: ...
    def isScoped(self) -> bool: ...
    def isSelected(self) -> bool: ...
    def saveClip(self, file_name: str, start: float|None=None, end: float|None=None, sample_rate: float=0) -> None: ...
    def loadClip(self, file_name: str, sample_rate: float=0, start: float|None=None) -> None: ...
    def clipData(self, start: float|None=None, end: float|None=None, binary: bool=True, use_blosc_compression: bool=True, sample_rate: float=0) -> bytes: ...
    def setClipData(self, data: bytes, binary: bool=True, blosc_compressed: bool=True, sample_rate: float=0, start: float|None=None) -> None: ...

    # Value evaluation
    def unexpandedString(self) -> str: ...
    def eval(self) -> int | float | str: ...
    def evalAsFloat(self) -> float: ...
    def evalAsFloatAtFrame(self, frame: float) -> float: ...
    def evalAsInt(self) -> int: ...
    def evalAsIntAtFrame(self, frame: float) -> int: ...
    def evalAsNode(self) -> 'OpNode': ...
    def evalAsNodeAtFrame(self, frame: float) -> 'OpNode': ...
    def evalAsNodes(self) -> tuple['OpNode', ...]: ...
    def evalAsNodesAtFrame(self, frame: float) -> tuple['OpNode', ...]: ...
    def evalAsString(self) -> str: ...
    def evalAsStringAtFrame(self, frame: float) -> str: ...
    def evalAtTime(self, time: float) -> int | float | str: ...
    def evalAtFrame(self, frame: float) -> int | float | str: ...
    def evalAsRamp(self) -> Any: ...  # Returns Ramp
    def evalAsRampAtFrame(self, frame: float) -> Any: ...  # Returns Ramp
    def evalAsGeometry(self) -> 'Geometry': ...
    def evalAsGeometryAtFrame(self, frame: float) -> 'Geometry': ...
    def evalAsImageLayer(self) -> Any: ...  # Returns ImageLayer
    def evalAsImageLayerAtFrame(self, frame: float) -> Any: ...  # Returns ImageLayer
    def evalAsNanoVDB(self) -> Any: ...  # Returns NanoVDB
    def evalAsNodePath(self) -> str: ...
    def evalAsNodePathAtFrame(self, frame: float) -> str: ...
    def evalAsNodePaths(self) -> tuple[str, ...]: ...
    def evalAsNodePathsAtFrame(self, frame: float) -> tuple[str, ...]: ...
    def rawValue(self) -> str: ...

    # Setting
    def set(self, value: Any, language: exprLanguage|None=None, follow_parm_reference: bool=True) -> None: ...
    def setFromParm(self, src: 'Parm') -> None: ...
    def setFromParmDefaults(self, src: 'Parm') -> None: ...

    # Expressions
    def expression(self) -> str: ...
    def setExpression(self, expression: str, language: exprLanguage|None=None, replace_expression: bool=True) -> None: ...
    def expressionLanguage(self) -> exprLanguage: ...
    def setExpressionLanguage(self, language: exprLanguage) -> None: ...

    # References
    def getReferencedParm(self) -> 'Parm': ...
    def parmsReferencingThis(self) -> tuple['Parm', ...]: ...

    # Defaults
    def hasTemporaryDefaults(self) -> bool: ...
    def isAtDefault(self, compare_temporary_defaults: bool=True, compare_expressions: bool=False) -> bool: ...
    def isAtRampDefault(self) -> bool: ...
    def overwriteDefaults(self) -> None: ...
    def revertToAndRestorePermanentDefaults(self) -> None: ...
    def revertToDefaults(self) -> None: ...
    def revertToRampDefaults(self) -> None: ...

    # Hierarchy
    def containingFolders(self) -> tuple[str, ...]: ...
    def containingFolderSetParmTuples(self) -> tuple['ParmTuple', ...]: ...
    def containingFolderIndices(self) -> tuple[int, ...]: ...

    # Clipboard
    def copyToParmClipboard(self) -> None: ...

    # Multiparms
    def insertMultiParmInstance(self, index: int) -> None: ...
    def removeMultiParmInstance(self, index: int) -> None: ...
    def moveDownMultiParmInstance(self, index: int) -> None: ...
    def moveUpMultiParmInstance(self, index: int) -> None: ...
    def moveMultiParmInstances(self, moves: Any) -> None: ...
    def isMultiParmInstance(self) -> bool: ...
    def isMultiParmParent(self) -> bool: ...
    def parentMultiParm(self) -> 'Parm': ...
    def multiParmInstanceIndices(self) -> tuple[int, ...]: ...
    def multiParmInstances(self) -> tuple['Parm', ...]: ...
    def multiParmInstancesPerItem(self) -> int: ...
    def multiParmInstancesCount(self) -> int: ...
    def multiParmStartOffset(self) -> int: ...

    # Menus
    def isDynamicMenu(self) -> bool: ...
    def menuLabels(self) -> tuple[str, ...]: ...
    def menuItems(self) -> tuple[str, ...]: ...
    def menuContents(self) -> tuple[str, ...]: ...

    # CHOPs
    def overrideTrack(self) -> Any: ...  # Returns Track or None
    def isOverrideTrackActive(self) -> bool: ...
    def createClip(self, parent_node: 'OpNode', name: str, create_new: bool, apply_immediately: bool, current_value_only: bool, create_locked: bool, set_value_to_default: bool) -> Any: ...  # Returns ChopNode
    def appendClip(self, chop_node: Any, apply_immediately: bool, current_value_only: bool, create_locked: bool, set_value_to_default: bool) -> None: ...

    # Scripts
    def pressButton(self, arguments: dict=...) -> None: ...

    # Misc
    def asCode(self, brief: bool=False, save_values: bool=True, save_keyframes: bool=True, save_keys_in_frames: bool=False, save_flag_values: bool=True, save_aliases: bool=True, function_name: str|None=None) -> str: ...
    def uiBackgroundColor(self) -> 'Color': ...
    def lock(self, on: bool) -> None: ...

class ParmTuple:
    """Houdini parameter tuple object (for vector parameters)."""
    def __init__(self) -> None: ...

    # Operators
    def __getitem__(self, index: int) -> 'Parm': ...
    def __len__(self) -> int: ...

    # Metadata
    def name(self) -> str: ...
    def description(self) -> str: ...
    def node(self) -> 'OpNode': ...
    def parmTemplate(self) -> 'ParmTemplate': ...
    def isSpare(self) -> bool: ...
    def isTimeDependent(self) -> bool: ...
    def lock(self, bool_values: Sequence[bool]) -> None: ...
    def disable(self, on: bool) -> None: ...
    def isDisabled(self) -> bool: ...
    def hide(self, on: bool) -> None: ...
    def isHidden(self) -> bool: ...
    def isConstrained(self) -> bool: ...

    # Evaluation
    def eval(self) -> tuple[int | float | str, ...] | Any: ...  # Can return Ramp
    def evalAtTime(self, time: float) -> tuple[int | float | str, ...] | Any: ...  # Can return Ramp
    def evalAtFrame(self, frame: float) -> tuple[int | float | str, ...] | Any: ...  # Can return Ramp
    def evalAsFloats(self) -> tuple[float, ...]: ...
    def evalAsFloatsAtFrame(self, frame: float) -> tuple[float, ...]: ...
    def evalAsInts(self) -> tuple[int, ...]: ...
    def evalAsIntsAtFrame(self, frame: float) -> tuple[int, ...]: ...
    def evalAsRamps(self) -> Any: ...  # Returns Ramp
    def evalAsRampsAtFrame(self, frame: float) -> Any: ...  # Returns Ramp
    def evalAsStrings(self) -> tuple[str, ...]: ...
    def evalAsStringsAtFrame(self, frame: float) -> tuple[str, ...]: ...
    def evalAsGeometries(self) -> tuple['Geometry', ...]: ...
    def evalAsGeometriesAtFrame(self, frame: float) -> tuple['Geometry', ...]: ...
    def evalAsImageLayers(self) -> tuple[Any, ...]: ...  # Returns tuple of ImageLayer
    def evalAsImageLayersAtFrame(self, frame: float) -> tuple[Any, ...]: ...  # Returns tuple of ImageLayer
    def evalAsNanoVDBs(self) -> tuple[Any, ...]: ...  # Returns tuple of NanoVDB
    def evalAsNanoVDBsAtFrame(self, frame: float) -> tuple[Any, ...]: ...  # Returns tuple of NanoVDB
    def evalAsJSONMaps(self) -> tuple[dict[str, str], ...]: ...
    def evalAsJSONMapsAtFrame(self, frame: float) -> tuple[dict[str, str], ...]: ...

    # Setting
    def set(self, values: Sequence[Any], language: exprLanguage|None=None, follow_parm_references: bool=True) -> None: ...

    # Animation
    def saveClip(self, file_name: str, start: float|None=None, end: float|None=None, sample_rate: float=0) -> None: ...
    def loadClip(self, file_name: str, sample_rate: float=0, start: float|None=None) -> None: ...
    def clipData(self, start: float|None=None, end: float|None=None, binary: bool=True, use_blosc_compression: bool=True, sample_rate: float=0) -> bytes: ...
    def setClipData(self, data: bytes, binary: bool=True, blosc_compressed: bool=True, sample_rate: float=0, start: float|None=None) -> None: ...
    def setPending(self, values: Sequence[Any]) -> None: ...
    def deleteAllKeyframes(self) -> None: ...
    def deleteKeyframeAtFrame(self, frame: float) -> None: ...
    def setAutoscope(self, bool_values: Sequence[bool]) -> None: ...
    def setKeyframe(self, keyframe_vector: Any) -> None: ...

    # Expressions
    def isShowingExpression(self) -> bool: ...
    def showExpression(self, on: bool) -> None: ...

    # Defaults
    def overwriteDefaults(self) -> None: ...
    def revertToAndRestorePermanentDefaults(self) -> None: ...
    def revertToDefaults(self) -> None: ...
    def isAtDefault(self, compare_temporary_defaults: bool=True, compare_expressions: bool=False) -> bool: ...
    def isAtRampDefault(self) -> bool: ...

    # Multiparms
    def isMultiParmInstance(self) -> bool: ...
    def isMultiParmParent(self) -> bool: ...
    def parentMultiParm(self) -> 'Parm': ...
    def multiParmInstanceIndices(self) -> tuple[int, ...]: ...
    def multiParmInstances(self) -> tuple['ParmTuple', ...]: ...
    def multiParmInstancesPerItem(self) -> int: ...
    def multiParmInstancesCount(self) -> int: ...
    def multiParmStartOffset(self) -> int: ...

    # CHOPs
    def createClip(self, parent_node: 'OpNode', name: str, create_new: bool, apply_immediately: bool, current_value_only: bool, create_locked: bool, set_value_to_default: bool) -> Any: ...  # Returns ChopNode
    def appendClip(self, chop_node: Any, apply_immediately: bool, current_value_only: bool, create_locked: bool, set_value_to_default: bool) -> None: ...

    # Hierarchy
    def containingFolders(self) -> tuple[str, ...]: ...
    def containingFolderSetParmTuples(self) -> tuple['ParmTuple', ...]: ...
    def containingFolderIndices(self) -> tuple[int, ...]: ...

    # Clipboard
    def copyToParmClipboard(self) -> None: ...

    # Misc
    def asCode(self, brief: bool=False, save_values: bool=True, save_keyframes: bool=True, save_keys_in_frames: bool=False, save_flag_values: bool=True, save_aliases: bool=True, function_name: str|None=None) -> str: ...

    # Scripts
    def pressScriptActionButton(self, arguments: dict=...) -> None: ...

class NodeConnection:
    """Houdini node connection object."""
    def __init__(self) -> None: ...
    def inputNode(self) -> 'Node': ...
    def outputNode(self) -> 'Node': ...
    def inputIndex(self) -> int: ...
    def outputIndex(self) -> int: ...

class NodeType:
    """Houdini node type object."""
    def __init__(self) -> None: ...

    # Basic information
    def name(self) -> str: ...
    def nameComponents(self) -> tuple[str, ...]: ...
    def nameWithCategory(self) -> str: ...
    def namespaceOrder(self) -> tuple[str, ...]: ...
    def versionNamespaceOrder(self) -> tuple[str, ...]: ...
    def description(self) -> str: ...
    def defaultName(self) -> str: ...
    def category(self) -> 'NodeTypeCategory': ...

    # Help and documentation
    def helpUrl(self) -> str: ...
    def defaultHelpUrl(self) -> str: ...
    def embeddedHelp(self) -> str: ...

    # Input/output configuration
    def maxNumInputs(self) -> int: ...
    def minNumInputs(self) -> int: ...
    def maxNumOutputs(self) -> int: ...
    def hasUnorderedInputs(self) -> bool: ...
    def hasEditableInputData(self) -> bool: ...

    # Node behavior
    def isGenerator(self) -> bool: ...
    def isManager(self, include_management_types: bool = True) -> bool: ...
    def hasPermanentUserDefaults(self) -> bool: ...

    # Child nodes
    def childTypeCategory(self) -> 'NodeTypeCategory | None': ...
    def containedNodeTypes(self) -> tuple[str, ...]: ...

    # Appearance
    def defaultColor(self) -> 'Color': ...
    def setDefaultColor(self, color: 'Color') -> None: ...
    def defaultShape(self) -> str: ...
    def setDefaultShape(self, shape: str) -> None: ...
    def icon(self) -> str: ...
    def resolvedIcon(self) -> str: ...

    # Permissions and visibility
    def isWritable(self) -> bool: ...
    def isReadOnly(self) -> bool: ...
    def isReadable(self) -> bool: ...
    def areContentsViewable(self) -> bool: ...

    # Parameters
    def parmTemplates(self) -> tuple['ParmTemplate', ...]: ...
    def parmTemplateGroup(self) -> 'ParmTemplateGroup': ...

    # Metadata
    def deprecationInfo(self) -> dict[str, Any]: ...

    # HDA/Digital Asset methods
    def definition(self) -> 'HDADefinition | None': ...
    def hdaModule(self) -> 'HDAModule': ...
    def hdaViewerStateModule(self) -> 'HDAViewerStateModule': ...
    def hdaViewerHandleModule(self) -> 'HDAViewerHandleModule': ...
    def allInstalledDefinitions(self) -> tuple['HDADefinition', ...]: ...

class ParmTemplateGroup:
    """Houdini parameter template group object."""
    def __init__(self, parm_templates: Sequence['ParmTemplate']=()) -> None: ...

    # Search and access
    def find(self, name: str) -> 'ParmTemplate|None': ...
    def findIndices(self, name_or_parm_template: str | 'ParmTemplate') -> tuple[int, ...]: ...
    def findFolder(self, label_or_labels: str | Sequence[str]) -> Any: ...  # Returns FolderParmTemplate or None
    def findIndicesForFolder(self, label_or_labels: str | Sequence[str]) -> tuple[int, ...]: ...
    def entryAtIndices(self, indices: Sequence[int]) -> 'ParmTemplate': ...
    def containingFolder(self, name_or_parm_template: str | 'ParmTemplate') -> Any: ...  # Returns FolderParmTemplate
    def containingFolderIndices(self, name_or_parm_template_or_indices: str | 'ParmTemplate' | Sequence[int]) -> tuple[int, ...]: ...

    # List contents
    def entries(self) -> tuple['ParmTemplate', ...]: ...
    def parmTemplates(self) -> tuple['ParmTemplate', ...]: ...
    def entriesWithoutFolders(self) -> tuple['ParmTemplate', ...]: ...

    # Modify structure
    def replace(self, name_or_parm_template_or_indices: str | 'ParmTemplate' | Sequence[int], parm_template: 'ParmTemplate') -> None: ...
    def insertBefore(self, name_or_parm_template_or_indices: str | 'ParmTemplate' | Sequence[int], parm_template: 'ParmTemplate') -> None: ...
    def insertAfter(self, name_or_parm_template_or_indices: str | 'ParmTemplate' | Sequence[int], parm_template: 'ParmTemplate') -> None: ...
    def append(self, parm_template: 'ParmTemplate') -> None: ...
    def addParmTemplate(self, parm_template: 'ParmTemplate') -> None: ...
    def appendToFolder(self, label_or_labels_or_parm_template_or_indices: str | Sequence[str] | 'ParmTemplate' | Sequence[int], parm_template: 'ParmTemplate') -> None: ...
    def remove(self, name_or_parm_template_or_indices: str | 'ParmTemplate' | Sequence[int]) -> None: ...

    # Visibility
    def hide(self, name_or_parm_template_or_indices: str | 'ParmTemplate' | Sequence[int], on: bool) -> None: ...
    def hideFolder(self, label_or_labels: str | Sequence[str], on: bool) -> None: ...
    def isHidden(self, name_or_parm_template_or_indices: str | 'ParmTemplate' | Sequence[int]) -> bool: ...
    def isFolderHidden(self, label_or_labels: str | Sequence[str]) -> bool: ...

    # Clear
    def clear(self) -> None: ...

    # Serialization
    def asDialogScript(self, rename_conflicting_parms: bool=False, full_info: bool=False, script_name: str|None=None, script_label: str|None=None, script_tags: dict=...) -> str: ...
    def setToDialogScript(self, dialog_script: str) -> None: ...
    def asCode(self, function_name: str|None=None, variable_name: str|None=None) -> str: ...

    # Metadata
    def sourceNode(self) -> 'OpNode|None': ...
    def sourceNodeType(self) -> 'NodeType|None': ...
    def name(self) -> str: ...
    def setName(self, name: str) -> None: ...
    def label(self) -> str: ...
    def setLabel(self, label: str) -> None: ...

class NodeTypeCategory:
    """Base class for node type categories (SOPs, DOPs, etc.)."""

    # Basic category information
    def label(self) -> str: ...
    def name(self) -> str: ...

    # Node type queries
    def nodeTypes(self) -> dict[str, 'NodeType']: ...
    def nodeType(self, type_name: str) -> 'NodeType|None': ...

    # Sub-network support
    def hasSubNetworkType(self) -> bool: ...
    def subNetworkType(self) -> 'NodeType|None': ...

    # Display properties - color
    def defaultColor(self) -> 'Color': ...
    def clearDefaultColors(self) -> None: ...
    def setDefaultColor(self, color: 'Color') -> None: ...

    # Display properties - shape
    def defaultShape(self) -> str: ...
    def clearDefaultShapes(self) -> None: ...
    def setDefaultShape(self, shape: str) -> None: ...

    # Display properties - wiring
    def defaultWireStyle(self) -> str: ...
    def setDefaultWireStyle(self, wirestyle: str) -> None: ...


class OpNodeTypeCategory(NodeTypeCategory):
    """Category for OP node types (SOPs, DOPs, CHOPs, etc.)."""

    # HDK custom operator loading
    def loadDSO(self, dso_path: str) -> None: ...

    # Digital asset creation
    def createDigitalAsset(self, name: str|None=None, hda_file_name: str|None=None, description: str|None=None) -> 'NodeType': ...

    # Node verbs (SOP category only)
    def nodeVerbs(self) -> dict[str, 'SopVerb']: ...
    def nodeVerb(self, name: str) -> 'SopVerb|None': ...

    # Viewer states
    def viewerStates(self, viewer_type) -> tuple: ...  # Returns tuple of ViewerState objects


class ApexNodeTypeCategory(NodeTypeCategory):
    """Category for APEX node types."""
    # Inherits all methods from NodeTypeCategory base class
    ...

class ApexNode:
    """APEX graph node for procedural geometry operations."""
    def name(self) -> str: ...
    def path(self) -> str: ...
    def nodeType(self) -> 'ApexNodeType': ...
    def connections(self) -> tuple['ApexNodeConnection', ...]: ...

class ApexNodeConnection:
    """Connection between APEX nodes."""
    def sourceNode(self) -> ApexNode: ...
    def destNode(self) -> ApexNode: ...
    def sourcePort(self) -> str: ...
    def destPort(self) -> str: ...

class ApexNodeType:
    """Type definition for APEX nodes."""
    def name(self) -> str: ...
    def category(self) -> str: ...

class AnimBar:
    """Animation toolbar control.

    The animation toolbar lives above the playbar or at the bottom of the animation
    editor, and consists of simple slider tools for easily manipulating animation curves.

    You cannot instantiate this object directly. Call hou.playbar.animBar or
    hou.ChannelEditorPane.animBar instead.

    See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html
    """

    def tools(self, shown_only: bool = True) -> tuple[str, ...]:
        """Returns tool IDs currently on the animation toolbar.

        Args:
            shown_only: If True, returns only visible tools. If False, includes hidden tools.

        Returns:
            Tuple of tool ID strings.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#tools
        """
        ...

    def hiddenTools(self) -> tuple[str, ...]:
        """Returns tool IDs that have been removed from the animation toolbar.

        Returns:
            Tuple of hidden tool ID strings.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#hiddenTools
        """
        ...

    def setTools(self, tool_ids: tuple[str, ...]) -> None:
        """Sets the active tools, replacing previously active tools.

        Args:
            tool_ids: Tuple of tool ID strings to set as active.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#setTools
        """
        ...

    def removeTool(self, id: str) -> None:
        """Removes a tool from the animation toolbar.

        Args:
            id: Tool ID to remove.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#removeTool
        """
        ...

    def addTool(self, id: str, index: int = -1) -> None:
        """Adds a tool to the animation toolbar if not already present.

        Args:
            id: Tool ID to add.
            index: Position index to insert tool. -1 appends to end.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#addTool
        """
        ...

    def reset(self) -> None:
        """Resets the toolbar, restoring all removed tools to original order.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#reset
        """
        ...

    def showLabels(self, show: bool) -> None:
        """Shows or hides tool labels.

        Args:
            show: True to show labels, False to hide.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#showLabels
        """
        ...

    def labelsShown(self) -> bool:
        """Returns whether full labels are currently displayed.

        Returns:
            True if labels are shown, False otherwise.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#labelsShown
        """
        ...

    def setToolSize(self, size: animBarToolSize) -> None:
        """Sets the size of tools on the toolbar.

        Args:
            size: Tool size setting from hou.animBarToolSize enum.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#setToolSize
        """
        ...

    def toolSize(self) -> animBarToolSize:
        """Returns the current tool size.

        Returns:
            Current tool size from hou.animBarToolSize enum.

        See https://www.sidefx.com/docs/houdini/hom/hou/AnimBar.html#toolSize
        """
        ...

class BaseKeyframe:
    """Abstract base class for all keyframe classes.

    This is the base class for hou.Keyframe and hou.StringKeyframe.

    See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html
    """

    def asCode(self, brief: bool = False, save_keys_in_frames: bool = False,
               function_name: str | None = None) -> str:
        """Returns Python code that can recreate this keyframe.

        Args:
            brief: If True, generates more compact code.
            save_keys_in_frames: If True, uses frame numbers instead of seconds.
            function_name: Optional function name to use in generated code.

        Returns:
            Python code string.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#asCode
        """
        ...

    def evaluatedType(self) -> parmData:
        """Returns the type that the keyframe evaluates to.

        Returns:
            Parameter data type enum value.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#evaluatedType
        """
        ...

    def expression(self) -> str:
        """Returns the keyframe's expression.

        Returns:
            Expression string.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#expression
        """
        ...

    def expressionLanguage(self) -> exprLanguage:
        """Returns the expression's language.

        Returns:
            Expression language enum value.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#expressionLanguage
        """
        ...

    def frame(self) -> float:
        """Returns the keyframe's frame number.

        Returns:
            Frame number as float.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#frame
        """
        ...

    def isExpressionLanguageSet(self) -> bool:
        """Returns whether the expression language is explicitly set.

        Returns:
            True if language is set, False otherwise.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#isExpressionLanguageSet
        """
        ...

    def isExpressionSet(self) -> bool:
        """Returns whether an expression is set on this keyframe.

        Returns:
            True if expression is set, False otherwise.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#isExpressionSet
        """
        ...

    def isTimeSet(self) -> bool:
        """Returns whether the keyframe's time is set.

        Returns:
            True if time is set, False otherwise.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#isTimeSet
        """
        ...

    def setExpression(self, expression: str, language: exprLanguage | None = None) -> None:
        """Sets the keyframe's expression and language.

        Args:
            expression: Expression string to set.
            language: Optional expression language. If None, uses default.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#setExpression
        """
        ...

    def setFrame(self, frame: float) -> None:
        """Sets the keyframe's frame number.

        Args:
            frame: Frame number to set.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#setFrame
        """
        ...

    def setTime(self, time: float) -> None:
        """Sets the keyframe's time in seconds.

        Args:
            time: Time in seconds.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#setTime
        """
        ...

    def time(self) -> float:
        """Returns the keyframe's time in seconds.

        Returns:
            Time in seconds as float.

        See https://www.sidefx.com/docs/houdini/hom/hou/BaseKeyframe.html#time
        """
        ...

class ChannelList:
    """Copy of a list of channels from Channel List or Animation Editor.

    See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html
    """

    def clear(self) -> None:
        """Clears the channel list.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#clear
        """
        ...

    def parms(self) -> tuple[Parm, ...]:
        """Returns all channels in the list.

        Returns:
            Tuple of hou.Parm objects.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#parms
        """
        ...

    def selected(self) -> tuple[Parm, ...]:
        """Returns selected channels.

        Returns:
            Tuple of selected hou.Parm objects.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#selected
        """
        ...

    def deselected(self) -> tuple[Parm, ...]:
        """Returns deselected channels.

        Returns:
            Tuple of deselected hou.Parm objects.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#deselected
        """
        ...

    def pinned(self) -> tuple[Parm, ...]:
        """Returns pinned channels.

        Returns:
            Tuple of pinned hou.Parm objects.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#pinned
        """
        ...

    def unpinned(self) -> tuple[Parm, ...]:
        """Returns unpinned channels.

        Returns:
            Tuple of unpinned hou.Parm objects.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#unpinned
        """
        ...

    def selectedValue(self) -> tuple[Parm, ...]:
        """Returns channels with value column selected.

        Returns:
            Tuple of hou.Parm objects with value column selected.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#selectedValue
        """
        ...

    def deselectedValue(self) -> tuple[Parm, ...]:
        """Returns channels with value column deselected.

        Returns:
            Tuple of hou.Parm objects with value column deselected.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#deselectedValue
        """
        ...

    def addParm(self, parm: Parm, selected: bool, pinned: bool, valueselected: bool) -> None:
        """Adds a parameter with flags.

        Args:
            parm: Parameter to add.
            selected: Selection state.
            pinned: Pin state.
            valueselected: Value column selection state.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#addParm
        """
        ...

    def addParms(self, parms: tuple[Parm, ...], selected: bool, pinned: bool,
                 valueselected: bool) -> None:
        """Adds multiple parameters with flags.

        Args:
            parms: Tuple of parameters to add.
            selected: Selection state.
            pinned: Pin state.
            valueselected: Value column selection state.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#addParms
        """
        ...

    def addPath(self, path: str, selected: bool, pinned: bool, valueselected: bool) -> None:
        """Adds a parameter by path with flags.

        Args:
            path: Parameter path.
            selected: Selection state.
            pinned: Pin state.
            valueselected: Value column selection state.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#addPath
        """
        ...

    def addPaths(self, paths: tuple[str, ...], selected: bool, pinned: bool,
                 valueselected: bool) -> None:
        """Adds multiple parameters by path with flags.

        Args:
            paths: Tuple of parameter paths.
            selected: Selection state.
            pinned: Pin state.
            valueselected: Value column selection state.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#addPaths
        """
        ...

    def remove(self, parm: Parm | tuple[Parm, ...]) -> None:
        """Removes parameter(s) from the list.

        Args:
            parm: Single parameter or tuple of parameters to remove.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#remove
        """
        ...

    def select(self, parm: Parm | tuple[Parm, ...]) -> None:
        """Selects parameter(s).

        Args:
            parm: Single parameter or tuple of parameters to select.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#select
        """
        ...

    def deselect(self, parm: Parm | tuple[Parm, ...]) -> None:
        """Deselects parameter(s).

        Args:
            parm: Single parameter or tuple of parameters to deselect.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#deselect
        """
        ...

    def pin(self, parm: Parm | tuple[Parm, ...]) -> None:
        """Pins parameter(s).

        Args:
            parm: Single parameter or tuple of parameters to pin.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#pin
        """
        ...

    def unpin(self, parm: Parm | tuple[Parm, ...]) -> None:
        """Unpins parameter(s).

        Args:
            parm: Single parameter or tuple of parameters to unpin.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#unpin
        """
        ...

    def selectValue(self, parm: Parm | tuple[Parm, ...]) -> None:
        """Selects value column of parameter(s).

        Args:
            parm: Single parameter or tuple of parameters.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#selectValue
        """
        ...

    def deselectValue(self, parm: Parm | tuple[Parm, ...]) -> None:
        """Deselects value column of parameter(s).

        Args:
            parm: Single parameter or tuple of parameters.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#deselectValue
        """
        ...

    def contains(self, parm: Parm) -> bool:
        """Checks if parameter is in the list.

        Args:
            parm: Parameter to check.

        Returns:
            True if parameter is in the list.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#contains
        """
        ...

    def isSelected(self, parm: Parm) -> bool:
        """Checks if parameter is selected.

        Args:
            parm: Parameter to check.

        Returns:
            True if selected.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#isSelected
        """
        ...

    def isPinned(self, parm: Parm) -> bool:
        """Checks if parameter is pinned.

        Args:
            parm: Parameter to check.

        Returns:
            True if pinned.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#isPinned
        """
        ...

    def isValueSelected(self, parm: Parm) -> bool:
        """Checks if parameter's value column is selected.

        Args:
            parm: Parameter to check.

        Returns:
            True if value column is selected.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#isValueSelected
        """
        ...

    def filter(self) -> str:
        """Returns the filter string.

        Returns:
            Filter pattern string.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#filter
        """
        ...

    def keepSelection(self) -> bool:
        """Returns Keep Selection flag.

        Returns:
            True if Keep Selection is enabled.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#keepSelection
        """
        ...

    def enableFilter(self) -> bool:
        """Returns whether filtering is active.

        Returns:
            True if filtering is enabled.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#enableFilter
        """
        ...

    def filterRotates(self) -> bool:
        """Returns whether rotation filtering is active.

        Returns:
            True if rotation filtering is enabled.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#filterRotates
        """
        ...

    def filterTranslates(self) -> bool:
        """Returns whether translation filtering is active.

        Returns:
            True if translation filtering is enabled.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#filterTranslates
        """
        ...

    def filterScales(self) -> bool:
        """Returns whether scale filtering is active.

        Returns:
            True if scale filtering is enabled.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#filterScales
        """
        ...

    def setFilter(self, pattern: str) -> None:
        """Sets the filter string.

        Args:
            pattern: Filter pattern to set.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#setFilter
        """
        ...

    def setKeepSelection(self, on: bool) -> None:
        """Sets Keep Selection flag.

        Args:
            on: True to enable, False to disable.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#setKeepSelection
        """
        ...

    def setEnableFilter(self, on: bool) -> None:
        """Enables or disables filtering.

        Args:
            on: True to enable, False to disable.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#setEnableFilter
        """
        ...

    def setFilterRotates(self, on: bool) -> None:
        """Enables or disables rotation filtering.

        Args:
            on: True to enable, False to disable.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#setFilterRotates
        """
        ...

    def setFilterTranslates(self, on: bool) -> None:
        """Enables or disables translation filtering.

        Args:
            on: True to enable, False to disable.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#setFilterTranslates
        """
        ...

    def setFilterScales(self, on: bool) -> None:
        """Enables or disables scale filtering.

        Args:
            on: True to enable, False to disable.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#setFilterScales
        """
        ...

    def addGeometryChannels(self, geometry: Geometry, collection_name: str | None = None,
                           pattern: str | None = None, selected: bool = True,
                           pinned: bool = False, valueselected: bool = False) -> str:
        """Adds geometry channel collection.

        Args:
            geometry: Geometry containing channel primitives.
            collection_name: Optional name for the collection.
            pattern: Optional pattern to filter channels.
            selected: Selection state.
            pinned: Pin state.
            valueselected: Value column selection state.

        Returns:
            Name of the created collection.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#addGeometryChannels
        """
        ...

    def addNodeGeometryChannels(self, node: Node, pattern: str | None = None,
                                selected: bool = True, pinned: bool = False,
                                valueselected: bool = False) -> str:
        """Adds geometry channels from a node.

        Args:
            node: Node containing geometry with channel primitives.
            pattern: Optional pattern to filter channels.
            selected: Selection state.
            pinned: Pin state.
            valueselected: Value column selection state.

        Returns:
            Name of the created collection.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#addNodeGeometryChannels
        """
        ...

    def removeGeometryChannels(self, collection_name: str | None = None) -> None:
        """Removes geometry channel collection.

        Args:
            collection_name: Name of collection to remove, or None for all.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#removeGeometryChannels
        """
        ...

    def geometryChannelCollectionNames(self) -> tuple[str, ...]:
        """Returns names of geometry channel collections.

        Returns:
            Tuple of collection name strings.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#geometryChannelCollectionNames
        """
        ...

    def geometryChannels(self, collection_name: str) -> tuple[ChannelPrim, ...]:
        """Returns channel primitives in a collection.

        Args:
            collection_name: Name of the collection.

        Returns:
            Tuple of hou.ChannelPrim objects.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#geometryChannels
        """
        ...

    def selectGeometryChannel(self, collection_name: str, channel: str | None = None) -> None:
        """Selects a geometry channel.

        Args:
            collection_name: Collection name.
            channel: Optional specific channel name.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#selectGeometryChannel
        """
        ...

    def deselectGeometryChannel(self, collection_name: str, channel: str | None = None) -> None:
        """Deselects a geometry channel.

        Args:
            collection_name: Collection name.
            channel: Optional specific channel name.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#deselectGeometryChannel
        """
        ...

    def pinGeometryChannel(self, collection_name: str, channel: str | None = None) -> None:
        """Pins a geometry channel.

        Args:
            collection_name: Collection name.
            channel: Optional specific channel name.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#pinGeometryChannel
        """
        ...

    def unpinGeometryChannel(self, collection_name: str, channel: str | None = None) -> None:
        """Unpins a geometry channel.

        Args:
            collection_name: Collection name.
            channel: Optional specific channel name.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#unpinGeometryChannel
        """
        ...

    def selectGeometryChannelValue(self, collection_name: str, channel: str | None = None) -> None:
        """Selects value column of a geometry channel.

        Args:
            collection_name: Collection name.
            channel: Optional specific channel name.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#selectGeometryChannelValue
        """
        ...

    def deselectGeometryChannelValue(self, collection_name: str,
                                    channel: str | None = None) -> None:
        """Deselects value column of a geometry channel.

        Args:
            collection_name: Collection name.
            channel: Optional specific channel name.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#deselectGeometryChannelValue
        """
        ...

    def containsGeometryChannel(self, collection_name: str, channel: str | None = None) -> bool:
        """Checks if geometry channel is present.

        Args:
            collection_name: Collection name.
            channel: Optional specific channel name.

        Returns:
            True if channel is present.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#containsGeometryChannel
        """
        ...

    def isGeometryChannelSelected(self, collection_name: str, channel: str) -> bool:
        """Checks if geometry channel is selected.

        Args:
            collection_name: Collection name.
            channel: Channel name.

        Returns:
            True if selected.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#isGeometryChannelSelected
        """
        ...

    def isGeometryChannelPinned(self, collection_name: str, channel: str) -> bool:
        """Checks if geometry channel is pinned.

        Args:
            collection_name: Collection name.
            channel: Channel name.

        Returns:
            True if pinned.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#isGeometryChannelPinned
        """
        ...

    def isGeometryChannelValueSelected(self, collection_name: str, channel: str) -> bool:
        """Checks if geometry channel's value column is selected.

        Args:
            collection_name: Collection name.
            channel: Channel name.

        Returns:
            True if value column is selected.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#isGeometryChannelValueSelected
        """
        ...

    def asCode(self, var_name: str) -> str:
        """Returns Python code to recreate this ChannelList.

        Args:
            var_name: Variable name to use in generated code.

        Returns:
            Python code string.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelList.html#asCode
        """
        ...


class ChannelPrim(Prim):
    """Geometry primitive that stores channel data.

    Channel primitives are lightweight, standalone channels optimized for quick
    evaluation. They inherit from hou.Prim and provide methods for creating,
    manipulating, and evaluating animation channels stored as geometry primitives.

    You cannot instantiate this object directly. Call hou.Geometry.createChannelPrim
    instead.

    See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html
    """

    def start(self) -> float:
        """Returns the start frame of this channel primitive.

        Returns:
            Start frame number.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#start
        """
        ...

    def end(self) -> float:
        """Returns the end frame of this channel primitive.

        Returns:
            End frame number.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#end
        """
        ...

    def length(self) -> float:
        """Returns the length in frames of this channel primitive.

        Returns:
            Length in frames.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#length
        """
        ...

    def setStart(self, frame: float) -> None:
        """Sets the start frame of this channel primitive.

        Args:
            frame: Start frame number.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#setStart
        """
        ...

    def defaultValue(self) -> float:
        """Returns the default value for this channel primitive.

        The default value is used when the channel is empty.

        Returns:
            Default channel value.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#defaultValue
        """
        ...

    def setDefaultValue(self, value: float) -> None:
        """Sets the default value for this channel primitive.

        Args:
            value: Default value to use when channel is empty.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#setDefaultValue
        """
        ...

    def eval(self, frame: float) -> float:
        """Evaluates the channel at the given frame.

        Args:
            frame: Frame number to evaluate at.

        Returns:
            Evaluated channel value.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#eval
        """
        ...

    def hasKeyAtFrame(self, frame: float) -> bool:
        """Returns whether the channel has a key at the given frame.

        Args:
            frame: Frame number to check.

        Returns:
            True if a key exists at the frame.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#hasKeyAtFrame
        """
        ...

    def insertKey(self, frame: float, auto_slope: bool = True) -> None:
        """Inserts a key at the given frame, if there isn't one already.

        Args:
            frame: Frame number for the key.
            auto_slope: Whether to automatically compute slopes.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#insertKey
        """
        ...

    def destroyKey(self, frame: float) -> None:
        """Destroys a key at the given frame, if one exists.

        Args:
            frame: Frame number of key to destroy.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#destroyKey
        """
        ...

    def destroyKeys(self, frame_start: float, frame_end: float) -> None:
        """Destroys all keys in the given time range, inclusive.

        Args:
            frame_start: Start of frame range.
            frame_end: End of frame range.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#destroyKeys
        """
        ...

    def clear(self) -> None:
        """Clears the channel primitive, removing all keys and segments.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#clear
        """
        ...

    def keyIndex(self, frame: float) -> int:
        """Returns the index of the key at the given frame.

        Args:
            frame: Frame number to query.

        Returns:
            Key index, or -1 if no key exists at that frame.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#keyIndex
        """
        ...

    def keyValue(self, frame: float, value: float,
                 key_half: '_EnumValue[keyHalf]' = keyHalf.Out) -> float:
        """Returns the value of the key at the given frame, if one exists.

        Args:
            frame: Frame number.
            value: Value parameter (purpose unclear in documentation).
            key_half: Which half of the key to query.

        Returns:
            Key value.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#keyValue
        """
        ...

    def setKeyValue(self, frame: float, value: float,
                    key_half: '_EnumValue[keyHalf]' = keyHalf.InOut) -> bool:
        """Sets the value of the key at the given frame, if one exists.

        Args:
            frame: Frame number.
            value: New key value.
            key_half: Which half of the key to set.

        Returns:
            True if successful.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#setKeyValue
        """
        ...

    def keySlope(self, frame: float, value: float,
                 key_half: '_EnumValue[keyHalf]' = keyHalf.Out) -> float:
        """Returns the slope of the key at the given frame, if one exists.

        Args:
            frame: Frame number.
            value: Value parameter (purpose unclear in documentation).
            key_half: Which half of the key to query.

        Returns:
            Key slope.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#keySlope
        """
        ...

    def setKeyAutoSlope(self, frame: float, auto_slope: bool,
                        key_half: '_EnumValue[keyHalf]' = keyHalf.InOut) -> bool:
        """Sets the auto slope property of the key at the given frame.

        Args:
            frame: Frame number.
            auto_slope: Whether to enable auto slope.
            key_half: Which half of the key to set.

        Returns:
            True if successful.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#setKeyAutoSlope
        """
        ...

    def segmentType(self, frame: float) -> segmentType:
        """Returns the type of the segment at the given frame.

        Args:
            frame: Frame number.

        Returns:
            Segment type.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#segmentType
        """
        ...

    def setSegmentType(self, frame: float, type: segmentType) -> None:
        """Sets the type of the segment at the given frame.

        Args:
            frame: Frame number.
            type: Segment type to set.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#setSegmentType
        """
        ...

    def keyFrames(self) -> tuple[float, ...]:
        """Returns an ordered list of frames at which keys exist.

        Returns:
            Tuple of frame numbers with keys.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#keyFrames
        """
        ...

    def keyValues(self, key_half: '_EnumValue[keyHalf]' = keyHalf.Out) -> tuple[float, ...]:
        """Returns values of all keys in the channel.

        Args:
            key_half: Which half of keys to query.

        Returns:
            Tuple of key values.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#keyValues
        """
        ...

    def smoothAutoSlopes(self) -> None:
        """Smooths the slopes of all keys with auto slope enabled.

        See https://www.sidefx.com/docs/houdini/hom/hou/ChannelPrim.html#smoothAutoSlopes
        """
        ...


class Gallery:
    """Collection of gallery entries for operator nodes.

    A gallery is a collection of node templates and their parameter presets,
    represented by hou.GalleryEntry objects. A gallery corresponds to a file
    where such templates are saved.

    You cannot instantiate this object directly. Use hou.galleries module functions
    instead.

    See https://www.sidefx.com/docs/houdini/hom/hou/Gallery.html
    """

    def createEntry(self, entry_name: str, node: Node | None = None) -> GalleryEntry:
        """Creates and returns a new gallery entry.

        Args:
            entry_name: Name for the new entry.
            node: Optional node to initialize entry from.

        Returns:
            The created gallery entry.

        See https://www.sidefx.com/docs/houdini/hom/hou/Gallery.html#createEntry
        """
        ...

    def deleteEntry(self, entry_name: str) -> None:
        """Deletes an entry from the gallery.

        Args:
            entry_name: Name of entry to delete.

        See https://www.sidefx.com/docs/houdini/hom/hou/Gallery.html#deleteEntry
        """
        ...

    def galleryEntries(self, name_pattern: str | None = None,
                      label_pattern: str | None = None,
                      keyword_pattern: str | None = None,
                      category: str | None = None,
                      node_type: NodeType | None = None) -> tuple[GalleryEntry, ...]:
        """Returns gallery entries matching the specified criteria.

        Args:
            name_pattern: Optional pattern for entry names.
            label_pattern: Optional pattern for entry labels.
            keyword_pattern: Optional pattern for entry keywords.
            category: Optional category filter.
            node_type: Optional node type filter.

        Returns:
            Tuple of matching gallery entries.

        See https://www.sidefx.com/docs/houdini/hom/hou/Gallery.html#galleryEntries
        """
        ...


class GalleryEntry:
    """Gallery entry that can be applied to operator nodes.

    A gallery entry contains data about an operator node setup, including parameter
    values, spare parameters, channels, and for subnet nodes, information about
    children. Gallery entries are like node templates or parameter presets that
    can be created from and applied to existing nodes.

    A gallery entry has a unique name and a non-unique label, and is usually
    associated with specific node types. Entries can have categories for organization
    and keywords for identification.

    You cannot instantiate this object directly. Use hou.Gallery.createEntry or
    hou.galleries module functions instead.

    See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html
    """

    def allowIconRegeneration(self) -> bool:
        """Returns whether this entry allows automatic icon regeneration.

        Returns:
            True if automatic icon regeneration is allowed.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#allowIconRegeneration
        """
        ...

    def applyToNode(self, node: Node) -> None:
        """Applies the gallery entry to a given node.

        Args:
            node: Node to apply entry to.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#applyToNode
        """
        ...

    def bestNodeType(self) -> NodeType | None:
        """Returns the best node type associated with this entry.

        Returns:
            Best matching node type, or None.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#bestNodeType
        """
        ...

    def canApplyToNode(self, node: Node) -> bool:
        """Returns whether this entry can be safely applied to the node.

        Args:
            node: Node to check.

        Returns:
            True if entry can be applied to node.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#canApplyToNode
        """
        ...

    def canCreateChildNode(self, parent: Node) -> bool:
        """Returns whether createChildNode can succeed.

        Args:
            parent: Parent network node.

        Returns:
            True if child node can be created.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#canCreateChildNode
        """
        ...

    def categories(self) -> tuple[str, ...]:
        """Returns the categories this entry subscribes to.

        Returns:
            Tuple of category names.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#categories
        """
        ...

    def createChildNode(self, parent: Node) -> Node:
        """Creates a new node in the parent network and applies this entry.

        Args:
            parent: Parent network node.

        Returns:
            The created and configured node.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#createChildNode
        """
        ...

    def description(self) -> str:
        """Returns the description of the gallery entry.

        Returns:
            Entry description.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#description
        """
        ...

    def helpURL(self) -> str:
        """Returns the URL of the help document for this entry.

        Returns:
            Help URL.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#helpURL
        """
        ...

    def isHidden(self) -> bool:
        """Returns whether this entry is hidden from the tools gallery menu.

        Returns:
            True if hidden.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#isHidden
        """
        ...

    def icon(self) -> str:
        """Returns the icon name or file path for this entry.

        Returns:
            Icon name or path.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#icon
        """
        ...

    def keywords(self) -> tuple[str, ...]:
        """Returns the keywords that describe this entry.

        Returns:
            Tuple of keywords.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#keywords
        """
        ...

    def label(self) -> str:
        """Returns the gallery entry label.

        Returns:
            Entry label.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#label
        """
        ...

    def name(self) -> str:
        """Returns the gallery entry name.

        Returns:
            Entry name.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#name
        """
        ...

    def nodeTypeCategory(self) -> NodeTypeCategory:
        """Returns the category of node types this entry is associated with.

        Returns:
            Node type category.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#nodeTypeCategory
        """
        ...

    def nodeTypeNames(self) -> tuple[str, ...]:
        """Returns the names of node types this entry is associated with.

        Returns:
            Tuple of node type names.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#nodeTypeNames
        """
        ...

    def requiredHDAFile(self) -> str:
        """Returns the HDA library file path required by this entry.

        Returns:
            HDA file path.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#requiredHDAFile
        """
        ...

    def script(self) -> str:
        """Returns the script that modifies node parameters.

        Returns:
            Parameter modification script.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#script
        """
        ...

    def setAllowIconRegeneration(self, allow: bool) -> None:
        """Sets the allow icon regeneration flag.

        Args:
            allow: Whether to allow icon regeneration.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setAllowIconRegeneration
        """
        ...

    def setCategories(self, categories: tuple[str, ...]) -> None:
        """Sets the categories this entry subscribes to.

        Args:
            categories: Tuple of category names.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setCategories
        """
        ...

    def setContentsFromNode(self, node: Node) -> None:
        """Saves information about the node contents (child nodes).

        Args:
            node: Node to save contents from.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setContentsFromNode
        """
        ...

    def setDescription(self, description: str) -> None:
        """Sets the description of the gallery entry.

        Args:
            description: Entry description.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setDescription
        """
        ...

    def setEqual(self, entry: GalleryEntry) -> None:
        """Sets this entry to be the same as the given entry, except for name.

        Args:
            entry: Entry to copy from.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setEqual
        """
        ...

    def setHelpURL(self, helpurl: str) -> None:
        """Sets the URL of the help document for this entry.

        Args:
            helpurl: Help URL.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setHelpURL
        """
        ...

    def setHidden(self, hide: bool) -> None:
        """Sets the hidden flag for this entry.

        Args:
            hide: Whether to hide the entry.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setHidden
        """
        ...

    def setIcon(self, icon: str) -> None:
        """Sets the icon name or file path for this entry.

        Args:
            icon: Icon name or path.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setIcon
        """
        ...

    def setKeywords(self, keywords: tuple[str, ...]) -> None:
        """Sets the keywords that describe this entry.

        Args:
            keywords: Tuple of keywords.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setKeywords
        """
        ...

    def setLabel(self, label: str) -> None:
        """Sets the gallery entry label.

        Args:
            label: Entry label.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setLabel
        """
        ...

    def setName(self, name: str) -> None:
        """Sets the gallery entry name.

        Args:
            name: Entry name.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setName
        """
        ...

    def setNodeTypeCategory(self, category: NodeTypeCategory) -> None:
        """Sets the category of node types this entry should be associated with.

        Args:
            category: Node type category.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setNodeTypeCategory
        """
        ...

    def setNodeTypeNames(self, nodetypes: tuple[str, ...]) -> None:
        """Sets the names of node types this entry should be associated with.

        Args:
            nodetypes: Tuple of node type names.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setNodeTypeNames
        """
        ...

    def setRequiredHDAFile(self, hda_file: str) -> None:
        """Sets the HDA library file path required by this entry.

        Args:
            hda_file: HDA file path.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setRequiredHDAFile
        """
        ...

    def setScript(self, script: str) -> None:
        """Sets the script that modifies parameters when entry is applied.

        Args:
            script: Parameter modification script.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setScript
        """
        ...

    def setScriptFromNode(self, node: Node) -> None:
        """Sets the script from a node's parameter values.

        Args:
            node: Node to generate script from.

        See https://www.sidefx.com/docs/houdini/hom/hou/GalleryEntry.html#setScriptFromNode
        """
        ...


class Bookmark:
    """Represents an animation bookmark.

    You cannot instantiate this object directly. Call hou.anim.newBookmark instead.

    See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html
    """
    def name(self) -> str:
        """Returns the name of this bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#name
        """
        ...

    def setName(self, name: str) -> None:
        """Updates the name of the bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#setName
        """
        ...

    def startFrame(self) -> int:
        """Returns the start frame of this bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#startFrame
        """
        ...

    def setStartFrame(self, start_frame: int) -> None:
        """Updates the start frame of the bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#setStartFrame
        """
        ...

    def endFrame(self) -> int:
        """Returns the end frame of this bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#endFrame
        """
        ...

    def setEndFrame(self, end_frame: int) -> None:
        """Updates the end frame of the bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#setEndFrame
        """
        ...

    def comment(self) -> str:
        """Returns the comment of this bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#comment
        """
        ...

    def setComment(self, comment: str) -> None:
        """Updates the comment of the bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#setComment
        """
        ...

    def color(self) -> Color:
        """Returns the color of this bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#color
        """
        ...

    def setColor(self, color: Color) -> None:
        """Updates the color of the bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#setColor
        """
        ...

    def visible(self) -> bool:
        """Returns whether or not this bookmark is visible.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#visible
        """
        ...

    def setVisible(self, visible: bool) -> None:
        """Updates the visibility of the bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#setVisible
        """
        ...

    def isTemporary(self) -> bool:
        """Returns whether or not this bookmark is marked as temporary.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#isTemporary
        """
        ...

    def setTemporary(self, temporary: bool) -> None:
        """Marks this bookmark as temporary or not.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#setTemporary
        """
        ...

    def isEnabled(self) -> bool:
        """Returns whether or not this bookmark is enabled.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#isEnabled
        """
        ...

    def enable(self, enabled: bool) -> None:
        """Enable or disable this bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#enable
        """
        ...

    def metadata(self, key: str, default_value: Any = None) -> Any:
        """Returns the metadata associated with the given key.

        Returns default_value if no such key exists in the metadata.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#metadata
        """
        ...

    def setMetadata(self, key: str, value: Any, type_hint: 'fieldType' = ...) -> None:
        """Adds a metadata property to this bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#setMetadata
        """
        ...

    def sessionId(self) -> int:
        """Returns the ID of the bookmark.

        See https://www.sidefx.com/docs/houdini/hom/hou/Bookmark.html#sessionId
        """
        ...

class Take:
    """Represents a take in Houdini's take system.

    Takes allow you to store different versions of parameter values
    within the same scene, making it easy to manage variations without
    duplicating the entire scene.

    See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html
    """

    def isCurrent(self) -> bool:
        """Return True if the take is the current take.

        Returns:
            True if this is the current take, False otherwise.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#isCurrent
        """
        ...

    def name(self) -> str:
        """Return the name of the take.

        Returns:
            The take name.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#name
        """
        ...

    def setName(self, name: str) -> None:
        """Rename the take.

        Args:
            name: The new name for the take.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#setName
        """
        ...

    def addChildTake(self, name: str) -> Take:
        """Create a new take with the given name and add it as a child to this take.

        Args:
            name: Name for the new child take.

        Returns:
            The newly created child take.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#addChildTake
        """
        ...

    def addNodeDisplayFlag(self, node: Node) -> None:
        """Include the given node's display flag in this take making it editable.

        Args:
            node: The node whose display flag should be included.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#addNodeDisplayFlag
        """
        ...

    def removeNodeDisplayFlag(self, node: Node) -> None:
        """Exclude the given node's display flag from this take.

        Args:
            node: The node whose display flag should be excluded.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#removeNodeDisplayFlag
        """
        ...

    def addNodeBypassFlag(self, node: Node) -> None:
        """Include the given node's bypass flag in this take making it editable.

        Args:
            node: The node whose bypass flag should be included.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#addNodeBypassFlag
        """
        ...

    def removeNodeBypassFlag(self, node: Node) -> None:
        """Exclude the given node's bypass flag from this take.

        Args:
            node: The node whose bypass flag should be excluded.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#removeNodeBypassFlag
        """
        ...

    def addNodeRenderFlag(self, node: Node) -> None:
        """Include the given node's render flag in this take making it editable.

        Args:
            node: The node whose render flag should be included.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#addNodeRenderFlag
        """
        ...

    def removeNodeRenderFlag(self, node: Node) -> None:
        """Exclude the given node's render flag from this take.

        Args:
            node: The node whose render flag should be excluded.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#removeNodeRenderFlag
        """
        ...

    def parmTuples(self) -> tuple[ParmTuple, ...]:
        """Return a tuple of node parameters that are included and editable in this take.

        Returns:
            Tuple of parameter tuples included in this take.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#parmTuples
        """
        ...

    def hasParmTuple(self, parm_tuple: ParmTuple) -> bool:
        """Return True if the given parameter is included in this take.

        Args:
            parm_tuple: The parameter tuple to check.

        Returns:
            True if the parameter is included, False otherwise.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#hasParmTuple
        """
        ...

    def addParmTuple(self, parm_tuple: ParmTuple) -> None:
        """Include the given parameter in this take making it editable.

        Args:
            parm_tuple: The parameter tuple to include.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#addParmTuple
        """
        ...

    def removeParmTuple(self, parm_tuple: ParmTuple) -> None:
        """Exclude the given parameter from this take.

        Args:
            parm_tuple: The parameter tuple to exclude.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#removeParmTuple
        """
        ...

    def addParmTuplesFromTake(self, take: Take, overwrite_existing: bool = True) -> None:
        """Include all the given take's parameters in this take.

        Args:
            take: The take whose parameters should be copied.
            overwrite_existing: Whether to overwrite existing parameter values.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#addParmTuplesFromTake
        """
        ...

    def addParmTuplesFromNode(self, node: Node) -> None:
        """Include all the given node's parameters in this take.

        Args:
            node: The node whose parameters should be included.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#addParmTuplesFromNode
        """
        ...

    def removeParmTuplesFromNode(self, node: Node) -> None:
        """Exclude all the given node's parameters from this take.

        Args:
            node: The node whose parameters should be excluded.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#removeParmTuplesFromNode
        """
        ...

    def children(self) -> tuple[Take, ...]:
        """Return a tuple of the child takes.

        Returns:
            Tuple of child takes.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#children
        """
        ...

    def destroy(self, recurse: bool = False) -> None:
        """Delete the take.

        Args:
            recurse: Whether to recursively delete child takes.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#destroy
        """
        ...

    def parent(self) -> Take | None:
        """Return the parent take or None if this take is the main (master) take.

        Returns:
            The parent take or None.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#parent
        """
        ...

    def path(self) -> str:
        """Return the path of the take.

        Returns:
            The take path.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#path
        """
        ...

    def insertTakeAbove(self, name: str) -> Take:
        """Create a new take with the given name and add it as a child of this take's parent.

        Args:
            name: Name for the new take.

        Returns:
            The newly created take.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#insertTakeAbove
        """
        ...

    def moveUnderTake(self, take: Take) -> None:
        """Reparent this take to the specified take.

        Args:
            take: The new parent take.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#moveUnderTake
        """
        ...

    def saveToFile(self, filename: str, recurse: bool = False) -> None:
        """Save this take to a file on disk.

        Args:
            filename: Path to save the take file.
            recurse: Whether to recursively save child takes.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#saveToFile
        """
        ...

    def loadChildTakeFromFile(self, filename: str) -> tuple[Take, ...]:
        """Load a take from a file and make it a child of this take.

        Args:
            filename: Path to the take file to load.

        Returns:
            Tuple of loaded takes.

        See: https://www.sidefx.com/docs/houdini/hom/hou/Take.html#loadChildTakeFromFile
        """
        ...

class Color:
    """Houdini color object."""
    def __init__(self, rgb: tuple) -> None: ...
    def rgb(self) -> tuple[float, float, float]: ...
    def setRgb(self, rgb: tuple[float, float, float]) -> None: ...
    def hsv(self) -> tuple[float, float, float]: ...
    def setHsv(self, hsv: tuple[float, float, float]) -> None: ...
    def hsl(self) -> tuple[float, float, float]: ...
    def setHsl(self, hsl: tuple[float, float, float]) -> None: ...
    def lab(self) -> tuple[float, float, float]: ...
    def setLAB(self, lab: tuple[float, float, float]) -> None: ...
    def tmi(self) -> tuple[float, float, float]: ...
    def setTmi(self, tmi: tuple[float, float, float]) -> None: ...
    def xyz(self) -> tuple[float, float, float]: ...
    def setXYZ(self, xyz: tuple[float, float, float]) -> None: ...
    def ocio_transform(self, from_space: str, to_space: str, looks: str) -> 'Color': ...
    def ocio_viewTransform(self, src_colorspace, display_name, view_name) -> 'Color': ...
    @staticmethod
    def reload_ocio() -> None: ...
    @staticmethod
    def ocio_spaces() -> tuple[str, ...]: ...
    @staticmethod
    def ocio_configPath() -> str: ...
    @staticmethod
    def ocio_activeDisplays() -> tuple[str, ...]: ...
    @staticmethod
    def ocio_activeViews() -> tuple[str, ...]: ...
    @staticmethod
    def ocio_looks() -> tuple[str, ...]: ...
    @staticmethod
    def ocio_roles() -> tuple[str, ...]: ...
    @staticmethod
    def ocio_views() -> tuple[str, ...]: ...
    @staticmethod
    def ocio_DefaultView() -> str: ...
    @staticmethod
    def ocio_DefaultDisplay() -> str: ...

class Ramp:
    """Interpolated ramp function for float or color values.

    Evaluates between 0.0 and 1.0, with values determined by key positions
    and interpolation basis. Used in ramp parameters for procedural control.
    """
    def __init__(self, basis: tuple, keys: tuple, values: tuple) -> None:
        """Create a ramp with specified basis, keys, and values.

        Args:
            basis: Tuple of hou.rampBasis enum values for interpolation
            keys: Tuple of key positions (0.0 to 1.0)
            values: Tuple of float values or tuple of RGB tuples for color ramps
        """
        ...

    # Type identification
    def isColor(self) -> bool: ...

    # Color-specific
    def colorType(self) -> 'colorType': ...
    def setColorType(self, color_type: 'colorType') -> None: ...

    # Evaluation
    def lookup(self, position: float) -> float | tuple[float, float, float]: ...

    # Structure access
    def basis(self) -> tuple[rampBasis, ...]: ...
    def keys(self) -> tuple[float, ...]: ...
    def values(self) -> tuple[float, ...] | tuple[tuple[float, float, float], ...]: ...

class ParmTemplate:
    """Houdini parameter template base class."""
    def __init__(self) -> None: ...

    # Basic properties
    def clone(self) -> 'ParmTemplate': ...
    def name(self) -> str: ...
    def setName(self, name: str) -> None: ...
    def label(self) -> str: ...
    def setLabel(self, label: str) -> None: ...
    def type(self) -> 'parmTemplateType': ...
    def interfaceType(self) -> 'parmTemplateInterfaceType': ...
    def dataType(self) -> 'parmData': ...

    # Components and naming
    def numComponents(self) -> int: ...
    def setNumComponents(self, num_components: int) -> None: ...
    def namingScheme(self) -> 'parmNamingScheme': ...
    def setNamingScheme(self, naming_scheme: 'parmNamingScheme') -> None: ...

    # Display
    def look(self) -> 'parmLook': ...
    def setLook(self, look: 'parmLook') -> None: ...

    # Help and documentation
    def help(self) -> str: ...
    def setHelp(self, help: str) -> None: ...

    # Visibility
    def isHidden(self) -> bool: ...
    def hide(self, on: bool) -> None: ...
    def isLabelHidden(self) -> bool: ...
    def hideLabel(self, on: bool) -> None: ...

    # Layout
    def joinsWithNext(self) -> bool: ...
    def joinWithNext(self) -> bool: ...
    def setJoinWithNext(self, on: bool) -> None: ...

    # Conditionals
    def disableWhen(self) -> str: ...
    def setDisableWhen(self, disable_when: str) -> None: ...
    def conditionals(self) -> dict[Any, str]: ...  # Dict of parmCondType to str
    def setConditional(self, type: parmCondType, conditional: str) -> None: ...  # Takes parmCondType enum

    # Tags and metadata
    def tags(self) -> dict[str, str]: ...
    def setTags(self, tags: dict[str, str]) -> None: ...

    # Script callbacks
    def scriptCallback(self) -> str: ...
    def setScriptCallback(self, script_callback: str) -> None: ...
    def scriptCallbackLanguage(self) -> scriptLanguage: ...
    def setScriptCallbackLanguage(self, script_callback_language: scriptLanguage) -> None: ...

    # Serialization
    def asCode(self, function_name: str|None=None, variable_name: str|None=None) -> str: ...

class ButtonParmTemplate(ParmTemplate):
    """Parameter template for button parameters that execute scripts."""
    def __init__(
        self,
        name: str,
        label: str,
        script_callback: str|None=None,
        script_callback_language: scriptLanguage=...,
        num_components: int=1,
        is_hidden: bool=False,
        join_with_next: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...
    # No additional methods beyond base ParmTemplate

class DataParmTemplate(ParmTemplate):
    """Parameter template for binary data parameters."""
    def __init__(
        self,
        name: str,
        label: str,
        num_components: int=1,
        naming_scheme: parmNamingScheme=...,
        default_expression: tuple[str, ...]=...,
        default_expression_language: tuple[scriptLanguage, ...]=...,
        data_parm_type: dataParmType=...,
        is_hidden: bool=False,
        join_with_next: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...

    def defaultExpression(self, component_index: int=0) -> str: ...
    def setDefaultExpression(self, default_expression: tuple[str, ...]) -> None: ...
    def defaultExpressionLanguage(self, component_index: int=0) -> scriptLanguage: ...
    def setDefaultExpressionLanguage(self, default_expression_language: tuple[scriptLanguage, ...]) -> None: ...
    def dataParmType(self) -> 'dataParmType': ...
    def setDataParmType(self, data_parm_type: 'dataParmType') -> None: ...

class FloatParmTemplate(ParmTemplate):
    """Parameter template for floating point numeric parameters."""
    def __init__(
        self,
        name: str,
        label: str,
        num_components: int,
        default_value: tuple[float, ...]=...,
        naming_scheme: parmNamingScheme=...,
        min: float=0.0,
        max: float=1.0,
        min_is_strict: bool=False,
        max_is_strict: bool=False,
        look: 'parmLook'=...,
        default_expression: tuple[str, ...]=...,
        default_expression_language: tuple[scriptLanguage, ...]=...,
        is_hidden: bool=False,
        join_with_next: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...

    def defaultValue(self) -> tuple[float, ...]: ...
    def setDefaultValue(self, default_value: tuple[float, ...]) -> None: ...
    def defaultExpression(self, component_index: int=0) -> str: ...
    def setDefaultExpression(self, default_expression: tuple[str, ...]) -> None: ...
    def defaultExpressionLanguage(self, component_index: int=0) -> scriptLanguage: ...
    def setDefaultExpressionLanguage(self, default_expression_language: tuple[scriptLanguage, ...]) -> None: ...
    def minValue(self) -> float: ...
    def setMinValue(self, min: float) -> None: ...
    def maxValue(self) -> float: ...
    def setMaxValue(self, max: float) -> None: ...
    def minIsStrict(self) -> bool: ...
    def setMinIsStrict(self, on: bool) -> None: ...
    def maxIsStrict(self) -> bool: ...
    def setMaxIsStrict(self, on: bool) -> None: ...

class FolderParmTemplate(ParmTemplate):
    """Parameter template for folder organization and multiparm blocks."""
    def __init__(
        self,
        name: str,
        label: str,
        parm_templates: tuple['ParmTemplate', ...]=...,
        folder_type: folderType=...,
        default_value: int=0,
        ends_tab_group: bool=False,
        is_hidden: bool=False,
        tags: dict[str, str]=...
    ) -> None: ...

    def parmTemplates(self) -> tuple['ParmTemplate', ...]: ...
    def setParmTemplates(self, parm_templates: tuple['ParmTemplate', ...]) -> None: ...
    def addParmTemplate(self, parm_template: 'ParmTemplate') -> None: ...
    def folderType(self) -> 'folderType': ...
    def setFolderType(self, folder_type: 'folderType') -> None: ...
    def isActualFolder(self) -> bool: ...
    def defaultValue(self) -> int: ...
    def setDefaultValue(self, default_value: int) -> None: ...
    def tabConditionals(self) -> dict[int, str]: ...
    def setTabConditionals(self, tab_conditionals: dict[int, str]) -> None: ...

class FolderSetParmTemplate(ParmTemplate):
    """Parameter template that controls which folder in a set is visible."""
    def __init__(
        self,
        name: str,
        label: str,
        folder_names: tuple[str, ...]=...,
        folder_type: folderType=...,
        is_hidden: bool=False,
        join_with_next: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...

    def folderNames(self) -> tuple[str, ...]: ...
    def setFolderNames(self, folder_names: tuple[str, ...]) -> None: ...
    def folderType(self) -> 'folderType': ...
    def setFolderType(self, folder_type: 'folderType') -> None: ...

class IntParmTemplate(ParmTemplate):
    """Parameter template for integer numeric parameters with optional menus."""
    def __init__(
        self,
        name: str,
        label: str,
        num_components: int,
        default_value: tuple[int, ...]=...,
        naming_scheme: parmNamingScheme=...,
        min: int=0,
        max: int=10,
        min_is_strict: bool=False,
        max_is_strict: bool=False,
        look: 'parmLook'=...,
        menu_items: tuple[str, ...]=...,
        menu_labels: tuple[str, ...]=...,
        icon_names: tuple[str, ...]=...,
        item_generator_script: str|None=None,
        item_generator_script_language: scriptLanguage=...,
        menu_type: menuType=...,
        menu_use_token: bool=False,
        default_expression: tuple[str, ...]=...,
        default_expression_language: tuple[scriptLanguage, ...]=...,
        is_hidden: bool=False,
        join_with_next: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...

    def defaultValue(self) -> tuple[int, ...]: ...
    def setDefaultValue(self, default_value: tuple[int, ...]) -> None: ...
    def defaultExpression(self, component_index: int=0) -> str: ...
    def setDefaultExpression(self, default_expression: tuple[str, ...]) -> None: ...
    def defaultExpressionLanguage(self, component_index: int=0) -> scriptLanguage: ...
    def setDefaultExpressionLanguage(self, default_expression_language: tuple[scriptLanguage, ...]) -> None: ...
    def minValue(self) -> int: ...
    def setMinValue(self, min: int) -> None: ...
    def maxValue(self) -> int: ...
    def setMaxValue(self, max: int) -> None: ...
    def minIsStrict(self) -> bool: ...
    def setMinIsStrict(self, on: bool) -> None: ...
    def maxIsStrict(self) -> bool: ...
    def setMaxIsStrict(self, on: bool) -> None: ...
    def menuItems(self) -> tuple[str, ...]: ...
    def setMenuItems(self, menu_items: tuple[str, ...]) -> None: ...
    def menuLabels(self) -> tuple[str, ...]: ...
    def setMenuLabels(self, menu_labels: tuple[str, ...]) -> None: ...
    def iconNames(self) -> tuple[str, ...]: ...
    def setIconNames(self, icon_names: tuple[str, ...]) -> None: ...
    def itemGeneratorScript(self) -> str: ...
    def setItemGeneratorScript(self, item_generator_script: str) -> None: ...
    def itemGeneratorScriptLanguage(self) -> scriptLanguage: ...
    def setItemGeneratorScriptLanguage(self, item_generator_script_language: scriptLanguage) -> None: ...
    def menuType(self) -> 'menuType': ...
    def setMenuType(self, menu_type: 'menuType') -> None: ...
    def menuUseToken(self) -> bool: ...
    def setMenuUseToken(self, on: bool) -> None: ...

class LabelParmTemplate(ParmTemplate):
    """Parameter template for static text labels and column headers."""
    def __init__(
        self,
        name: str,
        label: str,
        column_labels: tuple[str, ...]=...,
        label_parm_type: labelParmType=...,
        is_hidden: bool=False,
        join_with_next: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...

    def columnLabels(self) -> tuple[str, ...]: ...
    def setColumnLabels(self, column_labels: tuple[str, ...]) -> None: ...
    def labelParmType(self) -> 'labelParmType': ...
    def setLabelParmType(self, label_parm_type: 'labelParmType') -> None: ...

class MenuParmTemplate(ParmTemplate):
    """Parameter template for menu selection parameters."""
    def __init__(
        self,
        name: str,
        label: str,
        menu_items: tuple[str, ...],
        menu_labels: tuple[str, ...]=...,
        default_value: int=0,
        icon_names: tuple[str, ...]=...,
        item_generator_script: str|None=None,
        item_generator_script_language: scriptLanguage=...,
        menu_type: menuType=...,
        menu_use_token: bool=False,
        default_expression: str|None=None,
        default_expression_language: scriptLanguage=...,
        is_hidden: bool=False,
        join_with_next: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...

    def menuItems(self) -> tuple[str, ...]: ...
    def setMenuItems(self, menu_items: tuple[str, ...]) -> None: ...
    def menuLabels(self) -> tuple[str, ...]: ...
    def setMenuLabels(self, menu_labels: tuple[str, ...]) -> None: ...
    def defaultValue(self) -> int: ...
    def setDefaultValue(self, default_value: int) -> None: ...
    def defaultExpression(self) -> str: ...
    def setDefaultExpression(self, default_expression: str) -> None: ...
    def defaultExpressionLanguage(self) -> scriptLanguage: ...
    def setDefaultExpressionLanguage(self, default_expression_language: scriptLanguage) -> None: ...
    def defaultValueAsString(self) -> str: ...
    def iconNames(self) -> tuple[str, ...]: ...
    def setIconNames(self, icon_names: tuple[str, ...]) -> None: ...
    def itemGeneratorScript(self) -> str: ...
    def setItemGeneratorScript(self, item_generator_script: str) -> None: ...
    def itemGeneratorScriptLanguage(self) -> scriptLanguage: ...
    def setItemGeneratorScriptLanguage(self, item_generator_script_language: scriptLanguage) -> None: ...
    def menuType(self) -> 'menuType': ...
    def setMenuType(self, menu_type: 'menuType') -> None: ...
    def menuUseToken(self) -> bool: ...
    def setMenuUseToken(self, on: bool) -> None: ...
    def setAsMenu(self) -> None: ...
    def isMenu(self) -> bool: ...
    def setAsButtonStrip(self) -> None: ...
    def isButtonStrip(self) -> bool: ...
    def setAsIconStrip(self) -> None: ...
    def isIconStrip(self) -> bool: ...

class RampParmTemplate(ParmTemplate):
    """Parameter template for color or float ramps with interpolation."""
    def __init__(
        self,
        name: str,
        label: str,
        ramp_parm_type: 'rampParmType',
        default_value: int=2,
        default_basis: tuple['rampBasis', ...]=...,
        default_expression: str|None=None,
        default_expression_language: scriptLanguage=...,
        color_type: 'colorType'=...,
        shows_controls: bool=True,
        is_hidden: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...

    def defaultValue(self) -> int: ...
    def setDefaultValue(self, default_value: int) -> None: ...
    def defaultExpression(self) -> str: ...
    def setDefaultExpression(self, default_expression: str) -> None: ...
    def defaultExpressionLanguage(self) -> scriptLanguage: ...
    def setDefaultExpressionLanguage(self, default_expression_language: scriptLanguage) -> None: ...
    def showsControls(self) -> bool: ...
    def setShowsControls(self, shows_controls: bool) -> None: ...
    def parmType(self) -> 'rampParmType': ...
    def setParmType(self, ramp_parm_type: 'rampParmType') -> None: ...
    def defaultBasis(self) -> tuple['rampBasis', ...]: ...
    def setDefaultBasis(self, default_basis: tuple['rampBasis', ...]) -> None: ...
    def colorType(self) -> 'colorType': ...
    def setColorType(self, color_type: 'colorType') -> None: ...
    def parmTemplates(self) -> tuple['ParmTemplate', ...]: ...

class SeparatorParmTemplate(ParmTemplate):
    """Parameter template for visual separator lines."""
    def __init__(
        self,
        name: str,
        is_hidden: bool=False,
        tags: dict[str, str]=...
    ) -> None: ...
    # No additional methods beyond base ParmTemplate

class StringParmTemplate(ParmTemplate):
    """Parameter template for string text parameters with file paths and menus."""
    def __init__(
        self,
        name: str,
        label: str,
        num_components: int,
        default_value: tuple[str, ...]=...,
        naming_scheme: parmNamingScheme=...,
        string_type: stringParmType=...,
        file_type: fileType=...,
        menu_items: tuple[str, ...]=...,
        menu_labels: tuple[str, ...]=...,
        icon_names: tuple[str, ...]=...,
        item_generator_script: str|None=None,
        item_generator_script_language: scriptLanguage=...,
        menu_type: menuType=...,
        menu_use_token: bool=False,
        default_expression: tuple[str, ...]=...,
        default_expression_language: tuple[scriptLanguage, ...]=...,
        is_hidden: bool=False,
        join_with_next: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...

    def defaultValue(self) -> tuple[str, ...]: ...
    def setDefaultValue(self, default_value: tuple[str, ...]) -> None: ...
    def defaultExpression(self, component_index: int=0) -> str: ...
    def setDefaultExpression(self, default_expression: tuple[str, ...]) -> None: ...
    def defaultExpressionLanguage(self, component_index: int=0) -> scriptLanguage: ...
    def setDefaultExpressionLanguage(self, default_expression_language: tuple[scriptLanguage, ...]) -> None: ...
    def stringParmType(self) -> 'stringParmType': ...
    def setStringParmType(self, string_type: 'stringParmType') -> None: ...
    def fileType(self) -> 'fileType': ...
    def setFileType(self, file_type: 'fileType') -> None: ...
    def menuItems(self) -> tuple[str, ...]: ...
    def setMenuItems(self, menu_items: tuple[str, ...]) -> None: ...
    def menuLabels(self) -> tuple[str, ...]: ...
    def setMenuLabels(self, menu_labels: tuple[str, ...]) -> None: ...
    def iconNames(self) -> tuple[str, ...]: ...
    def setIconNames(self, icon_names: tuple[str, ...]) -> None: ...
    def itemGeneratorScript(self) -> str: ...
    def setItemGeneratorScript(self, item_generator_script: str) -> None: ...
    def itemGeneratorScriptLanguage(self) -> scriptLanguage: ...
    def setItemGeneratorScriptLanguage(self, item_generator_script_language: scriptLanguage) -> None: ...
    def menuType(self) -> 'menuType': ...
    def setMenuType(self, menu_type: 'menuType') -> None: ...
    def menuUseToken(self) -> bool: ...
    def setMenuUseToken(self, on: bool) -> None: ...

class ToggleParmTemplate(ParmTemplate):
    """Parameter template for boolean checkbox parameters."""
    def __init__(
        self,
        name: str,
        label: str,
        default_value: bool=False,
        default_expression: str|None=None,
        default_expression_language: scriptLanguage=...,
        is_hidden: bool=False,
        join_with_next: bool=False,
        help: str|None=None,
        tags: dict[str, str]=...
    ) -> None: ...

    def defaultValue(self) -> bool: ...
    def setDefaultValue(self, default_value: bool) -> None: ...
    def defaultExpression(self) -> str: ...
    def setDefaultExpression(self, default_expression: str) -> None: ...
    def defaultExpressionLanguage(self) -> scriptLanguage: ...
    def setDefaultExpressionLanguage(self, default_expression_language: scriptLanguage) -> None: ...

class SopNode(OpNode):
    """
    Represents a surface node.
    Houdini geometry (SOP) node for surface operations.
    """

    def geometry(self, output_index: int = 0) -> 'Geometry | None': ...
    def geometryAtFrame(self, frame: float, output_index: int = 0) -> 'Geometry | None': ...
    def inputGeometry(self, index: int) -> 'Geometry | None': ...
    def inputGeometryAtFrame(self, frame: float, index: int) -> 'Geometry | None': ...
    def generateInputAttribMenu(self, index: int, attrib_type: 'attribType | None' = None, data_type: 'attribData | None' = None, min_size: int = 1, max_size: int = -1, array_type: bool = True, scalar_type: bool = True, case_sensitive: bool = True, pattern: str = "*", decode_tokens: bool = False) -> tuple[str, ...]: ...
    def generateInputGroupMenu(self, index: int, group_types: 'tuple[groupType, ...] | None' = None, include_selection: bool = True, include_name_attrib: bool = True, case_sensitive: bool = True, pattern: str = "*", decode_tokens: bool = False, parm: 'Parm | None' = None) -> tuple[str, ...]: ...
    def geometryDelta(self) -> 'GeometryDelta | None': ...
    def geometryNoDep(self, output_index: int = 0) -> 'Geometry | None': ...
    def geometryDep(self, output_index: int = 0) -> None: ...
    def selection(self, selection_type: 'geometryType') -> 'Selection': ...
    def setSelection(self, selection: 'Selection') -> None: ...
    def curPoint(self) -> 'Point | None': ...
    def setCurPoint(self, point_or_none: 'Point | None' = None) -> None: ...
    def curPrim(self) -> 'Prim | None': ...
    def setCurPrim(self, prim_or_none: 'Prim | None' = None) -> None: ...
    def curVertex(self) -> 'Vertex | None': ...
    def setCurVertex(self, vertex_or_none: 'Vertex | None' = None) -> None: ...
    def displayNode(self) -> 'Node | None': ...
    def renderNode(self) -> 'OpNode | None': ...
    def isBypassed(self) -> bool: ...
    def bypass(self, on: bool) -> None: ...
    def isDisplayFlagSet(self) -> bool: ...
    def setDisplayFlag(self, on: bool) -> None: ...
    def isRenderFlagSet(self) -> bool: ...
    def setRenderFlag(self, on: bool) -> None: ...
    def isHighlightFlagSet(self) -> bool: ...
    def setHighlightFlag(self, on: bool) -> None: ...
    def isTemplateFlagSet(self) -> bool: ...
    def setTemplateFlag(self, on: bool) -> None: ...
    def isSelectableTemplateFlagSet(self) -> bool: ...
    def setSelectableTemplateFlag(self, on: bool) -> None: ...
    def isHardLocked(self) -> bool: ...
    def setHardLocked(self, on: bool) -> None: ...
    def isSoftLocked(self) -> bool: ...
    def setSoftLocked(self, on: bool) -> None: ...
    def isUnloadFlagSet(self) -> bool: ...
    def setUnloadFlag(self, on: bool) -> None: ...
    def hasVerb(self) -> bool: ...
    def verb(self) -> 'SopVerb': ...
    def managesAttribDataIds(self) -> bool: ...
    def setManagesAttribDataIds(self, on: bool) -> None: ...

class ShopNode(OpNode):
    """Houdini shader shop (SHOP) node."""
    def bypass(self, on: bool) -> None: ...
    def isBypassed(self) -> bool: ...
    def setDisplayFlag(self, on: bool) -> None: ...
    def isDisplayFlagSet(self) -> bool: ...
    def displayNode(self) -> Node: ...

class VopNode(OpNode):
    """Houdini VEX operator (VOP) node for shader networks."""
    def bypass(self, on: bool) -> None: ...
    def isBypassed(self) -> bool: ...
    def setDisplayFlag(self, on: bool) -> None: ...
    def isDisplayFlagSet(self) -> bool: ...
    def displayNode(self) -> Node: ...

class VopNetNode(OpNode):
    """Houdini VOP network container node."""
    def displayNode(self) -> Node: ...

class ObjNode(OpNode):
    """
    Houdini object (OBJ) node.
    Handles transforms and object-level operations.
    """
    # Transforms
    def worldTransform(self) -> Matrix4: ...
    def setWorldTransform(self, matrix: Matrix4) -> None: ...
    def localTransform(self) -> Matrix4: ...
    def setLocalTransform(self, matrix: Matrix4) -> None: ...
    def worldTransformAtTime(self, time: float) -> Matrix4: ...
    def localTransformAtTime(self, time: float) -> Matrix4: ...
    def parmTransform(self) -> Matrix4: ...
    def setParmTransform(self, matrix: Matrix4) -> None: ...
    def parmPivotTransform(self) -> Matrix4: ...
    def setParmPivotTransform(self, matrix: Matrix4, fail_on_locked_parms: bool=False) -> None: ...
    def parentAndSubnetTransform(self) -> Matrix4: ...

    # Pre-transform
    def preTransform(self) -> Matrix4: ...
    def setPreTransform(self, matrix: Matrix4, fail_on_locked_parms: bool=False) -> None: ...
    def moveParmTransformIntoPreTransform(self) -> None: ...
    def movePreTransformIntoParmTransform(self) -> None: ...

    # Transforming relative to other nodes
    def origin(self) -> Vector3: ...
    def setOrigin(self, origin: Vector3) -> None: ...

    # Geometry
    def combine(self, nodes: tuple[ObjNode, ...]) -> None: ...
    def displayNode(self) -> OpNode|None: ...
    def renderNode(self) -> OpNode|None: ...

    # Flags
    def isObjectDisplayed(self) -> bool: ...
    def isObjectDisplayedAtFrame(self, frame: float) -> bool: ...
    def isDisplayFlagSet(self) -> bool: ...
    def setDisplayFlag(self, on: bool) -> None: ...
    def isSelectableInViewport(self) -> bool: ...
    def setSelectableInViewport(self, on: bool) -> None: ...
    def isShowingOrigin(self) -> bool: ...
    def showOrigin(self, on: bool) -> None: ...
    def isUsingXray(self) -> bool: ...
    def useXray(self, on: bool) -> None: ...

    # Shading
    def material(self, operation: str, parameter: str) -> Any: ...

    # Python objects
    def setCookTransform(self, matrix: Matrix4) -> None: ...

    # Animation
    def saveParmClip(self, file_name: str, start: float|None=None, end: float|None=None, sample_rate: float=0, scoped_only: bool=False) -> None: ...
    def parmClipData(self, start: float|None=None, end: float|None=None, binary: bool=True, use_blosc_compression: bool=True, sample_rate: float=0, scoped_only: bool=False) -> bytes: ...

class ChopNode(OpNode):
    """Houdini channel operator (CHOP) node.

    CHOPs process motion/animation channel data. Extends OpNode for full operator functionality.
    """

    # Clip access
    def clip(self, output_index: int = 0) -> Any: ...  # Returns Clip
    def clipData(self, binary: bool) -> bytes: ...  # ASCII or binary clip data
    def setClipData(self, data: bytes|str, binary: bool) -> None: ...  # Set clip data
    def saveClip(self, file_name: str) -> None: ...  # Save clip to file

    # Track access
    def tracks(self) -> tuple['Track', ...]: ...  # All tracks in this node
    def track(self, track_name: str) -> 'Track|None': ...  # Get track by name

    # Sample conversion
    def sampleRange(self) -> tuple[float, float]: ...  # (start, end) sample range
    def sampleRate(self) -> float: ...  # Samples per second
    def frameToSamples(self, frame: float) -> float: ...  # Convert frame to samples
    def samplesToFrame(self, samples: float) -> float: ...  # Convert samples to frame
    def samplesToTime(self, samples: float) -> float: ...  # Convert samples to seconds
    def timeToSamples(self, time: float) -> float: ...  # Convert seconds to samples

    # Flags
    def bypass(self, on: bool) -> None: ...  # Set bypass flag
    def isBypassed(self) -> bool: ...  # Bypass flag state
    def isDisplayFlagSet(self) -> bool: ...  # Display flag state
    def setDisplayFlag(self, on: bool) -> None: ...  # Set display flag
    def isExportFlagSet(self) -> bool: ...  # Export flag state
    def setExportFlag(self, on: bool) -> None: ...  # Set export flag
    def isAudioFlagSet(self) -> bool: ...  # Audio flag state
    def setAudioFlag(self, on: bool) -> None: ...  # Set audio flag
    def isCurrentFlagSet(self) -> bool: ...  # Current flag state
    def setCurrentFlag(self, on: bool) -> None: ...  # Set current flag
    def isUnloadFlagSet(self) -> bool: ...  # Unload flag state
    def setUnloadFlag(self, on: bool) -> None: ...  # Set unload flag
    def isLocked(self) -> bool: ...  # Lock flag state
    def setLocked(self, on: bool) -> None: ...  # Set lock flag

class RopNode(OpNode):
    """Houdini render operator (ROP) node.

    ROPs handle rendering and output operations. Extends OpNode for full operator functionality.
    """

    # Rendering
    def render(self,
               frame_range: tuple[float, float]|None = None,
               res: tuple[int, int]|None = None,
               output_file: str|None = None,
               output_format: str|None = None,
               to_flipbook: bool = False,
               quality: int = 2,
               ignore_inputs: bool = False,
               method: renderMethod|None = None,
               ignore_bypass_flags: bool = False,
               ignore_lock_flags: bool = False,
               verbose: bool = False,
               output_progress: bool = False) -> None: ...  # Render this node

    # Input dependencies
    def inputDependencies(self) -> tuple[tuple['RopNode', ...], tuple[tuple[float, ...], ...]]: ...  # (ROPs, frames) that need rendering first

    # Render event callbacks
    def addRenderEventCallback(self, callback: Any, run_before_script: bool = False) -> None: ...  # Add render event callback
    def removeRenderEventCallback(self, callback: Any) -> None: ...  # Remove render event callback
    def removeAllRenderEventCallbacks(self) -> None: ...  # Remove all render event callbacks

    # Flags
    def bypass(self, on: bool) -> None: ...  # Set bypass flag
    def isBypassed(self) -> bool: ...  # Bypass flag state
    def isLocked(self) -> bool: ...  # Lock flag state
    def setLocked(self, on: bool) -> None: ...  # Set lock flagclass VopNode(Node):
    """Houdini VEX operator (VOP) node."""
    def vexCode(self) -> str: ...  # Generated VEX code
    def shaderName(self) -> str: ...

class DopNode(OpNode):
    """Houdini dynamics operator (DOP) node."""
    # DOP-specific methods
    def processedObjects(self) -> tuple['DopObject', ...]: ...
    def createdObjects(self) -> tuple['DopObject', ...]: ...
    def dopNetNode(self) -> OpNode: ...
    def simulation(self) -> 'DopSimulation': ...
    def isDisplayFlagSet(self) -> bool: ...
    def displayNode(self) -> OpNode|None: ...
    def setDisplayFlag(self, on: bool) -> None: ...
    def isTemplateFlagSet(self) -> bool: ...
    def setTemplateFlag(self, on: bool) -> None: ...
    def bypass(self, on: bool) -> None: ...
    def isBypassed(self) -> bool: ...
    def objectsToProcess(self) -> tuple['DopObject', ...]: ...
    def pythonSolverData(self) -> 'DopData': ...

# Additional specialized node types
class CopNode(OpNode):
    """Houdini compositing operator (COP) node."""
    # Geometry access
    def geometry(self, output_index: int=0) -> Geometry: ...
    def geometryAtFrame(self, frame: float, output_index: int=0) -> Geometry: ...

    # Layer access
    def layer(self, output_index: int=0) -> 'ImageLayer': ...
    def layerAtFrame(self, frame: float, output_index: int=0) -> 'ImageLayer': ...

    # VDB access
    def vdb(self, output_index: int=0) -> 'NanoVDB': ...
    def vdbAtFrame(self, frame: float, output_index: int=0) -> 'NanoVDB': ...

    # Verb support
    def hasVerb(self) -> bool: ...
    def verb(self) -> 'CopVerb': ...

    # Flags
    def setDisplayFlag(self, on: bool) -> None: ...
    def isDisplayFlagSet(self) -> bool: ...
    def setExportFlag(self, on: bool) -> None: ...
    def isExportFlagSet(self) -> bool: ...
    def setTemplateFlag(self, on: bool) -> None: ...
    def isTemplateFlagSet(self) -> bool: ...
    def isSelectableTemplateFlagSet(self) -> bool: ...
    def setSelectableTemplateFlag(self, on: bool) -> None: ...
    def setCompressFlag(self, on: bool) -> None: ...
    def isCompressFlagSet(self) -> bool: ...
    def bypass(self, on: bool) -> None: ...
    def isBypassed(self) -> bool: ...
    def displayNode(self) -> Node: ...

    # Inputs and Outputs
    def inputDataTypes(self) -> tuple[str, ...]: ...
    def outputDataTypes(self) -> tuple[str, ...]: ...
    def isInputCompatible(self, idx: int, other: Node, other_idx: int, allow_conversions: bool=False) -> bool: ...
    def inputCableStructure(self, idx: int) -> 'CopCableStructure': ...
    def outputCableStructure(self, idx: int) -> 'CopCableStructure': ...

class Cop2Node(OpNode):
    """Houdini COP2 (Composite Operator 2) node for image compositing."""
    def bypass(self, on: bool) -> None: ...
    def isBypassed(self) -> bool: ...
    def setDisplayFlag(self, on: bool) -> None: ...
    def isDisplayFlagSet(self) -> bool: ...
    def displayNode(self) -> Node: ...

class CopCableStructure:
    """Describes the structure of image data flowing through COP connections."""
    pass

class ImageLayer:
    """Represents an image layer in compositor operations."""
    pass

class NanoVDB:
    """NanoVDB volume representation for compositor operations."""
    pass

class LopNode(OpNode):
    """Houdini lighting operator (LOP/Solaris) node for USD scene graph operations."""
    # Flags
    def bypass(self, on: bool) -> None: ...
    def isBypassed(self) -> bool: ...
    def isDisplayFlagSet(self) -> bool: ...
    def setDisplayFlag(self, on: bool) -> None: ...
    def isDebugFlagSet(self) -> bool: ...
    def setDebugFlag(self, on: bool) -> None: ...

    # Display nodes
    def displayNode(self) -> Node: ...
    def viewerNode(self) -> Node: ...

    # USD Stage access
    def activeLayer(self, output_index: int=-1, ignore_errors: bool=False, use_last_cook_context_options: bool=True, frame: float|None=None, context_options: dict=...) -> Any: ...  # Returns pxr.Sdf.Layer
    def stage(self, output_index: int=-1, apply_viewport_overrides: bool=False, ignore_errors: bool=False, use_last_cook_context_options: bool=True, apply_post_layers: bool=True, frame: float|None=None, context_options: dict=...) -> Any: ...  # Returns pxr.Usd.Stage
    def isMostRecentStageLock(self) -> bool: ...
    def inEditLayerBlock(self) -> bool: ...

    # Stage statistics
    def stagePrimStats(self, primpath: str|None=None, output_index: int=-1, apply_viewport_overrides: bool=False, ignore_errors: bool=False, do_geometry_counts: bool=False, do_separate_purposes: bool=False, use_last_cook_context_options: bool=True, apply_post_layers: bool=True, frame: float|None=None, context_options: dict=..., do_kind_counts: bool=False, include_root: bool=True) -> dict: ...

    # Load masks
    def loadMasks(self, output_index: int=-1, force_cook: bool=False, use_last_cook_context_options: bool=True, frame: float|None=None, context_options: dict=...) -> 'LopViewportLoadMasks': ...

    # Primitive tracking
    def lastModifiedPrims(self) -> tuple: ...  # Returns tuple of pxr.Sdf.Path
    def inputPrims(self, inputidx: int) -> tuple: ...  # Returns tuple of pxr.Sdf.Path
    def setLastModifiedPrims(self, primpaths: list) -> None: ...

    # Save paths
    def savePaths(self) -> list[str]: ...

    # Selection rules
    def selectionRule(self, inputidx: int=-1, pattern: str|None=None) -> 'LopSelectionRule': ...

    # Python LOP scripting methods
    def editableLayer(self) -> Any: ...  # Returns pxr.Sdf.Layer with edit permission
    def editableStage(self) -> Any: ...  # Returns pxr.Usd.Stage with edit permission
    def uneditableStage(self) -> Any: ...  # Returns pxr.Usd.Stage without edit permission
    def addSubLayer(self, identifier: str) -> None: ...
    def addLockedGeometry(self, identifier: str, geo: Geometry, args: dict=...) -> str: ...

class LopNetwork(OpNode):
    """Houdini LOP network node containing LOP nodes."""
    # Cooking
    def displayNode(self) -> Node: ...
    def viewerNode(self) -> Node: ...
    def isDebugFlagSet(self) -> bool: ...
    def setDebugFlag(self, on: bool) -> None: ...

    # Selection
    def setSelection(self, selection: tuple[str, ...], currentprim: str|None=None) -> None: ...
    def selection(self) -> tuple[str, ...]: ...
    def selectionWithInstanceIds(self) -> tuple[str, ...]: ...
    def selectionCurrentPrim(self) -> str: ...
    def selectionRules(self) -> dict[str, 'LopSelectionRule']: ...
    def clearSelectionRules(self) -> None: ...
    def setSelectionRule(self, name: str, rule: Any) -> None: ...  # rule is LopSelectionRule

    # Viewport stage manipulation
    def viewportOverrides(self, lop: LopNode, output_index: int=0) -> Any: ...  # Returns LopViewportOverrides
    def namedViewportOverrides(self) -> tuple[str, ...]: ...
    def loadNamedViewportOverrides(self, name: str) -> None: ...
    def saveNamedViewportOverrides(self, name: str, overrides: Any=None) -> None: ...  # overrides is LopViewportOverrides
    def copyViewportOverrides(self, saved_name: str) -> Any: ...  # Returns LopViewportOverrides
    def setViewportOverrides(self, overrides: Any) -> None: ...  # overrides is LopViewportOverrides
    def viewportOverridesLayer(self, layer_id: Any) -> Any: ...  # Returns pxr.Sdf.Layer
    def viewportLoadMasks(self) -> Any: ...  # Returns LopViewportLoadMasks
    def setViewportLoadMasks(self, payload_config: Any) -> None: ...  # payload_config is LopViewportLoadMasks
    def namedViewportLoadMasks(self) -> tuple[str, ...]: ...
    def loadNamedViewportLoadMasks(self, name: str) -> Any: ...  # Returns LopViewportLoadMasks
    def saveNamedViewportLoadMasks(self, name: str) -> None: ...

    # Scene graph tree expansion state
    def expansionState(self) -> Any: ...  # Returns LopExpansionState
    def setExpansionState(self, expansion_state: Any) -> None: ...  # expansion_state is LopExpansionState
    def saveNamedExpansionState(self, name: str, expansion_state: Any) -> None: ...  # expansion_state is LopExpansionState
    def loadNamedExpansionState(self, name: str) -> Any: ...  # Returns LopExpansionState
    def namedExpansionStates(self) -> tuple[str, ...]: ...
    def setPrimitiveExpansionLocked(self, path: str, expanded_subpaths: Any, preserve_descendant_expansion: bool=True) -> bool: ...
    def setPrimitiveExpansionUnlocked(self, path: str, preserve_descendant_expansion: bool=True) -> bool: ...

    # Post-layers
    def postLayerNames(self) -> tuple[str, ...]: ...
    def postLayer(self, name: str) -> Any: ...  # Returns pxr.Sdf.Layer or None
    def removePostLayer(self, name: str) -> None: ...
    def editablePostLayer(self, name: str, lop: LopNode, output_index: int=0) -> 'LopPostLayer': ...

class LopExpansionState:
    """Tracks expansion state of USD primitives in LOP networks."""
    pass

class LopInstanceIdRule:
    """Rules for assigning instance IDs to USD primitives."""
    pass

class LopLockedStage:
    """Represents a locked USD stage from a LOP node."""
    pass

class LopPostLayer:
    """Post-process layer applied to USD stages."""
    pass

class LopSelectionRule:
    """Selection rule for USD primitives in LOP networks."""
    pass

class LopViewportLoadMasks:
    """Controls which USD primitives are loaded in the viewport."""
    pass

class LopViewportOverrides:
    """Viewport display overrides for USD primitives."""
    pass

class TopNode(Node):
    """Houdini task operator (TOP/PDG) node."""
    # Flags
    def bypass(self, on: bool) -> None: ...
    def isBypassed(self) -> bool: ...
    def isDisplayFlagSet(self) -> bool: ...
    def isRenderFlagSet(self) -> bool: ...
    def setDisplayFlag(self, on: bool) -> None: ...
    def setRenderFlag(self, on: bool) -> None: ...

    # Display/render nodes
    def displayNode(self) -> 'OpNode': ...
    def outputNode(self) -> 'OpNode': ...
    def renderNode(self) -> 'OpNode': ...
    def topParent(self) -> 'OpNode': ...

    # Work item cooking
    def cookWorkItems(self, block: bool = False, generate_only: bool = False, tops_only: bool = False, save_prompt: bool = False, nodes: list = []) -> None: ...
    def cookOutputWorkItems(self, block: bool = False, generate_only: bool = False, tops_only: bool = False) -> None: ...
    def cookAllOutputWorkItems(self, include_display_node: bool, block: bool = False, generate_only: bool = False, tops_only: bool = False) -> None: ...
    def executeGraph(self, filter_static: bool = False, block: bool = False, generate_only: bool = False, tops_only: bool = False) -> None: ...  # Deprecated

    # Static work item generation
    def generateStaticItems(self, block: bool) -> None: ...  # Deprecated
    def generateStaticWorkItems(self, block: bool = False, nodes: list = []) -> None: ...

    # Work item management
    def dirtyAllTasks(self, remove_outputs: bool) -> None: ...  # Deprecated
    def dirtyAllWorkItems(self, remove_outputs: bool) -> None: ...
    def dirtyTasks(self, remove_outputs: bool) -> None: ...  # Deprecated
    def dirtyWorkItems(self, remove_outputs: bool) -> None: ...

    # Graph commands
    def graphCommands(self) -> str: ...
    def taskGraphCommands(self) -> str: ...

    # PDG integration
    def getPDGGraphContextName(self) -> str: ...
    def getPDGGraphContext(self): ...  # Returns pdg.GraphContext
    def getPDGNodeName(self) -> str: ...
    def getPDGNode(self): ...  # Returns pdg.Node
    def getPDGNodeId(self) -> int: ...
    def getDataLayerInterfaceId(self) -> int: ...

    # Work item selection and filtering
    def getWorkItemName(self, idx: int) -> str: ...
    def setSelectedWorkItem(self, idx: int) -> bool: ...
    def getSelectedWorkItem(self) -> int: ...
    def addPDGFilter(self, idx: int) -> None: ...
    def removePDGFilter(self, idx: int) -> None: ...
    def isPDGFilter(self, idx: int) -> bool: ...
    def enablePDGFilter(self, filter_on: bool) -> None: ...
    def isFilterOn(self) -> bool: ...
    def getFilterNodes(self) -> tuple['OpNode', ...]: ...

    # Node type queries
    def isScheduler(self) -> bool: ...
    def isMapper(self) -> bool: ...
    def isProcessor(self) -> bool: ...
    def isPartitioner(self) -> bool: ...

    # Data types
    def outputDataTypes(self) -> tuple[str, ...]: ...
    def inputDataTypes(self) -> tuple[str, ...]: ...

    # Cook state
    def getCookState(self, force: bool) -> 'topCookState': ...
    def cancelCook(self) -> None: ...
    def pauseCook(self) -> None: ...

    # Work item states
    def workItemStates(self) -> list[int]: ...
    def workItems(self) -> tuple['WorkItem', ...]: ...

    # Collapsed items
    def collapsedItem(self, idx: int) -> int: ...
    def collapsedItems(self) -> tuple[int, ...]: ...
    def workItemsInCollapsedItemIds(self, id: int) -> tuple[int, ...]: ...

class NodeGroup:
    """
    Houdini node group object.

    Represents a node group that contains a set of nodes from the same network.
    Each group is named, and you can edit a group's contents from the network view pane.
    """
    def __init__(self) -> None: ...

    def name(self) -> str: ...
    def parent(self) -> 'OpNode': ...
    def nodes(self) -> tuple['OpNode', ...]: ...
    def addNode(self, node: 'OpNode') -> None: ...
    def removeNode(self, node: 'OpNode') -> None: ...
    def clear(self) -> None: ...
    def destroy(self) -> None: ...
    def asCode(self, save_creation_commands: bool = False, function_name: str|None = None) -> str: ...

class NodeInfoTree:
    """
    Houdini node info tree object.

    A tree structure designed to contain information about nodes and the data they
    generate. This class represents a tree structure, where each branch of the tree can have
    any number of named sub-trees, as well as a two dimensional grid of strings. Most
    often this grid has two columns ("Property" and "Value"), with some number of
    rows to represent arbitrary key/value pairs. But the grid can also contain more
    complex data (such as the volume information in geometry data).
    """
    def __init__(self) -> None: ...

    def name(self) -> str: ...
    def infoType(self) -> str: ...
    def branchOrder(self) -> tuple[str, ...]: ...
    def branches(self) -> dict[str, 'NodeInfoTree']: ...
    def headings(self) -> tuple[str, ...]: ...
    def rows(self) -> tuple[tuple[str, ...], ...]: ...

class Attrib:
    """Houdini geometry attribute."""
    def __init__(self) -> None: ...
    def name(self) -> str: ...
    def dataType(self) -> 'attribData': ...
    def size(self) -> int: ...

class Geometry:
    """Houdini geometry object containing points and primitives."""
    # Constructor
    def __init__(self, src_geo: 'Geometry | None' = None, clone_data_ids: bool = False) -> None: ...

    # Validation
    def isValid(self) -> bool: ...

    # Attributes - Finding
    def findPointAttrib(self, name: str, scope: 'attribScope' = ...) -> 'Attrib | None': ...
    def findPrimAttrib(self, name: str, scope: 'attribScope' = ...) -> 'Attrib | None': ...
    def findVertexAttrib(self, name: str, scope: 'attribScope' = ...) -> 'Attrib | None': ...
    def findGlobalAttrib(self, name: str, scope: 'attribScope' = ...) -> 'Attrib | None': ...

    # Attributes - Listing
    def pointAttribs(self, scope: 'attribScope' = ...) -> tuple['Attrib', ...]: ...
    def primAttribs(self, scope: 'attribScope' = ...) -> tuple['Attrib', ...]: ...
    def vertexAttribs(self, scope: 'attribScope' = ...) -> tuple['Attrib', ...]: ...
    def globalAttribs(self, scope: 'attribScope' = ...) -> tuple['Attrib', ...]: ...

    # Attributes - Creating
    def addAttrib(self, type: 'attribType', name: str, default_value: int | float | str | Sequence, transform_as_normal: bool = False, create_local_variable: bool = False) -> 'Attrib': ...
    def addArrayAttrib(self, type: 'attribType', name: str, data_type: 'attribData', tuple_size: int = 1) -> 'Attrib': ...

    # Attributes - Global values
    def attribValue(self, name_or_attrib: str | 'Attrib') -> int | float | str | tuple | dict: ...
    def floatAttribValue(self, name_or_attrib: str | 'Attrib') -> float: ...
    def floatListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[float, ...]: ...
    def intAttribValue(self, name_or_attrib: str | 'Attrib') -> int: ...
    def intListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[int, ...]: ...
    def stringAttribValue(self, name_or_attrib: str | 'Attrib') -> str: ...
    def stringListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[str, ...]: ...
    def dictAttribValue(self, name_or_attrib: str | 'Attrib') -> dict: ...
    def dictListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[str, ...]: ...
    def setGlobalAttribValue(self, name_or_attrib: str | 'Attrib', attrib_value: int | float | str | Sequence) -> None: ...

    # Attributes - Capture
    def attributeCaptureRegions(self) -> tuple[str, ...]: ...
    def attributeCaptureObjectPaths(self) -> tuple[str, ...]: ...

    # Attributes - Misc
    def attribType(self) -> 'attribType': ...
    def renamePointAttrib(self, old_name: str, new_name: str) -> None: ...
    def renamePrimAttrib(self, old_name: str, new_name: str) -> None: ...
    def renameVertexAttrib(self, old_name: str, new_name: str) -> None: ...
    def renameGlobalAttrib(self, old_name: str, new_name: str) -> None: ...
    def generateAttribMenu(self, attrib_type: 'attribType | None' = None, data_type: 'attribData | None' = None, min_size: int = 1, max_size: int = -1, array_type: bool = True, scalar_type: bool = True, case_sensitive: bool = True, pattern: str = "*", decode_tokens: bool = False) -> tuple[str, ...]: ...
    def copyAttrib(self, attrib: 'Attrib') -> None: ...
    def copyAttribs(self, attribs: Sequence['Attrib']) -> None: ...

    # Intrinsics
    def intrinsicValue(self, intrinsic_name: str) -> int | float | str | tuple: ...
    def intrinsicNames(self) -> tuple[str, ...]: ...
    def intrinsicValueDict(self) -> dict[str, int | float | str | tuple]: ...
    def setIntrinsicValue(self, intrinsic_name: str, value: int | float | str | Sequence) -> None: ...
    def intrinsicReadOnly(self, intrinsic_name: str) -> bool: ...
    def intrinsicSize(self, intrinsic_name: str) -> int: ...
    def preferredPrecision(self) -> int: ...
    def setPreferredPrecision(self, precision: int) -> None: ...

    # Data modification tracking
    def vexAttribDataId(self) -> tuple[int, ...]: ...
    def modificationCounter(self) -> int: ...
    def incrementModificationCounter(self) -> None: ...
    def incrementAllDataIds(self) -> None: ...
    def incrementDataIdsForAddOrRemove(self, for_points: bool = True, for_prims: bool = True) -> None: ...
    def primitiveIntrinsicsDataId(self) -> Any: ...  # AttribDataId
    def incrementPrimitiveIntrinsicsDataId(self) -> None: ...
    def topologyDataId(self) -> Any: ...  # AttribDataId
    def incrementTopologyDataId(self) -> None: ...

    # Averages and bounding
    def pointBoundingBox(self, pointpattern: str) -> 'BoundingBox': ...
    def primBoundingBox(self, primpattern: str) -> 'BoundingBox': ...
    def boundingBox(self, transform: 'Matrix4 | None' = None) -> 'BoundingBox': ...
    def orientedBoundingBox(self) -> 'OrientedBoundingBox': ...
    def orientedPointBoundingBox(self, pointpattern: str) -> 'OrientedBoundingBox': ...
    def orientedPrimBoundingBox(self, primpattern: str) -> 'OrientedBoundingBox': ...
    def averageMinDistance(self, local_transform: 'Matrix4', geometry: 'Geometry', geometry_transform: 'Matrix4') -> float: ...
    def averageEdgeLength(self) -> float: ...

    # Creation - Points
    def createPoint(self) -> 'Point': ...
    def createPoints(self, point_positions: Sequence[Sequence[float]]) -> tuple['Point', ...]: ...

    # Creation - Polygons
    def createPolygon(self, is_closed: bool = True) -> 'Polygon': ...
    def createPolygons(self, points: Sequence[Sequence['Point']], is_closed: bool = True) -> tuple['Polygon', ...]: ...

    # Creation - Volumes
    def createTetrahedron(self) -> 'Prim': ...
    def createTetrahedronInPlace(self, p0: 'Point', p1: 'Point', p2: 'Point', p3: 'Point') -> 'Prim': ...
    def createHexahedron(self) -> 'Prim': ...
    def createHexahedronInPlace(self, p0: 'Point', p1: 'Point', p2: 'Point', p3: 'Point', p4: 'Point', p5: 'Point', p6: 'Point', p7: 'Point') -> 'Prim': ...

    # Creation - Curves
    def createNURBSCurve(self, num_vertices: int = 4, is_closed: bool = False, order: int = 4) -> 'Face': ...
    def createBezierCurve(self, num_points: int = 4, is_closed: bool = False, order: int = 4) -> 'Face': ...

    # Creation - Surfaces
    def createNURBSSurface(self, rows: int, cols: int, is_closed_in_u: bool = False, is_closed_in_v: bool = False) -> 'Surface': ...
    def createBezierSurface(self, rows: int, cols: int, is_closed_in_u: bool = False, is_closed_in_v: bool = False) -> 'Surface': ...
    def createMeshSurface(self, rows: int, cols: int, is_closed_in_u: bool = False, is_closed_in_v: bool = False) -> 'Surface': ...

    # Creation - Volume and packed
    def createVolume(self, xres: int, yres: int, zres: int, bounding_box: 'BoundingBox | None' = None) -> 'Volume': ...
    def createChannelPrim(self) -> Any: ...  # ChannelPrim
    def createPacked(self, typename: str, point: 'Point | None' = None) -> Any: ...  # PackedPrim
    def createPackedGeometry(self, geo: 'Geometry', point: 'Point | None' = None) -> Any: ...  # PackedPrim

    # Deletion
    def deletePrims(self, prims: Sequence['Prim'], keep_points: bool = False) -> None: ...
    def deletePrimsOutsideBoundingBox(self, bbox: 'BoundingBox') -> None: ...
    def deletePoints(self, points: Sequence['Point']) -> None: ...

    # Groups - Point
    def findPointGroup(self, name: str, scope: groupScope = ...) -> 'PointGroup | None': ...
    def pointGroups(self, scope: groupScope = ...) -> tuple['PointGroup', ...]: ...
    def createPointGroup(self, name: str, is_ordered: bool = False, unique_name: bool = False) -> 'PointGroup': ...

    # Groups - Primitive
    def findPrimGroup(self, name: str, scope: groupScope = ...) -> 'PrimGroup | None': ...
    def primGroups(self, scope: groupScope = ...) -> tuple['PrimGroup', ...]: ...
    def createPrimGroup(self, name: str, is_ordered: bool = False, unique_name: bool = False) -> 'PrimGroup': ...

    # Groups - Edge
    def findEdgeGroup(self, name: str, scope: groupScope = ...) -> 'EdgeGroup | None': ...
    def edgeGroups(self, scope: groupScope = ...) -> tuple['EdgeGroup', ...]: ...
    def createEdgeGroup(self, name: str) -> 'EdgeGroup': ...

    # Groups - Vertex
    def findVertexGroup(self, name: str, scope: groupScope = ...) -> 'VertexGroup | None': ...
    def vertexGroups(self, scope: groupScope = ...) -> tuple['VertexGroup', ...]: ...
    def createVertexGroup(self, name: str, is_ordered: bool = False) -> 'VertexGroup': ...

    # Groups - Menu generation
    def generateGroupMenu(self, group_types: Sequence[str] | None = None, include_selection: bool = True, include_name_attrib: bool = True, case_sensitive: bool = True, pattern: str = "*", decode_tokens: bool = False, parm: 'Parm | None' = None) -> tuple[str, ...]: ...

    # Freezing
    def freeze(self, read_only: bool = False, clone_data_ids: bool = False) -> 'Geometry': ...
    def isReadOnly(self) -> bool: ...

    # Nodes
    def sopNode(self) -> 'SopNode | None': ...
    def sopNodeOutputIndex(self) -> int: ...

    # Points - Access
    def pointCount(self) -> int: ...
    def points(self) -> tuple['Point', ...]: ...
    def iterPoints(self) -> Any: ...  # generator of Point
    def globPoints(self, pattern: str, ordered: bool = False) -> tuple['Point', ...]: ...
    def point(self, index: int) -> 'Point': ...
    def nearestPoint(self, position: Sequence[float], ptgroup: Any = None, max_radius: float = 1e18) -> 'Point | None': ...
    def nearestPoints(self, position: Sequence[float], max_points: int, ptgroup: Any = None, max_radius: float = 1e18) -> tuple['Point', ...]: ...

    # Points - Bulk attribute access
    def pointFloatAttribValues(self, name: str) -> tuple[float, ...]: ...
    def pointFloatAttribValuesAsString(self, name: str, float_type: 'numericData' = ...) -> bytes: ...
    def setPointFloatAttribValues(self, name: str, values: Sequence[float]) -> None: ...
    def setPointFloatAttribValuesFromString(self, name: str, values: bytes, float_type: 'numericData' = ...) -> None: ...
    def pointIntAttribValues(self, name: str) -> tuple[int, ...]: ...
    def pointIntAttribValuesAsString(self, name: str, int_type: 'numericData' = ...) -> bytes: ...
    def setPointIntAttribValues(self, name: str, values: Sequence[int]) -> None: ...
    def setPointIntAttribValuesFromString(self, name: str, values: bytes, int_type: 'numericData' = ...) -> None: ...
    def pointStringAttribValues(self, name: str) -> tuple[str, ...]: ...
    def setPointStringAttribValues(self, name: str, values: Sequence[str]) -> None: ...

    # Edges
    def findEdge(self, p0: 'Point', p1: 'Point') -> 'Edge': ...
    def globEdges(self, pattern: str) -> tuple['Edge', ...]: ...

    # Primitives - Access
    def nearestPrim(self, position: Sequence[float]) -> tuple['Prim | None', float, float, float]: ...
    def primCount(self) -> int: ...
    def prims(self) -> tuple['Prim', ...]: ...
    def iterPrims(self) -> Any: ...  # generator of Prim
    def primsOfType(self, primtype: 'primType') -> tuple['Prim', ...]: ...
    def iterPrimsOfType(self, primtype: 'primType') -> Any: ...  # generator of Prim
    def globPrims(self, pattern: str) -> tuple['Prim', ...]: ...
    def prim(self, index: int) -> 'Prim': ...

    # Primitives - Type info
    def primTypeNames(self) -> tuple[str, ...]: ...
    def primTypeLabels(self) -> tuple[str, ...]: ...
    def primTypeIcons(self) -> tuple[str, ...]: ...
    def containsPrimType(self, type_or_name: 'primType | str') -> bool: ...
    def countPrimType(self, type_or_name: 'primType | str') -> int: ...
    def countUnusedPoints(self) -> int: ...

    # Primitives - Bulk attribute access
    def primFloatAttribValues(self, name: str) -> tuple[float, ...]: ...
    def primFloatAttribValuesAsString(self, name: str) -> bytes: ...
    def setPrimFloatAttribValues(self, name: str, values: Sequence[float]) -> None: ...
    def setPrimFloatAttribValuesFromString(self, name: str, values: bytes, float_type: 'numericData' = ...) -> None: ...
    def primIntAttribValues(self, name: str) -> tuple[int, ...]: ...
    def primIntAttribValuesAsString(self, name: str, int_type: 'numericData' = ...) -> bytes: ...
    def setPrimIntAttribValues(self, name: str, values: Sequence[int]) -> None: ...
    def setPrimIntAttribValuesFromString(self, name: str, values: bytes, int_type: 'numericData' = ...) -> None: ...
    def primStringAttribValues(self, name: str) -> tuple[str, ...]: ...
    def setPrimStringAttribValues(self, name: str, values: Sequence[str]) -> None: ...

    # Primitives - Intersection
    def intersect(self, ray_origin: Sequence[float], ray_direction: Sequence[float], position_out: list, normal_out: list, uvw_out: list, pattern: str | None = None, min_hit: float = 0.01, max_hit: float = 1e18, tolerance: float = 0.01) -> int: ...

    # Vertices - Access
    def vertexCount(self) -> int: ...
    def globVertices(self, pattern: str) -> tuple['Vertex', ...]: ...

    # Vertices - Bulk attribute access
    def vertexFloatAttribValues(self, name: str) -> tuple[float, ...]: ...
    def vertexFloatAttribValuesAsString(self, name: str, float_type: 'numericData' = ...) -> bytes: ...
    def setVertexFloatAttribValues(self, name: str, values: Sequence[float]) -> None: ...
    def setVertexFloatAttribValuesFromString(self, name: str, values: bytes, float_type: 'numericData' = ...) -> None: ...
    def vertexIntAttribValues(self, name: str) -> tuple[int, ...]: ...
    def vertexIntAttribValuesAsString(self, name: str, int_type: 'numericData' = ...) -> bytes: ...
    def setVertexIntAttribValues(self, name: str, values: Sequence[int]) -> None: ...
    def setVertexIntAttribValuesFromString(self, name: str, values: bytes, int_type: 'numericData' = ...) -> None: ...
    def vertexStringAttribValues(self, name: str) -> tuple[str, ...]: ...
    def setVertexStringAttribValues(self, name: str, values: Sequence[str]) -> None: ...

    # Data - I/O
    def data(self) -> bytes: ...
    def load(self, data: bytes) -> None: ...
    def saveToFile(self, file_name: str) -> None: ...
    def loadFromFile(self, file_name: str) -> None: ...
    def clear(self) -> None: ...

    # Data - Merging and copying
    def merge(self, geometry: 'Geometry', clone_data_ids: bool = False, prims: Sequence['Prim'] | None = None) -> None: ...
    def mergePoints(self, geometry: 'Geometry', points: Sequence['Point'] | None = None) -> None: ...
    def mergePrims(self, geometry: 'Geometry', prims: Sequence['Prim'] | None = None) -> None: ...
    def mergeEdges(self, geometry: 'Geometry', edges: Sequence | None = None) -> None: ...
    def copy(self, geometry: 'Geometry', clone_data_ids: bool = False, prims: Sequence['Prim'] | None = None) -> None: ...
    def copyPoints(self, geometry: 'Geometry', points: Sequence['Point'] | None = None) -> None: ...
    def copyPrims(self, geometry: 'Geometry', prims: Sequence['Prim'] | None = None) -> None: ...
    def copyEdges(self, geometry: 'Geometry', edges: Sequence | None = None) -> None: ...

    # Data - Verb execution
    def execute(self, verb: 'SopVerb', inputs: Sequence['Geometry'] = []) -> 'Geometry': ...

    # Data - USD/LOP import
    def importLop(self, lopnode: 'LopNode', selectionrule: Any, purpose: str | None = None, traversal: Any | None = None, path_attrib_name: str | None = None, name_attrib_name: str | None = None, strip_layers: bool = False, frame: float | None = None, lop_output_index: int = -1) -> Any: ...  # LopLockedStage
    def importUsdStage(self, stage: Any, selectionrule: Any, purpose: str | None = None, traversal: Any | None = None, path_attrib_name: str | None = None, name_attrib_name: str | None = None, frame: float | None = None) -> None: ...

    # Transformation
    def transform(self, matrix: 'Matrix4') -> None: ...
    def transformPrims(self, prims: Sequence['Prim'], matrix: 'Matrix4') -> None: ...

    # Loops
    def primLoop(self, prims: Sequence['Prim'], loop_type: componentLoopType) -> tuple['Prim', ...]: ...
    def pointLoop(self, points: Sequence['Point'], full_loop: bool) -> tuple['Point', ...]: ...
    def edgeLoop(self, edges: Sequence['Edge'], loop_type: componentLoopType, full_loop_per_edge: bool, force_ring: bool, allow_ring: bool) -> tuple['Edge', ...]: ...
    def pointNormals(self, points: Sequence['Point']) -> tuple['Vector3', ...]: ...

    # Selection
    def selection(self) -> 'Selection': ...

    # Packed folders
    def extractPackedPaths(self, pattern: str) -> tuple[str, ...]: ...
    def unpackFromFolder(self, path: str) -> 'Geometry': ...
    def removeFromFolder(self, path: str) -> bool: ...
    def packToFolder(self, path: str, geometry: 'Geometry', is_folder: bool = False, is_visible: bool = True, pack: bool = True) -> bool: ...
    def packedFolderProperties(self, path: str) -> dict: ...

class Point:
    """Houdini geometry point."""
    def __init__(self) -> None: ...
    # Point data
    def geometry(self) -> 'Geometry': ...
    def number(self) -> int: ...
    def prims(self) -> tuple['Prim', ...]: ...
    def vertices(self) -> tuple['Vertex', ...]: ...
    def position(self) -> 'Vector3': ...
    def setPosition(self, position: Sequence[float] | 'Vector3') -> None: ...
    def weight(self) -> float: ...
    def setWeight(self, weight: float) -> None: ...
    # Attributes
    def attribType(self) -> 'attribType': ...
    def attribValue(self, name_or_attrib: str | 'Attrib') -> int | float | str | tuple | dict: ...
    def setAttribValue(self, name_or_attrib: str | 'Attrib', attrib_value: int | float | str | Sequence) -> None: ...
    def floatAttribValue(self, name_or_attrib: str | 'Attrib') -> float: ...
    def floatListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[float, ...]: ...
    def intAttribValue(self, name_or_attrib: str | 'Attrib') -> int: ...
    def intListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[int, ...]: ...
    def stringAttribValue(self, name_or_attrib: str | 'Attrib') -> str: ...
    def stringListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[str, ...]: ...
    def dictAttribValue(self, name_or_attrib: str | 'Attrib') -> dict: ...
    def dictListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[str, ...]: ...

class Prim:
    """Houdini geometry primitive."""
    def __init__(self) -> None: ...
    def number(self) -> int: ...
    def vertices(self) -> tuple['Vertex', ...]: ...

class Vertex:
    """Houdini geometry vertex."""
    def __init__(self) -> None: ...
    # Attributes
    def attribValue(self, name_or_attrib: str | 'Attrib') -> int | float | str | tuple | dict: ...
    def floatAttribValue(self, name_or_attrib: str | 'Attrib') -> float: ...
    def floatListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[float, ...]: ...
    def intAttribValue(self, name_or_attrib: str | 'Attrib') -> int: ...
    def intListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[int, ...]: ...
    def stringAttribValue(self, name_or_attrib: str | 'Attrib') -> str: ...
    def stringListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[str, ...]: ...
    def dictAttribValue(self, name_or_attrib: str | 'Attrib') -> dict: ...
    def dictListAttribValue(self, name_or_attrib: str | 'Attrib') -> tuple[str, ...]: ...
    def setAttribValue(self, name_or_attrib: str | 'Attrib', attrib_value: int | float | str | Sequence) -> None: ...
    def attribType(self) -> 'attribType': ...
    # Vertex data
    def point(self) -> 'Point': ...
    def prim(self) -> 'Prim': ...
    def geometry(self) -> 'Geometry': ...
    def number(self) -> int: ...
    def linearNumber(self) -> int: ...

class Polygon(Face):
    """Houdini polygon primitive.

    A Polygon is a Face whose vertices are connected via straight lines.
    Inherits all methods from Face and its base class Prim.

    Currently Face and Prim contain all necessary methods for polygon inspection and manipulation.
    """
    pass

class Face(Prim):
    """Houdini NURBS/Bezier curve face primitive.

    Face primitives represent NURBS or Bezier curves, storing a sequence of vertices.
    """
    # Vertex management
    def addVertex(self, point: 'Point') -> 'Vertex': ...
    def vertex(self, index: int) -> 'Vertex': ...

    # Topology
    def isClosed(self) -> bool: ...
    def setIsClosed(self, on: bool) -> None: ...
    def closed(self) -> bool: ...  # Deprecated, use isClosed()

    # Geometry queries
    def normal(self) -> 'Vector3': ...
    def positionAt(self, u: float) -> 'Vector3': ...
    def attribValueAt(self, attrib_or_name: str | 'Attrib', u: float, du: int = 0) -> int | float | str | tuple: ...
    def arcLength(self, u_start: float, u_stop: float, divs: int = 10) -> float: ...

class Surface(Prim):
    """Houdini NURBS/Bezier/Mesh surface primitive.

    Surface primitives store a 2D grid of vertices for NURBS surfaces, Bezier surfaces, or meshes.
    """
    # Grid dimensions
    def numCols(self) -> int: ...
    def numRows(self) -> int: ...

    # Vertex access
    def vertex(self, u_index: int, v_index: int) -> 'Vertex': ...
    def verticesInCol(self, u_index: int) -> tuple['Vertex', ...]: ...
    def verticesInRow(self, v_index: int) -> tuple['Vertex', ...]: ...

    # Vertex grid modification
    def addCol(self, after: int = -1) -> None: ...
    def addRow(self, after: int = -1) -> None: ...

    # Geometry queries
    def positionAt(self, u: float, v: float) -> 'Vector3': ...
    def normalAt(self, u: float, v: float) -> 'Vector3': ...
    def attribValueAt(self, attrib_or_name: str | 'Attrib', u: float, v: float, du: int = 0, dv: int = 0) -> int | float | str | tuple: ...

    # Topology
    def isClosedInU(self) -> bool: ...
    def isClosedInV(self) -> bool: ...

class Volume(Prim):
    """Houdini volume primitive for storing 3D voxel data.

    Volumes store a 3D array of voxel values with various storage types and visualization modes.
    """
    # Volume properties
    def resolution(self) -> 'Vector3': ...
    def channelCount(self) -> int: ...
    def storageType(self) -> 'volumeStorageType': ...
    def visualization(self) -> 'volumeVisualization': ...

    # Voxel sampling
    def sample(self, position: Sequence[float]) -> float: ...
    def gradient(self, position: Sequence[float]) -> 'Vector3': ...
    def voxel(self, index: Sequence[int]) -> float: ...
    def setVoxel(self, index: Sequence[int], value: float) -> None: ...

    # Bulk voxel access
    def allVoxels(self) -> tuple[float, ...]: ...
    def allVoxelsAsString(self) -> bytes: ...
    def setAllVoxels(self, values: Sequence[float]) -> None: ...
    def setAllVoxelsFromString(self, values: bytes) -> None: ...

    # Voxel slices
    def voxelSlice(self, plane: str, index: int) -> tuple[float, ...]: ...
    def voxelSliceAsString(self, plane: str, index: int) -> bytes: ...
    def setVoxelSlice(self, values: Sequence[float], plane: str, index: int) -> None: ...
    def setVoxelSliceFromString(self, values: bytes, plane: str, index: int) -> None: ...

    # Coordinate conversion
    def posToIndex(self, position: Sequence[float]) -> tuple[int, int, int]: ...
    def indexToPos(self, index: Sequence[int]) -> 'Vector3': ...
    def isValidIndex(self, index: Sequence[int]) -> bool: ...

    # Volume type flags
    def isSDF(self) -> bool: ...
    def isHeightField(self) -> bool: ...

    # Statistics
    def volumeAverage(self) -> float: ...
    def volumeMin(self) -> float: ...
    def volumeMax(self) -> float: ...

    # Transformation
    def transform(self) -> 'Matrix3': ...
    def setTransform(self, matrix4: 'Matrix4') -> None: ...
    def voxelSize(self) -> 'Vector3': ...

class VDB(Prim):
    """Houdini VDB volume primitive for sparse voxel data structures."""
    def resolution(self) -> tuple[int, int, int]: ...
    def activeVoxelCount(self) -> int: ...
    def activeVoxelBoundingBox(self) -> 'BoundingBox': ...
    def voxelSize(self) -> tuple[float, float, float]: ...
    def transform(self) -> 'Matrix4': ...
    def taperX(self) -> float: ...
    def taperY(self) -> float: ...

class Quadric(Prim):
    """Houdini quadric primitive (sphere, tube, circle, etc.)."""
    def transform(self) -> 'Matrix4': ...
    def setTransform(self, matrix4: 'Matrix4') -> None: ...

class PackedPrim(Prim):
    """Base class for packed primitives that reference geometry."""
    def embeddedGeometry(self) -> 'Geometry': ...
    def sharedEmbeddedGeometry(self) -> 'Geometry': ...
    def intrinsicNames(self) -> tuple[str, ...]: ...
    def intrinsicValue(self, name: str) -> Any: ...
    def setIntrinsicValue(self, name: str, value: Any) -> None: ...
    def intrinsicSize(self, name: str) -> int: ...
    def fullName(self) -> str: ...
    def implementation(self) -> Any: ...  # Returns packed implementation object

class PackedGeometry(PackedPrim):
    """Packed primitive containing embedded geometry."""
    def setEmbeddedGeometry(self, geometry: 'Geometry') -> None: ...

class PackedFragment(PackedPrim):
    """Packed primitive referencing an RBD fragment."""
    pass

class Edge:
    """Houdini edge connecting two points."""
    def prims(self) -> tuple[Prim, ...]: ...
    def point(self, index: int) -> Point: ...
    def isValid(self) -> bool: ...
    def geometry(self) -> 'Geometry': ...
    def length(self) -> float: ...

class PointGroup:
    """Group of geometry points."""
    def name(self) -> str: ...
    def geometry(self) -> 'Geometry': ...
    def points(self) -> tuple[Point, ...]: ...
    def add(self, point_or_points: Point | Sequence[Point] | Sequence[int]) -> None: ...
    def remove(self, point_or_points: Point | Sequence[Point] | Sequence[int]) -> None: ...
    def clear(self) -> None: ...
    def contains(self, point: Point | int) -> bool: ...
    def destroy(self) -> None: ...
    def options(self) -> dict[str, Any]: ...
    def setOptions(self, options: dict[str, Any]) -> None: ...

class PrimGroup:
    """Group of geometry primitives."""
    def name(self) -> str: ...
    def geometry(self) -> 'Geometry': ...
    def prims(self) -> tuple[Prim, ...]: ...
    def add(self, prim_or_prims: Prim | Sequence[Prim] | Sequence[int]) -> None: ...
    def remove(self, prim_or_prims: Prim | Sequence[Prim] | Sequence[int]) -> None: ...
    def clear(self) -> None: ...
    def contains(self, prim: Prim | int) -> bool: ...
    def destroy(self) -> None: ...
    def options(self) -> dict[str, Any]: ...
    def setOptions(self, options: dict[str, Any]) -> None: ...

class EdgeGroup:
    """Group of geometry edges."""
    def name(self) -> str: ...
    def geometry(self) -> 'Geometry': ...
    def edges(self) -> tuple[Edge, ...]: ...
    def add(self, edge: Edge) -> None: ...
    def remove(self, edge: Edge) -> None: ...
    def clear(self) -> None: ...
    def contains(self, edge: Edge) -> bool: ...
    def destroy(self) -> None: ...

class VertexGroup:
    """Group of geometry vertices."""
    def name(self) -> str: ...
    def geometry(self) -> 'Geometry': ...
    def vertices(self) -> tuple[Vertex, ...]: ...
    def add(self, vertex_or_vertices: Vertex | Sequence[Vertex]) -> None: ...
    def remove(self, vertex_or_vertices: Vertex | Sequence[Vertex]) -> None: ...
    def clear(self) -> None: ...
    def contains(self, vertex: Vertex) -> bool: ...
    def destroy(self) -> None: ...

class AttribDataId:
    """Identifier for tracking attribute data changes."""
    def __init__(self) -> None: ...
    def isValid(self) -> bool: ...

class GeometryRayCache:
    """Accelerated ray intersection cache for geometry."""
    def __init__(self, geometry: 'Geometry', ray_flags: int = 0) -> None: ...
    def intersect(self, origin: Sequence[float], direction: Sequence[float], max_distance: float = -1) -> dict[str, Any]: ...

class IndexPairPropertyTable:
    """Property table mapping pairs of indices to values."""
    def __init__(self) -> None: ...
    def hasProperty(self, index1: int, index2: int, property_name: str) -> bool: ...
    def property(self, index1: int, index2: int, property_name: str) -> Any: ...
    def setProperty(self, index1: int, index2: int, property_name: str, value: Any) -> None: ...
    def removeProperty(self, index1: int, index2: int, property_name: str) -> None: ...

class AssetGalleryDataSource:
    """Provides an interface to any data source that can be used with an asset or snapshot gallery UI.

    Houdini's various asset catalog panels (the snapshot gallery attached to the LOP Scene Viewer,
    the Working Set in the Layout LOP's brush panel, and the Asset Catalog pane) are all populated
    by pulling data from this class.

    This object is created by providing a source identifier, and an optional additional string
    argument. The source identifier is used to find or create a shared underlying data source
    implementation object (which may be a C++ or python object).

    Houdini ships with three data source implementations:
    - SQL database (.db, .sqlite, .sqlite3 file extensions) - read and write
    - USD files (USD file extensions + primitive pattern argument) - read only
    - LOP stages (op:/path/to/lop + primitive pattern argument) - read only

    See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html
    """
    def __init__(self, source_identifier: str, args: str | None = None) -> None:
        """Constructs or finds a matching existing data source implementation object.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#__init__
        """
        ...

    def isValid(self) -> bool:
        """Return True if this data source has a valid implementation, otherwise return False.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#isValid
        """
        ...

    def isReadOnly(self) -> bool:
        """Return True if this data source only supports read operations, otherwise return False.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#isReadOnly
        """
        ...

    def sourceIdentifier(self) -> str:
        """Return the source identifier string used to create this data source object.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#sourceIdentifier
        """
        ...

    def sourceArgs(self) -> str:
        """Return the args string used to create this data source object.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#sourceArgs
        """
        ...

    def startTransaction(self) -> None:
        """For writable data sources, this method can be used to group multiple calls to edit the data source.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#startTransaction
        """
        ...

    def endTransaction(self, commit: bool = True) -> None:
        """This method is always called after a call to startTransaction.

        Indicates that the group of data source edits has been completed.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#endTransaction
        """
        ...

    def itemIds(self) -> tuple[str, ...]:
        """Return a unique identifier for each asset available in the data source.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#itemIds
        """
        ...

    def updatedItemIds(self) -> tuple[str, ...]:
        """Return a unique identifier for any asset that has changed since the last call to this method.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#updatedItemIds
        """
        ...

    def childItemIds(self, item_id: str) -> tuple[str, ...]:
        """Return a list of unique identifier for all assets that have this item set as its parent.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#childItemIds
        """
        ...

    def infoHtml(self) -> str:
        """Return a string in HTML format that will be displayed at the top of the asset catalog window.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#infoHtml
        """
        ...

    def sourceTypeName(self, item_id: str | None = None) -> str:
        """Return the data source type of the asset identified by the id.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#sourceTypeName
        """
        ...

    def typeName(self, item_id: str) -> str:
        """Return the type of asset identified by the id.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#typeName
        """
        ...

    def label(self, item_id: str) -> str:
        """Return the user-facing string that identifies and describes the item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#label
        """
        ...

    def thumbnail(self, item_id: str) -> bytes:
        """Return the raw data for a thumbnail image that represents the item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#thumbnail
        """
        ...

    def creationDate(self, item_id: str) -> int:
        """Return a long integer representing the unix timestamp at which the item was created.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#creationDate
        """
        ...

    def modificationDate(self, item_id: str) -> int:
        """Return a long integer representing the unix timestamp at which the item was last modified.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#modificationDate
        """
        ...

    def isStarred(self, item_id: str) -> bool:
        """Return True if this item has been marked as a favorite by the user.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#isStarred
        """
        ...

    def colorTag(self, item_id: str) -> str:
        """Return a string indicating a special color tag value that has been assigned by the user.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#colorTag
        """
        ...

    def tags(self, item_id: str) -> tuple[str, ...]:
        """Return a tuple of user defined tag strings that have been assigned to this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#tags
        """
        ...

    def metadata(self, item_id: str) -> dict[str, str | float]:
        """Return a dictionary of metadata that has been associated with this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#metadata
        """
        ...

    def filePath(self, item_id: str) -> str:
        """Return a string that can be used to access the raw data associated with this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#filePath
        """
        ...

    def ownsFile(self, item_id: str) -> bool:
        """Return True if the filePath for this item is a file on disk that should be deleted if the item is deleted.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#ownsFile
        """
        ...

    def blindData(self, item_id: str) -> bytes:
        """Return a block of data source implementation specific binary data associated with the item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#blindData
        """
        ...

    def status(self, item_id: str) -> str:
        """Return a string describing the current status of this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#status
        """
        ...

    def parentId(self, item_id: str) -> str:
        """Return the unique identifier for this item's parent item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#parentId
        """
        ...

    def prepareItemForUse(self, item_id: str) -> str:
        """Make sure that the item is ready to be used.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#prepareItemForUse
        """
        ...

    def setLabel(self, item_id: str, label: str) -> bool:
        """Set the value of the label for this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setLabel
        """
        ...

    def setThumbnail(self, item_id: str, thumbnail: bytes) -> bool:
        """Set the value of the thumbnail for this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setThumbnail
        """
        ...

    def setModificationDate(self, item_id: str, timestamp: int) -> bool:
        """Set the value of the modificationDate for this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setModificationDate
        """
        ...

    def setIsStarred(self, item_id: str, isstarred: bool) -> bool:
        """Set the value of the isStarred flag for this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setIsStarred
        """
        ...

    def setColorTag(self, item_id: str, color_tag: str) -> bool:
        """Set the value of the colorTag for this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setColorTag
        """
        ...

    def setMetadata(self, item_id: str, metadata: dict[str, str | float]) -> bool:
        """Set the value of the metadata dictionary for this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setMetadata
        """
        ...

    def setFilePath(self, item_id: str, file_path: str) -> bool:
        """Set the value of the filePath for this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setFilePath
        """
        ...

    def setOwnsFile(self, item_id: str, owns_file: bool) -> bool:
        """Set the value of the ownsFile flag for this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setOwnsFile
        """
        ...

    def setBlindData(self, item_id: str, data: bytes) -> bool:
        """Set the value of the blindData for this item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setBlindData
        """
        ...

    def setParentId(self, item_id: str, parent_item_id: str) -> bool:
        """Set the value of the parent of this item to be parent_item_id.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#setParentId
        """
        ...

    def createTag(self, tag: str) -> bool:
        """Create a tag in the data source, but do not assign it to any items.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#createTag
        """
        ...

    def deleteTag(self, tag: str, delete_if_assigned: bool) -> bool:
        """Delete a tag from the data source.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#deleteTag
        """
        ...

    def addTag(self, item_id: str, tag: str) -> bool:
        """Adds a tag to a specific item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#addTag
        """
        ...

    def removeTag(self, item_id: str, tag: str) -> bool:
        """Removes a tag from a specific item.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#removeTag
        """
        ...

    def generateItemFilePath(self, item_id: str, file_ext: str) -> str:
        """Return a unique file path with an extension provided in file_ext.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#generateItemFilePath
        """
        ...

    def addItem(
        self,
        label: str,
        file_path: str | None = None,
        thumbnail: bytes = b'',
        type_name: str = 'asset',
        blind_data: bytes = b'',
        creation_date: int = 0
    ) -> str:
        """Adds a new item to the data source.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#addItem
        """
        ...

    def markItemsForDeletion(self, item_ids: Sequence[str]) -> bool:
        """Marks one or more items to be deleted.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#markItemsForDeletion
        """
        ...

    def unmarkItemsForDeletion(self, item_ids: Sequence[str]) -> bool:
        """Remove the indicator in the data source that the supplied items should be deleted.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#unmarkItemsForDeletion
        """
        ...

    def saveAs(self, source_identifier: str) -> bool:
        """Create a copy of the data source, if supported.

        See https://www.sidefx.com/docs/houdini/hom/hou/AssetGalleryDataSource.html#saveAs
        """
        ...

class BoundingBox:
    """Houdini 3D bounding box."""
    def __init__(self, xmin: float = 0, ymin: float = 0, zmin: float = 0, xmax: float = 0, ymax: float = 0, zmax: float = 0) -> None: ...
    def min(self) -> 'Vector3': ...
    def max(self) -> 'Vector3': ...
    def center(self) -> 'Vector3': ...
    def size(self) -> 'Vector3': ...
    def isValid(self) -> bool: ...
    def contains(self, point: Sequence[float] | 'Vector3') -> bool: ...
    def intersects(self, bbox: 'BoundingBox') -> bool: ...
    def closestPoint(self, point: Sequence[float] | 'Vector3') -> 'Vector3': ...
    def expandBounds(self, dx: float, dy: float, dz: float) -> None: ...

class OrientedBoundingBox:
    """Houdini oriented 3D bounding box."""
    def __init__(self) -> None: ...
    def center(self) -> 'Vector3': ...
    def size(self) -> 'Vector3': ...
    def rotation(self) -> 'Matrix3': ...
    def orientation(self) -> 'Quaternion': ...

class Selection:
    """Houdini geometry selection object."""
    pass

class GeometryDelta:
    """Houdini geometry delta object for tracking changes.

    Geometry delta provides access to the geometry differences (deltas) stored by some
    Geometry nodes such as the Edit SOP.

    If you ask a SOP for its geometry delta via hou.SopNode.geometryDelta(), you'll get
    a reference to it. If the SOP recooks, the corresponding geometry delta objects will
    update to the SOP's new geometry delta object. If the SOP is deleted, accessing the
    geometry delta object will raise a hou.ObjectWasDeleted exception.
    """
    def setPointPositionsFromString(self, positions: str) -> None: ...

class OpVerb:
    """
    Base class for node operation verbs.
    Verbs represent compiled node operations that can be executed on data.
    """
    def loadParmsFromNode(self, node: 'OpNode') -> None: ...
    def loadParmsFromNodeAtTime(self, node: 'OpNode', time: float) -> None: ...
    def parms(self) -> dict[str, int | float | str]: ...
    def setParms(self, parmdictionary: dict[str, int | float | str]) -> None: ...
    def minNumInputs(self) -> int: ...

class SopVerb(OpVerb):
    """SOP verb for compiled geometry operations."""
    def __init__(self) -> None: ...
    def execute(self, destgeo: 'Geometry', inputgeolist: Sequence['Geometry']) -> None: ...
    def executeAtTime(self, destgeo: 'Geometry', inputgeolist: Sequence['Geometry'], time: float, add_time_dep: bool = True) -> None: ...

class CopVerb(OpVerb):
    """COP verb for compiled compositor operations."""
    def __init__(self) -> None: ...
    def execute(self, destimage: Any, inputimagelist: Sequence[Any]) -> None: ...  # TODO: Type image objects
    def executeAtTime(self, destimage: Any, inputimagelist: Sequence[Any], time: float, add_time_dep: bool = True) -> None: ...

class Matrix2:
    """2x2 matrix of floating point values."""
    def __init__(self, values: Sequence[float] | Sequence[Sequence[float]]) -> None: ...
    def at(self, row: int, col: int) -> float: ...
    def setAt(self, row: int, col: int, value: float) -> None: ...
    def asTuple(self) -> tuple[float, float, float, float]: ...
    def asTupleOfTuples(self) -> tuple[tuple[float, float], tuple[float, float]]: ...
    def setTo(self, sequence: Sequence[float] | Sequence[Sequence[float]]) -> None: ...
    def setToIdentity(self) -> None: ...
    def setToZero(self) -> None: ...
    def __add__(self, matrix2: 'Matrix2') -> 'Matrix2': ...
    def __sub__(self, matrix2: 'Matrix2') -> 'Matrix2': ...
    def __mul__(self, matrix2_or_scalar: 'Matrix2' | float) -> 'Matrix2': ...
    def preMult(self, matrix2: 'Matrix2') -> 'Matrix2': ...
    def determinant(self) -> float: ...
    def inverted(self) -> 'Matrix2': ...
    def transposed(self) -> 'Matrix2': ...
    def isAlmostEqual(self, matrix2: 'Matrix2', tolerance: float = 0.00001) -> bool: ...

class Vector2:
    """2D vector."""
    @overload
    def __init__(self, values: Sequence[float] = ...) -> None: ...
    @overload
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None: ...
    def __getitem__(self, index: int) -> float: ...
    def __setitem__(self, index: int, value: float) -> None: ...
    def setTo(self, sequence: Sequence[float]) -> None: ...
    def __len__(self) -> int: ...
    def __add__(self, vector2: 'Vector2') -> 'Vector2': ...
    def __sub__(self, vector2: 'Vector2') -> 'Vector2': ...
    def __neg__(self) -> 'Vector2': ...
    def __mul__(self, scalar_or_matrix2: float | 'Matrix2') -> 'Vector2': ...
    def __rmul__(self, scalar: float) -> 'Vector2': ...
    def __div__(self, scalar: float) -> 'Vector2': ...
    def length(self) -> float: ...
    def lengthSquared(self) -> float: ...
    def normalized(self) -> 'Vector2': ...
    def distanceTo(self, vector2: 'Vector2') -> float: ...
    def dot(self, vector2: 'Vector2') -> float: ...
    def almostEqual(self, vector2: 'Vector2', tolerance: float = 0.00001) -> bool: ...
    def isAlmostEqual(self, vector2: 'Vector2', tolerance: float = 0.00001) -> bool: ...
    def x(self) -> float: ...
    def y(self) -> float: ...

class Vector3:
    """3D vector."""
    @overload
    def __init__(self, values: Sequence[float] = ...) -> None: ...
    @overload
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None: ...
    def __getitem__(self, index: int) -> float: ...
    def __setitem__(self, index: int, value: float) -> None: ...
    def setTo(self, sequence: Sequence[float]) -> None: ...
    def __len__(self) -> int: ...
    def __add__(self, vector3: 'Vector3') -> 'Vector3': ...
    def __sub__(self, vector3: 'Vector3') -> 'Vector3': ...
    def __neg__(self) -> 'Vector3': ...
    def __mul__(self, scalar_or_matrix3_or_matrix4: float | 'Matrix3' | 'Matrix4') -> 'Vector3': ...
    def __rmul__(self, scalar: float) -> 'Vector3': ...
    def __div__(self, scalar: float) -> 'Vector3': ...
    def length(self) -> float: ...
    def lengthSquared(self) -> float: ...
    def normalized(self) -> 'Vector3': ...
    def multiplyAsDir(self, matrix4: 'Matrix4') -> 'Vector3': ...
    def distanceTo(self, vector3: 'Vector3') -> float: ...
    def dot(self, vector3: 'Vector3') -> float: ...
    def cross(self, vector3: 'Vector3') -> 'Vector3': ...
    def angleTo(self, vector3: 'Vector3') -> float: ...
    def matrixToRotateTo(self, vector3: 'Vector3') -> 'Matrix4': ...
    def almostEqual(self, vector3: 'Vector3', tolerance: float = 0.00001) -> bool: ...
    def isAlmostEqual(self, vector3: 'Vector3', tolerance: float = 0.00001) -> bool: ...
    def smoothRotation(self, reference: 'Vector3', rotate_order: str = 'xyz') -> 'Vector3': ...
    def ocio_transform(self, src_space: str, dest_space: str) -> 'Vector3': ...
    def x(self) -> float: ...
    def y(self) -> float: ...
    def z(self) -> float: ...
    def distanceToSegment(self, point1: 'Vector3', point2: 'Vector3') -> float: ...
    def distance2ToSegment(self, point1: 'Vector3', point2: 'Vector3') -> float: ...
    def pointOnSegment(self, point1: 'Vector3', point2: 'Vector3') -> 'Vector3': ...

class Vector4:
    """4D vector."""
    @overload
    def __init__(self, values: Sequence[float] = ...) -> None: ...
    @overload
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0) -> None: ...
    def __getitem__(self, index: int) -> float: ...
    def __setitem__(self, index: int, value: float) -> None: ...
    def setTo(self, sequence: Sequence[float]) -> None: ...
    def __len__(self) -> int: ...
    def __add__(self, vector4: 'Vector4') -> 'Vector4': ...
    def __sub__(self, vector4: 'Vector4') -> 'Vector4': ...
    def __mul__(self, scalar_or_matrix4: float | 'Matrix4') -> 'Vector4': ...
    def __rmul__(self, scalar: float) -> 'Vector4': ...
    def __div__(self, scalar: float) -> 'Vector4': ...
    def length(self) -> float: ...
    def lengthSquared(self) -> float: ...
    def normalized(self) -> 'Vector4': ...
    def dot(self, vector4: 'Vector4') -> float: ...
    def almostEqual(self, vector4: 'Vector4', tolerance: float = 0.00001) -> bool: ...
    def isAlmostEqual(self, vector4: 'Vector4', tolerance: float = 0.00001) -> bool: ...
    def ocio_transform(self, src_space: str, dest_space: str) -> 'Vector4': ...
    def x(self) -> float: ...
    def y(self) -> float: ...
    def z(self) -> float: ...
    def w(self) -> float: ...

class Matrix3:
    """3x3 matrix of floating point values."""
    def __init__(self, values: Sequence[float] | Sequence[Sequence[float]]) -> None: ...
    def at(self, row: int, col: int) -> float: ...
    def setAt(self, row: int, col: int, value: float) -> None: ...
    def asTuple(self) -> tuple[float, float, float, float, float, float, float, float, float]: ...
    def asTupleOfTuples(self) -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]: ...
    def setTo(self, sequence: Sequence[float] | Sequence[Sequence[float]]) -> None: ...
    def setToIdentity(self) -> None: ...
    def setToZero(self) -> None: ...
    def __add__(self, matrix3: 'Matrix3') -> 'Matrix3': ...
    def __sub__(self, matrix3: 'Matrix3') -> 'Matrix3': ...
    def __mul__(self, matrix3_or_scalar: 'Matrix3' | float) -> 'Matrix3': ...
    def preMult(self, matrix3: 'Matrix3') -> 'Matrix3': ...
    def determinant(self) -> float: ...
    def extractRotates(self, rotate_order: str = 'xyz') -> 'Vector3': ...
    def removeScalesAndShears(self, transform_order: str = 'srt') -> tuple['Vector3', 'Vector3']: ...
    def inverted(self) -> 'Matrix3': ...
    def transposed(self) -> 'Matrix3': ...
    def isAlmostEqual(self, matrix3: 'Matrix3', tolerance: float = 0.00001) -> bool: ...

class Matrix4:
    """4x4 transformation matrix."""
    def __init__(self, values: Sequence[float] | Sequence[Sequence[float]] | None = None) -> None: ...
    def at(self, row: int, col: int) -> float: ...
    def setAt(self, row: int, col: int, value: float) -> None: ...
    def asTuple(self) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]: ...
    def asTupleOfTuples(self) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float], tuple[float, float, float, float], tuple[float, float, float, float]]: ...
    def setTo(self, sequence: Sequence[float] | Sequence[Sequence[float]]) -> None: ...
    def setToIdentity(self) -> None: ...
    def setToZero(self) -> None: ...
    def __add__(self, matrix4: 'Matrix4') -> 'Matrix4': ...
    def __sub__(self, matrix4: 'Matrix4') -> 'Matrix4': ...
    def __mul__(self, matrix4_or_scalar: 'Matrix4' | float) -> 'Matrix4': ...
    def preMult(self, matrix4: 'Matrix4') -> 'Matrix4': ...
    def determinant(self) -> float: ...
    def explode(self, transform_order: str = 'srt', rotate_order: str = 'xyz', pivot: 'Vector3' = ..., pivot_rotate: 'Vector3' = ...) -> dict[str, 'Vector3']: ...
    def extractTranslates(self, transform_order: str = 'srt', pivot_rotate: 'Vector3' = ..., pivot: 'Vector3' = ...) -> 'Vector3': ...
    def extractRotates(self, transform_order: str = 'srt', rotate_order: str = 'xyz', pivot: 'Vector3' = ..., pivot_rotate: 'Vector3' = ...) -> 'Vector3': ...
    def extractScales(self, transform_order: str = 'srt', pivot: 'Vector3' = ..., pivot_rotate: 'Vector3' = ...) -> 'Vector3': ...
    def extractShears(self, transform_order: str = 'srt', pivot: 'Vector3' = ..., pivot_rotate: 'Vector3' = ...) -> 'Vector3': ...
    def extractRotationMatrix3(self) -> 'Matrix3': ...
    def inverted(self) -> 'Matrix4': ...
    def transposed(self) -> 'Matrix4': ...
    def isAlmostEqual(self, matrix4: 'Matrix4', tolerance: float = 0.00001) -> bool: ...
    def setToPerspective(self, zoom: float, image_aspect: float = 1, pixel_aspect: float = 1, clip_near: float = 0, clip_far: float = 1, window_xmin: float = 0, window_xmax: float = 1, window_ymin: float = 0, window_ymax: float = 1) -> None: ...
    def setToOrthographic(self, zoom: float, orthowidth: float = 1, image_aspect: float = 1, pixel_aspect: float = 1, clip_near: float = 0, clip_far: float = 1, window_xmin: float = 0, window_xmax: float = 1, window_ymin: float = 0, window_ymax: float = 1) -> None: ...

# Module-level functions - these are the PRIMARY module interface
# Note: These handle the static/instance confusion by being clearly module-level

def node(path: str) -> Node:
    """
    Get node by path. Returns None if path doesn't exist.
    This is the main way to access existing nodes.
    """
    ...

def root() -> Node:
    """Get root node. Always succeeds."""
    ...

def pwd() -> Node:
    """Get current working directory node. Always succeeds."""
    ...

def cd(path: str) -> None:
    """
    Change current directory. Can raise OperationFailed if path invalid.
    Affects behavior of relative paths in other hou functions.
    """
    ...

def selectedNodes() -> tuple[Node, ...]:
    """Get currently selected nodes. Empty tuple if none selected."""
    ...

def clearAllSelected() -> None:
    """Clear all node selections. Always succeeds."""
    ...

# Enhanced node finding with better error handling
def findNode(path: str) -> Node:
    """Find node by path, returns None if not found (alias for node())."""
    ...

def nodeAtPath(path: str, create_missing_dirs: bool = False) -> Node:
    """
    Get node at path, optionally creating parent directories.
    More robust than basic node() function.
    """
    ...

# Node type functions
def nodeTypeCategories() -> dict[str, NodeTypeCategory]:
    """Get all node type categories."""
    ...

def nodeType(category: str | NodeTypeCategory, name: str) -> NodeType|None:
    """Get a specific node type."""
    ...

def hdaDefinition(node_type_category: str | NodeTypeCategory, node_type_name: str, hda_file_path: str | None = None) -> HDADefinition | None:
    """
    Get the HDA definition for a node type.

    Args:
        node_type_category: Node type category (e.g., 'Sop', 'Object') or category object
        node_type_name: Name of the node type
        hda_file_path: Optional path to specific HDA file; if None, returns preferred definition

    Returns:
        HDADefinition object or None if not found
    """
    ...

def lopNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini lighting (LOP) nodes."""
    ...

def apexNodeTypeCategory() -> ApexNodeTypeCategory:
    """Return the NodeTypeCategory instance for APEX nodes."""
    ...

def chopNetNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini channel container (chopnet) nodes."""
    ...

def chopNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini channel (CHOP) nodes."""
    ...

def cop2NetNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini composite container (cop2net) nodes."""
    ...

def cop2NodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini composite (cop2) nodes."""
    ...

def copNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini composite (COP) nodes."""
    ...

def dataNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini data nodes."""
    ...

def dopNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini dynamic (DOP) nodes."""
    ...

def managerNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini manager nodes."""
    ...

def objNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini object nodes."""
    ...

def rootNodeTypeCategory() -> NodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini root (/) node."""
    ...

def ropNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini output (ROP) nodes."""
    ...

def shopNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini shader (SHOP) nodes."""
    ...

def sopNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini geometry (SOP) nodes."""
    ...

def topNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini task (TOP) nodes."""
    ...

def vopNetNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini VEX builder container (vopnet) nodes."""
    ...

def vopNodeTypeCategory() -> OpNodeTypeCategory:
    """Return the NodeTypeCategory instance for Houdini VEX builder (VOP) nodes."""
    ...

# Animation and channel interpolation functions
def bezier() -> float:
    """Bezier interpolation function."""
    ...

def constant() -> float:
    """Constant (hold) interpolation function."""
    ...

def cubic() -> float:
    """Cubic interpolation function."""
    ...

def cycle() -> float:
    """Cycle extrapolation function."""
    ...

def cycleoffset() -> float:
    """Cycle with offset extrapolation function."""
    ...

def cycleoffsett() -> float:
    """Cycle with offset in time extrapolation function."""
    ...

def cyclet() -> float:
    """Cycle in time extrapolation function."""
    ...

def ease() -> float:
    """Ease in/out interpolation function."""
    ...

def easein() -> float:
    """Ease in interpolation function."""
    ...

def easeinp() -> float:
    """Ease in with parameter interpolation function."""
    ...

def easeout() -> float:
    """Ease out interpolation function."""
    ...

def easeoutp() -> float:
    """Ease out with parameter interpolation function."""
    ...

def easep() -> float:
    """Ease with parameter interpolation function."""
    ...

def linear() -> float:
    """Linear interpolation function."""
    ...

def match() -> float:
    """Match slope interpolation function."""
    ...

def matchin() -> float:
    """Match incoming slope interpolation function."""
    ...

def matchout() -> float:
    """Match outgoing slope interpolation function."""
    ...

def qlinear() -> float:
    """Quaternion linear interpolation function."""
    ...

def quintic() -> float:
    """Quintic interpolation function."""
    ...

def repeat() -> float:
    """Repeat extrapolation function."""
    ...

def repeatt() -> float:
    """Repeat in time extrapolation function."""
    ...

def spline() -> float:
    """Spline interpolation function."""
    ...

def vmatch() -> float:
    """Vector match slope interpolation function."""
    ...

def vmatchin() -> float:
    """Vector match incoming slope interpolation function."""
    ...

def vmatchout() -> float:
    """Vector match outgoing slope interpolation function."""
    ...

# Playbar and time functions
def fps() -> float:
    """Get frames per second."""
    ...

def setFps(fps: float) -> None:
    """Set frames per second."""
    ...

def frame() -> float:
    """Get current frame."""
    ...

def setFrame(frame: float) -> None:
    """Set current frame."""
    ...

def intFrame() -> int:
    """Get current frame as integer."""
    ...

def time() -> float:
    """Get current time in seconds."""
    ...

def setTime(time: float) -> None:
    """Set current time in seconds."""
    ...

def frameToTime(frame: float) -> float:
    """Convert frame number to time in seconds."""
    ...

def timeToFrame(time: float) -> float:
    """Convert time in seconds to frame number."""
    ...

# Session info
def applicationName() -> str:
    """Get application name."""
    ...

def applicationVersion() -> tuple[int, int, int]:
    """Get application version as tuple."""
    ...

def applicationVersionString() -> str:
    """Get application version as string."""
    ...

def isUIAvailable() -> bool:
    """Check if UI is available."""
    ...

class Quaternion:
    """Houdini quaternion for rotation representation."""
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, w: float = 1) -> None: ...
    def extractRotationMatrix3(self) -> 'Matrix3': ...
    def extractRotationMatrix4(self) -> 'Matrix4': ...

# Note: Submodule stubs are in stubs/hou/*.pyi files
# hipFile is a module with functions for working with .hip files
# This allows cleaner separation and easier maintenance
# Accessible as: hou.anim, hou.audio, hou.clone, etc.

# ============================================================================
# EXCEPTION CLASSES
# ============================================================================

class Error(Exception):
    """Base class for all exceptions in the hou module.

    All Houdini-specific exceptions inherit from this class. Catch this
    exception to handle any Houdini-related error.

    See: https://www.sidefx.com/docs/houdini/hom/hou/Error.html
    """
    pass

class GeometryPermissionError(Error):
    """Raised if you try to modify SOP geometry from outside of a Python SOP.

    SOP geometry can only be modified within the context of a Python SOP node
    or similar geometry manipulation context. Attempting to modify geometry
    from outside these contexts will raise this error.

    See: https://www.sidefx.com/docs/houdini/hom/hou/GeometryPermissionError.html
    """
    pass

class HandleNotRegistered(Error):
    """Raised if you try to use a custom handle that is not registered with the system.

    Custom Python viewer handles must be registered before use. This error
    indicates an attempt to use an unregistered handle.

    See: https://www.sidefx.com/docs/houdini/hom/hou/HandleNotRegistered.html
    """
    pass

class InitScriptFailed(Error):
    """Raised when an initialization script fails to execute.

    See: https://www.sidefx.com/docs/houdini/hom/hou/InitScriptFailed.html
    """
    pass

class InvalidGeometry(Error):
    """Exception raised when you try to access a reference to SOP Geometry that has since failed to cook.

    When a SOP node fails to cook, any Geometry objects referencing its
    output become invalid. Attempting to use such objects raises this error.

    See: https://www.sidefx.com/docs/houdini/hom/hou/InvalidGeometry.html
    """
    pass

class InvalidInput(Error):
    """Raised if you try to set a node's input to something invalid.

    This error occurs when attempting to create invalid node connections,
    such as connecting incompatible node types or creating circular dependencies.

    See: https://www.sidefx.com/docs/houdini/hom/hou/InvalidInput.html
    """
    pass

class InvalidNodeType(Error):
    """Raised if you try to call a method on a Node that doesn't support it.

    Different node types have different methods available. This error indicates
    an attempt to call a method not applicable to the specific node type.

    See: https://www.sidefx.com/docs/houdini/hom/hou/InvalidNodeType.html
    """
    pass

class InvalidOutput(Error):
    """Raised if you try to set a node's output to something invalid.

    See: https://www.sidefx.com/docs/houdini/hom/hou/InvalidOutput.html
    """
    pass

class InvalidSize(Error):
    """Raised when you pass a sequence of the wrong length to a function.

    Many Houdini functions expect sequences of specific lengths (e.g., 3-tuples
    for vectors). This error indicates a length mismatch.

    See: https://www.sidefx.com/docs/houdini/hom/hou/InvalidSize.html
    """
    pass

class KeyframeValueNotSet(Error):
    """Raised when attempting to access a keyframe value that hasn't been set.

    See: https://www.sidefx.com/docs/houdini/hom/hou/KeyframeValueNotSet.html
    """
    pass

class LicenseError(Error):
    """Raised when a licensing error occurs.

    This error occurs when trying to access a feature or component without
    the appropriate license, or when license validation fails.

    See: https://www.sidefx.com/docs/houdini/hom/hou/LicenseError.html
    """
    pass

class LoadWarning(Warning):
    """Exception class for when loading a hip file in Houdini generates warnings.

    This is a warning rather than an error, indicating non-fatal issues
    encountered during file loading. The file loads successfully despite
    the warnings.

    See: https://www.sidefx.com/docs/houdini/hom/hou/LoadWarning.html
    """
    pass

class MatchDefinitionError(Error):
    """Raised when there's a match definition error.

    See: https://www.sidefx.com/docs/houdini/hom/hou/MatchDefinitionError.html
    """
    pass

class NameConflict(Error):
    """Exception raised when a name conflict is detected during an operation.

    This error occurs when attempting to create or rename something with
    a name that already exists in the same namespace.

    See: https://www.sidefx.com/docs/houdini/hom/hou/NameConflict.html
    """
    pass

class NodeError(Error):
    """Raise this exception in a Python node to signal that the node is in error.

    When writing Python SOPs, DOPs, or other Python nodes, raise this exception
    to put the node into an error state with a custom error message.

    See: https://www.sidefx.com/docs/houdini/hom/hou/NodeError.html
    """
    pass

class NodeWarning(Warning):
    """Raise this exception in a Python node to signal that the node has a warning.

    When writing Python SOPs, DOPs, or other Python nodes, raise this exception
    to display a warning message without putting the node into an error state.

    See: https://www.sidefx.com/docs/houdini/hom/hou/NodeWarning.html
    """
    pass

class NotAvailable(Error):
    """Raised when you try to call an API function/method that is not available.

    Some API features may not be available depending on the Houdini license,
    platform, or runtime context. This error indicates unavailable functionality.

    See: https://www.sidefx.com/docs/houdini/hom/hou/NotAvailable.html
    """
    pass

class ObjectWasDeleted(Error):
    """Raised when you try to access a reference to an object that has since been deleted.

    When you hold a reference to a Houdini object (node, parameter, etc.) and
    that object is deleted, subsequent attempts to use the reference raise
    this error.

    See: https://www.sidefx.com/docs/houdini/hom/hou/ObjectWasDeleted.html
    """
    pass

class OperationFailed(Error):
    """Generic catch-all exception for various errors in Houdini that don't have their own dedicated exception classes.

    This is used for operations that fail for various reasons when a more
    specific exception type doesn't apply.

    See: https://www.sidefx.com/docs/houdini/hom/hou/OperationFailed.html
    """
    pass

class OperationInterrupted(Error):
    """Raised when an operation is interrupted by the user.

    Long-running operations that can be interrupted (via Escape key or other
    means) raise this exception when interrupted.

    See: https://www.sidefx.com/docs/houdini/hom/hou/OperationInterrupted.html
    """
    pass

class PermissionError(Error):
    """Raised when a permission error occurs.

    This can occur when attempting file operations without proper permissions
    or accessing restricted functionality.

    See: https://www.sidefx.com/docs/houdini/hom/hou/PermissionError.html
    """
    pass

class StateNotRegistered(Error):
    """Raised if you try to unregister a Python state that was never registered.

    Custom Python viewer states must be registered before they can be used
    or unregistered. This error indicates an invalid unregistration attempt.

    See: https://www.sidefx.com/docs/houdini/hom/hou/StateNotRegistered.html
    """
    pass

class SystemExit(Error):
    """Raised when Houdini is exiting.

    See: https://www.sidefx.com/docs/houdini/hom/hou/SystemExit.html
    """
    pass

class TypeConflict(Error):
    """Raised if a type conflict occurs during an operation.

    Type conflicts may occur during the registration of a python state or
    python handle, or when attempting operations with incompatible types.

    See: https://www.sidefx.com/docs/houdini/hom/hou/TypeConflict.html
    """
    pass

# ============================================================================
# ADDITIONAL SPECIALIZED CLASSES
# ============================================================================

# Additional specialized classes for different node types
class Track:
    """CHOP track containing a sequence of floating-point samples over time.

    Represents a single channel in a ChopNode with unique name, time-based sample data,
    and methods to evaluate values at specific times/frames. Used for motion capture,
    audio analysis, parameter animation, and time-series data manipulation.
    """
    def __init__(self) -> None: ...

    # Identity and container
    def name(self) -> str: ...
    def clip(self) -> 'Clip': ...
    def chopNode(self) -> ChopNode | None: ...

    # Sample data access
    def numSamples(self) -> int: ...
    def allSamples(self) -> tuple[float, ...]: ...

    # Evaluation at specific positions
    def eval(self) -> float: ...
    def evalAtTime(self, time: float) -> float: ...
    def evalAtFrame(self, frame: float) -> float: ...
    def evalAtSample(self, sample: float) -> float: ...
    def evalAtSampleIndex(self, index: int) -> float: ...  # Deprecated: Use evalAtSample()

    # Range evaluation
    def evalAtTimeRange(self, start: float, end: float) -> tuple[float, ...]: ...
    def evalAtFrameRange(self, start: float, end: float) -> tuple[float, ...]: ...
    def evalAtSampleRange(self, start: int, end: int) -> tuple[float, ...]: ...

    # Extend modes
    def extendLeft(self) -> 'trackExtend': ...
    def extendRight(self) -> 'trackExtend': ...

    # Parameter override
    def isOverrideActive(self) -> bool: ...
    def overrideParm(self) -> Parm | None: ...

    # Display properties
    def color(self) -> Color: ...

    # Legacy aliases
    def samples(self) -> tuple[float, ...]: ...
    def values(self) -> tuple[float, ...]: ...

class Clip:
    """Animation clip containing CHOP track data.

    Represents a container of tracks with sample data, typically from CHOP nodes.
    Used for motion capture, animation playback, and channel data management.
    """
    def __init__(self) -> None: ...

    # Container properties
    def chopNode(self) -> ChopNode: ...
    def chopNodeOutputIndex(self) -> int: ...
    def mode(self) -> 'clipMode': ...

    # Sample range and rate
    def sampleRange(self) -> tuple[float, float]: ...
    def numSamples(self) -> int: ...
    def sampleRate(self) -> float: ...

    # Unit conversion
    def frameToSamples(self, frame: float) -> float: ...
    def samplesToFrame(self, samples: float) -> float: ...
    def samplesToTime(self, samples: float) -> float: ...
    def timeToSamples(self, time: float) -> float: ...

    # Track access
    def tracks(self) -> tuple[Track, ...]: ...
    def track(self, track_name: str) -> Track | None: ...

    # File I/O
    def saveToFile(self, file_name: str) -> None: ...
    def loadFromFile(self, file_name: str) -> None: ...

class DopData:
    """Base class for DOP data stored in simulation."""
    # Subdata management
    def subData(self) -> dict[str, 'DopData']: ...
    def findSubData(self, data_spec: str) -> 'DopData|None': ...
    def findAllSubData(self, data_spec: str, recurse: bool=False) -> dict[str, 'DopData']: ...

    # Freezing
    def freeze(self) -> 'DopData': ...
    def isFrozen(self) -> bool: ...

    # Path/identification
    def path(self) -> str: ...
    def selectionPath(self) -> str: ...
    def dataType(self) -> str: ...
    def id(self) -> str: ...

    # Records
    def recordTypes(self) -> tuple[str, ...]: ...
    def record(self, record_type: str, record_index: int=0) -> 'DopRecord': ...
    def records(self, record_type: str) -> tuple['DopRecord', ...]: ...
    def options(self) -> 'DopRecord': ...

    # Context
    def dopNetNode(self) -> OpNode: ...
    def simulation(self) -> 'DopSimulation': ...
    def creator(self) -> DopNode: ...

    # Subdata creation/modification
    def createSubData(self, data_name: str, data_type: str="SIM_EmptyData", avoid_name_collisions: bool=False) -> 'DopData': ...
    def attachSubData(self, data: 'DopData', new_data_name: str, avoid_name_collisions: bool=False) -> None: ...
    def removeSubData(self, data_spec: str) -> None: ...
    def copyContentsFrom(self, data: 'DopData') -> None: ...

    # Geometry access
    def fieldGeometry(self, name: str) -> Geometry|None: ...
    def geometry(self, name: str="Geometry") -> Geometry|None: ...
    def editableGeometry(self, name: str="Geometry") -> Any: ...  # Returns EditableDopGeometryGuard

class DopRecord:
    """Table of values stored inside DopData."""
    # Field access
    def field(self, field_name: str) -> int|bool|float|str|Vector2|Vector3|Vector4|Any|Matrix3|Matrix4|None: ...  # Any includes Quaternion
    def fieldNames(self) -> tuple[str, ...]: ...
    def fieldType(self, field_name: str) -> 'fieldType': ...

    # Record identification
    def recordIndex(self) -> int: ...
    def recordType(self) -> str: ...

    # Field modification
    def setField(self, field_name: str, value: Any) -> None: ...
    def setFieldBool(self, field_name: str, value: bool) -> None: ...

class DopRelationship(DopData):
    """DOP data storing relationships between objects."""
    # Relationship identification
    def name(self) -> str: ...
    def matches(self, pattern: str) -> bool: ...

    # Relationship type
    def relationshipTypeData(self) -> DopData|None: ...

    # Group management
    def setGroup(self, objects: tuple[DopObject, ...]) -> None: ...
    def setAffectorGroup(self, objects: tuple[DopObject, ...]) -> None: ...

class DopSimulation:
    """DOP simulation object."""
    def __init__(self) -> None: ...

    # Data access
    def findData(self, data_spec: str) -> 'DopData|None': ...
    def findAllData(self, data_spec: str) -> tuple['DopData', ...]: ...

    # Object management
    def objects(self) -> tuple['DopObject', ...]: ...
    def findObject(self, obj_spec: str) -> 'DopObject|None': ...
    def findAllObjects(self, obj_spec: str) -> tuple['DopObject', ...]: ...

    # Relationship management
    def relationships(self) -> tuple['DopRelationship', ...]: ...
    def findRelationship(self, rel_spec: str) -> 'DopRelationship': ...
    def findAllRelationships(self, rel_spec: str) -> tuple['DopRelationship', ...]: ...

    # DOP network
    def dopNetNode(self) -> OpNode: ...

    # Time management
    def time(self) -> float: ...
    def setTime(self, t: float, resim_last_timestep: bool=False, force_reset_sim: bool=False, allow_simulation: bool=True) -> None: ...
    def timestep(self) -> float: ...
    def setTimestep(self, t: float) -> None: ...

    # Memory
    def memoryUsage(self) -> int: ...

    # Object creation/removal
    def createObject(self, name: str, solve_on_creation_frame: bool) -> 'DopObject': ...
    def removeObject(self, object: 'DopObject') -> None: ...

    # Relationship creation/removal
    def createRelationship(self, name: str) -> 'DopRelationship': ...
    def removeRelationship(self, rel: 'DopRelationship') -> None: ...

class DopObject(DopData):
    """DOP simulation object."""
    # Object identification
    def name(self) -> str: ...
    def matches(self, pattern: str) -> bool: ...
    def objid(self) -> int: ...

    # Transform
    def transform(self, include_geometry_transform: bool=True) -> Matrix4: ...

class Image:
    """COP image object."""
    def __init__(self) -> None: ...
    def resolution(self) -> tuple[int, int]: ...
    def pixels(self) -> Any: ...  # NumPy array if available

class WorkItem:
    """TOP/PDG work item."""
    def __init__(self) -> None: ...
    def name(self) -> str: ...
    def state(self) -> str: ...  # "ready", "cooking", "cooked", "failed"

# Context managers for safer Houdini operations
class ScriptEvalContext:
    """Context manager for temporarily changing the scripting evaluation context.

    Use this to set a specific node or parameter as the evaluation context within
    a Python code block. This affects functions like hou.pwd(), hou.ch(), etc.
    """
    def __init__(self, node_or_parm: 'OpNode | Parm') -> None: ...
    def __enter__(self) -> 'ScriptEvalContext': ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
    def node(self) -> 'OpNode': ...
    def parm(self) -> 'Parm': ...

class ShellIO:
    """Proxy object that replaces Python's stdin, stdout, and stderr streams within Houdini.

    This class is mostly an implementation detail of how Houdini replaces Python's
    standard streams with versions that allow Python input and output in Houdini
    windows and pane tabs.

    The methods that might be useful outside of internal SideFX scripts are
    addCloseCallback(), removeCloseCallback(), and closeCallbacks(). These let you
    register functions that Houdini calls when the Python shell window or pane tab
    is closed (the equivalent of atexit() scripts in regular Python).

    See https://www.sidefx.com/docs/houdini/hom/hou/ShellIO.html
    """
    def addCloseCallback(self, callback: Callable[[], None]) -> None:
        """Register a Python callback to be called whenever the last Houdini Python Shell is closed.

        Args:
            callback: Function to call when shell closes.

        See https://www.sidefx.com/docs/houdini/hom/hou/ShellIO.html#addCloseCallback
        """
        ...

    def closeCallbacks(self) -> tuple[Callable[[], None], ...]:
        """Return a tuple of all Python callbacks registered with addCloseCallback.

        Returns:
            Tuple of registered callback functions.

        See https://www.sidefx.com/docs/houdini/hom/hou/ShellIO.html#closeCallbacks
        """
        ...

    def isatty(self) -> bool:
        """Implemented as part of the file-like object interface.

        Returns:
            Whether this is a TTY device.

        See https://www.sidefx.com/docs/houdini/hom/hou/ShellIO.html#isatty
        """
        ...

    def readline(self, size: int = -1) -> str:
        """Implemented as part of the file-like object interface.

        Args:
            size: Maximum number of bytes to read. -1 reads entire line.

        Returns:
            String read from input.

        See https://www.sidefx.com/docs/houdini/hom/hou/ShellIO.html#readline
        """
        ...

    def removeCloseCallback(self, callback: Callable[[], None]) -> None:
        """Remove a Python callback previously registered with addCloseCallback.

        Args:
            callback: Function to remove from callback list.

        See https://www.sidefx.com/docs/houdini/hom/hou/ShellIO.html#removeCloseCallback
        """
        ...

    def write(self, data: str) -> None:
        """Implemented as part of the file-like object interface.

        Args:
            data: String data to write.

        See https://www.sidefx.com/docs/houdini/hom/hou/ShellIO.html#write
        """
        ...

class LogEntry:
    """Represents a single log message sent by a source to a sink."""
    def __init__(
        self,
        message: str | None = None,
        source: str | None = None,
        source_context: str | None = None,
        severity: severityType | None = None,
        verbosity: int = 0,
        time: float = 0.0,
        thread_id: int = 0,
        has_external_info: bool = False,
        external_host_name: str | None = None,
        external_identifier: str | None = None,
        external_command_line: str | None = None,
        external_process_id: int = 0
    ) -> None: ...
    def source(self) -> str: ...
    def sourceContext(self) -> str: ...
    def message(self) -> str: ...
    def severity(self) -> severityType: ...
    def verbosity(self) -> int: ...
    def time(self) -> float: ...
    def threadId(self) -> int: ...
    def hasExternalInfo(self) -> bool: ...
    def externalHostName(self) -> str: ...
    def externalIdentifier(self) -> str: ...
    def externalCommandLine(self) -> str: ...
    def externalProcessId(self) -> int: ...

class PaneTab:
    """Base class for pane tabs in the Houdini UI."""
    def name(self) -> str: ...
    def setName(self, name: str) -> None: ...
    def type(self) -> paneTabType: ...
    def setType(self, type: paneTabType) -> 'PaneTab': ...
    def close(self) -> None: ...
    def isCurrentTab(self) -> bool: ...
    def setIsCurrentTab(self) -> None: ...
    def isFloating(self) -> bool: ...
    def clone(self) -> 'PaneTab': ...
    def linkGroup(self) -> paneLinkType: ...
    def setLinkGroup(self, group: paneLinkType) -> None: ...
    def isPin(self) -> bool: ...
    def setPin(self, pin: bool) -> None: ...
    def size(self) -> tuple[int, int]: ...
    def contentSize(self) -> tuple[int, int]: ...

class NetworkEditor(PaneTab):
    """Represents a Network Editor pane tab.

    Inherits from PaneTab and PathBasedPaneTab. Provides comprehensive control
    over network view, selection, display, and interaction within the network editor.
    """

    # Bounds and Transformations
    def cursorPosition(self, confine_to_view: bool = True) -> Vector2: ...
    def isShowingConnectors(self) -> bool: ...
    def isUnderCursor(self) -> bool: ...
    def isPosInside(self, pos: Vector2, ignore_floating_windows: bool = True) -> bool: ...
    def setCursorPosition(self, pos: Vector2) -> None: ...
    def screenBounds(self) -> BoundingRect: ...
    def visibleBounds(self) -> BoundingRect: ...
    def setVisibleBounds(
        self, bounds: BoundingRect, transition_time: float = 0.0,
        max_scale: float = 0.0, set_center_when_scale_rejected: bool = False
    ) -> None: ...
    def requestZoomReset(self) -> None: ...
    def isZoomResetRequested(self) -> bool: ...
    def setLocatingEnabled(self, enabled: bool) -> None: ...
    def locatingEnabled(self) -> bool: ...
    def lengthToScreen(self, len: float) -> float: ...
    def lengthFromScreen(self, len: float) -> float: ...
    def sizeToScreen(self, size: Vector2) -> Vector2: ...
    def sizeFromScreen(self, size: Vector2) -> Vector2: ...
    def posToScreen(self, pos: Vector2) -> Vector2: ...
    def posFromScreen(self, pos: Vector2) -> Vector2: ...
    def overviewPosToScreen(self, pos: Vector2) -> Vector2: ...
    def overviewPosFromScreen(self, pos: Vector2) -> Vector2: ...
    def overviewVisible(self) -> bool: ...
    def overviewVisibleIfAutomatic(self) -> bool: ...

    # Selection and Highlighting
    def networkItemsInBox(
        self, pos1: Vector2, pos2: Vector2, for_drop: bool = False, for_select: bool = False
    ) -> tuple[tuple[NetworkItem, str, int], ...]: ...
    def setDragSourceData(self, items: Sequence[NetworkItem]) -> None: ...
    def setDragSourceWorkItem(self, work_item_id: int) -> None: ...
    def setDropTargetItem(self, item: NetworkItem | None, name: str, index: int) -> None: ...
    def dropTargetItem(self) -> tuple[NetworkItem | None, str, int]: ...
    def setDecoratedItem(self, item: NetworkItem | None, interactive: bool) -> None: ...
    def decoratedItem(self) -> NetworkItem | None: ...
    def decorationInteractive(self) -> bool: ...
    def setPreSelectedItems(self, items: Sequence[NetworkItem]) -> None: ...
    def preSelectedItems(self) -> tuple[NetworkItem, ...]: ...
    def selectedConnections(self) -> tuple[NodeConnection, ...]: ...
    def clearAllSelected(self) -> None: ...
    def setNetworkBoxPendingRemovals(self, items: Sequence[NetworkMovableItem]) -> None: ...
    def networkBoxPendingRemovals(self) -> tuple[NetworkMovableItem, ...]: ...

    # Decoration
    def nodeShapes(self) -> tuple[str, ...]: ...
    def reloadNodeShapes(self) -> tuple[str, ...]: ...
    def setFootprints(self, footprints: Sequence[Any]) -> None: ...  # NetworkFootprint
    def footprints(self) -> tuple[Any, ...]: ...  # NetworkFootprint
    def setCursorMap(self, cursors: dict[tuple[str, int], str]) -> None: ...
    def cursorMap(self) -> dict[tuple[str, int], str]: ...
    def setDefaultCursor(self, cursor_name: str) -> None: ...
    def defaultCursor(self) -> str: ...
    def setBackgroundImages(self, images: Sequence[Any]) -> None: ...  # NetworkImage
    def backgroundImages(self) -> tuple[Any, ...]: ...  # NetworkImage
    def setAdjustments(
        self, items: Sequence[NetworkMovableItem], adjustments: Any, auto_remove: bool = False
    ) -> None: ...
    def setShapes(self, shapes: Sequence[Any]) -> None: ...  # NetworkShape
    def setOverlayShapes(self, shapes: Sequence[Any]) -> None: ...  # NetworkShape
    def redraw(self) -> None: ...

    # Network Item Information
    def itemRect(self, item: NetworkMovableItem, adjusted: bool = True) -> BoundingRect: ...
    def itemInputPos(self, item: Node | Any, input_index: int, adjusted: bool = True) -> Vector2: ...  # NetworkDot
    def itemInputDir(self, item: Node | Any, input_index: int) -> Vector2: ...  # NetworkDot
    def itemOutputPos(self, item: Node | Any, output_index: int, adjusted: bool = True) -> Vector2: ...  # NetworkDot or SubnetIndirectInput
    def itemOutputDir(self, item: Node | Any, output_index: int) -> Vector2: ...  # NetworkDot or SubnetIndirectInput
    def allVisibleRects(self, ignore_items: Sequence[NetworkMovableItem]) -> tuple[tuple[NetworkMovableItem, BoundingRect], ...]: ...

    # Prompts
    def setTooltip(self, tooltip: str) -> None: ...
    def tooltip(self) -> str: ...
    def setPrompt(self, prompt: str) -> None: ...
    def prompt(self) -> str: ...
    def flashMessage(self, image: str, message: str, duration: float) -> None: ...

    # Standard Menus and Editors
    def openTabMenu(
        self, key: str | None = None, auto_place: bool = False, branch: bool = False,
        src_item: Node | None = None, src_connector_index: int = -1,
        dest_item: Node | None = None, dest_connector_index: int = -1,
        node_position: Vector2 | None = None,
        src_items: Sequence[Node] = [], src_indexes: Sequence[int] = [],
        dest_items: Sequence[Node] = [], dest_indexes: Sequence[int] = []
    ) -> None: ...
    def openNodeMenu(self, node: Node | None = None, items: Sequence[Node] = []) -> None: ...
    def openVopEffectsMenu(self, node: Any, input_index: int) -> None: ...  # VopNode
    def openVopOutputInfoMenu(self, node: Any, output_index: int) -> None: ...  # VopNode
    def openCommentEditor(self, item: Any, select_all: bool = False) -> int: ...  # NetworkBox
    def openFloatingParameterEditor(self, node: Node) -> None: ...
    def openNameEditor(self, item: Node, select_all: bool = False) -> int: ...
    def openNoteEditor(self, stickynote: Any, select_all: bool = False) -> int: ...  # StickyNote
    def closeTextEditor(self, id: int, apply_changes: bool = True) -> None: ...
    def runShelfTool(self, tool_name: str) -> None: ...

    # Event Handling
    def scheduleTimerEvent(self, seconds: float) -> int: ...
    def handleCurrentKeyboardEvent(self, resend: bool = False) -> None: ...
    def setVolatileHotkeys(self, hotkey_symbols: Sequence[str]) -> None: ...
    def isVolatileHotkeyDown(self, hotkey_symbol: str) -> bool: ...
    def hotkeyAssignments(self, hotkey_symbols: Sequence[str]) -> tuple[tuple[str, ...], ...]: ...
    def pushEventContext(self, module: str, data: dict[str, Any]) -> bool: ...
    def popEventContext(self) -> None: ...
    def eventContextData(self) -> dict[str, Any]: ...

    # Preferences
    def setPref(self, pref: str, value: str) -> None: ...
    def getPref(self, pref: str) -> str: ...
    def setPrefs(self, prefs: dict[str, str]) -> None: ...
    def getPrefs(self) -> dict[str, str]: ...
    def registerPref(self, pref: str, value: str, global_pref: bool) -> None: ...
    def badges(self) -> tuple[tuple[str, ...], ...]: ...
    def textBadges(self) -> tuple[tuple[str, ...], ...]: ...

    # Parameter Editor
    def parmFilterEnabled(self) -> bool: ...
    def setParmFilterEnabled(self, on: bool, keyboard_lock: bool) -> None: ...
    def parmFilterMode(self) -> parmFilterMode: ...
    def setParmFilterMode(self, mode: parmFilterMode) -> None: ...
    def parmFilterCriteria(self) -> parmFilterCriteria: ...
    def setParmFilterCriteria(self, criteria: parmFilterCriteria) -> None: ...
    def parmFilterPattern(self) -> str: ...
    def setParmFilterPattern(self, pattern: str) -> None: ...
    def parmFilterExactMatch(self) -> bool: ...
    def setParmFilterExactMatch(self, on: bool) -> None: ...
    def parmScrollPosition(self) -> Vector2: ...
    def setParmScrollPosition(self, pos: Vector2) -> None: ...
    def parmScrollTo(self, parms: Sequence[Parm], scroll_pos: scrollPosition) -> None: ...
    def parmMoveFocusTo(self, parm: Parm) -> None: ...
    def setMultiParmTab(self, parm: Parm, tab_index: int) -> None: ...
    def multiParmTab(self, parm: Parm) -> int: ...

    # Methods from PaneTab (inherited)
    def name(self) -> str: ...
    def setName(self, name: str) -> None: ...
    def type(self) -> paneTabType: ...
    def setType(self, type: paneTabType) -> 'PaneTab': ...
    def close(self) -> None: ...
    def pane(self) -> Any | None: ...  # Pane
    def floatingPanel(self) -> Any | None: ...  # FloatingPanel
    def isCurrentTab(self) -> bool: ...
    def setIsCurrentTab(self) -> None: ...
    def isFloating(self) -> bool: ...
    def clone(self) -> 'PaneTab': ...
    def linkGroup(self) -> paneLinkType: ...
    def setLinkGroup(self, group: paneLinkType) -> None: ...
    def isPin(self) -> bool: ...
    def setPin(self, pin: bool) -> None: ...
    def size(self) -> tuple[int, int]: ...
    def contentSize(self) -> tuple[int, int]: ...

    # Methods from PathBasedPaneTab (inherited)
    def cd(self, path: str) -> None: ...
    def currentNode(self) -> Node: ...
    def pwd(self) -> Node: ...
    def setCurrentNode(self, node: Node, pick_node: bool = True) -> None: ...
    def setPwd(self, node: Node) -> None: ...

class UndoGroup:
    """Context manager for grouping operations into a single undo."""
    def __init__(self, name: str) -> None: ...
    def __enter__(self) -> 'UndoGroup': ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...

def undos() -> 'UndoManager':
    """Get undo manager for grouping operations."""
    ...

class UndoManager:
    """Undo manager for grouping operations."""
    def group(self, name: str) -> UndoGroup: ...
    def clear(self) -> None: ...
    def disabler(self) -> 'UndoDisabler': ...

class UndoDisabler:
    """Context manager to disable undo tracking."""
    def __enter__(self) -> 'UndoDisabler': ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...

# Progress reporting for long operations
def progressBar() -> 'ProgressBar':
    """Get progress bar for long operations."""
    ...

class ProgressBar:
    """Progress reporting for long operations."""
    def __init__(self) -> None: ...
    def __enter__(self) -> 'ProgressBar': ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
    def update(self, progress: float, message: str = "") -> None: ...
    def setLabel(self, label: str) -> None: ...

# Additional node access functions
def nodes(node_paths: tuple[str, ...]) -> tuple[Node|None, ...]:
    """Get multiple nodes by paths. Returns None for paths that don't exist."""
    ...

def items(item_paths: tuple[str, ...]) -> tuple[NetworkMovableItem|None, ...]:
    """Get multiple network items by paths. Returns None for paths that don't exist."""
    ...

def item(item_path: str) -> NetworkMovableItem|None:
    """Get network item by path. Returns None if path doesn't exist."""
    ...

def setPwd(node: Node) -> None:
    """Set current working directory node."""
    ...

def parent() -> Node:
    """Get parent of current node."""
    ...

def nodeBySessionId(session_id: int) -> Node|None:
    """Get node by session ID."""
    ...

def itemBySessionId(session_id: int) -> NetworkMovableItem|None:
    """Get network item by session ID."""
    ...

def networkBoxBySessionId(session_id: int) -> NetworkBox|None:
    """Get network box by session ID."""
    ...

def stickyNoteBySessionId(session_id: int) -> StickyNote|None:
    """Get sticky note by session ID."""
    ...

def networkDotBySessionId(session_id: int) -> NetworkDot|None:
    """Get network dot by session ID."""
    ...

def subnetIndirectInputBySessionId(session_id: int) -> IndirectInput|None:
    """Get subnet indirect input by session ID."""
    ...

def nodeConnectionBySessionId(session_id: int) -> NodeConnection|None:
    """Get node connection by session ID."""
    ...

# Selection functions
def selectedItems() -> tuple[NetworkMovableItem, ...]:
    """Get all selected network items."""
    ...

def selectedConnections() -> tuple[NodeConnection, ...]:
    """Get all selected node connections."""
    ...

# Node operations
def copyNodesTo(nodes: tuple[Node, ...], destination: Node) -> tuple[Node, ...]:
    """Copy nodes to new location."""
    ...

def moveNodesTo(nodes: tuple[Node, ...], destination: Node) -> None:
    """Move nodes to new location."""
    ...

def copyNodesToClipboard(nodes: tuple[Node, ...]) -> None:
    """Copy nodes to clipboard."""
    ...

def pasteNodesFromClipboard(destination: Node|None = None) -> tuple[Node, ...]:
    """Paste nodes from clipboard."""
    ...

def sortedNodes(nodes: tuple[Node, ...]) -> tuple[Node, ...]:
    """Sort nodes by input/output order."""
    ...

def sortedNodePaths(node_paths: tuple[str, ...]) -> tuple[str, ...]:
    """Sort node paths by input/output order."""
    ...

def preferredNodeType(category: str|NodeTypeCategory, name: str) -> NodeType|None:
    """Get preferred node type, evaluating aliases."""
    ...

# Parameter access functions
def parm(parm_path: str) -> Parm|None:
    """Get parameter by path."""
    ...

def parmTuple(parm_path: str) -> ParmTuple|None:
    """Get parameter tuple by path."""
    ...

def evalParm(parm_path: str) -> int|float|str:
    """Evaluate parameter by path."""
    ...

def evalParmTuple(parm_path: str) -> tuple[int|float|str, ...]:
    """Evaluate parameter tuple by path."""
    ...

def ch(parm_path: str) -> float:
    """Evaluate parameter (backward compatibility)."""
    ...

def chsop(parm_path: str) -> str:
    """Evaluate node reference parameter."""
    ...

def chsoplist(parm_path: str) -> tuple[str, ...]:
    """Evaluate node list parameter."""
    ...

def evaluatingParm() -> Parm|None:
    """Get currently evaluating parameter."""
    ...

def lvar(variable_name: str) -> Any:
    """Get local variable value."""
    ...

def parmClipboardContents() -> tuple[Parm, ...]:
    """Get parameter clipboard contents."""
    ...

# File I/O functions
def findFile(filename: str) -> str|None:
    """Find file in Houdini path."""
    ...

def findFiles(pattern: str) -> tuple[str, ...]:
    """Find all matching files in Houdini path."""
    ...

def findDirectory(dirname: str) -> str|None:
    """Find directory in Houdini path."""
    ...

def findDirectories(pattern: str) -> tuple[str, ...]:
    """Find all matching directories in Houdini path."""
    ...

def findFilesWithExtension(extension: str, directories: tuple[str, ...] = ...) -> tuple[str, ...]:
    """Find files by extension."""
    ...

def readFile(filename: str) -> str:
    """Read file contents as string."""
    ...

def readBinaryFile(filename: str) -> bytes:
    """Read file contents as bytes."""
    ...

def homeHoudiniDirectory() -> str:
    """Get home Houdini directory."""
    ...

def houdiniPath() -> tuple[str, ...]:
    """Get Houdini path as tuple of directories."""
    ...

def fileReferences() -> tuple[tuple[Parm, str], ...]:
    """Get file references in scene."""
    ...

# Scripting functions
def hscript(command: str) -> str:
    """Execute HScript command and return output."""
    ...

def hscriptExpression(expression: str) -> Any:
    """Evaluate HScript expression."""
    ...

def hscriptFloatExpression(expression: str) -> float:
    """Evaluate HScript float expression."""
    ...

def hscriptStringExpression(expression: str) -> str:
    """Evaluate HScript string expression."""
    ...

def hscriptVectorExpression(expression: str) -> tuple[float, ...]:
    """Evaluate HScript vector expression."""
    ...

def hscriptMatrixExpression(expression: str) -> Matrix4:
    """Evaluate HScript matrix expression."""
    ...

def hscriptCommandHelp(command: str) -> str:
    """Get HScript command help."""
    ...

def expandString(string: str) -> str:
    """Expand variables/expressions in string."""
    ...

def expandStringAtFrame(string: str, frame: float) -> str:
    """Expand variables/expressions at specific frame."""
    ...

def encode(string: str) -> str:
    """Encode string for use as attribute name."""
    ...

def decode(string: str) -> str:
    """Decode attribute name back to string."""
    ...

def incrementNumberedString(string: str) -> str:
    """Increment number in string (e.g., 'node1' -> 'node2')."""
    ...

def expressionGlobals() -> dict[str, Any]:
    """Get expression globals dictionary."""
    ...

# Environment functions
def getenv(var_name: str, default: str = "") -> str:
    """Get environment variable."""
    ...

def putenv(var_name: str, value: str) -> None:
    """Set environment variable."""
    ...

def unsetenv(var_name: str) -> None:
    """Unset environment variable."""
    ...

def allowEnvironmentToOverwriteVariable(var_name: str, allow: bool) -> None:
    """Allow environment to overwrite variable."""
    ...

# Application info functions
def applicationCompilationDate() -> str:
    """Get application compilation date."""
    ...

def applicationPlatformInfo() -> str:
    """Get platform information."""
    ...

def isApprentice() -> bool:
    """Check if running apprentice version."""
    ...

def licenseCategory() -> str:
    """Get license category."""
    ...

def hdkAPIVersion() -> str:
    """Get HDK API version."""
    ...

def exit(exit_code: int = 0, suppress_save_prompt: bool = False) -> None:
    """Exit Houdini."""
    ...

def machineName() -> str:
    """Get machine name."""
    ...

def userName() -> str:
    """Get user name."""
    ...

def maxThreads() -> int:
    """Get maximum thread count."""
    ...

def setMaxThreads(count: int) -> None:
    """Set maximum thread count."""
    ...

def releaseLicense() -> None:
    """Release Houdini license."""
    ...

def helpServerUrl() -> str:
    """Get help server base URL."""
    ...

def hipExtension() -> str:
    """Get hip file extension for current license."""
    ...

# Cooking functions
def updateModeSetting() -> str:
    """Get update mode setting (Auto Update, Manual, etc.)."""
    ...

def setUpdateMode(mode: str) -> None:
    """Set update mode."""
    ...

# Utilities
def almostEqual(a: float, b: float, tolerance: float = 0.00001) -> bool:
    """Compare floats with tolerance."""
    ...

def patternMatch(pattern: str, string: str) -> bool:
    """Pattern matching."""
    ...

def scaleFromMKS(value: float, unit_type: str) -> float:
    """Scale value from MKS units."""
    ...

def scaleToMKS(value: float, unit_type: str) -> float:
    """Scale value to MKS units."""
    ...

def assertTrue(condition: bool, message: str = "") -> None:
    """Assert condition is true."""
    ...

# Image functions
def imageResolution(filename: str) -> tuple[int, int]:
    """Get image resolution."""
    ...

def saveImageDataToFile(data: bytes, filename: str, width: int, height: int, format: str = "png") -> None:
    """Save image data to file."""
    ...

# Bundle functions
def addNodeBundle(name: str) -> 'NodeBundle':
    """Create a node bundle."""
    ...

def nodeBundle(name: str) -> 'NodeBundle|None':
    """Get node bundle by name."""
    ...

def nodeBundles() -> tuple['NodeBundle', ...]:
    """Get all node bundles."""
    ...

class NodeBundle:
    """Named collection of nodes."""
    def __init__(self) -> None: ...
    def name(self) -> str: ...
    def setName(self, name: str) -> None: ...
    def nodes(self) -> tuple[Node, ...]: ...
    def addNode(self, node: Node) -> None: ...
    def removeNode(self, node: Node) -> None: ...
    def clear(self) -> None: ...
    def destroy(self) -> None: ...

# Session module functions
def sessionModuleSource() -> str:
    """Get session module source code."""
    ...

def setSessionModuleSource(source: str) -> None:
    """Set session module source code."""
    ...

def appendSessionModuleSource(source: str) -> None:
    """Append to session module source code."""
    ...

# Context options
def contextOption(name: str) -> Any:
    """Get context option value."""
    ...

def setContextOption(name: str, value: Any) -> None:
    """Set context option value."""
    ...

def hasContextOption(name: str) -> bool:
    """Check if context option exists."""
    ...

def removeContextOption(name: str) -> None:
    """Remove context option."""
    ...

def contextOptions() -> tuple[str, ...]:
    """Get all context option names."""
    ...

# DOP functions
def currentDopNet() -> DopNode|None:
    """Get current DOP network."""
    ...

def setCurrentDopNet(dopnet: DopNode|None) -> None:
    """Set current DOP network."""
    ...

def simulationEnabled() -> bool:
    """Check if simulation is enabled."""
    ...

def setSimulationEnabled(enabled: bool) -> None:
    """Enable or disable simulation."""
    ...

# Colors
def defaultColor(category: str|NodeTypeCategory) -> Color:
    """Get default node color for category."""
    ...

def setDefaultColor(category: str|NodeTypeCategory, color: Color) -> None:
    """Set default node color for category."""
    ...

# VEX functions
def runVex(vex_code: str, geometry: Geometry|None = None, precision: str = "32") -> dict[str, Any]:
    """Run VEX code and return results."""
    ...

def vexContextForNodeTypeCategory(category: NodeTypeCategory) -> str:
    """Get VEX context name for node type category."""
    ...

def vexContextForShaderType(shader_type: str) -> str:
    """Get VEX context name for shader type."""
    ...

def vexContexts() -> tuple[str, ...]:
    """Get all VEX context names."""
    ...

# Preferences
def getPreference(name: str) -> Any:
    """Get preference value."""
    ...

def setPreference(name: str, value: Any) -> None:
    """Set preference value."""
    ...

def hasPreference(name: str) -> bool:
    """Check if preference exists."""
    ...

def removePreference(name: str) -> None:
    """Remove preference."""
    ...

def preferences() -> tuple[str, ...]:
    """Get all preference names."""
    ...

# Animation
def animationClips() -> tuple['AnimationClip', ...]:
    """Get all animation clips."""
    ...

def animationClip(name: str) -> 'AnimationClip|None':
    """Get animation clip by name."""
    ...

def addAnimationClip(name: str) -> 'AnimationClip':
    """Create animation clip."""
    ...

def animationLayers() -> tuple['AnimationLayer', ...]:
    """Get all animation layers."""
    ...

def animationLayer(name: str) -> 'AnimationLayer|None':
    """Get animation layer by name."""
    ...

def addAnimationLayer(name: str) -> 'AnimationLayer':
    """Create animation layer."""
    ...

class AnimationClip:
    """Animation clip."""
    def __init__(self) -> None: ...
    def name(self) -> str: ...
    def setName(self, name: str) -> None: ...
    def startTime(self) -> float: ...
    def endTime(self) -> float: ...
    def setTimeRange(self, start: float, end: float) -> None: ...
    def destroy(self) -> None: ...

class AnimationLayer:
    """Animation layer."""
    def __init__(self) -> None: ...
    def name(self) -> str: ...
    def setName(self, name: str) -> None: ...
    def weight(self) -> float: ...
    def setWeight(self, weight: float) -> None: ...
    def destroy(self) -> None: ...

# APEX functions
def apexNodeByPath(path: str) -> 'ApexNode|None':
    """Get APEX node by path."""
    ...

def apexNodes() -> tuple[ApexNode, ...]:
    """Get all APEX nodes."""
    ...

# Additional utility functions
def isValidNodeName(name: str) -> bool:
    """Check if string is valid node name."""
    ...

def isValidParameterName(name: str) -> bool:
    """Check if string is valid parameter name."""
    ...

def severityString(severity: int) -> str:
    """Convert severity number to string."""
    ...

# Third-party library versions
def thirdPartyLibraryVersions() -> dict[str, str]:
    """Get versions of third-party libraries."""
    ...

def vdbVersionInfo() -> dict[str, Any]:
    """Get OpenVDB version information."""
    ...

def videoEncoders() -> tuple[str, ...]:
    """Get available video encoder names."""
    ...

# Additional node bundle function
def selectedNodeBundles() -> tuple[NodeBundle, ...]:
    """Get all selected node bundles."""
    ...

# Additional file functions (CPIO and index data)
def loadCPIO(filename: str) -> dict[str, bytes]:
    """Load CPIO archive."""
    ...

def saveCPIO(data: dict[str, bytes], filename: str) -> None:
    """Save CPIO archive."""
    ...

def indexDataFromFile(filename: str) -> bytes:
    """Load index data from file."""
    ...

def saveIndexDataToFile(data: bytes, filename: str) -> None:
    """Save index data to file."""
    ...

# Hip file module functions
class hipFile:
    """HIP file operations."""

    @staticmethod
    def load(filename: str, suppress_save_prompt: bool = False, ignore_load_warnings: bool = False) -> None:
        """Load HIP file."""
        ...

    @staticmethod
    def save(filename: str|None = None, save_to_recent_files: bool = True) -> None:
        """Save HIP file."""
        ...

    @staticmethod
    def saveAndIncrementFileName() -> None:
        """Save HIP file and increment version number in filename."""
        ...

    @staticmethod
    def saveAsBackup() -> None:
        """Save as backup file."""
        ...

    @staticmethod
    def clear(suppress_save_prompt: bool = False) -> None:
        """Clear HIP file (new scene)."""
        ...

    @staticmethod
    def merge(filename: str, node_pattern: str = "*", overwrite_existing: bool = False, ignore_load_warnings: bool = False) -> None:
        """Merge nodes from HIP file."""
        ...

    @staticmethod
    def collisionNodesIfMerged(filename: str, node_pattern: str = "*") -> tuple[str, ...]:
        """Get node paths that would collide if file were merged."""
        ...

    @staticmethod
    def name() -> str:
        """Get current HIP file name."""
        ...

    @staticmethod
    def path() -> str:
        """Get current HIP file path."""
        ...

    @staticmethod
    def basename() -> str:
        """Get current HIP file basename (without directory)."""
        ...

    @staticmethod
    def isLoadingHipFile() -> bool:
        """Check if HIP file is currently loading."""
        ...

    @staticmethod
    def isShuttingDown() -> bool:
        """Check if Houdini is shutting down."""
        ...

    @staticmethod
    def hasUnsavedChanges() -> bool:
        """Check if HIP file has unsaved changes."""
        ...

    @staticmethod
    def setName(filename: str) -> None:
        """Set HIP file name (without saving)."""
        ...

    @staticmethod
    def isNewFile() -> bool:
        """Check if this is a new unsaved file."""
        ...

# Additional environment function
def getEnvConfigValue(name: str) -> Any:
    """Get environment config value."""
    ...

# Additional context option functions
def contextOptionNames() -> tuple[str, ...]:
    """Get all context option names (alias for contextOptions())."""
    ...

def contextOptionConfig(name: str) -> dict[str, Any]:
    """Get context option configuration."""
    ...

def setContextOptionConfig(name: str, config: dict[str, Any]) -> None:
    """Set context option configuration."""
    ...

def isAutoContextOption(name: str) -> bool:
    """Check if context option is automatically set."""
    ...

def isAutoContextOptionOverridden(name: str) -> bool:
    """Check if auto context option is overridden."""
    ...

def addContextOptionChangeCallback(callback: Any) -> int:
    """Add callback for context option changes. Returns callback ID."""
    ...

def removeContextOptionChangeCallback(callback_id: int) -> None:
    """Remove context option change callback."""
    ...

def removeAllContextOptionChangeCallbacks() -> None:
    """Remove all context option change callbacks."""
    ...

def contextOptionChangeCallbacks() -> tuple[int, ...]:
    """Get all context option change callback IDs."""
    ...

# Additional utility functions
def updateProgressAndCheckForInterrupt(message: str = "", percentage: float = -1) -> None:
    """Update progress and check if user interrupted."""
    ...

def refreshStartupPathCacheDirectory() -> None:
    """Refresh startup path cache directory."""
    ...

def registerOpdefPath(path: str) -> None:
    """Register operator definition path."""
    ...

def startHoudiniEngineDebugger() -> None:
    """Start Houdini Engine debugger."""
    ...

def chopExportConflictResolutionPattern() -> str:
    """Get CHOP export conflict resolution pattern."""
    ...

def setChopExportConflictResolutionPattern(pattern: str) -> None:
    """Set CHOP export conflict resolution pattern."""
    ...

# Additional APEX functions
def apexNodeBySessionId(session_id: int) -> ApexNode|None:
    """Get APEX node by session ID."""
    ...

def apexNodeConnectionBySessionId(session_id: int) -> 'ApexNodeConnection|None':
    """Get APEX node connection by session ID."""
    ...

def apexStickyNoteBySessionId(session_id: int) -> StickyNote|None:
    """Get APEX sticky note by session ID."""
    ...

def createApexRootNode(name: str = "apex") -> ApexNode:
    """Create APEX root node."""
    ...

# Additional preference functions
def addPreference(name: str, default_value: Any) -> None:
    """Add new preference."""
    ...

def getPreferenceNames() -> tuple[str, ...]:
    """Get all preference names (alias for preferences())."""
    ...

def loadPreferences(filename: str) -> None:
    """Load preferences from file."""
    ...

def savePreferences(filename: str) -> None:
    """Save preferences to file."""
    ...

def refreshPreferences() -> None:
    """Refresh preferences from disk."""
    ...

def createPreferenceRegistry() -> None:
    """Create preference registry."""
    ...

def refreshPreferenceRegistry() -> None:
    """Refresh preference registry."""
    ...

# Additional animation functions
def removeAnimationLayer(layer: AnimationLayer) -> None:
    """Remove animation layer."""
    ...

def createAnimationClip(name: str, start_time: float, end_time: float) -> AnimationClip:
    """Create animation clip with time range."""
    ...

def createAnimationLayers(count: int) -> tuple[AnimationLayer, ...]:
    """Create multiple animation layers."""
    ...

def clipInfo(clip: AnimationClip) -> dict[str, Any]:
    """Get clip information dictionary."""
    ...

def convertClipData(data: bytes, from_format: str, to_format: str) -> bytes:
    """Convert clip data between formats."""
    ...

def convertKeyframesToClipData(keyframes: dict[str, Any]) -> bytes:
    """Convert keyframes to clip data."""
    ...

def commitPendingKeyframes() -> None:
    """Commit pending keyframes to animation."""
    ...

# Additional file I/O functions
def loadCPIODataFromString(data: str) -> dict[str, bytes]:
    """Load CPIO data from string."""
    ...

def loadIndexDataFromString(data: str) -> bytes:
    """Load index data from string."""
    ...

def saveCPIODataToString(data: dict[str, bytes]) -> str:
    """Save CPIO data to string."""
    ...

def saveIndexDataToString(data: bytes) -> str:
    """Save index data to string."""
    ...

# ==============================================================================
# SUBMODULES
# ==============================================================================
# Note: Submodule stubs are in stubs/hou/*.pyi files
# These are pre-loaded C++ modules: anim, clone, crowds, data, dop, fs, galleries,
# hda, hmath, ik, logging, lop, perfMon, playbar, properties, pypanel, session,
# shelves, styles, takes, text, webServer
# Accessible as: hou.hmath, hou.dop, hou.logging, etc.

class PerfMonEvent:
    """Represents an event recorded by the performance monitor for generating statistics.

    Note: All methods may raise hou.OperationFailed if the event was not recorded.
    Time and memory statistics are reported in milliseconds and bytes respectively.
    """

    def id(self) -> int:
        """Return the event's unique identifier used internally by the performance monitor."""
        ...

    def isAutoNestEnabled(self) -> bool:
        """Return True if the event automatically nests other events started while this event is running."""
        ...

    def isRunning(self) -> bool:
        """Return True if the event has been started but not stopped."""
        ...

    def isTiming(self) -> bool:
        """Deprecated: Use isRunning() instead."""
        ...

    def name(self) -> str:
        """Return the event name."""
        ...

    def object(self) -> str:
        """Return the object that the event applies to."""
        ...

    def startTime(self) -> float:
        """Return the start time of the event in milliseconds since the epoch date."""
        ...

    def stop(self) -> tuple[float, int]:
        """Stop the event timer and return (elapsed_time_ms, memory_growth_bytes)."""
        ...


class PerfMonProfile:
    """Represents a performance monitor profile.

    Note: Time and memory statistics are reported in milliseconds and bytes respectively.
    """

    def cancel(self) -> None:
        """Stop the profile from recording events and remove it from the performance monitor."""
        ...

    def exportAsCSV(self, file_path: str) -> None:
        """Export the profile statistics to disk using comma-separated (CSV) format."""
        ...

    def id(self) -> int:
        """Return the profile's unique identifier used internally by the performance monitor."""
        ...

    def isActive(self) -> bool:
        """Return True if the profile is either recording events or is paused."""
        ...

    def isRecordingCookStats(self) -> bool:
        """Return True if the profile is recording cook events and statistics."""
        ...

    def isRecordingPDGCookStats(self) -> bool:
        """Return True if the profile is recording PDG node cook events and statistics."""
        ...

    def isRecordingDrawStats(self) -> bool:
        """Return True if the profile is recording draw events and statistics."""
        ...

    def isRecordingErrors(self) -> bool:
        """Return True if the profile is recording errors."""
        ...

    def isRecordingFrameStats(self) -> bool:
        """Return True if the profile is recording frame events and statistics."""
        ...

    def isRecordingGPUDrawStats(self) -> bool:
        """Return True if the profile is recording GPU draw events and statistics."""
        ...

    def isRecordingRenderStats(self) -> bool:
        """Return True if the profile is recording statistics related to rendering."""
        ...

    def isRecordingScriptStats(self) -> bool:
        """Return True if the profile is recording script events and statistics."""
        ...

    def isRecordingSolveStats(self) -> bool:
        """Return True if the profile is recording simulation solver events and statistics."""
        ...

    def isRecordingThreadStats(self) -> bool:
        """Return True if the profile is recording thread statistics."""
        ...

    def isRecordingViewportStats(self) -> bool:
        """Return True if the profile is recording viewport events and statistics."""
        ...

    def isPaused(self) -> bool:
        """Return True if the profile is paused from recording."""
        ...

    def pause(self) -> None:
        """Pause the profile from recording events and statistics."""
        ...

    def resume(self) -> None:
        """Unpause the profile so that it can record events and statistics."""
        ...

    def save(self, file_path: str) -> None:
        """Deprecated: Use hou.perfMon.saveProfile() instead."""
        ...

    def stats(self) -> str:
        """Return the profile statistics in JSON format."""
        ...

    def stop(self) -> None:
        """Stop the profile from recording and generate statistics for recorded events."""
        ...

    def title(self) -> str:
        """Return the profile title."""
        ...


class PerfMonRecordOptions:
    """Options specifying types of statistics to be recorded in a performance monitor profile."""

    def recordCookStats(self) -> bool:
        """Return True if cook statistics should be recorded."""
        ...

    def recordPDGCookStats(self) -> bool:
        """Return True if PDG node and work item cook statistics should be recorded."""
        ...

    def recordDrawStats(self) -> bool:
        """Return True if node draw statistics should be recorded."""
        ...

    def recordErrors(self) -> bool:
        """Return True if warnings and errors should be recorded."""
        ...

    def recordFrameStats(self) -> bool:
        """Return True if frame statistics should be recorded."""
        ...

    def recordGPUDrawStats(self) -> bool:
        """Return True if node GPU draw statistics should be recorded."""
        ...

    def recordMemoryStats(self) -> bool:
        """Return True if memory statistics should be recorded."""
        ...

    def recordPaneStats(self) -> bool:
        """Return True if non-viewport pane statistics should be recorded."""
        ...

    def recordRenderStats(self) -> bool:
        """Return True if Mantra render statistics should be recorded."""
        ...

    def recordScriptStats(self) -> bool:
        """Return True if hscript and Python statistics should be recorded."""
        ...

    def recordSolveStats(self) -> bool:
        """Return True if DOP solver statistics should be recorded."""
        ...

    def recordThreadStats(self) -> bool:
        """Return True if thread statistics should be recorded."""
        ...

    def recordViewportStats(self) -> bool:
        """Return True if viewport statistics should be recorded."""
        ...

    def setRecordCookStats(self, record: bool) -> None:
        """Turn the recording of node cook statistics on or off."""
        ...

    def setRecordPDGCookStats(self, record: bool) -> None:
        """Turn the recording of PDG node and work item cook statistics on or off."""
        ...

    def setRecordDrawStats(self, record: bool) -> None:
        """Turn the recording of node draw statistics on or off."""
        ...

    def setRecordErrors(self, record: bool) -> None:
        """Turn the recording of warnings and errors on or off."""
        ...

    def setRecordFrameStats(self, record: bool) -> None:
        """Turn the recording of frame statistics on or off."""
        ...

    def setRecordGPUDrawStats(self, record: bool) -> None:
        """Turn the recording of node GPU draw statistics on or off."""
        ...

    def setRecordMemoryStats(self, record: bool) -> None:
        """Turn the recording of memory statistics on or off."""
        ...

    def setRecordPaneStats(self, record: bool) -> None:
        """Turn the recording of non-viewport pane statistics on or off."""
        ...

    def setRecordRenderStats(self, record: bool) -> None:
        """Turn the recording of Mantra render statistics on or off."""
        ...

    def setRecordScriptStats(self, record: bool) -> None:
        """Turn the recording of hscript and Python statistics on or off."""
        ...

    def setRecordSolveStats(self, record: bool) -> None:
        """Turn the recording of DOP solver statistics on or off."""
        ...

    def setRecordThreadStats(self, record: bool) -> None:
        """Turn the recording of thread statistics on or off."""
        ...

    def setRecordViewportStats(self, record: bool) -> None:
        """Turn the recording of viewport statistics on or off."""
        ...

