"""
Convenience module for working with and testing the dynamic import system.

This module provides utilities for transforming Python code to use deferred imports,
examining the transformed AST, viewing the generated source code, and inspecting
the resulting bytecode.

The dynamic import system allows imports to be deferred until first use, which helps
break circular dependencies and improves startup time for large modules.

Limitations:
    Star imports (from module import *) are not transformed and remain as regular
    imports. This is intentional since star imports are primarily for interactive use,
    and transforming them would require rewriting every global variable access as a
    potential import lookup.

Example:
    >>> from zabob_houdini.dyn import transform, show_source
    >>> source = '''
    ... from __future__ import _dynamic_import
    ... from zabob_houdini.core import NodeInstance
    ... node = NodeInstance("box")
    ... '''
    >>> tree = transform(source)
    >>> show_source(tree)
    from zabob_houdini.dyn_import import dyn_import as __dynamic__
    __dynamic__ = __dynamic__(globals())
    __dynamic__._def('zabob_houdini.core', 'NodeInstance', 'NodeInstance')
    node = __dynamic__.load('NodeInstance', locals())('box')
"""

import ast
from dis import dis
from typing import Literal

from zabob_houdini.dyn_loader import (
    do_transform, DynamicImportTransformer, DynamicImportFinder, DynamicImportLoader,
)
from zabob_houdini.dyn_import import _SymbolMap, dyn_import


def transform(source: str | ast.AST,
              package_name: str = "<<string>>",
              dynamic_mode: bool = False) -> ast.Module:
    """Transform source code or AST to use dynamic imports.

    Args:
        source: Python source code string or AST module to transform
        package_name: Package name for resolving relative imports (default: "<<string>>")
        dynamic_mode: If True, enable dynamic import transformation immediately without
                     requiring `from __future__ import _dynamic_import` (default: False)

    Returns:
        Transformed AST module with dynamic import setup and transformed imports

    Example:
        >>> tree = transform("from foo import bar\\nprint(bar())")
        >>> ast.unparse(tree)
        "from foo import bar\\nprint(bar())"  # Not transformed (no marker)

        >>> tree = transform("from foo import bar\\nprint(bar())", dynamic_mode=True)
        >>> ast.unparse(tree)
        "__dynamic__._def('foo', 'bar', 'bar')\\nprint(__dynamic__.load('bar', locals())())"
    """
    return do_transform(source, package_name, dynamic_mode)


def show_ast(source: str | ast.AST,
             package_name: str = "<show-ast>",
             dynamic_mode: bool = False,
             transform: bool = True) -> None:
    """Print the AST tree structure for debugging and inspection.

    Displays the abstract syntax tree with indentation and field names,
    useful for understanding how code is transformed.

    Args:
        source: Python source code string or AST to examine
        package_name: Package name for resolving relative imports (default: "<show-ast>")
        dynamic_mode: If True, enable dynamic import transformation (default: False)
        transform: If True, apply transformation before showing AST (default: True)

    Example:
        >>> show_ast("x = 42", transform=False)
        Module(
            body=[
                Assign(
                    targets=[
                        Name(id='x', ctx=Store())],
                    value=Constant(value=42))],
            type_ignores=[])
    """
    if isinstance(source, str):
        tree = ast.parse(source)
    else:
        tree = source
    if transform:
        tree = do_transform(tree, package_name, dynamic_mode)

    print(ast.dump(tree, indent=4, annotate_fields=True))


def show_source(source: str | ast.AST,
                package_name: str = "<show-source>",
                dynamic_mode: bool = True,
                ) -> None:
    """Print the transformed Python source code.

    Transforms the input and unparses the AST back to Python source code,
    showing exactly what the dynamic import system generates.

    Args:
        source: Python source code string or AST to transform
        package_name: Package name for resolving relative imports (default: "<show-source>")
        dynamic_mode: If True, enable dynamic import transformation (default: True)

    Example:
        >>> show_source('''
        ... from foo import bar, baz
        ... result = bar() + baz()
        ... ''')
        from zabob_houdini.dyn_import import dyn_import as __dynamic__
        __dynamic__ = __dynamic__(globals())
        __dynamic__._def('foo', 'bar', 'bar', 'baz', 'baz')
        result = __dynamic__.load('bar', locals())() + __dynamic__.load('baz', locals())()
    """
    print(transform_source(source, package_name, dynamic_mode))


def transform_source(source: str | ast.AST,
                     package_name: str = "<transform-source>",
                     dynamic_mode: bool = False,
                     ) -> str:
    if isinstance(source, str):
        tree = ast.parse(source)
    else:
        tree = source
    tree = do_transform(tree, package_name, dynamic_mode)
    return ast.unparse(tree)


def show_code(source: str | ast.AST,
              package_name: str = "<show-code>",
              dynamic_mode: bool = False,
              transform: bool = True,
              mode: Literal['exec', 'eval', 'single'] = 'exec'
              ) -> None:
    """Disassemble and display Python bytecode for transformed source.

    Compiles the (optionally transformed) AST to bytecode and shows the
    disassembly, useful for understanding performance implications and
    verifying transformation correctness.

    Args:
        source: Python source code string, AST module, statement, or expression
        package_name: Package name for resolving relative imports (default: "<show-code>")
        dynamic_mode: If True, enable dynamic import transformation (default: False)
        transform: If True, apply transformation before disassembly (default: True)
        mode: Compilation mode - 'exec', 'eval', or 'single' (default: 'exec')

    Example:
        >>> show_code("x = 42", transform=False)
          1           0 RESUME                   0
                      2 LOAD_CONST               0 (42)
                      4 STORE_NAME               0 (x)
                      6 RETURN_CONST             1 (None)
    """
    match source:
        case str():
            tree = ast.parse(source)
        case ast.Module():
            tree = source
        case ast.stmt():
            tree = ast.Module(body=[source])
        case ast.expr():
            tree = ast.Module(body=[ast.Expr(value=source)])
        case _:
            raise TypeError(f"Unsupported source type: {type(source)}")
    if transform:
        tree = do_transform(tree, package_name, dynamic_mode)
    code = compile(tree, filename=package_name, mode=mode)
    dis(code)


__all__ = (
    'DynamicImportFinder',
    'DynamicImportLoader',
    'DynamicImportTransformer',
    "transform_source",
    "_SymbolMap",
    'dyn_import',
    'transform',
    'show_ast',
    'show_source',
    'show_code',
)
