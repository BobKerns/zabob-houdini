'''
Import hook to automatically transform imports into deferred loads.

Looks for files with `from __future__ import _dynamic_import` and transforms
all subsequent imports into deferred loading via _Ref tuples that are processed
by a custom __setattr__ hook.

Note: Star imports (from module import *) are NOT transformed and remain as regular
imports. This is intentional since star imports are primarily for interactive use,
and transforming them would require rewriting every global variable access as a
potential import lookup.
'''

import os
from pathlib import Path
import sys
import ast
import importlib
import re
from typing import Any, TypeVar
try:
    from typing import override  # type: ignore
except ImportError:
    def override(method: Any) -> Any:
        """No-op decorator for compatibility with older Python versions."""
        return method

MAX_LINE_CHECK = 100
"""
Number of lines to check for __future__ import check
"""

T = TypeVar('T')


def check(node: ast.AST, typ: type[T]) -> T:
    """Type check an AST node and cast it to the expected type.

    Args:
        node: The AST node to check
        typ: The expected AST node type

    Returns:
        The node cast to the expected type
    """
    if not isinstance(node, typ):
        raise TypeError(f"Expected node of type {typ.__name__}, got {type(node).__name__}")
    return node


class DynamicImportTransformer(ast.NodeTransformer):
    """Transform imports into deferred _Ref assignments after _dynamic_import marker."""

    def __init__(self, package_name: str, dynamic_mode: bool = False) -> None:
        self.package_name = package_name
        self.dynamic_mode = dynamic_mode  # Set to True after seeing the marker
        self.dynamic_names: set[str] = set()  # Track dynamically imported names
        self.in_match_pattern = False  # Skip Name transformation in match patterns
        self.in_function_or_class_body = False  # Skip import transformation in nested scopes
        self.local_names: set[str] = set()  # Track local variables in current scope

    def _ensure_location(self, node: ast.AST, source: ast.AST) -> ast.AST:
        """Ensure all nodes in the tree have location info.

        Args:
            node: The node to update
            source: The source node to copy location from

        Returns:
            The updated node
        """
        for child in ast.walk(node):
            if not hasattr(child, 'lineno'):
                ast.copy_location(child, source)
        return node

    def _visit_body(self, body: list[ast.AST]) -> list[ast.AST]:
        """Visit a list of statements, flattening any lists returned by visitors.

        When a visitor returns a list (like visit_Match), we need to splice it
        into the body rather than nesting it.
        """
        new_body = []
        for stmt in body:
            result = self.visit(stmt)
            if isinstance(result, list):
                new_body.extend(result)
            else:
                new_body.append(result)
        return new_body

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom | list[ast.AST] | ast.Expr | None:
        """Handle from imports - check for marker or transform if in dynamic mode."""
        if node.module == '__future__':
            if any(alias.name == '_dynamic_import' for alias in node.names):
                # Found the marker - switch to dynamic mode
                self.dynamic_mode = True

                # Remove _dynamic_import from the names
                remaining_names = [alias for alias in node.names if alias.name != '_dynamic_import']

                # Build result: remaining __future__ imports (if any) + setup code
                result = []
                if remaining_names:
                    # Include remaining __future__ imports
                    future_import = ast.ImportFrom(
                        module='__future__',
                        names=remaining_names,
                        level=0
                    )
                    ast.copy_location(future_import, node)
                    result.append(future_import)

                # Create setup code and copy location info
                for stmt in self._create_dynamic_setup():
                    self._ensure_location(stmt, node)
                    result.append(stmt)
                return result
            # Other __future__ imports pass through unchanged
            return node

        if not self.dynamic_mode:
            # Before marker, pass through unchanged
            return node

        # Don't transform imports inside function or class bodies
        if self.in_function_or_class_body:
            return node

        # In dynamic mode - transform to _Ref assignments
        return self._transform_from_import(node)

    def visit_Import(self, node: ast.Import) -> ast.Import | list[ast.Expr]:
        """Handle regular imports - transform if in dynamic mode."""
        if not self.dynamic_mode:
            return node

        # Don't transform imports inside function or class bodies
        if self.in_function_or_class_body:
            return node

        # Transform: import foo [as bar] => __dynamic__._def('foo', None, 'bar')
        # Each import statement becomes a separate _def call since modules differ
        stmts = []
        for alias in node.names:
            module_name = alias.name
            dest_name = alias.asname if alias.asname else alias.name

            # Track this name as dynamically imported
            self.dynamic_names.add(dest_name)

            # import foo [as bar] => __dynamic__._def('foo', None, 'bar')
            # Module import: from=None, to=dest_name
            stmt = ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id='__dynamic__', ctx=ast.Load()),
                        attr='_def_module',
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.Constant(value=module_name),
                        ast.Constant(value=dest_name)
                    ],
                    keywords=[]
                )
            )
            self._ensure_location(stmt, node)
            stmts.append(stmt)

        return stmts if len(stmts) > 1 else stmts[0]

    def _create_dynamic_setup(self) -> list[ast.AST]:
        """Create the setup code for dynamic imports."""
        return [
            # from zabob_houdini.dyn_import import dyn_import as __dynamic__
            ast.ImportFrom(
                module='zabob_houdini.dyn_import',
                names=[
                    ast.alias(name='dyn_import', asname='__dynamic__')
                ],
                level=0
            ),
            # __dynamic__ = __dynamic__(globals())
            ast.Assign(
                targets=[ast.Name(id='__dynamic__', ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id='__dynamic__', ctx=ast.Load()),
                    args=[ast.Call(
                        func=ast.Name(id='globals', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    )],
                    keywords=[]
                )
            )
        ]

    def _transform_from_import(self, node: ast.ImportFrom) -> ast.Expr | ast.ImportFrom:
        """Transform from imports into _def() or _star() registration call."""
        module_name = node.module or ''

        # Handle relative imports
        if module_name.startswith('.'):
            module_name = f"{self.package_name}.{module_name.lstrip('.')}"

        # Check for star import
        if len(node.names) == 1 and node.names[0].name == '*':
            # from foo import * => unchanged, nor amenable to dynamic import.
            return node

        # Collect all import arguments: module, from1, to1, from2, to2, ...
        args = [ast.Constant(value=module_name)]

        for alias in node.names:
            src_name = alias.name
            dest_name = alias.asname if alias.asname else src_name

            # Track this name as dynamically imported
            self.dynamic_names.add(dest_name)

            # from foo import bar [as baz] => __dynamic__._def('foo', 'bar', 'baz')
            args.extend([
                ast.Constant(value=src_name),
                ast.Constant(value=dest_name)
            ])

        # Emit single _def() call with module + from/to pairs
        stmt = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='__dynamic__', ctx=ast.Load()),
                    attr='_def',
                    ctx=ast.Load()
                ),
                args=args,  # pyright: ignore[reportArgumentType]
                keywords=[]
            )
        )
        self._ensure_location(stmt, node)
        return stmt

    @override
    def visit_Match(self, node: ast.Match) -> ast.Match | list[ast.AST]:
        """
        Visit Match statement - ensure dynamic imports in patterns are loaded first.

        Match patterns need actual class objects, not names. We scan the patterns
        for dynamically imported names and emit __getattr__ calls before the match
        to trigger loading.
        """
        if not self.dynamic_mode:
            return self.generic_visit(node)  # pyright: ignore[reportReturnType]

        # Collect dynamic names used in all case patterns
        pattern_names = set()
        for case in node.cases:
            pattern_names.update(self._collect_pattern_names(case.pattern))

        # Filter to only dynamically imported names
        dynamic_pattern_names = pattern_names & self.dynamic_names

        if not dynamic_pattern_names:
            # No dynamic imports in patterns, process normally
            return self.generic_visit(node)  # pyright: ignore[reportReturnType]

        # Emit load statements before the match
        result: list[ast.AST] = []
        for name in sorted(dynamic_pattern_names):  # Sort for deterministic output
            # Emit: __getattr__('name')  # Ensure name is loaded
            load_stmt = ast.Expr(
                value=ast.Call(
                    func=ast.Name(id='__getattr__', ctx=ast.Load()),
                    args=[ast.Constant(value=name)],
                    keywords=[]
                )
            )
            # Copy location info from the match statement
            self._ensure_location(load_stmt, node)
            result.append(load_stmt)

        # Now process the match statement normally (patterns keep bare names)
        processed = self.generic_visit(node)

        # generic_visit returns a single node or list - handle both
        if isinstance(processed, list):
            result.extend(processed)
        else:
            result.append(processed)

        return result

    def _collect_pattern_names(self, pattern: ast.pattern) -> set[str]:
        """Collect all Name nodes from a pattern (recursively)."""
        names = set()

        if isinstance(pattern, ast.MatchAs):
            if pattern.pattern:
                names.update(self._collect_pattern_names(pattern.pattern))
        elif isinstance(pattern, ast.MatchOr):
            for p in pattern.patterns:
                names.update(self._collect_pattern_names(p))
        elif isinstance(pattern, ast.MatchClass):
            # This is where class names appear: NodeInstance(), etc.
            if isinstance(pattern.cls, ast.Name):
                names.add(pattern.cls.id)
            elif isinstance(pattern.cls, ast.Attribute):
                # Handle qualified names like module.ClassName
                # Extract the base name
                node = pattern.cls
                while isinstance(node, ast.Attribute):
                    node = node.value
                if isinstance(node, ast.Name):
                    names.add(node.id)
            # Recursively collect from patterns
            for p in pattern.patterns:
                names.update(self._collect_pattern_names(p))
            for p in pattern.kwd_patterns:
                names.update(self._collect_pattern_names(p))
        elif isinstance(pattern, ast.MatchSequence):
            for p in pattern.patterns:
                names.update(self._collect_pattern_names(p))
        elif isinstance(pattern, ast.MatchMapping):
            for p in pattern.patterns:
                names.update(self._collect_pattern_names(p))

        return names

    def _collect_local_names(self, body: list[ast.stmt]) -> set[str]:
        """Collect all local variable names from a scope body."""
        names = set()

        for stmt in body:
            # Assignment targets
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    names.update(self._extract_names(target))
            elif isinstance(stmt, ast.AnnAssign) and stmt.target:
                names.update(self._extract_names(stmt.target))
            elif isinstance(stmt, ast.AugAssign) and stmt.target:
                names.update(self._extract_names(stmt.target))
            # For loops
            elif isinstance(stmt, ast.For):
                names.update(self._extract_names(stmt.target))
            # With statements
            elif isinstance(stmt, ast.With):
                for item in stmt.items:
                    if item.optional_vars:
                        names.update(self._extract_names(item.optional_vars))

        return names

    def _extract_names(self, node: ast.expr | ast.pattern) -> set[str]:
        """Extract variable names from an expression or pattern node."""
        names = set()

        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for elt in node.elts:
                names.update(self._extract_names(elt))
        elif isinstance(node, ast.Starred):
            names.update(self._extract_names(node.value))

        return names

    def visit_match_case(self, node: ast.match_case) -> ast.match_case:
        """
        Visit match case - keep patterns unchanged (processed by visit_Match).

        Match patterns require bare Name or Attribute nodes, not Call nodes.
        """
        # Transform guard and body normally, but leave pattern unchanged
        if node.guard:
            node.guard = self.visit(node.guard)
        node.body = self._visit_body(node.body)  # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]

        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """
        Visit function definition - track local scope for variable shadowing.

        Local variables inside functions can shadow dynamically imported names.
        """
        if not self.dynamic_mode:
            return self.generic_visit(node)  # pyright: ignore[reportReturnType]

        # Process decorators and annotations normally (they execute at module level)
        node.decorator_list = [self.visit(decorator) for decorator in node.decorator_list]
        if node.returns:
            node.returns = self.visit(node.returns)

        # Process arguments annotations normally
        node.args = self.visit(node.args)

        # Save current scope and track local names
        prev_local_names = self.local_names
        was_in_body = self.in_function_or_class_body

        # Collect parameter names
        param_names = {arg.arg for arg in node.args.args}
        param_names.update({arg.arg for arg in node.args.posonlyargs})
        param_names.update({arg.arg for arg in node.args.kwonlyargs})
        if node.args.vararg:
            param_names.add(node.args.vararg.arg)
        if node.args.kwarg:
            param_names.add(node.args.kwarg.arg)

        # Collect local assignments
        local_assigns = self._collect_local_names(node.body)

        # Combine parameters and local assignments
        self.local_names = prev_local_names | param_names | local_assigns
        self.in_function_or_class_body = True

        # Process body with local scope tracking
        node.body = self._visit_body(node.body)  # pyright: ignore[reportAttributeAccessIssue, reportArgumentType]

        # Restore previous scope
        self.local_names = prev_local_names
        self.in_function_or_class_body = was_in_body

        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """Visit async function definition - track local scope like regular functions."""
        if not self.dynamic_mode:
            return self.generic_visit(node)  # pyright: ignore[reportReturnType]

        # Process decorators and annotations normally
        node.decorator_list = [self.visit(decorator) for decorator in node.decorator_list]
        if node.returns:
            node.returns = self.visit(node.returns)

        # Process arguments annotations normally
        node.args = self.visit(node.args)

        # Save current scope and track local names
        prev_local_names = self.local_names
        was_in_body = self.in_function_or_class_body

        # Collect parameter names
        param_names = {arg.arg for arg in node.args.args}
        param_names.update({arg.arg for arg in node.args.posonlyargs})
        param_names.update({arg.arg for arg in node.args.kwonlyargs})
        if node.args.vararg:
            param_names.add(node.args.vararg.arg)
        if node.args.kwarg:
            param_names.add(node.args.kwarg.arg)

        # Collect local assignments
        local_assigns = self._collect_local_names(node.body)

        # Combine parameters and local assignments
        self.local_names = prev_local_names | param_names | local_assigns
        self.in_function_or_class_body = True

        # Process body with local scope tracking
        node.body = self._visit_body(node.body)  # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]

        # Restore previous scope
        self.local_names = prev_local_names
        self.in_function_or_class_body = was_in_body

        return node

    def visit_Lambda(self, node: ast.Lambda) -> ast.Lambda:
        """Visit lambda expression - track parameters as local variables."""
        if not self.dynamic_mode:
            visited = self.generic_visit(node)
            if not isinstance(visited, ast.Lambda):
                raise TypeError("generic_visit returned unexpected type")
            return visited

        # Save current scope
        prev_local_names = self.local_names

        # Collect parameter names
        param_names = {arg.arg for arg in node.args.args}
        param_names.update({arg.arg for arg in node.args.posonlyargs})
        param_names.update({arg.arg for arg in node.args.kwonlyargs})
        if node.args.vararg:
            param_names.add(node.args.vararg.arg)
        if node.args.kwarg:
            param_names.add(node.args.kwarg.arg)

        # Update scope with lambda parameters
        self.local_names = prev_local_names | param_names

        # Visit the lambda body
        node.body = self.visit(node.body)

        # Restore previous scope
        self.local_names = prev_local_names

        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """
        Visit class definition - track local scope for variable shadowing.

        Class bodies can contain local variables that shadow dynamically imported names.
        """
        if not self.dynamic_mode:
            return check(self.generic_visit(node), ast.ClassDef)

        # Process decorators normally (execute at module level)
        node.decorator_list = [self.visit(decorator) for decorator in node.decorator_list]

        # Process bases with special handling for dynamic names (execute at module level)
        node.bases = [self._transform_base(base) for base in node.bases]

        # Process keywords normally (execute at module level)
        node.keywords = [self.visit(keyword) for keyword in node.keywords]

        # Save current scope and track local names
        prev_local_names = self.local_names
        was_in_body = self.in_function_or_class_body

        # Collect local assignments in class body
        local_assigns = self._collect_local_names(node.body)

        # Update scope with class-local names
        self.local_names = prev_local_names | local_assigns
        self.in_function_or_class_body = True

        # Process body with local scope tracking
        node.body = self._visit_body(node.body)  # pyright: ignore[reportArgumentType, reportAttributeAccessIssue]

        # Restore previous scope
        self.local_names = prev_local_names
        self.in_function_or_class_body = was_in_body

        return node

    def _transform_base(self, base: ast.expr) -> ast.expr:
        """
        Transform a base class expression, converting dynamic names to __dynamic__.load() calls.

        This allows dynamic imports to be loaded before the class is defined, while
        maintaining valid AST structure that unparsing handles correctly.
        """
        if isinstance(base, ast.Name) and base.id in self.dynamic_names:
            # Transform: Generic => __dynamic__.load('Generic')
            load_call = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='__dynamic__', ctx=ast.Load()),
                    attr='load',
                    ctx=ast.Load()
                ),
                args=[ast.Constant(value=base.id)],
                keywords=[]
            )
            # Visit the created Call node to transform any nested expressions
            return self.visit(load_call)
        elif isinstance(base, ast.Subscript):
            # Handle subscripted generics: Generic[T_Node] => __dynamic__.load('Generic')[__dynamic__.load('T_Node')]
            # Transform both the base and the slice (which contains the type parameter)
            base.value = self._transform_base(base.value)
            base.slice = self._transform_base(base.slice)
            # Visit the modified Subscript to handle any other transformations
            return self.visit(base)
        elif isinstance(base, ast.Tuple):
            # Handle multiple type parameters: Generic[T, U] =>
            # __dynamic__.load('Generic')[__dynamic__.load('T'), __dynamic__.load('U')]
            base.elts = [self._transform_base(elt) for elt in base.elts]
            # Visit the modified Tuple to handle any other transformations
            return self.visit(base)
        else:
            # For all other expressions, use normal visitor to ensure complete transformation
            return self.visit(base)

    def visit_ListComp(self, node: ast.ListComp) -> ast.ListComp:
        """Visit list comprehension - track iteration variables in local scope."""
        if not self.dynamic_mode:
            return check(self.generic_visit(node), ast.ListComp)

        prev_local_names = self.local_names
        # Collect all iteration variables from generators
        comp_locals = set()
        for gen in node.generators:
            comp_locals.update(self._extract_names(gen.target))

        self.local_names = prev_local_names | comp_locals
        result = self.generic_visit(node)
        self.local_names = prev_local_names
        return check(result, ast.ListComp)

    def visit_SetComp(self, node: ast.SetComp) -> ast.SetComp:
        """Visit set comprehension - track iteration variables in local scope."""
        if not self.dynamic_mode:
            return check(self.generic_visit(node), ast.SetComp)

        prev_local_names = self.local_names
        comp_locals = set()
        for gen in node.generators:
            comp_locals.update(self._extract_names(gen.target))

        self.local_names = prev_local_names | comp_locals
        result = self.generic_visit(node)
        self.local_names = prev_local_names
        return check(result, ast.SetComp)

    def visit_DictComp(self, node: ast.DictComp) -> ast.DictComp:
        """Visit dict comprehension - track iteration variables in local scope."""
        if not self.dynamic_mode:
            return check(self.generic_visit(node), ast.DictComp)

        prev_local_names = self.local_names
        comp_locals = set()
        for gen in node.generators:
            comp_locals.update(self._extract_names(gen.target))

        self.local_names = prev_local_names | comp_locals
        result = self.generic_visit(node)
        self.local_names = prev_local_names
        return check(result, ast.DictComp)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> ast.GeneratorExp:
        """Visit generator expression - track iteration variables in local scope."""
        if not self.dynamic_mode:
            return check(self.generic_visit(node), ast.GeneratorExp)

        prev_local_names = self.local_names
        comp_locals = set()
        for gen in node.generators:
            comp_locals.update(self._extract_names(gen.target))

        self.local_names = prev_local_names | comp_locals
        result = self.generic_visit(node)
        self.local_names = prev_local_names
        return check(result, ast.GeneratorExp)

    def visit_Name(self, node: ast.Name) -> ast.Name | ast.Call:
        """
        Transform Name nodes for dynamically imported variables.

        When a dynamically imported name is referenced (Load context),
        wrap it in a __dynamic__.load() call that checks locals() for shadowing.

        The scope tracking (local_names) is an optimization to avoid unnecessary
        runtime checks, but semantic correctness comes from the runtime locals() check.
        """
        if not self.dynamic_mode:
            return node

        # Skip transformation in match patterns
        if self.in_match_pattern:
            return node

        # Only transform Load contexts (reading the variable)
        # Store contexts (assignment) should pass through
        if not isinstance(node.ctx, ast.Load):
            return node

        # Only transform names that were dynamically imported
        if node.id not in self.dynamic_names:
            return node

        # Optimization: Skip transformation for known local variables
        # But runtime check in __dynamic__.load() is the semantic guarantee
        if node.id in self.local_names:
            return node

        # Transform: name => __dynamic__.load('name', locals())
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='__dynamic__', ctx=ast.Load()),
                attr='load',
                ctx=ast.Load()
            ),
            args=[
                ast.Constant(value=node.id),
                ast.Call(
                    func=ast.Name(id='locals', ctx=ast.Load()),
                    args=[],
                    keywords=[]
                )
            ],
            keywords=[]
        )


