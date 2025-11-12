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

### Node Connection Enhancements
- [x] Support multi-output node connections with `(node, output_index)` tuple syntax
- [x] Test multi-output connection functionality with integration tests
- [x] Test sparse input merging functionality with comprehensive test cases
- [ ] Add validation for output index bounds checking
