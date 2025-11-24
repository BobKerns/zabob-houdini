# Missing Package-Level Entries in hou.pyi

This document catalogs the missing package-level entries from the Houdini `hou` module that are not yet implemented in `stubs/hou.pyi`. Entries are grouped by broad category of purpose.

## SHELF / UI SCRIPTING
**Purpose:** Scripting shelf tools, tabs, and sets

- `hou.Shelf` - Shelf tab
- `hou.ShelfSet` - Collection of shelf tabs
- `hou.ShelfDock` - Shelf area container
- `hou.ShelfElement` - Base class for shelf tools/tabs/sets
- `hou.Tool` - Individual shelf tool
- `hou.shelves` - Module for shelf management functions

## UI / DESKTOP / PANES
**Purpose:** Desktop layouts, panes, floating panels, dialogs

- `hou.Desktop` - Desktop/pane layout
- `hou.FloatingPanel` - Floating window
- `hou.Pane` - Container for pane tabs
- `hou.PaneTab` - Individual pane tab
- `hou.Dialog` - Houdini dialog
- `hou.NetworkEditor` - Network editor pane
- `hou.SceneViewer` - Scene viewer pane
- `hou.GeometryViewport` - Viewport within scene viewer
- `hou.ParameterEditor` - Parameter editor pane
- `hou.PerformanceMonitor` - Performance monitor pane
- `hou.DataTree` - Data tree pane
- `hou.CompositorViewer` - Compositing viewer pane
- `hou.HelpBrowser` - Help browser pane
- `hou.PythonPanel` - Custom Python panel
- `hou.PythonPanelInterface` - Python panel definition
- `hou.RenderGallery` - Render gallery pane
- `hou.GeometrySpreadsheet` - Geometry spreadsheet pane
- `hou.SceneGraphTree` - Scene graph tree (Solaris)
- `hou.ChannelEditorPane` - Channel editor pane
- `hou.ContextViewer` - Context viewer pane
- `hou.IPRViewer` - Interactive preview render window

## VIEWER STATES & HANDLES
**Purpose:** Custom viewer states and handles

- `hou.ViewerState` - Viewer state definition
- `hou.ViewerStateTemplate` - State template
- `hou.ViewerStateContext` - State execution context
- `hou.ViewerStateDragger` - State dragger
- `hou.ViewerStateMenu` - State context menu
- `hou.Handle` - Bound handle
- `hou.ViewerHandleTemplate` - Handle template
- `hou.ViewerHandleContext` - Handle execution context
- `hou.ViewerHandleDragger` - Handle dragger
- `hou.Selector` - Geometry selector
- `hou.ViewerDragger` - Interactive dragger

## VIEWPORT / DISPLAY
**Purpose:** Viewport settings, drawables, visualization

- `hou.GeometryViewportSettings` - Viewport display options
- `hou.GeometryViewportDisplaySet` - Display set for geometry context
- `hou.GeometryViewportBackground` - Viewport background
- `hou.GeometryViewportCamera` - Viewport camera
- `hou.ConstructionPlane` - Grid/construction plane
- `hou.ReferencePlane` - Reference plane
- `hou.FlipbookSettings` - Flipbook options
- `hou.Drawable` - Base drawable
- `hou.AdvancedDrawable` - Advanced drawable
- `hou.Drawable2D` - 2D drawable
- `hou.SimpleDrawable` - Simple guide geometry
- `hou.GeometryDrawable` - Guide geometry drawable
- `hou.GeometryDrawableGroup` - Drawable group
- `hou.GadgetDrawable` - Gadget with picking
- `hou.TextDrawable` - Viewport text
- `hou.NetworkShape` - Network editor shape base
- `hou.NetworkShapeBox` - Network rectangle
- `hou.NetworkShapeConnection` - Network wire
- `hou.NetworkShapeLine` - Network line
- `hou.NetworkShapeNodeShape` - Network node shape
- `hou.NetworkImage` - Network background image
- `hou.NetworkFootprint` - Node footprint ring
- `hou.NetworkAnimValue` - Network animation value
- `hou.ViewportVisualizer` - Viewport visualizer
- `hou.ViewportVisualizerType` - Visualizer type

## UI EVENTS
**Purpose:** User interface event handling

- `hou.UIEvent` - Base UI event
- `hou.UIEventDevice` - Device-specific event info
- `hou.ViewerEvent` - Viewer-specific event
- `hou.CompositorViewerEvent` - Compositor viewer event
- `hou.GeometrySelection` - Component selection in viewport
- `hou.Viewport2D` - 2D viewport (COP)
- `hou.GadgetContext` - Gadget context

