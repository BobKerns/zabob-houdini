# Understanding Houdini Node Type Hierarchies

This document explains the complex patterns used in Zabob-Houdini to represent Houdini's node type system, particularly focusing on the relationship between **node type inheritance** and **node containment**.

## Key Term: Reification

Throughout this document, we use the term **reify** (from Latin *res* = "thing"):

> **Reify**: To make abstract concepts concrete by representing them as actual objects/classes in code.

In type theory terms:
- **Abstract concept**: `Union[TypeA, TypeB, TypeC]` or `TypeA & TypeB` (intersection)
- **Reified form**: `class BaseType` that explicitly represents the union/intersection as a concrete class

**Example**:
```python
# Abstract union (exists only in type annotations):
NodeTypes = Union[NodeInstance, ForwardReference, ContextReference]

# Reified form (exists as actual Python class):
class NodeBase:  # Concrete class representing the union
    pass

class NodeInstance(NodeBase): pass
class ForwardReference(NodeBase): pass
```

**Why reify?** Python can't use abstract unions with `isinstance()` at runtime. By reifying the union as a class, we make it concrete and usable in actual Python code, not just type annotations.

When you see "reify" in this document, think: **"turn the abstract type into a concrete class"**.

### Note for Logic/AI Researchers

In formal logic notation (both LaTeX and Unicode for accessibility):

| Concept | Notation |
|---------|----------|
| **Union reification** | $\forall x: (x \in TypeA \vee x \in TypeB) \Leftrightarrow x \in BaseClass$ |
|  | `∀x: (x ∈ TypeA ∨ x ∈ TypeB) ⟺ x ∈ BaseClass` |
|  | *"For all x: x is in TypeA OR TypeB if and only if x is in BaseClass"* |
| **Intersection reification** | $\exists props: \forall x \in Union: x \text{ has } props$ |
|  | `∃props: ∀x ∈ Union: x has props` |
|  | *"There exist properties that all union members must have; BaseClass defines them"* |

This pattern may be familiar from:
- **Knowledge representation systems** (Cyc, ontologies, semantic networks)
- **Type theory & proof assistants** (Coq, Agda, Lean)
- **Functional programming (FP)** (type classes, traits)
- **Logic programming** (Prolog, Answer Set Programming)
- **Description logics** (OWL, RDF Schema)

In all these systems, abstract concepts must be grounded as concrete representations for the inference/reasoning engines to operate on them.

## The Challenge: Two Overlapping Hierarchies

Houdini has two distinct but interrelated hierarchies that we must model:

### 1. Node Type Inheritance Hierarchy (What a node IS)

This is the straightforward Python/C++ class inheritance:

```text
hou.Node                    # Base for all nodes
  ├─ hou.OpNode             # Operator nodes (nodes with parameters)
  │   ├─ hou.SopNode        # Surface operators (geometry)
  │   ├─ hou.ObjNode        # Object nodes (transforms, containers)
  │   ├─ hou.ChopNode       # Channel operators
  │   ├─ hou.RopNode        # Render operators
  │   ├─ hou.DopNode        # Dynamics operators
  │   ├─ hou.VopNode        # VEX operators
  │   └─ ...
  └─ (other node types)
```

This hierarchy determines what **methods and properties** a node has.

### 2. Node Containment Hierarchy (What a node CAN CONTAIN)

This hierarchy determines what **child nodes** can be created inside a parent node:

```text
/obj (Object level - hou.ObjNode)
  ├─ Can contain: ObjNode children (geo, cam, light, etc.)
  └─ /obj/geo (Geometry container - hou.ObjNode)
      ├─ Can contain: SopNode children (box, xform, merge, etc.)
      └─ /obj/geo/box (Box SOP - hou.SopNode)
          └─ Cannot contain children (leaf node)
```

**The confusing part**: An `ObjNode` can contain both other `ObjNode` children AND `SopNode` children, depending on its specific node type string (e.g., "geo" vs "cam").

## Generic Type Parameters: Modeling the Hierarchies

Our core classes use generic type parameters to capture both hierarchies:

```python
class NodeBase(Generic[T_Cat, T_Parent, T_Node, T_Child]):
    """
    T_Cat:    NodeTypeCategory - The category system (Sop, Object, etc.)
    T_Parent: The actual parent node type (what contains this node)
    T_Node:   The actual type of THIS node (what it inherits from)
    T_Child:  What types of children THIS node can contain
    """
```

