"""
Verification script to check if dynamic import hook is installed.

Run this in any Python environment to verify the import hook is active.
"""

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

import sys


def verify_import_hook():
    """Check if the zabob-houdini dynamic import hook is installed."""
    # Check if the finder is in sys.meta_path
    for finder in sys.meta_path:
        if 'DynamicImportFinder' in type(finder).__name__:
            print("✓ Dynamic import hook is installed")
            print(f"  Finder: {type(finder).__name__}")
            return True

    print("✗ Dynamic import hook is NOT installed")
    return False


def verify_test_import():
    """Test if dynamic imports actually work."""
    try:
        # Import the test module that uses dynamic imports
        from zabob_houdini import h_test_dynamic_imports

        if h_test_dynamic_imports.DYNAMIC_IMPORTS_WORK:
            print("✓ Dynamic import test passed")
            return True
        else:
            print("✗ Dynamic import test failed")
            return False

    except SyntaxError as e:
        print(f"✗ Dynamic import test failed (syntax error): {e}")
        print("  The import hook may not be working correctly")
        return False
    except Exception as e:
        print(f"✗ Dynamic import test failed: {e}")
        return False


if __name__ == "__main__":
    print("Zabob-Houdini Dynamic Import Verification")
    print("=" * 50)
    print()

    hook_ok = verify_import_hook()
    print()
    syntax_ok = verify_test_import()
    print()

    if hook_ok and syntax_ok:
        print("✓ All checks passed - dynamic imports are working!")
        sys.exit(0)
    else:
        print("✗ Some checks failed - dynamic imports may not work correctly")
        sys.exit(1)
