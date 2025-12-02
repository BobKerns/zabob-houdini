![Zabob Banner](../../docs/images/zabob-banner.jpg)

# Testing Directory (Hython Side)

This directory contains the **hython side** of zabob-houdini's test architecture. Code here runs in Houdini's Python environment (`hython`) and **can import the `hou` module**.

## Architecture Overview

Zabob-houdini uses a **split testing architecture**:

- **`tests/`**: Pytest test files that orchestrate execution
- **`src/testing/`** (this directory): Houdini integration code that runs in `hython`

This separation is necessary because importing `hou` outside of Houdini causes segmentation faults (SEGV).

## File Structure

### Naming Convention

Files in this directory use an **underscore prefix** to distinguish them from regular source files:

```text
src/testing/
├── _basic_nodes.py          # Hython code for tests/test_basic_nodes.py
├── _circular_graph.py       # Hython code for tests/test_circular_graph.py
├── _node_context.py         # Hython code for tests/test_node_context.py
└── ...
```

Each `_feature.py` file corresponds to a `test_feature.py` file in the `tests/` directory.

## Writing Integration Code

### Basic Structure

```python
# src/testing/_my_feature.py
"""
Houdini integration tests for my feature.

These tests run in hython and create actual Houdini nodes.
"""

from zabob_houdini.core import node, context, chain
import hou


def test_basic_feature():
    """Test basic feature functionality."""
    # Create geo container first
    geo = hou.node("/obj").createNode("geo", "test_geo")

    with context(geo) as ctx:
        box = ctx.node("box", "my_box")
        sphere = ctx.node("sphere", "my_sphere")

    # Access created nodes
    hou_box = ctx["my_box"].create()
    hou_sphere = ctx["my_sphere"].create()

    # Verify and return results
    return {
        "box_exists": hou_box is not None,
        "sphere_exists": hou_sphere is not None,
        "node_count": len(geo.children())
    }
```

The return values can be any JSON object. This is encapsulate
as the `"result"` field of the `HoudiniResult` typed dict.

`HoudiniResult` objects may be constructed and returned directly,
constructed with the `success_result()` and `error_result()`
functions.

### Key Rules

1. **DO** import `hou` and zabob-houdini modules freely
2. **DO** create actual Houdini nodes for testing
3. **DO** return JSON-serializable dictionaries
4. **DO NOT** return `hou.Node` objects or other non-serializable types
5. **DO** clean up nodes if needed (usually not required for tests)
6. **DO** create parent containers before creating child nodes
7. **DO NOT WRITE TO STDOUT!** -- it is reserved for communication

## Return Value Requirements

Functions must return **JSON-serializable dictionaries**:

```python
# ✅ Good - All JSON-serializable types
return {
    "count": 42,
    "names": ["box", "sphere"],
    "positions": [[0, 0], [1, 0]],
    "metadata": {"key": "value"}
}

# ❌ Bad - hou.Node is not JSON-serializable
return {
    "node": hou.node("/obj/geo1")
}

# ❌ Bad - Not a dictionary
return True

# ❌ Bad - Top-level list instead of dict
return [1, 2, 3]
```

### Extracting Information from hou.Node

When you need to return information about Houdini nodes, extract primitive data:

```python
def test_node_properties():
    geo = hou.node("/obj").createNode("geo", "test_geo")

    with context(geo) as ctx:
        box = ctx.node("box", "my_box", size=2.0)

    hou_box = ctx["my_box"].create()

    # Extract primitive data from hou.Node
    return {
        "success": True,
        "node_path": hou_box.path(),
        "node_type": hou_box.type().name(),
        "node_name": hou_box.name(),
        "position": list(hou_box.position()),
        "parm_value": hou_box.parm("size").eval(),
        "input_count": len(hou_box.inputs()),
        "has_error": hou_box.errors() != ""
    }
```

## Common Patterns

### Creating Test Containers

Always create a geometry container before creating SOP nodes:

```python
def test_sops():
    # Create parent geo node
    geo = hou.node("/obj").createNode("geo", "test_geo")

    # Now create SOP nodes under geo
    with context(geo) as ctx:
        ctx.node("box", "my_box")
```

### Testing Node Connections

```python
def test_connections():
    geo = hou.node("/obj").createNode("geo", "test_geo")

    with context(geo) as ctx:
        box = ctx.node("box", "source")
        xform = ctx.node("xform", "transform", _input="source")

    # Check connections after creation
    hou_xform = ctx["transform"].create()
    inputs = hou_xform.inputs()

    return {
        "success": True,
        "has_input": len(inputs) > 0,
        "input_is_correct": inputs[0].name() == "source" if inputs else False
    }
```

### Testing Context Behavior

```python
def test_context_features():
    geo = hou.node("/obj").createNode("geo", "test_geo")

    with context(geo) as ctx:
        # Create nodes
        ctx.node("box", "A")
        ctx.node("sphere", "B")
        ctx.node("merge", "C", _inputs=["A", "B"])

    # Context automatically calls .create() on exit
    # Access created nodes
    hou_a = ctx["A"].create()
    hou_b = ctx["B"].create()
    hou_c = ctx["C"].create()

    return {
        "success": True,
        "all_created": all([hou_a, hou_b, hou_c]),
        "merge_has_inputs": len(hou_c.inputs()) == 2
    }
```