### Type Parameter Meanings

| Parameter | Represents | Example Values |
|-----------|-----------|----------------|
| `T_Cat` | Category manager/registry | `hou.OpNodeTypeCategory` |
| `T_Parent` | Type of parent containing this node | `hou.ObjNode`, `hou.SopNode` |
| `T_Node` | Type of this node itself | `hou.SopNode`, `hou.ObjNode` |
| `T_Child` | Types this node can contain as children | `hou.SopNode`, `hou.OpNode` |

## Concrete Example: SOP Node Hierarchy

Let's trace a specific example: creating a box SOP inside a geo object.

### The Players

```python
# /obj - The root object level
obj_root = wrap_node(hou_node('/obj'))
# Type: NodeInstance[..., hou.OpNode, hou.ObjNode, hou.OpNode]
#                     ^            ^            ^
#                     Category     ParentType   NodeType = ObjNode

# /obj/geo - A geometry container (still an ObjNode)
geo = obj_root.node('geo', 'geo1')
# Type: NodeInstance[..., hou.ObjNode, hou.ObjNode, hou.SopNode]
#                     ^            ^            ^
#                     Parent       NodeType     ChildType = can contain SOPs

# /obj/geo/box - A box SOP
box = geo.node('box', 'box1')
# Type: NodeInstance[..., hou.ObjNode, hou.SopNode, hou.OpNode]
#                     ^            ^            ^
#                     Parent       NodeType     ChildType (leaf - generic)
```

### Why This Matters

The generic parameters let the type checker understand:

1. **What methods are available** (`T_Node`):
   - `box` is a `SopNode`, so it has `.geometry()` method
   - `geo` is an `ObjNode`, so it has `.worldTransform()` method

2. **What can be created inside** (`T_Child`):
   - `geo` can contain `SopNode` children → `geo.node('box', ...)` is valid
   - `box` cannot meaningfully contain children → typically uses generic `hou.OpNode` bound

3. **What context this node lives in** (`T_Parent`):
   - `box`'s parent is `ObjNode` (the `geo` container)
   - Used for path resolution and hierarchy validation

## Union Reification Pattern

A key design decision: we use **classes to reify unions** rather than explicit union types.

**Reification recap**: We turn abstract `Union[...]` types into concrete classes that exist at runtime, not just in type annotations.

### Why Not String Literal Types?

An earlier approach tried using string literal types for node types (e.g., `Literal["box", "sphere", "merge", ...]`). This maximized familiarity while providing type safety, but had a critical flaw:

**Type checkers struggled with large unions**. Just the SOP node types alone (100+ strings) overwhelmed type checking performance. Checking membership in such large unions is computationally expensive.

### The Reification Solution

Instead, we use **class hierarchies to represent unions implicitly**:

```python
# Instead of: Union[SopInstance, SopForwardRef, SopContextRef, ...]
# We have:
class SopBase:  # Reifies the union of all SOP-related types
    pass

class SopInstance(OpInstance, SopBase):  # Member of the union
    pass

class SopForwardRef(ForwardReference, SopBase):  # Member of the union
    pass
```

**Key insight**: Checking `isinstance(obj, SopBase)` is a simple MRO (Method Resolution Order) lookup, much faster than checking membership in a large union type.

### Multiple Inheritance Explained

The multiple inheritance pattern serves a specific purpose: **efficient union membership testing**.

```python
class OpBase(NodeBase[hou.OpNodeTypeCategory, T_OpParent, T_OpNode, T_OpChild]):
    """Reifies the union of all Op-related types (instances, forward refs, etc.)"""
    pass

class OpInstance(NodeInstance[...], OpBase[...]):
    """
    Concrete operator node instance.

    Inherits from:
    - NodeInstance: Gets creation, caching, and connection logic
    - OpBase: Declares membership in the Op type union
    """
    pass
```

At first glance, the multiple inheritance seems redundant - `OpInstance` doesn't override anything from `OpBase`. But it serves two critical purposes:

1. **Static type checking**: Type checkers can quickly determine `OpInstance` is a subtype of `OpBase`
2. **Runtime type checking**: `isinstance(obj, OpBase)` works efficiently via MRO lookup

### Union Hierarchy

The reification creates an implicit union hierarchy:

