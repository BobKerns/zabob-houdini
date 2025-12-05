![Zabob Banner](docs/images/zabob-banner.jpg)
# Zabob-Houdini API Documentation

## Overview

Zabob-Houdini provides a Python API for creating Houdini node graphs programmatically. The API is designed to be declarative - you define nodes and their connections, then create them all at once.

## Core Concepts

### ZNode

A `ZNode` represents a single Houdini node that can be created. It stores the node definition including its parent, type, parameters, and connections.

### ZChain

A `ZChain` represents a sequence of nodes that are automatically connected in order. Chains can be nested and combined to create complex node networks.

### Lazy Creation

Nodes and chains are defined first, then created later via the `.create()` method. This allows for:
- Forward references (nodes can reference other nodes not yet defined)
- Circular dependencies (with proper care)
- Batch creation for better performance

When using `with zcontext(...) as ctx:`, the network is created and laid out for you. However, you may call `.create()` yourself if you need to work with the underlying Houdini object, or use the `.hou_node` property.

## Main Functions

### `znode()`

Creates a single node definition.

```python
def znode(
    parent: NodeParent,
    node_type: NodeType,
    name: str | None = None,
    _input: 'InputNode | list[InputNode] | None' = None,
    _display: bool = False,
    _render: bool = False,
    **attributes: Any
) -> ZNode
```

**Parameters:**
- `parent`: Parent znode - can be a path string (e.g., `"/obj"`), `ZNode`, or `hou.Node`
- `node_type`: Houdini node type name (e.g., `"box"`, `"xform"`, `"merge"`)
- `name`: Optional node name. If not provided, auto-generated based on type
- `_input`: Input connections - single node/chain, `Sequence` of nodes/chains, or `None`
- `_display`: Set display flag when znode is created (for SOP nodes)
- `_render`: Set render flag when znode is created (for SOP nodes)
- `**attributes`: Node parameter values as keyword arguments

**Returns:** `ZNode` object that can be created later

**Examples:**
```python
# Using zcontext manager for organization
with zcontext(znode("/obj", "geo")) as ctx:
    # Simple geometry node
    box = ctx.node("box", sizex=2, sizey=2, sizez=2)

    # Transform with input
    xform = ctx.node("xform", "my_transform", _input=box, tx=5)

    # Node with display flag
    output = ctx.node("null", "OUT", _input=xform, _display=True)
```

### `zchain()`

Creates a chain of nodes that are automatically connected in sequence.

```python
def zchain(
    *nodes: ChainableNode,
    **attributes: Any
) -> ZChain
```

**Parameters:**
- `*nodes`: Sequence of `ZNode`, `ZChain`, or `hou.Node` objects
- `**attributes`: Reserved for future use

**Returns:** `ZChain` object that can be created later

**Examples:**
```python
# Using zcontext for network creation
with zcontext(znode("/obj", "geo")) as ctx:
    # Simple chain
    processing = ctx.chain(
        ctx.node("box"),
        ctx.node("xform", tx=2),
        ctx.node("subdivide", iterations=2)
    )

    # ZChain with external input
    chain_with_input = ctx.chain(
        ctx.node("xform", "scale_up", _input=some_input, sx=2, sy=2, sz=2),
        ctx.node("xform", "translate", tx=5)
    )
```

### `zmerge()`

Creates a merge node with multiple inputs. All inputs must have the same parent.

```python
def zmerge(*inputs: ZNode, **attributes: Any) -> ZNode
```

**Parameters:**
- `*inputs`: ZNode objects to merge (must have same parent)
- `**attributes`: Additional merge node parameters

**Returns:** `ZNode` for the zmerge node

**Raises:** `ValueError` if no inputs provided or inputs have different parents

