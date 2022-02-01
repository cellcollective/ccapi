from bpyutils.util.environ import getenv as bpy_getenv

from ccapi.__attr__ import __name__

NAME = __name__.upper()

def getenv(*args, **kwargs):
    return bpy_getenv(*args, **kwargs, prefix = NAME)