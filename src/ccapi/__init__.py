
from __future__ import absolute_import


try:
    import os

    if os.environ.get("CCAPI_GEVENT_PATCH"):
        from gevent import monkey
        monkey.patch_all(threaded = True, select = False)
except ImportError:
    pass

# imports - module imports
from ccapi.__attr__ import (
    __name__,
    __version__,
    __build__,

    __description__,

    __author__
)
from ccapi.config      import PATH
from ccapi.__main__    import main

from bpyutils.cache       import Cache
from bpyutils.config      import Settings
from bpyutils.util.jobs   import run_all as run_all_jobs, run_job

cache = Cache(dirname = __name__)
cache.create()

settings = Settings()

def get_version_str():
    version = "%s%s" % (__version__, " (%s)" % __build__ if __build__ else "")
    return version

# imports - module imports
from ccapi.__attr__     import (
    __name__,
    __version__,
    __author__
)
from ccapi.api          import Client
from ccapi.constant     import MODELS
from ccapi.model        import *
from ccapi._compat      import iterkeys

def load_model(name, *args, **kwargs):
    """
    Read a sample model.

    :param name: Name of the model (Can be obtained by list(ccapi.constant.MODELS)).
    :param client: Custom client object.
    """
    if not name in iterkeys(MODELS):
        raise ValueError("Model %s not found." % name)
    else:
        model = MODELS[name]

    client = kwargs.get("client", Client())
    model  = client.read(model["path"], type = model["type"])

    return model