**Examples:**
```python
# Using zcontext for merge operations
with zcontext(znode("/obj", "geo")) as ctx:
    # Merge two geometry nodes
    box = ctx.node("box")
    sphere = ctx.node("sphere")
    merged = ctx.merge(box, sphere)

    # Merge with parameters
    merged = ctx.merge(box, sphere, tol=0.01)

    # Merge multiple inputs by name
    merged = ctx.merge("box", "sphere", "tube")
```

## Type Safety

Zabob-Houdini provides full type safety through the `as_type` parameter in `ZNode.create()` methods:

```python
# Default behavior - returns hou.Node
generic_node = znode("/obj", "geo").create()

# Type narrowing for better IntelliSense and type checking
obj_node = znode("/obj", "geo").create(as_type=hou.ObjNode)
sop_node = znode(obj_node, "box").create(as_type=hou.SopNode)
chop_node = znode("/ch", "constant").create(as_type=hou.ChopNode)
rop_node = znode("/out", "geometry").create(as_type=hou.RopNode)

# Now you get proper method completion and type checking
geometry = sop_node.geometry()  # hou.SopNode.geometry() available
children = obj_node.children()  # hou.ObjNode.children() available
```

**Benefits of Type Narrowing:**
- **IntelliSense**: Get accurate method and property suggestions
- **Type Checking**: Catch type errors at development time with mypy/pylsp
- **Runtime Safety**: Ensures the created node matches expected type
- **Documentation**: Makes code intent clearer for maintainers

**Note:** The `as_type` parameter is only available on `ZNode.create()`. ZChain creation via `ZChain.create()` returns a tuple of `ZNode` objects without type narrowing.

## Context Management

### `zcontext()`

Creates a ZContext for organizing nodes under a specific parent.

```python
def zcontext(parent: NodeParent) -> ZContext
```

**Parameters:**
- `parent`: Parent node - can be a path string, `ZNode`, or `hou.Node`

**Returns:** A `ZContext` manager object for organizing nodes

**Examples:**
```python
# Using with ZNode
with zcontext(znode("/obj", "geo", "container")) as ctx:
    box = ctx.node("box", "my_box")

# Using with path string (parent must exist).
with zcontext("/obj") as ctx:
    geo1 = ctx.node("geo", "geometry1")
    geo2 = ctx.node("geo", "geometry2")
```

### Context Objects

The `zcontext()` function returns a `ZContext` manager for organizing node creation under a specific parent. Context objects provide convenient methods and name-based lookup, as well as automated creation and layout.

#### Properties

```python
@property
def parent(self) -> ZNode
    """Get the parent node for this `ZContext`."""
```

#### Methods

```python
def node(self, node_type: str, name: str | None = None, **attributes: Any) -> ZNode
    """
    Create a node under this context's parent.

    Args:
        node_type: Houdini node type name
        name: Optional node name (auto-generated if None)
        _input: Input or inputs to this node.
          - None
          - A node, or name of a node
          - a (node, index) tuple, referencing a specific output of another node.
          - A sequence of zero or more of the above.
        _display: flag indicating this node should be displayed
        _render: flag indicating this node should be rendered.
        **attributes: Node parameter values. All keyword arguments not starting with _ are interpreted as the names of Houdini Parms to be set.

    Returns:
        ZNode that will be created under the ZContext parent

    Note:
        If the node is named, it will be registered for lookup via ctx[name]
    """

def chain(self, *, _input: InputNode | Sequence[InputNode] | None = None, **attributes: Any) -> ZChainBuilder
    """
    Create a ZChainBuilder context manager for building chains.

    Args:
        _input: Optional input node(s) to connect to the first node in the chain
        **attributes: Additional attributes (currently unused, for future compatibility)

    Returns:
        ZChainBuilder context manager for building chains

    Note:
        - Always returns ZChainBuilder context manager
        - Use ZChainBuilder.node() method to add nodes to the chain
        - Named nodes are automatically registered with the context
    """

def merge(self, *inputs: ZNode | str, name: str | None = None, **attributes: Any) -> ZNode
    """
    Create a merge node. You may specify other nodes in this context by name, if a name was specified.

    Args:
        *input8: ZNode objects or string names (looked up in context)
        _name: Optional name for merge node
        **attributes: Additional merge parameters

    Returns:
        ZNode for the merge node

    Note:
        - String arguments are looked up as registered node names
        - External ZNode objects are registered automatically if named
    """

def __getitem__(self, name: str) -> ZNode
    """
    Look up a registered ZNode by name.

    Args:
        name: Node name to look up

    Returns:
        ZNode that was registered with this name

    Raises:
        KeyError: If no ZNode with this name is registered
    """
```