## ANIMATION / PLAYBAR
**Purpose:** Animation, keyframes, playback control

### Classes
- `hou.BaseKeyframe` - Abstract keyframe base
- `hou.Keyframe` - Numerical keyframe
- `hou.StringKeyframe` - String keyframe
- `hou.Bookmark` - Animation bookmark
- `hou.AnimBar` - Animation toolbar
- `hou.ChannelGraph` - Animation editor graph
- `hou.ChannelGraphSelection` - Graph selection
- `hou.ChannelList` - Channel list
- `hou.ChannelPrim` - Channel primitive

### Functions
- `addAnimationLayer()` - Add animation layer
- `removeAnimationLayer()` - Remove animation layer
- `createAnimationClip()` - Create animation clip mixer
- `createAnimationLayers()` - Create animation layer mixer
- `clipInfo()` - Clip information
- `convertClipData()` - Convert clip data
- `convertKeyframesToClipData()` - Convert keyframes to clip data
- `commitPendingKeyframes()` - Commit pending keyframes

### Interpolation Functions
- `bezier()` - Bezier interpolation
- `constant()` - Constant interpolation
- `cubic()` - Cubic interpolation
- `cycle()` - Cycle extrapolation
- `cycleoffset()` - Cycle with offset
- `cycleoffsett()` - Cycle with time offset
- `cyclet()` - Cycle with time
- `ease()` - Ease interpolation
- `easein()` - Ease in
- `easeinp()` - Ease in (parametric)
- `easeout()` - Ease out
- `easeoutp()` - Ease out (parametric)
- `easep()` - Ease (parametric)
- `linear()` - Linear interpolation
- `match()` - Match slopes
- `matchin()` - Match incoming slope
- `matchout()` - Match outgoing slope
- `qlinear()` - Quaternion linear interpolation
- `quintic()` - Quintic interpolation
- `repeat()` - Repeat motion
- `repeatt()` - Repeat with time
- `spline()` - Spline through keyframes
- `vmatch()` - Vector match
- `vmatchin()` - Vector match incoming
- `vmatchout()` - Vector match outgoing

### Playbar Functions
- `fps()` - Get frames per second
- `frame()` - Get current frame
- `intFrame()` - Get current frame (integer)
- `time()` - Get current time
- `setFps()` - Set frames per second
- `setFrame()` - Set current frame
- `setTime()` - Set current time
- `frameToTime()` - Convert frame to time
- `timeToFrame()` - Convert time to frame

## DIGITAL ASSETS (HDA)
**Purpose:** HDA definition, sections, options

- `hou.HDADefinition` - HDA definition
- `hou.HDAOptions` - HDA options
- `hou.HDASection` - HDA section
- `hdaDefinition()` - Get HDA definition
- `hou.hda` - HDA management module

## SHADING / GALLERIES / MATERIALS
**Purpose:** Shaders, materials, galleries, style sheets

- `hou.ShopNode` - SHOP node
- `hou.VopNode` - VOP node
- `hou.VopNetNode` - VOP network node
- `hou.Gallery` - Gallery collection
- `hou.GalleryEntry` - Gallery entry
- `hou.StyleSheet` - Style sheet
- `hou.galleries` - Gallery management module
- `hou.styles` - Style sheet module
- `hou.properties` - Render properties module

## VEX / CONTEXTS
**Purpose:** VEX execution and contexts

- `hou.VexContext` - VEX/VOP context
- `runVex()` - Execute VEX code
- `vexContextForNodeTypeCategory()` - Get VEX context for category
- `vexContextForShaderType()` - Get VEX context for shader type
- `vexContexts()` - Get all VEX contexts

## CROWDS / AGENTS
**Purpose:** Crowd simulation and agent primitives

- `hou.Agent` - Agent primitive
- `hou.AgentClip` - Animation clip
- `hou.AgentDefinition` - Shared agent data
- `hou.AgentLayer` - Agent layer
- `hou.AgentMetadata` - Agent metadata
- `hou.AgentRig` - Agent rig
- `hou.AgentShape` - Agent shape
- `hou.AgentShapeBinding` - Shape binding
- `hou.AgentShapeDeformer` - Shape deformer
- `hou.AgentShapeLibrary` - Shape library
- `hou.AgentTransformGroup` - Transform group
- `hou.crowds` - Crowd functions module

## SOLARIS / USD
**Purpose:** USD/Solaris (LOP) functionality

