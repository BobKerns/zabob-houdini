#!/usr/bin/env python3
"""
Generate a complete taxonomy of hou module entries with implementation status.

This script combines information from:
1. SideFX documentation (via docs/hou.md and missing_hou_entries.json)
2. Current implementation (via hou.pyi analysis)

Output: A single JSON file showing all entries with their implementation status.
"""

import ast
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Any


def parse_stub_file(stub_path: Path) -> dict[str, set[str]]:
    """Parse hou.pyi to extract all implemented items."""
    with open(stub_path) as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Syntax error parsing {stub_path}: {e}")
        return {"classes": set(), "enums": set(), "functions": set(), "variables": set()}

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
            if isinstance(node.target, ast.Name):
                variables.append(node.target.id)

    # Use regex as backup
    class_pattern = re.compile(r'^class\s+([A-Z][a-zA-Z0-9_]*)', re.MULTILINE)
    func_pattern = re.compile(r'^def\s+([a-z][a-zA-Z0-9_]*)\s*\(', re.MULTILINE)

    regex_classes = class_pattern.findall(content)
    regex_functions = func_pattern.findall(content)

    # Merge
    all_classes = set(classes + regex_classes)
    all_functions = set(functions + regex_functions)

    # Separate enums from classes
    enum_names = set(enums)
    final_classes = {c for c in all_classes if c not in enum_names and not c.startswith('_')}
    final_enums = {c for c in all_classes if c in enum_names or
                   (c and c[0].islower() and c not in ['session', 'hipFile'])}

    return {
        "classes": final_classes,
        "enums": final_enums,
        "functions": set(all_functions),
        "variables": set(variables)
    }


def build_complete_taxonomy(
    missing_json_path: Path,
    stub_path: Path
) -> dict[str, Any]:
    """
    Build complete taxonomy combining missing and implemented entries.

    Returns a structure like:
    {
        "metadata": {...},
        "categories": {
            "category_name": {
                "purpose": "...",
                "entries": {
                    "ClassName": {
                        "type": "class",
                        "implemented": true/false,
                        "category": "category_name"
                    },
                    ...
                }
            }
        },
        "uncategorized": {
            "entries": {...}  # Items in hou.pyi but not in docs
        }
    }
    """
    # Load missing entries
    with open(missing_json_path) as f:
        missing_data: dict = json.load(f)

    # Parse current implementation
    implemented = parse_stub_file(stub_path)
    implemented_set = (
        implemented["classes"] |
        implemented["enums"] |
        implemented["functions"] |
        implemented["variables"]
    )

    # Build taxonomy
    taxonomy: dict[str, Any] = {
        "metadata": {
            "description": "Complete taxonomy of hou module with implementation status",
            "date_generated": "2025-11-24",
            "source_stub_file": str(stub_path),
            "source_missing_file": str(missing_json_path),
            "statistics": {
                "total_documented_entries": 0,
                "total_implemented_entries": len(implemented_set),
                "documented_and_implemented": 0,
                "documented_but_missing": 0,
                "implemented_but_undocumented": 0,
                "categories_count": len(missing_data.get("categories", {}))
            }
        },
        "categories": {},
        "uncategorized": {
            "purpose": "Items implemented in hou.pyi but not found in documentation",
            "entries": {}
        }
    }

    # Process categories from missing entries
    all_documented = set()

    for category_name, category_data in missing_data.get("categories", {}).items():
        category_info = {
            "purpose": category_data.get("purpose", ""),
            "entries": {}
        }

        # Process classes
        for class_name in category_data.get("classes", []):
            all_documented.add(class_name)
            category_info["entries"][class_name] = {
                "type": "class",
                "implemented": class_name in implemented["classes"],
                "status": "implemented" if class_name in implemented["classes"] else "missing"
            }

        # Process modules
        for module_name in category_data.get("modules", []):
            all_documented.add(module_name)
            is_impl = module_name in implemented["variables"] or module_name in implemented["functions"]
            category_info["entries"][module_name] = {
                "type": "module",
                "implemented": is_impl,
                "status": "implemented" if is_impl else "missing"
            }

        # Process functions (handle both list and dict formats)
        functions_data = category_data.get("functions", [])
        if isinstance(functions_data, list):
            for func_name in functions_data:
                all_documented.add(func_name)
                category_info["entries"][func_name] = {
                    "type": "function",
                    "implemented": func_name in implemented["functions"],
                    "status": "implemented" if func_name in implemented["functions"] else "missing"
                }
        elif isinstance(functions_data, dict):
            # Nested groups (e.g., animation_playbar)
            for group_name, func_list in functions_data.items():
                for func_name in func_list:
                    all_documented.add(func_name)
                    category_info["entries"][func_name] = {
                        "type": "function",
                        "group": group_name,
                        "implemented": func_name in implemented["functions"],
                        "status": "implemented" if func_name in implemented["functions"] else "missing"
                    }

        # Process groups (package-level functions)
        for group_name, func_list in category_data.get("groups", {}).items():
            for func_name in func_list:
                all_documented.add(func_name)
                category_info["entries"][func_name] = {
                    "type": "function",
                    "group": group_name,
                    "implemented": func_name in implemented["functions"],
                    "status": "implemented" if func_name in implemented["functions"] else "missing"
                }

        # Only add category if it has entries
        if category_info["entries"]:
            taxonomy["categories"][category_name] = category_info

    # Find undocumented but implemented items
    undocumented = implemented_set - all_documented

    for item_name in sorted(undocumented):
        # Determine type
        if item_name in implemented["classes"]:
            item_type = "class"
        elif item_name in implemented["enums"]:
            item_type = "enum"
        elif item_name in implemented["functions"]:
            item_type = "function"
        else:
            item_type = "variable"

        taxonomy["uncategorized"]["entries"][item_name] = {
            "type": item_type,
            "implemented": True,
            "status": "implemented_undocumented"
        }

    # Calculate statistics
    stats = taxonomy["metadata"]["statistics"]
    stats["total_documented_entries"] = len(all_documented)
    stats["documented_and_implemented"] = len(all_documented & implemented_set)
    stats["documented_but_missing"] = len(all_documented - implemented_set)
    stats["implemented_but_undocumented"] = len(undocumented)

    return taxonomy


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent

    missing_json = project_root / "stubs" / "missing_hou_entries.json"
    stub_file = project_root / "stubs" / "hou.pyi"
    output_file = project_root / "stubs" / "hou_taxonomy.json"

    if not missing_json.exists():
        print(f"Error: {missing_json} not found")
        return 1

    if not stub_file.exists():
        print(f"Error: {stub_file} not found")
        return 1

    print("Building complete taxonomy...")
    taxonomy = build_complete_taxonomy(missing_json, stub_file)

    # Write output
    with open(output_file, 'w') as f:
        json.dump(taxonomy, f, indent=2)

    print(f"\nGenerated: {output_file}")
    print("\nStatistics:")
    stats = taxonomy["metadata"]["statistics"]
    print(f"  Total documented entries: {stats['total_documented_entries']}")
    print(f"  Total implemented entries: {stats['total_implemented_entries']}")
    print(f"  Documented AND implemented: {stats['documented_and_implemented']}")
    print(f"  Documented but MISSING: {stats['documented_but_missing']}")
    print(f"  Implemented but UNDOCUMENTED: {stats['implemented_but_undocumented']}")
    print(f"  Categories: {stats['categories_count']}")

    return 0


if __name__ == "__main__":
    exit(main())
