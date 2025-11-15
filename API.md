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
def create(self, as_type: type[T] = hou.Node, _skip_chain: bool = False) -> T
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
        _skip_chain: Internal flag to avoid recursion during chain creation

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

def copy(self, _inputs: InputNodes = (), _chain: 'Chain | None' = None) -> 'NodeInstance'
    """
    Create a copy of this NodeInstance with optional input modifications.

    Args:
        _inputs: New input connections for the copy
        _chain: Chain reference for the copied node

    Returns:
        New NodeInstance with copied attributes and specified inputs
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

def copy(self, _inputs: InputNodes = ()) -> 'Chain'
    """
    Create a deep copy of this chain.

    Args:
        _inputs: New input connections for the first node

    Returns:
        New Chain with copied NodeInstances
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
