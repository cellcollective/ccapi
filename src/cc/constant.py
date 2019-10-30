import os.path as osp

from cc.__attr__ import __version__

DEFAULT_URL                     = "https://cellcollective.org"
HEADER_AUTHENTICATION           = "X-AUTH-TOKEN"

USER_AGENT                      = "Python CCAPI / %s" % (__version__)

MAXIMUM_API_RESOURCE_FETCH      = 5

MODEL_EXPORT_TYPE_MAP           = dict({
    "sbml": "SBML"
})

_AUTHENTICATION_ERROR_STRING    = "Unable to login into Cell Collective with credentials provided."