#### Context Manager Protocol

```python
def __enter__(self)
    """Enter context manager - returns self."""

def __exit__(self, exc_type, exc_val, exc_tb) -> None
    """
    Exit context manager with automatic node creation and layout.

    This method automatically:
    1. Applies bidirectional layout to all registered nodes
    2. Creates all nodes in the Houdini scene
    3. Detects and creates sink nodes for outputs

    The layout algorithm uses a two-pass approach:
    - Upward pass: Calculate space requirements for each layer
    - Downward pass: Position nodes optimally within allocated space
    - Cycles left over are placed with an arbitrary node placed at the top.
    """
```

## Classes

### ZNode

Represents a single Houdini node definition.

#### Properties

```python
@property
def parent(self) -> ZNode
    """Get the parent ZNode."""

@property
def path(self) -> str
    """Get the expected path of the ZNode."""

@property
def inputs(self) -> Inputs
    """Get resolved input connections."""

@property
def first(self) -> ZNode
    """Return self (for consistency with ZChain)."""

@property
def last(self) -> ZNode
    """Return self (for consistency with ZChain)."""
```

#### Methods

```python
def create(self, as_type: type[T] = hou.Node) -> T
    """
    Create the actual Houdini node with optional type narrowing for type safety.

    Args:
        as_type: Expected node type for type narrowing. Must be a subtype of hou.Node.
        Provides better type checking and IntelliSense
                and type checking. Common types:
                - hou.Node (default): Generic node
                - hou.SopNode: Surface operator nodes
                - hou.ObjNode: Object nodes
                - hou.ChopNode: Channel operator nodes
                - hou.RopNode: Render operator nodes

    Returns:
        The created Houdini node, cached for subsequent calls. Type matches as_type.

    Example:
        # Generic node (hou.Node)
        node_generic = my_node.create()

        # Type-safe SOP node access
        sop_node = my_sop.create(as_type=hou.SopNode)
        sop_node.geometry()  # This method is available with proper typing

        # Type-safe OBJ node access
        obj_node = my_geo.create(as_type=hou.ObjNode)
        obj_node.children()  # ObjNode-specific methods available
    """

def copy(self,
         _inputs: InputNodes = (),
         _chain: ZChain | None = None,
         *,
         name: str | None = None,
         attributes: dict[str, Any] | None = None,
         _display: bool | None = None,
         _render: bool | None = None) -> ZNode
    """
    Create a copy with optional modifications to inputs, attributes, and properties.

    Args:
        _inputs: New input connections (merged with existing inputs)
        _chain: ZChain reference for the copied node
        name: New name for the node (preserves original if None)
        attributes: Additional/override attributes (merged with existing)
        _display: Override display flag (preserves original if None)
        _render: Override render flag (preserves original if None)

    Returns:
        New ZNode with merged properties and modifications applied

    Examples:
        # Copy with additional attributes
        modified = box.copy(divisions=4, sizex=3)

        # Copy with new name and display flags
        renamed = box.copy(name="new_box", _display=True, _render=True)

        # Copy with new inputs and comprehensive changes
        complex = box.copy(
            _inputs=[sphere],
            name="complex_box",
            detail=2,
            _display=True
        )
    """
```

### ZChain

Represents a sequence of connected nodes.

