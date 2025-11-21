# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Package Structure**: Internal test functions moved to optional `testing` subpackage
  - Normal installations (`pip install zabob-houdini`) no longer include internal Houdini test infrastructure
  - Developers can install testing support with `pip install zabob-houdini[testing]` or `uv sync --extra testing`
  - Reduces package size for end users who don't need test functions

### Added
- New `NodeContext` class for organizing nodes under a specific parent
  - Context manager protocol for convenient use with `with` statements
  - `node()` method creates nodes under the context's parent without specifying parent
  - `chain()` method creates chains with string name lookup for existing context nodes
  - Named node registration and lookup: `ctx["node_name"]` retrieves nodes by name
  - Dictionary-style access to named nodes created within the context
  - Automatic registration of new chain nodes (preserves existing context nodes)
  - Automatic layout application and sink node creation on context exit
- New `context()` function for creating NodeContext instances
  - Accepts NodeInstance, string path, or hou.Node as parent
  - Wraps non-NodeInstance parents automatically for consistent interface
  - Returns NodeContext that can be used as context manager
- New `ChainBuilder` class for enhanced chain construction within contexts
  - Context manager protocol with automatic registration and layout
  - Full Chain compatibility: `__getitem__`, `__len__`, `first`, `last`, `inputs` properties
  - Clean API without node arguments to prevent confusion with `node()` function
  - Seamless integration with existing Chain/ChainBuilder handling functions
- Bidirectional layout algorithm for improved node positioning
  - Upward pass calculates required widths for each layer
  - Downward pass distributes nodes evenly within allocated space
  - Eliminates "downward drift" and left-alignment issues
  - Proper centering of nodes in complex dependency graphs
- Enhanced `NodeInstance.copy()` with comprehensive parameter support
  - `name` parameter for renaming copied nodes
  - `_display` and `_render` parameters for display/render flag control
  - Smart attribute preservation: only creates new dict when modifications provided
- Enhanced `Chain.copy()` with flexible reordering and insertion capabilities
  - New `ChainCopyParam` type supporting `int`, `str`, and `NodeInstance` parameters
  - Index access: `chain.copy(3, 2, 1, 0)` for positional reordering
  - Name access: `chain.copy("cleanup", "input")` for name-based selection
  - NodeInstance insertion: `chain.copy(0, new_node, 1)` for adding new nodes
  - Mixed access: `chain.copy(0, "transform", new_node)` combining all types
- New `merge()` function for creating merge nodes with multiple inputs
  - Convenient shortcut: `merge(box, sphere, tube)` instead of `node(parent, "merge", _input=[...])`
  - Automatic parent validation ensures all inputs have same parent
  - Supports merge node parameters: `merge(box, sphere, tol=0.01)`
- Comprehensive copy operation documentation in API.md with Advanced Patterns section
- Test coverage for enhanced copy functionality including attribute merging and flag control
- Custom `__repr__` methods to prevent circular reference issues in debugging

### Changed
- **BREAKING**: `NodeContext.chain()` method simplified to keyword-only arguments
  - Removed node arguments to eliminate API confusion with `node()` function
  - Always returns `ChainBuilder` for consistent behavior
  - Clean separation of concerns: `node()` for individual nodes, `chain()` for sequences
- `Chain.copy()` method signature enhanced with `*copy_params: ChainCopyParam` parameter
- Simplified implementation using `self[param]` for uniform int/str handling
- Updated API.md with comprehensive examples for all copy parameter types
- Enhanced test coverage for name-based access and NodeInstance insertion
- Layout algorithm upgraded from single-pass to bidirectional for better positioning
- Dependency tracking improved with WeakKeyDictionary for automatic cleanup

### Fixed
- Node positioning algorithm now properly centers nodes in their layers
- Eliminated "downward drift" where nodes would accumulate toward bottom of layout
- Fixed circular reference issues in object string representations
- Resolved API confusion between `ctx.chain()` and `node()` methods
- All 78 tests now passing with clean API and enhanced functionality

### Documentation
- Chain reordering patterns section with practical examples
- Detailed `Chain.copy()` parameter documentation and signature
- Advanced patterns covering reverse processing, partial extraction, and node duplication
- Updated examples to reflect simplified ChainBuilder API

## [0.1.1] - 2025-11-14

### Added
- Automated changelog management with keepachangelog library integration
- Python-based release workflow automation

### Fixed
- Package naming consistency in pyproject.toml dependency groups

## [0.1.0] - 2025-11-09

### Added
- Two-tier testing: unit tests (CI-compatible) + integration tests (Houdini required)
- Test runner script (`./test.sh`) with multiple execution modes
- Release management script (`./release.sh`) for version bumping and publishing
- Comprehensive CI/CD with GitHub Actions
- NodeInstance registry using WeakKeyDictionary for node-to-instance mapping
- Houdini installer download functionality with SideFX authentication
- Automated changelog integration in GitHub releases

### Changed
- Eliminated all test mocking in favor of hython bridge pattern
- Improved lazy imports with dict comprehension and completion flag
- Fixed charset-normalizer compatibility issues with Python 3.14 alpha
- Enhanced type system with CreatableNode vs ChainableNode distinction

### Fixed
- SemVerParamType class method indentation and import issues
- Test architecture to avoid segfaults with hou module imports
- Version parsing in houdini_versions.py script

### Technical
- Pytest markers for test categorization (@pytest.mark.unit, @pytest.mark.integration)
- GitHub Actions status badges and comprehensive CI workflows
- Environment variable documentation in .env.example.* files

## [0.1.0] - 2025-11-07

### Added
- Initial project structure
- Basic API design and documentation
- Development environment setup

[Unreleased]: https://github.com/BobKerns/zabob-houdini/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/BobKerns/zabob-houdini/compare/v0.1.1...v0.1.1
[0.1.0]: https://github.com/BobKerns/zabob-houdini/releases/tag/v0.1.0
