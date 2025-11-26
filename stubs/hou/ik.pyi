"""Inverse kinematics module (hou.ik)."""

from __future__ import annotations
import hou


class Joint:
    """Represents a joint in an inverse kinematics skeleton.

    Joints can be created using hou.ik.Skeleton.addJoint().
    """

    def worldTransform(self) -> hou.Matrix4:
        """Returns the joint's world space transform."""
        ...

    def setWorldTransform(self, xform: hou.Matrix4) -> None:
        """Sets the joint's world space transform (a hou.Matrix4)."""
        ...

    def parent(self) -> Joint | None:
        """Returns the joint's parent, or None for a root joint."""
        ...

    def setParent(self, joint: Joint) -> None:
        """Sets the parent joint of this joint."""
        ...

    def rotationOrder(self) -> str:
        """Returns the joint's rotation order."""
        ...

    def setRotationOrder(self, rotate_order: str) -> None:
        """Sets the joint's rotation order."""
        ...

    def rotationWeights(self) -> hou.Vector3:
        """Returns the weights for the joint's rotation axes."""
        ...

    def setRotationWeights(self, weights: hou.Vector3) -> None:
        """Sets a hou.Vector3 specifying the weight of each rotation axis."""
        ...

    def translationWeights(self) -> hou.Vector3:
        """Returns the weights for the joint's translation axes."""
        ...

    def setTranslationWeights(self, weights: hou.Vector3) -> None:
        """Sets a hou.Vector3 specifying the weight of each translation axis."""
        ...

    def hasRotationLimits(self) -> bool:
        """Returns whether the joint has rotation limits."""
        ...

    def rotationLimits(self) -> tuple[hou.Vector3, hou.Vector3]:
        """Returns the lower and upper rotation limits (in radians) for the joint,
        relative to the rest transform.
        """
        ...

    def setRotationLimits(self, lower: hou.Vector3, upper: hou.Vector3) -> None:
        """Sets the lower and upper rotation limits (a hou.Vector3 in radians) for the joint."""
        ...

    def translationLimits(self) -> tuple[hou.Vector3, hou.Vector3]:
        """Returns the lower and upper translation limits for the joint, relative to the rest transform."""
        ...

    def setTranslationLimits(self, lower: hou.Vector3, upper: hou.Vector3) -> None:
        """Sets the lower and upper translation limits for the joint."""
        ...

    def hasTranslationLimits(self) -> bool:
        """Returns whether the joint has translation limits."""
        ...

    def restTransform(self) -> hou.Matrix4 | None:
        """Returns the joint's rest pose, or None if it has not been set."""
        ...

    def setRestTransform(self, xform: hou.Matrix4) -> None:
        """Sets a local space hou.Matrix4 specifying the joint's rest pose."""
        ...

    def restRotationWeights(self) -> hou.Vector3:
        """Returns the rest weights for the joint's rotation axes."""
        ...

    def setRestRotationWeights(self, weights: hou.Vector3) -> None:
        """Sets a hou.Vector3 specifying how strongly the solver attempts to match
        the rest transform for the rotation axes.
        """
        ...

    def restTranslationWeights(self) -> hou.Vector3:
        """Returns the rest weights for the joint's translation axes."""
        ...

    def setRestTranslationWeights(self, weights: hou.Vector3) -> None:
        """Sets a hou.Vector3 specifying how strongly the solver attempts to match
        the rest transform for the translation axes.
        """
        ...

    def mass(self) -> float:
        """Returns the mass of the body attached to this joint."""
        ...

    def setMass(self, mass: float) -> None:
        """Sets the mass of the body attached to this joint."""
        ...

    def localCenterOfMass(self) -> hou.Vector3:
        """Returns the local space position of the body attached to this joint."""
        ...

    def setLocalCenterOfMass(self, position: hou.Vector3) -> None:
        """Sets the local space position of the body attached to this joint."""
        ...


class Skeleton:
    """Represents a skeleton for use with inverse kinematics solvers."""

    def addJoint(
        self,
        world_transform: hou.Matrix4 = ...,
        parent: Joint | None = None,
        rotation_weights: hou.Vector3 = ...,
        translation_weights: hou.Vector3 = ...,
        mass: float = 1.0,
        local_com: hou.Vector3 = ...
    ) -> Joint:
        """Appends a new joint to the skeleton."""
        ...

    def joints(self) -> tuple[Joint, ...]:
        """Returns a list of the joints in the skeleton."""
        ...

    def centerOfMass(self) -> hou.Vector3:
        """Returns the world space position of the skeleton's center of mass."""
        ...


