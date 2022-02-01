# imports - module imports
from ccapi.__attr__         import __name__ as NAME, __version__
from ccapi.constant         import MODEL_TYPE, MODEL_DOMAIN_TYPE
from ccapi.core.singleton   import Singleton
from ccapi.core.mixins      import JupyterHTMLViewMixin
from bpyutils.util.environ     import getenv

# imports - standard imports
import logging

class Configuration(JupyterHTMLViewMixin, metaclass = Singleton):
    def __init__(self, *args, **kwargs):
        self.url                         = getenv("URL", "https://cellcollective.org")

        self.user_agent                  = "Python CCAPI / %s" % (__version__)
        
        self.model_type                  = MODEL_TYPE["BOOLEAN"]
        self.model_name                  = "Unnamed Model"
        self.model_domain_type           = MODEL_DOMAIN_TYPE["RESEARCH"]

        self.max_api_resource_fetch      = 5
        self.max_chunk_download_bytes    = 1024

        self.display_max_rows            = 15
        self.display_max_cols            = 20

        self.ginsim_version              = "2.4"
        
        self._verbose                    = False

    @property
    def verbose(self):
        return getattr(self, "_verbose", True)

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

        logger = logging.getLogger(NAME)

        if value:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)