- `hou.LopExpansionState` - Scene graph tree expansion state
- `hou.LopInstanceIdRule` - Instance ID pattern
- `hou.LopLockedStage` - USD stage lifetime guarantee
- `hou.LopPostLayer` - Post-layer authoring
- `hou.LopSelectionRule` - Scene graph selection rules
- `hou.LopViewportLoadMasks` - Payload load masks
- `hou.LopViewportOverrides` - Session overlay edits
- `hou.lop` - LOP functions module
- `hou.lopTraversalDemands` - Scene graph traversal specs

## COPERNICUS / IMAGES
**Purpose:** Compositing and image handling

- `hou.Cop2Node` - Compositor 2 node
- `hou.CopCableStructure` - Copernicus cable types
- `hou.CopVerb` - Copernicus node code
- `hou.ImageLayer` - 2D image layer
- `hou.NanoVDB` - NanoVDB volume
- `imageResolution()` - Get image resolution
- `saveImageDataToFile()` - Save image data

## GEOMETRY PRIMITIVES
**Purpose:** Additional geometry primitive types

- `hou.Quadric` - Quadric primitive
- `hou.VDB` - VDB primitive
- `hou.PackedPrim` - Packed primitive base
- `hou.PackedGeometry` - Packed geometry primitive
- `hou.PackedFragment` - Packed fragment primitive
- `hou.PointGroup` - Point group
- `hou.PrimGroup` - Primitive group
- `hou.EdgeGroup` - Edge group
- `hou.VertexGroup` - Vertex group
- `hou.Edge` - Edge
- `hou.AttribDataId` - Geometry change detection
- `hou.GeometryRayCache` - Ray intersection cache
- `hou.IndexPairPropertyTable` - Index pair properties

## APEX
**Purpose:** APEX node graphs

- `hou.ApexNode` - APEX node
- `hou.ApexNodeConnection` - APEX wire
- `hou.ApexNodeType` - APEX node type info
- `hou.ApexStickyNote` - APEX sticky note
- `apexNodeBySessionId()` - Get APEX node by session ID
- `apexNodeConnectionBySessionId()` - Get APEX connection by session ID
- `apexStickyNoteBySessionId()` - Get APEX sticky note by session ID
- `createApexRootNode()` - Create APEX session graph root

## ORGANIZATION / BUNDLES
**Purpose:** Node organization, bundles, network boxes

- `hou.NodeBundle` - Named node set
- `hou.OpNetworkBox` - OP network box
- `hou.OpStickyNote` - OP sticky note
- `hou.OpIndirectInput` - OP indirect input
- `hou.OpSubnetIndirectInput` - OP subnet input
- `hou.OpNetworkDot` - OP network dot
- `addNodeBundle()` - Create node bundle
- `nodeBundle()` - Get node bundle
- `nodeBundles()` - Get all node bundles
- `selectedNodeBundles()` - Get selected node bundles

## NODE CONNECTIONS
**Purpose:** Node connection types

- `hou.OpNodeConnection` - OP node connection
- `hou.SubnetIndirectInput` - Subnet indirect input

## TAKES
**Purpose:** Takes management

- `hou.Take` - Take object
- `hou.takes` - Takes module

## RADIAL MENUS
**Purpose:** Radial menu system

- `hou.RadialMenu` - Radial menu
- `hou.RadialItem` - Radial item base
- `hou.RadialScriptItem` - Radial script item
- `hou.RadialSubmenu` - Radial submenu

## PERFORMANCE MONITORING
**Purpose:** Performance profiling

- `hou.PerfMonEvent` - Performance event
- `hou.PerfMonProfile` - Performance profile
- `hou.PerfMonRecordOptions` - Recording options
- `hou.perfMon` - Performance monitoring module

## PREFERENCES
**Purpose:** User preferences management

- `addPreference()` - Add user preference
- `getPreference()` - Get preference value
- `setPreference()` - Set preference value
- `removePreference()` - Remove preference
- `getPreferenceNames()` - Get all preference names
- `loadPreferences()` - Load preferences from disk
- `savePreferences()` - Save preferences to disk
- `refreshPreferences()` - Refresh all preferences
- `createPreferenceRegistry()` - Create preference registry
- `refreshPreferenceRegistry()` - Update preference registry

## HOTKEYS
**Purpose:** Hotkey management

- `hou.PluginHotkeyDefinitions` - Plugin hotkey definitions
- `hou.hotkeys` - Hotkey functions module

## UTILITIES
**Purpose:** Utility classes and modules

- `hou.OrientedBoundingRect` - 2D oriented bounding rect
- `hou.InterruptableOperation` - Interruptable code block
- `hou.RedrawBlock` - Redraw batching
- `hou.ScriptEvalContext` - Scripting context
- `hou.ShellIO` - Shell I/O proxy
- `hou.AssetGalleryDataSource` - Asset gallery data source

