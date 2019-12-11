# imports - standard imports
import os.path as osp

# imports - module imports
from ccapi.__attr__    import __version__
from ccapi.util._dict  import autodict
from ccapi.constant    import MODEL_TYPE, MODEL_DOMAIN_TYPE

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

DEFAULT["GINSIM_VERSION"]           = "2.4"