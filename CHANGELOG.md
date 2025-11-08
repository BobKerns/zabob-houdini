# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Core `node()` and `chain()` API functions
- `NodeInstance` and `Chain` classes with `.create()` methods
- Comprehensive Houdini type stubs with modern Python types
- VS Code development environment setup
- cSpell spell checking configuration
- Comprehensive test suite with mocked Houdini integration
- CLI tools for validation and testing
- GitHub workflow for PyPI publishing

### Changed
- Migrated from legacy typing imports to modern built-in types
- Enhanced parameter setting to use `setParms()` for better performance

### Technical
- Python 3.13+ compatibility with 3.14 development environment
- UV package manager integration
- Modern Python packaging with hatchling
- Hand-maintained Houdini type stubs for better IDE support

## [0.1.0] - 2025-11-07

### Added
- Initial project structure
- Basic API design and documentation
- Development environment setup

[Unreleased]: https://github.com/BobKerns/zabob-houdini/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/BobKerns/zabob-houdini/releases/tag/v0.1.0
