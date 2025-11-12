'''
Extract useful information about the Houdini environment.
'''

import builtins
from collections import defaultdict
from collections.abc import Callable, Hashable, MutableMapping
from dataclasses import dataclass
from enum import Enum
from typing import Any, NotRequired, TypeAlias, TypeVar, TypedDict
from weakref import WeakKeyDictionary
import click
import hou

from zabob_houdini.houdini_bridge import JsonValue

JsonData: TypeAlias = JsonValue
'''
A JSON-serializable data type, which can be a string, number, boolean, null, array, or object.
This type is used for any data that can be returned from Houdini functions and sent to the
'''

@dataclass
class AnalysisDBItem:
    """
    Base class for items to be written to the analysis database.
    """
    pass

@dataclass
class NodeCategoryInfo(AnalysisDBItem):
    """
    Data class to hold information about a Houdini node category.
    """
    name: str
    label: str
    hasSubnetworkType: bool


@dataclass
class NodeTypeInfo(AnalysisDBItem):
    """
    Data class to hold information about a Houdini node type.
    """
    name: str
    category: str
    childCategory: str|None
    description: str
    helpUrl: str
    minNumInputs: int
    maxNumInputs: int
    maxNumOutputs: int
    isGenerator: bool
    isManager: bool
    isDeprecated: bool
    deprecation_reason: str|None
    deprecation_new_type: str|None
    deprecation_version: str|None


@dataclass
class ParmTemplateInfo(AnalysisDBItem):
    """
    Data class to hold information about a Houdini parameter template.
    """
    node_type_name: str
    node_type_category: str
    name: str
    type: builtins.type
    template_type: str
    defaultValue: JsonData
    label: str
    help: str
    script: str
    script_language: str
    tags: dict[str, str]


class ParameterSpec(TypedDict):
    """
    TypedDict for representing a function parameter specification.
    Used in function signature information embedded in JSON.

    Only the 'name', 'type', and 'kind' fields are required.
    Other fields are present only when applicable.
    """
    name: str  # Always present
    type: str  # Always present
    kind: str  # Always present - POSITIONAL_ONLY, POSITIONAL_OR_KEYWORD, VAR_POSITIONAL, KEYWORD_ONLY, VAR_KEYWORD
    is_optional: NotRequired[bool]  # Present only when parameter can be omitted
    default: NotRequired[JsonData]  # Present only when parameter has a default value

def analyze_categories():
    """
    Analyze node categories in the current Houdini session.
    Returns a dictionary mapping category names to their node types.

    Yields NodeCategoryInfo and NodeTypeInfo objects for each category and node type.

    This function iterates through all node type categories in Houdini,
    extracting information about each category and its node types.
    It yields NodeCategoryInfo for each category and NodeTypeInfo for each node type,
    including details such as the node type's name, category, child category, description,
    and parameters.

    Yields:
        NodeCategoryInfo: Information about each node category.
        NodeTypeInfo: Information about each node type within the categories.
        ParamTemplateInfo: Information about parameters of each node type.
    """
    yield from (item
            for name, category in hou.nodeTypeCategories().items()
            for item in _category_info(name, category)
    )


def _category_info(name: str, category: hou.NodeTypeCategory):
    """
    Extract information from a Houdini NodeTypeCategory.
    Returns a dictionary with category name and node types.

    Args:
        name (str): The name of the node type category.
        category (hou.NodeTypeCategory): The Houdini node type category to extract information from.
    Yields:
        NodeCategoryInfo: Information about the node category, including its name.
        NodeTypeInfo: Information about each node type within the category.
    """
    try:
        hasSubNetworkType = category.hasSubNetworkType()
    except hou.OperationFailed:
        # If the category does not support subnetwork types, we assume it does not have one.
        hasSubNetworkType = False
    yield NodeCategoryInfo(
        name=name,
        label=category.label(),
        hasSubnetworkType=hasSubNetworkType,
    )
    yield from (
        item
        for name, node_type in category.nodeTypes().items()
        for item in _node_type_info(name, node_type)
    )

def _node_type_info(name: str, node_type: hou.NodeType):
    """
    Extract information from a Houdini NodeType.
    Yields a NodeTypeInfo object with the node type name and category.
    Yields information about the node type's parameters.

    Args:
        name (str): The name of the node type.
        node_type (hou.NodeType): The Houdini node type to extract information from.
    Yields:
        NodeTypeInfo: Information about the node type, including its name, category, child category, description, and parameters.
        ParmTemplateInfo: Information about parameters of the node type.
    """
    if name == "bend" and node_type.category().name() == "Cop":
        return
    deprecationInfo: dict[str, Any] = node_type.deprecationInfo()
    yield NodeTypeInfo(
        name=name,
        category=node_type.category().name(),
        childCategory=node_type.childTypeCategory().name() if node_type.childTypeCategory() else None,
        description=node_type.description(),
        helpUrl=node_type.helpUrl(),
        minNumInputs=node_type.minNumInputs(),
        maxNumInputs=node_type.maxNumInputs(),
        maxNumOutputs=node_type.maxNumOutputs(),
        isGenerator=node_type.isGenerator(),
        isManager=node_type.isManager(),
        isDeprecated=node_type.deprecated(), # type: ignore
        deprecation_reason=deprecationInfo.get('reason', None),
        deprecation_new_type=none_or(deprecationInfo.get('new_type', None), get_name),
        deprecation_version=deprecationInfo.get('version', None),
    )
    yield from (
        item
        for param in node_type.parmTemplates()
        for item in _parm_template_info(node_type, param)
    )


