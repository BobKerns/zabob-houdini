"""Crowd simulation utilities module (hou.crowds).

This module provides utility functions for working with crowd agents,
including shape deformation setup, agent definition management, and
transform computation.

Example::

    import hou
    from hou import crowds

    # Setup blendshape deformation
    base_geo = shape.geometry()
    blendshapes = [smile_geo, frown_geo, blink_geo]
    channels = ['smile', 'frown', 'blink']
    crowds.addBlendshapeInputs(base_geo, blendshapes, channels)

    # Add in-between shapes for smoother blending
    smile_inbetweens = [smile_50, smile_75]
    weights = [0.5, 0.75]
    crowds.addInBetweenShapes(smile_geo, smile_inbetweens, weights)

    # Configure deformer parameters
    crowds.setBlendshapeDeformerParms(base_geo, attribs="P N",
                                      point_id_attrib="id")

    # Find a shape deformer
    deformer = crowds.findShapeDeformer('LinearSkinning')

    # Convert world to local transforms
    local_xforms = crowds.computeLocalTransforms(rig, world_xforms)

    # Replace agent definitions in geometry
    old_to_new = {'agent1': new_definition1, 'agent2': new_definition2}
    crowds.replaceAgentDefinitions(geo, old_to_new)

See https://www.sidefx.com/docs/houdini/hom/hou/crowds.html
"""

from typing import Any, Sequence
from hou import Geometry, AgentRig, Matrix4, AgentDefinition, AgentShapeDeformer, geometryType


def addBlendshapeInputs(
    base_shape_geo: Geometry,
    shapes: Sequence[Geometry],
    channel_names: Sequence[str]
) -> None:
    """Add blendshape inputs to a shape's geometry.

    This function prepares a base shape geometry for blendshape deformation by
    adding multiple blendshape targets and associating them with animation channels.
    The base shape is deformed by blending toward the target shapes based on
    channel values.

    Args:
        base_shape_geo: Base shape geometry to add blendshapes to
        shapes: Sequence of geometry objects to use as blendshape targets
        channel_names: Names for the blendshape channels (one per shape)

    Example::

        base = shape.geometry()
        targets = [smile_geo, frown_geo, blink_geo]
        channels = ['smile', 'frown', 'blink']
        hou.crowds.addBlendshapeInputs(base, targets, channels)

    See https://www.sidefx.com/docs/houdini/hom/hou/crowds.html#addBlendshapeInputs
    """
    ...


def addInBetweenShapes(
    primary_shape_geo: Geometry,
    shapes: Sequence[Geometry],
    weights: Sequence[float]
) -> None:
    """Add in-between shapes to a blendshape input.

    In-between shapes (also called progressive shapes) provide intermediate
    targets for smoother blending. For example, a 50% in-between shape for
    a smile provides a better result at 0.5 weight than simple linear interpolation.

    Args:
        primary_shape_geo: Primary blendshape target geometry
        shapes: Sequence of in-between geometries
        weights: Weight values (0-1) for each in-between shape

    Example::

        # Add 50% and 75% in-betweens for smoother smile blend
        smile_primary = smile_100_geo
        inbetweens = [smile_50_geo, smile_75_geo]
        weights = [0.5, 0.75]
        hou.crowds.addInBetweenShapes(smile_primary, inbetweens, weights)

    See https://www.sidefx.com/docs/houdini/hom/hou/crowds.html#addInBetweenShapes
    """
    ...


def applyUsdProcedural(
    stage: 'Any',  # pxr.Usd.Stage but avoiding import
    selection_rule: str,
    camera_path: str,
    resolution: tuple[int, int],
    lod_threshold: float,
    frame: float,
    optimize_identical_poses: bool = True,
    bake_all_agents: bool = False,
    prototype_material: str = "",
    instance_material: str = "",
    default_material: str = ""
) -> None:
    """Apply a crowd procedural to a USD stage.

    This function configures crowd rendering in a USD stage by setting up
    procedural crowd expansion with LOD control, material assignment, and
    optimization settings.

    Args:
        stage: USD stage to apply the procedural to
        selection_rule: Rule for selecting agents to process
        camera_path: USD path to the camera for LOD calculations
        resolution: Viewport resolution (width, height) for LOD
        lod_threshold: Screen-space threshold for LOD switching
        frame: Frame time to evaluate
        optimize_identical_poses: Optimize agents with identical poses
        bake_all_agents: Bake all agents instead of using instancing
        prototype_material: Material path for agent prototypes
        instance_material: Material path for agent instances
        default_material: Default material path for agents

    Example::

        import hou
        from pxr import Usd

        stage = Usd.Stage.Open('crowd.usd')
        hou.crowds.applyUsdProcedural(
            stage=stage,
            selection_rule='*',
            camera_path='/cameras/main',
            resolution=(1920, 1080),
            lod_threshold=0.05,
            frame=1.0,
            optimize_identical_poses=True
        )

    See https://www.sidefx.com/docs/houdini/hom/hou/crowds.html#applyUsdProcedural
    """
    ...


