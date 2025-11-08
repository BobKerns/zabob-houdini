# Houdini Type Stubs

This directory contains hand-maintained type stubs for Houdini's `hou` module to provide IntelliSense and type checking when developing outside of Houdini.

## Why Hand-Maintained?

The automatically generated stubs were extremely limited and missing many essential Houdini API methods like:

- `setParms()` - Essential for setting multiple parameters at once
- `parmTuple()` - For vector/tuple parameters
- Geometry classes (`Geometry`, `Point`, `Prim`, etc.)
- Node type and category classes
- Many other critical methods

## Modern Python Types

The stubs use modern Python 3.9+ built-in types for better compatibility and cleaner code:

- `tuple[T, ...]` instead of `Tuple[T, ...]`
- `list[T]` instead of `List[T]`
- `dict[K, V]` instead of `Dict[K, V]`
- Reduced imports from `typing` module

This approach is more future-proof and aligns with modern Python typing practices.

## Coverage

The current `hou.pyi` stub includes:

### Core Classes

- **`Node`** - Complete node interface with parameters, connections, creation, state management
- **`Parm`** - Parameter objects with evaluation and setting methods
- **`ParmTuple`** - Vector parameter objects
- **`SopNode`** - Geometry (SOP) nodes with geometry access
- **`ObjNode`** - Object (OBJ) nodes with transforms

### Geometry Classes

- **`Geometry`** - Geometry containers with points/prims access
- **`Point`**, **`Prim`**, **`Vertex`** - Geometry components
- **`Vector3`**, **`Matrix4`** - Math types

### Node Management

- **`NodeType`**, **`NodeTypeCategory`** - Node type system
- **`NodeConnection`** - Node connection objects
- **`ParmTemplate`** - Parameter templates

### Module Functions

- Node navigation (`node()`, `root()`, `pwd()`, `cd()`)
- Node type queries (`nodeTypeCategories()`, `nodeType()`)
- Session info (`applicationName()`, `applicationVersion()`)
- File operations (`hipFile()`)

### Exceptions

- **`OperationFailed`**, **`InvalidInput`**, **`LoadWarning`**

## Development Workflow

1. **VS Code Integration**: These stubs are automatically picked up by VS Code when `stubs/` is in the Python path
2. **Type Checking**: Works with mypy and other type checkers (when mypy is working properly)
3. **IntelliSense**: Provides autocomplete and documentation hints
4. **Validation**: Helps catch API usage errors before running in Houdini

## Maintenance

These stubs should be updated as:

1. New Houdini API methods are used in the project
2. Houdini versions introduce new functionality
3. Type annotations need refinement

The goal is comprehensive coverage of commonly used Houdini API methods while maintaining accuracy with the actual Houdini Python API.
