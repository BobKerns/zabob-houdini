"""Test enhanced NodeInstance.copy() functionality."""
import pytest


@pytest.mark.integration
def test_enhanced_copy_integration(hython_test):
    """Test the enhanced copy functionality using hython_test fixture."""
    result = hython_test("test_enhanced_copy_functionality")
    assert result['success'] is True

    data = result['result']

    # Test 1: Original node properties
    original = data["original"]
    assert original["name"] == "original_box"
    assert original["attributes"] == {"sizex": 2, "sizey": 3}
    assert original["display"] is False
    assert original["render"] is False

    # Test 2: Copy with attribute modifications
    attrs_copy = data["attributes_copy"]
    assert attrs_copy["name"] == "original_box"  # Name preserved
    # Attributes merged: sizex overridden, sizey preserved, sizez added
    assert attrs_copy["attributes"] == {"sizex": 5, "sizey": 3, "sizez": 4}

    # Test 3: Copy with new name
    renamed = data["renamed_copy"]
    assert renamed["name"] == "renamed_box"

    # Test 4: Copy with display/render flags
    display_copy = data["display_copy"]
    assert display_copy["display"] is True
    assert display_copy["render"] is True

    # Test 5: Copy with all parameters
    complex_copy = data["complex_copy"]
    assert complex_copy["name"] == "complex_box"
    # Should have original + new attributes
    assert complex_copy["attributes"] == {"sizex": 2, "sizey": 3, "divisions": 10}
    assert complex_copy["has_inputs"] is True
    assert complex_copy["display"] is True
    assert complex_copy["render"] is False

    # Test 6: None parameters preserve originals
    preserved = data["preserved_copy"]
    assert preserved["name"] == original["name"]
    assert preserved["attributes"] == original["attributes"]
    assert preserved["display"] == original["display"]
    assert preserved["render"] == original["render"]


@pytest.mark.integration
def test_enhanced_copy_parameter_validation(hython_test):
    """Test copy method parameter validation."""
    result = hython_test("test_copy_signature_validation")
    assert result['success'] is True

    data = result['result']

    # Verify all expected parameters exist
    assert data["has_inputs"] is True
    assert data["has_chain"] is True
    assert data["has_name"] is True
    assert data["has_attributes"] is True
    assert data["has_display"] is True
    assert data["has_render"] is True

    # Verify keyword-only parameters (after *)
    keyword_only = data["keyword_only_parameters"]
    expected_kw_only = ["name", "attributes", "_display", "_render"]

    for param in expected_kw_only:
        assert param in keyword_only, f"Parameter {param} should be keyword-only"

    # Verify parameter order (positional before keyword-only)
    all_params = data["all_parameters"]
    assert "_inputs" in all_params
    assert "_chain" in all_params