## LOGGING / DATA
**Purpose:** Logging, data handling, file system

- `hou.logging` - Logging module
- `hou.data` - Recipe data format module
- `hou.fs` - File system utilities module
- `hou.text` - String manipulation module

## MODULES (SUBMODULES)
**Purpose:** Organized submodules for specific domains

- `hou.anim` - Animation utilities
- `hou.audio` - Audio playback
- `hou.clone` - Clone process management
- `hou.dop` - DOP functions
- `hou.hda` - HDA management
- `hou.hipFile` - Hip file functions
- `hou.hmath` - 3D math functions
- `hou.ik` - Inverse kinematics
- `hou.playbar` - Playbar functions
- `hou.pypanel` - Python panel functions
- `hou.qt` - Qt integration
- `hou.ui` - UI functions
- `hou.undos` - Undo management
- `hou.viewportVisualizers` - Visualizer functions
- `hou.webServer` - Web server module

## PACKAGE-LEVEL FUNCTIONS

### Node/Item Access
- `node()` - Get node by path
- `nodes()` - Get multiple nodes by paths
- `item()` - Get network item by path
- `items()` - Get multiple items by paths
- `cd()` - Change current node
- `pwd()` - Get current node
- `setPwd()` - Set current node
- `parent()` - Get parent of current node
- `root()` - Get root node
- `nodeBySessionId()` - Get node by session ID
- `itemBySessionId()` - Get item by session ID
- `networkBoxBySessionId()` - Get network box by session ID
- `stickyNoteBySessionId()` - Get sticky note by session ID
- `networkDotBySessionId()` - Get network dot by session ID
- `subnetIndirectInputBySessionId()` - Get subnet input by session ID
- `nodeConnectionBySessionId()` - Get node connection by session ID

### Selection
- `selectedNodes()` - Get selected nodes
- `selectedItems()` - Get selected items
- `selectedConnections()` - Get selected connections
- `clearAllSelected()` - Clear all selections
- `selectedNodeBundles()` - Get selected node bundles

### Node Operations
- `copyNodesTo()` - Copy nodes to new location
- `moveNodesTo()` - Move nodes to new location
- `copyNodesToClipboard()` - Copy nodes to clipboard
- `pasteNodesFromClipboard()` - Paste nodes from clipboard
- `sortedNodes()` - Sort nodes by input/output order
- `sortedNodePaths()` - Sort node paths by input/output order
- `nodeType()` - Get node type by name
- `preferredNodeType()` - Get preferred node type (evaluates aliases)

### Parameter Access
- `parm()` - Get parameter by path
- `parmTuple()` - Get parameter tuple by path
- `evalParm()` - Evaluate parameter by path
- `evalParmTuple()` - Evaluate parameter tuple by path
- `ch()` - Evaluate parameter (backward compatibility)
- `chsop()` - Evaluate node reference parameter
- `chsoplist()` - Evaluate node list parameter
- `evaluatingParm()` - Get currently evaluating parameter
- `lvar()` - Get local variable value
- `parmClipboardContents()` - Get parameter clipboard contents

### File I/O
- `findFile()` - Find file in Houdini path
- `findFiles()` - Find all matching files in Houdini path
- `findDirectory()` - Find directory in Houdini path
- `findDirectories()` - Find all matching directories
- `findFilesWithExtension()` - Find files by extension
- `readFile()` - Read file contents as string
- `readBinaryFile()` - Read file contents as bytes
- `homeHoudiniDirectory()` - Get home Houdini directory
- `houdiniPath()` - Get Houdini path as tuple
- `fileReferences()` - Get file references in scene
- `loadCPIODataFromString()` - Load CPIO data
- `loadIndexDataFromFile()` - Load index data from file
- `loadIndexDataFromString()` - Load index data from string
- `saveCPIODataToString()` - Save data to CPIO format
- `saveIndexDataToFile()` - Save index data to file
- `saveIndexDataToString()` - Save index data to string

### Scripting
- `hscript()` - Execute HScript command
- `hscriptExpression()` - Evaluate HScript expression
- `hscriptFloatExpression()` - Evaluate HScript float expression
- `hscriptStringExpression()` - Evaluate HScript string expression
- `hscriptVectorExpression()` - Evaluate HScript vector expression
- `hscriptMatrixExpression()` - Evaluate HScript matrix expression
- `hscriptCommandHelp()` - Get HScript command help
- `expandString()` - Expand variables/expressions
- `expandStringAtFrame()` - Expand at specific frame
- `encode()` - Encode string for attribute name
- `decode()` - Decode attribute name
- `incrementNumberedString()` - Increment number in string
- `expressionGlobals()` - Get expression globals dictionary

