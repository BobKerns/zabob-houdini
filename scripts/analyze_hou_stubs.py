#!/usr/bin/env python3
"""
Analyze hou.pyi stub file and categorize its contents.

This script parses the hou.pyi file to extract classes, functions, and enums,
then categorizes them based on the missing_hou_entries.json mapping. Items
found in hou.pyi that aren't in the documentation are placed in an "extra" category.

Output is written to docs/hou_implemented.md and stubs/implemented_hou_entries.json
"""

import ast
import json
import re
from pathlib import Path
from typing import Any
from collections import defaultdict


def load_category_mapping(json_path: Path) -> dict[str, str]:
    """
    Load missing_hou_entries.json and create a mapping from entry name to category.
    Also adds mappings for currently implemented items based on common patterns.

    Returns:
        Dictionary mapping entry name -> category name
    """
    with open(json_path) as f:
        data: dict = json.load(f)

    name_to_category = {}

    for category_name, category_data in data["categories"].items():
        # Map classes
        if "classes" in category_data:
            for class_name in category_data["classes"]:
                name_to_category[class_name] = category_name

        # Map modules
        if "modules" in category_data:
            for module_name in category_data["modules"]:
                name_to_category[module_name] = category_name

        # Map functions
        if "functions" in category_data:
            funcs = category_data["functions"]
            if isinstance(funcs, list):
                for func_name in funcs:
                    name_to_category[func_name] = category_name
            elif isinstance(funcs, dict):
                # Handle nested function groups (like in animation_playbar)
                for group_name, func_list in funcs.items():
                    for func_name in func_list:
                        name_to_category[func_name] = category_name

        # Map package_functions groups
        if "groups" in category_data:
            for group_name, func_list in category_data["groups"].items():
                for func_name in func_list:
                    name_to_category[func_name] = category_name

    # Add mappings for implemented items based on patterns
    # These are items already in hou.pyi that need categorization
    implemented_categories = {
        # Core node system
        "nodes": ["Node", "OpNode", "NetworkItem", "NetworkMovableItem", "NetworkBox",
                  "StickyNote", "IndirectInput", "NetworkDot", "NodeConnection",
                  "NodeType", "NodeGroup", "NodeInfoTree"],

        # Node types by category
        "node_types": ["NodeTypeCategory", "OpNodeTypeCategory", "ApexNodeTypeCategory"],

        # Specific node types
        "geometry": ["SopNode", "Geometry", "Point", "Prim", "Vertex", "Polygon", "Face",
                     "Surface", "Volume", "Attrib", "Selection", "GeometryDelta", "SopVerb"],

        "objects": ["ObjNode"],

        "channels": ["ChopNode", "Track", "Clip"],

        "rendering": ["RopNode"],

        "dynamics": ["DopNode", "DopData", "DopRecord", "DopRelationship",
                     "DopSimulation", "DopObject"],

        "copernicus_images": ["CopNode", "Image"],

        "solaris_usd": ["LopNode", "LopNetwork"],

        "digital_assets": ["HDAModule", "HDAViewerStateModule", "HDAViewerHandleModule"],

        # Parameters
        "parameters": ["Parm", "ParmTuple"],

        # Parameter templates
        "parameter_templates": ["ParmTemplate", "ParmTemplateGroup", "ButtonParmTemplate",
                                "DataParmTemplate", "FloatParmTemplate", "FolderParmTemplate",
                                "FolderSetParmTemplate", "IntParmTemplate", "LabelParmTemplate",
                                "MenuParmTemplate", "RampParmTemplate", "SeparatorParmTemplate",
                                "StringParmTemplate", "ToggleParmTemplate"],

        # Utilities
        "utilities": ["BoundingRect", "BoundingBox", "OrientedBoundingBox", "Color", "Ramp",
                      "Matrix2", "Matrix3", "Matrix4", "Vector2", "Vector3", "Vector4",
                      "Quaternion", "HipFile", "UndoGroup", "UndoManager", "UndoDisabler",
                      "ProgressBar"],

        # PDG/TOPs
        "tops": ["TopNode", "WorkItem"],

        # Exceptions
        "exceptions": ["OperationFailed", "InvalidInput", "LoadWarning"],

        # Enums (lowercase convention in Houdini)
        "enums": ["networkItemType", "exprLanguage", "scriptLanguage", "parmTemplateType",
                  "attribType", "groupType", "geometryType", "attribData", "attribScope",
                  "groupScope", "primType", "componentLoopType", "numericData",
                  "volumeStorageType", "volumeVisualization", "colorType", "trackExtend",
                  "clipMode"]
    }

    for category, names in implemented_categories.items():
        for name in names:
            if name not in name_to_category:  # Don't override missing entries
                name_to_category[name] = category

    return name_to_category


