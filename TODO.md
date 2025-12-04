![Zabob Banner](docs/images/zabob-banner.jpg)
# TODO

## Deferred Tasks

### CI/CD Infrastructure
- [ ] Enable Houdini integration tests in CI environment [#32](https://github.com/BobKerns/zabob-houdini/issues/32)
  - [x] Requires code to locate download links
  - [ ] Configure CI to install Houdini with hython
  - [ ] Set up automated license handling for CI
  - [ ] Create CI workflow that runs integration tests via hython
  - Complex setup for automated testing with hython

### Coverage Integration
- [ ] Replace `_dynamic_import` marker with `print_function` to enable coverage [#33](https://github.com/BobKerns/zabob-houdini/issues/33)
  - Current `_dynamic_import` marker is invalid Python syntax - compiler rejects it
  - `print_function` is valid `__future__` import, no-op in Python 3.11+
  - Would require updating:
    - Marker detection regex in dyn_loader.py
    - AST transformation to look for print_function instead
    - All testing files (11 files in src/testing/h_*.py)
    - Documentation
  - Benefit: Coverage and other tools would work immediately with valid Python syntax
  - Note: Python compiler validates __future__ imports in C code, cannot be patched at runtime

### Future Enhancements
- [ ] Implement argument serialization for hython subprocess calls
- [ ] Add NodeTypeInstance for namespace resolution
- [ ] Context-aware validation (SOPs under geo nodes)
- [ ] Complete package installation system integration
- [ ] Create NodeInstance subtypes to eliminate need for `as_type` parameter
  - Ultimately, the `as_type` parameter won't be necessary as we'll create subtypes of NodeInstance that capture that information, based on parent and node type
  - This will provide automatic type narrowing without requiring explicit type specification

### Node Connection Enhancements
- [x] Support multi-output node connections with `(node, output_index)` tuple syntax
- [x] Test multi-output connection functionality with integration tests
- [x] Test sparse input merging functionality with comprehensive test cases
- [ ] Add validation for output index bounds checking

### Node Placement and Visual Improvements
- [ ] Create our own placement algorithm to replace moveToGoodPosition()
  - Current usage of moveToGoodPosition() is really ugly
  - Should implement intelligent node positioning based on connection topology

### Context Objects and Scoping
- [ ] Implement Context objects for shared parent and scoping control
  - Context objects hold a shared parent node reference
  - Provide `.node()` and `.chain()` methods that call top-level functions with context
  - Control scoping for layout algorithms and name lookup resolution
  - Enable hierarchical organization of node creation
  - Subclasses provide type safety for what kinds of nodes can be contained within other nodes
    - Example: `SopContext` ensures only SOP nodes can be created within geometry containers
    - Example: `ObjContext` manages object-level node creation with appropriate constraints

### Enhanced Copy Operations
- [ ] Extend `copy()` methods to support comprehensive modifications
  - Allow different inputs when copying NodeInstance or Chain objects
  - Support alterations to the sequence of nodes within chains during copy
  - Enable modification of node attributes during the copy process
  - Provide fluent API for chaining copy modifications
  - Examples:
    - `node.copy(_inputs=[new_input], attributes={'tx': 5})`
    - `chain.copy("name2", 1, node(geo, "attribwrangle"), 3, _inputs=[alt_input])`

    The arguments can refer to nodes by name, index, or supply a new NodeInstance.

### Dynamic Import Configuration System
- [ ] **HIGH PRIORITY**: Add configurable control over which imports use dynamic loading
  - Current behavior: All imports dynamically loaded when `from __future__ import _dynamic_import` is present
  - Problem 1: External imports (e.g., `import numpy`) add unnecessary overhead to every variable access
  - Problem 2: **Debugger usability** - stepping through code unexpectedly steps into deferred import machinery
  - Solution: Package-level configuration to specify which imports should be dynamic
  - **Immediate workaround**: Limit dynamic imports to only `zabob_houdini.*` by default

  **Proposed API:**
  ```python
  # In __dynamic__.py configuration file
  from zabob_houdini.dyn_import import dyn_configure

  dyn_configure('my_package.*', include=(...), exclude=(...))
  ```

  **Configuration Sources:**
  1. `__dynamic__.py` file in package (standard approach)
  2. Environment variable for post-packaging optimization:
     ```bash
     PYTHON_DYNAMIC_ENABLE_SOME_PACKAGE=/path/to/alternate/__dynamic__.py
     ```

  **Default Behavior:**
  - If `from __future__ import _dynamic_import` is present, enable for all imports (current behavior)
  - Configuration file can:
    - Enable dynamic imports for entire packages
    - Limit scope with include/exclude patterns (standard glob semantics)
    - Override per-package or per-module

  **Use Cases:**
  - Only make internal package imports dynamic (break circular deps)
  - Keep external library imports (numpy, requests) as regular imports (no overhead)
  - Enable for specific modules known to have circular dependency issues

  **Implementation Notes:**
  - Configuration loaded by DynamicImportTransformer before transformation
  - Pattern matching during AST traversal to decide which imports to transform
  - Falls back to current "transform all" behavior if no configuration present

  **Configuration File Locations (checked in order):**
  1. `__dynamic__.py` in package root (alongside `__init__.py`)
  2. `pyproject.toml` section: `[tool.zabob_houdini.dynamic_import]`
  3. Environment variable: `PYTHON_DYNAMIC_CONFIG=/path/to/config.py`

  **Pattern Matching:**
  - Glob patterns: `zabob_houdini.*`, `mypackage.core.*`
  - Specific modules: `zabob_houdini.core`, `zabob_houdini.core_node`
  - Include/exclude precedence: exclude takes priority over include
  - Default if no patterns: transform all (current behavior)

  **Quick Fix for Development:**
  - Add hardcoded default in `DynamicImportTransformer.__init__`:
    ```python
    self.include_patterns = ['zabob_houdini.*']  # Only transform internal imports
    ```
  - This immediately fixes debugger stepping issue without full config system

### Circular Graph Construction
- [ ] Implement circular graph support
  - Allow forward references to nodes not yet defined
  - Enable creating cycles in node networks (e.g., feedback loops)
  - Handle dependency resolution for circular dependencies
  - Prevent infinite loops during node creation

### Begin/End Loop Construction
- [ ] Add support for begin/end loop patterns
  - Implement constructs for for-each loops over geometry
  - Support while loops and conditional iteration
  - Provide clean API for loop body definition
  - Handle automatic begin/end node creation and wiring

### Jupyter Integration
- [ ] Create hython/Jupyter kernel for notebook support
  - Investigate IPython kernel protocol compatibility with hython
  - Implement kernel wrapper that launches hython subprocess
  - Handle hou module imports and state management across cells
  - Enable interactive Houdini scene manipulation from notebooks
  - Document setup process for developers

### Qt Module Stubs Completion
- [x] Added comprehensive methods for ColorPalette class (14 methods)
- [x] Added comprehensive methods for ListEditor class (40+ methods)
- [x] Added comprehensive methods for InputField class (15 methods)
- [x] Added comprehensive methods for FileChooserButton class (8 methods)
- [x] Added comprehensive methods for Icon class (enhanced \__init\__)
- [x] Added comprehensive methods for ParmDialog class (7 methods)
- [x] Added comprehensive methods for ViewerOverlay class (15 methods)
- [x] Added comprehensive methods for WindowOverlay class (5 methods)
- [x] Added comprehensive methods for XMLMenuParser class (8 methods)
- [x] Added all enum values for mimeType module (21 values)
- [x] Qt module now complete with all major classes expanded
  - ColorSwatchButton, ComboBox, Dialog, FieldLabel
  - FileChooserButton, FileLineEdit, GridLayout, HelpButton
  - Icon, Menu, MenuBar, MenuButton
  - NodeChooserButton, ParmChooserButton, ParmDialog, ParmTupleChooserButton
  - SearchLineEdit, Separator, ToolTip, TrackChooserButton
  - ViewerOverlay, Window, WindowOverlay, XMLMenuParser
  - Each class needs methods fetched from Sidefx documentation
  - Priority: Classes with extensive custom methods beyond Qt base classes
