# imports - standard imports
import os.path as osp
import tempfile

# imports - module imports
from ccapi.services.base    import Service
from bpyutils.util.request     import download_file
from ccapi.core.config      import Configuration
from bpyutils.log              import get_logger
from ccapi._compat          import iterkeys

logger = get_logger()
config = Configuration()

class BiGGModels(Service):
    PREFIX_URL  = "http://bigg.ucsd.edu"
    BASE_URL    = "%s/api/v2" % PREFIX_URL

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

    def download(self, model, location = ".", name = None, format_ = ".json.gz",
        **kwargs):
        url         = self._build_url(self.PREFIX_URL,
            "static", "models", "%s%s" % (model, format_), prefix = False)

        response    = self.request("GET", url = url, prefix = False)

        nchunk      = kwargs.get("nchunk", config.max_chunk_download_bytes)

        if not name:
            name    = "%s%s" % (model, format_)

        path        = osp.join(location, name)

        path        = download_file(response, path, chunk_size = nchunk)

        return path

def read_id(client, id_, **kwargs):
    bigg = BiGGModels()

    model       = None

    info        = bigg.get("model")

    found       = False

    for result in info["results"]:
        if result["bigg_id"] == id_:
            found = True
    
    if not found:
        raise ValueError("No valid BiGG Model found with id - %s" % id_)
    else:
        with tempfile.TemporaryDirectory() as dir_:
            path    = bigg.download(id_, location = dir_)
            model   = client.read(path, type = "metabolic", **kwargs)

    return model