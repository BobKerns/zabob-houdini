"""Dependency tracking test functions."""

from zabob_houdini.utils import JsonObject


def _test_dependency_tracking() -> JsonObject:
    """Test that node dependencies are tracked correctly."""
    try:
        from zabob_houdini.core import node, chain, context

        # Create some nodes with dependencies
        geo = node("/obj", "geo", "test_geo")
        box = node(geo, "box", "source_box")
        xform = node(geo, "xform", "transform", _input=box)

        # Create the nodes
        box.create()
        xform.create()

        # Create a context to test dependency tracking
        test_ctx = context(geo)

        # Re-create nodes through context for dependency tracking
        ctx_box = test_ctx.node("box", "ctx_box")
        ctx_xform = test_ctx.node("xform", "ctx_transform", _input=ctx_box)

        # Create nodes
        ctx_xform.create()

        # Test basic dependency tracking
        box_dependents = test_ctx.get_dependents(ctx_box)

        # Create nodes through context for dependency tracking
        sphere1 = test_ctx.node("sphere", "sphere1")
        merge1 = test_ctx.node("merge", "merge1", _input=sphere1)
        final_xform = test_ctx.node("xform", "final_xform", _input=merge1)

        # Create the nodes to establish dependencies
        sphere1.create()
        merge1.create()
        final_xform.create()

        sphere1_dependents = test_ctx.get_dependents(sphere1)
        merge1_dependents = test_ctx.get_dependents(merge1)

        # Test source/sink analysis using context methods
        # Build a network for analysis
        network_geo = node("/obj", "geo", "network_geo")
        ctx = context(network_geo)

        source1 = ctx.node("box", "source1")
        source2 = ctx.node("sphere", "source2")
        process1 = ctx.node("xform", "process1", _input=source1)
        process2 = ctx.node("xform", "process2", _input=source2)
        merge_node = ctx.node("merge", "combine", _input=[process1, process2])
        sink1 = ctx.node("null", "output1", _input=merge_node)
        sink2 = ctx.node("null", "output2", _input=merge_node)

        # Create the network
        sink1.create()
        sink2.create()

        # Use context methods for analysis
        sources = ctx.get_source_nodes()
        sinks = ctx.get_sink_nodes()

        return {
            'success': True,
            'box_has_dependent': len(box_dependents) > 0,
            'xform_is_dependent': ctx_xform in box_dependents,
            'sphere1_has_dependent': len(sphere1_dependents) > 0,
            'merge1_depends_on_sphere1': merge1 in sphere1_dependents,
            'merge1_has_dependent': len(merge1_dependents) > 0,
            'final_xform_depends_on_merge1': final_xform in merge1_dependents,
            'box_dependent_count': len(box_dependents),
            'sphere1_dependent_count': len(sphere1_dependents),
            'merge1_dependent_count': len(merge1_dependents),
            # Source/sink analysis results
            'source_count': len(sources),
            'sink_count': len(sinks),
            'sources_are_correct': source1 in sources and source2 in sources,
            'sinks_are_correct': sink1 in sinks and sink2 in sinks,
            'merge_not_source': merge_node not in sources,
            'merge_not_sink': merge_node not in sinks
        }
    except Exception as e:
        import traceback
        return {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
