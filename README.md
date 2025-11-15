![Zabob Banner](docs/images/zabob-banner.jpg)
# Zabob-Houdini

[![Tests](https://github.com/BobKerns/zabob-houdini/actions/workflows/test.yml/badge.svg)](https://github.com/BobKerns/zabob-houdini/actions/workflows/test.yml)
[![PyPI](https://github.com/BobKerns/zabob-houdini/actions/workflows/publish.yml/badge.svg)](https://github.com/BobKerns/zabob-houdini/actions/workflows/publish.yml)

A simple Python API for creating Houdini node graphs programmatically.

## What is Zabob-Houdini?

Zabob-Houdini provides a clean, Pythonic interface for building Houdini node networks. Instead of manually creating nodes and wiring connections, you can describe your node graph declaratively and let Zabob handle the details.

**Key Features:**
- **Declarative API**: Describe what you want, not how to build it
- **Immutable Objects**: Node and chain definitions are immutable for safety and caching
- **Automatic Connections**: Wire nodes together with simple syntax
- **Chain Support**: Create linear processing pipelines easily
- **Type Safety**: Full type hints for modern Python development
- **Flexible**: Works in Houdini scripts, shelf tools, and HDAs

📚 **[Complete API Documentation](API.md)** - Comprehensive reference for all functions, classes, and methods

## Quick Start

Zabob-Houdini provides two main functions:

- **`node()`** - Create individual nodes with automatic connections
- **`chain()`** - Create linear sequences of connected nodes

Both return **immutable objects** that use `.create()` to instantiate the actual Houdini nodes.

### Why Immutability?

**Safety**: Once defined, node configurations can't be accidentally modified, preventing bugs from unexpected changes.

**Caching**: Immutable objects can be safely cached and reused, improving performance when creating complex node networks.

**Predictability**: The same node definition always creates the same result, making code easier to reason about and debug.

**Templates**: Node definitions serve as reusable templates for creating networks, allowing the same pattern to be instantiated multiple times.

**Circular References**: Immutable definitions enable circular node graphs by allowing nodes to reference each other before instantiation *(feature planned for future release)*.

## Example Usage

```python
from zabob_houdini import node, chain

# Create immutable node definitions
geo_node = node("/obj", "geo", name="mygeometry")
box_node = node(geo_node, "box", name="mybox")
transform_node = node(geo_node, "xform", name="mytransform", _input=box_node)

# Or create a processing chain (also immutable)
processing_chain = chain(
    node(geo_node, "box"),
    node(geo_node, "xform"),
    node(geo_node, "subdivide")
)

# These definitions are cached and can be reused safely
same_geo = geo_node.create()  # Returns the same hou.Node instance
another_chain = processing_chain.create()  # Reuses cached nodes
```

For complete examples including multi-output connections, chain indexing, type narrowing, and advanced patterns, see the **[API Documentation](API.md)**.

### Installation from PyPI

Once published, users can install with:

```bash
# First ensure hython is on your path.
# This is a requirement for all usage.
# Then:

mkdir zabob-houdini
cd zabob-houdini

# Using uv (recommended)
uv venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows (Command Prompt)
# .venv\Scripts\Activate.ps1  # Windows (PowerShell)
uv add zabob-houdini

# Using pip
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows (Command Prompt)
# .venv\Scripts\Activate.ps1  # Windows (PowerShell)
pip install zabob-houdini

# Install into Houdini:
zabob-houdini install-package

# Validate:
zabob-houdini validate
```

### For Houdini Integration

```python
# In Houdini's Python shell, shelf tools, or HDAs
from zabob_houdini import node, chain
```

## Documentation

- **[API Documentation](API.md)**: Complete reference for all functions, classes, and methods
- **[Command Line Interface](COMMAND.md)**: CLI reference and usage guide
- **[Development Guide](DEVELOPMENT.md)**: Setup, testing, and contribution guidelines
- **[PyPI Setup](docs/PYPI_SETUP.md)**: Publishing and release information
