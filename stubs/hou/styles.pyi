"""Module for managing style sheets stored with the hip file.

Style sheets are stored in JSON format in the hip file and can be saved into IFD
files by the Mantra ROP. They provide a way to apply consistent styling to rendered
output.

See https://www.sidefx.com/docs/houdini/hom/hou/styles.html
"""

from collections.abc import Sequence


def hasStyle(name: str) -> bool:
    """Check if a style with the specified name exists.

    Args:
        name: The name of the style to check

    Returns:
        True if the style exists, False otherwise

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#hasStyle
    """
    ...


def styles() -> tuple[str, ...]:
    """Return a tuple of all style names in the style manager.

    Returns:
        Tuple of style names

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#styles
    """
    ...


def description(name: str) -> str:
    """Return the description text associated with the named style.

    Args:
        name: The name of the style

    Returns:
        The description text for the style

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#description
    """
    ...


def stylesheet(name: str) -> str:
    """Return the style sheet text associated with the named style.

    Args:
        name: The name of the style

    Returns:
        The style sheet text content

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#stylesheet
    """
    ...


def errors(name: str) -> str:
    """Return error messages from parsing the named style.

    Args:
        name: The name of the style

    Returns:
        Error messages from parsing, or empty string if no errors

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#errors
    """
    ...


def addStyle(name: str, description: str, stylesheet: str) -> None:
    """Create a new named style.

    Args:
        name: The name for the new style
        description: The description text for the style
        stylesheet: The style sheet text content

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#addStyle
    """
    ...


def renameStyle(old_name: str, new_name: str) -> None:
    """Change the name of an existing style sheet.

    Args:
        old_name: The current name of the style
        new_name: The new name for the style

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#renameStyle
    """
    ...


def reorderStyles(names: Sequence[str]) -> None:
    """Change the order of style sheets defined in the hip file.

    Args:
        names: Sequence of style names in the desired order

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#reorderStyles
    """
    ...


def removeStyle(name: str) -> None:
    """Delete an existing style sheet.

    Args:
        name: The name of the style to remove

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#removeStyle
    """
    ...


def removeAll() -> None:
    """Delete all existing style sheets.

    See https://www.sidefx.com/docs/houdini/hom/hou/styles.html#removeAll
    """
    ...
