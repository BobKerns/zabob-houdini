'''

Dynamic/deferred loading of imports referenced at runtime.

Usage:
    from zabob_loader.dyn_import import dyn_import as __dynamic__
    __dynamic__ = __dynamic__(globals())

    # Import specific symbols from submodules
    __dynamic__._def('zabob_houdini.core_node', 'ZNodeForwardRef', 'ZNodeForwardRef', 'ZNode', 'ZNode')

    # Import with alias
    __dynamic__._def('zabob_houdini.core_node', 'ZNode', 'NI')

    # Import entire module
    __dynamic__._def('zabob_houdini.core_node', None, 'cn')

    # Star imports are NOT transformed:
    # from module import *  # Left as-is, not amenable to dynamic import
    #
    # Star imports remain as regular imports because transforming them would require
    # rewriting every global variable access as a potential import lookup, which is
    # impractical. Star imports are primarily for interactive use.

    # Later at runtime, symbols/modules load on first access:
    ref = __dynamic__.load('ZNodeForwardRef', locals())  # Triggers import
    node = cn.ZNode(...)  # Triggers import via __getattr__
'''

from zabob_loader.dyn_loader import (
    DynamicImportTransformer, do_transform, transform_script,
    DynamicImportLoader, DynamicImportFinder, install_import_hook,
)

from zabob_loader.dyn_import import (
    _SymbolMap, dyn_import,
)

__all__ = (
    '_SymbolMap', 'dyn_import',
    'DynamicImportTransformer', 'do_transform', 'transform_script',
    'DynamicImportLoader', 'DynamicImportFinder', 'install_import_hook',
)