class Target:
    """Represents a position or orientation target for inverse kinematics solvers."""

    def __init__(
        self,
        joint: Joint | None = None,
        goal_transform: hou.Matrix4 = ...,
        joint_offset: hou.Matrix4 = ...,
        target_type: targetType = ...,
        weight: float = 1.0,
        priority: int = 0,
        depth: int = -1
    ) -> None:
        """Creates a new target."""
        ...

    def joint(self) -> Joint | None:
        """Returns the joint that the target is attached to, or None."""
        ...

    def setJoint(self, joint: Joint) -> None:
        """Sets the hou.ik.Joint that the target is attached to."""
        ...

    def goalTransform(self) -> hou.Matrix4:
        """Returns the world space goal transform."""
        ...

    def setGoalTransform(self, xform: hou.Matrix4) -> None:
        """Sets the target world space transform (a hou.Matrix4) for the joint."""
        ...

    def jointOffset(self) -> hou.Matrix4:
        """Returns the local space joint offset transform."""
        ...

    def setJointOffset(self, xform: hou.Matrix4) -> None:
        """Sets a local space transform (a hou.Matrix4) that is combined with the joint
        transform to produce the transform that the solver attempts to align with the goal transform.
        """
        ...

    def targetType(self) -> targetType:
        """Returns the target's type."""
        ...

    def setTargetType(self, target_type: targetType) -> None:
        """Sets a hou.ik.targetType, which specifies whether the target affects position, orientation, or both."""
        ...

    def weight(self) -> float:
        """Returns the target's weight."""
        ...

    def setWeight(self, weight: float) -> None:
        """Sets a float specifying the importance of the target."""
        ...

    def priority(self) -> int:
        """Returns the target's priority level."""
        ...

    def setPriority(self, priority: int) -> None:
        """Sets an int specifying the target's priority level."""
        ...

    def depth(self) -> int:
        """Returns the target's depth."""
        ...

    def setDepth(self, depth: int) -> None:
        """Specifies the number of parent joints that can be adjusted to achieve the goal transform."""
        ...


class targetType:
    """Enumeration of IK target types.

    Specifies whether a hou.ik.Target affects position, orientation, or both.
    """
    Position: int
    Orientation: int
    All: int


def solveFBIK(
    skeleton: Skeleton,
    targets: list[Target],
    iters: int = 30,
    tolerance: float = 1e-5,
    pin_root: bool = False
) -> None:
    """Applies a full-body inverse kinematics algorithm to a skeleton.

    This solver is equivalent to the solvefbik VEX function.

    Args:
        skeleton: The hou.ik.Skeleton to solve. The joints' transforms will be updated with the solution.
        targets: A list of hou.ik.Target specifying the goal transforms for particular joints.
            Raises hou.ValueError if any of the targets are not attached to a joint,
            or if multiple targets are attached to the same joint.
        iters: The maximum number of iterations to perform. The solver may terminate early
            if the tolerance parameter is used.
        tolerance: The tolerance to use when checking for convergence, defaults to 1e-5.
            If positions converge to within this tolerance, the algorithm will stop.
            If 0, the solver will always perform exactly iters iterations.
        pin_root: Specifies whether the root joint is allowed to translate.
    """
    ...


def solvePhysFBIK(
    skeleton: Skeleton,
    targets: list[Target],
    com_target: Target | None = None,
    iters: int = 30,
    damping: float = 0.5,
    tolerance: float = 1e-5
) -> None:
    """Applies a full-body inverse kinematics algorithm to a skeleton, with optional
    control over the center of mass.

    This solver is equivalent to the solvephysfbik VEX function.

    Args:
        skeleton: The hou.ik.Skeleton to solve. The joints' transforms will be updated with the solution.
        targets: A list of hou.ik.Target specifying the goal transforms for particular joints.
            Raises hou.ValueError if any of the targets are not attached to a joint,
            or if multiple targets are attached to the same joint.
        com_target: An optional hou.ik.Target which specifies the goal position of the skeleton's center of mass.
        iters: The maximum number of iterations to perform. The solver may terminate early
            if the tolerance parameter is used.
        damping: Damping factor for the solver. Larger values will produce more stable results
            when, for example, a target is unreachable. A value that is too large, however,
            will require more iterations to converge. Around 0.5 is typically a suitable initial value.
        tolerance: The tolerance to use when checking for convergence, defaults to 1e-5.
            If positions converge to within this tolerance, the algorithm will stop.
            If 0, the solver will always perform exactly iters iterations.
    """
    ...
