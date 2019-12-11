# imports - standard imports
import os.path as osp

# imports - module imports
from ccapi.__attr__    import __name__
from ccapi.util.system import pardir, makedirs
from ccapi.util._dict  import autodict

PATH              = autodict()
PATH["BASE"]      = pardir(__file__)
PATH["DATA"]      = osp.join(PATH["BASE"], "data")
PATH["TEMPLATES"] = osp.join(PATH["DATA"], "templates")
PATH["CACHE"]     = osp.join(osp.expanduser("~"), ".%s" % __name__)
PATH["MODELS"]    = dict({
    "fibroblasts": osp.join(PATH["DATA"], "models", "boolean", "sbml", "fibroblasts.sbml"),
     "lac-operon": osp.join(PATH["DATA"], "models", "boolean", "sbml", "lac-operon.sbml") 
})
makedirs(PATH["CACHE"], exist_ok = True)

URL                             = autodict()
URL["GINSIM_FILES"]             = "http://ginsim.org/sites/default/files"

MODEL_TYPE                      = dict({
    "BOOLEAN": {
        "value": "boolean"
    }
})
MODEL_DOMAIN_TYPE               = dict({
    "RESEARCH": {
        "value": "research"
    },
    "LEARN": {
        "value": "learn",
        "value_api": "learning",
    },
    "TEACH": {
        "value": "teach",
        "value_api": "teaching"
    }
})
AUTHENTICATION_HEADER           = "X-AUTH-TOKEN"
_AUTHENTICATION_ERROR_STRING    = "Unable to login into Cell Collective with credentials provided."

BOOLEAN_MODEL_EXPORT_TYPE       = dict({
    "sbml": {
        "name": "SBML",
        "value_api": "SBML"
    },
    "tt": {
        "name": "Truth Tables",
        "value_api": "TT"
    },
    "expr": {
        "name": "Boolean Expressions",
        "value_api": "EXPR"
    },
    "matrix": {
        "name": "Interaction Matrix",
        "value_api": "MATRIX"
    },
    "gml": {
        "name": "GML",
        "value_api": "GML"
    }
})