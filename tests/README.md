![Zabob Banner](../docs/images/zabob-banner.jpg)

# Tests Directory

This directory contains the **pytest side** of zabob-houdini's test architecture. Tests here run in a standard Python environment and **cannot import the `hou` module** directly.

## Architecture Overview

Zabob-houdini uses a **split testing architecture** to handle Houdini's Python environment requirements:

- **`tests/`** (this directory): Pytest test files that orchestrate test execution
- **`src/testing/`**: Houdini integration code that runs in `hython` and can import `hou`

This separation is necessary because importing `hou` outside of Houdini's Python environment causes segmentation faults (SEGV).

## Test Structure

### Test Files

Test files in this directory follow pytest conventions:

```python
# tests/test_feature.py
import pytest

@pytest.mark.integration
def test_something(hython_test):
    """Test description."""
    result = hython_test("test_something")

    assert result["success"] is True
    assert result["expected_value"] == 42
```

### Key Rules

1. **DO NOT** import `hou` or any zabob-houdini module that imports `hou` (like `zabob_houdini.core`)
2. **DO** import pytest and use standard Python libraries
3. **DO** use the `hython_test` fixture to run Houdini integration code
4. **DO** use `@pytest.mark.integration` for tests that require Houdini
5. **DO** use `@pytest.mark.unit` for pure Python tests that don't need Houdini

### Test Markers

- `@pytest.mark.integration`: Tests that require Houdini (use `hython_test` fixture)
- `@pytest.mark.unit`: Pure Python tests (no Houdini required)

## The `hython_test` Fixture

The `hython_test` fixture (defined in `conftest.py`) bridges the pytest and hython environments:

```python
def test_example(hython_test):
    # Call a function from src/testing/_example.py
    result = hython_test("test_example_function")

    # Result is a dict returned by the hython function
    assert result["success"] is True
```

### How It Works

1. Test calls `hython_test("function_name")`
2. Fixture spawns a persistent `hython` process
3. Function from `src/testing/_*.py` is executed in hython
4. Result (must be JSON-serializable dict) is returned to pytest
5. Test makes assertions on the result

### Naming Convention

For each test file `tests/test_feature.py`, there should be a corresponding `src/testing/_feature.py` containing the hython-side implementation functions.

## Writing Tests

### 1. Create Test File

```python
# tests/test_my_feature.py
import pytest

@pytest.mark.integration
def test_my_feature(hython_test):
    """Test my feature works correctly."""
    result = hython_test("test_my_feature")

    assert result["success"] is True
    assert result["node_count"] == 3
```

### 2. Create Implementation File

Create corresponding file in `src/testing/`:

```python
# src/testing/_my_feature.py
"""
Houdini integration tests for my feature.
These functions run in hython and can import hou.
"""
import hou
from zabob_houdini.core import node, context

def test_my_feature():
    """Implementation that runs in hython."""
    # Create geo container
    geo = hou.node("/obj").createNode("geo", "test_geo")

    # Use zabob-houdini API
    with context(geo) as ctx:
        ctx.node("box", "my_box")
        ctx.node("sphere", "my_sphere")

    # Return JSON-serializable dict
    return {
        "success": True,
        "node_count": len(geo.children())
    }
```

### 3. Return Data Format

Functions in `src/testing/` must return JSON-serializable dictionaries:

```python
# Good
return {
    "success": True,
    "count": 42,
    "names": ["box", "sphere"]
}

# Bad - hou.Node is not JSON-serializable
return {
    "node": hou.node("/obj/geo1")  # Will fail!
}
```

## Common Patterns

### Testing Node Creation

```python
@pytest.mark.integration
def test_node_creation(hython_test):
    result = hython_test("test_node_creation")

    assert result["node_exists"] is True
    assert result["node_type"] == "box"
    assert result["node_name"] == "my_box"
```

### Testing Context Management

```python
@pytest.mark.integration
def test_context_behavior(hython_test):
    result = hython_test("test_context_behavior")

    assert result["nodes_created"] == 5
    assert result["layout_applied"] is True
```

### Testing Forward References

```python
@pytest.mark.integration
def test_forward_reference(hython_test):
    result = hython_test("test_forward_reference")

    assert result["reference_resolved"] is True
    assert result["connection_exists"] is True
```

## Running Tests

```bash
# Run all tests
pytest

# Run only integration tests
pytest -m integration

# Run specific test file
pytest tests/test_my_feature.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_my_feature.py::test_specific_function
```

## Debugging Tests

### View hython Output

The `hython_test` fixture captures output from the hython process. If a test fails, check:

1. The error message in the pytest output
2. The hython traceback (included in failure messages)
3. The returned result dictionary

### Common Issues

**"Invalid JSON response from hython process"**
- The hython process terminated unexpectedly
- This usually indicates a fatal error (SEGV, import failure, etc.)
- Check for imports of modules that shouldn't be in hython context
- Note: Regular exceptions are caught and communicated back with full tracebacks

**"Node at path '...' does not exist"**
- Need to create parent container first
- Example: `geo = hou.node("/obj").createNode("geo", "geo1")`

**"maximum recursion depth exceeded"**
- Circular reference not being handled correctly
- Check ForwardReference resolution logic

## Related Documentation

- **[src/testing/README.md](../src/testing/README.md)**: Hython-side implementation guide
- **[DEVELOPMENT.md](../DEVELOPMENT.md)**: Overall development guide
- **[FORWARD_REFERENCES.md](../FORWARD_REFERENCES.md)**: Forward reference design
