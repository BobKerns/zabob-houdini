![Zabob Banner](../docs/images/zabob-banner.jpg)
# Houdini Type Safety Improvements

This document explains how our enhanced Houdini stubs address the real-world type checking issues that arise when working with Houdini's `hou` module.

## Core Problems Solved

### 1. Static vs Instance Method Confusion

**Problem**: Houdini has functions like `hou.node()` at module level and `node.node()` as instance methods, causing confusion about which to use.

**Solution**: Clear documentation and typing that distinguishes module-level functions as the primary interface:

```python
# Module-level (preferred for accessing existing nodes)
def node(path: str) -> Optional[Node]: ...

# Instance method (for relative navigation)
class Node:
    def node(self, path: str) -> Optional[Node]: ...
```

### 2. Return Type Clarity

**Problem**: C++ bindings don't indicate when methods can return `None` or what specific types they return.

**Solution**: Comprehensive Optional typing and specific return types:

```python
def parm(self, name: str) -> Optional['Parm']: ...  # None if parameter doesn't exist
def children(self) -> Tuple['Node', ...]: ...       # Empty tuple if no children
def evalParm(self, name: str) -> ParameterValue: ... # Union[int, float, str, bool]
```

### 3. Parameter Type Handling

**Problem**: Houdini parameters accept multiple types but it's unclear which types are valid.

**Solution**: Type unions and specialized methods:

```python
# Clear type unions
ParameterValue = Union[int, float, str, bool]
ParameterDict = Dict[str, ParameterValue]

# Type-specific methods for when you need guarantees
def evalParmAsFloat(self, name: str) -> float: ...
def evalParmAsString(self, name: str) -> str: ...
```

### 4. Exception Handling

**Problem**: Unclear when Houdini operations can fail and what exceptions they raise.

**Solution**: Documented exception patterns:

```python
def createNode(self, node_type: str, name: Optional[str] = None) -> 'Node':
    """Can raise OperationFailed if creation fails."""
    ...

def cook(self, force: bool = False) -> None:
    """Can raise cooking errors if node is invalid."""
    ...
```

### 5. Node Type Hierarchy

**Problem**: Different node types have different capabilities but the type system doesn't reflect this.

**Solution**: Proper inheritance hierarchy:

```python
class Node: ...                    # Base node functionality
class SopNode(Node): ...          # Geometry-specific methods
class ObjNode(Node): ...          # Object/transform methods
class ChopNode(Node): ...         # Channel-specific methods
```

## Advanced Features

### Context Managers for Safety

```python
# Safe undo grouping
def undos() -> 'UndoManager': ...

class UndoGroup:
    def __enter__(self) -> 'UndoGroup': ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
```

### Enhanced Connection Handling

```python
# Clear sparse input handling
def inputs(self) -> Tuple[Optional['Node'], ...]: ...  # None for unconnected
def connectedInputs(self) -> List[Optional['Node']]: ... # List with None gaps
def setInput(self, index: int, node: Optional['Node']) -> None: ... # None to disconnect
```

### Type-Safe Parameter Operations

```python
# Flexible parameter setting with proper types
def setParms(self, parm_dict: ParameterDict) -> None: ...
def setParmValues(self, parm_dict: Dict[str, Any]) -> None: ...  # More permissive
```

## Benefits for Development

1. **Better IntelliSense**: Accurate autocomplete with proper return types
2. **Error Prevention**: Catch type mismatches before running in Houdini
3. **Documentation**: Method signatures serve as inline documentation
4. **Refactoring Safety**: Type checker catches issues when changing code
5. **API Clarity**: Clear distinction between different types of operations

## Usage Patterns

### Safe Node Access

```python
parent_node = hou.node("/obj")
if parent_node is not None:  # Type checker knows this is needed
    child = parent_node.createNode("geo", "my_geo")
```

### Parameter Setting with Types

```python
# Type-safe parameter setting
params: ParameterDict = {"tx": 5.0, "ty": 10.0, "tz": 0.0}
node.setParms(params)  # Type checker validates parameter types
```

### Context-Aware Operations

```python
# Safe undo grouping
with hou.undos().group("Create nodes"):
    node1 = parent.createNode("box")
    node2 = parent.createNode("sphere")
    node2.setInput(0, node1)
```

This comprehensive typing approach makes Houdini development more reliable and helps catch issues early in the development process.