def parse_stub_file(stub_path: Path) -> dict[str, list[str]]:
    """
    Parse hou.pyi to extract classes, functions, and other top-level definitions.

    Returns:
        Dictionary with keys: 'classes', 'enums', 'functions', 'variables'
    """
    with open(stub_path) as f:
        content = f.read()

    # Parse with AST
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Syntax error parsing {stub_path}: {e}")
        return {"classes": [], "enums": [], "functions": [], "variables": []}

    classes = []
    enums = []
    functions = []
    variables = []

    # Get top-level nodes only
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            # Check if it's an enum (inherits from _Enum)
            is_enum = any(
                isinstance(base, ast.Name) and base.id == '_Enum'
                for base in node.bases
            )
            if is_enum:
                enums.append(class_name)
            else:
                classes.append(class_name)

        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.AnnAssign):
            # Top-level annotated assignments (variables/constants)
            if isinstance(node.target, ast.Name):
                variables.append(node.target.id)

    # Alternative: Use regex for more reliable top-level detection
    # This catches things AST might miss due to stub syntax
    class_pattern = re.compile(r'^class\s+([A-Z][a-zA-Z0-9_]*)', re.MULTILINE)
    func_pattern = re.compile(r'^def\s+([a-z][a-zA-Z0-9_]*)\s*\(', re.MULTILINE)

    regex_classes = class_pattern.findall(content)
    regex_functions = func_pattern.findall(content)

    # Merge and deduplicate
    all_classes = sorted(set(classes + regex_classes))
    all_functions = sorted(set(functions + regex_functions))

    # Separate enums from classes
    enum_names = set(enums)
    final_classes = [c for c in all_classes if c not in enum_names and not c.startswith('_')]
    final_enums = [c for c in all_classes if c in enum_names or
                   (c[0].islower() and c not in ['session', 'hipFile'])]

    return {
        "classes": final_classes,
        "enums": final_enums,
        "functions": all_functions,
        "variables": sorted(set(variables))
    }


def categorize_entries(
    parsed_data: dict[str, list[str]],
    name_to_category: dict[str, str]
) -> dict[str, dict[str, list[str]]]:
    """
    Categorize parsed entries based on the mapping.

    Returns:
        Nested dictionary: category -> type -> list of names
        Special "_implemented" category for all items in hou.pyi
        Special "uncategorized" category for items without a category mapping
    """
    categories = defaultdict(lambda: defaultdict(list))

    # Add "_implemented" as a special meta-category
    categories["_implemented"] = defaultdict(list)

    for entry_type, names in parsed_data.items():
        for name in names:
            # Skip internal/private entries
            if name.startswith('_') and name not in ['_Enum', '_EnumValue']:
                continue

            # Mark as implemented
            categories["_implemented"][entry_type].append(name)

            # Find category from mapping
            category = name_to_category.get(name, "uncategorized")
            categories[category][entry_type].append(name)

    return dict(categories)


