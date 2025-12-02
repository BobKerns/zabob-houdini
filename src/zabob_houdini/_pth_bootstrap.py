"""
Bootstrap module for installing dynamic import hook via .pth file.

This is imported by zzz_dynamic_imports.pth during Python startup.
"""


def _install():
    """Install the dynamic import hook if zabob_houdini is available."""
    try:
        from zabob_houdini.dyn_loader import install_import_hook
        install_import_hook()
    except ImportError:
        # zabob_houdini not installed or not in path yet
        pass
    except Exception as e:
        # Don't break Python startup on errors
        import sys
        print(f"Warning: zabob_houdini hook installation failed: {e}", file=sys.stderr)


# Install immediately when imported
_install()
