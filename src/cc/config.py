# imports - standard imports
import os.path as osp

# imports - module imports
from cc.__attr__    import __version__
from cc.util.system import pardir
from cc.util._dict  import autodict
from cc.constant    import MODEL_TYPE, MODEL_DOMAIN_TYPE

PATH              = autodict()
PATH["BASE"]      = pardir(__file__)
PATH["DATA"]      = osp.join(PATH["BASE"], "data")
PATH["TEMPLATES"] = osp.join(PATH["DATA"], "templates")

DEFAULT                             = autodict()
DEFAULT["URL"]                      = "https://cellcollective.org"
DEFAULT["USER_AGENT"]               = "Python CCAPI / %s" % (__version__)
DEFAULT["MODEL_TYPE"]               = MODEL_TYPE["BOOLEAN"]
DEFAULT["MODEL_NAME"]               = "Unnamed Model"
DEFAULT["MODEL_DOMAIN_TYPE"]        = MODEL_DOMAIN_TYPE["RESEARCH"]

DEFAULT["MAX_API_RESOURCE_FETCH"]   = 5