#### Properties

```python
@property
def parent(self) -> ZNode
    """Get the parent of the first node in the chain."""

@property
def inputs(self) -> Inputs
    """Get the inputs of the first node in the chain."""

@property
def first(self) -> ZNode
    """Get the first node in the chain."""

@property
def last(self) -> ZNode
    """Get the last node in the chain."""
```

#### Methods

```python
def create(self) -> tuple[ZNode, ...]
    """
    Create all nodes in the chain and connect them in sequence.

    Returns:
        Tuple of ZNode objects representing the created nodes
    """

def copy(self, *copy_params: ChainCopyParam, _inputs: InputNodes = ()) -> 'ZChain'
    """
    Create a copy of this chain with optional node reordering and insertion.

    Args:
        *copy_params: Parameters specifying nodes to copy:
                     - int: Index of existing node to copy
                     - str: Name of existing node to copy
                     - ZNode: New node to insert at this position
                     If empty, copies all nodes in original order.
        _inputs: New input connections for the first node in the copied chain

    Returns:
        New ZChain with copied NodeInstances in the specified order

    Examples:
        # Copy entire chain (same as original order)
        copy1 = chain.copy()

        # Reverse the chain order
        reversed_chain = chain.copy(3, 2, 1, 0)  # For 4-node chain

        # Copy by index or name
        by_name = chain[]"box"].copy()"sphere")    # Copy by name only

        # Insert new nodes
        new_node = node(geo, "noise")

        # Duplicate and reorder
        reordered = chain.copy(2, 0, 2, 1)       # [third, first, third, second]

        # Copy with new inputs
        with_inputs = chain.copy(1, 0, _inputs=[input_node])
    """

def __len__(self) -> int
    """Get the number of nodes in the chain."""

def __getitem__(self, index: int) -> ZNode
    """Get a node by index."""
```

#### Convenience Methods

```python
def first_node(self) -> hou.Node
    """Get the created hou.Node for the first node in the chain."""

def last_node(self) -> hou.Node
    """Get the created hou.Node for the last node in the chain."""
```

### ZChainBuilder

Context manager for building chains with conditional logic and automatic registration.

#### Overview

`ZChainBuilder` is returned by `ctx.chain()`. It provides a context manager interface for building chains incrementally with conditional node inclusion.

**Key Features:**
- **Context Manager**: Use with `with` statement for automatic registration
- **Conditional Logic**: Add nodes based on runtime conditions
- **Automatic Registration**: Nodes are registered with context on `__exit__`

#### Usage Pattern

```python
with ctx.chain(_input=source) as builder:
    builder.node("xform", "transform")
    if some_condition:
        builder.node("subdivide", "subdivide")  # Only added if condition is true
    builder.node("color", "colorize")

# ZChain is automatically registered and can be used in merges
final = ctx.merge(builder, other_chain, name="final")
```

#### Properties

```python
@property
chain."""

@property
def first(self) -> ZNode
    """Get the first node in the chain."""

@property
def last(self) -> ZNode
    """Get the last node in the chain."""
```

#### Methods

```python
def node(self, node_type: str, name: str | None = None, **attributes: Any) -> ZNode
    """
    Add a node to the chain being built.

    Args:
        node_type: Houdini node type name
        name: Optional node name (auto-generated if None)
        **attributes: Node parameter values

    Returns:
        ZNode that was added to the chain

    Note:
        The new node is automatically connected to the previous node in the chain
    """

def __enter__(self) -> ZChainBuilder
    """Enter context manager - returns self."""

def __exit__(self, exc_type, exc_val, exc_tb) -> None
    """
    Exit context manager and register the built chain with the context.

    This method converts the ZChainBuilder into a ZChain and registers it
    for dependency tracking and automatic creation.
    """
```

## Type System

### Type Aliases

