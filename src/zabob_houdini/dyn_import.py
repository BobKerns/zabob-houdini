'''
Dynamic/deferred loading of imports referenced at runtime.

Usage:
    from zabob_houdini.dyn_import import dyn_import as __dynamic__
    __dynamic__ = __dynamic__(globals())

    # Import specific symbols from submodules
    __dynamic__._def('zabob_houdini.core_node', 'ForwardReference', 'ForwardReference', 'NodeInstance', 'NodeInstance')

    # Import with alias
    __dynamic__._def('zabob_houdini.core_node', 'NodeInstance', 'NI')

    # Import entire module
    __dynamic__._def('zabob_houdini.core_node', None, 'cn')

    # Star imports are NOT transformed:
    # from module import *  # Left as-is, not amenable to dynamic import
    #
    # Star imports remain as regular imports because transforming them would require
    # rewriting every global variable access as a potential import lookup, which is
    # impractical. Star imports are primarily for interactive use.

    # Later at runtime, symbols/modules load on first access:
    ref = __dynamic__.load('ForwardReference', locals())  # Triggers import
    node = cn.NodeInstance(...)  # Triggers import via __getattr__
'''

from typing import Any
from collections.abc import Callable
import importlib


class _SymbolMap(dict[str, Callable[[], Any]]):
    """Dict subclass that allows setting attributes (like _Ref)."""
    _caller_globals: dict[str, Any]

    def __init__(self, caller_globals: dict[str, Any]) -> None:
        super().__init__()
        self._caller_globals = caller_globals

    def _def_module(self, module: str, dest_variable: str) -> None:
        """
        Register a module import.

        Args:
            module: Module name to import
            dest_variable: Name to assign the imported module to
        """

        def get_module() -> Any:
            return importlib.import_module(module)

        self[dest_variable] = get_module

    def _def(self, module: str, *args: str) -> None:
        """
        Register import definitions.

        Takes module name followed by from/to pairs.
        from is the symbol to import, and to the name to assign it to.

        Args:
            module: Module name to import from
            *args: Pairs of (from_name, to_name)
        """

        if len(args) % 2 != 0:
            raise ValueError(f"_def requires arguments in pairs after module, got {len(args)}")

        for i in range(0, len(args), 2):
            src_variable = args[i]
            dest_variable = args[i + 1]

            if not isinstance(dest_variable, str):
                raise ValueError(f"Destination name must be string, got {type(dest_variable)}")

            # from module import src_variable [as dest_variable]
            def make_symbol_getter(mod_path: str, sym: str):
                def get_symbol() -> Any:
                    mod = importlib.import_module(mod_path)
                    return getattr(mod, sym)
                return get_symbol
            self[dest_variable] = make_symbol_getter(module, src_variable)

    def load(self, name: str, local_vars: dict[str, Any] | None = None) -> Any:
        """
        Explicitly load a dynamically imported symbol.

        Checks locals first for shadowing, then loads via symbol map.

        Args:
            name: The name of the symbol to load
            local_vars: locals() from calling scope (optional)

        Returns:
            The loaded symbol

        Raises:
            KeyError: If the symbol is not registered for dynamic import
        """

        # Check locals first - handles shadowing
        if local_vars is not None and name in local_vars:
            return local_vars[name]

        # Already loaded in globals?
        if name in self._caller_globals:
            return self._caller_globals[name]

        # Load from symbol map
        if name in self:
            getter = self[name]
            result = getter()
            self._caller_globals[name] = result
            return result

        raise KeyError(f"Symbol '{name}' is not registered for dynamic import")


def dyn_import(caller_globals: dict[str, Any]) -> _SymbolMap:
    """
    Initialize dynamic import system for a module.

    Creates a symbol map, installs __getattr__ hook into caller's globals,
    and returns the map with _def method for registering imports.

    Args:
        caller_globals: The globals() dict of the calling module

    Returns:
        The symbol map with _def method for registering imports
    """

    # Map to store deferred imports (subclass allows setting attributes)
    symbol_map: _SymbolMap = _SymbolMap(caller_globals)

    existing_getattr = caller_globals.get('__getattr__')

    def custom_getattr(attr_name: str) -> Any:
        """Custom __getattr__ that resolves deferred imports."""
        # Special module attributes should be looked up in globals, not dynamic imports
        # These are set by Python's import system and should pass through
        if attr_name.startswith('__') and attr_name.endswith('__'):
            # Check if it's already in globals (set by import system)
            if attr_name in caller_globals:
                return caller_globals[attr_name]
            # If not found, let it raise AttributeError so import system handles it
            if existing_getattr is not None:
                return existing_getattr(attr_name)
            raise AttributeError(f"module has no attribute '{attr_name}'")

        if attr_name in symbol_map:
            getter = symbol_map[attr_name]
            result = getter()
            caller_globals[attr_name] = result
            return result

        if existing_getattr is not None:
            return existing_getattr(attr_name)

        raise NameError(f"name '{attr_name}' is not defined")

    # Install hook into caller's globals
    caller_globals['__getattr__'] = custom_getattr

    return symbol_map
