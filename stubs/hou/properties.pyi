"""Module for accessing standard render properties.

This module provides programmatic access to the standard properties that appear under
the Render Properties tab. It allows querying render property classes, categories, and
parameters, and enables adding render properties to nodes or digital assets.

See https://www.sidefx.com/docs/houdini/hom/hou/properties.html
"""

from collections.abc import Sequence
from . import ParmTemplate


def classes(tags: Sequence[str] | None = None) -> tuple[str, ...]:
    """Return a list of render property classes.

    Args:
        tags: Optional sequence of tags to filter by. Only classes matching
            the tags will be returned. If None, all classes are returned.

    Returns:
        Tuple of render property class names

    See https://www.sidefx.com/docs/houdini/hom/hou/properties.html#classes
    """
    ...


def classLabel(class_name: str) -> str:
    """Return a descriptive label for the provided render property class.

    Args:
        class_name: The name of the render property class

    Returns:
        The descriptive label for the class

    See https://www.sidefx.com/docs/houdini/hom/hou/properties.html#classLabel
    """
    ...


def categories(class_name: str) -> tuple[str, ...]:
    """Return the property categories in the provided render property class.

    Args:
        class_name: The name of the render property class

    Returns:
        Tuple of category names within the class

    See https://www.sidefx.com/docs/houdini/hom/hou/properties.html#categories
    """
    ...


def parameters(class_name: str, category_name: str) -> tuple[str, ...]:
    """Return the names of all parameters under the specified category within the class.

    Args:
        class_name: The name of the render property class
        category_name: The name of the category within the class

    Returns:
        Tuple of parameter names

    See https://www.sidefx.com/docs/houdini/hom/hou/properties.html#parameters
    """
    ...


def parmTemplate(class_name: str, parm_name: str) -> ParmTemplate:
    """Return the parameter template object for the specified render property parameter.

    Args:
        class_name: The name of the render property class
        parm_name: The name of the parameter

    Returns:
        The ParmTemplate object for the parameter

    See https://www.sidefx.com/docs/houdini/hom/hou/properties.html#parmTemplate
    """
    ...
