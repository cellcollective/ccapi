# imports - standard imports
import sys
import random
import re

# imports - module imports
from bpyutils.util.string  import lower
from bpyutils.limits       import MAX_UNSIGNED_SHORT

def get_temporary_id():
    id_ = random.randint(-MAX_UNSIGNED_SHORT, 0)
    return id_

def slugify_name(name):
    name = lower(name)

    name = name.replace("-", "").replace(" ", "-")
    name = re.sub(r"^[^a-zA-Z0-9-]", "", name)

    return name