```python
NodeBase             # Reifies: Union[NodeInstance, ForwardReference, ...]
├─ OpBase            # Reifies: Union[OpInstance, OpForwardRef, ...]
│  ├─ SopBase        # Reifies: Union[SopInstance, SopForwardRef, ...]
│  ├─ ObjBase        # Reifies: Union[ObjInstance, ObjForwardRef, ...]
│  └─ ChopBase       # (future)
└─ (other bases)
```

Each "Base" class represents a union of all concrete types at that level, without explicitly enumerating them.

## Python's Union Limitations

Python's type system has significant limitations with unions that make reification necessary:

### Runtime Limitations

Python doesn't treat unions as first-class types at runtime:

```python
from typing import Union

# This doesn't work:
NodeType = Union[NodeInstance, ForwardReference]
isinstance(obj, NodeType)  # ❌ TypeError: cannot use Union with isinstance()

# This works:
class NodeBase: pass
isinstance(obj, NodeBase)  # ✅ Standard Python runtime check
```

**The problem**: You cannot use `isinstance()` or `issubclass()` with `Union` types. This breaks runtime type checking, which is essential for dynamic node creation.

### Type Inference Limitations

Python's type inference with unions is less sophisticated than TypeScript:

1. **No type intersection**: Python cannot infer `TypeA & TypeB` (types satisfying both)
2. **No type negation**: Python cannot express "not TypeA"
3. **Limited narrowing**: Type checkers struggle to narrow union types through control flow

TypeScript example (not available in Python):
```typescript
// TypeScript can do this:
type Intersection = TypeA & TypeB;  // ❌ Not in Python
type Negation = Exclude<All, TypeA>;  // ❌ Not in Python
```

### The Intersection/Union Duality

This is where reification becomes particularly powerful. By creating a concrete base class, we simultaneously represent both:
1. A union (any of these types)
2. An intersection (what all these types share)

Base classes serve double duty:

```python
# Forward view: NodeBase is a UNION
class NodeBase: pass  # Union of all node-like types

class NodeInstance(NodeBase): pass
class ForwardReference(NodeBase): pass
# NodeBase = Union[NodeInstance, ForwardReference, ...]

# Reverse view: NodeBase is an INTERSECTION
# NodeBase is the set of properties/methods that ALL members MUST satisfy
# It's the intersection of what NodeInstance and ForwardReference have in common
```

**The duality**:
- **Union** (forward): "NodeBase represents any of these types"
- **Intersection** (reverse): "NodeBase is what all these types share"

### Reification Makes Intersection Explicit

In Python, intersection types aren't directly expressible. But by creating a base class, we **reify the intersection**:

```python
class NodeBase:
    """
    The intersection of all node-like types.

    This represents the minimal interface that ALL node types must satisfy:
    - NodeInstance must be a NodeBase
    - ForwardReference must be a NodeBase
    - Any new node-like type must be a NodeBase

    By inheriting from NodeBase, each type explicitly declares:
    "I satisfy the intersection of properties that define a node"
    """
    # Common properties/methods that ALL nodes must have
    name: str
    node_type: str
    # ... etc
```

**Why this matters**:

1. **Runtime checking works**: `isinstance(obj, NodeBase)` succeeds
2. **Type inference works**: Type checkers see the shared interface
3. **Intersection is explicit**: The base class documents what all union members share
4. **New types self-document**: Inheriting from `NodeBase` declares "I am a node type"

### Without Reification

If Python had TypeScript's intersection types, we could write:

```python
# Hypothetical Python with intersection (doesn't exist):
NodeIntersection = NodeInstance & ForwardReference & ...
# The minimal type that all of these satisfy

def process_node(node: NodeIntersection):
    # node has only the properties common to all union members
    pass
```

But since Python lacks this, we **invert the relationship**:

```python
# Actual Python - intersection reified as base class:
class NodeBase:  # The intersection, made explicit
    pass

class NodeInstance(NodeBase):  # Inherits the intersection
    pass

class ForwardReference(NodeBase):  # Inherits the intersection
    pass

def process_node(node: NodeBase):  # Works with the intersection
    pass
```

### The Power of Inheritance

By using inheritance to declare "I satisfy this intersection", we get:

1. **Runtime validation**: `isinstance()` checks work
2. **Type narrowing**: Type checkers can narrow from `NodeBase` to specific types
3. **Explicit contract**: The base class documents the shared interface
4. **Performance**: MRO lookup is faster than union enumeration

This is why multiple inheritance isn't redundant - it's declaring membership in **multiple intersection/union hierarchies simultaneously**:

