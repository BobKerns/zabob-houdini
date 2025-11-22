#!/usr/bin/env hython
"""
Test ForwardReference implementation
"""

def test_forward_reference_import():
    """Test that ForwardReference can be imported and basic functionality works."""
    try:
        from zabob_houdini.core import ForwardReference, NodeContext
        from zabob_houdini import node, ROOT
        print("✅ ForwardReference import successful")

        # Create a simple test context
        parent = node(ROOT, "geo", "test_geo")
        ctx = NodeContext(parent)

        # Test creating a ForwardReference
        forward_ref = ForwardReference(
            resolution_type='context_lookup',
            context=ctx,
            name='future_node'
        )
        print("✅ ForwardReference creation successful")
        print(f"   ForwardRef: {forward_ref}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_forward_reference_in_context():
    """Test ForwardReference usage in NodeContext."""
    try:
        from zabob_houdini.core import NodeContext
        from zabob_houdini import node, ROOT

        # Create test context
        parent = node(ROOT, "geo", "test_geo")
        ctx = NodeContext(parent)

        # Create a node that references a future node by string name
        print("📦 Creating node with forward reference...")
        box = ctx.node("box", "my_box", _input="future_sphere")
        print("✅ Node with forward reference created successfully")

        # Now create the referenced node
        print("🔮 Creating the referenced node...")
        sphere = ctx.node("sphere", "future_sphere")
        print("✅ Referenced node created successfully")

        return True

    except Exception as e:
        print(f"❌ Error in context test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chain_builder_forward_reference():
    """Test ForwardReference with ChainBuilder properties."""
    try:
        from zabob_houdini.core import NodeContext
        from zabob_houdini import node, ROOT

        # Create test context
        parent = node(ROOT, "geo", "test_geo")
        ctx = NodeContext(parent)

        print("🔗 Testing ChainBuilder forward references...")

        # This should work with the new ForwardReference implementation
        with ctx.chain() as pipeline:
            pipeline.node("box", "start_box")
            pipeline.node("xform", "transform")

            # Access .last while still building - should return ForwardReference
            last_ref = pipeline.last
            print(f"✅ Got last reference during construction: {last_ref}")

            # Try to use it as input to another node
            merge_node = ctx.node("merge", "test_merge", _input=[last_ref])
            print("✅ Used ChainBuilder.last as forward reference")

        return True

    except Exception as e:
        print(f"❌ Error in chain builder test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing ForwardReference Implementation")
    print("=" * 50)

    success = True

    print("\n1️⃣ Testing basic ForwardReference...")
    success &= test_forward_reference_import()

    print("\n2️⃣ Testing ForwardReference in NodeContext...")
    success &= test_forward_reference_in_context()

    print("\n3️⃣ Testing ChainBuilder ForwardReference...")
    success &= test_chain_builder_forward_reference()

    print("\n" + "=" * 50)
    if success:
        print("🎉 All ForwardReference tests passed!")
    else:
        print("💥 Some tests failed!")

    print("✨ Test completed")
