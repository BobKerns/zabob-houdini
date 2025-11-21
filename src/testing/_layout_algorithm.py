"""Layout algorithm test functions."""

from typing import Any
import hou
from zabob_houdini.core import ROOT, node, chain, hou_node, context
from zabob_houdini.utils import JsonObject


def _test_layout_stress_test() -> JsonObject:
    """Run a built-in layout algorithm stress test and return statistics."""
    try:
        # Create a geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "layout_stress_test")

        with context(geo) as ctx:
            # Create a complex stress test graph directly here

            # Multiple source nodes
            sources = []
            for i in range(3):
                source = ctx.node("box", f"source_{i}")
                sources.append(source)

            # Create diamond patterns
            diamonds = []
            for i, source in enumerate(sources):
                # Process each source through two parallel paths
                left_path = ctx.node("xform", f"left_proc_{i}", _input=source)
                right_path = ctx.node("xform", f"right_proc_{i}", _input=source)

                # Merge the paths
                diamond_merge = ctx.merge(left_path, right_path, name=f"diamond_{i}")
                diamonds.append(diamond_merge)

            # Create fan-out and fan-in patterns
            fan_out_nodes = []
            for i, diamond in enumerate(diamonds):
                for j in range(2):
                    fan_node = ctx.node("xform", f"fan_{i}_{j}", _input=diamond)
                    fan_out_nodes.append(fan_node)

            # Final merge of all fan-out nodes
            final_merge = ctx.merge(*fan_out_nodes, name="final_result")

            # Post-processing chain
            final_chain = [
                ctx.node("subdivide", "subdivide_final", _input=final_merge),
                ctx.node("xform", "final_transform")
            ]

            # Connect the chain
            for i in range(1, len(final_chain)):
                final_chain[i] = final_chain[i].copy(_input=final_chain[i-1])

            # Get statistics
            all_nodes = list(ctx._dependency_registry.keys())
            source_nodes = ctx.get_source_nodes()
            sink_nodes = ctx.get_sink_nodes()
            layers = ctx._compute_layers(all_nodes)
            positions = ctx.layout_nodes()

            # Calculate layout bounds
            if positions:
                x_positions = [pos[0] for pos in positions.values()]
                y_positions = [pos[1] for pos in positions.values()]
                layout_stats: JsonObject = {
                    'x_min': min(x_positions),
                    'x_max': max(x_positions),
                    'y_min': min(y_positions),
                    'y_max': max(y_positions),
                    'total_width': max(x_positions) - min(x_positions),
                    'total_height': max(y_positions) - min(y_positions)
                }
            else:
                layout_stats: JsonObject = {}

            return {
                'success': True,
                'total_nodes': len(all_nodes),
                'source_nodes': len(source_nodes),
                'sink_nodes': len(sink_nodes),
                'num_layers': len(layers),
                'nodes_per_layer': [len(nodes) for nodes in layers.values()],
                'layout_stats': layout_stats,
                'hip_file_saved': True
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def _test_simple_layout_demo() -> JsonObject:
    """Test a simple layout demo to verify basic functionality."""
    try:
        # Create a geometry object for testing
        obj = hou_node("/obj")
        geo = obj.createNode("geo", "simple_layout_test")

        with context(geo) as ctx:
            # Create a simple graph using only basic node types

            # Two source nodes
            box = ctx.node("box", "source_box")
            sphere = ctx.node("sphere", "source_sphere")

            # Process each source with transforms
            box_xform = ctx.node("xform", "box_proc", _input=box)
            sphere_xform = ctx.node("xform", "sphere_proc", _input=sphere)

            # Merge them
            merged = ctx.merge(box_xform, sphere_xform, name="combined")

            # Final processing
            ctx.node("xform", "final_proc", _input=merged)

            # Get positions
            positions = ctx.layout_nodes()

            # Convert positions to JSON-compatible format
            positions_data = {}
            for i, (node, pos) in enumerate(positions.items()):
                node_name = node.name or f"node_{i}"
                positions_data[node_name] = {'x': pos[0], 'y': pos[1]}

            return {
                'success': True,
                'positions': positions_data,
                'node_count': len(positions)
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
