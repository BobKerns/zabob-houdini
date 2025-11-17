![Zabob Banner](docs/images/zabob-banner.jpg)
# Zabob-Houdini API Documentation

## Overview

Zabob-Houdini provides a Python API for creating Houdini node graphs programmatically. The API is designed to be declarative - you define nodes and their connections, then create them all at once.

## Core Concepts

### NodeInstance

A `NodeInstance` represents a single Houdini node that can be created. It stores the node definition including its parent, type, parameters, and connections.

### Chain

A `Chain` represents a sequence of nodes that are automatically connected in order. Chains can be nested and combined to create complex node networks.

### Lazy Creation

Nodes and chains are defined first, then created later via the `.create()` method. This allows for:
- Forward references (nodes can reference other nodes not yet defined)
- Circular dependencies (with proper care)
- Batch creation for better performance

## Main Functions

### `node()`

Creates a single node definition.

```python
def node(
    parent: NodeParent,
    node_type: NodeType,
    name: str | None = None,
    _input: 'InputNode | list[InputNode] | None' = None,
    _node: 'hou.Node | None' = None,
    _display: bool = False,
    _render: bool = False,
    **attributes: Any
) -> NodeInstance
```

**Parameters:**
- `parent`: Parent node - can be a path string (e.g., `"/obj"`), `NodeInstance`, or `hou.Node`
- `node_type`: Houdini node type name (e.g., `"box"`, `"xform"`, `"merge"`)
- `name`: Optional node name. If not provided, auto-generated based on type
- `_input`: Input connections - single node/chain, list of nodes/chains, or `None`
- `_node`: Optional existing `hou.Node` to wrap (for integration with existing code)
- `_display`: Set display flag when node is created (for SOP nodes)
- `_render`: Set render flag when node is created (for SOP nodes)
- `**attributes`: Node parameter values as keyword arguments

**Returns:** `NodeInstance` object that can be created later

**Examples:**
```python
# Using context manager for organization
with context(node("/obj", "geo")) as ctx:
    # Simple geometry node
    box = ctx.node("box", sizex=2, sizey=2, sizez=2)

    # Transform with input
    xform = ctx.node("xform", "my_transform", _input=box, tx=5)

    # Node with display flag
    output = ctx.node("null", "OUT", _input=xform, _display=True)
```

### `chain()`

Creates a chain of nodes that are automatically connected in sequence.

```python
def chain(
    *nodes: ChainableNode,
    **attributes: Any
) -> Chain
```

**Parameters:**
- `*nodes`: Sequence of `NodeInstance`, `Chain`, or `hou.Node` objects
- `**attributes`: Reserved for future use

**Returns:** `Chain` object that can be created later

**Examples:**
```python
# Using context for chain creation
with context(node("/obj", "geo")) as ctx:
    # Simple chain
    processing = ctx.chain(
        ctx.node("box"),
        ctx.node("xform", tx=2),
        ctx.node("subdivide", iterations=2)
    )

    # Chain with external input
    chain_with_input = ctx.chain(
        ctx.node("xform", "scale_up", _input=some_input, sx=2, sy=2, sz=2),
        ctx.node("xform", "translate", tx=5)
    )
```

### `merge()`

Creates a merge node with multiple inputs. All inputs must have the same parent.

```python
def merge(*inputs: NodeInstance, **attributes: Any) -> NodeInstance
```

**Parameters:**
- `*inputs`: NodeInstance objects to merge (must have same parent)
- `**attributes`: Additional merge node parameters

**Returns:** `NodeInstance` for the merge node

**Raises:** `ValueError` if no inputs provided or inputs have different parents

**Examples:**
```python
# Using context for merge operations
with context(node("/obj", "geo")) as ctx:
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

Zabob-Houdini provides full type safety through the `as_type` parameter in `NodeInstance.create()` methods:

```python
# Default behavior - returns hou.Node
generic_node = node("/obj", "geo").create()

# Type narrowing for better IntelliSense and type checking
obj_node = node("/obj", "geo").create(as_type=hou.ObjNode)
sop_node = node(obj_node, "box").create(as_type=hou.SopNode)
chop_node = node("/ch", "constant").create(as_type=hou.ChopNode)
rop_node = node("/out", "geometry").create(as_type=hou.RopNode)

