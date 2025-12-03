"""Core caching test functions."""


from zabob_houdini.utils import HoudiniResult, JsonObject, error_result, success_result
from zabob_houdini.core_node import (
    NO_CONNECTION, NodeInstance,
    get_node_instance, wrap_node,
)
from zabob_houdini.solo_fns import (
    chain, node
)
from zabob_houdini.core_utils import hou_node


def h_test_create_caches_result() -> JsonObject:
    """Test NodeInstance.create() caching behavior."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create NodeInstance and test caching
    box_node = node(geo.path(), "box", name="cache_test_box")

    # First call should create the node
    created_node1 = box_node.create()

    # Second call should return cached node
    created_node2 = box_node.create()

    # Verify they're the same object (cached)
    same_object = created_node1 is created_node2

    return {
        'same_object': same_object,
        'node_path': created_node1.path(),
    }


def h_test_create_different_instances_different_nodes() -> JsonObject:
    """Test different NodeInstance objects create different nodes."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create two different NodeInstance objects
    node1 = node(geo.path(), "box", name="box1")
    node2 = node(geo.path(), "box", name="box2")

    created1 = node1.create()
    created2 = node2.create()

    different_objects = created1 is not created2
    different_paths = created1.path() != created2.path()

    return {
        'different_objects': different_objects,
        'different_paths': different_paths,
        'path1': created1.path(),
        'path2': created2.path(),
    }


def h_test_create_returns_tuple_of_node_instances() -> JsonObject:
    """Test Chain.create() returns tuple of NodeInstance copies."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create a chain
    node1 = node(geo.path(), "box", name="chain_box")
    node2 = node(geo.path(), "sphere", name="chain_sphere")
    test_chain = chain(node1, node2)

    hou_nodes = test_chain.create()
    nodes = test_chain.nodes

    # Check return type and length
    is_tuple = isinstance(hou_nodes, tuple)
    tuple_length = len(nodes)

    # Check that items are NodeInstance objects
    all_node_instances = all(isinstance(item, NodeInstance) for item in nodes)

    all_created = all(node is not None for node in hou_nodes)

    return {
        'is_tuple': is_tuple,
        'tuple_length': tuple_length,
        'all_node_instances': all_node_instances,
        'all_created': all_created,
        'node_paths': [node.path() for node in hou_nodes],
    }


def h_test_copy_creates_independent_instance() -> JsonObject:
    """Test NodeInstance.copy() creates independent copies."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create original NodeInstance
    original = node(geo.path(), "box", name="original", sizex=2.0)
    copied = original.copy()

    # Test that they're different objects
    different_objects = copied is not original

    # Test that they have same basic properties
    same_parent = copied.parent == original.parent
    same_node_type = copied.node_type == original.node_type
    same_name = copied.name == original.name

    # Test that attributes are copied (not shared)
    attributes_equal = copied.attributes == original.attributes
    attributes_shared = copied.attributes is original.attributes

    return {
        'different_objects': different_objects,
        'same_parent': same_parent,
        'same_node_type': same_node_type,
        'same_name': same_name,
        'attributes_equal': attributes_equal,
        'attributes_shared': attributes_shared,
    }


def h_test_copy_with_chain_inputs() -> JsonObject:
    """Test NodeInstance.copy() with various input types."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create a chain to use as input
    inner_node = node(geo, "sphere")
    inner_chain = chain(inner_node)

    # Create node with chain input
    original = node(geo, "merge", _input=inner_chain)
    copied = original.copy()

    # Test input structure
    has_inputs = copied.inputs != ()
    input_length = len(copied.inputs)

    # The input chain should be copied (different object)
    input_copied = False
    if copied.inputs and len(copied.inputs) > 0:
        # Check if it's a different Chain object - inputs now returns (node, output_index) tuples or None
        input_copied = copied.inputs[0] != NO_CONNECTION and copied.inputs[0][0] != inner_chain

    return {
        'has_inputs': has_inputs,
        'input_length': input_length,
        'input_copied': input_copied,
    }


def h_test_copy_creates_independent_chain() -> JsonObject:
    """Test Chain.copy() creates independent copy."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create original chain
    node1 = node(geo, "box")
    node2 = node(geo, "sphere")
    original = chain(node1, node2)

    # Copy the chain
    copied = original.copy()

    # Test basic properties
    different_objects = copied is not original
    same_parent = copied.parent == original.parent
    nodes_not_equal = all(a != b for (a, b) in zip(original.nodes, copied.nodes))
    nodes_not_shared = copied.nodes is not original.nodes

    return {
        'different_objects': different_objects,
        'same_parent': same_parent,
        "nodes_length": len(original.nodes) == len(copied.nodes),
        'nodes_not_shared': nodes_not_shared,
        'nodes_not_equal': nodes_not_equal,
    }