```python
NodeParent = str | ZNode | hou.Node
"""
A parent node specification.

When specifying a parent node, a ZNode, hou.Node, or a string path to an existing node can be supplied.

If not a ZNode, it will be wrapped in a ZNode.
"""

NodeType = str
"""A Houdini node type name."""

InputNodeSpec = ZNode | ZChain | hou.Node | str
"""A node that can be used as input."""

InputNode = tuple[InputNodeSpec, int] | InputNodeSpec | None
"""An input connection specification with optional output index."""

InputNodes = Sequence[InputNode]
"""Multiple input connections."""

ChainCopyParam = int | str | ZNode
"""
A parameter for ZChain.copy() reordering.

- int: Index of existing node to copy
- str: Name of existing node to copy
- ZNode: New node to insert at this position
"""
```

### Input Connection Patterns

#### Single Input
```python
# Direct connection (uses output 0)
node(geo, "xform", _input=source_node)

# Specific output index
znode(geo, "xform", _input=(multi_output_node, 1))
```

#### Multiple Inputs
```python
# Merge two sources
znode(geo, "merge", _input=[source1, source2])

# Sparse inputs (None for unused inputs)
znode(geo, "switch", _input=[source1, None, source3])

# Mixed with output indices
znode(geo, "merge", _input=[
    source1,                    # output 0
    (multi_output_node, 1),    # output 1
    None,                       # skip input 2
    source4                     # output 0
])
```

#### ZChain as Input
```python
# Use entire chain - connects to last node
processing_chain = zchain(
    znode(geo, "box"),
    znode(geo, "subdivide")
)
final_node = znode(geo, "xform", _input=processing_chain)
```

## Advanced Patterns

### Enhanced Copy Operations

The `.copy()` method supports comprehensive modifications for creating variations of nodes:

```python
# Base znode with some properties
base_box = znode(geo, "box", name="base", sizex=1, sizey=1, _display=False)

# Copy with attribute modifications (merged with existing)
larger_box = base_box.copy(
    sizex=2, sizez=3, # sizex overridden, sizez added, sizey preserved
    name="larger_box"
)

# Copy with display flags
display_box = base_box.copy(
    _display=True,
    _render=True,
    name="display_version"
)

# Copy with new inputs and comprehensive changes
source = znode(geo, "sphere", name="input_source")
complex_box = base_box.copy(
    _inputs=[source],
    name="connected_box",
    divisions=4, # Added attribute
    sizey=3, # Modified attribute
    _display=True,
    _render=False
)

# Attribute merging behavior
original_attrs = dict(base_box.attributes)        # {"sizex": 1, "sizey": 1}
modified_attrs = dict(larger_box.attributes)      # {"sizex": 2, "sizey": 1, "sizez": 3}
```

**Key Benefits:**
- **Attribute Merging**: New attributes are added, existing ones can be overridden
- **Selective Updates**: Only specify parameters you want to change (`None` preserves originals)
- **Immutability**: Original nodes remain unchanged, copies are independent
- **Type Safety**: All copy operations maintain proper typing and validation

### ZChain Reordering and Insertion

ZChain `.copy()` supports flexible znode sequence manipulation with indices, names, and insertions:

```python
# Original processing chain
original = zchain(
    znode(geo, "box", name="input"),
    znode(geo, "subdivide", name="detail"),
    znode(geo, "noise", name="distort"),
    znode(geo, "smooth", name="cleanup")
)

# Reverse the entire processing order
reversed_chain = original.copy(3, 2, 1, 0)
# Result: [cleanup, distort, detail, input]

# Copy by name instead of index
by_name = original.copy("cleanup", "input", "detail")
# Result: [cleanup, input, detail]

# Mix indices and names
mixed = original.copy(0, "distort", 3)
# Result: [input, distort, cleanup]

# Insert new processing steps
blur = znode(geo, "blur", name="blur")
enhanced = original.copy("input", "detail", blur, "cleanup")
# Result: [input, detail, blur, cleanup] - blur inserted before cleanup

# Duplicate steps for variations
double_detail = original.copy(0, "detail", 2, "detail", 3)
# Result: [input, detail, distort, detail, cleanup] - double detail

# Complex reordering with inputs
source = znode(geo, "sphere", name="source")
reordered = original.copy("distort", blur, "cleanup", _inputs=[source])
# Result: [distort, blur, cleanup] with sphere input
```

