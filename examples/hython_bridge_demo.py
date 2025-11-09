"""
Example using the hython bridge.
"""

from zabob_houdini import call_houdini_function
if __name__ == "__main__":
    print("Testing hython bridge...")

    try:
        result1 = call_houdini_function("simple_houdini_test")
        print(f"✓ Simple test: {result1}")
    except Exception as e:
        print(f"✗ Simple test failed: {e}")

    try:
        result2 = call_houdini_function("chain_creation_test")
        print(f"✓ Chain test: {result2}")
    except Exception as e:
        print(f"✗ Chain test failed: {e}")
