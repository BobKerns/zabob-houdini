# Zabob-Houdini, a simple API for creating Houdini node graphs

## Basics

The core function is `node`, which takes a parent, a `NodeType`, an optional name, and keyword attributes for the node. A NodeInstance is returned.

The parent can be:

- A literal path string such as `"/obj"`
- A more general node path string like `"/obj/geo1"`
- An actual Houdini node object

Special keyword attributes include `_input`, which supply 0 or more input nodes to connect.

The function `chain` takes a parent node (as for node), a sequence of nodes (NodeInstance objects, actual Houdini nodes, or Chain objects), and connects them in a linear graph. Chain objects are copied and spliced into the sequence. It takes a _input argument, allowing it to be directly connected to another node. The purpose of `chain` is to simplify the common case of a linear sequence of nodes. A Chain is returned.

A Chain object is indexable:

- **By integer**: `chain[0]` returns the first node in the chain
- **By slice**: `chain[1:3]` returns a new Chain with the subset of nodes
- **By name**: `chain["nodename"]` returns the node with that name

A `NodeInstance` or `Chain` is instantiated by calling the `.create` method.

## Example Usage

```python
from zabob_houdini import node, chain

# Create a geometry container in /obj
geo_node = node("/obj", "geo", name="mygeometry")

# Create individual SOP nodes
box_node = node(geo_node, "box", name="mybox")
transform_node = node(geo_node, "xform", name="mytransform", _input=box_node)

# Or create a chain of nodes for linear processing
box_node2 = node(geo_node, "box", name="source")
xform_node = node(geo_node, "xform", name="transform")
subdivide_node = node(geo_node, "subdivide", name="refine")
processing_chain = chain(geo_node, box_node2, xform_node, subdivide_node)

# Chains can also include other chains (spliced in)
detail_chain = chain(geo_node,
                    node(geo_node, "normal"),
                    processing_chain,  # This chain is spliced in
                    node(geo_node, "output"))

# Access nodes in the chain
first_node = processing_chain[0]              # First node (source box)
subset_chain = processing_chain[1:3]          # New Chain with subset (transform, refine)
named_node = processing_chain["transform"]    # Node by name

# Create the nodes in Houdini
geo_instance = geo_node.create()
box_instance = box_node.create()
transform_instance = transform_node.create()
chain_instance = processing_chain.create()
```

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

### Houdini Integration

#### For VS Code IntelliSense

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

#### Using with Houdini

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
   /path/to/houdini/python -m pip install zabob-houdini
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
- Setting up `.pth` files and environment variables is fragile and unreliable### VS Code Configuration

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

### Code Spell Checking (cSpell)

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

### Markdown Linting

The project uses markdownlint for consistent markdown formatting:

- **Configuration**: `.markdownlint.json` and VS Code settings suppress overly strict rules (MD021, MD022)
- **VS Code Integration**: Automatic linting as you edit markdown files
- **Rules disabled**: MD013 (line length), MD021/MD022 (heading spacing), MD031/MD032 (block spacing) for better readability

## Publishing to PyPI

This package is automatically published to PyPI using GitHub Actions. For detailed setup instructions, see [docs/PYPI_SETUP.md](docs/PYPI_SETUP.md).

### Quick Start

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

### Installation from PyPI

Once published, users can install with:

```bash
# Using pip
pip install zabob-houdini

# Using uv
uv add zabob-houdini
```
