# imports - standard imports
import sys
import random

# imports - module imports
from ccapi.limits import MAX_UNSIGNED_SHORT

def get_temporary_id():
    id_ = random.randint(-MAX_UNSIGNED_SHORT, 0)
    return id_