def _parm_template_info(node_type: hou.NodeType, parm: hou.ParmTemplate):
    """
    Extract information from a Houdini ParmTemplate.
    Yields a ParmTemplateInfo object with the parameter's type, name, label, and documentation.

    Args:
        node_type (hou.NodeType): The Houdini node type containing the parameter.
        param (hou.ParmTemplate): The parameter template to extract information from.
    Yields:
        ParmTemplateInfo: Information about the parameter template, including its type, name, label, and documentation.
    """
    def default_value(parm: hou.ParmTemplate) -> Any|None:
        """
        Get the default value of the parameter.
        Returns None if the parameter has no default value.
        """
        return parm.defaultValue() if hasattr(parm, 'defaultValue') else None # type: ignore
    yield ParmTemplateInfo(
        node_type_name=node_type.name(),
        node_type_category=node_type.category().name(),
        name=parm.name(),
        type=type(parm),
        template_type=str(parm.type()),
        defaultValue=default_value(parm),
        label=parm.label(),
        help=parm.help(),
        script=parm.scriptCallback(),
        script_language=get_name(parm.scriptCallbackLanguage()),
        tags=parm.tags()
    )


T = TypeVar('T')
R = TypeVar('R')
def none_or(value: T|None, fn: Callable[[T], R]) -> R|None:
    """
    Call a function with the given value if it is not `None`,
    otherwise return `None`.

    Args:
        value (T|None): The value to pass to the function.
        Callable[T]: The function to call with the value.

    Returns:
        R|None: The result of the function call or None if value is None.
    """
    if value is None:
        return None
    return fn(value)


_name_counter: MutableMapping[str, int] = defaultdict[str, int](lambda: 0)
_names: MutableMapping[Any, str] = WeakKeyDictionary[Any, str]()
def get_name(d: Any) -> str:
    '''
    Get the name of the given object. If it does not have a name,
    one will be assigned.

    If the object has a `name` or `__name__` attribute, it will
    be used as the name.

    If the object has a method called `name`, `getName`,
    or `get_name`, it will be called to try to get the name.

    Args:
        d (Any): The object to get the name of.
    Returns:
        str: The name of the object.
    '''
    match d:
        case Enum():
            return str(d.name)
        case str() | int() | float() | complex() | bool():
            return str(d)
        case None:
            return "None"
        case Exception():
            # If the object is an Exception, return its class name.
            return d.__class__.__name__
        case _ if hasattr(d, '__name__'):
            return str(d.__name__)
        case _ if hasattr(d, 'name') and isinstance(d.name, str):
            # If the object has a name attribute that is a string, return it.
            return str(d.name)
        case _ if hasattr(d, 'name') and callable(d.name):
            try:
                return str(d.name())
            except Exception:
                pass
        case _ if hasattr(d, 'get_name') and callable(d.get_name):
            try:
                return str(d.get_name())
            except Exception:
                pass
        case _ if hasattr(d, 'getName') and callable(d.getName):
            try:
                return str(d.get_name())
            except Exception:
                pass
        case _ if hasattr(d, 'name'):
            return str(d.name)
        case d if isinstance(d, Hashable):
            n = _names.get(d, None)
            if n is not None:
                return n
            pass
        case _:
            pass
    # If we reach here, we don't have a name, so generate one.
    typename = get_name(type(d))
    _name_counter[typename] += 1
    c = _name_counter[typename]
    n = f"{typename}_{c}"
    try:
        # If the object has a __name__ attribute, set it to the generated name.
        # This is useful for debugging and logging.
        setattr(d, '__name__', n)
        return n
    except AttributeError:
        match d:
            case _ if isinstance(d, Hashable):
                # If the object is hashable, store the name in a weak dictionary.
                try:
                    _names[d] = n
                    return n
                except TypeError:
                    pass
        # If we can't save the name, generate one based on the id.
        return f"{typename}_{id(d):x}"


@click.group("info")
def info():
    """
    Commands for extracting information about the Houdini environment.
    """
    pass


@info.command('categories')
@click.argument('categories', nargs=-1, type=str)
def categories(categories):
    """
    Analyze node categories in the current Houdini session and print the results.
    """
    for item in analyze_categories():
        if isinstance(item, NodeCategoryInfo):
            click.echo(f"Category: {item.name} (Label: {item.label}, Has Subnetwork Type: {item.hasSubnetworkType})")