**Enhanced Patterns:**
- **Index Access**: `chain.copy(3, 2, 1, 0)` - numeric indices
- **Name Access**: `chain.copy("cleanup", "input")` - znode names
- **Mixed Access**: `chain.copy(0, "distort", 3)` - combine both
- **Node Insertion**: `chain.copy(0, new_node, 1)` - insert NodeInstances
- **Duplication**: `chain.copy("detail", "detail")` - repeat by name or index

### ZContext and ZChainBuilder Pattern

The recommended way to organize znode creation is using the `context()` function with automatic context management:

```python
from zabob_houdini import zcontext, znode

do_subdivide: bool = True

# Create organized znode networks with automatic layout and znode creation
with zcontext(znode("/obj", "geo", "processing")) as ctx:
    # Create source node
    source = ctx.znode("box", "input_geometry", sizex=2, sizey=2, sizez=2)

    # Use ZChainBuilder for conditional chain construction
    with ctx.chain(_input=source) as processing_path:
        processing_path.znode("xform", "scale", sx=1.5)
        if do_subdivide:
            processing_path.znode("subdivide", "smooth")

    # Build alternate paths
    with ctx.chain(_input=source) as alternate_path:
        alternate_path.znode("sphere", "alternate_input")
        alternate_path.znode("color", "colorize", color=(1, 0, 0))

    # Merge operations with automatic dependency tracking
    final = ctx.merge(processing_path, alternate_path, name="combined")

    # Access nodes by name anytime
    retrieved = ctx["input_geometry"]  # Same as source

# Context automatically applies bidirectional layout and creates all nodes
# No need to call .create() - everything is handled on context exit!
```

### Automatic Layout and Context Management

**Key Features:**
- **Automatic Node Creation**: Context exit automatically creates all registered nodes
- **Bidirectional Layout**: Upward pass allocates space, downward pass positions nodes optimally
- **Sink Detection**: Automatically identifies and creates sink nodes for outputs
- **Dependency Tracking**: Smart dependency resolution prevents conflicts and duplicates

### Nested Contexts

The `zcontext()` method on `ZContext` enables organizing related znode hierarchies for layout purposes:

```python
# Organize multiple networks with nested contexts
with zcontext("/obj") as obj_ctx:
    # Create multiple networks, each in its own logical group
    with obj_ctx.context(znode("/obj", "topnet", name="network1")) as top1:
        top1.znode("pythonscript", "task1")
        top1.znode("waitforall", "collect1")

    with obj_ctx.context(znode("/obj", "topnet", name="network2")) as top2:
        top2.znode("pythonscript", "task2")
        top2.znode("waitforall", "collect2")

# All networks are laid out together at /obj level when outer context exits
```

This pattern is useful when you want multiple related znode hierarchies to be laid out together at the parent level, while maintaining clear code organization.

### Diamond Pattern with Context
Create nodes that share a common source using context organization:

```python
with zcontext(znode("/obj", "geo", "diamond_demo")) as ctx:
    # Shared source chain
    source = ctx.chain(
        ctx.znode("box", "base_geometry"),
        ctx.znode("xform", "center")
    )

    # Two processing paths using source
    path1 = ctx.chain(
        ctx.znode("xform", "scale_up", _input=source, sx=2),
        ctx.znode("xform", "rotate_y", ry=45)
    )

    path2 = ctx.chain(
        ctx.znode("xform", "scale_down", _input=source, sx=0.5),
        ctx.znode("xform", "rotate_x", rx=30)
    )

    # Merge results using string names
    final = ctx.merge("scale_up", "scale_down", name="combined")
    output = ctx.znode("null", "OUT", _input=final, _display=True)
```

