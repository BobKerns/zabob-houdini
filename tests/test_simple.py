"""
Simple test to check if pytest works at all.
"""

def test_basic_math():
    """Test basic math operations."""
    assert 1 + 1 == 2
    assert 2 * 3 == 6


def test_string_operations():
    """Test string operations."""
    assert "hello" + " world" == "hello world"
    assert "test".upper() == "TEST"