def computeLocalTransforms(
    rig: AgentRig,
    xforms: Sequence[Matrix4]
) -> tuple[Matrix4, ...]:
    """Convert world-space transforms to local-space transforms.

    Given a sequence of world-space transform matrices, compute the equivalent
    local-space transforms based on the rig's hierarchy. This is useful for
    converting absolute transforms back to rig-relative transforms.

    Args:
        rig: AgentRig defining the transform hierarchy
        xforms: Sequence of world-space 4x4 transform matrices

    Returns:
        Tuple of local-space 4x4 transform matrices

    Example::

        world_xforms = agent.worldTransforms()
        rig = agent.rig()
        local_xforms = hou.crowds.computeLocalTransforms(rig, world_xforms)

        # Now local_xforms can be used with setLocalTransforms()
        for i, xform in enumerate(local_xforms):
            agent.setLocalTransform(i, xform)

    See https://www.sidefx.com/docs/houdini/hom/hou/crowds.html#computeLocalTransforms
    """
    ...


def findShapeDeformer(name: str) -> AgentShapeDeformer | None:
    """Find a shape deformer by name.

    Shape deformers define how agent shapes are deformed based on the rig
    transforms. This function looks up a deformer by its name.

    Args:
        name: Name of the shape deformer to find

    Returns:
        AgentShapeDeformer if found, None otherwise

    Example::

        deformer = hou.crowds.findShapeDeformer('LinearSkinning')
        if deformer:
            # Use deformer...
            pass

    See https://www.sidefx.com/docs/houdini/hom/hou/crowds.html#findShapeDeformer
    See hou.agentShapeDeformerType for available deformer types
    """
    ...


def replaceAgentDefinitions(
    geometry: Geometry,
    new_definition_map: dict[str, AgentDefinition],
    group: str = "",
    group_type: 'geometryType | None' = None
) -> None:
    """Replace agent definitions in geometry.

    This function updates agent primitives in geometry to use new definitions.
    You can optionally limit the replacement to agents in a specific group.

    Args:
        geometry: Geometry containing agent primitives
        new_definition_map: Dict mapping old definition names to new AgentDefinition objects
        group: Optional group name to limit replacement (empty = all agents)
        group_type: Type of group (defaults to primitives)

    Example::

        # Create new definition
        new_rig = hou.AgentRig('/path/to/new_rig.json')
        new_shapes = hou.AgentShapeLibrary('/path/to/new_shapes.bgeo')
        new_def = hou.AgentDefinition(new_rig, new_shapelib)

        # Replace old definition with new one
        replacement_map = {'old_agent': new_def}
        hou.crowds.replaceAgentDefinitions(geo, replacement_map)

        # Or just update agents in a specific group
        hou.crowds.replaceAgentDefinitions(
            geo,
            replacement_map,
            group='hero_agents',
            group_type=hou.geometryType.Primitives
        )

    See https://www.sidefx.com/docs/houdini/hom/hou/crowds.html#replaceAgentDefinitions
    """
    ...


def setBlendshapeDeformerParms(
    base_shape_geo: Geometry,
    attribs: str = "P N",
    point_id_attrib: str = "id",
    prim_id_attrib: str = "id"
) -> None:
    """Set parameters for the blendshape deformer.

    This function configures which attributes should be deformed by blendshapes
    and how points/primitives are matched between the base shape and targets.

    Args:
        base_shape_geo: Base shape geometry to configure
        attribs: Space-separated list of attributes to deform (e.g., "P N Cd")
        point_id_attrib: Point attribute name for ID-based matching
        prim_id_attrib: Primitive attribute name for ID-based matching

    Example::

        # Deform position, normals, and color
        hou.crowds.setBlendshapeDeformerParms(
            base_geo,
            attribs="P N Cd",
            point_id_attrib="id",
            prim_id_attrib="id"
        )

        # Only deform position
        hou.crowds.setBlendshapeDeformerParms(base_geo, attribs="P")

    See https://www.sidefx.com/docs/houdini/hom/hou/crowds.html#setBlendshapeDeformerParms
    """
    ...
