#!/usr/bin/env python3
"""
Script to rename all Zabob-Houdini classes and functions to use Z prefix.

This performs a systematic rename across the entire codebase to clearly
distinguish our classes from Houdini's native classes.

Usage:
    python scripts/rename_to_z_prefix.py [--dry-run]
"""

import re
from pathlib import Path

import click


# Ordered list of replacements - ORDER MATTERS!
# Longer/more specific names must come before shorter ones to avoid partial matches
REPLACEMENTS: list[tuple[str, str]] = [
    # Classes - specific before general
    ('ChainForwardReference', 'ZChainForwardRef'),
    ('ChainFirstReference', 'ZChainFirstRef'),
    ('ChainLastReference', 'ZChainLastRef'),
    ('ChainReference', 'ZChainRef'),
    ('ContextReference', 'ZContextRef'),
    ('CopyReference', 'ZCopyRef'),
    ('ForwardReference', 'ZNodeForwardRef'),
    ('ImmediateNode', 'ZImmediateNode'),

    # Op/Sop/Obj classes - specific before general
    ('SopInstance', 'ZSopNode'),
    ('SopContext', 'ZSopContext'),
    ('SopChain', 'ZSopChain'),
    ('SopBase', 'ZSopNodeBase'),

    ('ObjInstance', 'ZObjNode'),
    ('ObjContext', 'ZObjContext'),
    ('ObjChain', 'ZObjChain'),

    ('OpInstance', 'ZOpNode'),
    ('OpContext', 'ZOpContext'),
    ('OpChain', 'ZOpChain'),
    ('OpBase', 'ZOpNodeBase'),

    # Chain classes
    ('ChainBuilder', 'ZChainBuilder'),
    ('Chain', 'ZChain'),

    # Context and Node classes
    ('NodeContext', 'ZContext'),
    ('NodeInstance', 'ZNode'),
    ('NodeBase', 'ZNodeBase'),

    # Functions
    ('get_node_instance', 'zget_node_instance'),
    ('wrap_node', 'zwrap_node'),
    ('context', 'zcontext'),
    ('merge', 'zmerge'),
    ('chain', 'zchain'),
    ('node', 'znode'),
]


def should_process_file(path: Path) -> bool:
    """Check if file should be processed."""
    # Skip ignored directories
    parts = path.parts
    ignore_dirs = {'.git', '.venv', '__pycache__', 'node_modules', '.pytest_cache',
                   '.mypy_cache', 'dist', 'build', '*.egg-info', 'hip'}
    if any(ignored in parts for ignored in ignore_dirs):
        return False

    # Skip binary files
    if path.suffix in {'.pyc', '.pyo', '.so', '.dylib', '.hip', '.hipnc', '.hiplc',
                       '.png', '.jpg', '.jpeg', '.gif', '.pdf'}:
        return False

    # Process text files
    if path.suffix in {'.py', '.md', '.txt', '.rst', '.toml', '.yaml', '.yml',
                       '.json', '.sh', '.bat', '.cfg', '.ini'}:
        return True

    # Process files without extension if they're likely text
    if not path.suffix and path.is_file():
        try:
            with open(path, 'rb') as f:
                sample = f.read(1024)
                # Check if it's text (no null bytes)
                return b'\x00' not in sample
        except Exception:
            return False

    return False


def replace_in_file(path: Path, replacements: list[tuple[str, str]], dry_run: bool = False) -> tuple[int, list[str]]:
    """
    Perform replacements in a single file.

    Returns:
        Tuple of (number of replacements made, list of changes)
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Skip files we can't read as UTF-8
        return 0, []

    original_content = content
    changes = []
    total_replacements = 0

    is_python = path.suffix == '.py'

    for old, new in replacements:
        # For Python files, handle functions and classes differently
        if is_python:
            # Check if this is a function (lowercase first letter)
            is_function = old[0].islower()

            if is_function:
                # Functions: only match when followed by '(' to avoid variables/kwargs
                pattern = r'\b' + re.escape(old) + r'(?=\()'
            else:
                # Classes: use word boundaries, but be careful with '[' for generics
                pattern = r'\b' + re.escape(old) + r'(?=\b|[^\w])'
        else:
            # Non-Python files: standard word boundary matching
            pattern = r'\b' + re.escape(old) + r'(?=\b|[^\w])'

        matches = list(re.finditer(pattern, content))

        if matches:
            count = len(matches)
            total_replacements += count
            changes.append(f"  {old} → {new} ({count} occurrences)")
            content = re.sub(pattern, new, content)

    if content != original_content and not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    return total_replacements, changes


@click.command()
@click.option(
    '--dry-run',
    is_flag=True,
    help='Show what would be changed without modifying files'
)
def main(dry_run: bool):
    """Rename Zabob-Houdini classes to use Z prefix."""
    # Start from repo root
    repo_root = Path(__file__).parent.parent

    click.echo(f"Scanning {repo_root}...")
    click.echo(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    click.echo()

    # Find all files to process
    script_path = Path(__file__).resolve()
    dyn_loader_path = (repo_root / 'src' / 'zabob_houdini' / 'dyn_loader.py').resolve()
    all_files = []
    for path in repo_root.rglob('*'):
        resolved_path = path.resolve()
        if (path.is_file()
                and resolved_path != script_path
                and resolved_path != dyn_loader_path
                and should_process_file(path)):
            all_files.append(path)

    click.echo(f"Found {len(all_files)} files to process")
    click.echo()

    # Process each file
    total_files_changed = 0
    total_replacements = 0

    for path in sorted(all_files):
        rel_path = path.relative_to(repo_root)
        count, changes = replace_in_file(path, REPLACEMENTS, dry_run)

        if changes:
            total_files_changed += 1
            total_replacements += count
            click.echo(f"📝 {rel_path}")
            for change in changes:
                click.echo(change)
            click.echo()

    click.echo("=" * 60)
    click.echo("Summary:")
    click.echo(f"  Files changed: {total_files_changed}")
    click.echo(f"  Total replacements: {total_replacements}")

    if dry_run:
        click.echo()
        click.echo("🔍 This was a DRY RUN - no files were modified")
        click.echo("   Run without --dry-run to apply changes")
    else:
        click.echo()
        click.echo("✅ Changes applied successfully")
        click.echo("   Review with: git diff")
        click.echo("   Revert with: git checkout .")


if __name__ == '__main__':
    main()
