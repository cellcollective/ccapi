# imports - module imports
from ccapi.__attr__         import __version__
from ccapi.constant         import MODEL_TYPE, MODEL_DOMAIN_TYPE
from ccapi.core.singleton   import Singleton
from ccapi.core.mixins      import JupyterHTMLViewMixin

class Configuration(JupyterHTMLViewMixin, metaclass = Singleton):
    def __init__(self, *args, **kwargs):
        self.url                         = "https://cellcollective.org"

        self.user_agent                  = "Python CCAPI / %s" % (__version__)
        
        self.model_type                  = MODEL_TYPE["BOOLEAN"]
        self.model_name                  = "Unnamed Model"
        self.model_domain_type           = MODEL_DOMAIN_TYPE["RESEARCH"]

        self.max_api_resource_fetch      = 5
        self.max_chunk_download_bytes    = 1024

        self.display_max_rows            = 15
        self.display_max_cols            = 20

        self.ginsim_version              = "2.4"