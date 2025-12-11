"""
Bootstrap module for installing dynamic import hook via .pth file.

This is imported by zzz_dynamic_imports.pth during Python startup.
"""

import __future__


def _install():
    """Install the dynamic import hook if zabob_loader is available."""
    try:
        from zabob_loader.dyn_loader import install_import_hook
        install_import_hook()
    except ImportError:
        # zabob_loader not installed or not in path yet
        pass
    except Exception as e:
        # Don't break Python startup on errors
        import sys
        print(f"Warning: zabob_loader hook installation failed: {e}", file=sys.stderr)


# Install immediately when imported
_install()

__future__.dynamic_import = True  # type: ignore
