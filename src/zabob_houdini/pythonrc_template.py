"""
Houdini pythonrc.py template for zabob-houdini.

This file is installed by `zabob-houdini install-package` to enable
dynamic imports in Houdini's Python environment.
"""

# Install the dynamic import hook for zabob
try:
    import sys
    from pathlib import Path

    # Find zabob-loader via PYTHONPATH
    for path_str in sys.path:
        path = Path(path_str)
        zabob_init = path / 'zabob_loader' / '__init__.py'
        if zabob_init.exists():
            # Found zabob-loader, now install the import hook
            from zabob_loader.dyn_loader import install_import_hook
            install_import_hook()
            break
except Exception as e:
    # Don't fail silently - log to Houdini console
    print(f"Warning: Failed to install zabob-houdini dynamic import hook: {e}", file=sys.stderr)
