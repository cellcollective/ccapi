# imports - standard imports
import sys
import random

def get_temporary_id():
    id_ = random.randint(-sys.maxint, 0)
    return id_