```python
class SopInstance(NodeInstance, SopBase):
    # Declares: "I satisfy the NodeInstance intersection"
    #       AND "I satisfy the SopBase intersection"
    # Therefore: "I'm in the union of all nodes"
    #       AND "I'm in the union of all SOPs"
    pass
```

Each inheritance declares satisfaction of an intersection, which grants membership in the corresponding union.

## Specialized Type Classes

Building on the reification pattern, we create specialized classes for common scenarios:

### OpNode Family (Base for Most Operators)

```python
class OpBase(NodeBase[hou.OpNodeTypeCategory, T_OpParent, T_OpNode, T_OpChild]):
    """
    Reifies the union of all Op-related types.
    Base for operator nodes - fixes the category to OpNodeTypeCategory.
    """
    pass

class OpInstance(NodeInstance[T_OpParent, T_OpNode, T_OpChild],
                 OpBase[T_OpParent, T_OpNode, T_OpChild]):
    """
    Concrete operator node instance.

    Multiple inheritance:
    - NodeInstance: Provides creation and connection logic
    - OpBase: Declares membership in Op union for efficient type checking
    """
    pass

class OpContext(NodeContext[hou.OpNodeTypeCategory, T_OpParent, T_OpCtx, T_OpNode]):
    """Context manager for creating operator nodes"""
    pass
```

### SOP Specialization

```python
class SopBase(OpBase[T_OpCtx, T_SopNode, T_OpChild]):
    """
    Reifies the union of all SOP-related types.
    Base for SOP nodes - parent context must support SOPs.
    """
    pass

class SopInstance(OpInstance[T_OpParent, T_SopNode, T_OpChild],
                  SopBase[T_OpParent, T_SopNode, T_OpChild]):
    """
    A concrete SOP node.

    Multiple inheritance:
    - OpInstance: Inherits Op functionality
    - SopBase: Declares membership in SOP union

    This allows both:
    - isinstance(sop_node, OpBase)   # True - it's an Op
    - isinstance(sop_node, SopBase)  # True - it's specifically a SOP
    """
    pass

class SopContext(OpContext[T_OpParent, T_SopNode, T_OpChild]):
    """Context for creating SOP nodes (inside a geo container)"""
    pass
```

### OBJ Specialization

```python
class ObjInstance(OpInstance[T_ObjParent, T_ObjNode, T_ObjChild]):
    """A concrete OBJ node"""
    pass

class ObjContext(OpContext[T_ObjParent, T_ObjCtx, T_ObjNode]):
    """Context for creating OBJ nodes (at object level)"""
    pass
```

## Usage Pattern Example

Here's how the types work together in practice:

```python
from zabob_houdini import wrap_node, hou_node
from zabob_houdini.op import OpInstance, OpContext
from zabob_houdini.sop import SopInstance, SopContext

# Start at object level
obj = wrap_node(hou_node('/obj'))
# Type: OpInstance[hou.OpNode, hou.ObjNode, hou.OpNode]

# Create a geometry container context
with OpContext(obj) as obj_ctx:
    # This creates an ObjNode that can contain SOPs
    geo = obj_ctx.node('geo', 'geo1')
    # Type: OpInstance[hou.ObjNode, hou.ObjNode, hou.SopNode]
    #                  ^parent     ^this node   ^children

    # Now create SOPs inside the geo
    with SopContext(geo) as sop_ctx:
        box = sop_ctx.node('box', 'box1')
        # Type: SopInstance[hou.ObjNode, hou.SopNode, hou.OpNode]
        #                   ^parent      ^this node   ^children

        xform = sop_ctx.node('xform', 'xform1', _input=box)
        # Type: SopInstance[hou.ObjNode, hou.SopNode, hou.OpNode]

# The type parameters ensure:
# - box.create().geometry() works (it's a SopNode)
# - geo.create().worldTransform() works (it's an ObjNode)
# - Type checker knows what nodes can be created in each context
```

## The Confusing Part: ObjNode's Dual Role

The most confusing aspect is that `hou.ObjNode` plays two roles:

1. **Container role**: A "geo" ObjNode contains SopNodes
   ```python
   geo: OpInstance[hou.ObjNode, hou.ObjNode, hou.SopNode]
   #                              ^this       ^children are SOPs
   ```

