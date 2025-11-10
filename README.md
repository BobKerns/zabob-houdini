![Zabob Banner](docs/images/zabob-banner.jpg)
# Zabob-Houdini

[![Tests](https://github.com/BobKerns/zabob-houdini/actions/workflows/test.yml/badge.svg)](https://github.com/BobKerns/zabob-houdini/actions/workflows/test.yml)
[![PyPI](https://github.com/BobKerns/zabob-houdini/actions/workflows/publish.yml/badge.svg)](https://github.com/BobKerns/zabob-houdini/actions/workflows/publish.yml)

A simple Python API for creating Houdini node graphs programmatically.

## What is Zabob-Houdini?

Zabob-Houdini provides a clean, Pythonic interface for building Houdini node networks. Instead of manually creating nodes and wiring connections, you can describe your node graph declaratively and let Zabob handle the details.

**Key Features:**
- **Declarative API**: Describe what you want, not how to build it
- **Automatic Connections**: Wire nodes together with simple syntax
- **Chain Support**: Create linear processing pipelines easily
- **Type Safety**: Full type hints for modern Python development
- **Flexible**: Works in Houdini scripts, shelf tools, and HDAs

## Core Concepts

### The `node()` Function

Create individual nodes with the `node()` function:

```python
node(parent, node_type, name=None, **attributes)
```

- **parent**: Where to create the node (`"/obj"`, `"/obj/geo1"`, or actual node object)
- **node_type**: Houdini node type (e.g., `"box"`, `"merge"`, `"xform"`)
- **name**: Optional name for the node
- **attributes**: Node parameters as keyword arguments
- **_input**: Special parameter to connect input nodes

### The `chain()` Function

Create linear sequences of connected nodes:

```python
chain(parent, *nodes, **kwargs)
```

Chains automatically connect nodes in sequence and can be nested or spliced together.

### Chain Indexing

Access nodes in chains with familiar Python syntax:

- **By integer**: `chain[0]` → first node
- **By slice**: `chain[1:3]` → subset as new chain
- **By name**: `chain["nodename"]` → named node

### Creation Pattern

Both `NodeInstance` and `Chain` objects use `.create()` to instantiate in Houdini:

```python
geo_node = node("/obj", "geo", name="mygeometry")
actual_node = geo_node.create()  # Creates the actual Houdini node
```

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

## Installation

### From PyPI (Recommended)

```bash
# Using uv (recommended)
uv add zabob-houdini

# Using pip
pip install zabob-houdini
```

### For Houdini Integration

Once installed, you can use Zabob-Houdini in several ways:

1. **Install as Houdini Package** (Recommended):
   ```bash
   zabob-houdini install-package
   zabob-houdini validate  # Verify installation
   ```

2. **Direct Import in Houdini Scripts**:
   ```python
   # In Houdini's Python shell, shelf tools, or HDAs
   from zabob_houdini import node, chain
   ```

3. **Development Setup**: See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed setup instructions.

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
source .venv/bin/activate
uv add zabob-houdini

# Using pip
python -m venv .venv
source .venv/bin/activate
pip install zabob-houdini

# Install into Houdini:
zabob-houdini install-package

# Validate:
zabob-houdini validate
```

## Documentation

- **[Development Guide](DEVELOPMENT.md)**: Detailed setup, testing, and contribution guidelines
- **[PyPI Setup](docs/PYPI_SETUP.md)**: Publishing and release information