# Now you get proper method completion and type checking
geometry = sop_node.geometry()  # hou.SopNode.geometry() available
children = obj_node.children()  # hou.ObjNode.children() available
```

**Benefits of Type Narrowing:**
- **IntelliSense**: Get accurate method and property suggestions
- **Type Checking**: Catch type errors at development time with mypy/pylsp
- **Runtime Safety**: Ensures the created node matches expected type
- **Documentation**: Makes code intent clearer for maintainers

**Note:** The `as_type` parameter is only available on `NodeInstance.create()`. Chain creation via `Chain.create()` returns a tuple of `NodeInstance` objects without type narrowing.

## Context Management

### `context()`

Creates a NodeContext for organizing nodes under a specific parent.

```python
def context(parent: NodeParent) -> NodeContext
```

**Parameters:**
- `parent`: Parent node - can be a path string, `NodeInstance`, or `hou.Node`

**Returns:** A context manager object for organizing nodes

**Examples:**
```python
# Using with NodeInstance
with context(node("/obj", "geo", "container")) as ctx:
    box = ctx.node("box", "my_box")

# Using with path string
with context("/obj") as ctx:
    geo1 = ctx.node("geo", "geometry1")
    geo2 = ctx.node("geo", "geometry2")
```

### Context Objects

The `context()` function returns a context manager for organizing node creation under a specific parent. Context objects provide convenient methods and name-based lookup.

#### Properties

```python
@property
def parent(self) -> NodeInstance
    """Get the parent node for this context."""
```

#### Methods

```python
def node(self, node_type: str, name: str | None = None, **attributes: Any) -> NodeInstance
    """
    Create a node under this context's parent.

    Args:
        node_type: Houdini node type name
        name: Optional node name (auto-generated if None)
        **attributes: Node parameter values

    Returns:
        NodeInstance that will be created under the context parent

    Note:
        If the node is named, it will be registered for lookup via ctx[name]
    """

def chain(self, *nodes: ChainableNode | str, **attributes: Any) -> Chain
    """
    Create a chain with string argument lookup in this context.

    Args:
        *nodes: NodeInstance, Chain, or string names to chain together
        **attributes: Reserved for future use

    Returns:
        Chain object

    Note:
        - String arguments are looked up as registered node names
        - Named nodes from external NodeInstances are registered automatically
    """

def merge(self, *inputs: NodeInstance | str, name: str | None = None, **attributes: Any) -> NodeInstance
    """
    Create a merge node with string argument lookup in this context.

    Args:
        *inputs: NodeInstance objects or string names (looked up in context)
        name: Optional name for merge node
        **attributes: Additional merge parameters

    Returns:
        NodeInstance for the merge node

    Note:
        - String arguments are looked up as registered node names
        - External NodeInstance objects are registered automatically if named
    """

def __getitem__(self, name: str) -> NodeInstance
    """
    Look up a registered node by name.

    Args:
        name: Node name to look up

    Returns:
        NodeInstance that was registered with this name

    Raises:
        KeyError: If no node with this name is registered
    """
```

#### Context Manager Protocol

```python
def __enter__(self)
    """Enter context manager - returns self."""

def __exit__(self, exc_type, exc_val, exc_tb) -> None
    """Exit context manager - no special cleanup needed."""
```

## Classes

### NodeInstance

Represents a single Houdini node definition.

#### Properties

```python
@property
def parent(self) -> NodeInstance
    """Get the parent node."""

@property
def path(self) -> str
    """Get the expected path of the node."""

@property
def inputs(self) -> Inputs
    """Get resolved input connections."""

@property
def first(self) -> NodeInstance
    """Return self (for consistency with Chain)."""

@property
def last(self) -> NodeInstance
    """Return self (for consistency with Chain)."""
```

#### Methods

```python
def create(self, as_type: type[T] = hou.Node) -> T
    """
    Create the actual Houdini node with optional type narrowing for type safety.

    Args:
        as_type: Expected node type for type narrowing. Must be a subtype of hou.Node.
        Provides better IntelliSense
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
         _chain: 'Chain | None' = None,
         *,
         name: str | None = None,
         attributes: dict[str, Any] | None = None,
         _display: bool | None = None,
         _render: bool | None = None) -> 'NodeInstance'
    """
    Create a copy with optional modifications to inputs, attributes, and properties.

    Args:
        _inputs: New input connections (merged with existing inputs)
        _chain: Chain reference for the copied node
        name: New name for the node (preserves original if None)
        attributes: Additional/override attributes (merged with existing)
        _display: Override display flag (preserves original if None)
        _render: Override render flag (preserves original if None)

    Returns:
        New NodeInstance with merged properties and modifications applied

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