def h_test_copy_deep_copies_node_instances() -> JsonObject:
    """Test Chain.copy() deep copies NodeInstances."""
    from zabob_houdini.core import NodeInstance

    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create original chain with attributed nodes
    node1 = node(geo, "box", sizex=1.0)
    node2 = node(geo, "sphere")
    original = chain(node1, node2)

    # Copy the chain
    copied = original.copy()

    # Test that nodes are copied
    nodes_length = len(copied.nodes)
    nodes_different = all(copied.nodes[i] is not original.nodes[i] for i in range(len(copied.nodes)))

    # Test basic structure - just verify we have NodeInstance objects
    first_is_node_instance = isinstance(copied.nodes[0], NodeInstance)
    second_is_node_instance = isinstance(copied.nodes[1], NodeInstance)

    return {
        'nodes_length': nodes_length,
        'nodes_different': nodes_different,
        'first_is_node_instance': first_is_node_instance,
        'second_is_node_instance': second_is_node_instance,
    }


def h_test_copy_deep_copies_nested_chains() -> JsonObject:
    """Test Chain.copy() recursively copies nested chains."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create nested structure
    inner_node = node(geo.path(), "box")
    inner_chain = chain(inner_node)

    outer_node = node(geo, "merge")
    original = chain(inner_chain, outer_node)

    # Copy the chain
    copied = original.copy()

    # Test structure
    nodes_length = len(copied.nodes)
    inner_chain_copied = copied.nodes[0] is not inner_chain

    # Test that first node is a Chain-like object
    first_is_chain = hasattr(copied.nodes[0], 'nodes')
    second_is_node_instance = hasattr(copied.nodes[1], 'node_type')

    return {
        'nodes_length': nodes_length,
        'inner_chain_copied': inner_chain_copied,
        'first_is_chain': first_is_chain,
        'second_is_node_instance': second_is_node_instance,
    }


def h_test_copy_preserves_non_chain_inputs() -> JsonObject:
    """Test NodeInstance.copy() preserves non-Chain inputs as-is."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create a NodeInstance to use as input
    input_node = node(geo.path(), "box", name="input_box")

    # Create node with multiple inputs including None for sparse connections
    original = node(geo.path(), "merge", _input=[input_node, None])
    copied = original.copy()

    has_inputs = copied.inputs is not None
    input_length = len(copied.inputs) if copied.inputs else 0
    # inputs now returns (node, output_index) tuples for actual nodes, None for None inputs
    first_input_same = (
        (copied.inputs[0][0] is input_node and copied.inputs[0][1] == 0)
        if copied.inputs and len(copied.inputs) > 0 and copied.inputs[0] is not None
        else False
    )
    second_input_none = copied.inputs[1] == NO_CONNECTION if copied.inputs and len(copied.inputs) > 1 else False

    return {
        'has_inputs': has_inputs,
        'input_length': input_length,
        'first_input_same': first_input_same,
        'second_input_none': second_input_none,
    }


def h_test_convenience_methods_with_created_nodes() -> JsonObject:
    """Test Chain convenience methods for accessing created hou.Node instances."""
    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create a 3-node chain
    node1 = node(geo.path(), "box", name="first_box")
    node2 = node(geo.path(), "sphere", name="middle_sphere")
    node3 = node(geo.path(), "merge", name="last_merge")
    test_chain = chain(node1, node2, node3)

    # Test convenience methods
    first = test_chain.first_node()
    last = test_chain.last_node()
    all_nodes = test_chain.hou_nodes
    nodes_list = list(test_chain.nodes_iter())

    first_last_different = first is not last
    all_nodes_length = len(all_nodes)
    nodes_iter_length = len(nodes_list)

    return {
        'first_path': first.path(),
        'last_path': last.path(),
        'first_last_different': first_last_different,
        'all_nodes_length': all_nodes_length,
        'nodes_iter_length': nodes_iter_length,
        'all_nodes_paths': [node.path() for node in all_nodes],
    }