### Testing Forward References

```python
def test_forward_references():
    """Test forward reference resolution."""
    geo = hou.node("/obj").createNode("geo", "test_geo")

    with context(geo) as ctx:
        # Reference a node before it's defined
        ctx.node("xform", "transform", _input="source")
        ctx.node("box", "source")  # Defined after it's referenced

    # Check if forward reference was resolved
    hou_xform = ctx["transform"].create()
    inputs = hou_xform.inputs()

    return {
        "success": True,
        "has_input": len(inputs) > 0,
        "resolved_correctly": inputs[0].name() == "source" if inputs else False
    }
```

### Testing Circular References

```python
def test_circular_reference():
    """Test circular node graph construction."""
    geo = hou.node("/obj").createNode("geo", "test_geo")

    with context(geo) as ctx:
        # Create circular reference
        ctx.node("null", "A", _input="B")
        ctx.node("null", "B", _input="A")

    # Access created nodes
    hou_a = ctx["A"].create()
    hou_b = ctx["B"].create()

    # Check if cycle was created
    a_inputs = hou_a.inputs()
    b_inputs = hou_b.inputs()

    return {
        "success": True,
        "a_has_input": len(a_inputs) > 0,
        "b_has_input": len(b_inputs) > 0,
        "cycle_exists": (
            len(a_inputs) > 0 and
            len(b_inputs) > 0 and
            a_inputs[0] is not None and
            b_inputs[0] is not None
        )
    }
```

## Testing Against Houdini's Behavior

### Expected Errors

Some tests verify that zabob-houdini correctly handles Houdini limitations:

```python
def test_invalid_parent():
    """Test that invalid parent raises appropriate error."""
    try:
        # This should fail - can't create SOP under /obj directly
        box = node("/obj", "box", "invalid")
        hou_box = box.create()

        return {"success": False, "error": "Should have raised exception"}
    except Exception as e:
        return {
            "success": True,
            "caught_error": True,
            "error_type": type(e).__name__
        }
```

### Node Evaluation Errors

Note that circular references may create nodes successfully but enter an error state when evaluated:

```python
def test_circular_creates_but_errors():
    """Circular references create but don't evaluate."""
    geo = hou.node("/obj").createNode("geo", "test_geo")

    with context(geo) as ctx:
        ctx.node("null", "A", _input="B")
        ctx.node("null", "B", _input="A")

    hou_a = ctx["A"].create()
    hou_b = ctx["B"].create()

    return {
        "success": True,
        "nodes_created": hou_a is not None and hou_b is not None,
        "has_errors": hou_a.errors() != "" or hou_b.errors() != ""
    }
```

## Debugging

### Print Statements

You can use `print()` for debugging - output will be captured by pytest:

```python
def test_debug_example():
    print("Starting test...")
    geo = hou.node("/obj").createNode("geo", "test_geo")
    print(f"Created geo: {geo.path()}")

    # ... rest of test
```

### Inspecting Nodes

```python
def test_inspect_nodes():
    geo = hou.node("/obj").createNode("geo", "test_geo")

    with context(geo) as ctx:
        ctx.node("box", "my_box")

    hou_box = ctx["my_box"].create()

    # Detailed inspection
    print(f"Node path: {hou_box.path()}")
    print(f"Node type: {hou_box.type().name()}")
    print(f"Inputs: {hou_box.inputs()}")
    print(f"Outputs: {hou_box.outputs()}")
    print(f"Errors: {hou_box.errors()}")

    return {"success": True}
```

## Common Issues

### Missing Parent Container

**Error**: "Node at path '/obj/geo1' does not exist"

**Solution**: Create the parent container first:

```python
# ❌ Wrong
with context("/obj/geo1") as ctx:
    ctx.node("box", "my_box")

# ✅ Correct
geo = hou.node("/obj").createNode("geo", "geo1")
with context(geo) as ctx:
    ctx.node("box", "my_box")
```

### Non-Serializable Return Value

**Error**: "Object of type 'Node' is not JSON serializable"

**Solution**: Extract primitive data instead:

```python
# ❌ Wrong
return {"node": hou_node}

# ✅ Correct
return {
    "node_path": hou_node.path(),
    "node_name": hou_node.name()
}
```

### Context Exit Behavior

After context exit, nodes are automatically created:

```python
with context(geo) as ctx:
    ctx.node("box", "my_box")
    # DON'T call .create() here

# Context exit handles creation
# Now access with .create() which returns cached result
hou_box = ctx["my_box"].create()
```

## Related Documentation

- **[tests/README.md](../../tests/README.md)**: Pytest-side test guide
- **[DEVELOPMENT.md](../../DEVELOPMENT.md)**: Overall development guide
- **[FORWARD_REFERENCES.md](../../FORWARD_REFERENCES.md)**: Forward reference design
