# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New `NodeContext` class for organizing nodes under a specific parent
  - Context manager protocol for convenient use with `with` statements
  - `node()` method creates nodes under the context's parent without specifying parent
  - `chain()` method creates chains with string name lookup for existing context nodes
  - Named node registration and lookup: `ctx["node_name"]` retrieves nodes by name
  - Dictionary-style access to named nodes created within the context
  - Automatic registration of new chain nodes (preserves existing context nodes)
- New `context()` function for creating NodeContext instances
  - Accepts NodeInstance, string path, or hou.Node as parent
  - Wraps non-NodeInstance parents automatically for consistent interface
  - Returns NodeContext that can be used as context manager
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

### Changed
- `Chain.copy()` method signature enhanced with `*copy_params: ChainCopyParam` parameter
- Simplified implementation using `self[param]` for uniform int/str handling
- Updated API.md with comprehensive examples for all copy parameter types
- Enhanced test coverage for name-based access and NodeInstance insertion

### Documentation
- Chain reordering patterns section with practical examples
- Detailed `Chain.copy()` parameter documentation and signature
- Advanced patterns covering reverse processing, partial extraction, and node duplication

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