### Nested Chains
Chains can contain other chains:

```python
sub_chain = chain(
    znode(geo, "sphere"),
    znode(geo, "xform", sx=2)
)

main_chain = zchain(
    znode(geo, "box"),
    sub_chain,  # Copied and fattened into main chain
    znode(geo, "merge")
)
```

### Lazy Creation
Only create what you need:

```python
# Define entire network
network = create_complex_network()

# Create only the final output - dependencies created automatically
final_node = network.last.create()
```

## Utility Functions

### Node Wrapping

```python
def wrap_node(hnode: hou.Node | ZNode | str) -> ZNode
    """
    Wrap various znode types into ZNode.

    Args:
        hnode: Node to wrap

    Returns:
        ZNode wrapper
    """

def get_node_instance(hnode: hou.Node) -> ZNode | None
    """
    Get the original ZNode that created a hou.Node.

    Returns:
        Original ZNode or None if not found
    """
```

### Direct Node Access

```python
def hou_node(path: str) -> hou.Node
    """Get a Houdini znode by path, raising exception if not found."""
```

### Dependency Analysis

The `ZContext` class provides methods for analyzing znode dependencies and network topology. **Dependency tracking is scoped to each context** - only nodes created through the context's methods (`node()`, `chain()`, `merge()`) have their dependencies tracked.

```python
class ZContext:
    def get_dependents(self, znode: ZNode) -> list[ZNode]
        """Get list of nodes that depend on the given node within this context."""

    def get_source_nodes(self) -> list[ZNode]
        """Get nodes in this context that have no inputs (source nodes)."""

    def get_sink_nodes(self) -> list[ZNode]
        """Get nodes in this context that have no dependents (sink nodes)."""
```

**Important**: Dependency tracking only works for nodes created through the context. Nodes created with the global `znode()` function or passed in from other contexts will not have their dependencies tracked.

**Usage Example:**
```python
# Build a node network
with zcontext(znode("/obj", "geo")) as ctx:
    box = ctx.node("box", "source1")
    sphere = ctx.node("sphere", "source2")
    xform1 = ctx.node("xform", "process1", _input=box)
    xform2 = ctx.node("xform", "process2", _input=sphere)
    merge = ctx.node("merge", "combine", _input=[xform1, xform2])
    output = ctx.node("null", "output", _input=merge)

    # Create all nodes
    output.create()

    # Analyze the network structure using context methods
    sources = ctx.get_source_nodes()      # [box, sphere] - automatically uses context nodes
    sinks = ctx.get_sink_nodes()          # [output] - automatically uses context nodes

    # Check what depends on a specific znode
    box_deps = ctx.get_dependents(box)    # [xform1]
```

## Caching and Performance

### Automatic Caching
- `ZNode.create()` is cached - calling it multiple times returns the same `hou.Node`
- `ZChain.create()` is cached - calling it multiple times returns the same tuple of nodes
- Node registry tracks which `ZNode` created each `hou.Node`.
  - This can be queried with `get_node_instance()`