def do_transform(source: str | ast.AST,
                 package_name: str = "<<string>>",
                 dynamic_mode: bool = False) -> ast.Module:
    """Transform source code or AST module using DynamicImportTransformer.

    Args:
        source: The source code string or AST module to transform
        package_name: The package name for resolving relative imports
        dynamic_mode: Whether to enable dynamic import transformation immediately
    Returns:
        The transformed AST module
    """
    if isinstance(source, str):
        tree = ast.parse(source)
    else:
        tree = source

    transformer = DynamicImportTransformer(package_name,
                                           dynamic_mode=dynamic_mode)
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)
    # Double-check: walk the tree and set location on any node that's still missing it
    for node in ast.walk(tree):
        if isinstance(node, ast.AST) and not hasattr(node, 'lineno'):
            # Use a reasonable default - first line
            node.lineno = 1             # type: ignore
            node.col_offset = 0         # type: ignore
            node.end_lineno = 1         # type: ignore
            node.end_col_offset = 0     # type: ignore
    return transformed_tree


_RE_FUTURE_IMPORT = re.compile(
    r'^\s*from\s+__future__\s+import\s.*\b_dynamic_import\b'
    )


def transform_script(source: str, filename: str = '<script>') -> tuple[Any, bool]:
    """Transform a script's source code if it uses dynamic imports.

    Args:
        source: The script source code
        filename: Optional filename for error messages

    Returns:
        Tuple of (compiled_code, was_transformed) where compiled_code is a code object
    """
    # Check if script uses dynamic imports
    has_marker = False
    for line in source.split('\n')[:MAX_LINE_CHECK]:
        if _RE_FUTURE_IMPORT.match(line):
            has_marker = True
            break

    if not has_marker:
        return (compile(source, filename, 'exec'), False)

    # Transform and compile
    tree = do_transform(source, '__main__')
    code = compile(tree, filename, 'exec')
    return (code, True)