### Chain

Represents a sequence of connected nodes.

#### Properties

```python
@property
def parent(self) -> NodeInstance
    """Get the parent of the first node in the chain."""

@property
def inputs(self) -> Inputs
    """Get the inputs of the first node in the chain."""

@property
def first(self) -> NodeInstance
    """Get the first node in the chain."""

@property
def last(self) -> NodeInstance
    """Get the last node in the chain."""
```

#### Methods

```python
def create(self) -> tuple[NodeInstance, ...]
    """
    Create all nodes in the chain and connect them in sequence.

    Returns:
        Tuple of NodeInstance objects representing the created nodes
    """

def copy(self, *copy_params: ChainCopyParam, _inputs: InputNodes = ()) -> 'Chain'
    """
    Create a copy of this chain with optional node reordering and insertion.

    Args:
        *copy_params: Parameters specifying nodes to copy:
                     - int: Index of existing node to copy
                     - str: Name of existing node to copy
                     - NodeInstance: New node to insert at this position
                     If empty, copies all nodes in original order.
        _inputs: New input connections for the first node in the copied chain

    Returns:
        New Chain with copied NodeInstances in the specified order

    Examples:
        # Copy entire chain (same as original order)
        copy1 = chain.copy()

        # Reverse the chain order
        reversed_chain = chain.copy(3, 2, 1, 0)  # For 4-node chain

        # Copy by index or name
        partial = chain.copy(0, "transform")     # Mix index and name
        by_name = chain.copy("box", "sphere")    # Copy by name only

        # Insert new nodes
        new_node = node(geo, "noise")
        enhanced = chain.copy(0, new_node, 1)    # Insert noise between nodes 0 and 1

        # Duplicate and reorder
        reordered = chain.copy(2, 0, 2, 1)       # [third, first, third, second]

        # Copy with new inputs
        with_inputs = chain.copy(1, 0, _inputs=[input_node])
    """

def __len__(self) -> int
    """Get the number of nodes in the chain."""

def __getitem__(self, index: int) -> NodeInstance
    """Get a node by index."""
```

#### Convenience Methods

```python
def first_node(self) -> hou.Node
    """Get the created hou.Node for the first node in the chain."""

def last_node(self) -> hou.Node
    """Get the created hou.Node for the last node in the chain."""
```

## Type System

### Type Aliases

```python
NodeParent = str | NodeInstance | hou.Node
"""
A parent node specification.

When specifying a parent node, a NodeInstance, hou.Node, or a string path to an existing node can be supplied.

If not a NodeInstance, it will be wrapped in a NodeInstance.
"""

NodeType = str
"""A Houdini node type name."""

InputNodeSpec = NodeInstance | Chain | hou.Node | str
"""A node that can be used as input."""

InputNode = tuple[InputNodeSpec, int] | InputNodeSpec | None
"""An input connection specification with optional output index."""

InputNodes = Sequence[InputNode]
"""Multiple input connections."""

ChainCopyParam = int | str | NodeInstance
"""
A parameter for Chain.copy() reordering.

- int: Index of existing node to copy
- str: Name of existing node to copy
- NodeInstance: New node to insert at this position
"""
```

### Input Connection Patterns

#### Single Input
```python
# Direct connection (uses output 0)
node(geo, "xform", _input=source_node)

# Specific output index
node(geo, "xform", _input=(multi_output_node, 1))
```

#### Multiple Inputs
```python
# Merge two sources
node(geo, "merge", _input=[source1, source2])

# Sparse inputs (None for unused inputs)
node(geo, "switch", _input=[source1, None, source3])

# Mixed with output indices
node(geo, "merge", _input=[
    source1,                    # output 0
    (multi_output_node, 1),    # output 1
    None,                       # skip input 2
    source4                     # output 0
])
```

