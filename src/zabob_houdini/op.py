'''
Specializations for OpNodes
'''

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from typing import Any, TypeVar  # noqa: F407 E261 # type: ignore


import hou

from zabob_houdini.core import (
    NodeContext, NodeInstance, Chain,
)
from zabob_houdini.core_node import NodeBase

T_OpNode = TypeVar('T_OpNode', bound=hou.OpNode)
T_OpCtx = TypeVar('T_OpCtx', bound=hou.OpNode)
T_OpParent = TypeVar('T_OpParent', bound=hou.OpNode)
T_OpChild = TypeVar('T_OpChild', bound='hou.OpNode')
T_OpInstance = TypeVar('T_OpInstance', bound='OpInstance')


class OpBase(NodeBase[hou.OpNodeTypeCategory, T_OpParent, T_OpNode, T_OpChild]):
    """
    Base class for operator (Op) nodes.

    Fixes the category to OpNodeTypeCategory while leaving parent, node, and child
    types as generic parameters. This is the foundation for all operator nodes
    (SOP, OBJ, CHOP, ROP, DOP, etc.).

    Type Parameters:
        T_OpParent: Type of the parent node containing this OpNode
        T_OpNode: The specific OpNode subtype (hou.SopNode, hou.ObjNode, etc.)
        T_OpChild: What types of children this node can contain

    See docs/NODE_TYPE_HIERARCHIES.md for detailed explanation of the type system.
    """
    pass


class OpInstance(NodeInstance[hou.OpNodeTypeCategory, T_OpParent, T_OpNode, T_OpChild],
                 NodeBase[hou.OpNodeTypeCategory, T_OpParent, T_OpNode, T_OpChild]):
    """
    Concrete instance of an operator node.

    Represents a specific operator node with full type information about its
    parent, its own type, and what children it can contain.

    Type Parameters:
        T_OpParent: Type of parent (e.g., hou.ObjNode for SOPs inside geo)
        T_OpNode: This node's type (e.g., hou.SopNode, hou.ObjNode)
        T_OpChild: Child types this can contain (e.g., hou.SopNode for geo containers)

    Example:
        OpInstance[hou.ObjNode, hou.SopNode, hou.OpNode]
        - Parent is ObjNode (geo container)
        - This is a SopNode (geometry operator)
        - Children are generic OpNodes (SOPs are typically leaf nodes)
    """
    pass


class OpContext(NodeContext[hou.OpNodeTypeCategory, T_OpParent, T_OpCtx, T_OpNode]):
    """
    Context manager for creating operator nodes.

    Provides a context for creating multiple operator nodes with automatic
    layout and dependency tracking.

    Type Parameters:
        T_OpParent: Type of the parent containing this context's nodes
        T_OpCtx: Type of this context's parent node
        T_OpNode: Types of nodes this context creates

    Example:
        with OpContext(geo_node) as ctx:
            # Creates SOP nodes inside the geo container
            box = ctx.node('box', 'box1')
    """
    def __init__(self, parent: OpInstance[T_OpParent, T_OpCtx, T_OpNode]):
        super().__init__(parent)

    def node(self,
             node_type: str,
             name: str,
             /,
             **parms: Any,
             ) -> OpInstance[T_OpCtx, T_OpNode, hou.OpNode]:
        """Create or get an Op node within this context."""
        node = super().node(node_type, name, **parms)
        return node.as_type(OpInstance[T_OpCtx, T_OpNode, hou.OpNode])

    def context(self) -> OpContext[T_OpCtx, T_OpNode, hou.OpNode]:
        """Create a nested OpContext within this context."""
        return OpContext(self.parent.as_type(OpInstance[T_OpCtx, T_OpNode, hou.OpNode]))


class OpChain(Chain[NodeBase[hou.OpNodeTypeCategory,
                             T_OpParent,
                             T_OpNode,
                             T_OpChild]]):
    def __init__(self, nodes: tuple[OpBase[T_OpParent,
                                           T_OpNode,
                                           T_OpChild], ...], *,
                 context: OpContext[hou.OpNode, T_OpParent, T_OpNode],
                 subset: bool = False,):
        super().__init__(nodes, context=context, subset=subset)
