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
# Simple geometry node
box = node("/obj/geo1", "box", sizex=2, sizey=2, sizez=2)

# Transform with input
xform = node("/obj/geo1", "xform", "my_transform", _input=box, tx=5)

# Node with display flag
output = node("/obj/geo1", "null", "OUT", _input=xform, _display=True)
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
# Simple chain
processing = chain(
    node(geo, "box"),
    node(geo, "xform", tx=2),
    node(geo, "subdivide", iterations=2)
)

# Chain with external input
chain_with_input = chain(
    node(geo, "xform", "scale_up", _input=some_input, sx=2, sy=2, sz=2),
    node(geo, "xform", "translate", tx=5)
)
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
        modified = box.copy(attributes={"divisions": 4, "sizex": 3})

        # Copy with new name and display flags
        renamed = box.copy(name="new_box", _display=True, _render=True)

        # Copy with new inputs and comprehensive changes
        complex = box.copy(
            _inputs=[sphere],
            name="complex_box",
            attributes={"detail": 2},
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
    attributes={"sizex": 2, "sizez": 3},  # sizex overridden, sizez added, sizey preserved
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
    attributes={"divisions": 4, "sizey": 2},  # Added + modified attributes
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

### Diamond Pattern
Create nodes that share a common source:

```python
# Shared source
source = chain(
    node(geo, "box"),
    node(geo, "xform", "center")
)

# Two processing paths
path1 = chain(
    node(geo, "xform", "scale_up", _input=source, sx=2),
    node(geo, "xform", "rotate_y", ry=45)
)

path2 = chain(
    node(geo, "xform", "scale_down", _input=source, sx=0.5),
    node(geo, "xform", "rotate_x", rx=30)
)

# Merge results
final = chain(
    node(geo, "merge", _input=[path1, path2]),
    node(geo, "xform", "final_transform", _display=True)
)
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

### Node Naming
```python
# Good - descriptive names
source = node(geo, "box", "source_geometry")
scaled = node(geo, "xform", "scale_2x", _input=source, sx=2, sy=2, sz=2)

# Acceptable - let system generate names
source = node(geo, "box")
scaled = node(geo, "xform", _input=source, sx=2, sy=2, sz=2)
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
# Good - logical groupings
preprocessing = chain(
    node(geo, "box"),
    node(geo, "xform", "center"),
    node(geo, "subdivide", iterations=1)
)

processing = chain(
    node(geo, "xform", "scale", _input=preprocessing, sx=2),
    node(geo, "xform", "rotate", ry=45)
)

# Good - clear final output
output = node(geo, "null", "OUT", _input=processing, _display=True, _render=True)
```

### Creation Patterns
```python
# Good - create final outputs, let dependencies propagate
geo_container = node("/obj", "geo", "my_geometry")
final_chain = create_processing_network(geo_container)

# Only create what's needed
geo_container.create()
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
