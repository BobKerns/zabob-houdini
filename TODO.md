![Zabob Banner](docs/images/zabob-banner.jpg)
# TODO

## Deferred Tasks

### CI/CD Infrastructure
- [ ] Install Houdini in CI environment
  - [x] Requires code to locate download links
  - Complex setup for automated testing with hython

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