def h_test_convenience_methods_empty_chain() -> HoudiniResult:
    """Test methods on an empty Chain."""
    try:
        # Fail to create empty chain
        chain()  # type: ignore
        return error_result("Chain() with no nodes did not raise an error")
    except Exception as e:
        return success_result(error_creating_chain=str(e),
                              _func=h_test_convenience_methods_empty_chain,
                              )


def h_test_node_registry_functionality() -> JsonObject:
    """Test NodeInstance registry functionality."""

    # Create geometry object for testing
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")

    # Create a NodeInstance and get its hou.Node
    box_node = node(geo, "box", name="registry_test_box")
    created_hou_node = box_node.create()

    # Test 1: get_node_instance should return the original NodeInstance
    retrieved_instance = get_node_instance(created_hou_node)
    found_original = retrieved_instance is box_node

    # Test 2: wrap_node should return the original NodeInstance, not create a new one
    wrapped_instance = wrap_node(created_hou_node)
    wrap_returns_original = wrapped_instance is box_node

    # Test 3: Create another node with the hou.Node in a chain - should use original
    sphere_node = node(geo, "sphere", name="registry_test_sphere")
    # Create a chain that includes the raw hou.Node
    test_chain = chain(box_node, sphere_node)
    created_chain_nodes = test_chain.create()

    # The first node in the chain should not be the original NodeInstance
    # Chain creates new NodeInstances owned by the chain.
    first_chain_node_is_original = created_chain_nodes[0] == created_hou_node

    return {
        'found_original': found_original,
        'wrap_returns_original': wrap_returns_original,
        'first_chain_node_is_original': first_chain_node_is_original,
        'original_node_path': created_hou_node.path(),
    }


def h_test_merge_inputs_sparse_handling() -> JsonObject:
    """Test _merge_inputs function with sparse (None) inputs."""
    from zabob_houdini.core_node import _merge_inputs
    from zabob_houdini.core_types import UnresolvedConnections

    # Create test nodes to use as inputs
    _obj = hou_node("/obj")
    geo = _obj.createNode("geo", "test_geo")
    node1 = node(geo.path(), "box", name="box1")
    node2 = node(geo.path(), "sphere", name="sphere1")
    c1 = (node1, 0)
    c2 = (node2, 0)
    in1: UnresolvedConnections = (c1, )
    in2: UnresolvedConnections = (c2, )

    # Test case 1: Both inputs are None - result should be None
    result1 = _merge_inputs((NO_CONNECTION,), (NO_CONNECTION,))
    both_none_result = result1[0] if result1 == NO_CONNECTION else None

    # Test case 2: First is None, second is not None - result should be second
    result2 = _merge_inputs((NO_CONNECTION,), in2)
    first_none_result = result2[0]
    first_none_is_node2 = first_none_result == c2

    # Test case 3: First is not None, second is None - result should be first
    result3 = _merge_inputs(in1, (NO_CONNECTION,))
    second_none_result = result3[0]
    second_none_is_node1 = second_none_result == c1

    # Test case 4: Both are not None - result should be first (preferring in1)
    result4 = _merge_inputs(in1, in2)
    both_not_none_result = result4[0]
    both_not_none_is_node1 = both_not_none_result == c1

    # Test case 5: Multiple positions with mixed None/not-None
    result5 = _merge_inputs((c1, (None, 0), c1), ((None, 0), c2, c2))
    multi_pos_correct = (
        len(result5) == 3 and
        result5[0] == c1 and  # First prefers in1
        result5[1] == c2 and  # None in1, so use in2
        result5[2] == c1      # Both not None, prefer in1
    )

    # Test case 6: Empty lists
    result6 = _merge_inputs((), ())
    empty_result = len(result6) == 0

    # Test case 7: One empty, one with content
    result7 = _merge_inputs((), (c1, c2))
    one_empty_result = len(result7) == 2 and result7[0] == c1 and result7[1] == c2

    return {
        'both_none_is_none': both_none_result is None,
        'first_none_gets_second': first_none_is_node2,
        'second_none_gets_first': second_none_is_node1,
        'both_not_none_gets_first': both_not_none_is_node1,
        'multi_position_correct': multi_pos_correct,
        'empty_lists_work': empty_result,
        'one_empty_works': one_empty_result
    }
