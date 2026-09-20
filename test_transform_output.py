#!/usr/bin/env python3
"""Quick test to verify transformation output."""

import ast
from zabob_houdini.dyn_loader import DynamicImportTransformer

source = """
from __future__ import _dynamic_import

from zabob_houdini.util import success_result, error_result
print(success_result())
print(error_result())
"""

tree = ast.parse(source)
transformer = DynamicImportTransformer("test_module")
transformed = transformer.visit(tree)
ast.fix_missing_locations(transformed)

code = ast.unparse(transformed)
print(code)
