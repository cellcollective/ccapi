import os.path as osp

from cc.__attr__ import __version__

DEFAULT_URL                 = "https://cellcollective.org"
HEADER_AUTHENTICATION       = "X-AUTH-TOKEN"

USER_AGENT                  = "Python CCAPI / %s" % (__version__)

MAXIMUM_API_RESOURCE_FETCH  = 5

_BASE_DIRECTORY             = osp.abspath(osp.dirname(__file__))
DATA_DIRECTORY              = osp.join(_BASE_DIRECTORY, "data")
TEMPLATES_DIRECTORY         = osp.join(DATA_DIRECTORY, "templates")