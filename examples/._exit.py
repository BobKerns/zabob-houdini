#!/usr/bin/env python3
"""Internal utility: Force-quit hython debugger sessions.

This is NOT an example file. Do not use this as a reference for how to write
Zabob-Houdini code. It exists solely to provide a quick exit mechanism when
debugging, bypassing Houdini's normal shutdown process.
"""

import os

os._exit(0)
