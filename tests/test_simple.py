"""
Simple test to check if pytest works at all.
"""

import pytest


@pytest.mark.unit
def test_basic_math():
    """Test basic math operations."""
    assert 1 + 1 == 2
    assert 2 * 3 == 6


@pytest.mark.unit
def test_string_operations():
    """Test string operations."""
    assert "hello" + " world" == "hello world"
    assert "test".upper() == "TEST"
