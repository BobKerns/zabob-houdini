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

### Test Architecture

Zabob-houdini uses a **split testing architecture** to handle Houdini's Python environment requirements:

- **[tests/README.md](tests/README.md)**: Pytest side - orchestrates test execution without importing `hou`
- **[src/testing/README.md](src/testing/README.md)**: Hython side - implements tests that run in Houdini's environment

This separation is necessary because importing `hou` outside of Houdini causes segmentation faults. See the README files above for detailed guidance on writing tests.

### Running Tests

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

### Debugging

Because most of the tests do their work in a `hython` subprocess, it is challenging to debug what happens during a test.

#### VS Code Launch Configurations and Tasks

The project includes dynamic launch configurations and tasks for working with hython:

**Launch Configurations (Debug → Start Debugging or F5):**

1. **Debug Houdini Test Function**: Select from a dropdown of test functions and debug them directly in hython
2. **Debug Houdini Example**: Select and debug example files under hython
3. **Hython Debugger: Current File**: Debug the currently open file in hython

**Tasks (Terminal → Run Task):**

1. **Setup VS Code Workspace**: Run the setup script to initialize development environment
2. **Run Houdini Example (Save HIP)**: Run an example file and save the resulting scene to `hip/<basename>.hip`
   - Prompts for example selection from dropdown
   - Uses `zabob-houdini run` command with `--hipfile` option
   - Useful for generating HIP files to inspect results

**Smart Launcher Behavior:**

The debug launchers automatically track your last-used test/example:
- First run shows `__initialize__` placeholder (run setup task to populate)
- After selecting a test/example, it becomes the default (first in list)
- Next debug session: just hit Enter to re-run the same test/example
- Press Escape to cancel without running anything
- Option lists are stored in `.vscode/tmp/` and auto-generated

To use the launchers:

1. Install the recommended Command Variable extension when prompted
2. Run the "Setup VS Code Workspace" task (first time only)
3. For debugging: Press F5 or use Run → Start Debugging
4. Select the test function or example file from the dropdown (or hit Enter for last-used)
5. Set breakpoints in test functions in the `src/testing/` directory

This allows direct stepping through the Houdini-side test code, which is much more effective than debugging the pytest wrapper.

#### Pytest Stack Trace Integration

When tests fail, pytest includes the complete hython stack trace with **clickable file links** in VS Code's Test Results view, making it easy to navigate directly to the error location.

Example failure output:

```text
=================================== FAILURES ===================================
______________ TestContextFunction.test_node_context_merge_method ______________
tests/test_node_context.py:120: in test_node_context_merge_method
    result = hython_test("_test_node_context_merge_method")
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/conftest.py:102: in run_houdini_test
    pytest.fail(msg)
E   Failed: hython test _test_node_context_merge_method failed:
E   Error executing testing._node_context._test_node_context_merge_method: Node at path 'my_box' does not exist.
E
E   ------Hython Error Traceback------
E     File "/Users/rwk/p/zabob-houdini/src/testing/_node_context.py", line 290, in _test_node_context_merge_method
E       merge_node = ctx.merge("my_box", "my_sphere", name="test_merge")
E                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E     File "/Users/rwk/p/zabob-houdini/src/zabob_houdini/core_context.py", line 329, in merge
E       return self.node("merge", name, _input=list(inputs), **attributes)
E              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E     File "/Users/rwk/p/zabob-houdini/src/zabob_houdini/core_context.py", line 168, in node
E       inputs = cnode._wrap_inputs(_input, self)
E                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E     File "/Users/rwk/p/zabob-houdini/src/zabob_houdini/core_node.py", line 885, in _wrap_inputs
E       return tuple(_wrap_input(inp, 0) for inp in inputs)
E              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E     File "/Users/rwk/p/zabob-houdini/src/zabob_houdini/core_node.py", line 885, in <genexpr>
E       return tuple(_wrap_input(inp, 0) for inp in inputs)
E                    ^^^^^^^^^^^^^^^^^^^
E     File "/Users/rwk/p/zabob-houdini/src/zabob_houdini/core_node.py", line 955, in _wrap_input
E       wrapped = _wrap_single_input(input)
E                 ^^^^^^^^^^^^^^^^^^^^^^^^^
E     File "/Users/rwk/p/zabob-houdini/src/zabob_houdini/core_node.py", line 937, in _wrap_single_input
E       return wrap_node(hou_node(input), )
E                        ^^^^^^^^^^^^^^^
E     File "/Users/rwk/p/zabob-houdini/src/zabob_houdini/core_utils.py", line 18, in hou_node
E       raise ValueError(f"Node at path '{path}' does not exist.")
E
E   ------ Location (Test, Error) ------
E   Tst> "src/testing/_node_context.py:278", in _test_node_context_merge_method
E   Err> "src/zabob_houdini/core_utils.py:18", in hou_node
--------------------------- Captured stderr teardown ---------------------------
Saved HIP file: hip/_test_node_context_merge_method.hip
=========================== short test summary info ============================
FAILED tests/test_node_context.py::TestContextFunction::test_node_context_merge_method
============================== 1 failed in 1.67s ===============================
Finished running tests!
```

