"""Test variable access transformation for dynamic imports."""


from zabob_houdini.dyn import show_code, transform_source


def test_simple_compile():
    print('here')
    show_code('''
from __future__ import _dynamic_import
''',
              dynamic_mode=False)


def test_simple_variable_reference():
    """Test that variable references use __dynamic__.load()."""
    source = """
from __future__ import _dynamic_import

import zabob_houdini.core

x = zabob_houdini.core.node
"""

    code = transform_source(source)

    # Should have setup code
    assert "from zabob_houdini.dyn_import import dyn_import as __dynamic__" in code
    assert "__dynamic__ = __dynamic__(globals())" in code

    # Import should be transformed to _def_module call
    assert "__dynamic__._def_module('zabob_houdini.core', 'zabob_houdini.core')" in code

    # Variable reference 'zabob_houdini' should be transformed to __dynamic__.load() call
    assert "x = __dynamic__.load('zabob_houdini', locals()).core.node" in code


def test_variable_in_function():
    """Test variable references inside functions."""
    source = """
from __future__ import _dynamic_import

from zabob_houdini.core import node

def get_node():
    return node
"""

    code = transform_source(source)

    # Import should be transformed to _def call
    assert "__dynamic__._def('zabob_houdini.core', 'node', 'node')" in code

    # Variable reference inside function should be transformed to load() call
    assert "return __dynamic__.load('node', locals())" in code


def test_attribute_access():
    """Test attribute access on imported modules."""
    source = """
from __future__ import _dynamic_import

import zabob_houdini.core

def get_info():
    return zabob_houdini.core.node, zabob_houdini.core.chain
"""

    code = transform_source(source)

    # Import should be transformed to _def_module
    assert "__dynamic__._def_module('zabob_houdini.core', 'zabob_houdini.core')" in code

    # Both references to 'zabob_houdini' should use load()
    assert "__dynamic__.load('zabob_houdini', locals()).core.node" in code
    assert "__dynamic__.load('zabob_houdini', locals()).core.chain" in code


def test_function_call():
    """Test calling functions from imported modules."""
    source = """
from __future__ import _dynamic_import

from zabob_houdini.core import znode

result = znode('box', 'mybox')
"""

    code = transform_source(source)

    # Import should be transformed to _def
    assert "__dynamic__._def('zabob_houdini.core', 'znode', 'znode')" in code

    # Function call reference should use load()
    assert "result = __dynamic__.load('znode', locals())('box', 'mybox')" in code


def test_name_in_expression():
    """Test names used in various expression contexts."""
    source = """
from __future__ import _dynamic_import

import zabob_houdini.core
from zabob_houdini.utils import HashableMapping

# Various contexts where names appear
a = zabob_houdini.core
b = HashableMapping
c = zabob_houdini.core.znode
d = [zabob_houdini.core, HashableMapping]
e = (zabob_houdini.core, HashableMapping)
f = {'core': zabob_houdini.core, 'map': HashableMapping}
"""

    code = transform_source(source)

    # Imports should be transformed
    assert "__dynamic__._def_module('zabob_houdini.core', 'zabob_houdini.core')" in code
    assert "__dynamic__._def('zabob_houdini.utils', 'HashableMapping', 'HashableMapping')" in code

    # All variable references should use load()
    assert "a = __dynamic__.load('zabob_houdini', locals()).core" in code
    assert "b = __dynamic__.load('HashableMapping', locals())" in code
    assert "c = __dynamic__.load('zabob_houdini', locals()).core.znode" in code
    assert (
        "d = [__dynamic__.load('zabob_houdini', locals()).core, "
        "__dynamic__.load('HashableMapping', locals())]"
    ) in code
    assert (
        "e = (__dynamic__.load('zabob_houdini', locals()).core, "
        "__dynamic__.load('HashableMapping', locals()))"
    ) in code
    assert (
        "f = {'core': __dynamic__.load('zabob_houdini', locals()).core, "
        "'map': __dynamic__.load('HashableMapping', locals())}"
    ) in code


