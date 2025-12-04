'''
Specialized SOP node classes and utilities.
'''

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore


from typing import TypeVar  # noqa: F407 E261 # type: ignore

import hou

from zabob_houdini.core_node import hou_node, wrap_node
from zabob_houdini.op import (
    OpBase, OpInstance, OpContext, OpChain, T_OpChild, T_OpCtx, T_OpParent
)

T_SopNode = TypeVar('T_SopNode', bound=hou.SopNode)
T_SopParent = TypeVar('T_SopParent', bound=hou.SopNode)
T_SopChild = TypeVar('T_SopChild', bound=hou.SopNode)
T_SopCtx = TypeVar('T_SopCtx', bound=hou.SopNode)
T_SopInstance = TypeVar('T_SopInstance', bound='SopInstance')


class SopBase(OpBase[T_OpCtx, T_SopNode, T_OpChild]):
    """
    Base class for Surface Operator (SOP) nodes.

    SOPs are geometry nodes in Houdini - they process and generate 3D geometry.
    This class specializes OpBase to work specifically with hou.SopNode types.

    Type Parameters:
        T_OpCtx: Type of context/parent that can contain SOPs (typically hou.ObjNode)
        T_SopNode: Specific SOP node type (hou.SopNode or subclass)
        T_OpChild: What children this SOP can contain (usually hou.OpNode for leaf nodes)

    See docs/NODE_TYPE_HIERARCHIES.md for understanding the type system.
    """
    pass


class SopInstance(OpInstance[T_OpParent, T_SopNode, T_OpChild],
                  SopBase[T_OpParent, T_SopNode, T_OpChild]):
    """
    Concrete instance of a SOP node.

    Represents a specific geometry operator with full type information.
    SOP nodes are typically contained within geometry containers (geo ObjNodes).

    Type Parameters:
        T_OpParent: Parent type (typically hou.ObjNode - the geo container)
        T_SopNode: This SOP's type (hou.SopNode or subclass)
        T_OpChild: Children this can contain (typically hou.OpNode - SOPs are usually leaf)

    Example:
        SopInstance[hou.ObjNode, hou.SopNode, hou.OpNode]
        - Lives inside an ObjNode (geo container)
        - Is a SopNode (geometry operator)
        - Can't meaningfully contain children (leaf node)

    Common patterns:
        box = node(geo, 'box', 'box1')
        # Type: SopInstance[hou.ObjNode, hou.SopNode, hou.OpNode]
    """
    pass


class SopContext(OpContext[T_OpParent, T_SopNode, T_OpChild]):
    """
    Context manager for creating SOP nodes.

    Use this context to create multiple geometry operators with automatic
    layout and dependency tracking. Typically used inside a geo container.

    Type Parameters:
        T_OpParent: Parent of the SOPs (typically hou.ObjNode)
        T_SopNode: The SOP type (hou.SopNode)
        T_OpChild: Children SOPs can have (typically hou.OpNode)

    Example:
        geo = node(obj, 'geo', 'geo1')
        with SopContext(geo) as sops:
            box = sops.node('box', 'box1')
            xform = sops.node('xform', 'xform1', _input=box)
    """
    pass


class SopChain(OpChain[T_OpParent,
                       T_SopNode,
                       T_OpChild,]):
    """
    Chain of SOP nodes connected in sequence.

    Represents a linear sequence of geometry operations where each SOP
    processes the output of the previous one.

    Type Parameters:
        T_OpParent: Parent containing the chain (typically hou.ObjNode)
        T_SopNode: SOP type (hou.SopNode)
        T_OpChild: Children type (typically hou.OpNode)

    Example:
        with geo.chain() as c:
            c.node('box')
            c.node('xform', tx=1.0)
            c.node('subdivide')
        # Creates: box -> xform -> subdivide
    """
    def __init__(self, nodes: tuple[SopBase[T_OpParent, T_SopNode, T_OpChild], ...], *,
                 context: OpContext[hou.OpNode, T_OpParent, T_SopNode],
                 subset: bool = False,):
        super().__init__(nodes, context=context, subset=subset)


def example_usage():
    """
    Example showing how to use SOP-specialized types.

    This demonstrates:
    1. Starting with a geo container (ObjNode that contains SopNodes)
    2. Creating SOP nodes inside using proper typing
    3. How the type parameters flow through the hierarchy

    NOTE: This is a documentation example showing type signatures,
    not meant to be executed as-is (missing proper type narrowing).
    """
    # Get the /obj/geo node - it's an ObjNode that can contain SOPs
    # In practice, you'd need to narrow the type properly
    # Type: OpInstance[?, hou.ObjNode, hou.SopNode]
    #                     ^parent    ^this node  ^children (SOPs)
    geo_container = wrap_node(hou_node('/obj/geo')).as_type(
        OpInstance[hou.OpNode, hou.ObjNode, hou.SopNode]
    )

    # Create a context for working inside the geo container
    with OpContext(geo_container) as geo_ctx:
        # Create SOP nodes inside the geo container
        # These are SopInstances with proper typing
        file1 = geo_ctx.node('file', 'file1', file='/path/to/file.bgeo')
        # Type: SopInstance[hou.ObjNode, hou.SopNode, hou.OpNode]

        box = geo_ctx.node('box', 'box1')
        # Type: SopInstance[hou.ObjNode, hou.SopNode, hou.OpNode]

        # Can also create nested contexts if needed
        with geo_ctx.context() as sop_ctx:
            xform = sop_ctx.node('xform', 'xform1',
                                 _input=box,
                                 tx=1.0, ty=2.0, tz=3.0)
            # Type: SopInstance[hou.ObjNode, hou.SopNode, hou.OpNode]

            merge_node = sop_ctx.node('merge', 'merge1',
                                      _input=[file1, xform])
            # Type: SopInstance[hou.ObjNode, hou.SopNode, hou.OpNode]

    # Type safety: The type checker knows these are SopNodes
    # so .geometry() method will be available:
    # geometry = box.create(as_type=hou.SopNode).geometry()

    return merge_node  # Return the final node in the chain
