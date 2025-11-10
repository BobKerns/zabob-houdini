# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-11-09

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
[0.1.1]: https://github.com/BobKerns/zabob-houdini/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/BobKerns/zabob-houdini/releases/tag/v0.1.0
