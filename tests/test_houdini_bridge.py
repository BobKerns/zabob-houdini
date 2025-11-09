"""
Test hython bridge functionality.
"""

import pytest
from unittest.mock import patch, Mock
from zabob_houdini.houdini_bridge import in_hython, _is_in_houdini, run_hython_script


def test_is_in_hython_detection():
    """Test detection of hython environment."""
    # Test when hou is not available
    with patch('builtins.__import__', side_effect=ImportError):
        assert not _is_in_houdini()

    # Test when hou is available but not hython
    mock_hou = Mock()
    mock_hou.applicationName.return_value = 'houdini'
    with patch('builtins.__import__', return_value=mock_hou):
        assert not _is_in_houdini()

    # Test when in hython
    mock_hou.applicationName.return_value = 'hython'
    with patch('builtins.__import__', return_value=mock_hou):
        assert _is_in_houdini()


def test_in_hython_decorator_direct_execution():
    """Test decorator when already in hython."""
    @in_hython
    def test_function(x, y=10):
        return x + y

    # Mock being in hython and the houdini function
    mock_func = Mock(return_value=20)

    with patch('zabob_houdini.hython_bridge._is_in_hython', return_value=True), \
         patch('zabob_houdini.hython_bridge.get_houdini_function', return_value=mock_func):
        result = test_function(5, y=15)
        assert result == 20


def test_in_hython_decorator_without_hython():
    """Test decorator behavior when hython is not available."""
    @in_hython
    def test_function(x):
        return x * 2

    # Mock not being in hython and hython not found
    with patch('zabob_houdini.hython_bridge._is_in_hython', return_value=False), \
         patch('zabob_houdini.hython_bridge._find_hython', side_effect=RuntimeError("hython not found")):

        with pytest.raises(RuntimeError, match="hython not found"):
            test_function(5)


def test_run_hython_script_direct():
    """Test running script when already in hython."""
    script = """
x = 5
y = 10
result = x + y
"""

    with patch('zabob_houdini.hython_bridge._is_in_hython', return_value=True):
        result = run_hython_script(script)
        assert result == 15


def test_simple_function_without_houdini():
    """Test that decorator works for functions that don't use Houdini."""
    @in_hython
    def simple_math(a, b):
        return a * b + 10

    # Even when not in hython, if hython is not found, should raise error
    with patch('zabob_houdini.hython_bridge._is_in_hython', return_value=False), \
         patch('zabob_houdini.hython_bridge._find_hython', side_effect=RuntimeError("hython not found")):

        with pytest.raises(RuntimeError):
            simple_math(3, 4)