#### Chain as Input
```python
# Use entire chain - connects to last node
processing_chain = chain(
    node(geo, "box"),
    node(geo, "subdivide")
)
final_node = node(geo, "xform", _input=processing_chain)
```

## Advanced Patterns

### Enhanced Copy Operations

The `.copy()` method supports comprehensive modifications for creating variations of nodes:

```python
# Base node with some properties
base_box = node(geo, "box", name="base", sizex=1, sizey=1, _display=False)

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
source = node(geo, "sphere", name="input_source")
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

### Chain Reordering and Insertion

Chain `.copy()` supports flexible node sequence manipulation with indices, names, and insertions:

```python
# Original processing chain
original = chain(
    node(geo, "box", name="input"),
    node(geo, "subdivide", name="detail"),
    node(geo, "noise", name="distort"),
    node(geo, "smooth", name="cleanup")
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
blur = node(geo, "blur", name="blur")
enhanced = original.copy("input", "detail", blur, "cleanup")
# Result: [input, detail, blur, cleanup] - blur inserted before cleanup

# Duplicate steps for variations
double_detail = original.copy(0, "detail", 2, "detail", 3)
# Result: [input, detail, distort, detail, cleanup] - double detail

# Complex reordering with inputs
source = node(geo, "sphere", name="source")
reordered = original.copy("distort", blur, "cleanup", _inputs=[source])
# Result: [distort, blur, cleanup] with sphere input
```

**Enhanced Patterns:**
- **Index Access**: `chain.copy(3, 2, 1, 0)` - numeric indices
- **Name Access**: `chain.copy("cleanup", "input")` - node names
- **Mixed Access**: `chain.copy(0, "distort", 3)` - combine both
- **Node Insertion**: `chain.copy(0, new_node, 1)` - insert NodeInstances
- **Duplication**: `chain.copy("detail", "detail")` - repeat by name or index

### NodeContext and Context Manager Pattern

The recommended way to organize node creation is using the `context()` function with a context manager:

```python
from zabob_houdini import context, node

# Create organized node networks with context manager
with context(node("/obj", "geo", "processing")) as ctx:
    # Create nodes using ctx.node() - automatically sets correct parent
    source = ctx.node("box", "input_geometry", sizex=2, sizey=2, sizez=2)

    # Use string names for clean chain definitions
    processing_chain = ctx.chain("input_geometry",
                                ctx.node("xform", "scale", sx=1.5),
                                ctx.node("subdivide", "smooth"))

    # Merge operations with string lookup
    alternate = ctx.node("sphere", "alternate_input")
    final = ctx.merge("input_geometry", "alternate_input", name="combined")

    # Access nodes by name anytime
    retrieved = ctx["input_geometry"]  # Same as source

# Context automatically handles parent relationships and name registration
```

### Diamond Pattern with Context
Create nodes that share a common source using context organization:

```python
with context(node("/obj", "geo", "diamond_demo")) as ctx:
    # Shared source chain
    source = ctx.chain(
        ctx.node("box", "base_geometry"),
        ctx.node("xform", "center")
    )

    # Two processing paths using source
    path1 = ctx.chain(
        ctx.node("xform", "scale_up", _input=source, sx=2),
        ctx.node("xform", "rotate_y", ry=45)
    )

    path2 = ctx.chain(
        ctx.node("xform", "scale_down", _input=source, sx=0.5),
        ctx.node("xform", "rotate_x", rx=30)
    )

    # Merge results using string names
    final = ctx.merge("scale_up", "scale_down", name="combined")
    output = ctx.node("null", "OUT", _input=final, _display=True)
```

### Nested Chains
Chains can contain other chains:

```python
sub_chain = chain(
    node(geo, "sphere"),
    node(geo, "xform", sx=2)
)

main_chain = chain(
    node(geo, "box"),
    sub_chain,  # Flattened into main chain
    node(geo, "merge")
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
def wrap_node(hnode: hou.Node | NodeInstance | str) -> NodeInstance
    """
    Wrap various node types into NodeInstance.

    Args:
        hnode: Node to wrap

    Returns:
        NodeInstance wrapper
    """

def get_node_instance(hnode: hou.Node) -> NodeInstance | None
    """
    Get the original NodeInstance that created a hou.Node.

    Returns:
        Original NodeInstance or None if not found
    """
```

### Direct Node Access

```python
def hou_node(path: str) -> hou.Node
    """Get a Houdini node by path, raising exception if not found."""
```

### Dependency Analysis

The `NodeContext` class provides methods for analyzing node dependencies and network topology. **Dependency tracking is scoped to each context** - only nodes created through the context's methods (`node()`, `chain()`, `merge()`) have their dependencies tracked.

```python
class NodeContext:
    def get_dependents(self, node: NodeInstance) -> list[NodeInstance]
        """Get list of nodes that depend on the given node within this context."""

    def get_source_nodes(self) -> list[NodeInstance]
        """Get nodes in this context that have no inputs (source nodes)."""

    def get_sink_nodes(self) -> list[NodeInstance]
        """Get nodes in this context that have no dependents (sink nodes)."""
```

**Important**: Dependency tracking only works for nodes created through the context. Nodes created with the global `node()` function or passed in from other contexts will not have their dependencies tracked.

**Usage Example:**
```python
# Build a node network
with context(node("/obj", "geo")) as ctx:
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

    # Check what depends on a specific node
    box_deps = ctx.get_dependents(box)    # [xform1]
```

## Caching and Performance

### Automatic Caching
- `NodeInstance.create()` is cached - calling it multiple times returns the same `hou.Node`
- `Chain.create()` is cached - calling it multiple times returns the same tuple of nodes
- Node registry tracks which `NodeInstance` created each `hou.Node`

### Memory Management
- Uses weak references to avoid circular dependencies
- Nodes are cached by path, not object identity (due to Houdini's node object behavior)

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
with context(node("/obj", "geo", "processing")) as ctx:
    # Descriptive names for important nodes
    source = ctx.node("box", "source_geometry", sizex=2, sizey=2, sizez=2)
    scaled = ctx.node("xform", "scale_2x", _input=source, sx=2, sy=2, sz=2)

    # Use string lookup in chains
    processing = ctx.chain("source_geometry", "scale_2x",
                          ctx.node("subdivide", "smooth"))

    # Merge operations with string names
    alternate = ctx.node("sphere", "alternate_input")
    final = ctx.merge("source_geometry", "alternate_input", name="combined")
```

### Node Naming
```python
# Good - descriptive names within context
with context(node("/obj", "geo", "demo")) as ctx:
    source = ctx.node("box", "source_geometry")
    scaled = ctx.node("xform", "scale_2x", _input="source_geometry", sx=2)

# Acceptable - let system generate names
with context(node("/obj", "geo", "demo")) as ctx:
    source = ctx.node("box")
    scaled = ctx.node("xform", _input=source, sx=2)
```

### Input Management
```python
# Good - clear input specifications
node(geo, "merge", _input=[primary_source, secondary_source])

# Good - explicit output indices when needed
node(geo, "switch", _input=(multi_output_node, 1))

# Good - sparse inputs when some are unused
node(geo, "switch", _input=[source1, None, source3])
```

### Chain Organization
```python
# Best practice - use context for logical groupings
with context(node("/obj", "geo", "processing")) as ctx:
    # Preprocessing steps
    preprocessing = ctx.chain(
        ctx.node("box", "input"),
        ctx.node("xform", "center"),
        ctx.node("subdivide", "detail", iterations=1)
    )

    # Main processing using string lookup
    processing = ctx.chain(
        "center",  # Reference by name
        ctx.node("xform", "scale", sx=2),
        ctx.node("xform", "rotate", ry=45)
    )

    # Clear final output
    output = ctx.node("null", "OUT", _input="rotate", _display=True, _render=True)
```

### Creation Patterns
```python
# Best practice - organize with context, create selectively
def create_processing_network():
    with context(node("/obj", "geo", "my_geometry")) as ctx:
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
enhanced = node(existing_geo, "xform", _input=wrapped, tx=5)
```

### Mixed Workflows
```python
# Create some nodes with Zabob
zabob_chain = chain(
    node(geo, "box"),
    node(geo, "xform", tx=2)
)

# Create with traditional Houdini API
traditional_node = geo.createNode("sphere")

# Combine them
combined = node(geo, "merge", _input=[zabob_chain, traditional_node])
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
# Find original NodeInstance from hou.Node
original = get_node_instance(some_hou_node)
if original:
    print(f"Originally created by: {original}")
```
