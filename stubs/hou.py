'''
This file exists so pylance and other tools have something that satisfies

>  import hou

in the codebase. The type signatures are supplied by the accompanying
hou.pyi file, rather than Houdini's own, which is auto-generated
and often incorrect or incomplete.
'''

raise ImportError("This is a stub file for type checking only.\n"
                  "If you see this, you should be using hython instead of "
                  "regular python, as the hou module is Houdini-only."
                  )
