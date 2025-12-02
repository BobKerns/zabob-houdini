#!/usr/bin/env python3
"""
VS Code workspace setup script for Zabob-Houdini.

This script sets up the development environment:
- Configures git to exclude personal VS Code files
- Creates .env from platform-specific example
- Generates initial debug launcher option lists
"""

import os
import platform
import subprocess
import sys
from pathlib import Path


def main():
    print("🚀 Setting up VS Code configuration for Zabob-Houdini...")

    # Find workspace root by searching upward for pyproject.toml
    def find_workspace_root(start_path: Path) -> Path | None:
        """Search upward from start_path for pyproject.toml."""
        current = start_path.resolve()
        while current != current.parent:  # Stop at filesystem root
            if (current / "pyproject.toml").exists():
                return current
            current = current.parent
        return None

    workspace_root = find_workspace_root(Path.cwd())
    if workspace_root is None:
        print("❌ Error: Could not find workspace root (pyproject.toml not found)")
        sys.exit(1)

    os.chdir(workspace_root)
    print(f"📁 Working in: {workspace_root}")
    print()

    # Configure git to exclude personal VS Code files
    print("\n📝 Configuring git to exclude personal VS Code files...")
    git_exclude = workspace_root / ".git" / "info" / "exclude"
    git_exclude.parent.mkdir(parents=True, exist_ok=True)

    exclude_files = [
        ".vscode/settings.json",
        ".vscode/tasks.json",
        ".vscode/launch.json"
    ]

    existing_excludes = set()
    if git_exclude.exists():
        existing_excludes = set(line.strip() for line in git_exclude.read_text().splitlines())

    with git_exclude.open("a") as f:
        for file in exclude_files:
            if file not in existing_excludes:
                f.write(f"{file}\n")
                print(f"✅ Added {file} to git exclude")
            else:
                print(f"ℹ️  {file} already in git exclude")

    # Copy environment file if it doesn't exist
    print("\n📝 Setting up .env file...")
    env_file = workspace_root / ".env"
    if not env_file.exists():
        system = platform.system()
        example_map = {
            "Darwin": ".env.example.macos",
            "Linux": ".env.example.linux",
            "Windows": ".env.example.windows"
        }

        example_file = example_map.get(system)
        if example_file:
            example_path = workspace_root / example_file
            if example_path.exists():
                env_file.write_text(example_path.read_text())
                print(f"✅ Created .env for {system}")
            else:
                print(f"⚠️  {example_file} not found")
        else:
            print(f"⚠️  Unknown platform: {system}, please manually copy the appropriate .env.example.* file")
    else:
        print("ℹ️  .env already exists, skipping...")

    # Generate initial debug launcher option lists
    print("\n📝 Generating debug launcher option lists...")
    vscode_tmp = workspace_root / ".vscode" / "tmp"
    vscode_tmp.mkdir(parents=True, exist_ok=True)

    # Create initial test-functions.txt
    test_functions_file = vscode_tmp / "test-functions.txt"
    if not test_functions_file.exists():
        test_functions_file.write_text("__initialize__\n")
        print("✅ Created initial test-functions.txt")
    else:
        print("ℹ️  test-functions.txt already exists")

    # Create initial example-files.txt
    example_files_file = vscode_tmp / "example-files.txt"
    if not example_files_file.exists():
        example_files_file.write_text("__initialize__\n")
        print("✅ Created initial example-files.txt")
    else:
        print("ℹ️  example-files.txt already exists")

    # Try to generate actual lists if zabob-houdini is available
    print("\n📝 Attempting to populate option lists...")
    try:
        result = subprocess.run(
            ["zabob-houdini", "generate", "test-list"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Generated test function list")
        else:
            print("ℹ️  Could not generate test list (zabob-houdini may not be installed yet)")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("ℹ️  zabob-houdini not available yet (run after virtual environment setup)")

    try:
        result = subprocess.run(
            ["zabob-houdini", "generate", "examples"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Generated example file list")
        else:
            print("ℹ️  Could not generate example list")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("ℹ️  Will generate example list after installation")

    print("\n🎉 VS Code setup complete!")
    print("\nNext steps:")
    print("1. Open VS Code in this directory: code .")
    print("2. Install recommended extensions if prompted")
    print("3. Edit .env if your Houdini installation path is different")
    print("4. Customize .vscode/settings.json, tasks.json, and launch.json as needed")
    print("   (These files are excluded from git so your changes stay personal)")
    print("\nRecommended VS Code extensions:")
    print("  - Python (ms-python.python)")
    print("  - Code Spell Checker (streetsidesoftware.code-spell-checker)")
    print("  - Pylance (ms-python.vscode-pylance)")
    print("  - Command Variable (rioj7.command-variable) - for dynamic launch configs")


if __name__ == "__main__":
    main()