def test_match_statement_patterns():
    """Test that match patterns don't get Name transformations but do get preloaded."""
    source = """
from __future__ import _dynamic_import

from zabob_houdini.core import ZNode, ZNodeForwardRef

def check_input(inp):
    match inp:
        case None:
            return "none"
        case ZNode() | ZNodeForwardRef() as node:
            return f"node: {node.name}"
        case _:
            return "other"
"""

    code = transform_source(source)

    # Imports should be transformed
    assert (
        "__dynamic__._def('zabob_houdini.core', 'ZNode', 'ZNode', "
        "'ZNodeForwardRef', 'ZNodeForwardRef')"
        in code
    )

    # Match patterns should use bare names (not transformed)
    assert "case ZNode() | ZNodeForwardRef() as node:" in code
    assert "case None:" in code

    # The pattern variable 'node' is not a dynamic import, so it shouldn't be wrapped
    assert "return f'node: {node.name}'" in code or 'return f"node: {node.name}"' in code


def test_class_base_inheritance():
    """Test that base class names in class definitions use __dynamic__.load()."""
    source = """
from __future__ import _dynamic_import

from zabob_houdini.core import ZNodeBase

class MyNode(ZNodeBase):
    def __init__(self):
        self.value = ZNodeBase()  # This should be transformed
"""

    code = transform_source(source)

    # Import should be transformed
    assert "__dynamic__._def('zabob_houdini.core', 'ZNodeBase', 'ZNodeBase')" in code

    # Base class should use __dynamic__.load() to trigger import before class definition
    assert "class MyNode(__dynamic__.load('ZNodeBase')):" in code
    assert "class MyNode(ZNodeBase):" not in code

    # Usage in method body should use load()
    assert "self.value = __dynamic__.load('ZNodeBase', locals())()" in code


def test_class_generic_base():
    """Test that external imports like typing.Generic are NOT transformed."""
    source = """
from __future__ import _dynamic_import

from typing import Generic, TypeVar

T = TypeVar('T')

class MyClass(Generic[T]):
    def __init__(self):
        pass
"""

    code = transform_source(source, package_name="zabob_houdini")

    # External imports (typing) should NOT be transformed - left as-is
    assert "from typing import Generic, TypeVar" in code
    assert "__dynamic__._def('typing'" not in code

    # Class definition should remain unchanged since Generic is not transformed
    assert "class MyClass(Generic[T]):" in code


def test_class_generic_with_imported_typevar():
    """Test that zabob_houdini base classes with type parameters get transformed."""
    source = """
from __future__ import _dynamic_import

from zabob_houdini.core_node import ZNodeBase
from zabob_houdini.core_types import T_Node

class MyNode(ZNodeBase[T_Node]):
    pass
"""

    code = transform_source(source)

    # Both zabob_houdini imports should be transformed
    assert "__dynamic__._def('zabob_houdini.core_node', 'ZNodeBase', 'ZNodeBase')" in code
    assert "__dynamic__._def('zabob_houdini.core_types', 'T_Node', 'T_Node')" in code

    # Both ZNodeBase and T_Node should use __dynamic__.load()
    assert "class MyNode(__dynamic__.load('ZNodeBase')[__dynamic__.load('T_Node')]):" in code
    assert "class MyNode(ZNodeBase[T_Node]):" not in code


def test_imports_inside_functions_not_transformed():
    """Test that imports inside function bodies are not transformed."""
    source = """
from __future__ import _dynamic_import

from zabob_houdini.utils import HashableMapping

def my_function():
    import sys  # External import inside function
    return sys
"""

    code = transform_source(source)

    # Module-level zabob_houdini import should be transformed
    assert "__dynamic__._def('zabob_houdini.utils', 'HashableMapping', 'HashableMapping')" in code

    # Import inside function should NOT be transformed (even though it's sys, which is external)
    assert "import sys" in code
    assert "_def_module('sys'" not in code
