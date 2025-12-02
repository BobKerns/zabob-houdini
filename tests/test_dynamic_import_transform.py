"""Unit tests for dynamic import AST transformation."""

import ast
import sys
from typing import Any

import pytest

from testing.h_circular_graph import ignore
from zabob_houdini.dyn import (
    DynamicImportTransformer, _SymbolMap, dyn_import,
    transform_source,
)


class TestASTTransformation:
    """Test the AST transformation logic."""

    def test_marker_detection(self):
        """Test that the _dynamic_import marker is detected."""
        source = """
from __future__ import _dynamic_import

import foo
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformer.visit(tree)

        # Check that dynamic_mode was activated
        assert transformer.dynamic_mode

    def test_marker_with_other_futures(self):
        """Test that other __future__ imports are preserved."""
        source = """
from __future__ import annotations, _dynamic_import

import foo
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)

        # Should have preserved 'annotations' import
        # First statement should be: from __future__ import annotations
        first_stmt = transformed.body[0]
        assert isinstance(first_stmt, ast.ImportFrom)
        assert first_stmt.module == '__future__'
        assert len(first_stmt.names) == 1
        assert first_stmt.names[0].name == 'annotations'

    def test_import_transformation(self):
        """Test that 'import foo' is transformed correctly."""
        source = """
from __future__ import _dynamic_import

import foo
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)

        """Test that 'import foo as bar' is transformed correctly."""
        source = """
from __future__ import _dynamic_import

import foo as bar
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)
        ignore(transformed)  # TODO: add assertions

    def test_from_import_transformation(self):
        """Test that 'from foo import bar' is transformed correctly."""
        source = """
from __future__ import _dynamic_import

from foo import bar
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)
        ignore(transformed)  # TODO: add assertions

    def test_from_import_as_transformation(self):
        """Test that 'from foo import bar as baz' is transformed correctly."""
        source = """
from __future__ import _dynamic_import

from foo import bar as baz
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)
        ignore(transformed)  # TODO: add assertions

    def test_star_import_transformation(self):
        """Test that 'from foo import *' is transformed correctly."""
        source = """
from __future__ import _dynamic_import

from foo import *
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)
        ignore(transformed)  # TODO: add assertions

    def test_setup_code_generation(self):
        """Test that setup code is generated correctly."""
        source = """
from __future__ import _dynamic_import

import foo
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)

        # First should be import statement
        import_stmt = transformed.body[0]
        assert isinstance(import_stmt, ast.ImportFrom)
        assert import_stmt.module == 'zabob_houdini.dyn_import'
        assert len(import_stmt.names) == 1
        assert import_stmt.names[0].name == 'dyn_import'
        assert import_stmt.names[0].asname == '__dynamic__'

        # Second should be assignment: __dynamic__ = __dynamic__(globals())
        assign_stmt = transformed.body[1]
        assert isinstance(assign_stmt, ast.Assign)
        assert len(assign_stmt.targets) == 1
        assert isinstance(assign_stmt.targets[0], ast.Name)
        assert assign_stmt.targets[0].id == '__dynamic__'


class TestRuntimeBehavior:
    """Test the runtime behavior of the dynamic import system."""

    def test_symbol_map_creation(self):
        """Test _SymbolMap can be created and has _Ref attribute."""
        caller_globals: dict[str, Any] = {}
        symbol_map = dyn_import(caller_globals)

        assert isinstance(symbol_map, _SymbolMap)

    def test_symbol_map_returned(self):
        """Test that symbol map is returned by dyn_import."""
        caller_globals: dict[str, Any] = {}
        symbol_map = dyn_import(caller_globals)
        assert isinstance(symbol_map, _SymbolMap)
        # __dynamic__ is not stored in caller_globals, it's returned
        # The transformer stores it: __dynamic__ = __dynamic__(globals())

    def test_getattr_hook_installed(self):
        """Test that __getattr__ hook is installed."""
        caller_globals: dict[str, Any] = {}
        symbol_map = dyn_import(caller_globals)
        assert isinstance(symbol_map, _SymbolMap)
        assert '__getattr__' in caller_globals
        assert callable(caller_globals['__getattr__'])

    def test_import_module_ref_handling(self):
        """Test that _Ref for 'import module' is handled correctly."""
        caller_globals: dict[str, Any] = {}
        symbol_map = dyn_import(caller_globals)

        # import sys as system
        symbol_map._def_module('sys', 'system')
        symbol_map.load('system', caller_globals)
        value = caller_globals['system']
        assert value is sys

        # Should store a getter in symbol_map
        assert 'system' in symbol_map
        assert callable(symbol_map['system'])

        # Calling __getattr__ should trigger the import
        result = caller_globals['__getattr__']('system')
        assert result is sys

        # Should now be in caller_globals
        assert 'system' in caller_globals
        assert caller_globals['system'] is sys

    def test_from_import_ref_handling(self):
        """Test that _def for 'from module import symbol' is handled correctly."""
        caller_globals: dict[str, Any] = {}
        symbol_map = dyn_import(caller_globals)

        # Simulate: from sys import version
        symbol_map._def('sys', 'version', 'version')

        # Should store a getter in symbol_map
        assert 'version' in symbol_map
        assert callable(symbol_map['version'])

        # Calling __getattr__ should trigger the import
        result = caller_globals['__getattr__']('version')
        assert result == sys.version

        # Should now be in caller_globals
        assert 'version' in caller_globals
        assert caller_globals['version'] == sys.version

    def test_direct_assignment_not_in_symbol_map(self):
        """Test that direct assignments don't go through symbol map."""
        caller_globals: dict[str, Any] = {}
        symbol_map = dyn_import(caller_globals)

        # Set a regular value directly
        caller_globals['foo'] = 42

        # Should be in caller_globals
        assert caller_globals['foo'] == 42

        # Should NOT be in symbol_map
        assert 'foo' not in symbol_map

    def test_getattr_chaining(self):
        """Test that existing __getattr__ is chained."""
        def existing_getattr(name: str) -> Any:
            if name == 'custom':
                return 'custom_value'
            raise AttributeError(f"no attribute {name}")

        caller_globals: dict[str, Any] = {'__getattr__': existing_getattr}
        symbol_map = dyn_import(caller_globals)
        assert isinstance(symbol_map, _SymbolMap)

        # Should chain to existing __getattr__
        result = caller_globals['__getattr__']('custom')
        assert result == 'custom_value'

    def test_getattr_raises_on_missing(self):
        """Test that __getattr__ raises NameError for missing names."""
        caller_globals: dict[str, Any] = {}
        dyn_import(caller_globals)

        with pytest.raises(NameError, match="name 'nonexistent' is not defined"):
            caller_globals['__getattr__']('nonexistent')


