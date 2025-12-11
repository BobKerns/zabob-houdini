#!/usr/bin/env python3
"""
PDG (TOP) Network Demo - Creating task dependency graphs.

This demonstrates creating a TOP network with various TOP nodes
for procedural dependency graph workflows.
"""

from zabob_houdini import zcontext


def create_simple_pdg_network(obj_ctx):
    """Create a simple PDG network with basic task dependencies."""

    # Create a TOP network at the /obj level
    with zcontext(obj_ctx.znode("topnet", name="pdg_demo")) as ctx:
        # Create a simple linear task chain
        with ctx.chain() as task_chain:
            task_chain.node("genericgenerator", "generate_tasks", itemcount=10)
            task_chain.node("pythonscript", "process_tasks",
                            script="print('Processing work item', work_item.index)")
            task_chain.node("waitforall", "collect_results")
        # Context exits here, triggering automatic layout and creation


def create_parallel_pdg_workflow(obj_ctx):
    """Create a PDG workflow with parallel processing branches."""

    with zcontext(obj_ctx.znode("topnet", name="parallel_pdg")) as ctx:
        # Generate initial tasks
        generator = ctx.znode("genericgenerator", "generate_items", itemcount=5)

        # Branch A: Fast processing
        with ctx.chain(_input=generator) as fast_branch:
            fast_branch.node("pythonscript", "fast_process",
                             script="import time; time.sleep(0.1); print('Fast:', work_item.index)")
            fast_branch.node("pythonscript", "fast_filter",
                             script="print('Fast filtered:', work_item.index)")

        # Branch B: Slow processing
        with ctx.chain(_input=generator) as slow_branch:
            slow_branch.node("pythonscript", "slow_process",
                             script="import time; time.sleep(0.5); print('Slow:', work_item.index)")
            slow_branch.node("pythonscript", "slow_filter",
                             script="print('Slow filtered:', work_item.index)")

        # Merge results
        with ctx.chain(_input=[fast_branch, slow_branch]) as merge_chain:
            merge_chain.node("waitforall", "wait_all")
            merge_chain.node("pythonscript", "final_output",
                             script="print('All complete:', work_item.index)")
        # Context exits here, triggering automatic layout and creation


def create_wedge_workflow(obj_ctx):
    """Create a PDG wedge workflow for parameter variation."""

    with zcontext(obj_ctx.node("topnet", name="wedge_demo")) as ctx:
        # Create wedge workflow
        with ctx.chain() as wedge_chain:
            wedge_chain.node("labs::wedge::1.0", "param_variation", wedgecount=5)
            wedge_chain.node("pythonscript", "process_wedge",
                             script="print(f'Wedge {work_item.index}: param={work_item.attrib(\"wedge\")}')")
            wedge_chain.node("waitforall", "collect_wedges")
            wedge_chain.node("pythonscript", "summarize",
                             script="print('All wedges complete')")

        # Context exits here, triggering automatic layout and creation


def create_filter_workflow(obj_ctx):
    """Create a PDG workflow demonstrating filtering and partitioning."""

    with zcontext(obj_ctx.node("topnet", name="filter_demo")) as ctx:
        # Filter and partition workflow
        with ctx.chain() as filter_chain:
            filter_chain.node("genericgenerator", "generate", itemcount=20)
            filter_chain.node("filterbyrange", "filter_range",
                              filterby=0, rangex=0, rangey=10)
            filter_chain.node("pythonscript", "process_filtered",
                              script="print('Filtered item:', work_item.index)")
            filter_chain.node("waitforall", "collect")
        # Context exits here, triggering automatic layout and creation


if __name__ == "__main__":
    print("=== PDG (TOP) Network Demos ===\n")

    # Create all TOP networks within a single /obj context for proper layout
    with zcontext("/obj") as obj_ctx:
        print("1. Simple PDG Network:")
        print("   Creating linear task dependency chain...")
        create_simple_pdg_network(obj_ctx)
        print("   ✓ Simple PDG network created with automatic layout\n")

        print("2. Parallel PDG Workflow:")
        print("   Creating parallel processing branches...")
        create_parallel_pdg_workflow(obj_ctx)
        print("   ✓ Parallel PDG workflow created with automatic layout\n")

        print("3. Wedge Workflow:")
        print("   Creating parameter variation workflow...")
        create_wedge_workflow(obj_ctx)
        print("   ✓ Wedge workflow created with automatic layout\n")

        print("4. Filter Workflow:")
        print("   Creating filter and partition workflow...")
        create_filter_workflow(obj_ctx)
        print("   ✓ Filter workflow created with automatic layout\n")

    print("""Summary:
  All PDG networks created successfully!
  Nodes are automatically laid out and created when context exits.
  Run with zabob-houdini run pdg_demo.py --open
  to open the generated hip file in Houdini.
""")
