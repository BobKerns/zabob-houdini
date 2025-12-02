"""Test variable access transformation for dynamic imports."""

from zabob_houdini.dyn import transform_source


def test_simple_variable_reference():
    """Test that variable references use __dynamic__.load()."""
    source = """
from __future__ import _dynamic_import

import sys

x = sys.version
"""

    code = transform_source(source)

    # Should have setup code
    assert "from zabob_houdini.dyn_import import dyn_import as __dynamic__" in code
    assert "__dynamic__ = __dynamic__(globals())" in code

    # Import should be transformed to _def_module call
    assert "__dynamic__._def_module('sys', 'sys')" in code

    # Variable reference 'sys' should be transformed to __dynamic__.load() call
    assert "x = __dynamic__.load('sys', locals()).version" in code


def test_variable_in_function():
    """Test variable references inside functions."""
    source = """
from __future__ import _dynamic_import

from sys import version

def get_version():
    return version
"""

    code = transform_source(source)

    # Import should be transformed to _def call
    assert "__dynamic__._def('sys', 'version', 'version')" in code

    # Variable reference inside function should be transformed to load() call
    assert "return __dynamic__.load('version', locals())" in code


def test_attribute_access():
    """Test attribute access on imported modules."""
    source = """
from __future__ import _dynamic_import

import sys

def get_info():
    return sys.version, sys.platform
"""

    code = transform_source(source)

    # Import should be transformed to _def_module
    assert "__dynamic__._def_module('sys', 'sys')" in code

    # Both references to 'sys' should use load()
    assert "__dynamic__.load('sys', locals()).version" in code
    assert "__dynamic__.load('sys', locals()).platform" in code


def test_function_call():
    """Test calling functions from imported modules."""
    source = """
from __future__ import _dynamic_import

from os.path import join

result = join('a', 'b')
"""

    code = transform_source(source)

    # Import should be transformed to _def
    assert "__dynamic__._def('os.path', 'join', 'join')" in code

    # Function call reference should use load()
    assert "result = __dynamic__.load('join', locals())('a', 'b')" in code


def test_name_in_expression():
    """Test names used in various expression contexts."""
    source = """
from __future__ import _dynamic_import

import sys
from os import path

# Various contexts where names appear
a = sys
b = path
c = sys.version
d = [sys, path]
e = (sys, path)
f = {'sys': sys, 'path': path}
"""

    code = transform_source(source)

    # Imports should be transformed
    assert "__dynamic__._def_module('sys', 'sys')" in code
    assert "__dynamic__._def('os', 'path', 'path')" in code

    # All variable references should use load()
    assert "a = __dynamic__.load('sys', locals())" in code
    assert "b = __dynamic__.load('path', locals())" in code
    assert "c = __dynamic__.load('sys', locals()).version" in code
    assert "d = [__dynamic__.load('sys', locals()), __dynamic__.load('path', locals())]" in code
    assert "e = (__dynamic__.load('sys', locals()), __dynamic__.load('path', locals()))" in code
    assert "f = {'sys': __dynamic__.load('sys', locals()), 'path': __dynamic__.load('path', locals())}" in code


def test_match_statement_patterns():
    """Test that match patterns don't get Name transformations but do get preloaded."""
    source = """
from __future__ import _dynamic_import

from zabob_houdini.core import NodeInstance, ForwardReference

def check_input(inp):
    match inp:
        case None:
            return "none"
        case NodeInstance() | ForwardReference() as node:
            return f"node: {node.name}"
        case _:
            return "other"
"""

    code = transform_source(source)

    # Imports should be transformed
    assert (
        "__dynamic__._def('zabob_houdini.core', 'NodeInstance', 'NodeInstance', "
        "'ForwardReference', 'ForwardReference')"
        in code
    )

    # Match patterns should use bare names (not transformed)
    assert "case NodeInstance() | ForwardReference() as node:" in code
    assert "case None:" in code

    # The pattern variable 'node' is not a dynamic import, so it shouldn't be wrapped
    assert "return f'node: {node.name}'" in code or 'return f"node: {node.name}"' in code


def test_class_base_inheritance():
    """Test that base class names in class definitions use __dynamic__.load()."""
    source = """
from __future__ import _dynamic_import

from zabob_houdini.core import NodeBase

class MyNode(NodeBase):
    def __init__(self):
        self.value = NodeBase()  # This should be transformed
"""

    code = transform_source(source)

    # Import should be transformed
    assert "__dynamic__._def('zabob_houdini.core', 'NodeBase', 'NodeBase')" in code

    # Base class should use __dynamic__.load() to trigger import before class definition
    assert "class MyNode(__dynamic__.load('NodeBase')):" in code
    assert "class MyNode(NodeBase):" not in code

    # Usage in method body should use load()
    assert "self.value = __dynamic__.load('NodeBase', locals())()" in code


def test_class_generic_base():
    """Test that Generic[T] in class definitions uses __dynamic__.load() for both parts."""
    source = """
from __future__ import _dynamic_import

from typing import Generic, TypeVar

T = TypeVar('T')

class MyClass(Generic[T]):
    def __init__(self):
        pass
"""

    code = transform_source(source)

    # Imports should be transformed
    assert "__dynamic__._def('typing', 'Generic', 'Generic', 'TypeVar', 'TypeVar')" in code

    # Generic[T] should use __dynamic__.load() for Generic, but T is not imported so left alone
    assert "class MyClass(__dynamic__.load('Generic')[T]):" in code
    assert "class MyClass(Generic[T]):" not in code


def test_class_generic_with_imported_typevar():
    """Test that Generic[ImportedType] loads both Generic and the type parameter."""
    source = """
from __future__ import _dynamic_import

from typing import Generic
from zabob_houdini.core_types import T_Node

class NodeBase(Generic[T_Node]):
    pass
"""

    code = transform_source(source)

    # Both imports should be transformed
    assert "__dynamic__._def('typing', 'Generic', 'Generic')" in code
    assert "__dynamic__._def('zabob_houdini.core_types', 'T_Node', 'T_Node')" in code

    # Both Generic and T_Node should use __dynamic__.load()
    assert "class NodeBase(__dynamic__.load('Generic')[__dynamic__.load('T_Node')]):" in code
    assert "class NodeBase(Generic[T_Node]):" not in code


def test_imports_inside_functions_not_transformed():
    """Test that imports inside function bodies are not transformed."""
    source = """
from __future__ import _dynamic_import

from typing import Generic

def my_function():
    from zabob_houdini.core import NodeInstance
    return NodeInstance
"""

    code = transform_source(source)

    # Module-level import should be transformed
    assert "__dynamic__._def('typing', 'Generic', 'Generic')" in code

    # Import inside function should NOT be transformed
    assert "from zabob_houdini.core import NodeInstance" in code
    assert "_def('zabob_houdini.core', 'NodeInstance'" not in code
