# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive API documentation (API.md) with 500+ lines covering all public interfaces
- Type safety documentation with `as_type` parameter usage and benefits
- Display and render flag support for node creation (`_display`, `_render` parameters)
- Enhanced immutability explanations in README.md highlighting safety, caching, and template benefits
- Future enhancement planning for context objects and enhanced copy operations

### Changed
- README.md restructured to be high-level focused with clear link to comprehensive API docs
- Improved code organization with `wrap_node` functionality cleanup
- Enhanced TODO.md with detailed roadmap for context objects and copy operation extensions

### Documentation
- Complete function signatures and parameter documentation for `node()` and `chain()`
- Detailed class documentation for `NodeInstance` and `Chain` with all methods and properties
- Comprehensive usage examples including multi-output connections, chain indexing, and type narrowing
- Registry system documentation for node-to-instance mapping
- Best practices and patterns for immutable node graph creation

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
