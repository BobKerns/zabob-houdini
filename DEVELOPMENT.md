![Zabob Banner](docs/images/zabob-banner.jpg)
# Development Guide

This document contains detailed information for developers working on Zabob-Houdini.

## Development Setup

### Prerequisites

This project uses [UV](https://docs.astral.sh/uv/) for Python package management. Install UV first:

**macOS and Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative installation methods:** See the [UV installation guide](https://docs.astral.sh/uv/getting-started/installation/)

### Development Workflow

**Recommended two-phase approach:**

#### Phase 1: Development with Modern Python

```bash
# Use modern Python tooling for development
uv sync                           # Install with latest Python
uv run pytest tests/             # Run tests
uv run zabob-houdini validate     # Test CLI
```

#### Phase 2: Integration with Houdini

```python
# Copy your zabob-houdini code into Houdini contexts:
# - Python shelf tools
# - HDA Python scripts
# - Houdini's Python shell

from zabob_houdini import node, chain
# This works within Houdini's Python environment
```

### Python Version Compatibility

**Important:** This project supports Python 3.11+ for general use, but Houdini constrains you to its bundled Python:

- **Houdini 20.5-21.x**: Python 3.11 (current limitation)
- **Houdini 22.x+**: Expected to support newer Python versions (anticipated early 2025)
- **Development**: Use any Python 3.11+ for testing and development

**For Houdini-compatible development**, you can use the provided Python version pin:
```bash
cp .python-version-houdini .python-version  # Pin to Python 3.11 for Houdini compatibility
uv sync  # Will use Python 3.11
```

### Setting up the Virtual Environment

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd zabob-houdini
   ```

2. **Create the virtual environment and install dependencies:**

   ```bash
   uv sync
   ```

   This will:

   - Create a virtual environment with Python 3.13+
   - Install all project dependencies
   - Install the project in development mode

3. **Activate the virtual environment** (optional, UV handles this automatically):

   ```bash
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

## Testing

The project uses a two-tier testing approach to support both local development and CI:

**Quick Test Commands:**

```bash
./test.sh unit          # Unit tests (no Houdini required)
./test.sh integration   # Integration tests (requires Houdini)
./test.sh all          # All tests
./test.sh list         # List all available tests
```

**Manual Testing:**

```bash
# Unit tests only (runs in CI)
uv run pytest -m "unit and not integration" -v

# Integration tests (requires Houdini)
uv run pytest -m "integration" -v

# All tests
uv run pytest -v
```

**Test Categories:**

- **Unit Tests** (`@pytest.mark.unit`): Bridge functionality, utilities, basic imports
  - Run without Houdini installation
  - Fast execution (< 1 second)
  - Used in CI/CD pipelines

- **Integration Tests** (`@pytest.mark.integration`): Core API functionality
  - Require Houdini installation and `hython` binary
  - Test actual node creation and graph building
  - Run locally or in specialized CI environments

**CI/CD:**

- **Pull Requests**: Run unit tests on Python 3.11, 3.12, 3.13
- **Releases**: Run unit tests + linting + spell checking
- **Integration tests**: Run manually or on `main` branch with special label

## CLI Architecture Pattern

The zabob-houdini CLI uses a bridge pattern to execute commands in both regular Python and Houdini's `hython` environment:

### Bridge Pattern Implementation

**1. CLI Entry Point (cli.py):**
- Uses Click for command structure
- Commands decorated with `@houdini_command` automatically dispatch to `hython`
- Regular Python commands work normally; Houdini-specific commands are bridged

**2. Houdini Implementation (houdini_info.py):**
- Contains the actual command logic that runs in Houdini
- Uses Click groups and commands that execute within `hython`
- Processes Houdini objects and data structures

**3. Bridge Mechanism:**
- `@houdini_command` decorator intercepts CLI calls
- Launches `hython -m zabob_houdini _exec <module> <function> <args>`
- Returns structured JSON results back to the CLI

### Example: Adding a New Python Info Command

These directions apply for commands which must run in a Houdini environment.  They will launch hython to perform the command if run in ordinary python.

#### Step 1: Add command to houdini_info.py

`houdini_info.py` holds code which runs in the Houdini environment.

```python
@info.command('types')
@click.argument('category', type=str, required=True)
def types(category: str):
    """List node types in the specified category."""
    for item in analyze_categories():
        if isinstance(item, NodeTypeInfo) and item.category.lower() == category.lower():
            click.echo(f"  {item.name}: {item.description}")
```

#### Step 2: Add bridge command to cli.py

This file gets a stub that runs hython with the same arguments. The mechanics for this are added by the `@houdini_command` decorator. The this should take the same arguments and options as the real command in `houdini_info.py`.

```python
@info.command('types')
@houdini_command
@click.argument('category', type=str, required=True)
def types(category: str) -> None:
    """List node types in the specified category."""
    pass  # Implementation handled by bridge
```

### Benefits

- **Dual Environment**: Same CLI works in both Python and Houdini contexts
- **Type Safety**: Full typing support for development in regular Python
- **Clean Separation**: Business logic separated from CLI bridging logic
- **Extensible**: Easy to add new commands following the same pattern

## Release Management

**Quick Release Commands:**

```bash
./release.sh status      # Check current version and git status
./release.sh test        # Test release workflow (TestPyPI)
./release.sh bump patch  # Bump version (patch/minor/major)
./release.sh release     # Create production release
```

**Release Workflow:**

1. **Test Release to TestPyPI:**
   ```bash
   ./release.sh test                    # Test current version
   # OR
   ./release.sh bump patch && ./release.sh test  # Bump and test
   ```
   - Go to [GitHub Actions](https://github.com/BobKerns/zabob-houdini/actions/workflows/publish.yml)
   - Click "Run workflow" → Select "testpypi"
   - Test install: `pip install -i https://test.pypi.org/simple/ zabob-houdini`

2. **Production Release to PyPI:**
   ```bash
   ./release.sh bump patch              # Update version
   git add pyproject.toml && git commit -m "Bump version to X.Y.Z"
   ./release.sh release                 # Create tag and push (auto-publishes)
   ```
   - Creates git tag → triggers automated PyPI release
   - Generates GitHub Release with artifacts

**Manual Release (GitHub UI):**
- Go to [GitHub Actions](https://github.com/BobKerns/zabob-houdini/actions/workflows/publish.yml)
- Click "Run workflow"
- Select repository: `testpypi` or `pypi`

## Houdini Integration

### For VS Code IntelliSense

For VS Code IntelliSense to work with Houdini's `hou` module, copy the appropriate platform-specific example file to `.env`:

**macOS:**

```bash
cp .env.example.macos .env
```

**Linux:**

```bash
cp .env.example.linux .env
```

**Windows (PowerShell):**

```powershell
Copy-Item .env.example.windows .env
```

**Windows (Command Prompt):**

```cmd
copy .env.example.windows .env
```

Each example file contains common installation paths for that platform. Edit `.env` if your Houdini installation is in a different location.

### Using with Houdini

**Important:** Due to Houdini's architecture, `hython` has severe compatibility issues with virtual environments, UV, and modern Python tooling. The linked symbol requirements make it extremely difficult to use external Python packages reliably.

**Recommended approach for Houdini integration:**

1. **Development and Testing:**
   ```bash
   # Use regular Python for development
   uv run zabob-houdini info
   uv run python -c "from zabob_houdini import node; print('API works!')"
   ```

2. **Production Use within Houdini:**
   ```python
   # Install in Houdini's Python environment
   # Within Houdini's Python shell or scripts:
   import sys
   sys.path.append('/path/to/your/project/src')
   from zabob_houdini import node, chain

   # Create nodes within Houdini
   geo_node = node("/obj", "geo", name="mygeometry")
   result = geo_node.create()  # This works within Houdini
   ```

3. **Alternative Installation:**
   ```bash
   # Install package directly in Houdini's Python
   /path/to/houdini/hython -m pip install zabob-houdini
   ```

**Where to use zabob-houdini in Houdini:**
- **Python shelf tools**: Create custom shelf buttons with zabob-houdini code
- **HDA script sections**: Use in digital asset Python callbacks
- **Houdini Python shell**: Interactive development within Houdini
- **Python SOP/TOP nodes**: For procedural workflows

**Why hython is problematic:**
- Requires linked symbols that conflict with virtual environments
- Cannot reliably import packages from external Python environments
- UV and pip installations don't work correctly with hython
- Setting up `.pth` files and environment variables is fragile and unreliable

## VS Code Configuration

The project includes VS Code configuration for optimal development experience:

**Quick Setup (Recommended):**

```bash
# Automated setup script
./.vscode/setup-vscode.sh
```

**Manual Setup:**

```bash
# Copy the example settings to create your personal settings
cp .vscode/settings.json.example .vscode/settings.json
```

**What's included in the example settings:**

- **cSpell Integration**: Project dictionary for spell checking
- **Python Environment**: Automatic virtual environment detection
- **Houdini Integration**: Path to Houdini Python libraries for IntelliSense
- **Type Stubs**: Enhanced Houdini type hints from `stubs/` directory

**Personal Overrides:**

Your personal `.vscode/settings.json` won't be committed, so you can safely add:

```jsonc
{
    // Project settings (from example) - keep these for best experience
    "cSpell.customDictionaries": { /* ... */ },
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",

    // Add your personal preferences
    "editor.fontSize": 14,
    "editor.theme": "your-favorite-theme",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

**Alternative: Workspace-only settings:**

If you prefer not to modify your personal settings, you can create a workspace-specific configuration by pressing `Ctrl/Cmd + Shift + P` and selecting `Preferences: Open Workspace Settings (JSON)`.

**Why this approach?**

- **No forced settings**: Your personal VS Code preferences won't be overridden
- **Easy onboarding**: New contributors can get started quickly with the setup script
- **Shared essentials**: Project-specific configurations (dictionaries, paths) are shared
- **Personal freedom**: Add your own preferences without affecting others

## Code Spell Checking (cSpell)

The project includes spell checking configuration for VS Code and command-line tools:

- **Dictionary**: `.vscode/project-dictionary.txt` contains project-specific words
- **Configuration**: `cspell.json` provides comprehensive spell checking settings
- **VS Code Integration**: Words are automatically validated as you type

**Adding new words to the dictionary:**

1. In VS Code, right-click on a misspelled word and select "Add to project dictionary"
2. Or manually add words to `.vscode/project-dictionary.txt` (one word per line)
3. Or use the command line:

   ```bash
   echo "yourword" >> .vscode/project-dictionary.txt
   ```

**Running spell check manually:**

```bash
# Using npm scripts (recommended)
npm install                      # Install cSpell first
npm run spell-check              # Check all files (quiet)
npm run spell-check-files        # Check with file context
npm run spell-check-verbose      # Check with verbose output

# Or using npx directly
npx cspell "**/*.{py,md,txt,json}"  # Check all files
npx cspell README.md                # Check specific file
```

**Note**: The spell checker is configured to ignore common paths like `.venv/`, `__pycache__/`, and build directories.

## Markdown Linting

The project uses markdownlint for consistent markdown formatting:

- **Configuration**: `.markdownlint.json` and VS Code settings suppress overly strict rules (MD021, MD022)
- **VS Code Integration**: Automatic linting as you edit markdown files
- **Rules disabled**: MD013 (line length), MD021/MD022 (heading spacing), MD031/MD032 (block spacing) for better readability

## Publishing to PyPI

This package is automatically published to PyPI using GitHub Actions. For detailed setup instructions, see [docs/PYPI_SETUP.md](docs/PYPI_SETUP.md).

**For releases:**
1. Create and push a version tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```
2. The workflow automatically:
   - Runs tests and checks
   - Builds the package
   - Publishes to PyPI
   - Creates a GitHub release

**For testing:**
1. Use the manual workflow dispatch in GitHub Actions
2. Select "testpypi" to publish to Test PyPI first
3. Verify the package works correctly