def generate_markdown_report(
    categorized: dict[str, dict[str, list[str]]],
    output_path: Path,
    stub_path: Path
) -> None:
    """Generate a markdown report of implemented entries by category."""

    # Calculate stats
    implemented = categorized.get("_implemented", {})
    total_classes = len(implemented.get("classes", []))
    total_enums = len(implemented.get("enums", []))
    total_functions = len(implemented.get("functions", []))
    total_variables = len(implemented.get("variables", []))

    uncategorized = categorized.get("uncategorized", {})
    uncategorized_classes = len(uncategorized.get("classes", []))
    uncategorized_enums = len(uncategorized.get("enums", []))
    uncategorized_functions = len(uncategorized.get("functions", []))

    lines = [
        "# Implemented Entries in hou.pyi",
        "",
        f"This document catalogs the package-level entries currently implemented in `{stub_path.name}`.",
        "Entries are grouped by the same categories as the missing entries documentation.",
        "",
        "## Summary Statistics",
        "",
        f"- **Total Classes:** {total_classes}",
        f"- **Total Enums:** {total_enums}",
        f"- **Total Functions:** {total_functions}",
        f"- **Total Variables:** {total_variables}",
        f"- **Total Items:** {total_classes + total_enums + total_functions + total_variables}",
        "",
        f"**Uncategorized Items** (need category assignment):",
        f"- Classes: {uncategorized_classes}",
        f"- Enums: {uncategorized_enums}",
        f"- Functions: {uncategorized_functions}",
        "",
        "---",
        ""
    ]

    # Sort categories, but put "uncategorized" at the end
    sorted_categories = sorted(
        [c for c in categorized.keys() if c not in ["_implemented", "uncategorized"]]
    )
    if "uncategorized" in categorized:
        sorted_categories.append("uncategorized")

    for category in sorted_categories:
        items = categorized[category]

        if not any(items.values()):
            continue

        # Format category name
        category_title = category.replace("_", " ").title()
        lines.append(f"## {category_title}")
        lines.append("")

        # Classes
        if items.get("classes"):
            lines.append("### Classes")
            lines.append("")
            for name in sorted(items["classes"]):
                lines.append(f"- `hou.{name}`")
            lines.append("")

        # Enums
        if items.get("enums"):
            lines.append("### Enums")
            lines.append("")
            for name in sorted(items["enums"]):
                lines.append(f"- `hou.{name}`")
            lines.append("")

        # Functions
        if items.get("functions"):
            lines.append("### Functions")
            lines.append("")
            for name in sorted(items["functions"]):
                lines.append(f"- `hou.{name}()`")
            lines.append("")

        # Variables
        if items.get("variables"):
            lines.append("### Variables/Modules")
            lines.append("")
            for name in sorted(items["variables"]):
                lines.append(f"- `hou.{name}`")
            lines.append("")

    output_path.write_text("\n".join(lines))
    print(f"Generated markdown report: {output_path}")


def generate_json_report(
    categorized: dict[str, dict[str, list[str]]],
    output_path: Path,
    stub_path: Path
) -> None:
    """Generate a JSON report of implemented entries."""

    implemented = categorized.get("_implemented", {})

    # Build structured output
    output: dict[str, Any] = {
        "metadata": {
            "description": f"Implemented entries in {stub_path.name}",
            "date_analyzed": "2025-11-24",
            "source_file": str(stub_path),
            "stats": {
                "total_classes": len(implemented.get("classes", [])),
                "total_enums": len(implemented.get("enums", [])),
                "total_functions": len(implemented.get("functions", [])),
                "total_variables": len(implemented.get("variables", [])),
                "uncategorized_classes": len(categorized.get("uncategorized", {}).get("classes", [])),
                "uncategorized_enums": len(categorized.get("uncategorized", {}).get("enums", [])),
                "uncategorized_functions": len(categorized.get("uncategorized", {}).get("functions", []))
            }
        },
        "categories": {}
    }

    # Exclude meta-category from output
    categories_dict: dict[str, Any] = output["categories"]
    for category, items in categorized.items():
        if category == "_implemented":
            continue

        categories_dict[category] = {
            "classes": sorted(items.get("classes", [])),
            "enums": sorted(items.get("enums", [])),
            "functions": sorted(items.get("functions", [])),
            "variables": sorted(items.get("variables", []))
        }

    output_path.write_text(json.dumps(output, indent=2))
    print(f"Generated JSON report: {output_path}")


def main():
    """Main entry point."""
    # Set up paths
    project_root = Path(__file__).parent.parent
    stub_path = project_root / "stubs" / "hou.pyi"
    json_path = project_root / "stubs" / "missing_hou_entries.json"

    md_output = project_root / "docs" / "hou_implemented.md"
    json_output = project_root / "stubs" / "implemented_hou_entries.json"

    # Validate inputs
    if not stub_path.exists():
        print(f"Error: {stub_path} not found")
        return 1

    if not json_path.exists():
        print(f"Error: {json_path} not found")
        return 1

    print(f"Analyzing {stub_path}...")

    # Load category mapping
    name_to_category = load_category_mapping(json_path)
    print(f"Loaded {len(name_to_category)} entries from category mapping")

    # Parse stub file
    parsed_data = parse_stub_file(stub_path)
    print(f"Parsed {len(parsed_data['classes'])} classes, "
          f"{len(parsed_data['enums'])} enums, "
          f"{len(parsed_data['functions'])} functions")

    # Categorize
    categorized = categorize_entries(parsed_data, name_to_category)

    # Generate reports
    generate_markdown_report(categorized, md_output, stub_path)
    generate_json_report(categorized, json_output, stub_path)

    print("\nAnalysis complete!")
    return 0


if __name__ == "__main__":
    exit(main())
