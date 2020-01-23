# imports - standard imports
import os.path as osp

# imports - module imports
from ccapi.services.base    import Service
from ccapi.util.request     import response_download
from ccapi.core.config      import Configuration
from ccapi.log              import get_logger
from ccapi._compat          import iterkeys

logger = get_logger()
config = Configuration()

class BiGGModels(Service):
    PREFIX_URL  = "http://bigg.ucsd.edu"
    BASE_URL    = "%s/api/v2" % PREFIX_URL
    
    _accepted_download_formats = dict({
        "gzip": dict({
            "extension": ".xml.gz"
        }),
        "sbml": dict({
            "extension": ".xml"
        }),
        "json": dict({
            "extension": ".json"
        }),
        "matlab": dict({
            "extension": ".mat"
        })
    })

    def __init__(self, *args, **kwargs):
        self.super = super(BiGGModels, self)
        self.super.__init__(*args, **kwargs)

    def ping(self):
        self.request("GET", url = "database_version")

    def get(self, resource, id = None):
        if   resource == "model":
            url         = self._build_url("models")

            response    = self.request("GET", url = url, prefix = False)
            json_       = response.json()

            return json_
        else:
            raise ValueError("Unknown resource type %s" % resource)

    def download(self, model, location = ".", name = None, format_ = "json",
        **kwargs):
        accepted_formats    = self._accepted_download_formats
        
        formats             = list(iterkeys(accepted_formats))

        if format_ in formats:
            extension   = accepted_formats[format_]["extension"]
            url         = self._build_url(self.PREFIX_URL,
                "static", "models", "%s%s" % (model, extension),
                prefix = False)

            response    = self.request("GET", url = url, prefix = False)

            nchunk      = kwargs.get("nchunk", config.max_chunk_download_bytes)

            if not name:
                name    = "%s%s" % (model, extension)

            path        = osp.join(location, name)

            path        = response_download(response, path, chunk_size = nchunk)

            return path
        else:
            raise ValueError("Unknown download format %s. Must be either of %s"
                % (format_, formats))