### Memory Management
- Uses weak references to avoid circular dependencies
- Nodes are cached by path, not object identity (due to Houdini's `hou.Node` object behavior)

### Creation Optimization
- Nodes are only created when `.create()` is called
- Dependencies are created automatically during creation
- Batch creation minimizes Houdini API calls

## Error Handling

### Common Exceptions
- `TypeError`: Invalid node types or connection specifications
- `ValueError`: Invalid parameter values or connection indices
- `RuntimeError`: Node creation failures or missing dependencies

### Validation
- Input connections are validated during creation
- Parameter types are checked when possible
- Missing parent nodes cause creation failures

## Best Practices

### Context Organization
```python
# Best practice - use context manager for organization
with zcontext(znode("/obj", "geo", "processing")) as ctx:
    # Descriptive names for important nodes
    source = ctx.node("box", "source_geometry", sizex=2, sizey=2, sizez=2)
    scaled = ctx.node("xform", "scale_2x", _input=source, sx=2, sy=2, sz=2)

    # Use string lookup in chains
    processing = ctx.chain("source_geometry", "scale_2x",
                          ctx.znode("subdivide", "smooth"))

    # Merge operations with string names
    alternate = ctx.node("sphere", "alternate_input")
    final = ctx.merge("source_geometry", "alternate_input", name="combined")
```

### Node Naming
```python
# Good - descriptive names within context
with zcontext(znode("/obj", "geo", "demo")) as ctx:
    source = ctx.node("box", "source_geometry")
    scaled = ctx.node("xform", "scale_2x", _input="source_geometry", sx=2)

# Acceptable - let system generate names
with zcontext(znode("/obj", "geo", "demo")) as ctx:
    source = ctx.node("box")
    scaled = ctx.node("xform", _input=source, sx=2)
```

### Input Management
```python
# Good - clear input specifications
znode(geo, "merge", _input=[primary_source, secondary_source])

# Good - explicit output indices when needed
znode(geo, "switch", _input=(multi_output_node, 1))

# Good - sparse inputs when some are unused
znode(geo, "switch", _input=[source1, None, source3])
```

### ZChain Organization
```python
# Best practice - use zcontext for logical groupings
with zcontext(znode("/obj", "geo", "processing")) as ctx:
    # Preprocessing steps
    preprocessing = ctx.chain(
        ctx.node("box", "input"),
        ctx.node("xform", "center"),
        ctx.node("subdivide", "detail", iterations=1)
    )

    # Main processing using string lookup
    processing = ctx.chain(
        "center",  # Reference by name
        ctx.znode("xform", "scale", sx=2),
        ctx.znode("xform", "rotate", ry=45)
    )

    # Clear final output
    output = ctx.node("null", "OUT", _input="rotate", _display=True, _render=True)
```

### Creation Patterns
```python
# Best practice - organize with zcontext, create selectively
def create_processing_network():
    with zcontext(znode("/obj", "geo", "my_geometry")) as ctx:
        # Define entire network
        final_chain = ctx.chain(
            ctx.node("box", "input"),
            ctx.node("xform", "process"),
            ctx.node("null", "output", _display=True)
        )
        return ctx.parent, final_chain

# Only create what's needed - dependencies propagate automatically
geo_container, final_chain = create_processing_network()
final_chain.create()  # Creates entire dependency tree
```

## Integration with Existing Code

### Wrapping Existing Nodes
```python
# Wrap existing Houdini nodes
existing_geo = hou.node("/obj/geo1")
wrapped = wrap_node(existing_geo)

# Use in new network
enhanced = znode(existing_geo, "xform", _input=wrapped, tx=5)
```

### Mixed Workflows
```python
# Create some nodes with Zabob
zabob_chain = zchain(
    znode(geo, "box"),
    znode(geo, "xform", tx=2)
)

# Create with traditional Houdini API
traditional_node = geo.createNode("sphere")

# Combine them
combined = znode(geo, "merge", _input=[zabob_chain, traditional_node])
```

## Debugging and Inspection

### Path Information
```python
# Get expected paths before creation
print(f"Node will be created at: {my_node.path}")

# Check parent relationships
print(f"Parent: {my_node.parent.path}")
```

### Input Inspection
```python
# Examine resolved inputs
for i, connection in enumerate(my_node.inputs):
    if connection:
        node_instance, output_idx = connection
        print(f"Input {i}: {node_instance.path} output {output_idx}")
```

### Registry Queries
```python
# Find original ZNode from hou.Node
original = get_node_instance(some_hou_node)
if original:
    print(f"Originally created by: {original}")
```
