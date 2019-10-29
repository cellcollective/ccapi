import os.path as osp

from cc.__attr__ import __version__

DEFAULT_URL                 = "https://cellcollective.org"
HEADER_AUTHENTICATION       = "X-AUTH-TOKEN"

USER_AGENT                  = "Python CCAPI / %s" % (__version__)

MAXIMUM_API_RESOURCE_FETCH  = 5

DATA_DIRECTORY              = osp.abspath(osp.join(osp.dirname(__file__), "data"))