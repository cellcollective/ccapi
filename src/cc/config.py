# imports - standard imports
import os.path as osp

# imports - module imports
from cc.util.system import pardir
from cc.util.types  import autodict

PATH              = autodict()
PATH["BASE"]      = pardir(__file__)
PATH["DATA"]      = osp.join(PATH["BASE"], "data")
PATH["TEMPLATES"] = osp.join(PATH["DATA"], "templates") 