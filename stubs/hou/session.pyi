"""Session module for user-defined code (hou.session).

This module is used to define custom classes, functions and variables that can
be called from within the current Houdini session. The contents of this module
are saved into the .hip file.

You can add your own custom definitions to this module and refer to them
anywhere python is used in Houdini. This includes shelf tools, parameter fields,
callback scripts and the Python Shell pane. For example, if you write a `fooBar`
method in the module, you can invoke it from your python code with
`hou.session.fooBar()`.

To view and edit the contents of this module, choose Windows ▸ Python Source
Editor. You can also read and write the module contents from HOM using:
- hou.sessionModuleSource() - to read the source code
- hou.setSessionModuleSource() - to set the source code
- hou.appendSessionModuleSource() - to append to the source code

Note: This is a dynamic module. Users add their own content at runtime.
The stub provides the structure but not the user's custom definitions.
"""

# This module is intentionally empty in the stub
# Users populate it with their own custom classes, functions, and variables
# which are saved in the .hip file and persist across sessions
