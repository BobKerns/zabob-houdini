"""Mapping of hython test functions to their respective modules.

This module provides a registry that maps function names to their locations
in the split testing subpackage structure.
"""

from typing import Dict, Any, Callable
import importlib
from zabob_houdini.utils import JsonObject


class HythonTestRegistry:
    """Registry for hython test functions split across multiple modules."""

    def __init__(self):
        self._function_cache: Dict[str, Callable[[], JsonObject]] = {}

        # Module mapping: function_prefix -> module_name
        self.module_map = {
            '_test_basic_node_creation_in_houdini': 'houdini_integration',
            '_test_zabob_node_creation': 'node_creation',
            '_test_zabob_chain_creation': 'houdini_integration',
            '_test_layout_stress_test': 'layout_algorithm',
            '_test_simple_layout_demo': 'layout_algorithm',
            '_test_node_input_connections': 'input_connections',
            '_test_create_caches_result': 'core_caching',
            '_test_create_different_instances_different_nodes': 'core_caching',
            '_test_create_returns_tuple_of_node_instances': 'core_caching',
            '_test_convenience_methods_with_created_nodes': 'chain_positional_copy',
            '_test_convenience_methods_empty_chain': 'chain_positional_copy',
            '_test_copy_creates_independent_instance': 'enhanced_copy',
            '_test_copy_with_chain_inputs': 'enhanced_copy',
            '_test_copy_creates_independent_chain': 'enhanced_copy',
            '_test_copy_deep_copies_node_instances': 'enhanced_copy',
            '_test_copy_deep_copies_nested_chains': 'enhanced_copy',
            '_test_create_empty_chain_returns_empty_tuple': 'chain_positional_copy',
            '_test_copy_preserves_non_chain_inputs': 'enhanced_copy',
            '_test_node_registry_functionality': 'dependency_tracking',
            '_test_hou_module_available': 'houdini_integration',
            '_test_node_parentage': 'node_creation',
        }

    def get_function(self, function_name: str) -> Callable[[], JsonObject]:
        """Get a test function by name, loading its module if necessary."""
        if function_name in self._function_cache:
            return self._function_cache[function_name]

        module_name = self.module_map.get(function_name)
        if not module_name:
            raise ValueError(f"Unknown test function: {function_name}")

        module_path = f"zabob_houdini.testing.{module_name}"
        try:
            module = importlib.import_module(module_path)
            func = getattr(module, function_name)
            self._function_cache[function_name] = func
            return func
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Could not load {function_name} from {module_path}: {e}")

    def list_functions(self) -> list[str]:
        """List all available test function names."""
        return list(self.module_map.keys())


# Global registry instance
registry = HythonTestRegistry()