**Key features:**

- **Full traceback**: Complete call stack from inside the hython subprocess, filtered to show relevant frames
- **Clickable links**: File paths in VS Code's terminal are clickable - jump directly to the error location
- **Location markers**:
  - `Tst>` points to where the test function is defined (where to add breakpoints)
  - `Err>` points to where the actual error occurred in the implementation
- **Context preservation**: Shows the exact line of code and surrounding call chain that led to the failure

#### HIP File Inspection

If you have a directory named `hip/` in your working directory, the tests will write out hip files when they finish. This allows you to inspect the Houdini environment with the Houdini editor, or explore the final state interactively with the Houdini python shell. The directory to use can be overridden with the `TEST_HIP_DIR` environment variable, or suppressed by setting it to the empty string or a directory which does not exist. The `hip` directory does not exist in CI so it is not written in that context.

**CI/CD:**

- **Pull Requests**: Run unit tests on Python 3.11, 3.12, 3.13
- **Releases**: Run unit tests + linting + spell checking
- **Integration tests**: Run manually or on `main` branch with special label

## CLI Architecture Pattern

The zabob-houdini CLI uses a bridge pattern to execute commands in both regular Python and Houdini's `hython` environment. For complete CLI usage documentation, see **[Command Line Interface](COMMAND.md)**.

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

**Development Workflow:**

For development, install zabob-houdini as a Houdini package pointing to your worktree's `src/` directory:

```bash
# Ensure virtual environment is active and correct
source .venv/bin/activate  # or activate.bat on Windows

# Install package pointing to current worktree's src/
zabob-houdini install-package

# Verify installation points to correct location
zabob-houdini diagnose
```

This creates a Houdini package JSON that adds your worktree's `src/` directory to Houdini's PYTHONPATH, allowing you to:
- Test changes immediately in Houdini without reinstalling
- Debug code in your active worktree
- Run examples and tests with `hython`

**⚠️ Important for Git Worktrees:**

Each worktree needs its own virtual environment. If you see the wrong code running:

1. **Check with diagnostics:**
   ```bash
   zabob-houdini diagnose
   ```

2. **If venv points to wrong worktree:**
   ```bash
   deactivate 2>/dev/null  # Exit venv if active
   rm -rf .venv            # Remove incorrect venv
   uv sync                 # Create new venv for this worktree
   ```

3. **Reinstall package:**
   ```bash
   source .venv/bin/activate
   zabob-houdini install-package  # Points to current worktree's src/
   ```

The package installation is global to Houdini but can be overwritten - just run `zabob-houdini install-package` from the worktree you want to use. No need to uninstall first.

**Production Use:**

For production use outside of development, use `uvx` to install and run zabob-houdini commands. This automatically handles virtual environment creation and other installation gotchas:

```bash
# Install and run zabob-houdini using uvx (recommended)
uvx zabob-houdini install-package

# Or use with any other zabob-houdini command
uvx zabob-houdini diagnose
uvx zabob-houdini run examples/diamond_chain_demo.py
```

Alternatively, you can install directly into Houdini's Python environment:

```bash
# Install into Houdini's Python (alternative method)
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
# Python script (cross-platform, recommended)
python .vscode/setup.py

# Or use the VS Code task: Terminal → Run Task → "Setup VS Code Workspace
```

This setup automatically:
- Configures git to exclude personal VS Code files (`.git/info/exclude`)
- Creates `.env` from platform-specific example
- Generates initial debug launcher option lists with `__initialize__` placeholders
- Attempts to populate option lists if `zabob-houdini` is already installed

The Python script is cross-platform and can be run from any directory within the workspace - it will automatically find the workspace root.

### Git Exclude Configuration

The setup script uses `.git/info/exclude` (instead of `.gitignore`) to exclude personal VS Code files:

- **Files excluded**: `.vscode/settings.json`, `.vscode/tasks.json`, `.vscode/launch.json`
- **Why `.git/info/exclude`**: This is a personal exclude file (not shared via git) that prevents your customizations from being committed while keeping the base configurations available for all contributors
- **Benefits**:
  - No risk of accidentally committing personal settings
  - No need to maintain separate `.example` files
  - No sync issues between template and personal files
  - Each developer can freely customize their VS Code experience

**Understanding .git/info/exclude:**

Most developers are familiar with `.gitignore`, but `.git/info/exclude` is better for personal exclusions as it itself is not committed:

```bash
# View current exclusions
cat .git/info/exclude

# Manually add files to exclude (setup script does this automatically)
echo ".vscode/settings.json" >> .git/info/exclude
```

The key difference is that `.gitignore` is shared with all developers, while `.git/info/exclude` is personal to your local repository.

**What's included in the base configurations:**

- **cSpell Integration**: Project dictionary for spell checking
- **Python Environment**: Automatic virtual environment detection
- **Houdini Integration**: Path to Houdini Python libraries for IntelliSense
- **Type Stubs**: Enhanced Houdini type hints from `stubs/` directory
- **Dynamic Launch Configs**: Test function and example file selection with Command Variable extension

**Personal Overrides:**

Since your personal VS Code configs are excluded from git, you can safely customize:

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
