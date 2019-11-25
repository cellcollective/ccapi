# imports - compatibility imports
from cc._compat import _is_python_version

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