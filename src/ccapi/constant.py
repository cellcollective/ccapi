# imports - standard imports
import os.path as osp

# imports - module imports
from ccapi.__attr__    import __name__
from bpyutils.util.system import pardir, makedirs
from bpyutils.util._dict  import autodict

PATH              = autodict()
PATH["BASE"]      = pardir(__file__)
PATH["DATA"]      = osp.join(PATH["BASE"], "data")
PATH["TEMPLATES"] = osp.join(PATH["DATA"], "templates")
PATH["CACHE"]     = osp.join(osp.expanduser("~"), ".%s" % __name__)

MODELS            = dict({
    "fibroblasts": dict({
        "path": osp.join(PATH["DATA"], "models", "boolean", "sbml", "fibroblasts.sbml"),
        "type": "boolean"
    }),
    "lac-operon": dict({
        "path": osp.join(PATH["DATA"], "models", "boolean", "sbml", "lac-operon.sbml"),
        "type": "boolean"
    }),
    "dehalococcoides": dict({
        "path": osp.join(PATH["DATA"], "models", "metabolic", "sbml", "dehalococcoides.sbml"),
        "type": "metabolic"
    }),
    "stm_1.0": dict({
        "path": osp.join(PATH["DATA"], "models", "metabolic", "json", "stm_1.0.json"),
        "type": "metabolic"
    })
})
makedirs(PATH["CACHE"], exist_ok = True)

URL                             = autodict()
URL["GINSIM_FILES"]             = "http://ginsim.org/sites/default/files"

MODEL_TYPE                      = dict({
    "BOOLEAN": {
        "value": "boolean"
    },
    "METABOLIC": {
        "value": "metabolic"
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

CONSTRAINT_BASED_MODEL_EXPORT_TYPE  = dict({
    "sbml": {
         "name": "SBML",
        "value": "sbml"
    },
    "json": {
         "name": "CobraPy JSON Format",
        "value": "json"
    },
    "yaml": {
         "name": "CobraPy YAML Format",
        "value": "yaml"
    },
    "matlab": {
         "name": "MATLAB",
        "value": "matlab"
    }
})