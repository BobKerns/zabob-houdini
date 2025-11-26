# Scan Stub Completeness

Scan the Houdini Python API stubs for completeness against the official documentation.

## Task

1. **Search for all stub files** in `stubs/hou/*.pyi`
2. **Check implementation status** using grep to find classes, functions, and enums
3. **Identify completed modules** - modules with full implementations
4. **Identify gaps** - missing classes, functions, and enums compared to official docs
5. **Provide summary report** with:
   - List of completed modules (✅)
   - Major gaps in main `__init__.pyi` organized by category
   - Status of other stub files (completed/unknown/incomplete)
   - Prioritization suggestions for next implementations

## Expected Output Format

```markdown
**Completed modules:**
- ✅ `hou.module` - Description (N classes, M functions, P enums)

**Major gaps in main `__init__.pyi`:**

**Missing Category** (~N classes):
- Class list with brief descriptions

**Other stub files:**
- Status of each .pyi file
```

## Reference

The comprehensive Houdini API documentation is at:
<https://www.sidefx.com/docs/houdini/hom/hou/index.html>

Module-specific docs follow pattern:
<https://www.sidefx.com/docs/houdini/hom/hou/{module}.html>
