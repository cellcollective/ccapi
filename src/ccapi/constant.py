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