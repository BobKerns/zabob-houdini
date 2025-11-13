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
