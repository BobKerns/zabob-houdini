"""Dynamic import configuration for zabob_houdini package.

This file configures which imports get transformed by the dynamic import system.
By default, only zabob_houdini.* imports are transformed to support circular
dependency resolution while avoiding debugger stepping issues with external libraries.
"""

patterns = {
    'include': ['zabob_houdini.*', 'zabob_houdini'],
    'exclude': []
}
