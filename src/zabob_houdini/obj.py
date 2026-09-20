'''
Specialized types for Obj nodes.
'''

from __future__ import annotations, _dynamic_import  # noqa: F407 E261 # type: ignore

from typing import TypeVar  # noqa: F407 E261 # type: ignore

import hou


from zabob_houdini.op import ZOpContext, ZOpNode


T_ObjNode = TypeVar('T_ObjNode', bound=hou.ObjNode)
T_ObjCtx = TypeVar('T_ObjCtx', bound=hou.ObjNode)
T_ObjParent = TypeVar('T_ObjParent', bound=hou.ObjNode)
T_ObjChild = TypeVar('T_ObjChild', bound=hou.ObjNode)
T_ObjInstance = TypeVar('T_ObjInstance', bound='ZObjNode')


class ZObjNode(ZOpNode[T_ObjParent, T_ObjNode, T_ObjChild]):
    """
    Concrete instance of an Object (OBJ) node.

    OBJ nodes represent objects in Houdini's scene hierarchy. They handle
    transforms, contain geometry networks (geo), cameras, lights, etc.

    OBJ nodes have a dual role:
    1. Container role: 'geo' ObjNodes contain SopNodes (geometry operators)
    2. Object role: Other ObjNodes (cam, light, etc.) are scene objects

    Type Parameters:
        T_ObjParent: Parent type (hou.ObjNode for /obj level)
        T_ObjNode: This node's type (hou.ObjNode)
        T_ObjChild: What this can contain (hou.SopNode for geo, hou.ObjNode for others)

    Examples:
        # Geometry container
        geo: ZObjNode[hou.ObjNode, hou.ObjNode, hou.SopNode]
        # Can create SOP children inside

        # Camera object
        cam: ZObjNode[hou.ObjNode, hou.ObjNode, hou.ObjNode]
        # Is an object, not a container for other node types

    See docs/NODE_TYPE_HIERARCHIES.md for more on ObjNode's dual role.
    """
    pass


class ZObjContext(ZOpContext[T_ObjParent, T_ObjCtx, T_ObjNode]):
    """
    Context manager for creating Object-level nodes.

    Use this at the /obj level to create objects (geo, cam, light, etc.)
    with automatic layout and dependency tracking.

    Type Parameters:
        T_ObjParent: Parent type (typically hou.ObjNode for /obj)
        T_ObjCtx: Context node type (hou.ObjNode)
        T_ObjNode: Types created (hou.ObjNode)

    Example:
        obj = zwrap_node(hou.znode('/obj'))
        with ZObjContext(obj) as ctx:
            geo = ctx.znode('geo', 'geo1')
            cam = ctx.znode('cam', 'cam1')
    """
    pass


class ZObjChain(ZOpNode[T_ObjParent, T_ObjNode, T_ObjChild]):
    """
    ZChain of Object-level nodes.

    Note: OBJ chains are less common than SOP chains since object-level
    networks typically represent scene hierarchy rather than data flow.

    Type Parameters:
        T_ObjParent: Parent type (hou.ObjNode)
        T_ObjNode: Node type (hou.ObjNode)
        T_ObjChild: Children type (hou.ObjNode or hou.SopNode)

    This may be refined or reconsidered as the OBJ specialization develops.
    """
    pass
