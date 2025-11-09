"""
Test for the Houdini bridge functionality.
"""

import pytest
import subprocess
from unittest.mock import patch, Mock
from zabob_houdini.houdini_bridge import call_houdini_function, _is_in_houdini


def test_is_in_houdini_detection_when_available():
    """Test detection when hou module is available."""
    # This test only makes sense if we're actually in hython
    # In normal Python, this will be False
    result = _is_in_houdini()
    assert isinstance(result, bool)
    # We can't assert True/False since it depends on environment


def test_call_houdini_function_subprocess_logic():
    """Test subprocess call logic without heavy mocking."""
    # Test the command building logic by mocking subprocess only
    with patch('zabob_houdini.houdini_bridge._is_in_houdini', return_value=False), \
         patch('zabob_houdini.houdini_bridge._find_hython', return_value='/mock/hython'), \
         patch('subprocess.run') as mock_run:

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "function result"
        mock_run.return_value.stderr = ""

        result = call_houdini_function('test_function', 'arg1', 'arg2')

        assert result['success'] is True
        assert 'result' in result
        assert result['result']['value'] == "function result"
        mock_run.assert_called_once_with([
            '/mock/hython', '-m', 'zabob_houdini', 'houdini_functions', 'test_function', 'arg1', 'arg2'
        ], check=True, capture_output=True, text=True)


def test_call_houdini_function_subprocess_error_handling():
    """Test handling of subprocess errors."""
    with patch('zabob_houdini.houdini_bridge._is_in_houdini', return_value=False), \
         patch('zabob_houdini.houdini_bridge._find_hython', return_value='/mock/hython'), \
         patch('subprocess.run') as mock_run:

        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd', stderr="error message")

        with pytest.raises(RuntimeError, match="hython -m zabob_houdini houdini_functions test_function failed"):
            call_houdini_function('test_function')


def test_call_houdini_function_hython_not_found():
    """Test error when not in Houdini and hython not found."""
    with patch('zabob_houdini.houdini_bridge._is_in_houdini', return_value=False), \
         patch('zabob_houdini.houdini_bridge._find_hython', side_effect=RuntimeError("hython not found")):

        with pytest.raises(RuntimeError, match="hython not found"):
            call_houdini_function('test_function')


def test_call_houdini_function_module_parameter():
    """Test that module parameter is passed correctly."""
    with patch('zabob_houdini.houdini_bridge._is_in_houdini', return_value=False), \
         patch('zabob_houdini.houdini_bridge._find_hython', return_value='/mock/hython'), \
         patch('subprocess.run') as mock_run:

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "test result"
        mock_run.return_value.stderr = ""

        result = call_houdini_function('test_func', 'arg1', module='custom_module')

        assert result['success'] is True
        assert 'result' in result
        assert result['result']['value'] == "test result"
        mock_run.assert_called_once_with([
            '/mock/hython', '-m', 'zabob_houdini', 'custom_module', 'test_func', 'arg1'
        ], check=True, capture_output=True, text=True)

import pytest
import subprocess
from unittest.mock import patch, Mock
from zabob_houdini.houdini_bridge import call_houdini_function, _is_in_houdini


def test_is_in_houdini_detection():
    """Test detection of Houdini environment."""
    # Test when hou is not in sys.modules
    with patch.dict('sys.modules', {}, clear=True):
        assert not _is_in_houdini()

    # Test when hou is in sys.modules
    mock_hou = Mock()
    with patch.dict('sys.modules', {'hou': mock_hou}):
        assert _is_in_houdini()


def test_call_houdini_function_direct_execution():
    """Test calling function when already in Houdini."""
    # Mock being in Houdini and the houdini_functions module
    mock_func = Mock(return_value="test result")
    mock_module = Mock()
    mock_module.test_function = mock_func

    with patch('zabob_houdini.houdini_bridge._is_in_houdini', return_value=True), \
         patch.dict('sys.modules', {'zabob_houdini.houdini_functions': mock_module}):

        result = call_houdini_function('test_function', 'arg1', 'arg2')

        mock_func.assert_called_once_with('arg1', 'arg2')
        assert result['success'] is True
        assert 'result' in result
        assert result['result']['value'] == "test result"
def test_call_houdini_function_without_hython():
    """Test function call behavior when hython is not available."""
    # Mock not being in Houdini and hython not found
    with patch('zabob_houdini.houdini_bridge._is_in_houdini', return_value=False), \
         patch('zabob_houdini.houdini_bridge._find_hython', side_effect=RuntimeError("hython not found")):

        with pytest.raises(RuntimeError, match="hython not found"):
            call_houdini_function('test_function', 'arg1')


def test_call_houdini_function_subprocess():
    """Test calling function via subprocess when not in Houdini."""
    with patch('zabob_houdini.houdini_bridge._is_in_houdini', return_value=False), \
         patch('zabob_houdini.houdini_bridge._find_hython', return_value='/mock/hython'), \
         patch('subprocess.run') as mock_run:

        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "function result"
        mock_run.return_value.stderr = ""

        result = call_houdini_function('test_function', 'arg1', 'arg2')

        assert result['success'] is True
        assert 'result' in result
        assert result['result']['value'] == "function result"
        mock_run.assert_called_once_with([
            '/mock/hython', '-m', 'zabob_houdini', 'houdini_functions', 'test_function', 'arg1', 'arg2'
        ], check=True, capture_output=True, text=True)


def test_call_houdini_function_subprocess_error():
    """Test handling of subprocess errors."""
    with patch('zabob_houdini.houdini_bridge._is_in_houdini', return_value=False), \
         patch('zabob_houdini.houdini_bridge._find_hython', return_value='/mock/hython'), \
         patch('subprocess.run') as mock_run:

        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd', stderr="error message")

        with pytest.raises(RuntimeError, match="hython -m zabob_houdini houdini_functions test_function failed"):
            call_houdini_function('test_function')