class TestEndToEnd:
    """End-to-end tests of the complete system."""

    def test_complete_transformation_and_execution(self):
        """
        Test complete transformation and execution of transformed code.

        With the visit_Name transformation, variable references are wrapped
        in __getattr__ calls, which triggers the deferred import mechanism.
        """
        source = """
from __future__ import _dynamic_import

from sys import version
import os as operating_system

def get_info():
    return version, operating_system
"""
        # Parse and transform
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)
        ast.fix_missing_locations(transformed)

        # Compile and execute
        code = compile(transformed, '<test>', 'exec')
        test_globals: dict[str, Any] = {}
        exec(code, test_globals)

        # Call the function - this should trigger imports via __getattr__
        get_info = test_globals['get_info']
        version_result, os_result = get_info()

        import os
        assert version_result == sys.version
        assert os_result is os

        # Now they should be in globals (cached after first access)
        assert test_globals['version'] == sys.version
        assert test_globals['operating_system'] is os


class TestScopeTracking:
    """Test that scope tracking correctly handles local variables."""

    def test_lambda_parameters_not_transformed(self):
        """Test that lambda parameters are not transformed."""
        source = """
from __future__ import _dynamic_import

from operator import add

# Lambda parameter 'x' should not be transformed
func = lambda x: add(x, 1)
"""
        code = transform_source(source)

        # Import should be transformed
        assert "__dynamic__._def('operator', 'add', 'add')" in code

        # 'add' in lambda body should be transformed to load()
        assert "__dynamic__.load('add', locals())" in code

        # Lambda parameter 'x' should NOT be transformed - appears as plain 'x'
        # The lambda should look like: lambda x: __dynamic__.load('add', locals())(x, 1)
        assert "lambda x:" in code
        # Check that x is used directly in the call, not wrapped
        assert "(x, 1)" in code

    def test_comprehension_iteration_var_not_transformed(self):
        """Test that comprehension iteration variables are not transformed."""
        source = """
from __future__ import _dynamic_import

from zabob_houdini.core import node

# 'node' in the comprehension should not be transformed
nodes = [node for node in range(5)]
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)
        ast.fix_missing_locations(transformed)

        # Find the assignment with list comprehension
        assign_stmt = None
        for stmt in transformed.body:
            if isinstance(stmt, ast.Assign) and any(
                target.id == 'nodes' for target in stmt.targets if isinstance(target, ast.Name)
            ):
                assign_stmt = stmt
                break

        assert assign_stmt is not None
        comp_node = assign_stmt.value
        assert isinstance(comp_node, ast.ListComp)

        # The element expression should be a plain Name('node'), not __getattr__('node')
        elt = comp_node.elt
        assert isinstance(elt, ast.Name), "Iteration var 'node' should be plain Name"
        assert elt.id == 'node'

    def test_function_parameter_not_transformed(self):
        """Test that function parameters are not transformed."""
        source = """
from __future__ import _dynamic_import

from operator import add

def apply(x, y):
    # 'add' should be transformed, 'x' and 'y' should not
    return add(x, y)
"""
        code = transform_source(source)

        # Import should be transformed
        assert "__dynamic__._def('operator', 'add', 'add')" in code

        # 'add' should be transformed to load(), but 'x' and 'y' should not
        assert "return __dynamic__.load('add', locals())(x, y)" in code

        # Function parameters should appear as plain names
        assert "def apply(x, y):" in code

    def test_nested_comprehension_scopes(self):
        """Test that nested comprehensions track separate scopes."""
        source = """
from __future__ import _dynamic_import

from operator import add

# Outer 'x' and inner 'x' are different variables
result = [[add(x, y) for x in range(3)] for y in range(2)]
"""
        tree = ast.parse(source)
        transformer = DynamicImportTransformer("test_module")
        transformed = transformer.visit(tree)
        ast.fix_missing_locations(transformed)

        # Just verify it transforms without error
        # Both 'x' and 'y' should not be transformed (they're iteration vars)
        # 'add' should be transformed
        code = compile(transformed, '<test>', 'exec')
        assert code is not None
