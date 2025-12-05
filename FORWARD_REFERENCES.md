![Zabob Banner](docs/images/zabob-banner.jpg)
# Forward Reference Resolution Design

## Overview

Forward references allow nodes to reference other nodes by name before they are created. This enables more natural declaration order and supports circular dependencies in node graphs.

## Core Principles

### 1. Registration Strategy

**Current Decision: Register by Name**
- When ZNode objects with names are passed as inputs to context methods, they are registered under their name
- Registering by name (vs. path) is simpler and safer for initial implementation
- Allows easy lookup and prevents shadowing issues

**Future Enhancement: Register on `__enter__`**
- Consider registering all nodes under context parent when entering context
- Benefits:
  - Early detection of name conflicts
  - Avoids conflicts with generated names
  - Centralizes registration logic

\[This is mostly done]

### 2. Parent Validation

**Strict Enforcement**
- All nodes registered in a context MUST have the same parent as the context
- Validation occurs during auto-registration of external nodes
- Throws `ValueError` if parent mismatch detected

**Future Enhancement: Separate Registry**
- Maintain separate registry for path-referenced nodes
- Useful for round-tripping and metadata association
- Does not require parent matching

### 3. Name Resolution Logic

**Ambiguity Prevention**
- If a ZNode is already registered under a name, use it directly
- Don't create ZNodeForwardRef for names that already resolve
- Prevents ambiguity between registered nodes and forward references

**Current Behavior**
- `_process_input()` creates ForwardReferences for ALL string arguments
- This ensures deferred resolution during `.create()`
- May need refinement to check existing registrations first

## Forward Reference Resolution Algorithm

### Deque-Based Resolution

When resolving forward references during `.create()`:

    Algorithm:
    1. Add all refs to deque
    2. While deque not empty:
       a. Pop reference from front
       b. Try to resolve it
       c. If successful: add to resolved list, reset counter
       d. If fails: push to back, increment counter
    3. Terminate when:
       - Deque empty (success - all resolved)
       - Counter == deque length (deadlock - tried all, none resolved)


### Termination Conditions

1. **Success**: `deque` becomes empty
   - All forward references successfully resolved
   - Ready to proceed with node creation

2. **Deadlock**: `counter == len(deque)`
   - Tried every reference in the queue
   - None could be resolved
   - Circular dependency or missing node detected
   - Raise informative error with unresolved names

### Benefits

- Handles dependencies in any order
- Supports circular references
- Clear failure mode with diagnostic information
- O(n²) worst case, O(n) typical case

## Implementation Notes

### ZNodeForwardRef Structure

```python
@dataclass(frozen=True)
class ZNodeForwardRef:
    resolution_type: str  # 'context_lookup', 'path', etc.
    context: ZContext  # Context to search in
    name: str             # Name to look up

    def resolve(self) -> ZNode:
        """Attempt to resolve to actual ZNode."""
        ...
        # ... other resolution types
```

### Context Integration

- ZContext maintains `_nodes: dict[str, ZNode]` registry
- When creating nodes, ForwardReferences are resolved just-in-time
- Resolution happens during `.create()` call, not during construction
- This preserves the declarative nature of the API

## Open Questions

1. **Generated Name Conflicts**
   - How to handle when auto-generated name conflicts with explicit name?
   - Should we reserve a namespace for generated names?

2. **Circular Dependencies**
   - Do we want to support circular dependencies?
   - If so, how do we break cycles during creation?

3. **Cross-Context References**
   - Should nodes reference nodes from other contexts?
   - What are the semantics if contexts have different parents?

4. **Path vs Name Registration**
   - When should we use path-based registration?
   - How do we distinguish in the API?

## Testing Strategy

- Test name resolution with ForwardReferences
- Test parent validation enforcement
- Test auto-registration of external nodes
- Test resolution algorithm with various dependency orders
- Test deadlock detection with unresolvable references
- Test error messages are informative