2. **Object role**: A "cam" ObjNode is just an object (leaf or contains other ObjNodes)
   ```python
   cam: OpInstance[hou.ObjNode, hou.ObjNode, hou.ObjNode]
   #                              ^this       ^children are ObjNodes (or none)
   ```

**Currently**: We use string node types (e.g., "geo", "cam") and rely on Houdini to determine what can be created inside.

**Future**: We'll introduce `NodeTypeInstance` classes that encode the child type in the type system:
```python
class GeoNodeType:
    """Represents the 'geo' node type - creates ObjNode containing SopNodes"""
    child_category = hou.sopNodeTypeCategory()
    creates = OpInstance[hou.ObjNode, hou.ObjNode, hou.SopNode]
```

## Practical Guidelines

When working with these types:

1. **T_Parent**: Think "what contains me"
   - Used for path construction
   - Determines context hierarchy

2. **T_Node**: Think "what am I"
   - Determines available methods
   - Drives type narrowing (`.create(as_type=...)`)

3. **T_Child**: Think "what can I create"
   - Determines what `.node()` calls are valid
   - Used by context managers

4. **T_Cat**: Usually just follows from T_Node
   - `OpNode` → `OpNodeTypeCategory`
   - Mostly bookkeeping for Houdini's registry system

## Why This Complexity?

This pattern is necessary because:

1. **Houdini's node containment is type-driven, not class-driven**
   - The string "geo" determines you can create SOPs inside
   - The string "cam" means you can't (or create other ObjNodes)

2. **Type safety without performance penalty**
   - Generic parameters give us compile-time checks
   - Union reification makes runtime checks fast (MRO lookup vs union membership)
   - Earlier attempts with string literal unions killed type checker performance

3. **Context-aware node creation**
   - `SopContext` knows it creates SOPs
   - Type checker prevents creating SOPs in wrong contexts
   - Runtime checks are efficient via `isinstance()`

4. **Houdini's flexibility preserved**
   - Still use string node types for maximum compatibility
   - Future: can add strongly-typed node types
   - Doesn't break existing code

5. **Efficient type checking**
   - Multiple inheritance creates fast union membership tests
   - Type checkers search MRO instead of enumerating union members
   - Critical for large type systems (100+ SOP types, 50+ OBJ types, etc.)

## Future: Strongly-Typed Node Types

Eventually, we'll replace strings with typed node type classes:

```python
# Instead of:
geo.node('box', 'box1')

# We'll have:
geo.node(BoxSop, 'box1')

# Where BoxSop knows:
class BoxSop(SopNodeType):
    name = "box"
    creates = SopInstance[..., hou.SopNode, hou.OpNode]
    category = hou.sopNodeTypeCategory()
```

This will give us:
- Parameter autocompletion
- Type-safe parameter passing
- Documentation in the type system

But for now, strings work fine and let us prototype the architecture.

## Performance Considerations

The union reification pattern provides concrete performance benefits:

### String Literal Union Approach (Rejected)

```python
# This kills type checker performance:
SopNodeType = Literal["box", "sphere", "merge", "xform", "subdivide", ...]  # 100+ types

def create_sop(node_type: SopNodeType) -> SopNode:
    # Type checker must check 'node_type' against 100+ literal values
    pass
```

**Problem**: Type checkers must enumerate and check all union members. With 100+ SOP types, 50+ OBJ types, etc., this becomes prohibitively expensive.

### Class Hierarchy Approach (Current)

```python
# Fast type checking via MRO:
class SopBase: pass
class BoxSop(SopInstance, SopBase): pass

def create_sop(node_base: SopBase) -> SopNode:
    # Type checker just checks: "Is node_base a subclass of SopBase?"
    # This is an O(MRO depth) operation, not O(union size)
    pass
```

**Advantage**: MRO lookup is logarithmic in depth, not linear in union size. Checking `isinstance(obj, SopBase)` walks the MRO (typically <10 classes) rather than checking 100+ union members.

### Why Multiple Inheritance Isn't Redundant

The multiple inheritance serves as **union membership declaration**:

```python
class SopInstance(OpInstance, SopBase):
    pass

# Now type checkers know:
# - isinstance(sop, SopInstance) → True (exact type)
# - isinstance(sop, SopBase)     → True (member of SOP union)
# - isinstance(sop, OpBase)      → True (member of Op union)
# - isinstance(sop, NodeBase)    → True (member of all nodes union)

# All checked via fast MRO lookup, not union enumeration!
```

