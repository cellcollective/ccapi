# imports - compatibility imports
from ccapi._compat import _is_python_version

# imports - standard imports
import itertools

def sequencify(value, type_ = list):
    if not isinstance(value, (list, tuple)):
        value = list([value])

    value = type_(value)
  
    return value

def squash(seq):
    value = seq

    if isinstance(value, (list, tuple)) and len(value) == 1:
        value = value[0]
    
    return value

def flatten(arr):
    if _is_python_version(major = 2, minor = 6):
        chainer = itertools.chain.from_iterable
    else:
        chainer = itertools.chain

    flattened = list(chainer(*arr))

    return flattened

def find(arr, kind, default = None, raise_err = False):
    obj = kind

    if not callable(kind):
        kind = lambda x: x == obj
    
    found = list(filter(kind, arr))

    if not found:
        if raise_err:
            raise ValueError("%s not found in array." % obj)
        else:
            found = default
    else:
        found = squash(found)

    return found

    