# imports - standard imports
import os.path as osp

# imports - module imports
from cc.util.system import pardir
from cc.util.types  import autodict
from cc.constant    import MODEL_TYPE, MODEL_DOMAIN_TYPE

PATH                    = autodict()
PATH["BASE"]            = pardir(__file__)
PATH["DATA"]            = osp.join(PATH["BASE"], "data")
PATH["TEMPLATES"]       = osp.join(PATH["DATA"], "templates")

DEFAULT                         = autodict()
DEFAULT["URL"]                  = "https://cellcollective.org"
DEFAULT["MODEL_TYPE"]           = MODEL_TYPE["BOOLEAN"]
DEFAULT["MODEL_NAME"]           = "Unnamed Model"
DEFAULT["MODEL_DOMAIN_TYPE"]    = MODEL_DOMAIN_TYPE["RESEARCH"]