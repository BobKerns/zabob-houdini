# Copilot Instructions for Zabob-Houdini

## Project Overview
Zabob-Houdini is a Python API for creating Houdini node graphs programmatically. This is an early-stage project that provides a simplified interface for building and connecting Houdini nodes.

## Core Architecture Concepts

### Node Graph API Design
- **`node()`** function: Core API for creating individual nodes
  - Takes `NodeType`, optional name, and keyword attributes
  - Returns `NodeInstance` objects
  - Special `_input` keyword connects 0+ input nodes
- **`chain()`** function: Creates linear node sequences
  - Connects nodes in sequence automatically
  - Accepts `_input` for external connections
  - Can be nested/spliced into other chains
  - Returns `Chain` objects
- **Instantiation Pattern**: Both `NodeInstance` and `Chain` use `.create()` method for actual creation

### Project Structure
- `src/zabob_houdini/`: Main package directory
- Currently minimal implementation - most API described in README is not yet implemented
- Uses modern Python packaging with `pyproject.toml` and hatchling

## Development Conventions

### Python Standards
- **Compatibility**: Requires Python 3.13+ (pyproject.toml), but developed with Python 3.14 (`.python-version`)
- **Future type annotations**: May require Python 3.14+ features eventually, but maintains 3.13+ compatibility for now
- **Houdini integration**: Leverages Houdini's modern virtual environment and Python support
- **Legacy concerns**: Houdini's historical dependence on older Python versions has been problematic; using 3.14 helps surface any remaining compatibility issues (e.g., with `hython`)
- Entry point: `zabob_houdini:main` console script
- **CLI framework**: Uses Click instead of argparse for command-line interface
- **Type hints**: Use modern built-in types (`list`, `dict`, `tuple`) instead of `typing.List`, etc.
- **Docstrings**: Write comprehensive docstrings for all public functions and classes
- **Modern constructs**: Use dataclasses, match statements, and other Python 3.13+ features
- **Parameter typing**: Declare all parameter types explicitly

### Key Files to Understand
- `README.md`: Contains the complete API specification and usage patterns
- `src/zabob_houdini/__init__.py`: Current minimal implementation
- `pyproject.toml`: Project configuration and dependencies
- `.gitignore`: Python and Houdini-specific ignore patterns
- `.gitattributes`: LFS configuration for Houdini binary files
- `.env.example.*`: Platform-specific environment variable templates (users copy to `.env`)
- `stubs/hou.pyi`: Type stubs for Houdini's `hou` module for development IntelliSense

## Implementation Notes

### Current State
The project is in early development - the README describes the intended API, but implementation is minimal (just a hello world function). When implementing:

1. **Follow the README specification exactly** - it defines the expected behavior
2. **Implement the `node()` and `chain()` functions** as the core API
3. **Create `NodeInstance` and `Chain` classes** with `.create()` methods
4. **Handle the `_input` keyword parameter** for node connections
5. **Start with string-based NodeType** (SOP node names like "box", "merge")
6. **Defer `hou` module calls** - only execute during `.create()`, not during node definition
7. **Plan for NodeTypeInstance expansion** - namespace resolution for duplicate names across categories

### Integration Considerations
- **Abstraction Layer**: This is a Python wrapper that calls Houdini's `hou` module during `.create()` execution
- **Houdini Python compatibility**: Watch for potential issues with `hython` and other Houdini Python tools due to historical version constraints
- **NodeType Implementation**:
  - Initially: strings representing SOP node type names (e.g., "box", "merge", "transform")
  - Future: `NodeTypeInstance` objects to resolve namespace conflicts across categories
  - Long-term: Context-aware validation (e.g., SOPs under `geo` nodes)
- **Creation Pattern**: Nodes are defined declaratively, then `.create()` calls `hou` module functions

## Testing & Development
- **Testing**: Uses pytest framework for testing
- **Package management**: Uses UV - always run `uv sync` after modifying dependencies in pyproject.toml
- **Code organization**: Consider dataclasses for structured data (e.g., node configurations)
- **Modern Python**: Leverage Python 3.13+ features like improved type hints and pattern matching
- No CI/CD setup yet - runs as console application via entry point
- Development should focus on implementing the API described in README.md first

## VS Code Configuration Management
- **Personal Settings**: `.vscode/settings.json` is personal (not committed) and created from `.vscode/settings.json.example`
- **Template Sync**: When `.vscode/settings.json` is modified with project-relevant changes, remind the user to update `.vscode/settings.json.example` for other contributors
- **Project Files**: `.vscode/project-dictionary.txt`, `.vscode/extensions.json`, and `.vscode/setup-vscode.sh` are committed
- **Setup Script**: New contributors use `./.vscode/setup-vscode.sh` for automated setup
- **Spell Checking**: Uses cSpell with project dictionary - add technical terms to `.vscode/project-dictionary.txt`