class DynamicImportLoader(importlib.abc.SourceLoader):
    """Loader that transforms source code before execution."""

    def __init__(self, fullname: str, path: str):
        self.fullname = fullname
        self.path = path

    def get_filename(self, fullname: str) -> str:
        return self.path

    def get_data(self, path: str) -> bytes:
        with open(path, 'rb') as f:
            return f.read()

    def exec_module(self, module: Any) -> None:
        """Execute module with transformed source."""
        source = self.get_data(self.path).decode('utf-8')

        package_name = self.fullname.rsplit('.', 1)[0]
        tree = do_transform(source, package_name)
        # Compile and execute
        code = compile(tree, self.path, 'exec')
        exec(code, module.__dict__)


DYNAMIC_IMPORT_ALLOW = {'zabob_houdini', 'tests', 'test_'}
"""
Allowed module origins for dynamic import processing. A comma-separated list
of additional origins can be specified via the DYNAMIC_IMPORT_ALLOW environment
variable.

Note: Scripts executed directly use transform_script() instead of the import hook.
"""
DYNAMIC_IMPORT_ALLOW |= {f for f in os.getenv("DYNAMIC_IMPORT_ALLOW", "").split(',') if f}


class DynamicImportFinder(importlib.abc.MetaPathFinder):
    """Finder that intercepts imports and checks for dynamic_import __future__."""

    def find_spec(self, fullname: str, path: Any, target: Any = None) -> importlib.machinery.ModuleSpec | None:
        """Find module spec - intercept BEFORE normal import to check for marker."""
        # Process zabob_houdini modules and test modules
        if not any(fullname.startswith(origin) for origin in DYNAMIC_IMPORT_ALLOW):
            return None

        # Determine search paths
        if path is None:
            # Top-level module, search sys.path
            search_paths = sys.path
        else:
            # Submodule, use provided path (package's __path__)
            search_paths = path

        # Convert module name to file path
        parts = fullname.split('.')
        module_name = parts[-1]  # Last component is the actual module name

        for search_path in search_paths:
            search_dir = Path(search_path)

            # Try as a package (__init__.py)
            package_path = search_dir / module_name
            if package_path.is_dir():
                py_file = package_path
            else:
                # Try as a module
                py_file = search_dir / f"{module_name}.py"

            # Check if file has dynamic_import __future__ declaration
            if py_file.exists():
                try:
                    with open(py_file, 'r') as f:
                        # Only read first ~100 lines to check for marker
                        for _ in range(MAX_LINE_CHECK):
                            line = f.readline()
                            if not line:
                                break
                            if _RE_FUTURE_IMPORT.match(line):
                                # Found it - use our transformer
                                loader = DynamicImportLoader(fullname, str(py_file))
                                return importlib.machinery.ModuleSpec(
                                    fullname, loader, origin=str(py_file)
                                )
                except (IOError, OSError):
                    pass

        return None


def install_import_hook() -> None:
    """Install the dynamic import hook."""
    if not any(isinstance(finder, DynamicImportFinder) for finder in sys.meta_path):
        sys.meta_path.insert(0, DynamicImportFinder())


# Auto-install when imported
install_import_hook()
