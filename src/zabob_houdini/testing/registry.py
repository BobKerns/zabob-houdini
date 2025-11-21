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

        # Module mapping: function_name -> module_name
        self.module_map = {
            # houdini_integration - basic Houdini functionality
            '_test_basic_node_creation_in_houdini': 'houdini_integration',
            '_test_zabob_chain_creation': 'houdini_integration',
            '_test_hou_module_available': 'houdini_integration',

            # node_creation - node instantiation and parentage
            '_test_zabob_node_creation': 'node_creation',
            '_test_node_parentage': 'node_creation',
            '_test_geometry_creation': 'node_creation',
            '_test_parameter_setting': 'node_creation',

            # input_connections - node input handling
            '_test_node_input_connections': 'input_connections',
            '_test_input_connections_basic': 'input_connections',
            '_test_chain_input_delegation': 'input_connections',
            '_test_multiple_inputs_basic': 'input_connections',
            '_test_chain_input_connections': 'input_connections',
            '_test_multiple_input_merge': 'input_connections',

            # core_caching - creation and caching behavior
            '_test_create_caches_result': 'core_caching',
            '_test_create_different_instances_different_nodes': 'core_caching',
            '_test_create_returns_tuple_of_node_instances': 'core_caching',

            # layout_algorithm - layout and positioning
            '_test_layout_stress_test': 'layout_algorithm',
            '_test_simple_layout_demo': 'layout_algorithm',

            # chain_positional_copy - chain convenience and positioning
            '_test_convenience_methods_with_created_nodes': 'chain_positional_copy',
            '_test_convenience_methods_empty_chain': 'chain_positional_copy',
            '_test_create_empty_chain_returns_empty_tuple': 'chain_positional_copy',
            '_test_chain_reference_vs_copy': 'chain_positional_copy',
            '_test_chain_rejects_input_parameter': 'chain_positional_copy',
            '_test_positional_reordering': 'chain_positional_copy',

            # enhanced_copy - copy operations
            '_test_copy_creates_independent_instance': 'enhanced_copy',
            '_test_copy_with_chain_inputs': 'enhanced_copy',
            '_test_copy_creates_independent_chain': 'enhanced_copy',
            '_test_copy_deep_copies_node_instances': 'enhanced_copy',
            '_test_copy_deep_copies_nested_chains': 'enhanced_copy',
            '_test_copy_preserves_non_chain_inputs': 'enhanced_copy',
            '_test_enhanced_copy_integration': 'enhanced_copy',
            '_test_copy_signature_includes_args': 'enhanced_copy',

            # dependency_tracking - node registry and tracking
            '_test_node_registry_functionality': 'dependency_tracking',
            '_test_dependency_tracking': 'dependency_tracking',

            # input_validation - input validation and error handling
            '_test_parameter_validation_comprehensive': 'input_validation',
            '_test_valid_input_patterns': 'input_validation',
            '_test_node_input_validation': 'input_validation',
            '_test_invalid_input_types': 'input_validation',
            '_test_merge_inputs_sparse_handling': 'input_validation',

            # node_duplication - diamond patterns and deduplication
            '_test_diamond_pattern_creation': 'node_duplication',
            '_test_diamond_no_duplication': 'node_duplication',

            # node_context - NodeContext functionality (skipped tests)
            '_test_node_context_dataclass': 'node_context',
            '_test_node_context_context_manager': 'node_context',
            '_test_node_context_mutable': 'node_context',
            '_test_context_with_node_instance': 'node_context',
            '_test_context_with_string_path': 'node_context',
            '_test_context_usage_example': 'node_context',
            '_test_context_preserves_parent_type': 'node_context',
            '_test_node_context_node_method': 'node_context',
            '_test_node_context_name_lookup': 'node_context',
            '_test_node_context_integration': 'node_context',
            '_test_node_context_chain_method': 'node_context',
            '_test_node_context_chain_registration': 'node_context',
            '_test_node_context_merge_method': 'node_context',
            '_test_node_context_merge_registration': 'node_context',
            '_test_parent_validation_chain': 'node_context',
            '_test_parent_validation_merge': 'node_context',
            '_test_node_context_parent_validation': 'node_context',
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
