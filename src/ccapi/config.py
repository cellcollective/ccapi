# imports - standard imports
import os.path as osp

# imports - module imports
from ccapi.__attr__    import __name__, __version__
from ccapi.util.system import pardir, makedirs
from ccapi.util._dict  import autodict
from ccapi.constant    import MODEL_TYPE, MODEL_DOMAIN_TYPE

PATH              = autodict()
PATH["BASE"]      = pardir(__file__)
PATH["DATA"]      = osp.join(PATH["BASE"], "data")
PATH["TEMPLATES"] = osp.join(PATH["DATA"], "templates")
PATH["CACHE"]     = osp.join(osp.expanduser("~"), ".%s" % __name__)

makedirs(PATH["CACHE"], exist_ok = True)

DEFAULT                             = autodict()
DEFAULT["URL"]                      = "https://cellcollective.org"
DEFAULT["USER_AGENT"]               = "Python CCAPI / %s" % (__version__)
DEFAULT["MODEL_TYPE"]               = MODEL_TYPE["BOOLEAN"]
DEFAULT["MODEL_NAME"]               = "Unnamed Model"
DEFAULT["MODEL_DOMAIN_TYPE"]        = MODEL_DOMAIN_TYPE["RESEARCH"]

DEFAULT["MAX_API_RESOURCE_FETCH"]   = 5
DEFAULT["MAX_CHUNK_DOWNLOAD_BYTES"] = 1024

DEFAULT["DISPLAY_MAX_ROWS"]         = 15
DEFAULT["DISPLAY_MAX_COLS"]         = 20