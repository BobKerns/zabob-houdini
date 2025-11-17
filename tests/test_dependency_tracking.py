"""Tests for node dependency tracking functionality."""

import pytest

class TestDependencyTracking:
    """Test dependency tracking between nodes."""

    def test_dependency_tracking(self, hython_test):
        """Test that dependencies are correctly tracked for nodes and chains."""
        response = hython_test("test_dependency_tracking")

        if not response.get('success', False):
            pytest.fail(f"Test function failed: {response.get('error', 'Unknown error')}")

        result = response.get('result', {})
        if not result.get('success', False):
            pytest.fail(f"Test function failed: {result.get('error', 'Unknown error')}\nTraceback:\n{result.get('traceback', 'No traceback')}")

        # Basic dependency tracking
        assert result['box_has_dependent'], "Box should have dependents"
        assert result['xform_is_dependent'], "Transform should depend on box"
        assert result['box_dependent_count'] == 1, "Box should have exactly one dependent"

        # Chain dependency tracking
        assert result['sphere1_has_dependent'], "Sphere1 should have dependents"
        assert result['merge1_depends_on_sphere1'], "Merge1 should depend on sphere1"
        assert result['sphere1_dependent_count'] == 1, "Sphere1 should have exactly one dependent"

        assert result['merge1_has_dependent'], "Merge1 should have dependents"
        assert result['final_xform_depends_on_merge1'], "Final xform should depend on merge1"
        assert result['merge1_dependent_count'] == 1, "Merge1 should have exactly one dependent"

        # Source/sink analysis
        assert result['source_count'] == 2, "Should have exactly 2 source nodes"
        assert result['sink_count'] == 2, "Should have exactly 2 sink nodes"
        assert result['sources_are_correct'], "Sources should be the input nodes"
        assert result['sinks_are_correct'], "Sinks should be the output nodes"
        assert result['merge_not_source'], "Merge node should not be a source"
        assert result['merge_not_sink'], "Merge node should not be a sink"