Without the multiple inheritance, we'd need explicit `Union[SopInstance, SopForwardRef, ...]` declarations everywhere, killing performance.

## Summary

The generic type parameters model TWO hierarchies:

1. **Inheritance hierarchy** (`T_Node`): What class methods are available
2. **Containment hierarchy** (`T_Parent`, `T_Child`): What can contain what

The `T_Cat` parameter is mostly bookkeeping for Houdini's category system.

**The union reification pattern** (using base classes like `SopBase`, `OpBase`) provides:
- Fast type checking via MRO instead of union enumeration
- Implicit union membership without explicit `Union[...]` types
- Multiple inheritance that serves a concrete purpose: efficient union testing

The specialized classes (`OpInstance`, `SopInstance`, etc.) lock down common combinations to make the types more manageable while preserving type checker performance.

The complexity is necessary to give type safety to Houdini's dynamic, string-based node creation system without losing flexibility or performance.

## Quick Reference: Design Patterns

### Pattern 1: Reify Unions with Base Classes (Intersection/Union Duality)

**Don't**: Use explicit union types
```python
# Multiple problems:
SopType = Union[BoxSop, SphereSop, MergeSop, ...]  # 100+ types
# - Kills type checker performance
# - Can't use with isinstance() at runtime
# - Doesn't express what properties union members share (intersection)
```

**Do**: Use base classes to reify both union and intersection
```python
# Fast MRO-based checking + runtime support:
class SopBase:  # The intersection of what all SOPs must satisfy
    pass

class BoxSop(SopInstance, SopBase):  # Declares satisfaction of intersection
    pass                              # → member of union

# Now works at runtime:
isinstance(box, SopBase)  # ✅ True

# Type checker sees intersection (shared interface) AND union (membership)
```

**The duality**: `SopBase` is simultaneously:
- **Union**: Represents "any SOP type" (forward view)
- **Intersection**: Defines "what all SOPs share" (reverse view)

### Pattern 2: Multiple Inheritance for Union Membership

**Purpose**: Declare that a type satisfies multiple intersections (belongs to multiple unions)

```python
class SopInstance(OpInstance, SopBase):
    #                ^           ^
    #                |           └─ Satisfies SopBase intersection → member of SOP union
    #                └─ Satisfies OpInstance intersection → inherits Op functionality
    pass
```

**Key insight**: Each base class represents an intersection of properties that all union members must satisfy. By inheriting from multiple bases, a type declares "I satisfy all these intersections", which grants membership in the corresponding unions.

**Result**: Fast type checking at all hierarchy levels via MRO, plus Python runtime `isinstance()` support

### Pattern 3: Generic Parameters for Two Hierarchies

**Inheritance** (what methods exist):
```python
T_Node = hou.SopNode  # Has .geometry() method
```

**Containment** (what can be created):
```python
T_Parent = hou.ObjNode  # Lives in a geo container
T_Child = hou.OpNode    # Typically a leaf node
```

### Pattern 4: Specialized Classes Lock Down Combinations

Instead of manually specifying all 4 type parameters everywhere:
```python
# Verbose:
NodeInstance[hou.OpNodeTypeCategory, hou.ObjNode, hou.SopNode, hou.OpNode]

# Concise:
SopInstance[hou.ObjNode, hou.SopNode, hou.OpNode]
# OpNodeTypeCategory is fixed by SopInstance
```

## Historical Context

This is the **second implementation** of this pattern. The first version used string literal types (`Literal["box", "sphere", ...]`) to maximize familiarity while providing type safety. While this worked functionally, type checkers struggled with the large unions (100+ SOP types alone).

The current approach uses **class hierarchies to reify unions**, providing the same type safety with dramatically better performance. The multiple inheritance pattern, while appearing redundant at first, serves a critical purpose: enabling efficient `isinstance()` checks and fast type checker validation via MRO lookup rather than union enumeration.

## For Future Development

When adding new node type families (CHOP, ROP, DOP, etc.):

1. Create a `*Base` class (e.g., `ChopBase(OpBase)`) to reify the union
2. Create specialized classes using multiple inheritance:
   ```python
   class ChopInstance(OpInstance, ChopBase): pass
   class ChopContext(OpContext): pass
   ```
3. Update generic type parameters to restrict to appropriate types
4. Add examples showing the type flow through the hierarchy

The pattern scales efficiently because MRO lookup time is logarithmic in hierarchy depth, not linear in the number of node types.