### Environment
- `getenv()` - Get environment variable
- `putenv()` - Set environment variable
- `unsetenv()` - Unset environment variable
- `allowEnvironmentToOverwriteVariable()` - Allow env override
- `getEnvConfigValue()` - Get config value as Houdini treats it

### Application Info
- `applicationName()` - Get application name
- `applicationVersion()` - Get version as tuple
- `applicationVersionString()` - Get version as string
- `applicationCompilationDate()` - Get compilation date
- `applicationPlatformInfo()` - Get platform info
- `isApprentice()` - Check if apprentice version
- `licenseCategory()` - Get license category
- `hdkAPIVersion()` - Get HDK API version
- `exit()` - Exit Houdini
- `machineName()` - Get machine name
- `userName()` - Get user name
- `maxThreads()` - Get max thread count
- `setMaxThreads()` - Set max thread count
- `releaseLicense()` - Release Houdini license
- `helpServerUrl()` - Get help server base URL
- `hipExtension()` - Get hip file extension for license
- `thirdPartyLibraryVersions()` - Get third-party library versions
- `vdbVersionInfo()` - Get VDB version info
- `videoEncoders()` - Get available video encoders

### Session
- `session` - Session module
- `sessionModuleSource()` - Get session module source
- `setSessionModuleSource()` - Set session module source
- `appendSessionModuleSource()` - Append to session module source

### Context Options
- `contextOption()` - Get context option value
- `setContextOption()` - Set context option value
- `removeContextOption()` - Remove context option
- `hasContextOption()` - Check if context option exists
- `contextOptionNames()` - Get all context option names
- `contextOptionConfig()` - Get context option UI config
- `setContextOptionConfig()` - Set context option UI config
- `isAutoContextOption()` - Check if auto option
- `isAutoContextOptionOverridden()` - Check if auto option overridden
- `addContextOptionChangeCallback()` - Add context option callback
- `removeContextOptionChangeCallback()` - Remove context option callback
- `removeAllContextOptionChangeCallbacks()` - Remove all context option callbacks
- `contextOptionChangeCallbacks()` - Get context option callbacks

### Cooking
- `updateModeSetting()` - Get update mode setting
- `setUpdateMode()` - Set update mode

### DOP
- `currentDopNet()` - Get current DOP network
- `setCurrentDopNet()` - Set current DOP network
- `simulationEnabled()` - Check if simulation enabled
- `setSimulationEnabled()` - Set simulation enabled

### Colors
- `defaultColor()` - Get default color for element
- `setDefaultColor()` - Set default color for element

### Utilities
- `almostEqual()` - Compare floats with tolerance
- `patternMatch()` - Pattern matching
- `scaleFromMKS()` - Scale from MKS units
- `scaleToMKS()` - Scale to MKS units
- `assertTrue()` - Assert condition is true
- `updateProgressAndCheckForInterrupt()` - Update progress (deprecated)
- `refreshStartupPathCacheDirectory()` - Refresh startup cache
- `registerOpdefPath()` - Register opdef path for web server
- `startHoudiniEngineDebugger()` - Start Houdini Engine debugger
- `chopExportConflictResolutionPattern()` - Get CHOP export pattern
- `setChopExportConflictResolutionPattern()` - Set CHOP export pattern

### UI Utilities
- `isUIAvailable()` - Check if UI is available

## Summary

Approximately **200+ missing types/functions** organized into **30+ functional categories**. The current stub file (3017 lines, 68 classes, 18 enums) has good coverage of:
- ✅ Core geometry (Geometry, Point, Prim, Vertex, Face, etc.)
- ✅ Nodes (Node, OpNode, SopNode, etc.)
- ✅ Parameters (Parm, ParmTuple, ParmTemplate types)
- ✅ Basic node types (SOP, OBJ, CHOP, ROP, DOP, COP, LOP)
- ✅ CHOP data (Track, Clip)
- ✅ Basic utilities (Vector, Matrix, Color, BoundingBox, Ramp)

Missing coverage areas:
- ❌ UI/Desktop/Panes (20+ classes)
- ❌ Viewer States & Handles (11+ classes)
- ❌ Viewport/Display (25+ classes)
- ❌ Animation/Playbar (40+ functions, 9 classes)
- ❌ Shelf system (6 classes + module)
- ❌ Crowds/Agents (11 classes + module)
- ❌ Solaris/USD (9 classes + module)
- ❌ Performance monitoring (3 classes + module)
- ❌ Galleries/Shading (8 classes + 3 modules)
- ❌ Most package-level functions (100+ functions)
- ❌ Many specialized modules (20+ modules)
