import os.path as osp

from cc.__attr__ import __version__

MODEL_TYPE                      = dict({
    "BOOLEAN": {
        "value": "boolean"
    }
})
MODEL_DOMAIN_TYPE               = dict({
    "RESEARCH": {
        "value": "research"
    }
})
HEADER_AUTHENTICATION           = "X-AUTH-TOKEN"

DEFAULT_URL                     = "https://cellcollective.org"

USER_AGENT                      = "Python CCAPI / %s" % (__version__)

MAXIMUM_API_RESOURCE_FETCH      = 5

MODEL_EXPORT_TYPE_MAP           = dict({
    "sbml": "SBML"
})

_AUTHENTICATION_ERROR_STRING    = "Unable to login into Cell Collective with credentials provided."