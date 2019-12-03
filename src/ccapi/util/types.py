# pylint: disable=E1101

# imports - compatibility imports
from ccapi._compat import (
    PY2,
    PYTHON_VERSION,
    _is_python_version,
    iteritems
)

# imports - standard imports
import inspect

# imports - third-party imports
from ccapi.util._dict import dict_from_list

def get_function_arguments(fn):
    # https://stackoverflow.com/a/2677263
    params  = dict()
    success = False

    if PY2:
        argspec_getter = inspect.getargspec
        success        = True
    if PYTHON_VERSION >= (3,0) and (3,4) <= PYTHON_VERSION:
        argspec_getter = inspect.getfullargspec
        success        = True

    if success:
        argspec   = argspec_getter(fn)
        params    = dict_from_list(argspec.args, argspec.defaults or [])

    if PYTHON_VERSION >= (3,5):
        signature  = inspect.signature(fn)
        parameters = signature.parameters

        params     = { k: v.default for k, v in iteritems(parameters) }

        success    = True

    if not success:
        raise ValueError("Unknown Python Version {} for fetching functional arguments.".format(sys.version))

    return params

def auto_typecast(value):
    str_to_bool = lambda x: { "True": True, "False": False, "None": None}[x]

    for type_ in (str_to_bool, int, float):
        try:
            return type_(value)
        except (KeyError, ValueError, TypeError):
            pass

    return value