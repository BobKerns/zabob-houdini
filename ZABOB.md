![Zabob Banner](docs/images/zabob-banner.jpg)
# ZABOB: Agentic Houdini Workflows

## Project Vision

ZABOB is an ambitious project to enable AI agents to understand, analyze, and modify Houdini workflows through comprehensive knowledge representation and executable Python APIs. The ultimate goal is to create a system where agents can reason about complex node graphs, understand their dependencies, and make intelligent modifications to procedural workflows.

## Architecture Overview

The ZABOB ecosystem consists of several interconnected components:

### 1. Knowledge Layer (MCP Server)
An MCP (Model Context Protocol) server that provides comprehensive analysis of:
- **Static Analysis**: Complete metadata about Houdini installations, node types, parameters, and capabilities
- **Runtime Analysis**: Live inspection of Houdini sessions and .hip files
- **Multi-layered Dependencies**: Understanding visual connections, parameter references, and attribute flow

### 2. Executable Representation (zabob-houdini)
**This repository** provides the Python API for programmatically creating and connecting Houdini nodes:
- Clean, declarative syntax using `node()` and `chain()` functions
- Immutable node definitions with lazy evaluation via `.create()` methods
- Type-safe interfaces with comprehensive Houdini integration

### 3. Intelligent Retrieval
Context-aware information delivery at multiple detail levels:
- **Level 1**: Graph structure only (minimal context for reasoning)
- **Level 2**: Key non-default parameters (workflow understanding)
- **Level 3**: Complete representation (round-trip editing)

## Key Capabilities

### For AI Agents
- **Graph Reasoning**: Understand workflow structure and node relationships
- **Intelligent Modifications**: Make informed changes based on comprehensive knowledge
- **Context Efficiency**: Request only the level of detail needed for each task
- **Safe Operations**: Validate modifications against Houdini's type system and constraints

### For Developers
- **HDA Liberation**: Extract complex workflows from binary HDAs into version-controllable Python code
- **Git Integration**: Escape Git LFS limitations with diffable, mergeable representations
- **Programmatic Workflows**: Build and modify node graphs through clean Python APIs
- **Round-trip Safety**: Maintain synchronization between Python and .hip representations with safety flags

## Standalone Value

Even without the full MCP server infrastructure, **zabob-houdini provides immediate value** as a standalone tool:

### Programmatic Graph Creation
```python
# Clean, readable workflow definitions
geo = node("/obj", "geo", name="terrain_geo")
terrain = chain(
    node(geo, "heightfield"),
    node(geo, "heightfield_erode", iterations=10),
    node(geo, "heightfield_scatter", density=1000)
)

# Execute when ready
terrain_nodes = terrain.create()
```

### Version Control Benefits
- Convert binary HDAs to readable Python code
- Track workflow changes through standard diff tools
- Enable collaborative development on complex procedural setups
- Eliminate Git LFS merge conflicts and storage limitations

### Workflow Analysis
Extract and analyze existing .hip files to understand their structure, dependencies, and patterns - valuable for documentation, optimization, and knowledge transfer.

## Current Status

This project represents a modern, open-source implementation of concepts previously explored in closed-source systems. The current focus is on building the foundational executable representation layer, with the broader agentic capabilities planned for future development.

The modular design ensures that each component provides standalone value while contributing to the larger vision of AI-assisted procedural workflow development.

## Future Directions

As the project evolves, we plan to expand into:
- **Parameter Dependency Analysis**: Understanding expression-based connections between nodes
- **Attribute Flow Tracking**: Semantic analysis of geometry attribute propagation
- **Pattern Recognition**: Identifying common workflow patterns for agent recommendations
- **Collaborative Workflows**: Multi-agent systems working together on complex procedural projects

---

*ZABOB represents the convergence of procedural modeling, version control, and artificial intelligence - creating new possibilities for how we create, share, and evolve complex digital content pipelines.*
