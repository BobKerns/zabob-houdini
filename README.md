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
